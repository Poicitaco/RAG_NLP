# Data Pipeline

Thu muc nay phuc vu phan quan trong nhat cua du an: du lieu cho RAG duoc.

## Cau truc

- `raw/`: du lieu tai ve nguyen goc tu nguon cong khai.
- `raw/dav/`: JSONL tu API cong khai cua Cuc Quan ly Duoc.
- `raw/documents/`: file PDF/HDSD/mau nhan tai ve neu API co URL tai lieu.
- `processed/`: du lieu da chuan hoa cho RAG.
- `chunks/`: cac chunk co metadata de index vao vector store.
- `evaluation/`: bo cau hoi test retrieval, citation va guardrail.

## Dataset snapshot hien tai

Tinh den lan chay gan nhat:

- `data/processed/dav_otc_drugs.jsonl`: 4,989 thuoc khong ke don tu DAV.
- `data/processed/dav_otc_drugs.csv`: ban CSV de phan tich va dua vao bao cao.
- `data/chunks/dav_otc_drugs_chunks.jsonl`: 19,158 chunks dang truong thong tin thuoc, dung de index vao vector store.
- `data/raw/dav/otc_raw.jsonl`: raw API snapshot, giu lai de tai lap preprocessing.
- `data/processed/dav_otc_profile.md`: thong ke dataset cho bao cao NLP.
- `data/processed/dav_all_drugs.jsonl`: 54,186 thuoc dang ky cong khai tu DAV, phu hop ho tro thuoc da duoc bac si ke.
- `data/processed/dav_all_drugs.csv`: ban CSV cua toan bo registry DAV.
- `data/processed/dav_all_profile.md`: thong ke full DAV registry.
- `data/chunks/dav_all_drugs_chunks_parts/`: 185,487 chunks registry DAV all, duoc tach shard de GitHub chap nhan.
- `data/processed/dav_recalls.jsonl`: 84 dong cong van thu hoi thuoc tu DAV.
- `data/chunks/dav_recalls_chunks.jsonl`: 84 chunks canh bao/thu hoi thuoc.
- `data/processed/canhgiacduoc_safety_articles.jsonl`: 459 bai safety/ADR/canh giac duoc.
- `data/chunks/canhgiacduoc_safety_chunks.jsonl`: 1,200 chunks an toan thuoc tu CanhGiacDuoc.
- `data/processed/dav_otc_document_priority.jsonl`: 40 thuoc uu tien tai HDSD/nhan theo 20 hoat chat OTC pho bien.
- `data/raw/documents/dav_otc_manifest.jsonl`: manifest 60 tai lieu PDF da tai tu DAV.
- `data/processed/dav_otc_pdf_text.jsonl`: 60 PDF da extract; 10 file co text layer doc duoc, 50 file can OCR.
- `data/chunks/dav_otc_pdf_chunks.jsonl`: 88 chunks tu PDF huong dan su dung/nhan doc duoc.
- `data/processed/dav_otc_pdf_ocr_text.jsonl`: 50 PDF scan da OCR bang Tesseract `vie+eng`, tong 458,631 ky tu.
- `data/chunks/dav_otc_pdf_ocr_chunks.jsonl`: 784 chunks OCR tu PDF scan.
- `data/processed/dav_otc_ocr_validation.jsonl`: report doi chieu OCR voi DAV registry.
- `data/processed/dav_otc_ocr_validation.csv`: bang review thu cong cho cac OCR doc can kiem tra.
- `data/chunks/rag_corpus_parts/`: 187,643 chunks tong hop de ingest vao vector store, duoc tach shard de GitHub chap nhan.
- `data/processed/rag_corpus_manifest.json`: thong ke thanh phan corpus tong hop.
- `data/processed/rag_corpus_parts_manifest.json`: manifest cac shard corpus tong hop.

Da lay du danh muc OTC va full registry DAV cong khai tai thoi diem chay script. PDF/nhan/HDSD da duoc tai theo mau uu tien top hoat chat pho bien; chua tai toan bo tai lieu PDF vi dung luong lon va nhieu file scan can OCR.

Dataset nay dung cho:

- Retrieval theo ten thuoc, so dang ky, hoat chat, ham luong, dang bao che, nha san xuat.
- Citation trong cau tra loi RAG bang metadata nguon DAV.
- Bao cao NLP: mo ta nguon du lieu, preprocessing, chunking, retrieval, guardrail, va danh gia faithfulness/citation.
- Tao bo test cau hoi an toan: cau hoi binh thuong, thieu thong tin nguoi dung, rui ro cao, va cap cuu.

## Nguon uu tien

1. DAV public API: `https://dichvucong.dav.gov.vn/api/services/app/soDangKy/GetAllPublicServerPaging`
2. Danh muc thuoc khong ke don: filter `thongTinThuocCoBan_LoaiThuocId = 1`
3. Cong van thu hoi thuoc DAV: `https://dav.gov.vn/cong-van-thu-hoi-thuoc-cn89.html`
4. Canh giac Duoc: ADR va thong tin an toan thuoc.
5. Duoc dien Viet Nam: chi nen dung bo sung cho chuan hoa ten dang bao che, tieu chuan/chat luong, phu luc va chuyen luan can thiet; khong thay the HDSD/nhan thuoc trong tu van su dung.

