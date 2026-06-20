# Hybrid Retrieval Evaluation

This evaluates BM25 + Chroma retrieval with evidence-aware source adjustment.

## Summary

- Cases: 15
- Top K: 5
- Hit@K: 1
- Strict Hit@K: 1
- MRR: 0.95
- Strict MRR: 0.8833

## By Category

| Category | Cases | Hit@K | Strict Hit@K | MRR | Strict MRR |
|---|---:|---:|---:|---:|---:|
| counterfeit | 1 | 1.0 | 1.0 | 1.0 | 1.0 |
| dosage_ocr_risk | 1 | 1.0 | 1.0 | 1.0 | 1.0 |
| drug_registry | 4 | 1.0 | 1.0 | 1.0 | 0.875 |
| high_risk_context | 1 | 1.0 | 1.0 | 0.25 | 0.25 |
| interaction | 1 | 1.0 | 1.0 | 1.0 | 1.0 |
| ocr_leaflet | 1 | 1.0 | 1.0 | 1.0 | 0.5 |
| recall | 4 | 1.0 | 1.0 | 1.0 | 1.0 |
| registration_number | 1 | 1.0 | 1.0 | 1.0 | 1.0 |
| safety_warning | 1 | 1.0 | 1.0 | 1.0 | 1.0 |

## Failures

- None

## Top Results

- `drug_registry_001` hit=True strict=True rank=1 top=`dav_all`/`drug_info` Vocinti 10mg
- `drug_registry_002` hit=True strict=True rank=1 top=`dav_all`/`drug_info` Glanatec Ophthalmic Solution 0.4%
- `drug_registry_003` hit=True strict=True rank=1 top=`dav_all`/`drug_info` Ferinject
- `drug_registry_004` hit=True strict=True rank=1 top=`dav_all`/`drug_info` Qlaira
- `recall_001` hit=True strict=True rank=1 top=`canhgiacduoc`/`safety_article` DAV: Thông báo thu hồi trên toàn quốc lô thuốc Aceclofenac Stella 100mg
- `recall_002` hit=True strict=True rank=1 top=`canhgiacduoc`/`safety_article` DAV: Cảnh báo về thuốc Clorocid TW3 (cloramphenicol 250mg) giả mạo
- `recall_003` hit=True strict=True rank=1 top=`dav_recall`/`safety_recall` Quyết định số 696/QĐ-QLD về việc thu hồi do vi phạm mức độ 3 của thuốc Padobaby (Số giấy đăng ký lưu hành: 893100414024 (SĐK cũ: VD-32292-19))
- `recall_004` hit=True strict=True rank=1 top=`dav_recall`/`safety_recall` Công văn số 841/QLD-CL về việc thông báo thu hồi thuốc vi phạm mức độ 3 (Cốm pha hỗn dịch uống Pyfaclor Kid (Cefaclor 125mg), Số GĐKLH: VD-26427-17, Số lô: 330823, NSX: 10823, HD: 210826; Số lô: 050124, NSX: 250124, HD: 250127)
- `recall_005` hit=True strict=True rank=1 top=`dav_recall`/`safety_recall` Quyết định số 46/QĐ-QLD về việc thu hồi do vi phạm mức độ 3 của thuốc Diacerin 50 (Số giấy đăng ký lưu hành: 893110447024)
- `ocr_001` hit=True strict=True rank=1 top=`dav_pdf_ocr`/`drug_info` Nafacolex 400 mg
- `ocr_002` hit=True strict=True rank=1 top=`dav_all`/`drug_info` Nafacolex 400 mg
- `safety_001` hit=True strict=True rank=4 top=`canhgiacduoc`/`safety_article` ANSM: Các biện pháp giảm thiểu nguy cơ u màng não khi sử dụng dẫn chất progestin
- `safety_002` hit=True strict=True rank=1 top=`dav_pdf_ocr`/`interaction` Nafacolex 400 mg
- `safety_003` hit=True strict=True rank=1 top=`canhgiacduoc`/`safety_article` DAV: Cảnh báo về các sản phẩm chứa phenylbutazone không rõ nguồn gốc
- `registration_001` hit=True strict=True rank=1 top=`canhgiacduoc`/`safety_article` DAV: Cảnh báo về thuốc Clorocid TW3 (cloramphenicol 250mg) giả mạo
