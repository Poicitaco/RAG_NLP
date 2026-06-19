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
- `data/processed/dav_recalls.jsonl`: 8 dong cong van thu hoi thuoc mau.
- `data/raw/documents/dav_otc_manifest.jsonl`: manifest tai lieu PDF da tai thu.
- `data/processed/dav_otc_pdf_text.jsonl`: 3 PDF da extract; 1 file co text layer doc duoc, 2 file can OCR.
- `data/chunks/dav_otc_pdf_chunks.jsonl`: 25 chunks tu PDF huong dan su dung doc duoc.

Da lay du danh muc OTC dang ky cong khai tu DAV tai thoi diem chay script. Chua tai toan bo PDF/nhan/HDSD kem theo vi phan nay co dung luong lon va nhieu file scan can OCR.

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

## Lenh mau

Lay 2 trang dau cua danh muc OTC de test:

```bash
python scripts/collect_dav_drugs.py --dataset otc --max-pages 2 --page-size 100
```

Lay toan bo OTC:

```bash
python scripts/collect_dav_drugs.py --dataset otc --page-size 500
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
