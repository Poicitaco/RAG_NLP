"""
Quản lý vector store cho hệ thống RAG.
"""
from typing import List, Dict, Any, Optional, Tuple, Iterable
from abc import ABC, abstractmethod
import chromadb
from chromadb.config import Settings as ChromaSettings
from pathlib import Path
import uuid
import re
import unicodedata
from backend.config import settings
from backend.utils import app_logger


CARDIAC_SPECIALTY_TERMS = {
    "milrinone",
    "milrinon",
    "lidocain",
    "lidocaine",
    "digoxin",
    "amiodaron",
    "amiodarone",
    "dobutamin",
    "dobutamine",
    "dopamin",
    "dopamine",
    "norepinephrin",
    "norepinephrine",
    "epinephrin",
    "epinephrine",
    "procainamid",
    "procainamide",
    "disopyramid",
    "disopyramide",
    "mexiletin",
    "mexiletine",
    "propafenon",
    "propafenone",
    "flecainid",
    "flecainide",
    "verapamil",
    "ivabradin",
    "ivabradine",
}

CARDIAC_SECTION_TERMS = {
    "he tim mach",
    "thuoc dieu tri tim",
    "chong loan nhip",
    "kich thich tim",
    "gian mach dung trong benh tim",
    "thuoc tim mach",
}


def _normalize_text(text: str) -> str:
    value = (text or "").replace("Đ", "D").replace("đ", "d").lower()
    decomposed = unicodedata.normalize("NFD", value)
    stripped = "".join(ch for ch in decomposed if unicodedata.category(ch) != "Mn")
    return re.sub(r"\s+", " ", stripped).strip()


def _contains_any(text: str, terms: Iterable[str]) -> bool:
    normalized = _normalize_text(text)
    return any(_normalize_text(term) in normalized for term in terms if term)


