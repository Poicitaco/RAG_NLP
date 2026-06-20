# BM25 Retrieval Evaluation

This report evaluates the dependency-light BM25 retrieval baseline for the pharmaceutical RAG corpus.

## Summary

- Cases: 15
- Top K: 5
- Hit@K: 0.8667
- Strict Hit@K: 0.8667
- MRR: 0.8
- Strict MRR: 0.7222

Strict matching requires the retrieved result to satisfy source/type/trust checks and contain all required terms.

## By Category

| Category | Cases | Hit@K | Strict Hit@K | MRR | Strict MRR |
|---|---:|---:|---:|---:|---:|
| counterfeit | 1 | 1.0 | 1.0 | 0.5 | 0.5 |
| dosage_ocr_risk | 1 | 1.0 | 1.0 | 1.0 | 1.0 |
| drug_registry | 4 | 1.0 | 1.0 | 1.0 | 0.875 |
| high_risk_context | 1 | 0.0 | 0.0 | 0.0 | 0.0 |
| interaction | 1 | 1.0 | 1.0 | 1.0 | 1.0 |
| ocr_leaflet | 1 | 1.0 | 1.0 | 1.0 | 0.3333 |
| recall | 4 | 0.75 | 0.75 | 0.625 | 0.625 |
| registration_number | 1 | 1.0 | 1.0 | 1.0 | 1.0 |
| safety_warning | 1 | 1.0 | 1.0 | 1.0 | 1.0 |

## Case Results

### drug_registry_001

- Question: Vocinti 10mg có hoạt chất gì và số đăng ký là gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Vocinti 10mg

### drug_registry_002

- Question: Glanatec Ophthalmic Solution 0.4% là dạng bào chế gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Glanatec Ophthalmic Solution 0.4%

### drug_registry_003

- Question: Ferinject số đăng ký 400110081626 do nước nào sản xuất?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 2
- Top result: `dav_all` / `drug_info` / `official_registry` / Ferinject

### drug_registry_004

- Question: Qlaira có hoạt chất nào?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Qlaira

### recall_001

- Question: Aceclofenac Stella 100mg có bị thu hồi không?
- Category: recall
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 2
- First strict rank: 2
- Top result: `dav_all` / `drug_info` / `official_registry` / Aceclofenac STELLA 100 mg

### recall_002

- Question: Clorocid TW3 cloramphenicol 250mg giả mạo là sao?
- Category: counterfeit
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 2
- First strict rank: 2
- Top result: `dav_all` / `drug_info` / `official_registry` / Clorocid TW3 250mg

### recall_003

- Question: Padobaby bị thu hồi vì lý do gì?
- Category: recall
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_recall` / `safety_recall` / `official_registry` / Quyết định số 696/QĐ-QLD về việc thu hồi do vi phạm mức độ 3 của thuốc Padobaby (Số giấy đăng ký lưu hành: 893100414024 (SĐK cũ: VD-32292-19))

### recall_004

- Question: Pyfaclor Kid cefaclor 125mg có thông báo thu hồi không?
- Category: recall
- Hit@K: False | Strict Hit@K: False
- First relevant rank: None
- First strict rank: None
- Top result: `dav_all` / `drug_info` / `official_registry` / Pyfaclor Kid

### recall_005

- Question: Diacerin 50 số đăng ký 893110447024 có quyết định thu hồi nào?
- Category: recall
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_recall` / `safety_recall` / `official_registry` / Quyết định số 46/QĐ-QLD về việc thu hồi do vi phạm mức độ 3 của thuốc Diacerin 50 (Số giấy đăng ký lưu hành: 893110447024)

### ocr_001

- Question: Nafacolex 400 mg thành phần là gì?
- Category: ocr_leaflet
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 3
- Top result: `dav_pdf_ocr` / `drug_info` / `unverified_ocr` / Nafacolex 400 mg

### ocr_002

- Question: Nafacolex 400 liều dùng ibuprofen như thế nào?
- Category: dosage_ocr_risk
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_pdf_ocr` / `dosage` / `unverified_ocr` / Nafacolex 400 mg

### safety_001

- Question: Tôi đang mang thai có dùng ibuprofen được không?
- Category: high_risk_context
- Hit@K: False | Strict Hit@K: False
- First relevant rank: None
- First strict rank: None
- Top result: `dav_pdf_ocr` / `interaction` / `unverified_ocr` / Paracetamol 325 mg/Ibuprofen 200 mg

### safety_002

- Question: Tôi uống aspirin cùng ibuprofen được không?
- Category: interaction
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_pdf_ocr` / `interaction` / `unverified_ocr` / Nafacolex 400 mg

### safety_003

- Question: Có thuốc chứa phenylbutazone không rõ nguồn gốc có nguy hiểm không?
- Category: safety_warning
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / DAV: Cảnh báo về các sản phẩm chứa phenylbutazone không rõ nguồn gốc

### registration_001

- Question: VD-25305-16 liên quan thuốc nào?
- Category: registration_number
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / DAV: Cảnh báo về thuốc Clorocid TW3 (cloramphenicol 250mg) giả mạo

