# JSON Text Quality Audit

This audit scans JSON/JSONL files for mojibake, replacement characters, control characters, safety signals, and OCR review flags.

## Summary

- Files scanned: 30
- Rows scanned: 886753
- Files with parse errors: 0
- Files with mojibake markers: 0
- OCR rows requiring human review: 2402

## Issue Counts

| Issue | Count |
|---|---:|
| replacement_char | 7 |
| safety_signal | 122 |

## Files With Most Issues

| File | Rows | Issues | OCR review rows |
|---|---:|---:|---:|
| `data\chunks\rag_corpus.jsonl` | 187643 | 32 | 784 |
| `data\chunks\rag_corpus_parts\rag_corpus_part002.jsonl` | 65708 | 32 | 784 |
| `data\chunks\canhgiacduoc_safety_chunks.jsonl` | 1200 | 30 | 0 |
| `data\processed\canhgiacduoc_safety_articles.jsonl` | 459 | 21 | 0 |
| `data\evaluation\bm25_retrieval_results.json` | 1 | 8 | 0 |
| `data\evaluation\bm25_retrieval_benchmark.jsonl` | 15 | 3 | 0 |
| `data\chunks\dav_otc_pdf_chunks.jsonl` | 88 | 2 | 0 |
| `data\processed\dav_otc_pdf_text.jsonl` | 60 | 1 | 0 |
| `data\chunks\dav_otc_pdf_ocr_chunks.jsonl` | 784 | 0 | 784 |
| `data\processed\dav_otc_ocr_validation.jsonl` | 50 | 0 | 50 |

## Samples

### data\chunks\rag_corpus.jsonl

