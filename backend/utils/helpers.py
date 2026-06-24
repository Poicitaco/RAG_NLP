"""
Cac ham tien ich chung cho ung dung.
"""
import uuid
import hashlib
from typing import Dict, Any, List, Optional
from datetime import datetime
import re


def generate_session_id() -> str:
    """
    Tạo ID phiên duy nhất
    
    Returns:
        Chuỗi UUID
    """
    return str(uuid.uuid4())


def generate_user_id(email: str) -> str:
    """
    Tạo ID người dùng từ email sử dụng hash
    
    Args:
        email: Email người dùng
        
    Returns:
        User ID đã hash
    """
    return hashlib.sha256(email.encode()).hexdigest()[:16]


def format_response(
    success: bool,
    data: Any = None,
    message: str = "",
    metadata: Optional[Dict] = None
) -> Dict[str, Any]:
    """
    Định dạng phản hồi API theo cấu trúc nhất quán
    
    Args:
        success: Liệu thao tác có thành công không
        data: Dữ liệu phản hồi
        message: Tin nhắn phản hồi
        metadata: Metadata bổ sung
        
    Returns:
        Dictionary phản hồi đã định dạng
    """
    response = {
        "success": success,
        "timestamp": datetime.utcnow().isoformat(),
        "message": message,
    }
    
    if data is not None:
        response["data"] = data
    
    if metadata:
        response["metadata"] = metadata
    
    return response


def chunk_text(
    text: str,
    chunk_size: int = 1000,
    chunk_overlap: int = 200,
    separator: str = "\n\n"
) -> List[str]:
    """
    Chia văn bản thành các chunks có chồng chéo
    
    Args:
        text: Văn bản cần chia
        chunk_size: Kích thước tối đa của mỗi chunk
        chunk_overlap: Phần chồng chéo giữa các chunks
        separator: Ký tự phân tách
        
    Returns:
        Danh sách các text chunks
    """
    if not text:
        return []
    
    # Chia theo separator trước
    sections = text.split(separator)
    
    chunks = []
    current_chunk = ""
    
    for section in sections:
        # Nếu thêm section này vượt quá chunk_size, lưu chunk hiện tại
        if len(current_chunk) + len(section) > chunk_size and current_chunk:
            chunks.append(current_chunk.strip())
            # Bắt đầu chunk mới với phần chồng chéo
            current_chunk = current_chunk[-chunk_overlap:] if chunk_overlap > 0 else ""
        
        current_chunk += section + separator
    
    # Thêm chunk còn lại
    if current_chunk.strip():
        chunks.append(current_chunk.strip())
    
    return chunks


def sanitize_input(text: str) -> str:
    """
    Làm sạch input của người dùng bằng cách loại bỏ ký tự có khả năng gây hại
    
    Args:
        text: Văn bản đầu vào
        
    Returns:
        Văn bản đã làm sạch
    """
    if not text:
        return ""
    
    # Loại bỏ thẻ HTML
    text = re.sub(r'<[^>]+>', '', text)
    
    # Loại bỏ thẻ script
    text = re.sub(r'<script.*?</script>', '', text, flags=re.DOTALL)
    
    # Loại bỏ khoảng trắng thừa
    text = re.sub(r'\s+', ' ', text)
    
    return text.strip()


def format_medical_disclaimer() -> str:
    """
    Lấy văn bản disclaimer y tế
    
    Returns:
        Văn bản disclaimer
    """
    return (
        "**Lưu ý quan trọng**: Thông tin chỉ mang tính tham khảo, không thay thế "
        "bác sĩ hoặc dược sĩ. Không tự ý dùng thuốc kê đơn, đổi liều, ngưng thuốc "
        "hoặc phối hợp nhiều thuốc khi chưa được chuyên gia y tế xác nhận."
    )


def format_drug_info(drug_data: Dict[str, Any]) -> str:
    """
    Định dạng thông tin thuốc để hiển thị
    
    Args:
        drug_data: Dictionary chứa thông tin thuốc
        
    Returns:
        Chuỗi đã định dạng
    """
    sections = []
    
    if "name" in drug_data:
        sections.append(f"**Tên thuốc**: {drug_data['name']}")
    
    if "active_ingredient" in drug_data:
        sections.append(f"**Hoạt chất**: {drug_data['active_ingredient']}")
    
    if "dosage" in drug_data:
        sections.append(f"**Liều lượng**: {drug_data['dosage']}")
    
    if "usage" in drug_data:
        sections.append(f"**Cách dùng**: {drug_data['usage']}")
    
    if "indications" in drug_data:
        sections.append(f"**Chỉ định**: {drug_data['indications']}")
    
    if "contraindications" in drug_data:
        sections.append(f"**Chống chỉ định**: {drug_data['contraindications']}")
    
    if "side_effects" in drug_data:
        sections.append(f"**Tác dụng phụ**: {drug_data['side_effects']}")
    
    return "\n\n".join(sections)


def extract_keywords(text: str, max_keywords: int = 10) -> List[str]:
    """
    Trích xuất keywords từ văn bản (triển khai đơn giản)
    
    Args:
        text: Văn bản đầu vào
        max_keywords: Số lượng keywords tối đa trích xuất
        
    Returns:
        Danh sách keywords
    """
    # Loai bo dau cau va chuyen thanh chu thuong
    text = re.sub(r'[^\w\s]', '', text.lower())
    
    # Tach thanh danh sach tu
    words = text.split()
    
    # Loai bo stop words tieng Viet
    stop_words = {
        'và', 'của', 'có', 'cho', 'với', 'được', 'trong', 'là', 'các',
        'một', 'này', 'để', 'như', 'khi', 'đã', 'sẽ', 'không', 'thì'
    }
    
    # Loc va dem tan suat
    word_freq = {}
    for word in words:
        if word not in stop_words and len(word) > 2:
            word_freq[word] = word_freq.get(word, 0) + 1
    
    # Sap xep theo tan suat va tra ve cac tu khoa hang dau
    sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
    return [word for word, _ in sorted_words[:max_keywords]]


def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """
    Cat ngan van ban den do dai toi da cho phep.
    
    Args:
        text: Van ban can cat ngan
        max_length: Do dai toi da
        suffix: Hau to them vao khi bi cat ngan
        
    Returns:
        Van ban da cat ngan
    """
    if len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)].strip() + suffix