## Lenh mau

Lay 2 trang dau cua danh muc OTC de test:

```bash
python scripts/collect_dav_drugs.py --dataset otc --max-pages 2 --page-size 100
```

Lay toan bo OTC:

```bash
python scripts/collect_dav_drugs.py --dataset otc --page-size 500
```

Lay toan bo registry DAV:

```bash
python scripts/collect_dav_drugs.py --dataset all --page-size 1000
python scripts/rebuild_dav_processed_from_raw.py --dataset all
python scripts/profile_drug_dataset.py --input data/processed/dav_all_drugs.jsonl --json-output data/processed/dav_all_profile.json --md-output data/processed/dav_all_profile.md
python scripts/prepare_drug_chunks.py --input data/processed/dav_all_drugs.jsonl
```

Tao chunks tu file processed:

```bash
python scripts/prepare_drug_chunks.py --input data/processed/dav_otc_drugs.jsonl
```

Thong ke dataset cho bao cao NLP:

```bash
python scripts/profile_drug_dataset.py --input data/processed/dav_otc_drugs.jsonl
```

Tai thu HDSD/nhan tu DAV:

```bash
python scripts/download_dav_documents.py --input data/processed/dav_otc_drugs.jsonl --limit 20
```

Tai toan bo tai lieu OTC co the rat ton dung luong. Nen chay gioi han truoc, sau do moi bo `--limit`.

Extract text/chunks tu PDF da tai:

```bash
python scripts/extract_dav_pdf_chunks.py --manifest data/raw/documents/dav_otc_manifest.jsonl
```

Luu y: mot so PDF DAV la file scan/anh nen `pypdf` se khong doc duoc text. Output `data/processed/dav_otc_pdf_text.jsonl` co truong `extraction_status=needs_ocr` de danh dau cac file can OCR sau.

OCR cac PDF scan bang Tesseract. Tai lieu DAV chu yeu la tieng Viet, co xen tieng Anh o ten hoat chat/nhan/manufacturer, nen dung `vie+eng`:

```bash
python scripts/ocr_dav_documents.py --dpi 200 --lang vie+eng
```

Script can `pdftoppm` va `tesseract`. Neu thieu model tieng Viet, script se tai `vie.traineddata` vao `tools/tessdata/`.

Doi chieu OCR voi DAV registry de danh dau rui ro:

```bash
python scripts/validate_ocr_against_registry.py
python scripts/annotate_ocr_chunks.py
python scripts/build_rag_corpus.py
```

Tat ca chunk OCR duoc gan `trust_level=unverified_ocr` va `requires_human_review=true`. File CSV validation la noi de review cac mismatch ve hoat chat, ham luong, so lieu va don vi.

Chon tap PDF uu tien theo hoat chat pho bien:

```bash
python scripts/select_dav_document_sample.py --top-ingredients 20 --per-ingredient 2
python scripts/download_dav_documents.py --input data/processed/dav_otc_document_priority.jsonl --limit 60 --reset-manifest
```

Tao corpus RAG tong hop:

```bash
python scripts/collect_canhgiacduoc_articles.py --pages 18
python scripts/prepare_safety_article_chunks.py
python scripts/prepare_recall_chunks.py
python scripts/build_rag_corpus.py
python scripts/split_jsonl.py --input data/chunks/rag_corpus.jsonl --output-dir data/chunks/rag_corpus_parts --prefix rag_corpus --max-mb 80 --manifest data/processed/rag_corpus_parts_manifest.json
```

Build lexical BM25 index local de smoke-test retrieval khong can OpenAI API:

```bash
python scripts/build_bm25_index.py
python scripts/smoke_search_bm25.py "Aceclofenac Stella 100mg thu hồi" --top-k 3
python scripts/smoke_search_bm25.py "Nafacolex 400 liều dùng ibuprofen" --top-k 3
```

BM25 index duoc luu o `data/embeddings/bm25/` va khong commit len Git. Day la baseline rat huu ich cho ten thuoc, so dang ky, hoat chat va canh bao thu hoi. Chroma/vector embedding co the dung sau khi moi truong Python ho tro `chromadb`/`chroma-hnswlib` phu hop.

## Retrieval evaluation

Danh gia retrieval BM25 bang benchmark co rang buoc source/type/trust:

```bash
python scripts/evaluate_bm25_retrieval.py --top-k 5
```

Output:

- `data/evaluation/bm25_retrieval_results.json`: ket qua chi tiet tung cau hoi.
- `data/evaluation/bm25_retrieval_report.md`: bang tom tat Hit@K, Strict Hit@K, MRR va cac ca fail can toi uu.