- line 185553 `$.document` ['replacement_char']: THANH PHAN CONG THUC: M6i vien cht'.ra: Thanh phfin duqc chAt: Loperamid hydroclorid 2 mg Thanh phfin ta duqc: Manitol, sucralose, natri starch glycolat, huong tutti fruti, magnesi stearat, silic dioxyd d�ng keo khan, ce
- line 185554 `$.document` ['replacement_char']: LIEU DUNG, cAcH DUNG Liiu dung Ngu·o·i Jo·n Tieu chay cdp tfnh: Khai ddu 2 vien, ti8p theo la 1 vien sau m6i ldn di tieu phan long ti8p theo. Thai gian di€u tri: 2 ngay. B?nh nhan tieu chay mc;m tfnh va c&t h6i trang: Kh
- line 186444 `$.document` ['safety_signal']: DAV: Thông báo thu hồi trên toàn quốc lô thuốc Aceclofenac Stella 100mg 06/04/2026 12:00:00 SA Ngày 31/03/2026, Cục Quản lý Dược có quyết định số 184/QĐ-QLD về thông báo thu hồi do vi phạm mức độ 2 đối với lô thuốc viên 
- line 186447 `$.document` ['safety_signal']: DAV: Cảnh báo về thuốc Clorocid TW3 (cloramphenicol 250mg) giả mạo 05/12/2025 12:00:00 SA Ngày 04/12/2025, Cục Quản lý Dược vừa có Công văn số 4334/QLD-CL về sản phẩm thuốc giả mạo Viên nén Clorocid TW3 (cloramphenicol 2
- line 186447 `$.metadata.title` ['safety_signal']: DAV: Cảnh báo về thuốc Clorocid TW3 (cloramphenicol 250mg) giả mạo

### data\chunks\rag_corpus_parts\rag_corpus_part002.jsonl

- line 63618 `$.document` ['replacement_char']: THANH PHAN CONG THUC: M6i vien cht'.ra: Thanh phfin duqc chAt: Loperamid hydroclorid 2 mg Thanh phfin ta duqc: Manitol, sucralose, natri starch glycolat, huong tutti fruti, magnesi stearat, silic dioxyd d�ng keo khan, ce
- line 63619 `$.document` ['replacement_char']: LIEU DUNG, cAcH DUNG Liiu dung Ngu·o·i Jo·n Tieu chay cdp tfnh: Khai ddu 2 vien, ti8p theo la 1 vien sau m6i ldn di tieu phan long ti8p theo. Thai gian di€u tri: 2 ngay. B?nh nhan tieu chay mc;m tfnh va c&t h6i trang: Kh
- line 64509 `$.document` ['safety_signal']: DAV: Thông báo thu hồi trên toàn quốc lô thuốc Aceclofenac Stella 100mg 06/04/2026 12:00:00 SA Ngày 31/03/2026, Cục Quản lý Dược có quyết định số 184/QĐ-QLD về thông báo thu hồi do vi phạm mức độ 2 đối với lô thuốc viên 
- line 64512 `$.document` ['safety_signal']: DAV: Cảnh báo về thuốc Clorocid TW3 (cloramphenicol 250mg) giả mạo 05/12/2025 12:00:00 SA Ngày 04/12/2025, Cục Quản lý Dược vừa có Công văn số 4334/QLD-CL về sản phẩm thuốc giả mạo Viên nén Clorocid TW3 (cloramphenicol 2
- line 64512 `$.metadata.title` ['safety_signal']: DAV: Cảnh báo về thuốc Clorocid TW3 (cloramphenicol 250mg) giả mạo

### data\chunks\canhgiacduoc_safety_chunks.jsonl

- line 1 `$.document` ['safety_signal']: DAV: Thông báo thu hồi trên toàn quốc lô thuốc Aceclofenac Stella 100mg 06/04/2026 12:00:00 SA Ngày 31/03/2026, Cục Quản lý Dược có quyết định số 184/QĐ-QLD về thông báo thu hồi do vi phạm mức độ 2 đối với lô thuốc viên 
- line 4 `$.document` ['safety_signal']: DAV: Cảnh báo về thuốc Clorocid TW3 (cloramphenicol 250mg) giả mạo 05/12/2025 12:00:00 SA Ngày 04/12/2025, Cục Quản lý Dược vừa có Công văn số 4334/QLD-CL về sản phẩm thuốc giả mạo Viên nén Clorocid TW3 (cloramphenicol 2
- line 4 `$.metadata.title` ['safety_signal']: DAV: Cảnh báo về thuốc Clorocid TW3 (cloramphenicol 250mg) giả mạo
- line 5 `$.metadata.title` ['safety_signal']: DAV: Cảnh báo về thuốc Clorocid TW3 (cloramphenicol 250mg) giả mạo
- line 6 `$.metadata.title` ['safety_signal']: DAV: Cảnh báo về thuốc Clorocid TW3 (cloramphenicol 250mg) giả mạo

### data\processed\canhgiacduoc_safety_articles.jsonl

- line 1 `$.article_text` ['safety_signal']: DAV: Thông báo thu hồi trên toàn quốc lô thuốc Aceclofenac Stella 100mg 06/04/2026 12:00:00 SA Ngày 31/03/2026, Cục Quản lý Dược có quyết định số 184/QĐ-QLD về thông báo thu hồi do vi phạm mức độ 2 đối với lô thuốc viên 
- line 2 `$.title` ['safety_signal']: DAV: Cảnh báo về thuốc Clorocid TW3 (cloramphenicol 250mg) giả mạo
- line 2 `$.article_text` ['safety_signal']: DAV: Cảnh báo về thuốc Clorocid TW3 (cloramphenicol 250mg) giả mạo 05/12/2025 12:00:00 SA Ngày 04/12/2025, Cục Quản lý Dược vừa có Công văn số 4334/QLD-CL về sản phẩm thuốc giả mạo Viên nén Clorocid TW3 (cloramphenicol 2
- line 4 `$.article_text` ['safety_signal']: DAV: Thông báo thu hồi trên toàn quốc lô thuốc cốm pha hỗn dịch uống Pyfaclor Kid 10/10/2025 12:00:00 SA Ngày 29/09/2025, Cục Quản lý Dược có quyết định số 475/QĐ-QLD về thông báo thu hồi do vi phạm mức độ 2 đối với thuố
- line 5 `$.title` ['safety_signal']: DAV: Cảnh báo về các sản phẩm chứa phenylbutazone không rõ nguồn gốc

### data\evaluation\bm25_retrieval_results.json

- line 1 `$.cases[5].question` ['safety_signal']: Clorocid TW3 cloramphenicol 250mg giả mạo là sao?
- line 1 `$.cases[5].results[1].title_or_drug` ['safety_signal']: DAV: Cảnh báo về thuốc Clorocid TW3 (cloramphenicol 250mg) giả mạo
- line 1 `$.cases[13].question` ['safety_signal']: Có thuốc chứa phenylbutazone không rõ nguồn gốc có nguy hiểm không?
- line 1 `$.cases[13].top_result.title_or_drug` ['safety_signal']: DAV: Cảnh báo về các sản phẩm chứa phenylbutazone không rõ nguồn gốc
- line 1 `$.cases[13].results[0].title_or_drug` ['safety_signal']: DAV: Cảnh báo về các sản phẩm chứa phenylbutazone không rõ nguồn gốc

### data\evaluation\bm25_retrieval_benchmark.jsonl

- line 6 `$.question` ['safety_signal']: Clorocid TW3 cloramphenicol 250mg giả mạo là sao?
- line 14 `$.question` ['safety_signal']: Có thuốc chứa phenylbutazone không rõ nguồn gốc có nguy hiểm không?
- line 14 `$.required_terms[1]` ['safety_signal']: không rõ nguồn gốc

### data\chunks\dav_otc_pdf_chunks.jsonl

- line 66 `$.document` ['replacement_char']: THANH PHAN CONG THUC: M6i vien cht'.ra: Thanh phfin duqc chAt: Loperamid hydroclorid 2 mg Thanh phfin ta duqc: Manitol, sucralose, natri starch glycolat, huong tutti fruti, magnesi stearat, silic dioxyd d�ng keo khan, ce
- line 67 `$.document` ['replacement_char']: LIEU DUNG, cAcH DUNG Liiu dung Ngu·o·i Jo·n Tieu chay cdp tfnh: Khai ddu 2 vien, ti8p theo la 1 vien sau m6i ldn di tieu phan long ti8p theo. Thai gian di€u tri: 2 ngay. B?nh nhan tieu chay mc;m tfnh va c&t h6i trang: Kh

### data\processed\dav_otc_pdf_text.jsonl

- line 39 `$.pages[0].text` ['replacement_char']: HUONG DAN SU DTJNG LOCABIS 'n phan tan trong mi?ng Loperamid hydroclorid 2 mg) I>pc y lU'O U' tl{tng truuc khi dung THANH PHAN CONG THUC: M6i vien cht'.ra: Thanh phfin duqc chAt: Loperamid hydroclorid 2 mg Thanh phfin ta