def _build_runtime_where(filter_dict: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    if not filter_dict:
        return None
    if any(key.startswith("$") for key in filter_dict):
        return filter_dict

    must_avoid_sections = list(
        filter_dict.get("must_avoid_sections")
        or filter_dict.get("must_avoid_sections_in_rag")
        or []
    )
    target_group = filter_dict.get("target_otc_group") or filter_dict.get("target_group")
    passthrough = {
        key: value
        for key, value in filter_dict.items()
        if key not in {"must_avoid_sections", "must_avoid_sections_in_rag", "target_otc_group", "target_group"}
    }

    conditions: List[Dict[str, Any]] = []
    if must_avoid_sections:
        conditions.append({"section": {"$nin": must_avoid_sections}})
    if target_group:
        conditions.append({"otc_category": {"$eq": target_group}})
    conditions.extend({key: {"$eq": value}} for key, value in passthrough.items())

    if not conditions:
        return None
    if len(conditions) == 1:
        return conditions[0]
    return {"$and": conditions}


def _passes_runtime_filter(
    document: str,
    metadata: Dict[str, Any],
    filter_dict: Optional[Dict[str, Any]],
) -> bool:
    if not filter_dict:
        return True

    must_avoid_sections = list(
        filter_dict.get("must_avoid_sections")
        or filter_dict.get("must_avoid_sections_in_rag")
        or []
    )
    section_text = " ".join(
        str(metadata.get(field) or "")
        for field in ("section", "section_title", "type", "slug")
    )
    haystack = " ".join(
        str(value)
        for value in [
            document,
            metadata.get("title"),
            metadata.get("drug_name"),
            metadata.get("active_ingredient"),
            metadata.get("active_ingredients"),
            section_text,
        ]
        if value
    )
    if must_avoid_sections and _contains_any(section_text + " " + haystack, must_avoid_sections):
        return False

    target_group = filter_dict.get("target_otc_group") or filter_dict.get("target_group")
    if target_group:
        target = _normalize_text(str(target_group))
        category = _normalize_text(
            str(metadata.get("target_group") or metadata.get("otc_category") or "")
        )
        if category and category != target:
            return False
        if target == "zinc_supplement":
            if _contains_any(haystack, CARDIAC_SPECIALTY_TERMS):
                return False
            if _contains_any(section_text, CARDIAC_SECTION_TERMS):
                return False

    return True


class VectorStore(ABC):
    """Lớp abstract base cho vector stores"""
    
    @abstractmethod
    async def add_documents(
        self,
        documents: List[str],
        metadatas: List[Dict[str, Any]],
        ids: Optional[List[str]] = None
    ) -> List[str]:
        """Thêm documents vào vector store"""
        pass
    
    @abstractmethod
    async def search(
        self,
        query_embedding: List[float],
        top_k: int = 5,
        filter_dict: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Tìm kiếm documents tương tự"""
        pass
    
    @abstractmethod
    async def delete_documents(self, ids: List[str]) -> bool:
        """Xóa documents khỏi vector store"""
        pass
    
    @abstractmethod
    async def get_document(self, doc_id: str) -> Optional[Dict[str, Any]]:
        """Lấy một document cụ thể theo ID"""
        pass


class ChromaVectorStore(VectorStore):
    """Triển khai ChromaDB vector store"""
    
    def __init__(
        self,
        collection_name: Optional[str] = None,
        persist_directory: Optional[str] = None
    ):
        """
        Khởi tạo ChromaDB vector store
        
        Args:
            collection_name: Tên của collection
            persist_directory: Thư mục lưu trữ dữ liệu
        """
        self.collection_name = collection_name or settings.LOCAL_CHROMA_COLLECTION
        self.persist_directory = persist_directory or settings.CHROMA_PERSIST_DIR
        
        # Đảm bảo thư mục tồn tại
        Path(self.persist_directory).mkdir(parents=True, exist_ok=True)
        
        # Khởi tạo ChromaDB client
        self.client = chromadb.Client(ChromaSettings(
            chroma_db_impl="duckdb+parquet",
            persist_directory=self.persist_directory
        ))
        
        # Lấy hoặc tạo collection
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            metadata={
                "description": "Pharmaceutical knowledge base embedded with local BAAI/bge-m3",
                "embedding_provider": "sentence-transformers",
                "embedding_model": settings.LOCAL_EMBEDDING_MODEL,
                "embedding_dimension": settings.LOCAL_EMBEDDING_DIMENSION,
            }
        )
        if self.collection.count() == 0:
            app_logger.warning(
                f"Chroma collection '{self.collection_name}' is empty. Re-index the RAG corpus with "
                "local BAAI/bge-m3 embeddings before relying on vector retrieval."
            )
        
        app_logger.info(
            f"Initialized ChromaDB vector store: {self.collection_name} "
            f"at {self.persist_directory}"
        )
    
    async def add_documents(
        self,
        documents: List[str],
        metadatas: List[Dict[str, Any]],
        ids: Optional[List[str]] = None,
        embeddings: Optional[List[List[float]]] = None
    ) -> List[str]:
        """
        Thêm documents vào ChromaDB
        
        Args:
            documents: Danh sách văn bản documents
            metadatas: Danh sách metadata dicts
            ids: Danh sách document IDs tùy chọn
            embeddings: Embeddings đã tính toán sẵn tùy chọn
            
        Returns:
            Danh sách document IDs
        """
        try:
            # Tạo IDs nếu không được cung cấp
            if ids is None:
                ids = [str(uuid.uuid4()) for _ in documents]
            
            # Thêm vào collection
            if embeddings:
                self.collection.add(
                    documents=documents,
                    metadatas=metadatas,
                    ids=ids,
                    embeddings=embeddings
                )
            else:
                self.collection.add(
                    documents=documents,
                    metadatas=metadatas,
                    ids=ids
                )
            
            app_logger.info(f"Added {len(documents)} documents to vector store")
            return ids
            
        except Exception as e:
            app_logger.error(f"Lỗi khi thêm documents vào vector store: {e}")
            raise
    
    async def search(
        self,
        query_embedding: List[float],
        top_k: int = 5,
        filter_dict: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Tìm kiếm documents tương tự
        
        Args:
            query_embedding: Vector embedding cho query
            top_k: Số lượng kết quả trả về
            filter_dict: Bộ lọc metadata tùy chọn
            
        Returns:
            Danh sách kết quả với documents, metadata, và scores
        """
        try:
            runtime_where = _build_runtime_where(filter_dict)
            query_kwargs = {
                "query_embeddings": [query_embedding],
                "n_results": max(top_k, 20),
            }
            if runtime_where:
                query_kwargs["where"] = runtime_where
            results = self.collection.query(**query_kwargs)
            
            # Định dạng kết quả
            formatted_results = []
            if results['ids'] and results['ids'][0]:
                for i in range(len(results['ids'][0])):
                    document = results['documents'][0][i]
                    metadata = results['metadatas'][0][i]
                    if not _passes_runtime_filter(document, metadata, filter_dict):
                        continue
                    formatted_results.append({
                        'id': results['ids'][0][i],
                        'document': document,
                        'metadata': metadata,
                        'distance': results['distances'][0][i],
                        'similarity': 1 - results['distances'][0][i]  # Chuyển distance sang similarity
                    })
                    if len(formatted_results) >= top_k:
                        break
            
            app_logger.info(f"Found {len(formatted_results)} results for query")
            return formatted_results
            
        except Exception as e:
            app_logger.error(f"Lỗi khi tìm kiếm vector store: {e}")
            raise
    
    async def delete_documents(self, ids: List[str]) -> bool:
        """Xóa documents theo IDs"""
        try:
            self.collection.delete(ids=ids)
            app_logger.info(f"Deleted {len(ids)} documents from vector store")
            return True
        except Exception as e:
            app_logger.error(f"Lỗi khi xóa documents: {e}")
            return False
    
    async def get_document(self, doc_id: str) -> Optional[Dict[str, Any]]:
        """Lấy một document cụ thể theo ID"""
        try:
            results = self.collection.get(ids=[doc_id])
            if results['ids']:
                return {
                    'id': results['ids'][0],
                    'document': results['documents'][0],
                    'metadata': results['metadatas'][0]
                }
            return None
        except Exception as e:
            app_logger.error(f"Lỗi khi lấy document: {e}")
            return None
    
    def get_collection_stats(self) -> Dict[str, Any]:
        """Lấy thống kê về collection"""
        return {
            'name': self.collection_name,
            'count': self.collection.count(),
            'metadata': self.collection.metadata
        }
    
    def persist(self) -> None:
        """Lưu trữ collection vào đĩa"""
        self.client.persist()
        app_logger.info("Persisted vector store to disk")


class FAISSVectorStore(VectorStore):
    """Triển khai FAISS vector store (placeholder for future)"""
    
    def __init__(self, dimension: int = 1536):
        """Khởi tạo FAISS vector store"""
        self.dimension = dimension
        # TODO: Implement FAISS
        raise NotImplementedError("FAISS implementation coming soon")
    
    async def add_documents(
        self,
        documents: List[str],
        metadatas: List[Dict[str, Any]],
        ids: Optional[List[str]] = None
    ) -> List[str]:
        raise NotImplementedError()
    
    async def search(
        self,
        query_embedding: List[float],
        top_k: int = 5,
        filter_dict: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        raise NotImplementedError()
    
    async def delete_documents(self, ids: List[str]) -> bool:
        raise NotImplementedError()
    
    async def get_document(self, doc_id: str) -> Optional[Dict[str, Any]]:
        raise NotImplementedError()


# Factory function
def get_vector_store(
    store_type: Optional[str] = None,
    **kwargs
) -> VectorStore:
    """
    Hàm factory để lấy instance vector store
    
    Args:
        store_type: Loại vector store ('chromadb', 'faiss')
        **kwargs: Các tham số bổ sung cho vector store
        
    Returns:
        Instance VectorStore
    """
    store_type = store_type or settings.VECTOR_STORE_TYPE
    
    if store_type == "chromadb":
        return ChromaVectorStore(**kwargs)
    elif store_type == "faiss":
        return FAISSVectorStore(**kwargs)
    else:
        raise ValueError(f"Loại vector store không được hỗ trợ: {store_type}")


# Global vector store instance
_vector_store: Optional[VectorStore] = None


def get_default_vector_store() -> VectorStore:
    """Lấy hoặc tạo instance vector store mặc định"""
    global _vector_store
    if _vector_store is None:
        _vector_store = get_vector_store()
    return _vector_store