Ket qua baseline gan nhat voi 15 cau hoi: Hit@5 = 0.8667, Strict Hit@5 = 0.8667, MRR = 0.8, Strict MRR = 0.7222. Hai loi can uu tien la truy van thu hoi bi registry lan at va cau hoi high-risk bi lay chunk OCR/interaction chua du an toan.

## JSON quality audit

Tao va dung virtual environment:

```bash
py -3.14 -m venv .venv
.\.venv\Scripts\python.exe --version
```

Quet chat luong JSON/JSONL:

```bash
.\.venv\Scripts\python.exe scripts\audit_json_text_quality.py --roots data
```

Sua ky tu dieu khien/mojibake co the phuc hoi:

```bash
.\.venv\Scripts\python.exe scripts\repair_json_text_quality.py data
```

Ket qua audit gan nhat: 30 file JSON/JSONL, 886,753 rows, 0 parse error, 0 repairable mojibake, 7 replacement-char tu PDF extraction va 2,402 OCR rows can human review/guardrail.

## Chroma smoke index

Sau khi tao `.venv` bang Python 3.11, co the kiem tra vector store voi 1,000 chunks truoc khi build full index:

```bash
.\.venv\Scripts\python.exe scripts\ingest_rag_corpus.py --limit 1000 --batch-size 64 --reset --persist-dir data\embeddings\chroma_smoke --collection pharmaceutical_smoke
.\.venv\Scripts\python.exe scripts\smoke_search_rag.py "Vocinti 10mg hoạt chất" --persist-dir data\embeddings\chroma_smoke --collection pharmaceutical_smoke --top-k 3
```

Kiem tra gan nhat: Chroma ingest thanh cong 1,000 chunks voi model `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`. Query exact-name co the kem BM25, vi vay huong toi uu nen la hybrid retrieval: BM25 cho exact match ten thuoc/SDK/hoat chat, vector search cho cau hoi dien dat tu nhien.

## Hybrid retrieval

Chay hybrid search BM25 + Chroma:

```bash
.\.venv\Scripts\python.exe scripts\hybrid_search_rag.py "Aceclofenac Stella 100mg thu hồi" --chroma-dir data\embeddings\chroma_smoke --collection pharmaceutical_smoke --top-k 3
```

Danh gia hybrid tren benchmark:

```bash
.\.venv\Scripts\python.exe scripts\evaluate_hybrid_retrieval.py --chroma-dir data\embeddings\chroma_smoke --collection pharmaceutical_smoke --top-k 5
```

Ket qua gan nhat tren benchmark 15 cau:

- BM25 baseline: Hit@5 = 0.8667, MRR = 0.8.
- Hybrid BM25 + Chroma smoke + source adjustment: Hit@5 = 1.0, MRR = 0.9556.

Luu y: Chroma hien moi la smoke index 1,000 chunks, nen ket qua nay dung de chung minh pipeline hybrid va source reranking. Khi build full Chroma index, can chay lai evaluation de lay so lieu chinh thuc cho bao cao.

## Chroma priority index

De tranh full vector index bi registry DAV lan at safety/recall evidence, tao priority corpus cho Chroma:

```bash
.\.venv\Scripts\python.exe scripts\build_chroma_priority_corpus.py --max-registry 12000
.\.venv\Scripts\python.exe scripts\ingest_rag_corpus.py --inputs data\chunks\chroma_priority_corpus.jsonl --batch-size 128 --reset --persist-dir data\embeddings\chroma_priority --collection pharmaceutical_priority
.\.venv\Scripts\python.exe scripts\evaluate_hybrid_retrieval.py --chroma-dir data\embeddings\chroma_priority --collection pharmaceutical_priority --top-k 5 --json-output data\evaluation\hybrid_priority_retrieval_results.json --md-output data\evaluation\hybrid_priority_retrieval_report.md
```

Priority corpus gan nhat co 14,156 chunks:

- DAV registry slice: 12,000 chunks.
- DAV PDF text: 88 chunks.
- DAV OCR PDF: 784 chunks.
- DAV recall: 84 chunks.
- CanhGiacDuoc safety: 1,200 chunks.

Ket qua hybrid priority index tren benchmark 15 cau: Hit@5 = 1.0, Strict Hit@5 = 1.0, MRR = 0.95, Strict MRR = 0.8833. Chroma index directory nam trong `data/embeddings/chroma_priority/` va khong commit len Git.

## Evidence guardrail evaluation

Evidence guardrail chay sau retrieval de quyet dinh bang chung co du an toan de sinh cau tra loi hay khong:

```bash
.\.venv\Scripts\python.exe scripts\evaluate_evidence_guardrails.py --input data\evaluation\hybrid_priority_retrieval_results.json
```

Ket qua gan nhat tren 15 cau benchmark:

- `allow`: 11 cau.
- `allow_with_caution`: 2 cau.
- `handoff`: 2 cau.

Hai ca bi handoff la cac cau rui ro cao ma bang chung chua du loai nguon da xac minh: cau hoi lieu dung dua vao OCR va cau hoi tuong tac chi co OCR. Day la hanh vi mong muon cho chatbot duoc pham an toan.
