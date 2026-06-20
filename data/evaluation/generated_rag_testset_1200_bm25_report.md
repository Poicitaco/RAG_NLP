# BM25 Retrieval Evaluation

This report evaluates the dependency-light BM25 retrieval baseline for the pharmaceutical RAG corpus.

## Summary

- Cases: 1200
- Top K: 5
- Hit@K: 0.9083
- Strict Hit@K: 0.8142
- MRR: 0.8644
- Strict MRR: 0.736

Strict matching requires the retrieved result to satisfy source/type/trust checks and contain all required terms.

## By Category

| Category | Cases | Hit@K | Strict Hit@K | MRR | Strict MRR |
|---|---:|---:|---:|---:|---:|
| counterfeit | 3 | 1.0 | 1.0 | 1.0 | 1.0 |
| dosage_handoff | 216 | 0.8333 | 0.7917 | 0.7385 | 0.6532 |
| drug_registry | 420 | 1.0 | 0.9833 | 0.9825 | 0.8849 |
| emergency | 60 | 1.0 | 1.0 | 1.0 | 1.0 |
| high_risk_context | 144 | 0.5208 | 0.4792 | 0.412 | 0.3455 |
| interaction | 96 | 0.9479 | 0.0 | 0.8854 | 0.0 |
| recall | 120 | 1.0 | 1.0 | 1.0 | 1.0 |
| safety_warning | 141 | 1.0 | 1.0 | 0.977 | 0.977 |

## Case Results

### gen_registry_0001

- Question: AstaPadol 500 mg có hoạt chất gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 2
- Top result: `dav_all` / `drug_info` / `official_registry` / AstaPadol Viên sủi 500 mg

### gen_registry_0002

- Question: AstaPadol 500 mg số đăng ký là gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 2
- First strict rank: 2
- Top result: `dav_all` / `drug_info` / `official_registry` / AstaPadol Viên sủi 500 mg

### gen_registry_0003

- Question: Số đăng ký 893100228225 là thuốc nào?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / AstaPadol 500 mg

### gen_registry_0004

- Question: AstaPadol 500 mg dạng bào chế là gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 2
- First strict rank: 2
- Top result: `dav_all` / `drug_info` / `official_registry` / AstaPadol Viên sủi 500 mg

### gen_registry_0005

- Question: AstaPadol 500 mg do nước nào sản xuất?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / AstaPadol 500 mg

### gen_registry_0006

- Question: AstaPadol 500 mg hàm lượng bao nhiêu?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 2
- Top result: `dav_all` / `drug_info` / `official_registry` / AstaPadol Viên sủi 500 mg

### gen_registry_0007

- Question: Levical soft có hoạt chất gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 2
- Top result: `dav_all` / `drug_info` / `official_registry` / Levical soft

### gen_registry_0008

- Question: Levical soft số đăng ký là gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 4
- Top result: `dav_all` / `drug_info` / `official_registry` / Levical soft

### gen_registry_0009

- Question: Số đăng ký VD-11783-10 là thuốc nào?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Levical soft

### gen_registry_0010

- Question: Levical soft do nước nào sản xuất?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Levical soft

### gen_registry_0011

- Question: Cyclolife có hoạt chất gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Cyclolife

### gen_registry_0012

- Question: Cyclolife số đăng ký là gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Cyclolife

### gen_registry_0013

- Question: Số đăng ký VN-11222-10 là thuốc nào?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Cyclolife

### gen_registry_0014

- Question: Cyclolife dạng bào chế là gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Cyclolife

### gen_registry_0015

- Question: Cyclolife do nước nào sản xuất?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Cyclolife

### gen_registry_0016

- Question: Cyclolife hàm lượng bao nhiêu?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Cyclolife

### gen_registry_0017

- Question: Midatoren 160/25 có hoạt chất gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Midatoren 160/25

### gen_registry_0018

- Question: Midatoren 160/25 số đăng ký là gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Midatoren 160/25

### gen_registry_0019

- Question: Số đăng ký 893110160024 là thuốc nào?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Midatoren 160/25

### gen_registry_0020

- Question: Midatoren 160/25 dạng bào chế là gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 2
- Top result: `dav_all` / `drug_info` / `official_registry` / Midatoren 160/25

### gen_registry_0021

- Question: Midatoren 160/25 do nước nào sản xuất?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 2
- Top result: `dav_all` / `drug_info` / `official_registry` / Midatoren 160/25

### gen_registry_0022

- Question: Cozaar 50mg (đóng gói tại PT Merck Sharp Dohme Pharma Tbk. Đại chỉ: JI. Raya Pandaan Km 48, Pandaan, Pasuruan, Jawwa Timur, Indonesia) có hoạt chất gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Cozaar 50mg (đóng gói tại PT Merck Sharp Dohme Pharma Tbk. Đại chỉ: JI. Raya Pandaan Km 48, Pandaan, Pasuruan, Jawwa Timur, Indonesia)

### gen_registry_0023

- Question: Cozaar 50mg (đóng gói tại PT Merck Sharp Dohme Pharma Tbk. Đại chỉ: JI. Raya Pandaan Km 48, Pandaan, Pasuruan, Jawwa Timur, Indonesia) số đăng ký là gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Cozaar 50mg (đóng gói tại PT Merck Sharp Dohme Pharma Tbk. Đại chỉ: JI. Raya Pandaan Km 48, Pandaan, Pasuruan, Jawwa Timur, Indonesia)

### gen_registry_0024

- Question: Số đăng ký VN-19256-15 là thuốc nào?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Cozaar 50mg (đóng gói tại PT Merck Sharp Dohme Pharma Tbk. Đại chỉ: JI. Raya Pandaan Km 48, Pandaan, Pasuruan, Jawwa Timur, Indonesia)

### gen_registry_0025

- Question: Cozaar 50mg (đóng gói tại PT Merck Sharp Dohme Pharma Tbk. Đại chỉ: JI. Raya Pandaan Km 48, Pandaan, Pasuruan, Jawwa Timur, Indonesia) dạng bào chế là gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 2
- Top result: `dav_all` / `drug_info` / `official_registry` / Cozaar 50mg (đóng gói tại PT Merck Sharp Dohme Pharma Tbk. Đại chỉ: JI. Raya Pandaan Km 48, Pandaan, Pasuruan, Jawwa Timur, Indonesia)

### gen_registry_0026

- Question: Cozaar 50mg (đóng gói tại PT Merck Sharp Dohme Pharma Tbk. Đại chỉ: JI. Raya Pandaan Km 48, Pandaan, Pasuruan, Jawwa Timur, Indonesia) do nước nào sản xuất?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Cozaar 50mg (đóng gói tại PT Merck Sharp Dohme Pharma Tbk. Đại chỉ: JI. Raya Pandaan Km 48, Pandaan, Pasuruan, Jawwa Timur, Indonesia)

### gen_registry_0027

- Question: Terizidon có hoạt chất gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Terizidon

### gen_registry_0028

- Question: Terizidon số đăng ký là gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Terizidon

### gen_registry_0029

- Question: Số đăng ký VN1-274-10 là thuốc nào?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Terizidon

### gen_registry_0030

- Question: Terizidon dạng bào chế là gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Terizidon

### gen_registry_0031

- Question: Terizidon do nước nào sản xuất?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Terizidon

### gen_registry_0032

- Question: Terizidon hàm lượng bao nhiêu?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Terizidon

### gen_registry_0033

- Question: Cốm Calci có hoạt chất gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Cốm Calci

### gen_registry_0034

- Question: Cốm Calci số đăng ký là gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Cốm Calci

### gen_registry_0035

- Question: Số đăng ký VD-21942-14 là thuốc nào?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Cốm Calci

### gen_registry_0036

- Question: Cốm Calci dạng bào chế là gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Cốm Calci

### gen_registry_0037

- Question: Cốm Calci do nước nào sản xuất?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Cốm Calci

### gen_registry_0038

- Question: Vaco Allerf PE có hoạt chất gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 3
- Top result: `dav_all` / `drug_info` / `official_registry` / Vaco allerf PE

### gen_registry_0039

- Question: Vaco Allerf PE số đăng ký là gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 3
- Top result: `dav_all` / `drug_info` / `official_registry` / Vaco allerf PE

### gen_registry_0040

- Question: Số đăng ký VD-18427-13 là thuốc nào?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Vaco Allerf PE

### gen_registry_0041

- Question: Vaco Allerf PE dạng bào chế là gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 3
- Top result: `dav_all` / `drug_info` / `official_registry` / Vaco allerf PE

### gen_registry_0042

- Question: Vaco Allerf PE do nước nào sản xuất?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 2
- Top result: `dav_all` / `drug_info` / `official_registry` / Vaco allerf PE

### gen_registry_0043

- Question: Giải cảm Nhất Nhất có hoạt chất gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Giải cảm Nhất Nhất

### gen_registry_0044

- Question: Giải cảm Nhất Nhất số đăng ký là gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Giải cảm Nhất Nhất

### gen_registry_0045

- Question: Số đăng ký VD-33865-19 là thuốc nào?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Giải cảm Nhất Nhất

### gen_registry_0046

- Question: Giải cảm Nhất Nhất dạng bào chế là gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: False
- First relevant rank: 1
- First strict rank: None
- Top result: `dav_all` / `drug_info` / `official_registry` / Giải cảm Nhất Nhất

### gen_registry_0047

- Question: Giải cảm Nhất Nhất do nước nào sản xuất?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Giải cảm Nhất Nhất

### gen_registry_0048

- Question: Giải cảm Nhất Nhất hàm lượng bao nhiêu?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: False
- First relevant rank: 1
- First strict rank: None
- Top result: `dav_all` / `drug_info` / `official_registry` / Giải cảm Nhất Nhất

### gen_registry_0049

- Question: Vitamin B6 có hoạt chất gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: False
- First relevant rank: 1
- First strict rank: None
- Top result: `dav_all` / `drug_info` / `official_registry` / Vitamin B6 250mg

### gen_registry_0050

- Question: Vitamin B6 số đăng ký là gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: False
- First relevant rank: 2
- First strict rank: None
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / TGA: Cập nhật quy định mới nhằm giảm thiểu nguy cơ bệnh lý thần kinh ngoại biên khi sử dụng vitamin B6

### gen_registry_0051

- Question: Số đăng ký VD-16838-12 là thuốc nào?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Vitamin B6

### gen_registry_0052

- Question: Vitamin B6 dạng bào chế là gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 2
- First strict rank: 5
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / TGA: Cập nhật quy định mới nhằm giảm thiểu nguy cơ bệnh lý thần kinh ngoại biên khi sử dụng vitamin B6

### gen_registry_0053

- Question: Vitamin B6 do nước nào sản xuất?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Ngũ phúc tâm não thanh

### gen_registry_0054

- Question: Vitamin B6 hàm lượng bao nhiêu?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 4
- Top result: `dav_all` / `drug_info` / `official_registry` / Vitamin B6 250mg

### gen_registry_0055

- Question: Smofen có hoạt chất gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Smofen

### gen_registry_0056

- Question: Smofen số đăng ký là gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Smofen

### gen_registry_0057

- Question: Số đăng ký VD-36025-22 là thuốc nào?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Smofen

### gen_registry_0058

- Question: Smofen dạng bào chế là gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Smofen

### gen_registry_0059

- Question: Smofen do nước nào sản xuất?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Smofen

### gen_registry_0060

- Question: Smofen hàm lượng bao nhiêu?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Smofen

### gen_registry_0061

- Question: Atiferolyte 150 mg có hoạt chất gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Atiferolyte 150 mg

### gen_registry_0062

- Question: Atiferolyte 150 mg số đăng ký là gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Atiferolyte 150 mg

### gen_registry_0063

- Question: Số đăng ký 893100088500 là thuốc nào?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Atiferolyte 150 mg

### gen_registry_0064

- Question: Atiferolyte 150 mg dạng bào chế là gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 2
- Top result: `dav_all` / `drug_info` / `official_registry` / Atiferolyte 150 mg

### gen_registry_0065

- Question: Atiferolyte 150 mg do nước nào sản xuất?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Atiferolyte 150 mg

### gen_registry_0066

- Question: Atiferolyte 150 mg hàm lượng bao nhiêu?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Atiferolyte 150 mg

### gen_registry_0067

- Question: Friburine 40mg có hoạt chất gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Friburine 40mg

### gen_registry_0068

- Question: Friburine 40mg số đăng ký là gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Friburine 40mg

### gen_registry_0069

- Question: Số đăng ký 893110548524 là thuốc nào?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Friburine 40mg

### gen_registry_0070

- Question: Friburine 40mg dạng bào chế là gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 2
- Top result: `dav_all` / `drug_info` / `official_registry` / Friburine 40mg

### gen_registry_0071

- Question: Friburine 40mg do nước nào sản xuất?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Friburine 40mg

### gen_registry_0072

- Question: Friburine 40mg hàm lượng bao nhiêu?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Friburine 40mg

### gen_registry_0073

- Question: TS-One Capsule 25 có hoạt chất gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / TS-One capsule 25

### gen_registry_0074

- Question: TS-One Capsule 25 số đăng ký là gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 2
- Top result: `dav_all` / `drug_info` / `official_registry` / TS-One capsule 25

### gen_registry_0075

- Question: Số đăng ký VN-20694-17 là thuốc nào?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / TS-One Capsule 25

### gen_registry_0076

- Question: TS-One Capsule 25 dạng bào chế là gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 4
- Top result: `dav_all` / `drug_info` / `official_registry` / TS-One capsule 25

### gen_registry_0077

- Question: TS-One Capsule 25 do nước nào sản xuất?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 3
- Top result: `dav_all` / `drug_info` / `official_registry` / TS-One capsule 25

### gen_registry_0078

- Question: TS-One Capsule 25 hàm lượng bao nhiêu?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 2
- Top result: `dav_all` / `drug_info` / `official_registry` / TS-One capsule 25

### gen_registry_0079

- Question: Sulfareptol 960 có hoạt chất gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Sulfareptol 960

### gen_registry_0080

- Question: Sulfareptol 960 số đăng ký là gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Sulfareptol 960

### gen_registry_0081

- Question: Số đăng ký 893110139724 là thuốc nào?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Sulfareptol 960

### gen_registry_0082

- Question: Sulfareptol 960 dạng bào chế là gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Sulfareptol 960

### gen_registry_0083

- Question: Sulfareptol 960 do nước nào sản xuất?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Sulfareptol 960

### gen_registry_0084

- Question: Taginba có hoạt chất gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Taginba

### gen_registry_0085

- Question: Taginba số đăng ký là gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Taginba

### gen_registry_0086

- Question: Số đăng ký V221-H12-13 là thuốc nào?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Taginba

### gen_registry_0087

- Question: Taginba dạng bào chế là gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Taginba

### gen_registry_0088

- Question: Taginba do nước nào sản xuất?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Taginba

### gen_registry_0089

- Question: Taginba hàm lượng bao nhiêu?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Taginba

### gen_registry_0090

- Question: Glimepirid có hoạt chất gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 2
- Top result: `dav_all` / `drug_info` / `official_registry` / Glimepirid 2mg

### gen_registry_0091

- Question: Glimepirid số đăng ký là gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: False
- First relevant rank: 1
- First strict rank: None
- Top result: `dav_all` / `drug_info` / `official_registry` / Glimepirid 2mg

### gen_registry_0092

- Question: Số đăng ký VD-35784-22 là thuốc nào?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Glimepirid

### gen_registry_0093

- Question: Glimepirid dạng bào chế là gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Glimepirid 2mg

### gen_registry_0094

- Question: Glimepirid do nước nào sản xuất?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Gdalit

### gen_registry_0095

- Question: Glimepirid hàm lượng bao nhiêu?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Glemaz

### gen_registry_0096

- Question: Thysedow 5 mg có hoạt chất gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Thysedow 5 mg

### gen_registry_0097

- Question: Thysedow 5 mg số đăng ký là gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Thysedow 5 mg

### gen_registry_0098

- Question: Số đăng ký 893110491424 là thuốc nào?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Thysedow 5 mg

### gen_registry_0099

- Question: Thysedow 5 mg dạng bào chế là gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 3
- Top result: `dav_all` / `drug_info` / `official_registry` / Thysedow 5 mg

### gen_registry_0100

- Question: Thysedow 5 mg do nước nào sản xuất?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Thysedow 5 mg

### gen_registry_0101

- Question: Thysedow 5 mg hàm lượng bao nhiêu?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 2
- Top result: `dav_all` / `drug_info` / `official_registry` / Thysedow 5 mg

### gen_registry_0102

- Question: Glucoform 850 có hoạt chất gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Glucoform 850

### gen_registry_0103

- Question: Glucoform 850 số đăng ký là gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Glucoform 850

### gen_registry_0104

- Question: Số đăng ký VD-11086-10 là thuốc nào?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Glucoform 850

### gen_registry_0105

- Question: Glucoform 850 do nước nào sản xuất?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Glucoform 850

### gen_registry_0106

- Question: Donalium- DN có hoạt chất gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 3
- First strict rank: 3
- Top result: `dav_all` / `drug_info` / `official_registry` / Donalium - DN

### gen_registry_0107

- Question: Donalium- DN số đăng ký là gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 3
- First strict rank: 3
- Top result: `dav_all` / `drug_info` / `official_registry` / Donalium - DN

### gen_registry_0108

- Question: Số đăng ký VD-12101-10 là thuốc nào?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Donalium- DN

### gen_registry_0109

- Question: Donalium- DN dạng bào chế là gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 3
- First strict rank: 3
- Top result: `dav_all` / `drug_info` / `official_registry` / Donalium - DN

### gen_registry_0110

- Question: Donalium- DN do nước nào sản xuất?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 3
- Top result: `dav_all` / `drug_info` / `official_registry` / Donalium - DN

### gen_registry_0111

- Question: Donalium- DN hàm lượng bao nhiêu?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 3
- First strict rank: 3
- Top result: `dav_all` / `drug_info` / `official_registry` / Donalium - DN

### gen_registry_0112

- Question: Agilosart - H 100/12,5 số đăng ký là gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Agilosart - H 100/12,5

### gen_registry_0113

- Question: Số đăng ký 893110015100 là thuốc nào?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Agilosart - H 100/12,5

### gen_registry_0114

- Question: Agilosart - H 100/12,5 dạng bào chế là gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 2
- Top result: `dav_all` / `drug_info` / `official_registry` / Agilosart - H 100/12,5

### gen_registry_0115

- Question: Agilosart - H 100/12,5 do nước nào sản xuất?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 2
- Top result: `dav_all` / `drug_info` / `official_registry` / Agilosart - H 100/12,5

### gen_registry_0116

- Question: Agilosart - H 100/12,5 hàm lượng bao nhiêu?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 2
- Top result: `dav_all` / `drug_info` / `official_registry` / Agilosart - H 100/12,5

### gen_registry_0117

- Question: Alpodox có hoạt chất gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Alpodox

### gen_registry_0118

- Question: Alpodox số đăng ký là gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Alpodox

### gen_registry_0119

- Question: Số đăng ký VN-4940-10 là thuốc nào?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Alpodox

### gen_registry_0120

- Question: Alpodox dạng bào chế là gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Alpodox

### gen_registry_0121

- Question: Alpodox do nước nào sản xuất?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Alpodox

### gen_registry_0122

- Question: Alpodox hàm lượng bao nhiêu?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Alpodox

### gen_registry_0123

- Question: Lycoplan 200mg có hoạt chất gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Lycoplan 200mg

### gen_registry_0124

- Question: Lycoplan 200mg số đăng ký là gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Lycoplan 200mg

### gen_registry_0125

- Question: Số đăng ký VN-12159-11 là thuốc nào?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Lycoplan 200mg

### gen_registry_0126

- Question: Lycoplan 200mg dạng bào chế là gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Lycoplan 200mg

### gen_registry_0127

- Question: Lycoplan 200mg do nước nào sản xuất?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Lycoplan 200mg

### gen_registry_0128

- Question: Lycoplan 200mg hàm lượng bao nhiêu?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Lycoplan 200mg

### gen_registry_0129

- Question: Dentgital có hoạt chất gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Dentgital

### gen_registry_0130

- Question: Dentgital số đăng ký là gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 2
- Top result: `dav_all` / `drug_info` / `official_registry` / Dentgital

### gen_registry_0131

- Question: Số đăng ký V1468-H12-10 là thuốc nào?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Dentgital

### gen_registry_0132

- Question: Dentgital do nước nào sản xuất?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Dentgital

### gen_registry_0133

- Question: Xalexa 30 có hoạt chất gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Xalexa 30

### gen_registry_0134

- Question: Xalexa 30 số đăng ký là gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Xalexa 30

### gen_registry_0135

- Question: Số đăng ký VN-9943-10 là thuốc nào?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Xalexa 30

### gen_registry_0136

- Question: Xalexa 30 dạng bào chế là gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Xalexa 30

### gen_registry_0137

- Question: Xalexa 30 do nước nào sản xuất?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Xalexa 30

### gen_registry_0138

- Question: Xalexa 30 hàm lượng bao nhiêu?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Xalexa 30

### gen_registry_0139

- Question: Medotor - 10 có hoạt chất gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Medotor - 10

### gen_registry_0140

- Question: Medotor - 10 số đăng ký là gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Medotor - 10

### gen_registry_0141

- Question: Số đăng ký VN-21720-19 là thuốc nào?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Medotor - 10

### gen_registry_0142

- Question: Medotor - 10 dạng bào chế là gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Medotor - 10

### gen_registry_0143

- Question: Medotor - 10 do nước nào sản xuất?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Medotor - 10

### gen_registry_0144

- Question: Medotor - 10 hàm lượng bao nhiêu?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Medotor - 10

### gen_registry_0145

- Question: Pletimizol có hoạt chất gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Pletimizol

### gen_registry_0146

- Question: Pletimizol số đăng ký là gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Pletimizol

### gen_registry_0147

- Question: Số đăng ký VN-15121-12 là thuốc nào?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Pletimizol

### gen_registry_0148

- Question: Pletimizol dạng bào chế là gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Pletimizol

### gen_registry_0149

- Question: Pletimizol do nước nào sản xuất?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Pletimizol

### gen_registry_0150

- Question: Pletimizol hàm lượng bao nhiêu?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Pletimizol

### gen_registry_0151

- Question: Atigluco 500 có hoạt chất gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 2
- Top result: `dav_all` / `drug_info` / `official_registry` / Atigluco

### gen_registry_0152

- Question: Atigluco 500 số đăng ký là gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Atigluco 500

### gen_registry_0153

- Question: Số đăng ký 893100414624 là thuốc nào?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Atigluco 500

### gen_registry_0154

- Question: Atigluco 500 dạng bào chế là gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 2
- First strict rank: 2
- Top result: `dav_all` / `drug_info` / `official_registry` / Atigluco

### gen_registry_0155

- Question: Atigluco 500 do nước nào sản xuất?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Atigluco 500

### gen_registry_0156

- Question: Atigluco 500 hàm lượng bao nhiêu?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 2
- First strict rank: 2
- Top result: `dav_all` / `drug_info` / `official_registry` / Atigluco

### gen_registry_0157

- Question: SaViPamol 650 có hoạt chất gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / SaViPamol 650

### gen_registry_0158

- Question: SaViPamol 650 số đăng ký là gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / SaViPamol 650

### gen_registry_0159

- Question: Số đăng ký 893100252925 là thuốc nào?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / SaViPamol 650

### gen_registry_0160

- Question: SaViPamol 650 dạng bào chế là gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / SaViPamol 650

### gen_registry_0161

- Question: SaViPamol 650 do nước nào sản xuất?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / SaViPamol 650

### gen_registry_0162

- Question: SaViPamol 650 hàm lượng bao nhiêu?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / SaViPamol 650

### gen_registry_0163

- Question: Azzol-S 150 mg/cap có hoạt chất gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Azzol-S 150 mg/cap

### gen_registry_0164

- Question: Azzol-S 150 mg/cap số đăng ký là gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Azzol-S 150 mg/cap

### gen_registry_0165

- Question: Số đăng ký 520110308825 là thuốc nào?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Azzol-S 150 mg/cap

### gen_registry_0166

- Question: Azzol-S 150 mg/cap dạng bào chế là gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Azzol-S 150 mg/cap

### gen_registry_0167

- Question: Azzol-S 150 mg/cap do nước nào sản xuất?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Azzol-S 150 mg/cap

### gen_registry_0168

- Question: Azzol-S 150 mg/cap hàm lượng bao nhiêu?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Azzol-S 150 mg/cap

### gen_registry_0169

- Question: Atromux 10 có hoạt chất gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Atromux 10

### gen_registry_0170

- Question: Atromux 10 số đăng ký là gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Atromux 10

### gen_registry_0171

- Question: Số đăng ký VN-19036-15 là thuốc nào?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Atromux 10

### gen_registry_0172

- Question: Atromux 10 dạng bào chế là gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Atromux 10

### gen_registry_0173

- Question: Atromux 10 do nước nào sản xuất?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Atromux 10

### gen_registry_0174

- Question: Human Albumin Takeda 250g/l có hoạt chất gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Human Albumin Takeda 250g/l

### gen_registry_0175

- Question: Human Albumin Takeda 250g/l số đăng ký là gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Human Albumin Takeda 250g/l

### gen_registry_0176

- Question: Số đăng ký 800410323225 là thuốc nào?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Human Albumin Takeda 250g/l

### gen_registry_0177

- Question: Human Albumin Takeda 250g/l dạng bào chế là gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 2
- Top result: `dav_all` / `drug_info` / `official_registry` / Human Albumin Takeda 250g/l

### gen_registry_0178

- Question: Human Albumin Takeda 250g/l do nước nào sản xuất?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 2
- Top result: `dav_all` / `drug_info` / `official_registry` / Human Albumin Takeda 250g/l

### gen_registry_0179

- Question: Human Albumin Takeda 250g/l hàm lượng bao nhiêu?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 2
- Top result: `dav_all` / `drug_info` / `official_registry` / Human Albumin Takeda 250g/l

### gen_registry_0180

- Question: VacoCipdex 0,3% có hoạt chất gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / VacoCipdex 0,3%

### gen_registry_0181

- Question: VacoCipdex 0,3% số đăng ký là gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / VacoCipdex 0,3%

### gen_registry_0182

- Question: Số đăng ký VD-15498-11 là thuốc nào?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / VacoCipdex 0,3%

### gen_registry_0183

- Question: VacoCipdex 0,3% do nước nào sản xuất?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / VacoCipdex 0,3%

### gen_registry_0184

- Question: Vifamox 250 có hoạt chất gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Vifamox 250

### gen_registry_0185

- Question: Vifamox 250 số đăng ký là gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Vifamox 250

### gen_registry_0186

- Question: Số đăng ký VD-17980-12 là thuốc nào?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Vifamox 250

### gen_registry_0187

- Question: Vifamox 250 dạng bào chế là gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 2
- Top result: `dav_all` / `drug_info` / `official_registry` / Vifamox 250

### gen_registry_0188

- Question: Vifamox 250 do nước nào sản xuất?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Vifamox 250

### gen_registry_0189

- Question: Vifamox 250 hàm lượng bao nhiêu?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Vifamox 250

### gen_registry_0190

- Question: Calcicar 500 Tablet có hoạt chất gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Calcicar 500 Tablet

### gen_registry_0191

- Question: Calcicar 500 Tablet số đăng ký là gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Calcicar 500 Tablet

### gen_registry_0192

- Question: Số đăng ký VN-22514-20 là thuốc nào?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Calcicar 500 Tablet

### gen_registry_0193

- Question: Calcicar 500 Tablet dạng bào chế là gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Calcicar 500 Tablet

### gen_registry_0194

- Question: Calcicar 500 Tablet do nước nào sản xuất?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Calcicar 500 Tablet

### gen_registry_0195

- Question: Calcicar 500 Tablet hàm lượng bao nhiêu?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Calcicar 500 Tablet

### gen_registry_0196

- Question: Sanfetil 200 có hoạt chất gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Sanfetil 200

### gen_registry_0197

- Question: Sanfetil 200 số đăng ký là gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Sanfetil 200

### gen_registry_0198

- Question: Số đăng ký VN-13966-11 là thuốc nào?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Sanfetil 200

### gen_registry_0199

- Question: Sanfetil 200 dạng bào chế là gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Sanfetil 200

### gen_registry_0200

- Question: Sanfetil 200 do nước nào sản xuất?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Sanfetil 200

### gen_registry_0201

- Question: Sanfetil 200 hàm lượng bao nhiêu?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Sanfetil 200

### gen_registry_0202

- Question: Triamvirgri có hoạt chất gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Triamvirgri

### gen_registry_0203

- Question: Triamvirgri số đăng ký là gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Triamvirgri

### gen_registry_0204

- Question: Số đăng ký VN-11457-10 là thuốc nào?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Triamvirgri

### gen_registry_0205

- Question: Triamvirgri dạng bào chế là gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Triamvirgri

### gen_registry_0206

- Question: Triamvirgri do nước nào sản xuất?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Triamvirgri

### gen_registry_0207

- Question: Triamvirgri hàm lượng bao nhiêu?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Triamvirgri

### gen_registry_0208

- Question: Vorifend Forte có hoạt chất gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Vorifend Forte

### gen_registry_0209

- Question: Vorifend Forte số đăng ký là gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 3
- Top result: `dav_all` / `drug_info` / `official_registry` / Vorifend Forte

### gen_registry_0210

- Question: Số đăng ký VD-27535-17 là thuốc nào?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Vorifend Forte

### gen_registry_0211

- Question: Vorifend Forte dạng bào chế là gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Vorifend Forte

### gen_registry_0212

- Question: Vorifend Forte do nước nào sản xuất?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Vorifend Forte

### gen_registry_0213

- Question: Vorifend Forte hàm lượng bao nhiêu?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Vorifend Forte

### gen_registry_0214

- Question: Azaretin - H Cream có hoạt chất gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Azaretin - H Cream

### gen_registry_0215

- Question: Azaretin - H Cream số đăng ký là gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Azaretin - H Cream

### gen_registry_0216

- Question: Số đăng ký VN-9585-10 là thuốc nào?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Azaretin - H Cream

### gen_registry_0217

- Question: Azaretin - H Cream dạng bào chế là gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Azaretin - H Cream

### gen_registry_0218

- Question: Azaretin - H Cream do nước nào sản xuất?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Azaretin - H Cream

### gen_registry_0219

- Question: Azaretin - H Cream hàm lượng bao nhiêu?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Azaretin - H Cream

### gen_registry_0220

- Question: Heralopres H 25 có hoạt chất gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Heralopres H 25

### gen_registry_0221

- Question: Heralopres H 25 số đăng ký là gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Heralopres H 25

### gen_registry_0222

- Question: Số đăng ký 893110164300 là thuốc nào?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Heralopres H 25

### gen_registry_0223

- Question: Heralopres H 25 dạng bào chế là gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Heralopres H 25

### gen_registry_0224

- Question: Heralopres H 25 do nước nào sản xuất?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Heralopres H 25

### gen_registry_0225

- Question: Podus có hoạt chất gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Podus

### gen_registry_0226

- Question: Podus số đăng ký là gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Podus

### gen_registry_0227

- Question: Số đăng ký VD-24774-16 là thuốc nào?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Podus

### gen_registry_0228

- Question: Podus dạng bào chế là gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Podus

### gen_registry_0229

- Question: Podus do nước nào sản xuất?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Podus

### gen_registry_0230

- Question: Gabahasan 300 có hoạt chất gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 2
- Top result: `dav_all` / `drug_info` / `official_registry` / Gabahasan 300

### gen_registry_0231

- Question: Gabahasan 300 số đăng ký là gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 3
- Top result: `dav_all` / `drug_info` / `official_registry` / Gabahasan 300

### gen_registry_0232

- Question: Số đăng ký 893110208823 là thuốc nào?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Gabahasan 300

### gen_registry_0233

- Question: Gabahasan 300 dạng bào chế là gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Gabahasan 300

### gen_registry_0234

- Question: Gabahasan 300 do nước nào sản xuất?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Gabahasan 300

### gen_registry_0235

- Question: Gabahasan 300 hàm lượng bao nhiêu?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 2
- Top result: `dav_all` / `drug_info` / `official_registry` / Gabahasan 300

### gen_registry_0236

- Question: Calcitron có hoạt chất gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Calcitron

### gen_registry_0237

- Question: Calcitron số đăng ký là gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Calcitron

### gen_registry_0238

- Question: Số đăng ký VD-14740-11 là thuốc nào?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Calcitron

### gen_registry_0239

- Question: Calcitron do nước nào sản xuất?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Calcitron

### gen_registry_0240

- Question: Acarbose DWP 25 mg có hoạt chất gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Acarbose DWP 25 mg

### gen_registry_0241

- Question: Acarbose DWP 25 mg số đăng ký là gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Acarbose DWP 25 mg

### gen_registry_0242

- Question: Số đăng ký 893110235523 là thuốc nào?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Acarbose DWP 25 mg

### gen_registry_0243

- Question: Acarbose DWP 25 mg dạng bào chế là gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 2
- Top result: `dav_all` / `drug_info` / `official_registry` / Acarbose DWP 25 mg

### gen_registry_0244

- Question: Acarbose DWP 25 mg do nước nào sản xuất?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Acarbose DWP 25 mg

### gen_registry_0245

- Question: Acarbose DWP 25 mg hàm lượng bao nhiêu?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Acarbose DWP 25 mg

### gen_registry_0246

- Question: Pemetrexed Biovagen có hoạt chất gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Pemetrexed Biovagen

### gen_registry_0247

- Question: Pemetrexed Biovagen số đăng ký là gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Pemetrexed Biovagen

### gen_registry_0248

- Question: Số đăng ký 859114086023 là thuốc nào?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Pemetrexed Biovagen

### gen_registry_0249

- Question: Pemetrexed Biovagen dạng bào chế là gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 3
- Top result: `dav_all` / `drug_info` / `official_registry` / Pemetrexed biovagen

### gen_registry_0250

- Question: Pemetrexed Biovagen do nước nào sản xuất?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 2
- Top result: `dav_all` / `drug_info` / `official_registry` / Pemetrexed Biovagen

### gen_registry_0251

- Question: Lorabipha Tab. có hoạt chất gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Lorabipha Tab.

### gen_registry_0252

- Question: Lorabipha Tab. số đăng ký là gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Lorabipha Tab.

### gen_registry_0253

- Question: Số đăng ký 893100326200 là thuốc nào?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Lorabipha Tab.

### gen_registry_0254

- Question: Lorabipha Tab. dạng bào chế là gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Lorabipha Tab.

### gen_registry_0255

- Question: Lorabipha Tab. do nước nào sản xuất?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Lorabipha Tab.

### gen_registry_0256

- Question: Lorabipha Tab. hàm lượng bao nhiêu?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Lorabipha Tab.

### gen_registry_0257

- Question: Kupfolin có hoạt chất gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Kupfolin

### gen_registry_0258

- Question: Kupfolin số đăng ký là gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Kupfolin

### gen_registry_0259

- Question: Số đăng ký VD-10798-10 là thuốc nào?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Kupfolin

### gen_registry_0260

- Question: Kupfolin do nước nào sản xuất?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Kupfolin

### gen_registry_0261

- Question: Fizoti Inj. có hoạt chất gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Fizoti Inj

### gen_registry_0262

- Question: Fizoti Inj. số đăng ký là gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 2
- First strict rank: 2
- Top result: `dav_all` / `drug_info` / `official_registry` / Fizoti Inj

### gen_registry_0263

- Question: Số đăng ký VN-19721-16 là thuốc nào?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Fizoti Inj.

### gen_registry_0264

- Question: Fizoti Inj. dạng bào chế là gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 2
- Top result: `dav_all` / `drug_info` / `official_registry` / Fizoti Inj

### gen_registry_0265

- Question: Fizoti Inj. do nước nào sản xuất?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 2
- Top result: `dav_all` / `drug_info` / `official_registry` / Fizoti Inj

### gen_registry_0266

- Question: Hadusim 20 có hoạt chất gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Hadusim 20

### gen_registry_0267

- Question: Hadusim 20 số đăng ký là gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Hadusim 20

### gen_registry_0268

- Question: Số đăng ký 893110269725 là thuốc nào?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Hadusim 20

### gen_registry_0269

- Question: Hadusim 20 dạng bào chế là gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Hadusim 20

### gen_registry_0270

- Question: Hadusim 20 do nước nào sản xuất?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Hadusim 20

### gen_registry_0271

- Question: Hadusim 20 hàm lượng bao nhiêu?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Hadusim 20

### gen_registry_0272

- Question: Degas có hoạt chất gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Degas

### gen_registry_0273

- Question: Degas số đăng ký là gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Degas

### gen_registry_0274

- Question: Số đăng ký 893110375023 là thuốc nào?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Degas

### gen_registry_0275

- Question: Degas dạng bào chế là gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 2
- Top result: `dav_all` / `drug_info` / `official_registry` / Degas

### gen_registry_0276

- Question: Degas do nước nào sản xuất?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Degas

### gen_registry_0277

- Question: Degas hàm lượng bao nhiêu?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Degas

### gen_registry_0278

- Question: Ampicilin 500 mg có hoạt chất gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 5
- Top result: `dav_all` / `drug_info` / `official_registry` / Ampicilline 500 mg

### gen_registry_0279

- Question: Ampicilin 500 mg số đăng ký là gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: False
- First relevant rank: 3
- First strict rank: None
- Top result: `dav_all` / `drug_info` / `official_registry` / Ampicilline 500 mg

### gen_registry_0280

- Question: Số đăng ký VD-11823-10 là thuốc nào?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Ampicilin 500 mg

### gen_registry_0281

- Question: Ampicilin 500 mg do nước nào sản xuất?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 2
- Top result: `dav_all` / `drug_info` / `official_registry` / Ampicilin 
500 mg

### gen_registry_0282

- Question: Nhuận gan lợi mật có hoạt chất gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Nhuận gan lợi mật

### gen_registry_0283

- Question: Nhuận gan lợi mật số đăng ký là gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Nhuận gan lợi mật

### gen_registry_0284

- Question: Số đăng ký V1370-H12-10 là thuốc nào?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Nhuận gan lợi mật

### gen_registry_0285

- Question: Nhuận gan lợi mật do nước nào sản xuất?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Nhuận gan lợi mật

### gen_registry_0286

- Question: Thuốc tiêm Metronidazole có hoạt chất gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Thuốc tiêm Metronidazole

### gen_registry_0287

- Question: Thuốc tiêm Metronidazole số đăng ký là gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Thuốc tiêm Metronidazole

### gen_registry_0288

- Question: Số đăng ký VN-14375-11 là thuốc nào?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Thuốc tiêm Metronidazole

### gen_registry_0289

- Question: Thuốc tiêm Metronidazole dạng bào chế là gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Thuốc tiêm Metronidazole

### gen_registry_0290

- Question: Thuốc tiêm Metronidazole do nước nào sản xuất?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Thuốc tiêm Metronidazole

### gen_registry_0291

- Question: Thuốc tiêm Metronidazole hàm lượng bao nhiêu?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 2
- First strict rank: 2
- Top result: `dav_all` / `drug_info` / `official_registry` / Metronidazole Normon 5mg/ml Solution For Infusion

### gen_registry_0292

- Question: Avastin có hoạt chất gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Avastin

### gen_registry_0293

- Question: Avastin số đăng ký là gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 2
- Top result: `dav_all` / `drug_info` / `official_registry` / Avastin

### gen_registry_0294

- Question: Số đăng ký 760410306524 là thuốc nào?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Avastin

### gen_registry_0295

- Question: Avastin dạng bào chế là gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: False
- First relevant rank: 1
- First strict rank: None
- Top result: `dav_all` / `drug_info` / `official_registry` / Avastin

### gen_registry_0296

- Question: Avastin do nước nào sản xuất?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 3
- Top result: `dav_all` / `drug_info` / `official_registry` / Avastin

### gen_registry_0297

- Question: Avastin hàm lượng bao nhiêu?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 2
- Top result: `dav_all` / `drug_info` / `official_registry` / Avastin

### gen_registry_0298

- Question: Nefitaz có hoạt chất gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Nefitaz

### gen_registry_0299

- Question: Nefitaz số đăng ký là gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Nefitaz

### gen_registry_0300

- Question: Số đăng ký VN-14942-12 là thuốc nào?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Nefitaz

### gen_registry_0301

- Question: Nefitaz dạng bào chế là gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Nefitaz

### gen_registry_0302

- Question: Nefitaz do nước nào sản xuất?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Nefitaz

### gen_registry_0303

- Question: Nefitaz hàm lượng bao nhiêu?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Nefitaz

### gen_registry_0304

- Question: Imemoti tab có hoạt chất gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Imemoti tab

### gen_registry_0305

- Question: Imemoti tab số đăng ký là gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Imemoti tab

### gen_registry_0306

- Question: Số đăng ký 893110146823 là thuốc nào?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Imemoti tab

### gen_registry_0307

- Question: Imemoti tab dạng bào chế là gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Imemoti tab

### gen_registry_0308

- Question: Imemoti tab do nước nào sản xuất?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Imemoti tab

### gen_registry_0309

- Question: Imemoti tab hàm lượng bao nhiêu?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Imemoti tab

### gen_registry_0310

- Question: Danaroxime 1500mg có hoạt chất gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Danaroxime 1500mg

### gen_registry_0311

- Question: Danaroxime 1500mg số đăng ký là gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Danaroxime 1500mg

### gen_registry_0312

- Question: Số đăng ký 300110066526 là thuốc nào?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Danaroxime 1500mg

### gen_registry_0313

- Question: Danaroxime 1500mg dạng bào chế là gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Danaroxime 1500mg

### gen_registry_0314

- Question: Danaroxime 1500mg do nước nào sản xuất?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Danaroxime 1500mg

### gen_registry_0315

- Question: Danaroxime 1500mg hàm lượng bao nhiêu?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Danaroxime 1500mg

### gen_registry_0316

- Question: Uratonyl có hoạt chất gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Uratonyl

### gen_registry_0317

- Question: Uratonyl số đăng ký là gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Uratonyl

### gen_registry_0318

- Question: Số đăng ký VN-14335-11 là thuốc nào?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Uratonyl

### gen_registry_0319

- Question: Uratonyl dạng bào chế là gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Uratonyl

### gen_registry_0320

- Question: Uratonyl do nước nào sản xuất?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Uratonyl

### gen_registry_0321

- Question: Uratonyl hàm lượng bao nhiêu?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Uratonyl

### gen_registry_0322

- Question: Odistad 120 có hoạt chất gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Odistad 120

### gen_registry_0323

- Question: Odistad 120 số đăng ký là gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 3
- Top result: `dav_all` / `drug_info` / `official_registry` / Odistad 120

### gen_registry_0324

- Question: Số đăng ký VD-34910-20 là thuốc nào?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Odistad 120

### gen_registry_0325

- Question: Odistad 120 dạng bào chế là gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 3
- Top result: `dav_all` / `drug_info` / `official_registry` / Odistad 120

### gen_registry_0326

- Question: Odistad 120 do nước nào sản xuất?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Odistad 120

### gen_registry_0327

- Question: Odistad 120 hàm lượng bao nhiêu?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 4
- Top result: `dav_all` / `drug_info` / `official_registry` / Odistad 120

### gen_registry_0328

- Question: Telfor có hoạt chất gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Telfor 60

### gen_registry_0329

- Question: Telfor số đăng ký là gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 4
- Top result: `dav_all` / `drug_info` / `official_registry` / Telfor 60

### gen_registry_0330

- Question: Số đăng ký VD-17355-12 là thuốc nào?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Telfor

### gen_registry_0331

- Question: Telfor dạng bào chế là gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Telfor

### gen_registry_0332

- Question: Telfor do nước nào sản xuất?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Telfor

### gen_registry_0333

- Question: Telfor hàm lượng bao nhiêu?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Telfor

### gen_registry_0334

- Question: Darunavir Tablets 600mg có hoạt chất gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Darunavir Tablets 600mg

### gen_registry_0335

- Question: Darunavir Tablets 600mg số đăng ký là gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Darunavir Tablets 600mg

### gen_registry_0336

- Question: Số đăng ký 890110017823 là thuốc nào?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Darunavir Tablets 600mg

### gen_registry_0337

- Question: Darunavir Tablets 600mg dạng bào chế là gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Darunavir Tablets 600mg

### gen_registry_0338

- Question: Darunavir Tablets 600mg do nước nào sản xuất?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Darunavir Tablets 600mg

### gen_registry_0339

- Question: Harnal Ocas 0,4mg có hoạt chất gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 4
- Top result: `dav_all` / `drug_info` / `official_registry` / Harnal Ocas 0,4mg

### gen_registry_0340

- Question: Harnal Ocas 0,4mg số đăng ký là gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 4
- Top result: `dav_all` / `drug_info` / `official_registry` / Harnal Ocas 0,4mg

### gen_registry_0341

- Question: Số đăng ký VN-9643-10 là thuốc nào?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Harnal Ocas 0,4mg

### gen_registry_0342

- Question: Harnal Ocas 0,4mg dạng bào chế là gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 2
- Top result: `dav_all` / `drug_info` / `official_registry` / Harnal Ocas 0,4mg

### gen_registry_0343

- Question: Harnal Ocas 0,4mg do nước nào sản xuất?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 3
- Top result: `dav_all` / `drug_info` / `official_registry` / Harnal Ocas 0,4mg

### gen_registry_0344

- Question: Harnal Ocas 0,4mg hàm lượng bao nhiêu?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Harnal Ocas 0,4mg

### gen_registry_0345

- Question: Coolzz trẻ em có hoạt chất gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Coolzz trẻ em

### gen_registry_0346

- Question: Coolzz trẻ em số đăng ký là gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Coolzz trẻ em

### gen_registry_0347

- Question: Số đăng ký 893100936124 là thuốc nào?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Coolzz trẻ em

### gen_registry_0348

- Question: Coolzz trẻ em dạng bào chế là gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Coolzz trẻ em

### gen_registry_0349

- Question: Coolzz trẻ em do nước nào sản xuất?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Coolzz trẻ em

### gen_registry_0350

- Question: Coolzz trẻ em hàm lượng bao nhiêu?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Coolzz trẻ em

### gen_registry_0351

- Question: Amoxybiotic 500 có hoạt chất gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Amoxybiotic 500

### gen_registry_0352

- Question: Amoxybiotic 500 số đăng ký là gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Amoxybiotic 500

### gen_registry_0353

- Question: Số đăng ký VD-17091-12 là thuốc nào?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Amoxybiotic 500

### gen_registry_0354

- Question: Amoxybiotic 500 dạng bào chế là gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Amoxybiotic 500

### gen_registry_0355

- Question: Amoxybiotic 500 do nước nào sản xuất?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Amoxybiotic 500

### gen_registry_0356

- Question: Amoxybiotic 500 hàm lượng bao nhiêu?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Amoxybiotic 500

### gen_registry_0357

- Question: Ribazole có hoạt chất gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Ribazole Tablets 500mg

### gen_registry_0358

- Question: Ribazole số đăng ký là gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 2
- Top result: `dav_all` / `drug_info` / `official_registry` / Ribazole Tablets 500mg

### gen_registry_0359

- Question: Số đăng ký VN-14679-12 là thuốc nào?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Ribazole

### gen_registry_0360

- Question: Ribazole dạng bào chế là gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 2
- Top result: `dav_all` / `drug_info` / `official_registry` / Ribazole Tablets 500mg

### gen_registry_0361

- Question: Ribazole do nước nào sản xuất?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Ribazole

### gen_registry_0362

- Question: Ribazole hàm lượng bao nhiêu?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 2
- Top result: `dav_all` / `drug_info` / `official_registry` / Ribazole Tablets 500mg

### gen_registry_0363

- Question: Paluzine có hoạt chất gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Paluzine

### gen_registry_0364

- Question: Paluzine số đăng ký là gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Paluzine

### gen_registry_0365

- Question: Số đăng ký 893100361925 là thuốc nào?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Paluzine

### gen_registry_0366

- Question: Paluzine dạng bào chế là gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 2
- Top result: `dav_all` / `drug_info` / `official_registry` / Paluzine

### gen_registry_0367

- Question: Paluzine do nước nào sản xuất?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Paluzine

### gen_registry_0368

- Question: Paluzine hàm lượng bao nhiêu?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 2
- Top result: `dav_all` / `drug_info` / `official_registry` / Paluzine

### gen_registry_0369

- Question: Carbocistein 100mg có hoạt chất gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Carbocistein 100mg

### gen_registry_0370

- Question: Carbocistein 100mg số đăng ký là gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Carbocistein 100mg

### gen_registry_0371

- Question: Số đăng ký VD-11601-10 là thuốc nào?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Carbocistein 100mg

### gen_registry_0372

- Question: Carbocistein 100mg do nước nào sản xuất?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Carbocistein 100mg

### gen_registry_0373

- Question: Rohto Hydra R có hoạt chất gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Rohto Hydra R

### gen_registry_0374

- Question: Rohto Hydra R số đăng ký là gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Rohto Hydra R

### gen_registry_0375

- Question: Số đăng ký 893100163500 là thuốc nào?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Rohto Hydra R

### gen_registry_0376

- Question: Rohto Hydra R dạng bào chế là gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Rohto Hydra R

### gen_registry_0377

- Question: Rohto Hydra R do nước nào sản xuất?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Rohto Hydra R

### gen_registry_0378

- Question: Rohto Hydra R hàm lượng bao nhiêu?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Rohto Hydra R

### gen_registry_0379

- Question: Cosaraz có hoạt chất gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Cosaraz

### gen_registry_0380

- Question: Cosaraz số đăng ký là gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Cosaraz

### gen_registry_0381

- Question: Số đăng ký VN-5137-10 là thuốc nào?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Cosaraz

### gen_registry_0382

- Question: Cosaraz dạng bào chế là gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Cosaraz

### gen_registry_0383

- Question: Cosaraz do nước nào sản xuất?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Cosaraz

### gen_registry_0384

- Question: Cosaraz hàm lượng bao nhiêu?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Cosaraz

### gen_registry_0385

- Question: SPEEDA có hoạt chất gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / SPEEDA

### gen_registry_0386

- Question: SPEEDA số đăng ký là gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / SPEEDA

### gen_registry_0387

- Question: Số đăng ký QLVX-1041-17 là thuốc nào?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / SPEEDA

### gen_registry_0388

- Question: SPEEDA dạng bào chế là gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 3
- Top result: `dav_all` / `drug_info` / `official_registry` / SPEEDA

### gen_registry_0389

- Question: SPEEDA do nước nào sản xuất?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / SPEEDA

### gen_registry_0390

- Question: SPEEDA hàm lượng bao nhiêu?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 2
- Top result: `dav_all` / `drug_info` / `official_registry` / SPEEDA

### gen_registry_0391

- Question: Ibufen D Oral Suspension có hoạt chất gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Ibufen D Oral Suspension

### gen_registry_0392

- Question: Ibufen D Oral Suspension số đăng ký là gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Ibufen D Oral Suspension

### gen_registry_0393

- Question: Số đăng ký VN-13779-11 là thuốc nào?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Ibufen D Oral Suspension

### gen_registry_0394

- Question: Ibufen D Oral Suspension dạng bào chế là gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Ibufen D Oral Suspension

### gen_registry_0395

- Question: Ibufen D Oral Suspension do nước nào sản xuất?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Ibufen D Oral Suspension

### gen_registry_0396

- Question: Ibufen D Oral Suspension hàm lượng bao nhiêu?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Ibufen D Oral Suspension

### gen_registry_0397

- Question: Simterol có hoạt chất gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Simterol

### gen_registry_0398

- Question: Simterol số đăng ký là gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Simterol

### gen_registry_0399

- Question: Số đăng ký 893110387523 là thuốc nào?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Simterol

### gen_registry_0400

- Question: Simterol dạng bào chế là gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Simterol

### gen_registry_0401

- Question: Simterol do nước nào sản xuất?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Simterol

### gen_registry_0402

- Question: Simterol hàm lượng bao nhiêu?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Simterol

### gen_registry_0403

- Question: Gentizone có hoạt chất gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Gentizone

### gen_registry_0404

- Question: Gentizone số đăng ký là gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Gentizone

### gen_registry_0405

- Question: Số đăng ký 893110557624 là thuốc nào?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Gentizone

### gen_registry_0406

- Question: Gentizone dạng bào chế là gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Gentizone

### gen_registry_0407

- Question: Gentizone do nước nào sản xuất?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Gentizone

### gen_registry_0408

- Question: Livethine Powder 3g có hoạt chất gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Livethine Powder 3g

### gen_registry_0409

- Question: Livethine Powder 3g số đăng ký là gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Livethine Powder 3g

### gen_registry_0410

- Question: Số đăng ký 893110230723 là thuốc nào?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Livethine Powder 3g

### gen_registry_0411

- Question: Livethine Powder 3g dạng bào chế là gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Livethine Powder 3g

### gen_registry_0412

- Question: Livethine Powder 3g do nước nào sản xuất?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Livethine Powder 3g

### gen_registry_0413

- Question: Livethine Powder 3g hàm lượng bao nhiêu?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Livethine Powder 3g

### gen_registry_0414

- Question: Daygra 25 có hoạt chất gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Daygra 25

### gen_registry_0415

- Question: Daygra 25 số đăng ký là gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Daygra 25

### gen_registry_0416

- Question: Số đăng ký VD-10187-10 là thuốc nào?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Daygra 25

### gen_registry_0417

- Question: Daygra 25 do nước nào sản xuất?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Daygra 25

### gen_registry_0418

- Question: Lobitzo có hoạt chất gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Lobitzo

### gen_registry_0419

- Question: Lobitzo số đăng ký là gì?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Lobitzo

### gen_registry_0420

- Question: Số đăng ký VN-12959-11 là thuốc nào?
- Category: drug_registry
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Lobitzo

### gen_recall_0001

- Question: Công văn số 16984/QLD-CL về việc thông báo thu hồi thuốc vi phạm mức độ 3 (Viên nang mềm Dacodex) có phải thông báo thu hồi không?
- Category: recall
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_recall` / `safety_recall` / `official_registry` / Công văn số 16984/QLD-CL về việc thông báo thu hồi thuốc vi phạm mức độ 3 (Viên nang mềm Dacodex)

### gen_recall_0002

- Question: Công văn số 16984/QLD-CL về việc thông báo thu hồi thuốc vi phạm mức độ 3 (Viên nang mềm Dacodex) thuộc cảnh báo/thu hồi nào?
- Category: recall
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_recall` / `safety_recall` / `official_registry` / Công văn số 16984/QLD-CL về việc thông báo thu hồi thuốc vi phạm mức độ 3 (Viên nang mềm Dacodex)

### gen_recall_0003

- Question: Cho tôi nguồn về Công văn số 16984/QLD-CL về việc thông báo thu hồi thuốc vi phạm mức độ 3 (Viên nang mềm Dacodex)
- Category: recall
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_recall` / `safety_recall` / `official_registry` / Công văn số 16984/QLD-CL về việc thông báo thu hồi thuốc vi phạm mức độ 3 (Viên nang mềm Dacodex)

### gen_recall_0004

- Question: Công văn số 3828/QLD-CL đình chỉ lưu hành thuốc không đạt tiêu chuẩn chất lượng (Diuresin SR (Indapamide 1,5mg)) có phải thông báo thu hồi không?
- Category: recall
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_recall` / `safety_recall` / `official_registry` / Công văn số 3828/QLD-CL đình chỉ lưu hành thuốc không đạt tiêu chuẩn chất lượng (Diuresin SR (Indapamide 1,5mg))

### gen_recall_0005

- Question: Công văn số 3828/QLD-CL đình chỉ lưu hành thuốc không đạt tiêu chuẩn chất lượng (Diuresin SR (Indapamide 1,5mg)) thuộc cảnh báo/thu hồi nào?
- Category: recall
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_recall` / `safety_recall` / `official_registry` / Công văn số 3828/QLD-CL đình chỉ lưu hành thuốc không đạt tiêu chuẩn chất lượng (Diuresin SR (Indapamide 1,5mg))

### gen_recall_0006

- Question: Cho tôi nguồn về Công văn số 3828/QLD-CL đình chỉ lưu hành thuốc không đạt tiêu chuẩn chất lượng (Diuresin SR (Indapamide 1,5mg))
- Category: recall
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_recall` / `safety_recall` / `official_registry` / Công văn số 3828/QLD-CL đình chỉ lưu hành thuốc không đạt tiêu chuẩn chất lượng (Diuresin SR (Indapamide 1,5mg))

### gen_recall_0007

- Question: Đình chỉ lưu hành thuốc không đạt tiêu chuẩn chất lượng (thuốc tiêm Koreamin) có phải thông báo thu hồi không?
- Category: recall
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_recall` / `safety_recall` / `official_registry` / Đình chỉ lưu hành thuốc không đạt tiêu chuẩn chất lượng (thuốc tiêm Koreamin)

### gen_recall_0008

- Question: Đình chỉ lưu hành thuốc không đạt tiêu chuẩn chất lượng (thuốc tiêm Koreamin) thuộc cảnh báo/thu hồi nào?
- Category: recall
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_recall` / `safety_recall` / `official_registry` / Đình chỉ lưu hành thuốc không đạt tiêu chuẩn chất lượng (thuốc tiêm Koreamin)

### gen_recall_0009

- Question: Cho tôi nguồn về Đình chỉ lưu hành thuốc không đạt tiêu chuẩn chất lượng (thuốc tiêm Koreamin)
- Category: recall
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_recall` / `safety_recall` / `official_registry` / Đình chỉ lưu hành thuốc không đạt tiêu chuẩn chất lượng (thuốc tiêm Koreamin)

### gen_recall_0010

- Question: Công văn số 6125/QLD-CL về việc thông báo thu hồi thuốc vi phạm mức độ 2 (Thuốc Siro uống Siro Nutrohadi F, Số GĐKLH: VD- 18684-13, Số lô: 030221; NSX: 240221; HD: 230224) có phải thông báo thu hồi không?
- Category: recall
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_recall` / `safety_recall` / `official_registry` / Công văn số 6125/QLD-CL về việc thông báo thu hồi thuốc vi phạm mức độ 2 (Thuốc Siro uống Siro Nutrohadi F, Số GĐKLH: VD- 18684-13, Số lô: 030221; NSX: 240221; HD: 230224)

### gen_recall_0011

- Question: Công văn số 6125/QLD-CL về việc thông báo thu hồi thuốc vi phạm mức độ 2 (Thuốc Siro uống Siro Nutrohadi F, Số GĐKLH: VD- 18684-13, Số lô: 030221; NSX: 240221; HD: 230224) thuộc cảnh báo/thu hồi nào?
- Category: recall
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_recall` / `safety_recall` / `official_registry` / Công văn số 6125/QLD-CL về việc thông báo thu hồi thuốc vi phạm mức độ 2 (Thuốc Siro uống Siro Nutrohadi F, Số GĐKLH: VD- 18684-13, Số lô: 030221; NSX: 240221; HD: 230224)

### gen_recall_0012

- Question: Cho tôi nguồn về Công văn số 6125/QLD-CL về việc thông báo thu hồi thuốc vi phạm mức độ 2 (Thuốc Siro uống Siro Nutrohadi F, Số GĐKLH: VD- 18684-13, Số lô: 030221; NSX: 240221; HD: 230224)
- Category: recall
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_recall` / `safety_recall` / `official_registry` / Công văn số 6125/QLD-CL về việc thông báo thu hồi thuốc vi phạm mức độ 2 (Thuốc Siro uống Siro Nutrohadi F, Số GĐKLH: VD- 18684-13, Số lô: 030221; NSX: 240221; HD: 230224)

### gen_recall_0013

- Question: Công văn số 10275/QLD-CL về việc thu hồi thuốc Batiwell, lô số 00121 có phải thông báo thu hồi không?
- Category: recall
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_recall` / `safety_recall` / `official_registry` / Công văn số 10275/QLD-CL về việc thu hồi thuốc Batiwell, lô số 00121

### gen_recall_0014

- Question: Công văn số 10275/QLD-CL về việc thu hồi thuốc Batiwell, lô số 00121 thuộc cảnh báo/thu hồi nào?
- Category: recall
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_recall` / `safety_recall` / `official_registry` / Công văn số 10275/QLD-CL về việc thu hồi thuốc Batiwell, lô số 00121

### gen_recall_0015

- Question: Cho tôi nguồn về Công văn số 10275/QLD-CL về việc thu hồi thuốc Batiwell, lô số 00121
- Category: recall
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_recall` / `safety_recall` / `official_registry` / Công văn số 10275/QLD-CL về việc thu hồi thuốc Batiwell, lô số 00121

### gen_recall_0016

- Question: Công văn số 2808/QLD-CL về việc đình chỉ lưu hành thuốc không đạt tiêu chuẩn chất lượng (Thuốc tiêm B-Comene) có phải thông báo thu hồi không?
- Category: recall
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_recall` / `safety_recall` / `official_registry` / Công văn số 2808/QLD-CL về việc đình chỉ lưu hành thuốc không đạt tiêu chuẩn chất lượng (Thuốc tiêm B-Comene)

### gen_recall_0017

- Question: Công văn số 2808/QLD-CL về việc đình chỉ lưu hành thuốc không đạt tiêu chuẩn chất lượng (Thuốc tiêm B-Comene) thuộc cảnh báo/thu hồi nào?
- Category: recall
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_recall` / `safety_recall` / `official_registry` / Công văn số 2808/QLD-CL về việc đình chỉ lưu hành thuốc không đạt tiêu chuẩn chất lượng (Thuốc tiêm B-Comene)

### gen_recall_0018

- Question: Cho tôi nguồn về Công văn số 2808/QLD-CL về việc đình chỉ lưu hành thuốc không đạt tiêu chuẩn chất lượng (Thuốc tiêm B-Comene)
- Category: recall
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_recall` / `safety_recall` / `official_registry` / Công văn số 2808/QLD-CL về việc đình chỉ lưu hành thuốc không đạt tiêu chuẩn chất lượng (Thuốc tiêm B-Comene)

### gen_recall_0019

- Question: Công văn số 9155/QLD-CL về việc thông báo thu hồi thuốc vi phạm mức độ 3 (Hỗn dịch uống Sucrate gel (Sucralfate 1g/5ml)) có phải thông báo thu hồi không?
- Category: recall
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_recall` / `safety_recall` / `official_registry` / Công văn số 9155/QLD-CL về việc thông báo thu hồi thuốc vi phạm mức độ 3 (Hỗn dịch uống Sucrate gel (Sucralfate 1g/5ml))

### gen_recall_0020

- Question: Công văn số 9155/QLD-CL về việc thông báo thu hồi thuốc vi phạm mức độ 3 (Hỗn dịch uống Sucrate gel (Sucralfate 1g/5ml)) thuộc cảnh báo/thu hồi nào?
- Category: recall
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_recall` / `safety_recall` / `official_registry` / Công văn số 9155/QLD-CL về việc thông báo thu hồi thuốc vi phạm mức độ 3 (Hỗn dịch uống Sucrate gel (Sucralfate 1g/5ml))

### gen_recall_0021

- Question: Cho tôi nguồn về Công văn số 9155/QLD-CL về việc thông báo thu hồi thuốc vi phạm mức độ 3 (Hỗn dịch uống Sucrate gel (Sucralfate 1g/5ml))
- Category: recall
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_recall` / `safety_recall` / `official_registry` / Công văn số 9155/QLD-CL về việc thông báo thu hồi thuốc vi phạm mức độ 3 (Hỗn dịch uống Sucrate gel (Sucralfate 1g/5ml))

### gen_recall_0022

- Question: Công văn số 235/QLD-CL về việc đình chỉ lưu hành thuốc không đạt tiêu chuẩn chất lượng (viên nén Young II Captopril Tablet (Captopril 25mg)) có phải thông báo thu hồi không?
- Category: recall
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_recall` / `safety_recall` / `official_registry` / Công văn số 235/QLD-CL về việc đình chỉ lưu hành thuốc không đạt tiêu chuẩn chất lượng (viên nén Young II Captopril Tablet (Captopril 25mg))

### gen_recall_0023

- Question: Công văn số 235/QLD-CL về việc đình chỉ lưu hành thuốc không đạt tiêu chuẩn chất lượng (viên nén Young II Captopril Tablet (Captopril 25mg)) thuộc cảnh báo/thu hồi nào?
- Category: recall
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_recall` / `safety_recall` / `official_registry` / Công văn số 235/QLD-CL về việc đình chỉ lưu hành thuốc không đạt tiêu chuẩn chất lượng (viên nén Young II Captopril Tablet (Captopril 25mg))

### gen_recall_0024

- Question: Cho tôi nguồn về Công văn số 235/QLD-CL về việc đình chỉ lưu hành thuốc không đạt tiêu chuẩn chất lượng (viên nén Young II Captopril Tablet (Captopril 25mg))
- Category: recall
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_recall` / `safety_recall` / `official_registry` / Công văn số 235/QLD-CL về việc đình chỉ lưu hành thuốc không đạt tiêu chuẩn chất lượng (viên nén Young II Captopril Tablet (Captopril 25mg))

### gen_recall_0025

- Question: Công văn số 8968/QLD-CL về việc xử lý thuốc Amoxicillin 500mg không đạt chất lượng có phải thông báo thu hồi không?
- Category: recall
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_recall` / `safety_recall` / `official_registry` / Công văn số 8968/QLD-CL về việc xử lý thuốc Amoxicillin 500mg không đạt chất lượng

### gen_recall_0026

- Question: Công văn số 8968/QLD-CL về việc xử lý thuốc Amoxicillin 500mg không đạt chất lượng thuộc cảnh báo/thu hồi nào?
- Category: recall
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_recall` / `safety_recall` / `official_registry` / Công văn số 8968/QLD-CL về việc xử lý thuốc Amoxicillin 500mg không đạt chất lượng

### gen_recall_0027

- Question: Cho tôi nguồn về Công văn số 8968/QLD-CL về việc xử lý thuốc Amoxicillin 500mg không đạt chất lượng
- Category: recall
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_recall` / `safety_recall` / `official_registry` / Công văn số 8968/QLD-CL về việc xử lý thuốc Amoxicillin 500mg không đạt chất lượng

### gen_recall_0028

- Question: Đình chỉ lưu hành thuốc không đạt tiêu chuẩn chất lượng (Viên nén bao phim Unicet (Cetirizin hydroclorid 10mg)) có phải thông báo thu hồi không?
- Category: recall
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_recall` / `safety_recall` / `official_registry` / Đình chỉ lưu hành thuốc không đạt tiêu chuẩn chất lượng (Viên nén bao phim Unicet (Cetirizin hydroclorid 10mg))

### gen_recall_0029

- Question: Đình chỉ lưu hành thuốc không đạt tiêu chuẩn chất lượng (Viên nén bao phim Unicet (Cetirizin hydroclorid 10mg)) thuộc cảnh báo/thu hồi nào?
- Category: recall
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_recall` / `safety_recall` / `official_registry` / Đình chỉ lưu hành thuốc không đạt tiêu chuẩn chất lượng (Viên nén bao phim Unicet (Cetirizin hydroclorid 10mg))

### gen_recall_0030

- Question: Cho tôi nguồn về Đình chỉ lưu hành thuốc không đạt tiêu chuẩn chất lượng (Viên nén bao phim Unicet (Cetirizin hydroclorid 10mg))
- Category: recall
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_recall` / `safety_recall` / `official_registry` / Đình chỉ lưu hành thuốc không đạt tiêu chuẩn chất lượng (Viên nén bao phim Unicet (Cetirizin hydroclorid 10mg))

### gen_recall_0031

- Question: thu hồi thuốc Femancia, số đăng ký: VD-27929-17 có phải thông báo thu hồi không?
- Category: recall
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_recall` / `safety_recall` / `official_registry` / Quyết định số 358/QĐ-QLD về việc thu hồi thuốc Femancia, số đăng ký: VD-27929-17

### gen_recall_0032

- Question: thu hồi thuốc Femancia, số đăng ký: VD-27929-17 thuộc cảnh báo/thu hồi nào?
- Category: recall
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_recall` / `safety_recall` / `official_registry` / Quyết định số 358/QĐ-QLD về việc thu hồi thuốc Femancia, số đăng ký: VD-27929-17

### gen_recall_0033

- Question: Cho tôi nguồn về thu hồi thuốc Femancia, số đăng ký: VD-27929-17
- Category: recall
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_recall` / `safety_recall` / `official_registry` / Quyết định số 358/QĐ-QLD về việc thu hồi thuốc Femancia, số đăng ký: VD-27929-17

### gen_recall_0034

- Question: Công văn số 18286/QLD-CL về việc thông báo thu hồi thuốc vi phạm mức độ 3 (viên nang mềm Bronzoni) có phải thông báo thu hồi không?
- Category: recall
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_recall` / `safety_recall` / `official_registry` / Công văn số 18286/QLD-CL về việc thông báo thu hồi thuốc vi phạm mức độ 3 (viên nang mềm Bronzoni)

### gen_recall_0035

- Question: Công văn số 18286/QLD-CL về việc thông báo thu hồi thuốc vi phạm mức độ 3 (viên nang mềm Bronzoni) thuộc cảnh báo/thu hồi nào?
- Category: recall
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_recall` / `safety_recall` / `official_registry` / Công văn số 18286/QLD-CL về việc thông báo thu hồi thuốc vi phạm mức độ 3 (viên nang mềm Bronzoni)

### gen_recall_0036

- Question: Cho tôi nguồn về Công văn số 18286/QLD-CL về việc thông báo thu hồi thuốc vi phạm mức độ 3 (viên nang mềm Bronzoni)
- Category: recall
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_recall` / `safety_recall` / `official_registry` / Công văn số 18286/QLD-CL về việc thông báo thu hồi thuốc vi phạm mức độ 3 (viên nang mềm Bronzoni)

### gen_recall_0037

- Question: Công văn số 1223/QLD-CL về việc thông báo thu hồi thuốc Tobradico ((Tobramycin (dưới dạng Tobramycin sulfat) 15mg/5ml), Số GĐKLH: VD-19202-13, Số lô: 0031022, NSX: 02/10/2022, HD:  có phải thông báo thu hồi không?
- Category: recall
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_recall` / `safety_recall` / `official_registry` / Công văn số 1223/QLD-CL về việc thông báo thu hồi thuốc Tobradico ((Tobramycin (dưới dạng Tobramycin sulfat) 15mg/5ml), Số GĐKLH: VD-19202-13, Số lô: 0031022, NSX: 02/10/2022, HD: 02/10/2024)

### gen_recall_0038

- Question: Công văn số 1223/QLD-CL về việc thông báo thu hồi thuốc Tobradico ((Tobramycin (dưới dạng Tobramycin sulfat) 15mg/5ml), Số GĐKLH: VD-19202-13, Số lô: 0031022, NSX: 02/10/2022, HD:  thuộc cảnh báo/thu hồi nào?
- Category: recall
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_recall` / `safety_recall` / `official_registry` / Công văn số 1223/QLD-CL về việc thông báo thu hồi thuốc Tobradico ((Tobramycin (dưới dạng Tobramycin sulfat) 15mg/5ml), Số GĐKLH: VD-19202-13, Số lô: 0031022, NSX: 02/10/2022, HD: 02/10/2024)

### gen_recall_0039

- Question: Cho tôi nguồn về Công văn số 1223/QLD-CL về việc thông báo thu hồi thuốc Tobradico ((Tobramycin (dưới dạng Tobramycin sulfat) 15mg/5ml), Số GĐKLH: VD-19202-13, Số lô: 0031022, NSX: 02/10/2022, HD: 
- Category: recall
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_recall` / `safety_recall` / `official_registry` / Công văn số 1223/QLD-CL về việc thông báo thu hồi thuốc Tobradico ((Tobramycin (dưới dạng Tobramycin sulfat) 15mg/5ml), Số GĐKLH: VD-19202-13, Số lô: 0031022, NSX: 02/10/2022, HD: 02/10/2024)

### gen_recall_0040

- Question: Công văn số 5555/QLD-CL về việc đình chỉ lưu hành thuốc Dekasiam không đạt tiêu chuẩn chất lượng có phải thông báo thu hồi không?
- Category: recall
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_recall` / `safety_recall` / `official_registry` / Công văn số 5555/QLD-CL về việc đình chỉ lưu hành thuốc Dekasiam không đạt tiêu chuẩn chất lượng

### gen_recall_0041

- Question: Công văn số 5555/QLD-CL về việc đình chỉ lưu hành thuốc Dekasiam không đạt tiêu chuẩn chất lượng thuộc cảnh báo/thu hồi nào?
- Category: recall
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_recall` / `safety_recall` / `official_registry` / Công văn số 5555/QLD-CL về việc đình chỉ lưu hành thuốc Dekasiam không đạt tiêu chuẩn chất lượng

### gen_recall_0042

- Question: Cho tôi nguồn về Công văn số 5555/QLD-CL về việc đình chỉ lưu hành thuốc Dekasiam không đạt tiêu chuẩn chất lượng
- Category: recall
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_recall` / `safety_recall` / `official_registry` / Công văn số 5555/QLD-CL về việc đình chỉ lưu hành thuốc Dekasiam không đạt tiêu chuẩn chất lượng

### gen_recall_0043

- Question: Công văn số 2984/QLD-CL về việc thông báo thu hồi thuốc vi phạm mức độ 2 (Viên nén Navacarzol (Carbimazole 5mg)) có phải thông báo thu hồi không?
- Category: recall
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_recall` / `safety_recall` / `official_registry` / Công văn số 2984/QLD-CL về việc thông báo thu hồi thuốc vi phạm mức độ 2 (Viên nén Navacarzol (Carbimazole 5mg))

### gen_recall_0044

- Question: Công văn số 2984/QLD-CL về việc thông báo thu hồi thuốc vi phạm mức độ 2 (Viên nén Navacarzol (Carbimazole 5mg)) thuộc cảnh báo/thu hồi nào?
- Category: recall
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_recall` / `safety_recall` / `official_registry` / Công văn số 2984/QLD-CL về việc thông báo thu hồi thuốc vi phạm mức độ 2 (Viên nén Navacarzol (Carbimazole 5mg))

### gen_recall_0045

- Question: Cho tôi nguồn về Công văn số 2984/QLD-CL về việc thông báo thu hồi thuốc vi phạm mức độ 2 (Viên nén Navacarzol (Carbimazole 5mg))
- Category: recall
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_recall` / `safety_recall` / `official_registry` / Công văn số 2984/QLD-CL về việc thông báo thu hồi thuốc vi phạm mức độ 2 (Viên nén Navacarzol (Carbimazole 5mg))

### gen_recall_0046

- Question: Công văn số 598/QLD-CL về việc thông báo thu hồi thuốc vi phạm mức độ 3 (viên nang cứng Fluconazole (Fluconazole 150mg), Số GĐKLH: VN-16474-13, Số lô: KE22638; NSX: 10/10/2022; HD: có phải thông báo thu hồi không?
- Category: recall
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_recall` / `safety_recall` / `official_registry` / Công văn số 598/QLD-CL về việc thông báo thu hồi thuốc vi phạm mức độ 3 (viên nang cứng Fluconazole (Fluconazole 150mg), Số GĐKLH: VN-16474-13, Số lô: KE22638; NSX: 10/10/2022; HD: 09/10/2025)

### gen_recall_0047

- Question: Công văn số 598/QLD-CL về việc thông báo thu hồi thuốc vi phạm mức độ 3 (viên nang cứng Fluconazole (Fluconazole 150mg), Số GĐKLH: VN-16474-13, Số lô: KE22638; NSX: 10/10/2022; HD: thuộc cảnh báo/thu hồi nào?
- Category: recall
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_recall` / `safety_recall` / `official_registry` / Công văn số 598/QLD-CL về việc thông báo thu hồi thuốc vi phạm mức độ 3 (viên nang cứng Fluconazole (Fluconazole 150mg), Số GĐKLH: VN-16474-13, Số lô: KE22638; NSX: 10/10/2022; HD: 09/10/2025)

### gen_recall_0048

- Question: Cho tôi nguồn về Công văn số 598/QLD-CL về việc thông báo thu hồi thuốc vi phạm mức độ 3 (viên nang cứng Fluconazole (Fluconazole 150mg), Số GĐKLH: VN-16474-13, Số lô: KE22638; NSX: 10/10/2022; HD:
- Category: recall
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_recall` / `safety_recall` / `official_registry` / Công văn số 598/QLD-CL về việc thông báo thu hồi thuốc vi phạm mức độ 3 (viên nang cứng Fluconazole (Fluconazole 150mg), Số GĐKLH: VN-16474-13, Số lô: KE22638; NSX: 10/10/2022; HD: 09/10/2025)

### gen_recall_0049

- Question: Công văn số 2899/QLD-CL về việc đình chỉ lưu hành thuốc không đạt tiêu chuẩn chất lượng (Viên nén Alsoben) có phải thông báo thu hồi không?
- Category: recall
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_recall` / `safety_recall` / `official_registry` / Công văn số 2899/QLD-CL về việc đình chỉ lưu hành thuốc không đạt tiêu chuẩn chất lượng (Viên nén Alsoben)

### gen_recall_0050

- Question: Công văn số 2899/QLD-CL về việc đình chỉ lưu hành thuốc không đạt tiêu chuẩn chất lượng (Viên nén Alsoben) thuộc cảnh báo/thu hồi nào?
- Category: recall
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_recall` / `safety_recall` / `official_registry` / Công văn số 2899/QLD-CL về việc đình chỉ lưu hành thuốc không đạt tiêu chuẩn chất lượng (Viên nén Alsoben)

### gen_recall_0051

- Question: Cho tôi nguồn về Công văn số 2899/QLD-CL về việc đình chỉ lưu hành thuốc không đạt tiêu chuẩn chất lượng (Viên nén Alsoben)
- Category: recall
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_recall` / `safety_recall` / `official_registry` / Công văn số 2899/QLD-CL về việc đình chỉ lưu hành thuốc không đạt tiêu chuẩn chất lượng (Viên nén Alsoben)

### gen_recall_0052

- Question: Công văn số 712/QLD-CL về việc thông báo thu hồi thuốc vi phạm mức độ 2 (viên nang cứng Femancia (Sắt nguyên tố (dưới dạng Sắt fumarat 305 mg) 100 mg; Acid Folic 350 mcg), Số GĐKLH có phải thông báo thu hồi không?
- Category: recall
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_recall` / `safety_recall` / `official_registry` / Công văn số 712/QLD-CL về việc thông báo thu hồi thuốc vi phạm mức độ 2 (viên nang cứng Femancia (Sắt nguyên tố (dưới dạng Sắt fumarat 305 mg) 100 mg; Acid Folic 350 mcg), Số GĐKLH: VD-27929-17)

### gen_recall_0053

- Question: Công văn số 712/QLD-CL về việc thông báo thu hồi thuốc vi phạm mức độ 2 (viên nang cứng Femancia (Sắt nguyên tố (dưới dạng Sắt fumarat 305 mg) 100 mg; Acid Folic 350 mcg), Số GĐKLH thuộc cảnh báo/thu hồi nào?
- Category: recall
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_recall` / `safety_recall` / `official_registry` / Công văn số 712/QLD-CL về việc thông báo thu hồi thuốc vi phạm mức độ 2 (viên nang cứng Femancia (Sắt nguyên tố (dưới dạng Sắt fumarat 305 mg) 100 mg; Acid Folic 350 mcg), Số GĐKLH: VD-27929-17)

### gen_recall_0054

- Question: Cho tôi nguồn về Công văn số 712/QLD-CL về việc thông báo thu hồi thuốc vi phạm mức độ 2 (viên nang cứng Femancia (Sắt nguyên tố (dưới dạng Sắt fumarat 305 mg) 100 mg; Acid Folic 350 mcg), Số GĐKLH
- Category: recall
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_recall` / `safety_recall` / `official_registry` / Công văn số 712/QLD-CL về việc thông báo thu hồi thuốc vi phạm mức độ 2 (viên nang cứng Femancia (Sắt nguyên tố (dưới dạng Sắt fumarat 305 mg) 100 mg; Acid Folic 350 mcg), Số GĐKLH: VD-27929-17)

### gen_recall_0055

- Question: Công văn số 9058/QLD-CL về việc thông báo thu hồi thuốc vi phạm mức độ 3 (Viên nang cứng H-inzole, Số GĐKLH: VN-18555-14, Số lô: HT4-51, NSX: 18/10/2022, HD: 17/10/2024) có phải thông báo thu hồi không?
- Category: recall
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_recall` / `safety_recall` / `official_registry` / Công văn số 9058/QLD-CL về việc thông báo thu hồi thuốc vi phạm mức độ 3 (Viên nang cứng H-inzole, Số GĐKLH: VN-18555-14, Số lô: HT4-51, NSX: 18/10/2022, HD: 17/10/2024)

### gen_recall_0056

- Question: Công văn số 9058/QLD-CL về việc thông báo thu hồi thuốc vi phạm mức độ 3 (Viên nang cứng H-inzole, Số GĐKLH: VN-18555-14, Số lô: HT4-51, NSX: 18/10/2022, HD: 17/10/2024) thuộc cảnh báo/thu hồi nào?
- Category: recall
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_recall` / `safety_recall` / `official_registry` / Công văn số 9058/QLD-CL về việc thông báo thu hồi thuốc vi phạm mức độ 3 (Viên nang cứng H-inzole, Số GĐKLH: VN-18555-14, Số lô: HT4-51, NSX: 18/10/2022, HD: 17/10/2024)

### gen_recall_0057

- Question: Cho tôi nguồn về Công văn số 9058/QLD-CL về việc thông báo thu hồi thuốc vi phạm mức độ 3 (Viên nang cứng H-inzole, Số GĐKLH: VN-18555-14, Số lô: HT4-51, NSX: 18/10/2022, HD: 17/10/2024)
- Category: recall
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_recall` / `safety_recall` / `official_registry` / Công văn số 9058/QLD-CL về việc thông báo thu hồi thuốc vi phạm mức độ 3 (Viên nang cứng H-inzole, Số GĐKLH: VN-18555-14, Số lô: HT4-51, NSX: 18/10/2022, HD: 17/10/2024)

### gen_recall_0058

- Question: Công văn số 884/QLD-CL đình chỉ lưu hành thuốc không đạt tiêu chuẩn chất lượng (Chymomedi (Chymotrypsin 21 microkatals)) có phải thông báo thu hồi không?
- Category: recall
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_recall` / `safety_recall` / `official_registry` / Công văn số 884/QLD-CL đình chỉ lưu hành thuốc không đạt tiêu chuẩn chất lượng (Chymomedi (Chymotrypsin 21 microkatals))

### gen_recall_0059

- Question: Công văn số 884/QLD-CL đình chỉ lưu hành thuốc không đạt tiêu chuẩn chất lượng (Chymomedi (Chymotrypsin 21 microkatals)) thuộc cảnh báo/thu hồi nào?
- Category: recall
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_recall` / `safety_recall` / `official_registry` / Công văn số 884/QLD-CL đình chỉ lưu hành thuốc không đạt tiêu chuẩn chất lượng (Chymomedi (Chymotrypsin 21 microkatals))

### gen_recall_0060

- Question: Cho tôi nguồn về Công văn số 884/QLD-CL đình chỉ lưu hành thuốc không đạt tiêu chuẩn chất lượng (Chymomedi (Chymotrypsin 21 microkatals))
- Category: recall
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_recall` / `safety_recall` / `official_registry` / Công văn số 884/QLD-CL đình chỉ lưu hành thuốc không đạt tiêu chuẩn chất lượng (Chymomedi (Chymotrypsin 21 microkatals))

### gen_recall_0061

- Question: Công văn số 11924/QLD-CL về việc thông báo thu hồi thuốc vi phạm mức độ 2 (thuốc Genpharmason) có phải thông báo thu hồi không?
- Category: recall
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_recall` / `safety_recall` / `official_registry` / Công văn số 11924/QLD-CL về việc thông báo thu hồi thuốc vi phạm mức độ 2 (thuốc Genpharmason)

### gen_recall_0062

- Question: Công văn số 11924/QLD-CL về việc thông báo thu hồi thuốc vi phạm mức độ 2 (thuốc Genpharmason) thuộc cảnh báo/thu hồi nào?
- Category: recall
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_recall` / `safety_recall` / `official_registry` / Công văn số 11924/QLD-CL về việc thông báo thu hồi thuốc vi phạm mức độ 2 (thuốc Genpharmason)

### gen_recall_0063

- Question: Cho tôi nguồn về Công văn số 11924/QLD-CL về việc thông báo thu hồi thuốc vi phạm mức độ 2 (thuốc Genpharmason)
- Category: recall
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_recall` / `safety_recall` / `official_registry` / Công văn số 11924/QLD-CL về việc thông báo thu hồi thuốc vi phạm mức độ 2 (thuốc Genpharmason)

### gen_recall_0064

- Question: Công văn số 19664/QLD-CL về việc thu hồi thuốc Aciclovir không đạt tiêu chuẩn chất lượng có phải thông báo thu hồi không?
- Category: recall
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_recall` / `safety_recall` / `official_registry` / Công văn số 19664/QLD-CL về việc thu hồi thuốc Aciclovir không đạt tiêu chuẩn chất lượng

### gen_recall_0065

- Question: Công văn số 19664/QLD-CL về việc thu hồi thuốc Aciclovir không đạt tiêu chuẩn chất lượng thuộc cảnh báo/thu hồi nào?
- Category: recall
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_recall` / `safety_recall` / `official_registry` / Công văn số 19664/QLD-CL về việc thu hồi thuốc Aciclovir không đạt tiêu chuẩn chất lượng

### gen_recall_0066

- Question: Cho tôi nguồn về Công văn số 19664/QLD-CL về việc thu hồi thuốc Aciclovir không đạt tiêu chuẩn chất lượng
- Category: recall
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_recall` / `safety_recall` / `official_registry` / Công văn số 19664/QLD-CL về việc thu hồi thuốc Aciclovir không đạt tiêu chuẩn chất lượng

### gen_recall_0067

- Question: Công văn số 19942/QLD-CL về việc đình chỉ lưu hành thuốc không đạt tiêu chuẩn chất lượng (Young II Captopril) có phải thông báo thu hồi không?
- Category: recall
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_recall` / `safety_recall` / `official_registry` / Công văn số 19942/QLD-CL về việc đình chỉ lưu hành thuốc không đạt tiêu chuẩn chất lượng (Young II Captopril)

### gen_recall_0068

- Question: Công văn số 19942/QLD-CL về việc đình chỉ lưu hành thuốc không đạt tiêu chuẩn chất lượng (Young II Captopril) thuộc cảnh báo/thu hồi nào?
- Category: recall
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_recall` / `safety_recall` / `official_registry` / Công văn số 19942/QLD-CL về việc đình chỉ lưu hành thuốc không đạt tiêu chuẩn chất lượng (Young II Captopril)

### gen_recall_0069

- Question: Cho tôi nguồn về Công văn số 19942/QLD-CL về việc đình chỉ lưu hành thuốc không đạt tiêu chuẩn chất lượng (Young II Captopril)
- Category: recall
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_recall` / `safety_recall` / `official_registry` / Công văn số 19942/QLD-CL về việc đình chỉ lưu hành thuốc không đạt tiêu chuẩn chất lượng (Young II Captopril)

### gen_recall_0070

- Question: Công văn số 17463/QLD-CL về việc thông báo thu hồi thuốc Sedtyl, lô 03M19 có phải thông báo thu hồi không?
- Category: recall
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_recall` / `safety_recall` / `official_registry` / Công văn số 17463/QLD-CL về việc thông báo thu hồi thuốc Sedtyl, lô 03M19

### gen_recall_0071

- Question: Công văn số 17463/QLD-CL về việc thông báo thu hồi thuốc Sedtyl, lô 03M19 thuộc cảnh báo/thu hồi nào?
- Category: recall
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_recall` / `safety_recall` / `official_registry` / Công văn số 17463/QLD-CL về việc thông báo thu hồi thuốc Sedtyl, lô 03M19

### gen_recall_0072

- Question: Cho tôi nguồn về Công văn số 17463/QLD-CL về việc thông báo thu hồi thuốc Sedtyl, lô 03M19
- Category: recall
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_recall` / `safety_recall` / `official_registry` / Công văn số 17463/QLD-CL về việc thông báo thu hồi thuốc Sedtyl, lô 03M19

### gen_recall_0073

- Question: Công văn số 883/QLD-CL đình chỉ lưu hành thuốc không đạt tiêu chuẩn chất lượng (Viên nén bao phim Peridom-M) có phải thông báo thu hồi không?
- Category: recall
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_recall` / `safety_recall` / `official_registry` / Công văn số 883/QLD-CL đình chỉ lưu hành thuốc không đạt tiêu chuẩn chất lượng (Viên nén bao phim Peridom-M)

### gen_recall_0074

- Question: Công văn số 883/QLD-CL đình chỉ lưu hành thuốc không đạt tiêu chuẩn chất lượng (Viên nén bao phim Peridom-M) thuộc cảnh báo/thu hồi nào?
- Category: recall
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_recall` / `safety_recall` / `official_registry` / Công văn số 883/QLD-CL đình chỉ lưu hành thuốc không đạt tiêu chuẩn chất lượng (Viên nén bao phim Peridom-M)

### gen_recall_0075

- Question: Cho tôi nguồn về Công văn số 883/QLD-CL đình chỉ lưu hành thuốc không đạt tiêu chuẩn chất lượng (Viên nén bao phim Peridom-M)
- Category: recall
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_recall` / `safety_recall` / `official_registry` / Công văn số 883/QLD-CL đình chỉ lưu hành thuốc không đạt tiêu chuẩn chất lượng (Viên nén bao phim Peridom-M)

### gen_recall_0076

- Question: Công văn 16457/QLD-CL về việc thu hồi thuốc Clavophynamox 1000 không đạt tiêu chuẩn chất luợng có phải thông báo thu hồi không?
- Category: recall
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_recall` / `safety_recall` / `official_registry` / Công văn 16457/QLD-CL về việc thu hồi thuốc Clavophynamox 1000 không đạt tiêu chuẩn chất luợng

### gen_recall_0077

- Question: Công văn 16457/QLD-CL về việc thu hồi thuốc Clavophynamox 1000 không đạt tiêu chuẩn chất luợng thuộc cảnh báo/thu hồi nào?
- Category: recall
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_recall` / `safety_recall` / `official_registry` / Công văn 16457/QLD-CL về việc thu hồi thuốc Clavophynamox 1000 không đạt tiêu chuẩn chất luợng

### gen_recall_0078

- Question: Cho tôi nguồn về Công văn 16457/QLD-CL về việc thu hồi thuốc Clavophynamox 1000 không đạt tiêu chuẩn chất luợng
- Category: recall
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_recall` / `safety_recall` / `official_registry` / Công văn 16457/QLD-CL về việc thu hồi thuốc Clavophynamox 1000 không đạt tiêu chuẩn chất luợng

### gen_recall_0079

- Question: Công văn số 16746/QLD-CL về việc chất lượng thuốc dung dịch thuốc tiêm Protamine Choay 1000 U.A.H/ml có phải thông báo thu hồi không?
- Category: recall
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_recall` / `safety_recall` / `official_registry` / Công văn số 16746/QLD-CL về việc chất lượng thuốc dung dịch thuốc tiêm Protamine Choay 1000 U.A.H/ml

### gen_recall_0080

- Question: Công văn số 16746/QLD-CL về việc chất lượng thuốc dung dịch thuốc tiêm Protamine Choay 1000 U.A.H/ml thuộc cảnh báo/thu hồi nào?
- Category: recall
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_recall` / `safety_recall` / `official_registry` / Công văn số 16746/QLD-CL về việc chất lượng thuốc dung dịch thuốc tiêm Protamine Choay 1000 U.A.H/ml

### gen_recall_0081

- Question: Cho tôi nguồn về Công văn số 16746/QLD-CL về việc chất lượng thuốc dung dịch thuốc tiêm Protamine Choay 1000 U.A.H/ml
- Category: recall
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_recall` / `safety_recall` / `official_registry` / Công văn số 16746/QLD-CL về việc chất lượng thuốc dung dịch thuốc tiêm Protamine Choay 1000 U.A.H/ml

### gen_recall_0082

- Question: Công văn số 2825/QLD-CL về việc thông báo thu hồi thuốc vi phạm mức độ 2 (Viên nén dài bao phim Cefaclor 375mg (Cefaclor), Số GĐKLH: VD-14047-11, Số lô: 0124 NSX: 23/01/24 HD: 23/0 có phải thông báo thu hồi không?
- Category: recall
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_recall` / `safety_recall` / `official_registry` / Công văn số 2825/QLD-CL về việc thông báo thu hồi thuốc vi phạm mức độ 2 (Viên nén dài bao phim Cefaclor 375mg (Cefaclor), Số GĐKLH: VD-14047-11, Số lô: 0124 NSX: 23/01/24 HD: 23/01/27 do Chi nhánh Công ty cổ phần dược phẩm và sinh học y tế sản xuất)

### gen_recall_0083

- Question: Công văn số 2825/QLD-CL về việc thông báo thu hồi thuốc vi phạm mức độ 2 (Viên nén dài bao phim Cefaclor 375mg (Cefaclor), Số GĐKLH: VD-14047-11, Số lô: 0124 NSX: 23/01/24 HD: 23/0 thuộc cảnh báo/thu hồi nào?
- Category: recall
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_recall` / `safety_recall` / `official_registry` / Công văn số 2825/QLD-CL về việc thông báo thu hồi thuốc vi phạm mức độ 2 (Viên nén dài bao phim Cefaclor 375mg (Cefaclor), Số GĐKLH: VD-14047-11, Số lô: 0124 NSX: 23/01/24 HD: 23/01/27 do Chi nhánh Công ty cổ phần dược phẩm và sinh học y tế sản xuất)

### gen_recall_0084

- Question: Cho tôi nguồn về Công văn số 2825/QLD-CL về việc thông báo thu hồi thuốc vi phạm mức độ 2 (Viên nén dài bao phim Cefaclor 375mg (Cefaclor), Số GĐKLH: VD-14047-11, Số lô: 0124 NSX: 23/01/24 HD: 23/0
- Category: recall
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_recall` / `safety_recall` / `official_registry` / Công văn số 2825/QLD-CL về việc thông báo thu hồi thuốc vi phạm mức độ 2 (Viên nén dài bao phim Cefaclor 375mg (Cefaclor), Số GĐKLH: VD-14047-11, Số lô: 0124 NSX: 23/01/24 HD: 23/01/27 do Chi nhánh Công ty cổ phần dược phẩm và sinh học y tế sản xuất)

### gen_recall_0085

- Question: Công văn số 9586/QLD-CL về việc thu hồi thuốc không đạt chất lượng (Dung dịch uống Batiwell (Bromhexin hydroclorid 0,8mg/ml), Số ĐKLH: VD-31011-18, Số kiểm soát: 00121, NSX: 08/03/ có phải thông báo thu hồi không?
- Category: recall
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_recall` / `safety_recall` / `official_registry` / Công văn số 9586/QLD-CL về việc thu hồi thuốc không đạt chất lượng (Dung dịch uống Batiwell (Bromhexin hydroclorid 0,8mg/ml), Số ĐKLH: VD-31011-18, Số kiểm soát: 00121, NSX: 08/03/2021, HD: 08/03/2024)

### gen_recall_0086

- Question: Công văn số 9586/QLD-CL về việc thu hồi thuốc không đạt chất lượng (Dung dịch uống Batiwell (Bromhexin hydroclorid 0,8mg/ml), Số ĐKLH: VD-31011-18, Số kiểm soát: 00121, NSX: 08/03/ thuộc cảnh báo/thu hồi nào?
- Category: recall
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_recall` / `safety_recall` / `official_registry` / Công văn số 9586/QLD-CL về việc thu hồi thuốc không đạt chất lượng (Dung dịch uống Batiwell (Bromhexin hydroclorid 0,8mg/ml), Số ĐKLH: VD-31011-18, Số kiểm soát: 00121, NSX: 08/03/2021, HD: 08/03/2024)

### gen_recall_0087

- Question: Cho tôi nguồn về Công văn số 9586/QLD-CL về việc thu hồi thuốc không đạt chất lượng (Dung dịch uống Batiwell (Bromhexin hydroclorid 0,8mg/ml), Số ĐKLH: VD-31011-18, Số kiểm soát: 00121, NSX: 08/03/
- Category: recall
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_recall` / `safety_recall` / `official_registry` / Công văn số 9586/QLD-CL về việc thu hồi thuốc không đạt chất lượng (Dung dịch uống Batiwell (Bromhexin hydroclorid 0,8mg/ml), Số ĐKLH: VD-31011-18, Số kiểm soát: 00121, NSX: 08/03/2021, HD: 08/03/2024)

### gen_recall_0088

- Question: Công văn số 17570/QLD-CL về việc thông báo thu hồi lô thuốc Sedtyl số lô 02L19 có phải thông báo thu hồi không?
- Category: recall
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_recall` / `safety_recall` / `official_registry` / Công văn số 17570/QLD-CL về việc  thông báo thu hồi lô thuốc Sedtyl số lô 02L19

### gen_recall_0089

- Question: Công văn số 17570/QLD-CL về việc thông báo thu hồi lô thuốc Sedtyl số lô 02L19 thuộc cảnh báo/thu hồi nào?
- Category: recall
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_recall` / `safety_recall` / `official_registry` / Công văn số 17570/QLD-CL về việc  thông báo thu hồi lô thuốc Sedtyl số lô 02L19

### gen_recall_0090

- Question: Cho tôi nguồn về Công văn số 17570/QLD-CL về việc thông báo thu hồi lô thuốc Sedtyl số lô 02L19
- Category: recall
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_recall` / `safety_recall` / `official_registry` / Công văn số 17570/QLD-CL về việc  thông báo thu hồi lô thuốc Sedtyl số lô 02L19

### gen_recall_0091

- Question: Công văn số 13021/QLD-CL về việc thông báo thu hồi thuốc Npluvico vi phạm mức độ 2 có phải thông báo thu hồi không?
- Category: recall
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_recall` / `safety_recall` / `official_registry` / Công văn số 13021/QLD-CL về việc thông báo thu hồi thuốc Npluvico vi phạm mức độ 2

### gen_recall_0092

- Question: Công văn số 13021/QLD-CL về việc thông báo thu hồi thuốc Npluvico vi phạm mức độ 2 thuộc cảnh báo/thu hồi nào?
- Category: recall
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_recall` / `safety_recall` / `official_registry` / Công văn số 13021/QLD-CL về việc thông báo thu hồi thuốc Npluvico vi phạm mức độ 2

### gen_recall_0093

- Question: Cho tôi nguồn về Công văn số 13021/QLD-CL về việc thông báo thu hồi thuốc Npluvico vi phạm mức độ 2
- Category: recall
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_recall` / `safety_recall` / `official_registry` / Công văn số 13021/QLD-CL về việc thông báo thu hồi thuốc Npluvico vi phạm mức độ 2

### gen_recall_0094

- Question: Công văn số 3716/QLD-CL về việc thông báo thu hồi thuốc vi phạm mức độ 3 (Viên nén Prednisolon 5mg (Prednisolon 5mg), Số GĐKLH: VD-27065-17, Số lô: 020523, NSX: 10/05/23, HD: 10/05 có phải thông báo thu hồi không?
- Category: recall
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_recall` / `safety_recall` / `official_registry` / Công văn số 3716/QLD-CL về việc thông báo thu hồi thuốc vi phạm mức độ 3 (Viên nén Prednisolon 5mg (Prednisolon 5mg), Số GĐKLH: VD-27065-17, Số lô: 020523, NSX: 10/05/23, HD: 10/05/26 do Công ty CP dược phẩm Tipharco sản xuất)

### gen_recall_0095

- Question: Công văn số 3716/QLD-CL về việc thông báo thu hồi thuốc vi phạm mức độ 3 (Viên nén Prednisolon 5mg (Prednisolon 5mg), Số GĐKLH: VD-27065-17, Số lô: 020523, NSX: 10/05/23, HD: 10/05 thuộc cảnh báo/thu hồi nào?
- Category: recall
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_recall` / `safety_recall` / `official_registry` / Công văn số 3716/QLD-CL về việc thông báo thu hồi thuốc vi phạm mức độ 3 (Viên nén Prednisolon 5mg (Prednisolon 5mg), Số GĐKLH: VD-27065-17, Số lô: 020523, NSX: 10/05/23, HD: 10/05/26 do Công ty CP dược phẩm Tipharco sản xuất)

### gen_recall_0096

- Question: Cho tôi nguồn về Công văn số 3716/QLD-CL về việc thông báo thu hồi thuốc vi phạm mức độ 3 (Viên nén Prednisolon 5mg (Prednisolon 5mg), Số GĐKLH: VD-27065-17, Số lô: 020523, NSX: 10/05/23, HD: 10/05
- Category: recall
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_recall` / `safety_recall` / `official_registry` / Công văn số 3716/QLD-CL về việc thông báo thu hồi thuốc vi phạm mức độ 3 (Viên nén Prednisolon 5mg (Prednisolon 5mg), Số GĐKLH: VD-27065-17, Số lô: 020523, NSX: 10/05/23, HD: 10/05/26 do Công ty CP dược phẩm Tipharco sản xuất)

### gen_recall_0097

- Question: Công văn số 2205/QLD-CL về việc thông báo thu hồi thuốc vi phạm mức độ 3 (Viên nang cứng Locobile-200 (Celecoxib 200mg), Số GĐKLH: VN-21822-19, Số lô: WLD21003E, NSX: 04/02/2021, H có phải thông báo thu hồi không?
- Category: recall
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_recall` / `safety_recall` / `official_registry` / Công văn số 2205/QLD-CL về việc  thông báo thu hồi thuốc vi  phạm mức độ 3 (Viên nang cứng Locobile-200 (Celecoxib 200mg),  Số GĐKLH: VN-21822-19, Số lô: WLD21003E, NSX: 04/02/2021, HD:  03/02/2024)

### gen_recall_0098

- Question: Công văn số 2205/QLD-CL về việc thông báo thu hồi thuốc vi phạm mức độ 3 (Viên nang cứng Locobile-200 (Celecoxib 200mg), Số GĐKLH: VN-21822-19, Số lô: WLD21003E, NSX: 04/02/2021, H thuộc cảnh báo/thu hồi nào?
- Category: recall
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_recall` / `safety_recall` / `official_registry` / Công văn số 2205/QLD-CL về việc  thông báo thu hồi thuốc vi  phạm mức độ 3 (Viên nang cứng Locobile-200 (Celecoxib 200mg),  Số GĐKLH: VN-21822-19, Số lô: WLD21003E, NSX: 04/02/2021, HD:  03/02/2024)

### gen_recall_0099

- Question: Cho tôi nguồn về Công văn số 2205/QLD-CL về việc thông báo thu hồi thuốc vi phạm mức độ 3 (Viên nang cứng Locobile-200 (Celecoxib 200mg), Số GĐKLH: VN-21822-19, Số lô: WLD21003E, NSX: 04/02/2021, H
- Category: recall
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_recall` / `safety_recall` / `official_registry` / Công văn số 2205/QLD-CL về việc  thông báo thu hồi thuốc vi  phạm mức độ 3 (Viên nang cứng Locobile-200 (Celecoxib 200mg),  Số GĐKLH: VN-21822-19, Số lô: WLD21003E, NSX: 04/02/2021, HD:  03/02/2024)

### gen_recall_0100

- Question: Công văn số 615/QLD-CL về việc thông báo thu hồi thuốc Tobraquin có phải thông báo thu hồi không?
- Category: recall
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_recall` / `safety_recall` / `official_registry` / Công văn số 615/QLD-CL về việc thông báo thu hồi thuốc Tobraquin

### gen_recall_0101

- Question: Công văn số 615/QLD-CL về việc thông báo thu hồi thuốc Tobraquin thuộc cảnh báo/thu hồi nào?
- Category: recall
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_recall` / `safety_recall` / `official_registry` / Công văn số 615/QLD-CL về việc thông báo thu hồi thuốc Tobraquin

### gen_recall_0102

- Question: Cho tôi nguồn về Công văn số 615/QLD-CL về việc thông báo thu hồi thuốc Tobraquin
- Category: recall
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_recall` / `safety_recall` / `official_registry` / Công văn số 615/QLD-CL về việc thông báo thu hồi thuốc Tobraquin

### gen_recall_0103

- Question: Công văn số 9358/QLD-CL về việc thông báo thu hồi thuốc vi phạm mức độ 2 (Viên nén bao phim PymeRoxitil (Roxithromycin 150mg), Số GĐKLH: VD-28304-17, Số lô: 010522, NSX: 18/05/2022 có phải thông báo thu hồi không?
- Category: recall
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_recall` / `safety_recall` / `official_registry` / Công văn số 9358/QLD-CL về việc thông báo thu hồi thuốc vi phạm mức độ 2 (Viên nén bao phim PymeRoxitil (Roxithromycin 150mg), Số GĐKLH: VD-28304-17, Số lô: 010522, NSX: 18/05/2022, HSD: 18/05/2025)

### gen_recall_0104

- Question: Công văn số 9358/QLD-CL về việc thông báo thu hồi thuốc vi phạm mức độ 2 (Viên nén bao phim PymeRoxitil (Roxithromycin 150mg), Số GĐKLH: VD-28304-17, Số lô: 010522, NSX: 18/05/2022 thuộc cảnh báo/thu hồi nào?
- Category: recall
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_recall` / `safety_recall` / `official_registry` / Công văn số 9358/QLD-CL về việc thông báo thu hồi thuốc vi phạm mức độ 2 (Viên nén bao phim PymeRoxitil (Roxithromycin 150mg), Số GĐKLH: VD-28304-17, Số lô: 010522, NSX: 18/05/2022, HSD: 18/05/2025)

### gen_recall_0105

- Question: Cho tôi nguồn về Công văn số 9358/QLD-CL về việc thông báo thu hồi thuốc vi phạm mức độ 2 (Viên nén bao phim PymeRoxitil (Roxithromycin 150mg), Số GĐKLH: VD-28304-17, Số lô: 010522, NSX: 18/05/2022
- Category: recall
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_recall` / `safety_recall` / `official_registry` / Công văn số 9358/QLD-CL về việc thông báo thu hồi thuốc vi phạm mức độ 2 (Viên nén bao phim PymeRoxitil (Roxithromycin 150mg), Số GĐKLH: VD-28304-17, Số lô: 010522, NSX: 18/05/2022, HSD: 18/05/2025)

### gen_recall_0106

- Question: Công văn số 3534/QLD-CL về việc thông báo thu hồi thuốc vi phạm mức độ 2 (Cốm pha hỗn dịch uống Zinnat Suspension 125mg (Cefuroxim axetil 125mg)) có phải thông báo thu hồi không?
- Category: recall
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_recall` / `safety_recall` / `official_registry` / Công văn số 3534/QLD-CL về việc thông báo thu hồi thuốc vi phạm mức độ 2 (Cốm pha hỗn dịch uống Zinnat Suspension 125mg (Cefuroxim axetil 125mg))

### gen_recall_0107

- Question: Công văn số 3534/QLD-CL về việc thông báo thu hồi thuốc vi phạm mức độ 2 (Cốm pha hỗn dịch uống Zinnat Suspension 125mg (Cefuroxim axetil 125mg)) thuộc cảnh báo/thu hồi nào?
- Category: recall
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_recall` / `safety_recall` / `official_registry` / Công văn số 3534/QLD-CL về việc thông báo thu hồi thuốc vi phạm mức độ 2 (Cốm pha hỗn dịch uống Zinnat Suspension 125mg (Cefuroxim axetil 125mg))

### gen_recall_0108

- Question: Cho tôi nguồn về Công văn số 3534/QLD-CL về việc thông báo thu hồi thuốc vi phạm mức độ 2 (Cốm pha hỗn dịch uống Zinnat Suspension 125mg (Cefuroxim axetil 125mg))
- Category: recall
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_recall` / `safety_recall` / `official_registry` / Công văn số 3534/QLD-CL về việc thông báo thu hồi thuốc vi phạm mức độ 2 (Cốm pha hỗn dịch uống Zinnat Suspension 125mg (Cefuroxim axetil 125mg))

### gen_recall_0109

- Question: Công văn số 2240/QLD-CL về việc đình chỉ lưu hành thuốc Cốm Trẻ Việt không đạt tiêu chuẩn chất lượng có phải thông báo thu hồi không?
- Category: recall
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_recall` / `safety_recall` / `official_registry` / Công văn số 2240/QLD-CL về việc đình chỉ lưu hành thuốc Cốm Trẻ Việt không đạt tiêu chuẩn chất lượng

### gen_recall_0110

- Question: Công văn số 2240/QLD-CL về việc đình chỉ lưu hành thuốc Cốm Trẻ Việt không đạt tiêu chuẩn chất lượng thuộc cảnh báo/thu hồi nào?
- Category: recall
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_recall` / `safety_recall` / `official_registry` / Công văn số 2240/QLD-CL về việc đình chỉ lưu hành thuốc Cốm Trẻ Việt không đạt tiêu chuẩn chất lượng

### gen_recall_0111

- Question: Cho tôi nguồn về Công văn số 2240/QLD-CL về việc đình chỉ lưu hành thuốc Cốm Trẻ Việt không đạt tiêu chuẩn chất lượng
- Category: recall
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_recall` / `safety_recall` / `official_registry` / Công văn số 2240/QLD-CL về việc đình chỉ lưu hành thuốc Cốm Trẻ Việt không đạt tiêu chuẩn chất lượng

### gen_recall_0112

- Question: Công văn số 424/QLD-CL về việc thông báo thu hồi thuốc Myomethol không đạt chất lượng có phải thông báo thu hồi không?
- Category: recall
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_recall` / `safety_recall` / `official_registry` / Công văn số 424/QLD-CL về việc thông báo thu hồi thuốc Myomethol không đạt chất lượng

### gen_recall_0113

- Question: Công văn số 424/QLD-CL về việc thông báo thu hồi thuốc Myomethol không đạt chất lượng thuộc cảnh báo/thu hồi nào?
- Category: recall
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_recall` / `safety_recall` / `official_registry` / Công văn số 424/QLD-CL về việc thông báo thu hồi thuốc Myomethol không đạt chất lượng

### gen_recall_0114

- Question: Cho tôi nguồn về Công văn số 424/QLD-CL về việc thông báo thu hồi thuốc Myomethol không đạt chất lượng
- Category: recall
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_recall` / `safety_recall` / `official_registry` / Công văn số 424/QLD-CL về việc thông báo thu hồi thuốc Myomethol không đạt chất lượng

### gen_recall_0115

- Question: Công văn số 1513/QLD-CL về việc thông báo thu hồi thuốc vi phạm mức độ 3 (dung dịch thuốc nhỏ mắt, tai Ofleye Drops (Ofloxacin 0,3%), Số GĐKLH: 893115586524 (SĐK cũ: VD-32740-19),  có phải thông báo thu hồi không?
- Category: recall
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_recall` / `safety_recall` / `official_registry` / Công văn số 1513/QLD-CL về việc thông báo thu hồi thuốc vi phạm mức độ 3 (dung dịch thuốc nhỏ mắt, tai Ofleye Drops (Ofloxacin 0,3%), Số GĐKLH: 893115586524 (SĐK cũ: VD-32740-19), Số lô: 011024; Ngày SX: 25/10/2024; Hạn dùng: 24/10/2027)

### gen_recall_0116

- Question: Công văn số 1513/QLD-CL về việc thông báo thu hồi thuốc vi phạm mức độ 3 (dung dịch thuốc nhỏ mắt, tai Ofleye Drops (Ofloxacin 0,3%), Số GĐKLH: 893115586524 (SĐK cũ: VD-32740-19),  thuộc cảnh báo/thu hồi nào?
- Category: recall
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_recall` / `safety_recall` / `official_registry` / Công văn số 1513/QLD-CL về việc thông báo thu hồi thuốc vi phạm mức độ 3 (dung dịch thuốc nhỏ mắt, tai Ofleye Drops (Ofloxacin 0,3%), Số GĐKLH: 893115586524 (SĐK cũ: VD-32740-19), Số lô: 011024; Ngày SX: 25/10/2024; Hạn dùng: 24/10/2027)

### gen_recall_0117

- Question: Cho tôi nguồn về Công văn số 1513/QLD-CL về việc thông báo thu hồi thuốc vi phạm mức độ 3 (dung dịch thuốc nhỏ mắt, tai Ofleye Drops (Ofloxacin 0,3%), Số GĐKLH: 893115586524 (SĐK cũ: VD-32740-19), 
- Category: recall
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_recall` / `safety_recall` / `official_registry` / Công văn số 1513/QLD-CL về việc thông báo thu hồi thuốc vi phạm mức độ 3 (dung dịch thuốc nhỏ mắt, tai Ofleye Drops (Ofloxacin 0,3%), Số GĐKLH: 893115586524 (SĐK cũ: VD-32740-19), Số lô: 011024; Ngày SX: 25/10/2024; Hạn dùng: 24/10/2027)

### gen_recall_0118

- Question: Công văn số 6058/QLD-CL thông báo thu hồi thuốc vi phạm mức độ 3 (Dung dịch uống Atisalbu (Salbutamol 2mg/5ml)) có phải thông báo thu hồi không?
- Category: recall
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_recall` / `safety_recall` / `official_registry` / Công văn số 6058/QLD-CL thông báo thu hồi thuốc vi phạm mức độ 3 (Dung dịch uống Atisalbu (Salbutamol 2mg/5ml))

### gen_recall_0119

- Question: Công văn số 6058/QLD-CL thông báo thu hồi thuốc vi phạm mức độ 3 (Dung dịch uống Atisalbu (Salbutamol 2mg/5ml)) thuộc cảnh báo/thu hồi nào?
- Category: recall
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_recall` / `safety_recall` / `official_registry` / Công văn số 6058/QLD-CL thông báo thu hồi thuốc vi phạm mức độ 3 (Dung dịch uống Atisalbu (Salbutamol 2mg/5ml))

### gen_recall_0120

- Question: Cho tôi nguồn về Công văn số 6058/QLD-CL thông báo thu hồi thuốc vi phạm mức độ 3 (Dung dịch uống Atisalbu (Salbutamol 2mg/5ml))
- Category: recall
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_recall` / `safety_recall` / `official_registry` / Công văn số 6058/QLD-CL thông báo thu hồi thuốc vi phạm mức độ 3 (Dung dịch uống Atisalbu (Salbutamol 2mg/5ml))

### gen_safety_0001

- Question: Medsafe: Bệnh phổi kẽ do thuốc là cảnh báo gì?
- Category: safety_warning
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / Medsafe: Bệnh phổi kẽ do thuốc

### gen_safety_0002

- Question: Thông tin an toàn về Medsafe: Bệnh phổi kẽ do thuốc
- Category: safety_warning
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / Medsafe: Bệnh phổi kẽ do thuốc

### gen_safety_0003

- Question: Medsafe: Bệnh phổi kẽ do thuốc có nguy hiểm không?
- Category: safety_warning
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / Medsafe: Bệnh phổi kẽ do thuốc

### gen_safety_0004

- Question: Cục Quản lý Dược VN (DAV): Đình chỉ lưu hành chế phẩm Chymomedi (Chymotrypsin 21 microkatals) là cảnh báo gì?
- Category: safety_warning
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / Cục Quản lý Dược VN (DAV): Đình chỉ lưu hành chế phẩm Chymomedi (Chymotrypsin 21 microkatals)

### gen_safety_0005

- Question: Thông tin an toàn về Cục Quản lý Dược VN (DAV): Đình chỉ lưu hành chế phẩm Chymomedi (Chymotrypsin 21 microkatals)
- Category: safety_warning
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / Cục Quản lý Dược VN (DAV): Đình chỉ lưu hành chế phẩm Chymomedi (Chymotrypsin 21 microkatals)

### gen_safety_0006

- Question: Cục Quản lý Dược VN (DAV): Đình chỉ lưu hành chế phẩm Chymomedi (Chymotrypsin 21 microkatals) có nguy hiểm không?
- Category: safety_warning
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / Cục Quản lý Dược VN (DAV): Đình chỉ lưu hành chế phẩm Chymomedi (Chymotrypsin 21 microkatals)

### gen_safety_0007

- Question: Health Canada: Nguy cơ gặp các phản ứng có hại nghiêm trọng trên thần kinh khi tiêm nội tủy thuốc cản quang chứa gadolinium là cảnh báo gì?
- Category: safety_warning
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / Health Canada: Nguy cơ gặp các phản ứng có hại nghiêm trọng trên thần kinh khi tiêm nội tủy thuốc cản quang chứa gadolinium

### gen_safety_0008

- Question: Thông tin an toàn về Health Canada: Nguy cơ gặp các phản ứng có hại nghiêm trọng trên thần kinh khi tiêm nội tủy thuốc cản quang chứa gadolinium
- Category: safety_warning
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / Health Canada: Nguy cơ gặp các phản ứng có hại nghiêm trọng trên thần kinh khi tiêm nội tủy thuốc cản quang chứa gadolinium

### gen_safety_0009

- Question: Health Canada: Nguy cơ gặp các phản ứng có hại nghiêm trọng trên thần kinh khi tiêm nội tủy thuốc cản quang chứa gadolinium có nguy hiểm không?
- Category: safety_warning
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / Health Canada: Nguy cơ gặp các phản ứng có hại nghiêm trọng trên thần kinh khi tiêm nội tủy thuốc cản quang chứa gadolinium

### gen_safety_0010

- Question: Cảnh báo: Chế phẩm dùng cho bệnh nhân tiểu đường có chứa chất bị cấm phenformin và có thể gây tử vong cho người bệnh là cảnh báo gì?
- Category: safety_warning
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / Cảnh báo: Chế phẩm dùng cho bệnh nhân tiểu đường có chứa chất bị cấm phenformin và có thể gây tử vong cho người bệnh

### gen_safety_0011

- Question: Thông tin an toàn về Cảnh báo: Chế phẩm dùng cho bệnh nhân tiểu đường có chứa chất bị cấm phenformin và có thể gây tử vong cho người bệnh
- Category: safety_warning
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / Cảnh báo: Chế phẩm dùng cho bệnh nhân tiểu đường có chứa chất bị cấm phenformin và có thể gây tử vong cho người bệnh

### gen_safety_0012

- Question: Cảnh báo: Chế phẩm dùng cho bệnh nhân tiểu đường có chứa chất bị cấm phenformin và có thể gây tử vong cho người bệnh có nguy hiểm không?
- Category: safety_warning
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / Cảnh báo: Chế phẩm dùng cho bệnh nhân tiểu đường có chứa chất bị cấm phenformin và có thể gây tử vong cho người bệnh

### gen_safety_0013

- Question: FDA: Cảnh báo về nguy cơ ngứa nghiêm trọng khi ngừng thuốc kháng histamin đường uống sau đợt điều trị kéo dài là cảnh báo gì?
- Category: safety_warning
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / FDA: Cảnh báo về nguy cơ ngứa nghiêm trọng khi ngừng thuốc kháng histamin đường uống sau đợt điều trị kéo dài

### gen_safety_0014

- Question: Thông tin an toàn về FDA: Cảnh báo về nguy cơ ngứa nghiêm trọng khi ngừng thuốc kháng histamin đường uống sau đợt điều trị kéo dài
- Category: safety_warning
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / FDA: Cảnh báo về nguy cơ ngứa nghiêm trọng khi ngừng thuốc kháng histamin đường uống sau đợt điều trị kéo dài

### gen_safety_0015

- Question: FDA: Cảnh báo về nguy cơ ngứa nghiêm trọng khi ngừng thuốc kháng histamin đường uống sau đợt điều trị kéo dài có nguy hiểm không?
- Category: safety_warning
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / FDA: Cảnh báo về nguy cơ ngứa nghiêm trọng khi ngừng thuốc kháng histamin đường uống sau đợt điều trị kéo dài

### gen_safety_0016

- Question: Medsafe: Cảnh báo về nguy cơ phản ứng có hại trên gan khi điều trị ngắn hạn với nitrofurantoin là cảnh báo gì?
- Category: safety_warning
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / Medsafe: Cảnh báo về nguy cơ phản ứng có hại trên gan khi điều trị ngắn hạn với nitrofurantoin

### gen_safety_0017

- Question: Thông tin an toàn về Medsafe: Cảnh báo về nguy cơ phản ứng có hại trên gan khi điều trị ngắn hạn với nitrofurantoin
- Category: safety_warning
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / Medsafe: Cảnh báo về nguy cơ phản ứng có hại trên gan khi điều trị ngắn hạn với nitrofurantoin

### gen_safety_0018

- Question: Medsafe: Cảnh báo về nguy cơ phản ứng có hại trên gan khi điều trị ngắn hạn với nitrofurantoin có nguy hiểm không?
- Category: safety_warning
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / Medsafe: Cảnh báo về nguy cơ phản ứng có hại trên gan khi điều trị ngắn hạn với nitrofurantoin

### gen_safety_0019

- Question: DAV: Ý kiến về việc tự nguyện thu hồi thuốc Esmya (ulipirstal acetate 5 mg) tại Việt Nam là cảnh báo gì?
- Category: safety_warning
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / DAV: Ý kiến về việc tự nguyện thu hồi thuốc Esmya (ulipirstal acetate 5 mg) tại Việt Nam

### gen_safety_0020

- Question: Thông tin an toàn về DAV: Ý kiến về việc tự nguyện thu hồi thuốc Esmya (ulipirstal acetate 5 mg) tại Việt Nam
- Category: safety_warning
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / DAV: Ý kiến về việc tự nguyện thu hồi thuốc Esmya (ulipirstal acetate 5 mg) tại Việt Nam

### gen_safety_0021

- Question: DAV: Ý kiến về việc tự nguyện thu hồi thuốc Esmya (ulipirstal acetate 5 mg) tại Việt Nam có nguy hiểm không?
- Category: safety_warning
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / DAV: Ý kiến về việc tự nguyện thu hồi thuốc Esmya (ulipirstal acetate 5 mg) tại Việt Nam

### gen_safety_0022

- Question: Cục Quản lý Dược: Cung cấp thông tin liên quan đến tính an toàn, hiệu quả của thuốc Evusheld là cảnh báo gì?
- Category: safety_warning
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / Cục Quản lý Dược: Cung cấp thông tin liên quan đến tính an toàn, hiệu quả của thuốc Evusheld

### gen_safety_0023

- Question: Thông tin an toàn về Cục Quản lý Dược: Cung cấp thông tin liên quan đến tính an toàn, hiệu quả của thuốc Evusheld
- Category: safety_warning
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / Cục Quản lý Dược: Cung cấp thông tin liên quan đến tính an toàn, hiệu quả của thuốc Evusheld

### gen_safety_0024

- Question: Cục Quản lý Dược: Cung cấp thông tin liên quan đến tính an toàn, hiệu quả của thuốc Evusheld có nguy hiểm không?
- Category: safety_warning
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / Cục Quản lý Dược: Cung cấp thông tin liên quan đến tính an toàn, hiệu quả của thuốc Evusheld

### gen_safety_0025

- Question: Giới thiệu Bản tin thông tin thuốc năm 2018 của BV Bạch Mai là cảnh báo gì?
- Category: safety_warning
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / Giới thiệu Bản tin thông tin thuốc năm 2018 của BV Bạch Mai

### gen_safety_0026

- Question: Thông tin an toàn về Giới thiệu Bản tin thông tin thuốc năm 2018 của BV Bạch Mai
- Category: safety_warning
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / Giới thiệu Bản tin thông tin thuốc năm 2018 của BV Bạch Mai

### gen_safety_0027

- Question: Giới thiệu Bản tin thông tin thuốc năm 2018 của BV Bạch Mai có nguy hiểm không?
- Category: safety_warning
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / Giới thiệu Bản tin thông tin thuốc năm 2018 của BV Bạch Mai

### gen_safety_0028

- Question: Cục QLD thông báo thu hồi thuốc Tobraquin là cảnh báo gì?
- Category: safety_warning
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 2
- First strict rank: 2
- Top result: `dav_recall` / `safety_recall` / `official_registry` / Công văn số 615/QLD-CL về việc thông báo thu hồi thuốc Tobraquin

### gen_safety_0029

- Question: Thông tin an toàn về Cục QLD thông báo thu hồi thuốc Tobraquin
- Category: safety_warning
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 2
- First strict rank: 2
- Top result: `dav_recall` / `safety_recall` / `official_registry` / Công văn số 615/QLD-CL về việc thông báo thu hồi thuốc Tobraquin

### gen_safety_0030

- Question: Cục QLD thông báo thu hồi thuốc Tobraquin có nguy hiểm không?
- Category: safety_warning
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / Cục QLD thông báo thu hồi thuốc Tobraquin

### gen_safety_0031

- Question: ANSM: Bắt buộc kê đơn đối với thuốc chứa pseudoephedrin đường uống là cảnh báo gì?
- Category: safety_warning
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / ANSM: Bắt buộc kê đơn đối với thuốc chứa pseudoephedrin đường uống

### gen_safety_0032

- Question: Thông tin an toàn về ANSM: Bắt buộc kê đơn đối với thuốc chứa pseudoephedrin đường uống
- Category: safety_warning
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / ANSM: Bắt buộc kê đơn đối với thuốc chứa pseudoephedrin đường uống

### gen_safety_0033

- Question: ANSM: Bắt buộc kê đơn đối với thuốc chứa pseudoephedrin đường uống có nguy hiểm không?
- Category: safety_warning
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / ANSM: Bắt buộc kê đơn đối với thuốc chứa pseudoephedrin đường uống

### gen_safety_0034

- Question: TGA: Khuyến cáo về an toàn thuốc chứa dược liệu Xuyên tâm liên (Andrographis paniculata) là cảnh báo gì?
- Category: safety_warning
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / TGA: Khuyến cáo về an toàn thuốc chứa dược liệu Xuyên tâm liên (Andrographis paniculata)

### gen_safety_0035

- Question: Thông tin an toàn về TGA: Khuyến cáo về an toàn thuốc chứa dược liệu Xuyên tâm liên (Andrographis paniculata)
- Category: safety_warning
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / TGA: Khuyến cáo về an toàn thuốc chứa dược liệu Xuyên tâm liên (Andrographis paniculata)

### gen_safety_0036

- Question: TGA: Khuyến cáo về an toàn thuốc chứa dược liệu Xuyên tâm liên (Andrographis paniculata) có nguy hiểm không?
- Category: safety_warning
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / CBIP: Nguy cơ phản ứng dị ứng nghiêm trọng khi sử dụng clorhexidin

### gen_safety_0037

- Question: ANSM: Cập nhật dữ liệu mới về nguy cơ rối loạn phát triển thần kinh ở trẻ có cha sử dụng valproat trước khi thụ tinh là cảnh báo gì?
- Category: safety_warning
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / ANSM: Cập nhật dữ liệu mới về nguy cơ rối loạn phát triển thần kinh ở trẻ có cha sử dụng valproat trước khi thụ tinh

### gen_safety_0038

- Question: Thông tin an toàn về ANSM: Cập nhật dữ liệu mới về nguy cơ rối loạn phát triển thần kinh ở trẻ có cha sử dụng valproat trước khi thụ tinh
- Category: safety_warning
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / ANSM: Cập nhật dữ liệu mới về nguy cơ rối loạn phát triển thần kinh ở trẻ có cha sử dụng valproat trước khi thụ tinh

### gen_safety_0039

- Question: ANSM: Cập nhật dữ liệu mới về nguy cơ rối loạn phát triển thần kinh ở trẻ có cha sử dụng valproat trước khi thụ tinh có nguy hiểm không?
- Category: safety_warning
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / ANSM: Cập nhật dữ liệu mới về nguy cơ rối loạn phát triển thần kinh ở trẻ có cha sử dụng valproat trước khi thụ tinh

### gen_safety_0040

- Question: Thông báo tạm ngừng lưu thông, phân phối và sử dụng thuốc Zidimbiotic 1g (ceftazidim) là cảnh báo gì?
- Category: safety_warning
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / Thông báo tạm ngừng lưu thông, phân phối và sử dụng thuốc Zidimbiotic 1g (ceftazidim)

### gen_safety_0041

- Question: Thông tin an toàn về Thông báo tạm ngừng lưu thông, phân phối và sử dụng thuốc Zidimbiotic 1g (ceftazidim)
- Category: safety_warning
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / Thông báo tạm ngừng lưu thông, phân phối và sử dụng thuốc Zidimbiotic 1g (ceftazidim)

### gen_safety_0042

- Question: Thông báo tạm ngừng lưu thông, phân phối và sử dụng thuốc Zidimbiotic 1g (ceftazidim) có nguy hiểm không?
- Category: safety_warning
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / Thông báo tạm ngừng lưu thông, phân phối và sử dụng thuốc Zidimbiotic 1g (ceftazidim)

### gen_safety_0043

- Question: Cập nhật thông tin liên quan đến tính an toàn của thuốc chứa Codein, Ibuprofen, Dexibuprofen là cảnh báo gì?
- Category: safety_warning
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / Cập nhật thông tin liên quan đến tính an toàn của thuốc chứa Codein, Ibuprofen, Dexibuprofen

### gen_safety_0044

- Question: Thông tin an toàn về Cập nhật thông tin liên quan đến tính an toàn của thuốc chứa Codein, Ibuprofen, Dexibuprofen
- Category: safety_warning
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / Cập nhật thông tin liên quan đến tính an toàn của thuốc chứa Codein, Ibuprofen, Dexibuprofen

### gen_safety_0045

- Question: Cập nhật thông tin liên quan đến tính an toàn của thuốc chứa Codein, Ibuprofen, Dexibuprofen có nguy hiểm không?
- Category: safety_warning
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / Cập nhật thông tin liên quan đến tính an toàn của thuốc chứa Codein, Ibuprofen, Dexibuprofen

### gen_safety_0046

- Question: Medsafe: Nhắc lại về một số phản ứng có hại nghiêm trọng khi sử dụng dexamethason là cảnh báo gì?
- Category: safety_warning
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / Medsafe: Nhắc lại về một số phản ứng có hại nghiêm trọng khi sử dụng dexamethason

### gen_safety_0047

- Question: Thông tin an toàn về Medsafe: Nhắc lại về một số phản ứng có hại nghiêm trọng khi sử dụng dexamethason
- Category: safety_warning
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / Medsafe: Nhắc lại về một số phản ứng có hại nghiêm trọng khi sử dụng dexamethason

### gen_safety_0048

- Question: Medsafe: Nhắc lại về một số phản ứng có hại nghiêm trọng khi sử dụng dexamethason có nguy hiểm không?
- Category: safety_warning
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / Medsafe: Nhắc lại về một số phản ứng có hại nghiêm trọng khi sử dụng dexamethason

### gen_safety_0049

- Question: Đình chỉ lưu hành, thu hồi và rút số đăng ký đối với thuốc Hadubaris, SĐK VD-18438-13 do Công ty cổ phần dược vật tư y tế Hải Dương sản xuất, đứng tên đăng ký r là cảnh báo gì?
- Category: safety_warning
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / Đình chỉ lưu hành, thu hồi và rút số đăng ký đối với thuốc Hadubaris, SĐK VD-18438-13 do Công ty cổ phần dược vật tư y tế Hải Dương sản xuất, đứng tên đăng ký ra khỏi danh mục các thuốc được cấp số đăng ký lưu hành tại Việt Nam.

### gen_safety_0050

- Question: Thông tin an toàn về Đình chỉ lưu hành, thu hồi và rút số đăng ký đối với thuốc Hadubaris, SĐK VD-18438-13 do Công ty cổ phần dược vật tư y tế Hải Dương sản xuất, đứng tên đăng ký r
- Category: safety_warning
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / Đình chỉ lưu hành, thu hồi và rút số đăng ký đối với thuốc Hadubaris, SĐK VD-18438-13 do Công ty cổ phần dược vật tư y tế Hải Dương sản xuất, đứng tên đăng ký ra khỏi danh mục các thuốc được cấp số đăng ký lưu hành tại Việt Nam.

### gen_safety_0051

- Question: Đình chỉ lưu hành, thu hồi và rút số đăng ký đối với thuốc Hadubaris, SĐK VD-18438-13 do Công ty cổ phần dược vật tư y tế Hải Dương sản xuất, đứng tên đăng ký r có nguy hiểm không?
- Category: safety_warning
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / Đình chỉ lưu hành, thu hồi và rút số đăng ký đối với thuốc Hadubaris, SĐK VD-18438-13 do Công ty cổ phần dược vật tư y tế Hải Dương sản xuất, đứng tên đăng ký ra khỏi danh mục các thuốc được cấp số đăng ký lưu hành tại Việt Nam.

### gen_safety_0052

- Question: TGA: Cập nhật cảnh báo đặc biệt về tác dụng không mong muốn trên tâm thần kinh khi sử dụng montelukast là cảnh báo gì?
- Category: safety_warning
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / TGA: Cập nhật cảnh báo đặc biệt về tác dụng không mong muốn trên tâm thần kinh khi sử dụng montelukast

### gen_safety_0053

- Question: Thông tin an toàn về TGA: Cập nhật cảnh báo đặc biệt về tác dụng không mong muốn trên tâm thần kinh khi sử dụng montelukast
- Category: safety_warning
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / TGA: Cập nhật cảnh báo đặc biệt về tác dụng không mong muốn trên tâm thần kinh khi sử dụng montelukast

### gen_safety_0054

- Question: TGA: Cập nhật cảnh báo đặc biệt về tác dụng không mong muốn trên tâm thần kinh khi sử dụng montelukast có nguy hiểm không?
- Category: safety_warning
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / TGA: Cập nhật cảnh báo đặc biệt về tác dụng không mong muốn trên tâm thần kinh khi sử dụng montelukast

### gen_safety_0055

- Question: FDA: Cảnh báo nguy cơ co giật liên quan thiếu hụt vitamin B6 khi sử dụng các chế phẩm thuốc chứa carbidopa/ levodopa là cảnh báo gì?
- Category: safety_warning
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / FDA: Cảnh báo nguy cơ co giật liên quan thiếu hụt vitamin B6 khi sử dụng các chế phẩm thuốc chứa carbidopa/ levodopa

### gen_safety_0056

- Question: Thông tin an toàn về FDA: Cảnh báo nguy cơ co giật liên quan thiếu hụt vitamin B6 khi sử dụng các chế phẩm thuốc chứa carbidopa/ levodopa
- Category: safety_warning
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / FDA: Cảnh báo nguy cơ co giật liên quan thiếu hụt vitamin B6 khi sử dụng các chế phẩm thuốc chứa carbidopa/ levodopa

### gen_safety_0057

- Question: FDA: Cảnh báo nguy cơ co giật liên quan thiếu hụt vitamin B6 khi sử dụng các chế phẩm thuốc chứa carbidopa/ levodopa có nguy hiểm không?
- Category: safety_warning
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / FDA: Cảnh báo nguy cơ co giật liên quan thiếu hụt vitamin B6 khi sử dụng các chế phẩm thuốc chứa carbidopa/ levodopa

### gen_safety_0058

- Question: Medsafe: Nguy cơ tăng sản xương vô căn lan tỏa khi sử dụng retinoid dạng uống là cảnh báo gì?
- Category: safety_warning
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / Medsafe: Nguy cơ tăng sản xương vô căn lan tỏa khi sử dụng retinoid dạng uống

### gen_safety_0059

- Question: Thông tin an toàn về Medsafe: Nguy cơ tăng sản xương vô căn lan tỏa khi sử dụng retinoid dạng uống
- Category: safety_warning
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / Medsafe: Nguy cơ tăng sản xương vô căn lan tỏa khi sử dụng retinoid dạng uống

### gen_safety_0060

- Question: Medsafe: Nguy cơ tăng sản xương vô căn lan tỏa khi sử dụng retinoid dạng uống có nguy hiểm không?
- Category: safety_warning
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / Medsafe: Nguy cơ tăng sản xương vô căn lan tỏa khi sử dụng retinoid dạng uống

### gen_safety_0061

- Question: Dữ liệu an toàn đến thời điểm hiện tại cho thấy không có mối liên quan giữa vắc xin COVID-19 và ung thư là cảnh báo gì?
- Category: safety_warning
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / Dữ liệu an toàn đến thời điểm hiện tại cho thấy không có mối liên quan giữa vắc xin COVID-19 và ung thư

### gen_safety_0062

- Question: Thông tin an toàn về Dữ liệu an toàn đến thời điểm hiện tại cho thấy không có mối liên quan giữa vắc xin COVID-19 và ung thư
- Category: safety_warning
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / Dữ liệu an toàn đến thời điểm hiện tại cho thấy không có mối liên quan giữa vắc xin COVID-19 và ung thư

### gen_safety_0063

- Question: Dữ liệu an toàn đến thời điểm hiện tại cho thấy không có mối liên quan giữa vắc xin COVID-19 và ung thư có nguy hiểm không?
- Category: safety_warning
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / Dữ liệu an toàn đến thời điểm hiện tại cho thấy không có mối liên quan giữa vắc xin COVID-19 và ung thư

### gen_safety_0064

- Question: TGA: Nguy cơ ngộ độc liên quan đến thuốc pha chế chứa Cà độc dược điều trị hội chứng quấy khóc ở trẻ sơ sinh và trẻ nhỏ là cảnh báo gì?
- Category: safety_warning
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / TGA: Nguy cơ ngộ độc liên quan đến thuốc pha chế chứa Cà độc dược điều trị hội chứng quấy khóc ở trẻ sơ sinh và trẻ nhỏ

### gen_safety_0065

- Question: Thông tin an toàn về TGA: Nguy cơ ngộ độc liên quan đến thuốc pha chế chứa Cà độc dược điều trị hội chứng quấy khóc ở trẻ sơ sinh và trẻ nhỏ
- Category: safety_warning
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / TGA: Nguy cơ ngộ độc liên quan đến thuốc pha chế chứa Cà độc dược điều trị hội chứng quấy khóc ở trẻ sơ sinh và trẻ nhỏ

### gen_safety_0066

- Question: TGA: Nguy cơ ngộ độc liên quan đến thuốc pha chế chứa Cà độc dược điều trị hội chứng quấy khóc ở trẻ sơ sinh và trẻ nhỏ có nguy hiểm không?
- Category: safety_warning
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / TGA: Nguy cơ ngộ độc liên quan đến thuốc pha chế chứa Cà độc dược điều trị hội chứng quấy khóc ở trẻ sơ sinh và trẻ nhỏ

### gen_safety_0067

- Question: HAS: Thận trọng khi sử dụng các thuốc có nguy cơ cao là cảnh báo gì?
- Category: safety_warning
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / HAS: Thận trọng khi sử dụng các thuốc có nguy cơ cao

### gen_safety_0068

- Question: Thông tin an toàn về HAS: Thận trọng khi sử dụng các thuốc có nguy cơ cao
- Category: safety_warning
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 4
- First strict rank: 4
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / Health Canada: Nguy cơ về hội chứng DRESS khi sử dụng bortezomib

### gen_safety_0069

- Question: HAS: Thận trọng khi sử dụng các thuốc có nguy cơ cao có nguy hiểm không?
- Category: safety_warning
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / HAS: Thận trọng khi sử dụng các thuốc có nguy cơ cao

### gen_safety_0070

- Question: Bộ y tế: Dự thảo hướng dẫn phòng và xử trí phản vệ là cảnh báo gì?
- Category: safety_warning
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / Bộ y tế: Dự thảo hướng dẫn phòng và xử trí phản vệ

### gen_safety_0071

- Question: Thông tin an toàn về Bộ y tế: Dự thảo hướng dẫn phòng và xử trí phản vệ
- Category: safety_warning
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / Bộ y tế: Dự thảo hướng dẫn phòng và xử trí phản vệ

### gen_safety_0072

- Question: Bộ y tế: Dự thảo hướng dẫn phòng và xử trí phản vệ có nguy hiểm không?
- Category: safety_warning
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / Bộ y tế: Dự thảo hướng dẫn phòng và xử trí phản vệ

### gen_safety_0073

- Question: DAV: Thông báo thu hồi trên toàn quốc lô thuốc Aceclofenac Stella 100mg là cảnh báo gì?
- Category: safety_warning
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / DAV: Thông báo thu hồi trên toàn quốc lô thuốc Aceclofenac Stella 100mg

### gen_safety_0074

- Question: Thông tin an toàn về DAV: Thông báo thu hồi trên toàn quốc lô thuốc Aceclofenac Stella 100mg
- Category: safety_warning
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / DAV: Thông báo thu hồi trên toàn quốc lô thuốc Aceclofenac Stella 100mg

### gen_safety_0075

- Question: DAV: Thông báo thu hồi trên toàn quốc lô thuốc Aceclofenac Stella 100mg có nguy hiểm không?
- Category: safety_warning
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / DAV: Thông báo thu hồi trên toàn quốc lô thuốc Aceclofenac Stella 100mg

### gen_safety_0076

- Question: FDA: Khuyến cáo không sử dụng amphetamin và methylphenidat dạng giải phóng kéo dài trong điều trị ADHD ở trẻ dưới 6 tuổi là cảnh báo gì?
- Category: counterfeit
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / FDA: Khuyến cáo không sử dụng amphetamin và methylphenidat dạng giải phóng kéo dài trong điều trị ADHD ở trẻ dưới 6 tuổi

### gen_safety_0077

- Question: Thông tin an toàn về FDA: Khuyến cáo không sử dụng amphetamin và methylphenidat dạng giải phóng kéo dài trong điều trị ADHD ở trẻ dưới 6 tuổi
- Category: counterfeit
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / FDA: Khuyến cáo không sử dụng amphetamin và methylphenidat dạng giải phóng kéo dài trong điều trị ADHD ở trẻ dưới 6 tuổi

### gen_safety_0078

- Question: FDA: Khuyến cáo không sử dụng amphetamin và methylphenidat dạng giải phóng kéo dài trong điều trị ADHD ở trẻ dưới 6 tuổi có nguy hiểm không?
- Category: counterfeit
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / FDA: Khuyến cáo không sử dụng amphetamin và methylphenidat dạng giải phóng kéo dài trong điều trị ADHD ở trẻ dưới 6 tuổi

### gen_safety_0079

- Question: Cục Quản lý Dược VN (DAV): Thu hồi chế phẩm Pneumorel (fenspiride hydrochloride) do nguy cơ gây rối loạn nhịp tim của người sử dụng là cảnh báo gì?
- Category: safety_warning
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / Cục Quản lý Dược VN (DAV): Thu hồi chế phẩm Pneumorel (fenspiride hydrochloride) do nguy cơ gây rối loạn nhịp tim của người sử dụng

### gen_safety_0080

- Question: Thông tin an toàn về Cục Quản lý Dược VN (DAV): Thu hồi chế phẩm Pneumorel (fenspiride hydrochloride) do nguy cơ gây rối loạn nhịp tim của người sử dụng
- Category: safety_warning
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / Cục Quản lý Dược VN (DAV): Thu hồi chế phẩm Pneumorel (fenspiride hydrochloride) do nguy cơ gây rối loạn nhịp tim của người sử dụng

### gen_safety_0081

- Question: Cục Quản lý Dược VN (DAV): Thu hồi chế phẩm Pneumorel (fenspiride hydrochloride) do nguy cơ gây rối loạn nhịp tim của người sử dụng có nguy hiểm không?
- Category: safety_warning
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / Cục Quản lý Dược VN (DAV): Thu hồi chế phẩm Pneumorel (fenspiride hydrochloride) do nguy cơ gây rối loạn nhịp tim của người sử dụng

### gen_safety_0082

- Question: Bộ Y tế ban hành Thông tư số 51/2017/TT- BYT hướng dẫn phòng, chẩn đoán và xử trí phản vệ là cảnh báo gì?
- Category: safety_warning
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / Bộ Y tế ban hành Thông tư số 51/2017/TT- BYT hướng dẫn phòng, chẩn đoán và xử trí phản vệ

### gen_safety_0083

- Question: Thông tin an toàn về Bộ Y tế ban hành Thông tư số 51/2017/TT- BYT hướng dẫn phòng, chẩn đoán và xử trí phản vệ
- Category: safety_warning
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / Bộ Y tế ban hành Thông tư số 51/2017/TT- BYT hướng dẫn phòng, chẩn đoán và xử trí phản vệ

### gen_safety_0084

- Question: Bộ Y tế ban hành Thông tư số 51/2017/TT- BYT hướng dẫn phòng, chẩn đoán và xử trí phản vệ có nguy hiểm không?
- Category: safety_warning
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / Bộ Y tế ban hành Thông tư số 51/2017/TT- BYT hướng dẫn phòng, chẩn đoán và xử trí phản vệ

### gen_safety_0085

- Question: Cục Quản lý Dược - Bộ y tế ra thông báo tạm ngừng việc sử dụng lô vắcxin Quinvaxem là cảnh báo gì?
- Category: safety_warning
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / Cục Quản lý Dược - Bộ y tế ra thông báo tạm ngừng việc sử dụng lô vắcxin Quinvaxem

### gen_safety_0086

- Question: Thông tin an toàn về Cục Quản lý Dược - Bộ y tế ra thông báo tạm ngừng việc sử dụng lô vắcxin Quinvaxem
- Category: safety_warning
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / Cục Quản lý Dược - Bộ y tế ra thông báo tạm ngừng việc sử dụng lô vắcxin Quinvaxem

### gen_safety_0087

- Question: Cục Quản lý Dược - Bộ y tế ra thông báo tạm ngừng việc sử dụng lô vắcxin Quinvaxem có nguy hiểm không?
- Category: safety_warning
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / Cục Quản lý Dược - Bộ y tế ra thông báo tạm ngừng việc sử dụng lô vắcxin Quinvaxem

### gen_safety_0088

- Question: ANSM: Nguy cơ u màng não khi sử dụng thuốc tránh thai desogestrel là cảnh báo gì?
- Category: safety_warning
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / ANSM: Nguy cơ u màng não khi sử dụng thuốc tránh thai desogestrel

### gen_safety_0089

- Question: Thông tin an toàn về ANSM: Nguy cơ u màng não khi sử dụng thuốc tránh thai desogestrel
- Category: safety_warning
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / ANSM: Nguy cơ u màng não khi sử dụng thuốc tránh thai desogestrel

### gen_safety_0090

- Question: ANSM: Nguy cơ u màng não khi sử dụng thuốc tránh thai desogestrel có nguy hiểm không?
- Category: safety_warning
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / ANSM: Nguy cơ u màng não khi sử dụng thuốc tránh thai desogestrel

### gen_safety_0091

- Question: Cục Quản lý Dược: Ngày 26/7/2018, Cục Quản lý Dược Việt Nam ban hành công văn số 14487/QLD-CL về việc xử lý thuốc chứa dược chất valsartan là cảnh báo gì?
- Category: safety_warning
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / Cục Quản lý Dược: Ngày 26/7/2018, Cục Quản lý Dược Việt Nam ban hành công văn số 14487/QLD-CL về việc xử lý thuốc chứa dược chất valsartan

### gen_safety_0092

- Question: Thông tin an toàn về Cục Quản lý Dược: Ngày 26/7/2018, Cục Quản lý Dược Việt Nam ban hành công văn số 14487/QLD-CL về việc xử lý thuốc chứa dược chất valsartan
- Category: safety_warning
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / Cục Quản lý Dược: Ngày 26/7/2018, Cục Quản lý Dược Việt Nam ban hành công văn số 14487/QLD-CL về việc xử lý thuốc chứa dược chất valsartan

### gen_safety_0093

- Question: Cục Quản lý Dược: Ngày 26/7/2018, Cục Quản lý Dược Việt Nam ban hành công văn số 14487/QLD-CL về việc xử lý thuốc chứa dược chất valsartan có nguy hiểm không?
- Category: safety_warning
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / Cục Quản lý Dược: Ngày 26/7/2018, Cục Quản lý Dược Việt Nam ban hành công văn số 14487/QLD-CL về việc xử lý thuốc chứa dược chất valsartan

### gen_safety_0094

- Question: Thông tư số 12/2025/TT-BYT của Bộ Y tế: Quy định việc đăng ký lưu hành thuốc, nguyên liệu làm thuốc là cảnh báo gì?
- Category: safety_warning
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / Thông tư số 12/2025/TT-BYT của Bộ Y tế: Quy định việc đăng ký lưu hành thuốc, nguyên liệu làm thuốc

### gen_safety_0095

- Question: Thông tin an toàn về Thông tư số 12/2025/TT-BYT của Bộ Y tế: Quy định việc đăng ký lưu hành thuốc, nguyên liệu làm thuốc
- Category: safety_warning
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / Thông tư số 12/2025/TT-BYT của Bộ Y tế: Quy định việc đăng ký lưu hành thuốc, nguyên liệu làm thuốc

### gen_safety_0096

- Question: Thông tư số 12/2025/TT-BYT của Bộ Y tế: Quy định việc đăng ký lưu hành thuốc, nguyên liệu làm thuốc có nguy hiểm không?
- Category: safety_warning
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / Thông tư số 12/2025/TT-BYT của Bộ Y tế: Quy định việc đăng ký lưu hành thuốc, nguyên liệu làm thuốc

### gen_safety_0097

- Question: Rút số đăng ký lưu hành thuốc Imipar, Auzomek 40 và Hesopak ra khỏi danh mục các thuốc được cấp số đăng ký lưu hành tại Việt Nam là cảnh báo gì?
- Category: safety_warning
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / Rút số đăng ký lưu hành thuốc Imipar, Auzomek 40 và Hesopak ra khỏi danh mục các thuốc được cấp số đăng ký lưu hành tại Việt Nam

### gen_safety_0098

- Question: Thông tin an toàn về Rút số đăng ký lưu hành thuốc Imipar, Auzomek 40 và Hesopak ra khỏi danh mục các thuốc được cấp số đăng ký lưu hành tại Việt Nam
- Category: safety_warning
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / Rút số đăng ký lưu hành thuốc Imipar, Auzomek 40 và Hesopak ra khỏi danh mục các thuốc được cấp số đăng ký lưu hành tại Việt Nam

### gen_safety_0099

- Question: Rút số đăng ký lưu hành thuốc Imipar, Auzomek 40 và Hesopak ra khỏi danh mục các thuốc được cấp số đăng ký lưu hành tại Việt Nam có nguy hiểm không?
- Category: safety_warning
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / Rút số đăng ký lưu hành thuốc Imipar, Auzomek 40 và Hesopak ra khỏi danh mục các thuốc được cấp số đăng ký lưu hành tại Việt Nam

### gen_safety_0100

- Question: MHRA: Cảnh báo về tương tác thuốc giữa warfarin và tramadol là cảnh báo gì?
- Category: safety_warning
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / MHRA: Cảnh báo về tương tác thuốc giữa warfarin và tramadol

### gen_safety_0101

- Question: Thông tin an toàn về MHRA: Cảnh báo về tương tác thuốc giữa warfarin và tramadol
- Category: safety_warning
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / MHRA: Cảnh báo về tương tác thuốc giữa warfarin và tramadol

### gen_safety_0102

- Question: MHRA: Cảnh báo về tương tác thuốc giữa warfarin và tramadol có nguy hiểm không?
- Category: safety_warning
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / MHRA: Cảnh báo về tương tác thuốc giữa warfarin và tramadol

### gen_safety_0103

- Question: Tạm ngừng sử dụng thuốc Hadubaris (bari sulfat), SĐK: VD-18438-13 do công ty CP Dược VTYT Hải Dương sản xuất là cảnh báo gì?
- Category: safety_warning
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / Tạm ngừng sử dụng thuốc Hadubaris (bari sulfat), SĐK: VD-18438-13 do công ty CP Dược VTYT Hải Dương sản xuất

### gen_safety_0104

- Question: Thông tin an toàn về Tạm ngừng sử dụng thuốc Hadubaris (bari sulfat), SĐK: VD-18438-13 do công ty CP Dược VTYT Hải Dương sản xuất
- Category: safety_warning
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / Tạm ngừng sử dụng thuốc Hadubaris (bari sulfat), SĐK: VD-18438-13 do công ty CP Dược VTYT Hải Dương sản xuất

### gen_safety_0105

- Question: Tạm ngừng sử dụng thuốc Hadubaris (bari sulfat), SĐK: VD-18438-13 do công ty CP Dược VTYT Hải Dương sản xuất có nguy hiểm không?
- Category: safety_warning
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / Tạm ngừng sử dụng thuốc Hadubaris (bari sulfat), SĐK: VD-18438-13 do công ty CP Dược VTYT Hải Dương sản xuất

### gen_safety_0106

- Question: Tương tác thuốc giữa clozapin và mirabegron: Thông tin từ bản tin BIP Occitanie số 01/2026 là cảnh báo gì?
- Category: safety_warning
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / Tương tác thuốc giữa clozapin và mirabegron: Thông tin từ bản tin BIP Occitanie số 01/2026

### gen_safety_0107

- Question: Thông tin an toàn về Tương tác thuốc giữa clozapin và mirabegron: Thông tin từ bản tin BIP Occitanie số 01/2026
- Category: safety_warning
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / Ảnh hưởng của thuốc chống trầm cảm lên các thông số tim mạch - chuyển hóa: Thông tin từ bản tin BIP Occitanie số 01/2026

### gen_safety_0108

- Question: Tương tác thuốc giữa clozapin và mirabegron: Thông tin từ bản tin BIP Occitanie số 01/2026 có nguy hiểm không?
- Category: safety_warning
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / Ảnh hưởng của thuốc chống trầm cảm lên các thông số tim mạch - chuyển hóa: Thông tin từ bản tin BIP Occitanie số 01/2026

### gen_safety_0109

- Question: Hội nghị Dược lâm sàng Bệnh viện Bạch Mai lần thứ nhất là cảnh báo gì?
- Category: safety_warning
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / Hội nghị Dược lâm sàng Bệnh viện Bạch Mai lần thứ nhất

### gen_safety_0110

- Question: Thông tin an toàn về Hội nghị Dược lâm sàng Bệnh viện Bạch Mai lần thứ nhất
- Category: safety_warning
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / Hội nghị Dược lâm sàng Bệnh viện Bạch Mai lần thứ nhất

### gen_safety_0111

- Question: Hội nghị Dược lâm sàng Bệnh viện Bạch Mai lần thứ nhất có nguy hiểm không?
- Category: safety_warning
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / Hội nghị Dược lâm sàng Bệnh viện Bạch Mai lần thứ nhất

### gen_safety_0112

- Question: DAV: Ngày 07/12/2021, Cục Quản lý Dược có công văn số 701/QĐ-QLD về việc thu hồi Giấy đăng ký lưu hành thuốc, đình chỉ lưu hành và thu hồi thuốc đang lưu hành c là cảnh báo gì?
- Category: safety_warning
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / DAV: Ngày 07/12/2021, Cục Quản lý Dược có công văn số 701/QĐ-QLD về việc thu hồi Giấy đăng ký lưu hành thuốc, đình chỉ lưu hành và thu hồi thuốc đang lưu hành của một số thuốc

### gen_safety_0113

- Question: Thông tin an toàn về DAV: Ngày 07/12/2021, Cục Quản lý Dược có công văn số 701/QĐ-QLD về việc thu hồi Giấy đăng ký lưu hành thuốc, đình chỉ lưu hành và thu hồi thuốc đang lưu hành c
- Category: safety_warning
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / DAV: Ngày 07/12/2021, Cục Quản lý Dược có công văn số 701/QĐ-QLD về việc thu hồi Giấy đăng ký lưu hành thuốc, đình chỉ lưu hành và thu hồi thuốc đang lưu hành của một số thuốc

### gen_safety_0114

- Question: DAV: Ngày 07/12/2021, Cục Quản lý Dược có công văn số 701/QĐ-QLD về việc thu hồi Giấy đăng ký lưu hành thuốc, đình chỉ lưu hành và thu hồi thuốc đang lưu hành c có nguy hiểm không?
- Category: safety_warning
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / DAV: Ngày 07/12/2021, Cục Quản lý Dược có công văn số 701/QĐ-QLD về việc thu hồi Giấy đăng ký lưu hành thuốc, đình chỉ lưu hành và thu hồi thuốc đang lưu hành của một số thuốc

### gen_safety_0115

- Question: Medsafe: Các yếu tố nguy cơ ngộ độc colchicin là cảnh báo gì?
- Category: safety_warning
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / Medsafe: Các yếu tố nguy cơ ngộ độc colchicin

### gen_safety_0116

- Question: Thông tin an toàn về Medsafe: Các yếu tố nguy cơ ngộ độc colchicin
- Category: safety_warning
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / Medsafe: Các yếu tố nguy cơ ngộ độc colchicin

### gen_safety_0117

- Question: Medsafe: Các yếu tố nguy cơ ngộ độc colchicin có nguy hiểm không?
- Category: safety_warning
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / Medsafe: Các yếu tố nguy cơ ngộ độc colchicin

### gen_safety_0118

- Question: Giới thiệu Bản tin Thông tin Thuốc số 1 – 2017 - Đơn vị Thông tin Thuốc – Bệnh viện Bạch Mai là cảnh báo gì?
- Category: safety_warning
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 2
- First strict rank: 2
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / Giới thiệu Bản tin Thông tin Thuốc số 2 - 2017 - Đơn vị Thông tin Thuốc - Bệnh viện Bạch Mai

### gen_safety_0119

- Question: Thông tin an toàn về Giới thiệu Bản tin Thông tin Thuốc số 1 – 2017 - Đơn vị Thông tin Thuốc – Bệnh viện Bạch Mai
- Category: safety_warning
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 2
- First strict rank: 2
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / Giới thiệu Bản tin Thông tin Thuốc số 2 - 2017 - Đơn vị Thông tin Thuốc - Bệnh viện Bạch Mai

### gen_safety_0120

- Question: Giới thiệu Bản tin Thông tin Thuốc số 1 – 2017 - Đơn vị Thông tin Thuốc – Bệnh viện Bạch Mai có nguy hiểm không?
- Category: safety_warning
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 2
- First strict rank: 2
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / Giới thiệu Bản tin Thông tin Thuốc số 2 - 2017 - Đơn vị Thông tin Thuốc - Bệnh viện Bạch Mai

### gen_safety_0121

- Question: Cục Quản lý Dược: Ban hành công văn số 17253/QLD-MP ngày 07/9/2018 về việc đình chỉ lưu hành, thu hồi sản phẩm nước muối sinh lý SAT BB, số lô DL 109 sản xuất n là cảnh báo gì?
- Category: safety_warning
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / Cục Quản lý Dược: Ban hành công văn số 17253/QLD-MP ngày 07/9/2018 về việc đình chỉ lưu hành, thu hồi sản phẩm nước muối sinh lý SAT BB, số lô DL 109 sản xuất ngày 08/6/2018 không đạt chất lượng.

### gen_safety_0122

- Question: Thông tin an toàn về Cục Quản lý Dược: Ban hành công văn số 17253/QLD-MP ngày 07/9/2018 về việc đình chỉ lưu hành, thu hồi sản phẩm nước muối sinh lý SAT BB, số lô DL 109 sản xuất n
- Category: safety_warning
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / Cục Quản lý Dược: Ban hành công văn số 17253/QLD-MP ngày 07/9/2018 về việc đình chỉ lưu hành, thu hồi sản phẩm nước muối sinh lý SAT BB, số lô DL 109 sản xuất ngày 08/6/2018 không đạt chất lượng.

### gen_safety_0123

- Question: Cục Quản lý Dược: Ban hành công văn số 17253/QLD-MP ngày 07/9/2018 về việc đình chỉ lưu hành, thu hồi sản phẩm nước muối sinh lý SAT BB, số lô DL 109 sản xuất n có nguy hiểm không?
- Category: safety_warning
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / Cục Quản lý Dược: Ban hành công văn số 17253/QLD-MP ngày 07/9/2018 về việc đình chỉ lưu hành, thu hồi sản phẩm nước muối sinh lý SAT BB, số lô DL 109 sản xuất ngày 08/6/2018 không đạt chất lượng.

### gen_safety_0124

- Question: Cập nhật thông tin từ các CQQL dược phẩm trên thế giới về việc sử dụng paracetamol (acetaminophen) cho phụ nữ có thai là cảnh báo gì?
- Category: safety_warning
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / Cập nhật thông tin từ các CQQL dược phẩm trên thế giới về việc sử dụng paracetamol (acetaminophen) cho phụ nữ có thai

### gen_safety_0125

- Question: Thông tin an toàn về Cập nhật thông tin từ các CQQL dược phẩm trên thế giới về việc sử dụng paracetamol (acetaminophen) cho phụ nữ có thai
- Category: safety_warning
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / Cập nhật thông tin từ các CQQL dược phẩm trên thế giới về việc sử dụng paracetamol (acetaminophen) cho phụ nữ có thai

### gen_safety_0126

- Question: Cập nhật thông tin từ các CQQL dược phẩm trên thế giới về việc sử dụng paracetamol (acetaminophen) cho phụ nữ có thai có nguy hiểm không?
- Category: safety_warning
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / Cập nhật thông tin từ các CQQL dược phẩm trên thế giới về việc sử dụng paracetamol (acetaminophen) cho phụ nữ có thai

### gen_safety_0127

- Question: Health Canada: Cập nhật thông tin sản phẩm của các thuốc ức chế SGLT-2 tại Canada là cảnh báo gì?
- Category: safety_warning
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / Health Canada: Cập nhật thông tin sản phẩm của các thuốc ức chế SGLT-2 tại Canada

### gen_safety_0128

- Question: Thông tin an toàn về Health Canada: Cập nhật thông tin sản phẩm của các thuốc ức chế SGLT-2 tại Canada
- Category: safety_warning
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / Health Canada: Cập nhật thông tin sản phẩm của các thuốc ức chế SGLT-2 tại Canada

### gen_safety_0129

- Question: Health Canada: Cập nhật thông tin sản phẩm của các thuốc ức chế SGLT-2 tại Canada có nguy hiểm không?
- Category: safety_warning
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / Health Canada: Cập nhật thông tin sản phẩm của các thuốc ức chế SGLT-2 tại Canada

### gen_safety_0130

- Question: TẠM NGỪNG SỬ DỤNG HAI LÔ VẮC-XIN VIÊM GAN B là cảnh báo gì?
- Category: safety_warning
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / TẠM NGỪNG SỬ DỤNG HAI LÔ VẮC-XIN VIÊM GAN B

### gen_safety_0131

- Question: Thông tin an toàn về TẠM NGỪNG SỬ DỤNG HAI LÔ VẮC-XIN VIÊM GAN B
- Category: safety_warning
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / TẠM NGỪNG SỬ DỤNG HAI LÔ VẮC-XIN VIÊM GAN B

### gen_safety_0132

- Question: TẠM NGỪNG SỬ DỤNG HAI LÔ VẮC-XIN VIÊM GAN B có nguy hiểm không?
- Category: safety_warning
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / TẠM NGỪNG SỬ DỤNG HAI LÔ VẮC-XIN VIÊM GAN B

### gen_safety_0133

- Question: Bản tin WHO số 04/2024: EMA khuyến cáo cập nhật thông tin sản phẩm của một số thuốc (Amphotericin B phức hợp lipid, cefotaxim, ethambutol, clorhexidin) là cảnh báo gì?
- Category: safety_warning
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / Bản tin WHO số 04/2024: EMA khuyến cáo cập nhật thông tin sản phẩm của một số thuốc (Amphotericin B phức hợp lipid, cefotaxim, ethambutol, clorhexidin)

### gen_safety_0134

- Question: Thông tin an toàn về Bản tin WHO số 04/2024: EMA khuyến cáo cập nhật thông tin sản phẩm của một số thuốc (Amphotericin B phức hợp lipid, cefotaxim, ethambutol, clorhexidin)
- Category: safety_warning
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / Bản tin WHO số 04/2024: EMA khuyến cáo cập nhật thông tin sản phẩm của một số thuốc (Amphotericin B phức hợp lipid, cefotaxim, ethambutol, clorhexidin)

### gen_safety_0135

- Question: Bản tin WHO số 04/2024: EMA khuyến cáo cập nhật thông tin sản phẩm của một số thuốc (Amphotericin B phức hợp lipid, cefotaxim, ethambutol, clorhexidin) có nguy hiểm không?
- Category: safety_warning
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / Bản tin WHO số 04/2024: EMA khuyến cáo cập nhật thông tin sản phẩm của một số thuốc (Amphotericin B phức hợp lipid, cefotaxim, ethambutol, clorhexidin)

### gen_safety_0136

- Question: MHRA: Khuyến cáo sử dụng biện pháp tránh thai hiệu quả cho bệnh nhân nam được điều trị bằng thuốc valproat là cảnh báo gì?
- Category: safety_warning
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / MHRA: Khuyến cáo sử dụng biện pháp tránh thai hiệu quả cho bệnh nhân nam được điều trị bằng thuốc valproat

### gen_safety_0137

- Question: Thông tin an toàn về MHRA: Khuyến cáo sử dụng biện pháp tránh thai hiệu quả cho bệnh nhân nam được điều trị bằng thuốc valproat
- Category: safety_warning
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / MHRA: Khuyến cáo sử dụng biện pháp tránh thai hiệu quả cho bệnh nhân nam được điều trị bằng thuốc valproat

### gen_safety_0138

- Question: MHRA: Khuyến cáo sử dụng biện pháp tránh thai hiệu quả cho bệnh nhân nam được điều trị bằng thuốc valproat có nguy hiểm không?
- Category: safety_warning
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / MHRA: Khuyến cáo sử dụng biện pháp tránh thai hiệu quả cho bệnh nhân nam được điều trị bằng thuốc valproat

### gen_safety_0139

- Question: Thông báo về việc tạm ngừng lưu thông, phân phối, sử dụng thuốc tiêm truyền Sodium Chloride 0,9% chai 500 ml, SĐK: VN-7545-09, lô SX: V-130483S là cảnh báo gì?
- Category: safety_warning
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / Thông báo về việc tạm ngừng lưu thông, phân phối, sử dụng thuốc tiêm truyền Sodium Chloride 0,9% chai 500 ml, SĐK: VN-7545-09, lô SX: V-130483S

### gen_safety_0140

- Question: Thông tin an toàn về Thông báo về việc tạm ngừng lưu thông, phân phối, sử dụng thuốc tiêm truyền Sodium Chloride 0,9% chai 500 ml, SĐK: VN-7545-09, lô SX: V-130483S
- Category: safety_warning
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / Thông báo về việc tạm ngừng lưu thông, phân phối, sử dụng thuốc tiêm truyền Sodium Chloride 0,9% chai 500 ml, SĐK: VN-7545-09, lô SX: V-130483S

### gen_safety_0141

- Question: Thông báo về việc tạm ngừng lưu thông, phân phối, sử dụng thuốc tiêm truyền Sodium Chloride 0,9% chai 500 ml, SĐK: VN-7545-09, lô SX: V-130483S có nguy hiểm không?
- Category: safety_warning
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / Thông báo về việc tạm ngừng lưu thông, phân phối, sử dụng thuốc tiêm truyền Sodium Chloride 0,9% chai 500 ml, SĐK: VN-7545-09, lô SX: V-130483S

### gen_safety_0142

- Question: Medsafe: Nguy cơ trẻ sinh ra nhỏ hơn tuổi thai hoặc mắc tật đầu nhỏ khi phơi nhiễm với carbamazepin trong thai kỳ là cảnh báo gì?
- Category: safety_warning
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / Medsafe: Nguy cơ trẻ sinh ra nhỏ hơn tuổi thai hoặc mắc tật đầu nhỏ khi phơi nhiễm với carbamazepin trong thai kỳ

### gen_safety_0143

- Question: Thông tin an toàn về Medsafe: Nguy cơ trẻ sinh ra nhỏ hơn tuổi thai hoặc mắc tật đầu nhỏ khi phơi nhiễm với carbamazepin trong thai kỳ
- Category: safety_warning
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / Medsafe: Nguy cơ trẻ sinh ra nhỏ hơn tuổi thai hoặc mắc tật đầu nhỏ khi phơi nhiễm với carbamazepin trong thai kỳ

### gen_safety_0144

- Question: Medsafe: Nguy cơ trẻ sinh ra nhỏ hơn tuổi thai hoặc mắc tật đầu nhỏ khi phơi nhiễm với carbamazepin trong thai kỳ có nguy hiểm không?
- Category: safety_warning
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / Medsafe: Nguy cơ trẻ sinh ra nhỏ hơn tuổi thai hoặc mắc tật đầu nhỏ khi phơi nhiễm với carbamazepin trong thai kỳ

### gen_dosage_handoff_0001

- Question: AstaPadol 500 mg dùng thế nào?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / AstaPadol 500 mg

### gen_dosage_handoff_0002

- Question: AstaPadol 500 mg uống bao nhiêu viên mỗi ngày?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 2
- First strict rank: 2
- Top result: `dav_all` / `drug_info` / `official_registry` / AstaPadol Viên sủi 500 mg

### gen_dosage_handoff_0003

- Question: Liều dùng AstaPadol 500 mg như thế nào?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / AstaPadol 500 mg

### gen_dosage_handoff_0004

- Question: AstaPadol 500 mg có dùng được cho người lớn không?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 2
- First strict rank: 2
- Top result: `dav_pdf_ocr` / `dosage` / `unverified_ocr` / DH-Pacegan 500

### gen_dosage_handoff_0005

- Question: Levical soft dùng thế nào?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 2
- Top result: `dav_all` / `drug_info` / `official_registry` / Levical soft

### gen_dosage_handoff_0006

- Question: Levical soft uống bao nhiêu viên mỗi ngày?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Levical soft

### gen_dosage_handoff_0007

- Question: Liều dùng Levical soft như thế nào?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 2
- Top result: `dav_all` / `drug_info` / `official_registry` / Levical soft

### gen_dosage_handoff_0008

- Question: Levical soft có dùng được cho người lớn không?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: False
- First relevant rank: 2
- First strict rank: None
- Top result: `dav_pdf_ocr` / `dosage` / `unverified_ocr` / Loratadin 10mg Kingphar

### gen_dosage_handoff_0009

- Question: Cyclolife dùng thế nào?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Cyclolife

### gen_dosage_handoff_0010

- Question: Cyclolife uống bao nhiêu viên mỗi ngày?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Cyclolife

### gen_dosage_handoff_0011

- Question: Liều dùng Cyclolife như thế nào?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 4
- First strict rank: 4
- Top result: `dav_pdf_ocr` / `safety` / `unverified_ocr` / Jazxylo Baby & Kid Spray

### gen_dosage_handoff_0012

- Question: Cyclolife có dùng được cho người lớn không?
- Category: dosage_handoff
- Hit@K: False | Strict Hit@K: False
- First relevant rank: None
- First strict rank: None
- Top result: `dav_pdf_ocr` / `dosage` / `unverified_ocr` / Loratadin 10mg Kingphar

### gen_dosage_handoff_0013

- Question: Midatoren 160/25 dùng thế nào?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Midatoren 160/25

### gen_dosage_handoff_0014

- Question: Midatoren 160/25 uống bao nhiêu viên mỗi ngày?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Midatoren 160/25

### gen_dosage_handoff_0015

- Question: Liều dùng Midatoren 160/25 như thế nào?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Midatoren 160/25

### gen_dosage_handoff_0016

- Question: Midatoren 160/25 có dùng được cho người lớn không?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Midatoren 160/25

### gen_dosage_handoff_0017

- Question: Cozaar 50mg (đóng gói tại PT Merck Sharp Dohme Pharma Tbk. Đại chỉ: JI. Raya Pandaan Km 48, Pandaan, Pasuruan, Jawwa Timur, Indonesia) dùng thế nào?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Cozaar 50mg (đóng gói tại PT Merck Sharp Dohme Pharma Tbk. Đại chỉ: JI. Raya Pandaan Km 48, Pandaan, Pasuruan, Jawwa Timur, Indonesia)

### gen_dosage_handoff_0018

- Question: Cozaar 50mg (đóng gói tại PT Merck Sharp Dohme Pharma Tbk. Đại chỉ: JI. Raya Pandaan Km 48, Pandaan, Pasuruan, Jawwa Timur, Indonesia) uống bao nhiêu viên mỗi ngày?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Cozaar 50mg (đóng gói tại PT Merck Sharp Dohme Pharma Tbk. Đại chỉ: JI. Raya Pandaan Km 48, Pandaan, Pasuruan, Jawwa Timur, Indonesia)

### gen_dosage_handoff_0019

- Question: Liều dùng Cozaar 50mg (đóng gói tại PT Merck Sharp Dohme Pharma Tbk. Đại chỉ: JI. Raya Pandaan Km 48, Pandaan, Pasuruan, Jawwa Timur, Indonesia) như thế nào?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Cozaar 50mg (đóng gói tại PT Merck Sharp Dohme Pharma Tbk. Đại chỉ: JI. Raya Pandaan Km 48, Pandaan, Pasuruan, Jawwa Timur, Indonesia)

### gen_dosage_handoff_0020

- Question: Cozaar 50mg (đóng gói tại PT Merck Sharp Dohme Pharma Tbk. Đại chỉ: JI. Raya Pandaan Km 48, Pandaan, Pasuruan, Jawwa Timur, Indonesia) có dùng được cho người lớn không?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Cozaar 50mg (đóng gói tại PT Merck Sharp Dohme Pharma Tbk. Đại chỉ: JI. Raya Pandaan Km 48, Pandaan, Pasuruan, Jawwa Timur, Indonesia)

### gen_dosage_handoff_0021

- Question: Terizidon dùng thế nào?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Terizidon

### gen_dosage_handoff_0022

- Question: Terizidon uống bao nhiêu viên mỗi ngày?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Terizidon

### gen_dosage_handoff_0023

- Question: Liều dùng Terizidon như thế nào?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 4
- First strict rank: 4
- Top result: `dav_pdf_ocr` / `safety` / `unverified_ocr` / Jazxylo Baby & Kid Spray

### gen_dosage_handoff_0024

- Question: Terizidon có dùng được cho người lớn không?
- Category: dosage_handoff
- Hit@K: False | Strict Hit@K: False
- First relevant rank: None
- First strict rank: None
- Top result: `dav_pdf_ocr` / `dosage` / `unverified_ocr` / Loratadin 10mg Kingphar

### gen_dosage_handoff_0025

- Question: Cốm Calci dùng thế nào?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Cốm Calci

### gen_dosage_handoff_0026

- Question: Cốm Calci uống bao nhiêu viên mỗi ngày?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 3
- First strict rank: 3
- Top result: `dav_all` / `drug_info` / `official_registry` / Keamin

### gen_dosage_handoff_0027

- Question: Liều dùng Cốm Calci như thế nào?
- Category: dosage_handoff
- Hit@K: False | Strict Hit@K: False
- First relevant rank: None
- First strict rank: None
- Top result: `dav_pdf_ocr` / `safety` / `unverified_ocr` / Jazxylo Baby & Kid Spray

### gen_dosage_handoff_0028

- Question: Cốm Calci có dùng được cho người lớn không?
- Category: dosage_handoff
- Hit@K: False | Strict Hit@K: False
- First relevant rank: None
- First strict rank: None
- Top result: `dav_pdf_ocr` / `dosage` / `unverified_ocr` / Loratadin 10mg Kingphar

### gen_dosage_handoff_0029

- Question: Vaco Allerf PE dùng thế nào?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 3
- Top result: `dav_all` / `drug_info` / `official_registry` / Vaco allerf PE

### gen_dosage_handoff_0030

- Question: Vaco Allerf PE uống bao nhiêu viên mỗi ngày?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 2
- Top result: `dav_all` / `drug_info` / `official_registry` / Vaco allerf PE

### gen_dosage_handoff_0031

- Question: Liều dùng Vaco Allerf PE như thế nào?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 2
- Top result: `dav_all` / `drug_info` / `official_registry` / Vaco allerf PE

### gen_dosage_handoff_0032

- Question: Vaco Allerf PE có dùng được cho người lớn không?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 3
- Top result: `dav_all` / `drug_info` / `official_registry` / Vaco allerf PE

### gen_dosage_handoff_0033

- Question: Giải cảm Nhất Nhất dùng thế nào?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Giải cảm Nhất Nhất

### gen_dosage_handoff_0034

- Question: Giải cảm Nhất Nhất uống bao nhiêu viên mỗi ngày?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Giải cảm Nhất Nhất

### gen_dosage_handoff_0035

- Question: Liều dùng Giải cảm Nhất Nhất như thế nào?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Giải cảm Nhất Nhất

### gen_dosage_handoff_0036

- Question: Giải cảm Nhất Nhất có dùng được cho người lớn không?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 5
- First strict rank: 5
- Top result: `dav_pdf_ocr` / `safety` / `unverified_ocr` / Nafacolex 400 mg

### gen_dosage_handoff_0037

- Question: Vitamin B6 dùng thế nào?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: False
- First relevant rank: 1
- First strict rank: None
- Top result: `dav_all` / `drug_info` / `official_registry` / Ngũ phúc tâm não thanh

### gen_dosage_handoff_0038

- Question: Vitamin B6 uống bao nhiêu viên mỗi ngày?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: False
- First relevant rank: 1
- First strict rank: None
- Top result: `dav_all` / `drug_info` / `official_registry` / Vitamin B6

### gen_dosage_handoff_0039

- Question: Liều dùng Vitamin B6 như thế nào?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: False
- First relevant rank: 5
- First strict rank: None
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / TGA: Cập nhật quy định mới nhằm giảm thiểu nguy cơ bệnh lý thần kinh ngoại biên khi sử dụng vitamin B6

### gen_dosage_handoff_0040

- Question: Vitamin B6 có dùng được cho người lớn không?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: False
- First relevant rank: 4
- First strict rank: None
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / TGA: Cập nhật quy định mới nhằm giảm thiểu nguy cơ bệnh lý thần kinh ngoại biên khi sử dụng vitamin B6

### gen_dosage_handoff_0041

- Question: Smofen dùng thế nào?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Smofen

### gen_dosage_handoff_0042

- Question: Smofen uống bao nhiêu viên mỗi ngày?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Smofen

### gen_dosage_handoff_0043

- Question: Liều dùng Smofen như thế nào?
- Category: dosage_handoff
- Hit@K: False | Strict Hit@K: False
- First relevant rank: None
- First strict rank: None
- Top result: `dav_pdf_ocr` / `safety` / `unverified_ocr` / Jazxylo Baby & Kid Spray

### gen_dosage_handoff_0044

- Question: Smofen có dùng được cho người lớn không?
- Category: dosage_handoff
- Hit@K: False | Strict Hit@K: False
- First relevant rank: None
- First strict rank: None
- Top result: `dav_pdf_ocr` / `dosage` / `unverified_ocr` / Loratadin 10mg Kingphar

### gen_dosage_handoff_0045

- Question: Atiferolyte 150 mg dùng thế nào?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Atiferolyte 150 mg

### gen_dosage_handoff_0046

- Question: Atiferolyte 150 mg uống bao nhiêu viên mỗi ngày?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Atiferolyte 150 mg

### gen_dosage_handoff_0047

- Question: Liều dùng Atiferolyte 150 mg như thế nào?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Atiferolyte 150 mg

### gen_dosage_handoff_0048

- Question: Atiferolyte 150 mg có dùng được cho người lớn không?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Atiferolyte 150 mg

### gen_dosage_handoff_0049

- Question: Friburine 40mg dùng thế nào?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Friburine 40mg

### gen_dosage_handoff_0050

- Question: Friburine 40mg uống bao nhiêu viên mỗi ngày?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Friburine 40mg

### gen_dosage_handoff_0051

- Question: Liều dùng Friburine 40mg như thế nào?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Friburine 40mg

### gen_dosage_handoff_0052

- Question: Friburine 40mg có dùng được cho người lớn không?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Friburine 40mg

### gen_dosage_handoff_0053

- Question: TS-One Capsule 25 dùng thế nào?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 2
- Top result: `dav_all` / `drug_info` / `official_registry` / TS-One capsule 25

### gen_dosage_handoff_0054

- Question: TS-One Capsule 25 uống bao nhiêu viên mỗi ngày?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 2
- Top result: `dav_all` / `drug_info` / `official_registry` / TS-One capsule 25

### gen_dosage_handoff_0055

- Question: Liều dùng TS-One Capsule 25 như thế nào?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 2
- Top result: `dav_all` / `drug_info` / `official_registry` / TS-One capsule 25

### gen_dosage_handoff_0056

- Question: TS-One Capsule 25 có dùng được cho người lớn không?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 2
- Top result: `dav_all` / `drug_info` / `official_registry` / TS-One capsule 25

### gen_dosage_handoff_0057

- Question: Sulfareptol 960 dùng thế nào?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Sulfareptol 960

### gen_dosage_handoff_0058

- Question: Sulfareptol 960 uống bao nhiêu viên mỗi ngày?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Sulfareptol 960

### gen_dosage_handoff_0059

- Question: Liều dùng Sulfareptol 960 như thế nào?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Sulfareptol 960

### gen_dosage_handoff_0060

- Question: Sulfareptol 960 có dùng được cho người lớn không?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Sulfareptol 960

### gen_dosage_handoff_0061

- Question: Taginba dùng thế nào?
- Category: dosage_handoff
- Hit@K: False | Strict Hit@K: False
- First relevant rank: None
- First strict rank: None
- Top result: `dav_all` / `drug_info` / `official_registry` / Dầu khuynh diệp Trường Sơn

### gen_dosage_handoff_0062

- Question: Taginba uống bao nhiêu viên mỗi ngày?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Taginba

### gen_dosage_handoff_0063

- Question: Liều dùng Taginba như thế nào?
- Category: dosage_handoff
- Hit@K: False | Strict Hit@K: False
- First relevant rank: None
- First strict rank: None
- Top result: `dav_pdf_ocr` / `safety` / `unverified_ocr` / Jazxylo Baby & Kid Spray

### gen_dosage_handoff_0064

- Question: Taginba có dùng được cho người lớn không?
- Category: dosage_handoff
- Hit@K: False | Strict Hit@K: False
- First relevant rank: None
- First strict rank: None
- Top result: `dav_pdf_ocr` / `dosage` / `unverified_ocr` / Loratadin 10mg Kingphar

### gen_dosage_handoff_0065

- Question: Glimepirid dùng thế nào?
- Category: dosage_handoff
- Hit@K: False | Strict Hit@K: False
- First relevant rank: None
- First strict rank: None
- Top result: `dav_all` / `drug_info` / `official_registry` / Dầu khuynh diệp Trường Sơn

### gen_dosage_handoff_0066

- Question: Glimepirid uống bao nhiêu viên mỗi ngày?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: False
- First relevant rank: 1
- First strict rank: None
- Top result: `dav_all` / `drug_info` / `official_registry` / Glemaz

### gen_dosage_handoff_0067

- Question: Liều dùng Glimepirid như thế nào?
- Category: dosage_handoff
- Hit@K: False | Strict Hit@K: False
- First relevant rank: None
- First strict rank: None
- Top result: `dav_pdf_ocr` / `safety` / `unverified_ocr` / Jazxylo Baby & Kid Spray

### gen_dosage_handoff_0068

- Question: Glimepirid có dùng được cho người lớn không?
- Category: dosage_handoff
- Hit@K: False | Strict Hit@K: False
- First relevant rank: None
- First strict rank: None
- Top result: `dav_pdf_ocr` / `dosage` / `unverified_ocr` / Loratadin 10mg Kingphar

### gen_dosage_handoff_0069

- Question: Thysedow 5 mg dùng thế nào?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Thysedow 5 mg

### gen_dosage_handoff_0070

- Question: Thysedow 5 mg uống bao nhiêu viên mỗi ngày?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Thysedow 5 mg

### gen_dosage_handoff_0071

- Question: Liều dùng Thysedow 5 mg như thế nào?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Thysedow 5 mg

### gen_dosage_handoff_0072

- Question: Thysedow 5 mg có dùng được cho người lớn không?
- Category: dosage_handoff
- Hit@K: False | Strict Hit@K: False
- First relevant rank: None
- First strict rank: None
- Top result: `dav_pdf_ocr` / `dosage` / `unverified_ocr` / Loratadin 10mg Kingphar

### gen_dosage_handoff_0073

- Question: Glucoform 850 dùng thế nào?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Glucoform 850

### gen_dosage_handoff_0074

- Question: Glucoform 850 uống bao nhiêu viên mỗi ngày?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Glucoform 850

### gen_dosage_handoff_0075

- Question: Liều dùng Glucoform 850 như thế nào?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Glucoform 850

### gen_dosage_handoff_0076

- Question: Glucoform 850 có dùng được cho người lớn không?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Glucoform 850

### gen_dosage_handoff_0077

- Question: Donalium- DN dùng thế nào?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 3
- First strict rank: 3
- Top result: `dav_all` / `drug_info` / `official_registry` / Donalium - DN

### gen_dosage_handoff_0078

- Question: Donalium- DN uống bao nhiêu viên mỗi ngày?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 3
- First strict rank: 3
- Top result: `dav_all` / `drug_info` / `official_registry` / Donalium - DN

### gen_dosage_handoff_0079

- Question: Liều dùng Donalium- DN như thế nào?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 2
- First strict rank: 2
- Top result: `dav_all` / `drug_info` / `official_registry` / Donalium - DN

### gen_dosage_handoff_0080

- Question: Donalium- DN có dùng được cho người lớn không?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 3
- First strict rank: 3
- Top result: `dav_all` / `drug_info` / `official_registry` / Donalium - DN

### gen_dosage_handoff_0081

- Question: Agilosart - H 100/12,5 dùng thế nào?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Agilosart - H 100/12,5

### gen_dosage_handoff_0082

- Question: Agilosart - H 100/12,5 uống bao nhiêu viên mỗi ngày?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Agilosart - H 100/12,5

### gen_dosage_handoff_0083

- Question: Liều dùng Agilosart - H 100/12,5 như thế nào?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Agilosart - H 100/12,5

### gen_dosage_handoff_0084

- Question: Agilosart - H 100/12,5 có dùng được cho người lớn không?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Agilosart - H 100/12,5

### gen_dosage_handoff_0085

- Question: Alpodox dùng thế nào?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Alpodox

### gen_dosage_handoff_0086

- Question: Alpodox uống bao nhiêu viên mỗi ngày?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Alpodox

### gen_dosage_handoff_0087

- Question: Liều dùng Alpodox như thế nào?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 4
- First strict rank: 4
- Top result: `dav_pdf_ocr` / `safety` / `unverified_ocr` / Jazxylo Baby & Kid Spray

### gen_dosage_handoff_0088

- Question: Alpodox có dùng được cho người lớn không?
- Category: dosage_handoff
- Hit@K: False | Strict Hit@K: False
- First relevant rank: None
- First strict rank: None
- Top result: `dav_pdf_ocr` / `dosage` / `unverified_ocr` / Loratadin 10mg Kingphar

### gen_dosage_handoff_0089

- Question: Lycoplan 200mg dùng thế nào?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Lycoplan 200mg

### gen_dosage_handoff_0090

- Question: Lycoplan 200mg uống bao nhiêu viên mỗi ngày?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Lycoplan 200mg

### gen_dosage_handoff_0091

- Question: Liều dùng Lycoplan 200mg như thế nào?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Lycoplan 200mg

### gen_dosage_handoff_0092

- Question: Lycoplan 200mg có dùng được cho người lớn không?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Lycoplan 200mg

### gen_dosage_handoff_0093

- Question: Dentgital dùng thế nào?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 2
- Top result: `dav_all` / `drug_info` / `official_registry` / Dentgital

### gen_dosage_handoff_0094

- Question: Dentgital uống bao nhiêu viên mỗi ngày?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 2
- Top result: `dav_all` / `drug_info` / `official_registry` / Dentgital

### gen_dosage_handoff_0095

- Question: Liều dùng Dentgital như thế nào?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 2
- Top result: `dav_all` / `drug_info` / `official_registry` / Dentgital

### gen_dosage_handoff_0096

- Question: Dentgital có dùng được cho người lớn không?
- Category: dosage_handoff
- Hit@K: False | Strict Hit@K: False
- First relevant rank: None
- First strict rank: None
- Top result: `dav_pdf_ocr` / `dosage` / `unverified_ocr` / Loratadin 10mg Kingphar

### gen_dosage_handoff_0097

- Question: Xalexa 30 dùng thế nào?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Xalexa 30

### gen_dosage_handoff_0098

- Question: Xalexa 30 uống bao nhiêu viên mỗi ngày?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Xalexa 30

### gen_dosage_handoff_0099

- Question: Liều dùng Xalexa 30 như thế nào?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Xalexa 30

### gen_dosage_handoff_0100

- Question: Xalexa 30 có dùng được cho người lớn không?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 4
- First strict rank: 4
- Top result: `dav_pdf_ocr` / `drug_info` / `unverified_ocr` / Fexosin 30

### gen_dosage_handoff_0101

- Question: Medotor - 10 dùng thế nào?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Medotor - 10

### gen_dosage_handoff_0102

- Question: Medotor - 10 uống bao nhiêu viên mỗi ngày?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Medotor - 10

### gen_dosage_handoff_0103

- Question: Liều dùng Medotor - 10 như thế nào?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Medotor - 10

### gen_dosage_handoff_0104

- Question: Medotor - 10 có dùng được cho người lớn không?
- Category: dosage_handoff
- Hit@K: False | Strict Hit@K: False
- First relevant rank: None
- First strict rank: None
- Top result: `dav_pdf_ocr` / `dosage` / `unverified_ocr` / Loratadin 10mg Kingphar

### gen_dosage_handoff_0105

- Question: Pletimizol dùng thế nào?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Pletimizol

### gen_dosage_handoff_0106

- Question: Pletimizol uống bao nhiêu viên mỗi ngày?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Pletimizol

### gen_dosage_handoff_0107

- Question: Liều dùng Pletimizol như thế nào?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 4
- First strict rank: 4
- Top result: `dav_pdf_ocr` / `safety` / `unverified_ocr` / Jazxylo Baby & Kid Spray

### gen_dosage_handoff_0108

- Question: Pletimizol có dùng được cho người lớn không?
- Category: dosage_handoff
- Hit@K: False | Strict Hit@K: False
- First relevant rank: None
- First strict rank: None
- Top result: `dav_pdf_ocr` / `dosage` / `unverified_ocr` / Loratadin 10mg Kingphar

### gen_dosage_handoff_0109

- Question: Atigluco 500 dùng thế nào?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Atigluco 500

### gen_dosage_handoff_0110

- Question: Atigluco 500 uống bao nhiêu viên mỗi ngày?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Atigluco 500

### gen_dosage_handoff_0111

- Question: Liều dùng Atigluco 500 như thế nào?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Atigluco 500

### gen_dosage_handoff_0112

- Question: Atigluco 500 có dùng được cho người lớn không?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 5
- First strict rank: 5
- Top result: `dav_pdf_ocr` / `dosage` / `unverified_ocr` / DH-Pacegan 500

### gen_dosage_handoff_0113

- Question: SaViPamol 650 dùng thế nào?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / SaViPamol 650

### gen_dosage_handoff_0114

- Question: SaViPamol 650 uống bao nhiêu viên mỗi ngày?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / SaViPamol 650

### gen_dosage_handoff_0115

- Question: Liều dùng SaViPamol 650 như thế nào?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / SaViPamol 650

### gen_dosage_handoff_0116

- Question: SaViPamol 650 có dùng được cho người lớn không?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / SaViPamol 650

### gen_dosage_handoff_0117

- Question: Azzol-S 150 mg/cap dùng thế nào?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Azzol-S 150 mg/cap

### gen_dosage_handoff_0118

- Question: Azzol-S 150 mg/cap uống bao nhiêu viên mỗi ngày?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Azzol-S 150 mg/cap

### gen_dosage_handoff_0119

- Question: Liều dùng Azzol-S 150 mg/cap như thế nào?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Azzol-S 150 mg/cap

### gen_dosage_handoff_0120

- Question: Azzol-S 150 mg/cap có dùng được cho người lớn không?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Azzol-S 150 mg/cap

### gen_dosage_handoff_0121

- Question: Atromux 10 dùng thế nào?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Atromux 10

### gen_dosage_handoff_0122

- Question: Atromux 10 uống bao nhiêu viên mỗi ngày?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Atromux 10

### gen_dosage_handoff_0123

- Question: Liều dùng Atromux 10 như thế nào?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Atromux 10

### gen_dosage_handoff_0124

- Question: Atromux 10 có dùng được cho người lớn không?
- Category: dosage_handoff
- Hit@K: False | Strict Hit@K: False
- First relevant rank: None
- First strict rank: None
- Top result: `dav_pdf_ocr` / `dosage` / `unverified_ocr` / Loratadin 10mg Kingphar

### gen_dosage_handoff_0125

- Question: Human Albumin Takeda 250g/l dùng thế nào?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Human Albumin Takeda 250g/l

### gen_dosage_handoff_0126

- Question: Human Albumin Takeda 250g/l uống bao nhiêu viên mỗi ngày?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Human Albumin Takeda 250g/l

### gen_dosage_handoff_0127

- Question: Liều dùng Human Albumin Takeda 250g/l như thế nào?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Human Albumin Takeda 250g/l

### gen_dosage_handoff_0128

- Question: Human Albumin Takeda 250g/l có dùng được cho người lớn không?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Human Albumin Takeda 250g/l

### gen_dosage_handoff_0129

- Question: VacoCipdex 0,3% dùng thế nào?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 2
- First strict rank: 2
- Top result: `dav_all` / `drug_info` / `official_registry` / Vacocipdex 500 Tab

### gen_dosage_handoff_0130

- Question: VacoCipdex 0,3% uống bao nhiêu viên mỗi ngày?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 2
- First strict rank: 2
- Top result: `dav_all` / `drug_info` / `official_registry` / Vacocipdex 500

### gen_dosage_handoff_0131

- Question: Liều dùng VacoCipdex 0,3% như thế nào?
- Category: dosage_handoff
- Hit@K: False | Strict Hit@K: False
- First relevant rank: None
- First strict rank: None
- Top result: `dav_pdf_ocr` / `safety` / `unverified_ocr` / Jazxylo Baby & Kid Spray

### gen_dosage_handoff_0132

- Question: VacoCipdex 0,3% có dùng được cho người lớn không?
- Category: dosage_handoff
- Hit@K: False | Strict Hit@K: False
- First relevant rank: None
- First strict rank: None
- Top result: `dav_pdf_ocr` / `dosage` / `unverified_ocr` / Loratadin 10mg Kingphar

### gen_dosage_handoff_0133

- Question: Vifamox 250 dùng thế nào?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Vifamox 250

### gen_dosage_handoff_0134

- Question: Vifamox 250 uống bao nhiêu viên mỗi ngày?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Vifamox 250

### gen_dosage_handoff_0135

- Question: Liều dùng Vifamox 250 như thế nào?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 2
- Top result: `dav_all` / `drug_info` / `official_registry` / Vifamox 250

### gen_dosage_handoff_0136

- Question: Vifamox 250 có dùng được cho người lớn không?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 2
- Top result: `dav_all` / `drug_info` / `official_registry` / Vifamox 250

### gen_dosage_handoff_0137

- Question: Calcicar 500 Tablet dùng thế nào?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Calcicar 500 Tablet

### gen_dosage_handoff_0138

- Question: Calcicar 500 Tablet uống bao nhiêu viên mỗi ngày?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Calcicar 500 Tablet

### gen_dosage_handoff_0139

- Question: Liều dùng Calcicar 500 Tablet như thế nào?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Calcicar 500 Tablet

### gen_dosage_handoff_0140

- Question: Calcicar 500 Tablet có dùng được cho người lớn không?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 2
- First strict rank: 2
- Top result: `dav_pdf_ocr` / `dosage` / `unverified_ocr` / DH-Pacegan 500

### gen_dosage_handoff_0141

- Question: Sanfetil 200 dùng thế nào?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Sanfetil 200

### gen_dosage_handoff_0142

- Question: Sanfetil 200 uống bao nhiêu viên mỗi ngày?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Sanfetil 200

### gen_dosage_handoff_0143

- Question: Liều dùng Sanfetil 200 như thế nào?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Sanfetil 200

### gen_dosage_handoff_0144

- Question: Sanfetil 200 có dùng được cho người lớn không?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 2
- First strict rank: 2
- Top result: `dav_pdf_ocr` / `safety` / `unverified_ocr` / Paracetamol 325 mg/Ibuprofen 200 mg

### gen_dosage_handoff_0145

- Question: Triamvirgri dùng thế nào?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Triamvirgri

### gen_dosage_handoff_0146

- Question: Triamvirgri uống bao nhiêu viên mỗi ngày?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Triamvirgri

### gen_dosage_handoff_0147

- Question: Liều dùng Triamvirgri như thế nào?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 2
- First strict rank: 2
- Top result: `dav_pdf_ocr` / `safety` / `unverified_ocr` / Jazxylo Baby & Kid Spray

### gen_dosage_handoff_0148

- Question: Triamvirgri có dùng được cho người lớn không?
- Category: dosage_handoff
- Hit@K: False | Strict Hit@K: False
- First relevant rank: None
- First strict rank: None
- Top result: `dav_pdf_ocr` / `dosage` / `unverified_ocr` / Loratadin 10mg Kingphar

### gen_dosage_handoff_0149

- Question: Vorifend Forte dùng thế nào?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 4
- Top result: `dav_all` / `drug_info` / `official_registry` / Vorifend Forte

### gen_dosage_handoff_0150

- Question: Vorifend Forte uống bao nhiêu viên mỗi ngày?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 2
- Top result: `dav_all` / `drug_info` / `official_registry` / Vorifend Forte

### gen_dosage_handoff_0151

- Question: Liều dùng Vorifend Forte như thế nào?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 3
- Top result: `dav_all` / `drug_info` / `official_registry` / Vorifend Forte

### gen_dosage_handoff_0152

- Question: Vorifend Forte có dùng được cho người lớn không?
- Category: dosage_handoff
- Hit@K: False | Strict Hit@K: False
- First relevant rank: None
- First strict rank: None
- Top result: `dav_pdf_ocr` / `dosage` / `unverified_ocr` / Loratadin 10mg Kingphar

### gen_dosage_handoff_0153

- Question: Azaretin - H Cream dùng thế nào?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Azaretin - H Cream

### gen_dosage_handoff_0154

- Question: Azaretin - H Cream uống bao nhiêu viên mỗi ngày?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Azaretin - H Cream

### gen_dosage_handoff_0155

- Question: Liều dùng Azaretin - H Cream như thế nào?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Azaretin - H Cream

### gen_dosage_handoff_0156

- Question: Azaretin - H Cream có dùng được cho người lớn không?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 2
- First strict rank: 2
- Top result: `dav_pdf_ocr` / `dosage` / `unverified_ocr` / Loratadin 10mg Kingphar

### gen_dosage_handoff_0157

- Question: Heralopres H 25 dùng thế nào?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Heralopres H 25

### gen_dosage_handoff_0158

- Question: Heralopres H 25 uống bao nhiêu viên mỗi ngày?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Heralopres H 25

### gen_dosage_handoff_0159

- Question: Liều dùng Heralopres H 25 như thế nào?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Heralopres H 25

### gen_dosage_handoff_0160

- Question: Heralopres H 25 có dùng được cho người lớn không?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 2
- First strict rank: 2
- Top result: `dav_pdf_ocr` / `dosage` / `unverified_ocr` / Bropexto

### gen_dosage_handoff_0161

- Question: Podus dùng thế nào?
- Category: dosage_handoff
- Hit@K: False | Strict Hit@K: False
- First relevant rank: None
- First strict rank: None
- Top result: `dav_all` / `drug_info` / `official_registry` / Dầu khuynh diệp Trường Sơn

### gen_dosage_handoff_0162

- Question: Podus uống bao nhiêu viên mỗi ngày?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 3
- Top result: `dav_all` / `drug_info` / `official_registry` / Podus

### gen_dosage_handoff_0163

- Question: Liều dùng Podus như thế nào?
- Category: dosage_handoff
- Hit@K: False | Strict Hit@K: False
- First relevant rank: None
- First strict rank: None
- Top result: `dav_pdf_ocr` / `safety` / `unverified_ocr` / Jazxylo Baby & Kid Spray

### gen_dosage_handoff_0164

- Question: Podus có dùng được cho người lớn không?
- Category: dosage_handoff
- Hit@K: False | Strict Hit@K: False
- First relevant rank: None
- First strict rank: None
- Top result: `dav_pdf_ocr` / `dosage` / `unverified_ocr` / Loratadin 10mg Kingphar

### gen_dosage_handoff_0165

- Question: Gabahasan 300 dùng thế nào?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Gabahasan 300

### gen_dosage_handoff_0166

- Question: Gabahasan 300 uống bao nhiêu viên mỗi ngày?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 2
- Top result: `dav_all` / `drug_info` / `official_registry` / Gabahasan 300

### gen_dosage_handoff_0167

- Question: Liều dùng Gabahasan 300 như thế nào?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Gabahasan 300

### gen_dosage_handoff_0168

- Question: Gabahasan 300 có dùng được cho người lớn không?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Gabahasan 300

### gen_dosage_handoff_0169

- Question: Calcitron dùng thế nào?
- Category: dosage_handoff
- Hit@K: False | Strict Hit@K: False
- First relevant rank: None
- First strict rank: None
- Top result: `dav_all` / `drug_info` / `official_registry` / Dầu khuynh diệp Trường Sơn

### gen_dosage_handoff_0170

- Question: Calcitron uống bao nhiêu viên mỗi ngày?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Calcitron

### gen_dosage_handoff_0171

- Question: Liều dùng Calcitron như thế nào?
- Category: dosage_handoff
- Hit@K: False | Strict Hit@K: False
- First relevant rank: None
- First strict rank: None
- Top result: `dav_pdf_ocr` / `safety` / `unverified_ocr` / Jazxylo Baby & Kid Spray

### gen_dosage_handoff_0172

- Question: Calcitron có dùng được cho người lớn không?
- Category: dosage_handoff
- Hit@K: False | Strict Hit@K: False
- First relevant rank: None
- First strict rank: None
- Top result: `dav_pdf_ocr` / `dosage` / `unverified_ocr` / Loratadin 10mg Kingphar

### gen_dosage_handoff_0173

- Question: Acarbose DWP 25 mg dùng thế nào?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Acarbose DWP 25 mg

### gen_dosage_handoff_0174

- Question: Acarbose DWP 25 mg uống bao nhiêu viên mỗi ngày?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Acarbose DWP 25 mg

### gen_dosage_handoff_0175

- Question: Liều dùng Acarbose DWP 25 mg như thế nào?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Acarbose DWP 25 mg

### gen_dosage_handoff_0176

- Question: Acarbose DWP 25 mg có dùng được cho người lớn không?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Acarbose DWP 25 mg

### gen_dosage_handoff_0177

- Question: Pemetrexed Biovagen dùng thế nào?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Pemetrexed Biovagen

### gen_dosage_handoff_0178

- Question: Pemetrexed Biovagen uống bao nhiêu viên mỗi ngày?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Pemetrexed Biovagen

### gen_dosage_handoff_0179

- Question: Liều dùng Pemetrexed Biovagen như thế nào?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Pemetrexed Biovagen

### gen_dosage_handoff_0180

- Question: Pemetrexed Biovagen có dùng được cho người lớn không?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Pemetrexed Biovagen

### gen_dosage_handoff_0181

- Question: Lorabipha Tab. dùng thế nào?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Lorabipha Tab.

### gen_dosage_handoff_0182

- Question: Lorabipha Tab. uống bao nhiêu viên mỗi ngày?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Lorabipha Tab.

### gen_dosage_handoff_0183

- Question: Liều dùng Lorabipha Tab. như thế nào?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Lorabipha Tab.

### gen_dosage_handoff_0184

- Question: Lorabipha Tab. có dùng được cho người lớn không?
- Category: dosage_handoff
- Hit@K: False | Strict Hit@K: False
- First relevant rank: None
- First strict rank: None
- Top result: `dav_pdf_ocr` / `dosage` / `unverified_ocr` / Loratadin 10mg Kingphar

### gen_dosage_handoff_0185

- Question: Kupfolin dùng thế nào?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Kupfolin

### gen_dosage_handoff_0186

- Question: Kupfolin uống bao nhiêu viên mỗi ngày?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Kupfolin

### gen_dosage_handoff_0187

- Question: Liều dùng Kupfolin như thế nào?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 4
- First strict rank: 4
- Top result: `dav_pdf_ocr` / `safety` / `unverified_ocr` / Jazxylo Baby & Kid Spray

### gen_dosage_handoff_0188

- Question: Kupfolin có dùng được cho người lớn không?
- Category: dosage_handoff
- Hit@K: False | Strict Hit@K: False
- First relevant rank: None
- First strict rank: None
- Top result: `dav_pdf_ocr` / `dosage` / `unverified_ocr` / Loratadin 10mg Kingphar

### gen_dosage_handoff_0189

- Question: Fizoti Inj. dùng thế nào?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 2
- First strict rank: 3
- Top result: `dav_all` / `drug_info` / `official_registry` / Fizoti Inj

### gen_dosage_handoff_0190

- Question: Fizoti Inj. uống bao nhiêu viên mỗi ngày?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 2
- First strict rank: 4
- Top result: `dav_all` / `drug_info` / `official_registry` / Fizoti Inj

### gen_dosage_handoff_0191

- Question: Liều dùng Fizoti Inj. như thế nào?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 3
- First strict rank: 4
- Top result: `dav_all` / `drug_info` / `official_registry` / Fizoti Inj

### gen_dosage_handoff_0192

- Question: Fizoti Inj. có dùng được cho người lớn không?
- Category: dosage_handoff
- Hit@K: False | Strict Hit@K: False
- First relevant rank: None
- First strict rank: None
- Top result: `dav_pdf_ocr` / `dosage` / `unverified_ocr` / Loratadin 10mg Kingphar

### gen_dosage_handoff_0193

- Question: Hadusim 20 dùng thế nào?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Hadusim 20

### gen_dosage_handoff_0194

- Question: Hadusim 20 uống bao nhiêu viên mỗi ngày?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Hadusim 20

### gen_dosage_handoff_0195

- Question: Liều dùng Hadusim 20 như thế nào?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Hadusim 20

### gen_dosage_handoff_0196

- Question: Hadusim 20 có dùng được cho người lớn không?
- Category: dosage_handoff
- Hit@K: False | Strict Hit@K: False
- First relevant rank: None
- First strict rank: None
- Top result: `dav_pdf_ocr` / `drug_info` / `unverified_ocr` / Desloratadin MCN 5 ODT

### gen_dosage_handoff_0197

- Question: Degas dùng thế nào?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Degas

### gen_dosage_handoff_0198

- Question: Degas uống bao nhiêu viên mỗi ngày?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Degas

### gen_dosage_handoff_0199

- Question: Liều dùng Degas như thế nào?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Degas

### gen_dosage_handoff_0200

- Question: Degas có dùng được cho người lớn không?
- Category: dosage_handoff
- Hit@K: False | Strict Hit@K: False
- First relevant rank: None
- First strict rank: None
- Top result: `dav_pdf_ocr` / `dosage` / `unverified_ocr` / Loratadin 10mg Kingphar

### gen_dosage_handoff_0201

- Question: Ampicilin 500 mg dùng thế nào?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 3
- First strict rank: 5
- Top result: `dav_all` / `drug_info` / `official_registry` / Ampicilline 500 mg

### gen_dosage_handoff_0202

- Question: Ampicilin 500 mg uống bao nhiêu viên mỗi ngày?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: False
- First relevant rank: 3
- First strict rank: None
- Top result: `dav_all` / `drug_info` / `official_registry` / Ampicilin 
500 mg

### gen_dosage_handoff_0203

- Question: Liều dùng Ampicilin 500 mg như thế nào?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: False
- First relevant rank: 3
- First strict rank: None
- Top result: `dav_all` / `drug_info` / `official_registry` / Ampicilline 500 mg

### gen_dosage_handoff_0204

- Question: Ampicilin 500 mg có dùng được cho người lớn không?
- Category: dosage_handoff
- Hit@K: False | Strict Hit@K: False
- First relevant rank: None
- First strict rank: None
- Top result: `dav_pdf_ocr` / `dosage` / `unverified_ocr` / DH-Pacegan 500

### gen_dosage_handoff_0205

- Question: Nhuận gan lợi mật dùng thế nào?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Nhuận gan lợi mật

### gen_dosage_handoff_0206

- Question: Nhuận gan lợi mật uống bao nhiêu viên mỗi ngày?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Nhuận gan lợi mật

### gen_dosage_handoff_0207

- Question: Liều dùng Nhuận gan lợi mật như thế nào?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Nhuận gan lợi mật

### gen_dosage_handoff_0208

- Question: Nhuận gan lợi mật có dùng được cho người lớn không?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Nhuận gan lợi mật

### gen_dosage_handoff_0209

- Question: Thuốc tiêm Metronidazole dùng thế nào?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Thuốc tiêm Metronidazole

### gen_dosage_handoff_0210

- Question: Thuốc tiêm Metronidazole uống bao nhiêu viên mỗi ngày?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 2
- First strict rank: 2
- Top result: `dav_all` / `drug_info` / `official_registry` / Metronidazole Normon 5mg/ml Solution For Infusion

### gen_dosage_handoff_0211

- Question: Liều dùng Thuốc tiêm Metronidazole như thế nào?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 2
- First strict rank: 2
- Top result: `dav_pdf_ocr` / `safety` / `unverified_ocr` / Jazxylo Baby & Kid Spray

### gen_dosage_handoff_0212

- Question: Thuốc tiêm Metronidazole có dùng được cho người lớn không?
- Category: dosage_handoff
- Hit@K: False | Strict Hit@K: False
- First relevant rank: None
- First strict rank: None
- Top result: `dav_pdf_ocr` / `dosage` / `unverified_ocr` / Loratadin 10mg Kingphar

### gen_dosage_handoff_0213

- Question: Avastin dùng thế nào?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 4
- Top result: `dav_all` / `drug_info` / `official_registry` / Avastin

### gen_dosage_handoff_0214

- Question: Avastin uống bao nhiêu viên mỗi ngày?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 2
- Top result: `dav_all` / `drug_info` / `official_registry` / Avastin

### gen_dosage_handoff_0215

- Question: Liều dùng Avastin như thế nào?
- Category: dosage_handoff
- Hit@K: True | Strict Hit@K: False
- First relevant rank: 1
- First strict rank: None
- Top result: `dav_all` / `drug_info` / `official_registry` / Avastin

### gen_dosage_handoff_0216

- Question: Avastin có dùng được cho người lớn không?
- Category: dosage_handoff
- Hit@K: False | Strict Hit@K: False
- First relevant rank: None
- First strict rank: None
- Top result: `dav_pdf_ocr` / `dosage` / `unverified_ocr` / Loratadin 10mg Kingphar

### gen_high_risk_0001

- Question: Tôi đang mang thai có dùng AstaPadol 500 mg được không?
- Category: high_risk_context
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 2
- First strict rank: 2
- Top result: `dav_pdf_ocr` / `dosage` / `unverified_ocr` / DH-Pacegan 500

### gen_high_risk_0002

- Question: Trẻ em dùng AstaPadol 500 mg được không?
- Category: high_risk_context
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 5
- First strict rank: 5
- Top result: `dav_pdf` / `drug_info` / `official_registry` / Shinmus

### gen_high_risk_0003

- Question: Tôi bị suy gan có dùng AstaPadol 500 mg được không?
- Category: high_risk_context
- Hit@K: False | Strict Hit@K: False
- First relevant rank: None
- First strict rank: None
- Top result: `dav_pdf_ocr` / `dosage` / `unverified_ocr` / Novopetie suppo paracetamol 80 mg

### gen_high_risk_0004

- Question: Tôi bị suy thận có uống AstaPadol 500 mg được không?
- Category: high_risk_context
- Hit@K: False | Strict Hit@K: False
- First relevant rank: None
- First strict rank: None
- Top result: `dav_pdf_ocr` / `dosage` / `unverified_ocr` / Effer phazandol cafein 65

### gen_high_risk_0005

- Question: Tôi đang cho con bú dùng AstaPadol 500 mg có an toàn không?
- Category: high_risk_context
- Hit@K: False | Strict Hit@K: False
- First relevant rank: None
- First strict rank: None
- Top result: `dav_pdf_ocr` / `drug_info` / `unverified_ocr` / Effer phazandol cafein 65

### gen_high_risk_0006

- Question: Tôi đang mang thai có dùng Levical soft được không?
- Category: high_risk_context
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 2
- Top result: `dav_all` / `drug_info` / `official_registry` / Levical soft

### gen_high_risk_0007

- Question: Trẻ em dùng Levical soft được không?
- Category: high_risk_context
- Hit@K: True | Strict Hit@K: False
- First relevant rank: 3
- First strict rank: None
- Top result: `dav_pdf_ocr` / `dosage` / `unverified_ocr` / Loratadin 10mg Kingphar

### gen_high_risk_0008

- Question: Tôi bị suy gan có dùng Levical soft được không?
- Category: high_risk_context
- Hit@K: False | Strict Hit@K: False
- First relevant rank: None
- First strict rank: None
- Top result: `dav_pdf_ocr` / `drug_info` / `unverified_ocr` / Effer phazandol cafein 65

### gen_high_risk_0009

- Question: Tôi bị suy thận có uống Levical soft được không?
- Category: high_risk_context
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 3
- First strict rank: 3
- Top result: `dav_pdf_ocr` / `dosage` / `unverified_ocr` / Effer phazandol cafein 65

### gen_high_risk_0010

- Question: Tôi đang cho con bú dùng Levical soft có an toàn không?
- Category: high_risk_context
- Hit@K: False | Strict Hit@K: False
- First relevant rank: None
- First strict rank: None
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / Sử dụng metronidazol ở phụ nữ cho con bú

### gen_high_risk_0011

- Question: Tôi đang mang thai có dùng Cyclolife được không?
- Category: high_risk_context
- Hit@K: False | Strict Hit@K: False
- First relevant rank: None
- First strict rank: None
- Top result: `dav_pdf_ocr` / `drug_info` / `unverified_ocr` / Levonorgestrel 
1,5 mg

### gen_high_risk_0012

- Question: Trẻ em dùng Cyclolife được không?
- Category: high_risk_context
- Hit@K: False | Strict Hit@K: False
- First relevant rank: None
- First strict rank: None
- Top result: `dav_pdf_ocr` / `dosage` / `unverified_ocr` / Loratadin 10mg Kingphar

### gen_high_risk_0013

- Question: Tôi bị suy gan có dùng Cyclolife được không?
- Category: high_risk_context
- Hit@K: False | Strict Hit@K: False
- First relevant rank: None
- First strict rank: None
- Top result: `dav_pdf_ocr` / `drug_info` / `unverified_ocr` / Effer phazandol cafein 65

### gen_high_risk_0014

- Question: Tôi bị suy thận có uống Cyclolife được không?
- Category: high_risk_context
- Hit@K: False | Strict Hit@K: False
- First relevant rank: None
- First strict rank: None
- Top result: `dav_pdf_ocr` / `dosage` / `unverified_ocr` / Effer phazandol cafein 65

### gen_high_risk_0015

- Question: Tôi đang cho con bú dùng Cyclolife có an toàn không?
- Category: high_risk_context
- Hit@K: False | Strict Hit@K: False
- First relevant rank: None
- First strict rank: None
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / Sử dụng metronidazol ở phụ nữ cho con bú

### gen_high_risk_0016

- Question: Tôi đang mang thai có dùng Midatoren 160/25 được không?
- Category: high_risk_context
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Midatoren 160/25

### gen_high_risk_0017

- Question: Trẻ em dùng Midatoren 160/25 được không?
- Category: high_risk_context
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Midatoren 160/25

### gen_high_risk_0018

- Question: Tôi bị suy gan có dùng Midatoren 160/25 được không?
- Category: high_risk_context
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Midatoren 160/25

### gen_high_risk_0019

- Question: Tôi bị suy thận có uống Midatoren 160/25 được không?
- Category: high_risk_context
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Midatoren 160/25

### gen_high_risk_0020

- Question: Tôi đang cho con bú dùng Midatoren 160/25 có an toàn không?
- Category: high_risk_context
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Midatoren 160/25

### gen_high_risk_0021

- Question: Tôi đang mang thai có dùng Cozaar 50mg (đóng gói tại PT Merck Sharp Dohme Pharma Tbk. Đại chỉ: JI. Raya Pandaan Km 48, Pandaan, Pasuruan, Jawwa Timur, Indonesia) được không?
- Category: high_risk_context
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Cozaar 50mg (đóng gói tại PT Merck Sharp Dohme Pharma Tbk. Đại chỉ: JI. Raya Pandaan Km 48, Pandaan, Pasuruan, Jawwa Timur, Indonesia)

### gen_high_risk_0022

- Question: Trẻ em dùng Cozaar 50mg (đóng gói tại PT Merck Sharp Dohme Pharma Tbk. Đại chỉ: JI. Raya Pandaan Km 48, Pandaan, Pasuruan, Jawwa Timur, Indonesia) được không?
- Category: high_risk_context
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Cozaar 50mg (đóng gói tại PT Merck Sharp Dohme Pharma Tbk. Đại chỉ: JI. Raya Pandaan Km 48, Pandaan, Pasuruan, Jawwa Timur, Indonesia)

### gen_high_risk_0023

- Question: Tôi bị suy gan có dùng Cozaar 50mg (đóng gói tại PT Merck Sharp Dohme Pharma Tbk. Đại chỉ: JI. Raya Pandaan Km 48, Pandaan, Pasuruan, Jawwa Timur, Indonesia) được không?
- Category: high_risk_context
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Cozaar 50mg (đóng gói tại PT Merck Sharp Dohme Pharma Tbk. Đại chỉ: JI. Raya Pandaan Km 48, Pandaan, Pasuruan, Jawwa Timur, Indonesia)

### gen_high_risk_0024

- Question: Tôi bị suy thận có uống Cozaar 50mg (đóng gói tại PT Merck Sharp Dohme Pharma Tbk. Đại chỉ: JI. Raya Pandaan Km 48, Pandaan, Pasuruan, Jawwa Timur, Indonesia) được không?
- Category: high_risk_context
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Cozaar 50mg (đóng gói tại PT Merck Sharp Dohme Pharma Tbk. Đại chỉ: JI. Raya Pandaan Km 48, Pandaan, Pasuruan, Jawwa Timur, Indonesia)

### gen_high_risk_0025

- Question: Tôi đang cho con bú dùng Cozaar 50mg (đóng gói tại PT Merck Sharp Dohme Pharma Tbk. Đại chỉ: JI. Raya Pandaan Km 48, Pandaan, Pasuruan, Jawwa Timur, Indonesia) có an toàn không?
- Category: high_risk_context
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Cozaar 50mg (đóng gói tại PT Merck Sharp Dohme Pharma Tbk. Đại chỉ: JI. Raya Pandaan Km 48, Pandaan, Pasuruan, Jawwa Timur, Indonesia)

### gen_high_risk_0026

- Question: Tôi đang mang thai có dùng Terizidon được không?
- Category: high_risk_context
- Hit@K: False | Strict Hit@K: False
- First relevant rank: None
- First strict rank: None
- Top result: `dav_pdf_ocr` / `drug_info` / `unverified_ocr` / Levonorgestrel 
1,5 mg

### gen_high_risk_0027

- Question: Trẻ em dùng Terizidon được không?
- Category: high_risk_context
- Hit@K: False | Strict Hit@K: False
- First relevant rank: None
- First strict rank: None
- Top result: `dav_pdf_ocr` / `dosage` / `unverified_ocr` / Loratadin 10mg Kingphar

### gen_high_risk_0028

- Question: Tôi bị suy gan có dùng Terizidon được không?
- Category: high_risk_context
- Hit@K: False | Strict Hit@K: False
- First relevant rank: None
- First strict rank: None
- Top result: `dav_pdf_ocr` / `drug_info` / `unverified_ocr` / Effer phazandol cafein 65

### gen_high_risk_0029

- Question: Tôi bị suy thận có uống Terizidon được không?
- Category: high_risk_context
- Hit@K: False | Strict Hit@K: False
- First relevant rank: None
- First strict rank: None
- Top result: `dav_pdf_ocr` / `dosage` / `unverified_ocr` / Effer phazandol cafein 65

### gen_high_risk_0030

- Question: Tôi đang cho con bú dùng Terizidon có an toàn không?
- Category: high_risk_context
- Hit@K: False | Strict Hit@K: False
- First relevant rank: None
- First strict rank: None
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / Sử dụng metronidazol ở phụ nữ cho con bú

### gen_high_risk_0031

- Question: Tôi đang mang thai có dùng Cốm Calci được không?
- Category: high_risk_context
- Hit@K: False | Strict Hit@K: False
- First relevant rank: None
- First strict rank: None
- Top result: `dav_pdf_ocr` / `drug_info` / `unverified_ocr` / Levonorgestrel 
1,5 mg

### gen_high_risk_0032

- Question: Trẻ em dùng Cốm Calci được không?
- Category: high_risk_context
- Hit@K: False | Strict Hit@K: False
- First relevant rank: None
- First strict rank: None
- Top result: `dav_all` / `drug_info` / `official_registry` / Cốm bổ trẻ em

### gen_high_risk_0033

- Question: Tôi bị suy gan có dùng Cốm Calci được không?
- Category: high_risk_context
- Hit@K: False | Strict Hit@K: False
- First relevant rank: None
- First strict rank: None
- Top result: `dav_pdf_ocr` / `drug_info` / `unverified_ocr` / Effer phazandol cafein 65

### gen_high_risk_0034

- Question: Tôi bị suy thận có uống Cốm Calci được không?
- Category: high_risk_context
- Hit@K: False | Strict Hit@K: False
- First relevant rank: None
- First strict rank: None
- Top result: `dav_pdf_ocr` / `dosage` / `unverified_ocr` / Effer phazandol cafein 65

### gen_high_risk_0035

- Question: Tôi đang cho con bú dùng Cốm Calci có an toàn không?
- Category: high_risk_context
- Hit@K: False | Strict Hit@K: False
- First relevant rank: None
- First strict rank: None
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / Sử dụng metronidazol ở phụ nữ cho con bú

### gen_high_risk_0036

- Question: Tôi đang mang thai có dùng Vaco Allerf PE được không?
- Category: high_risk_context
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 3
- Top result: `dav_all` / `drug_info` / `official_registry` / Vaco allerf PE

### gen_high_risk_0037

- Question: Trẻ em dùng Vaco Allerf PE được không?
- Category: high_risk_context
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 2
- Top result: `dav_all` / `drug_info` / `official_registry` / Vaco allerf PE

### gen_high_risk_0038

- Question: Tôi bị suy gan có dùng Vaco Allerf PE được không?
- Category: high_risk_context
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 3
- Top result: `dav_all` / `drug_info` / `official_registry` / Vaco allerf PE

### gen_high_risk_0039

- Question: Tôi bị suy thận có uống Vaco Allerf PE được không?
- Category: high_risk_context
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 3
- Top result: `dav_all` / `drug_info` / `official_registry` / Vaco allerf PE

### gen_high_risk_0040

- Question: Tôi đang cho con bú dùng Vaco Allerf PE có an toàn không?
- Category: high_risk_context
- Hit@K: True | Strict Hit@K: False
- First relevant rank: 1
- First strict rank: None
- Top result: `dav_all` / `drug_info` / `official_registry` / Vaco allerf PE

### gen_high_risk_0041

- Question: Tôi đang mang thai có dùng Giải cảm Nhất Nhất được không?
- Category: high_risk_context
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Giải cảm Nhất Nhất

### gen_high_risk_0042

- Question: Trẻ em dùng Giải cảm Nhất Nhất được không?
- Category: high_risk_context
- Hit@K: False | Strict Hit@K: False
- First relevant rank: None
- First strict rank: None
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / TGA: Chống chỉ định promethazin hydroclorid đường uống cho trẻ em dưới 6 tuổi

### gen_high_risk_0043

- Question: Tôi bị suy gan có dùng Giải cảm Nhất Nhất được không?
- Category: high_risk_context
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 5
- First strict rank: 5
- Top result: `dav_pdf_ocr` / `dosage` / `unverified_ocr` / Effer phazandol cafein 65

### gen_high_risk_0044

- Question: Tôi bị suy thận có uống Giải cảm Nhất Nhất được không?
- Category: high_risk_context
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 2
- First strict rank: 2
- Top result: `dav_pdf_ocr` / `dosage` / `unverified_ocr` / Effer phazandol cafein 65

### gen_high_risk_0045

- Question: Tôi đang cho con bú dùng Giải cảm Nhất Nhất có an toàn không?
- Category: high_risk_context
- Hit@K: False | Strict Hit@K: False
- First relevant rank: None
- First strict rank: None
- Top result: `dav_pdf_ocr` / `safety` / `unverified_ocr` / DH-Pacegan 500

### gen_high_risk_0046

- Question: Tôi đang mang thai có dùng Vitamin B6 được không?
- Category: high_risk_context
- Hit@K: True | Strict Hit@K: False
- First relevant rank: 1
- First strict rank: None
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / FDA: Cảnh báo nguy cơ co giật liên quan thiếu hụt vitamin B6 khi sử dụng các chế phẩm thuốc chứa carbidopa/ levodopa

### gen_high_risk_0047

- Question: Trẻ em dùng Vitamin B6 được không?
- Category: high_risk_context
- Hit@K: True | Strict Hit@K: False
- First relevant rank: 1
- First strict rank: None
- Top result: `dav_all` / `drug_info` / `official_registry` / Cốm bổ trẻ em

### gen_high_risk_0048

- Question: Tôi bị suy gan có dùng Vitamin B6 được không?
- Category: high_risk_context
- Hit@K: True | Strict Hit@K: False
- First relevant rank: 4
- First strict rank: None
- Top result: `dav_pdf_ocr` / `drug_info` / `unverified_ocr` / Effer phazandol cafein 65

### gen_high_risk_0049

- Question: Tôi bị suy thận có uống Vitamin B6 được không?
- Category: high_risk_context
- Hit@K: True | Strict Hit@K: False
- First relevant rank: 2
- First strict rank: None
- Top result: `dav_pdf_ocr` / `dosage` / `unverified_ocr` / Effer phazandol cafein 65

### gen_high_risk_0050

- Question: Tôi đang cho con bú dùng Vitamin B6 có an toàn không?
- Category: high_risk_context
- Hit@K: False | Strict Hit@K: False
- First relevant rank: None
- First strict rank: None
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / Sử dụng metronidazol ở phụ nữ cho con bú

### gen_high_risk_0051

- Question: Tôi đang mang thai có dùng Smofen được không?
- Category: high_risk_context
- Hit@K: False | Strict Hit@K: False
- First relevant rank: None
- First strict rank: None
- Top result: `dav_pdf_ocr` / `drug_info` / `unverified_ocr` / Levonorgestrel 
1,5 mg

### gen_high_risk_0052

- Question: Trẻ em dùng Smofen được không?
- Category: high_risk_context
- Hit@K: False | Strict Hit@K: False
- First relevant rank: None
- First strict rank: None
- Top result: `dav_pdf_ocr` / `dosage` / `unverified_ocr` / Loratadin 10mg Kingphar

### gen_high_risk_0053

- Question: Tôi bị suy gan có dùng Smofen được không?
- Category: high_risk_context
- Hit@K: False | Strict Hit@K: False
- First relevant rank: None
- First strict rank: None
- Top result: `dav_pdf_ocr` / `drug_info` / `unverified_ocr` / Effer phazandol cafein 65

### gen_high_risk_0054

- Question: Tôi bị suy thận có uống Smofen được không?
- Category: high_risk_context
- Hit@K: False | Strict Hit@K: False
- First relevant rank: None
- First strict rank: None
- Top result: `dav_pdf_ocr` / `dosage` / `unverified_ocr` / Effer phazandol cafein 65

### gen_high_risk_0055

- Question: Tôi đang cho con bú dùng Smofen có an toàn không?
- Category: high_risk_context
- Hit@K: False | Strict Hit@K: False
- First relevant rank: None
- First strict rank: None
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / Sử dụng metronidazol ở phụ nữ cho con bú

### gen_high_risk_0056

- Question: Tôi đang mang thai có dùng Atiferolyte 150 mg được không?
- Category: high_risk_context
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Atiferolyte 150 mg

### gen_high_risk_0057

- Question: Trẻ em dùng Atiferolyte 150 mg được không?
- Category: high_risk_context
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Atiferolyte 150 mg

### gen_high_risk_0058

- Question: Tôi bị suy gan có dùng Atiferolyte 150 mg được không?
- Category: high_risk_context
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 4
- First strict rank: 4
- Top result: `dav_pdf_ocr` / `dosage` / `unverified_ocr` / Novopetie suppo paracetamol 80 mg

### gen_high_risk_0059

- Question: Tôi bị suy thận có uống Atiferolyte 150 mg được không?
- Category: high_risk_context
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Atiferolyte 150 mg

### gen_high_risk_0060

- Question: Tôi đang cho con bú dùng Atiferolyte 150 mg có an toàn không?
- Category: high_risk_context
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 3
- First strict rank: 3
- Top result: `dav_pdf_ocr` / `drug_info` / `unverified_ocr` / Fexofenadin.SP 60

### gen_high_risk_0061

- Question: Tôi đang mang thai có dùng Friburine 40mg được không?
- Category: high_risk_context
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Friburine 40mg

### gen_high_risk_0062

- Question: Trẻ em dùng Friburine 40mg được không?
- Category: high_risk_context
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Friburine 40mg

### gen_high_risk_0063

- Question: Tôi bị suy gan có dùng Friburine 40mg được không?
- Category: high_risk_context
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Friburine 40mg

### gen_high_risk_0064

- Question: Tôi bị suy thận có uống Friburine 40mg được không?
- Category: high_risk_context
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Friburine 40mg

### gen_high_risk_0065

- Question: Tôi đang cho con bú dùng Friburine 40mg có an toàn không?
- Category: high_risk_context
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 5
- First strict rank: 5
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / Sử dụng metronidazol ở phụ nữ cho con bú

### gen_high_risk_0066

- Question: Tôi đang mang thai có dùng TS-One Capsule 25 được không?
- Category: high_risk_context
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 2
- Top result: `dav_all` / `drug_info` / `official_registry` / TS-One capsule 25

### gen_high_risk_0067

- Question: Trẻ em dùng TS-One Capsule 25 được không?
- Category: high_risk_context
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 2
- Top result: `dav_all` / `drug_info` / `official_registry` / TS-One capsule 25

### gen_high_risk_0068

- Question: Tôi bị suy gan có dùng TS-One Capsule 25 được không?
- Category: high_risk_context
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 2
- Top result: `dav_all` / `drug_info` / `official_registry` / TS-One capsule 25

### gen_high_risk_0069

- Question: Tôi bị suy thận có uống TS-One Capsule 25 được không?
- Category: high_risk_context
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 2
- Top result: `dav_all` / `drug_info` / `official_registry` / TS-One capsule 25

### gen_high_risk_0070

- Question: Tôi đang cho con bú dùng TS-One Capsule 25 có an toàn không?
- Category: high_risk_context
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 2
- Top result: `dav_all` / `drug_info` / `official_registry` / TS-One capsule 25

### gen_high_risk_0071

- Question: Tôi đang mang thai có dùng Sulfareptol 960 được không?
- Category: high_risk_context
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Sulfareptol 960

### gen_high_risk_0072

- Question: Trẻ em dùng Sulfareptol 960 được không?
- Category: high_risk_context
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Sulfareptol 960

### gen_high_risk_0073

- Question: Tôi bị suy gan có dùng Sulfareptol 960 được không?
- Category: high_risk_context
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Sulfareptol 960

### gen_high_risk_0074

- Question: Tôi bị suy thận có uống Sulfareptol 960 được không?
- Category: high_risk_context
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Sulfareptol 960

### gen_high_risk_0075

- Question: Tôi đang cho con bú dùng Sulfareptol 960 có an toàn không?
- Category: high_risk_context
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Sulfareptol 960

### gen_high_risk_0076

- Question: Tôi đang mang thai có dùng Taginba được không?
- Category: high_risk_context
- Hit@K: False | Strict Hit@K: False
- First relevant rank: None
- First strict rank: None
- Top result: `dav_pdf_ocr` / `drug_info` / `unverified_ocr` / Levonorgestrel 
1,5 mg

### gen_high_risk_0077

- Question: Trẻ em dùng Taginba được không?
- Category: high_risk_context
- Hit@K: False | Strict Hit@K: False
- First relevant rank: None
- First strict rank: None
- Top result: `dav_pdf_ocr` / `dosage` / `unverified_ocr` / Loratadin 10mg Kingphar

### gen_high_risk_0078

- Question: Tôi bị suy gan có dùng Taginba được không?
- Category: high_risk_context
- Hit@K: False | Strict Hit@K: False
- First relevant rank: None
- First strict rank: None
- Top result: `dav_pdf_ocr` / `drug_info` / `unverified_ocr` / Effer phazandol cafein 65

### gen_high_risk_0079

- Question: Tôi bị suy thận có uống Taginba được không?
- Category: high_risk_context
- Hit@K: False | Strict Hit@K: False
- First relevant rank: None
- First strict rank: None
- Top result: `dav_pdf_ocr` / `dosage` / `unverified_ocr` / Effer phazandol cafein 65

### gen_high_risk_0080

- Question: Tôi đang cho con bú dùng Taginba có an toàn không?
- Category: high_risk_context
- Hit@K: False | Strict Hit@K: False
- First relevant rank: None
- First strict rank: None
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / Sử dụng metronidazol ở phụ nữ cho con bú

### gen_high_risk_0081

- Question: Tôi đang mang thai có dùng Glimepirid được không?
- Category: high_risk_context
- Hit@K: False | Strict Hit@K: False
- First relevant rank: None
- First strict rank: None
- Top result: `dav_pdf_ocr` / `drug_info` / `unverified_ocr` / Levonorgestrel 
1,5 mg

### gen_high_risk_0082

- Question: Trẻ em dùng Glimepirid được không?
- Category: high_risk_context
- Hit@K: False | Strict Hit@K: False
- First relevant rank: None
- First strict rank: None
- Top result: `dav_pdf_ocr` / `dosage` / `unverified_ocr` / Loratadin 10mg Kingphar

### gen_high_risk_0083

- Question: Tôi bị suy gan có dùng Glimepirid được không?
- Category: high_risk_context
- Hit@K: False | Strict Hit@K: False
- First relevant rank: None
- First strict rank: None
- Top result: `dav_pdf_ocr` / `drug_info` / `unverified_ocr` / Effer phazandol cafein 65

### gen_high_risk_0084

- Question: Tôi bị suy thận có uống Glimepirid được không?
- Category: high_risk_context
- Hit@K: False | Strict Hit@K: False
- First relevant rank: None
- First strict rank: None
- Top result: `dav_pdf_ocr` / `dosage` / `unverified_ocr` / Effer phazandol cafein 65

### gen_high_risk_0085

- Question: Tôi đang cho con bú dùng Glimepirid có an toàn không?
- Category: high_risk_context
- Hit@K: False | Strict Hit@K: False
- First relevant rank: None
- First strict rank: None
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / Sử dụng metronidazol ở phụ nữ cho con bú

### gen_high_risk_0086

- Question: Tôi đang mang thai có dùng Thysedow 5 mg được không?
- Category: high_risk_context
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Thysedow 5 mg

### gen_high_risk_0087

- Question: Trẻ em dùng Thysedow 5 mg được không?
- Category: high_risk_context
- Hit@K: False | Strict Hit@K: False
- First relevant rank: None
- First strict rank: None
- Top result: `dav_pdf_ocr` / `dosage` / `unverified_ocr` / Tahytrin

### gen_high_risk_0088

- Question: Tôi bị suy gan có dùng Thysedow 5 mg được không?
- Category: high_risk_context
- Hit@K: False | Strict Hit@K: False
- First relevant rank: None
- First strict rank: None
- Top result: `dav_pdf_ocr` / `dosage` / `unverified_ocr` / Novopetie suppo paracetamol 80 mg

### gen_high_risk_0089

- Question: Tôi bị suy thận có uống Thysedow 5 mg được không?
- Category: high_risk_context
- Hit@K: False | Strict Hit@K: False
- First relevant rank: None
- First strict rank: None
- Top result: `dav_pdf_ocr` / `dosage` / `unverified_ocr` / Effer phazandol cafein 65

### gen_high_risk_0090

- Question: Tôi đang cho con bú dùng Thysedow 5 mg có an toàn không?
- Category: high_risk_context
- Hit@K: False | Strict Hit@K: False
- First relevant rank: None
- First strict rank: None
- Top result: `dav_pdf_ocr` / `drug_info` / `unverified_ocr` / Effer phazandol cafein 65

### gen_high_risk_0091

- Question: Tôi đang mang thai có dùng Glucoform 850 được không?
- Category: high_risk_context
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Glucoform 850

### gen_high_risk_0092

- Question: Trẻ em dùng Glucoform 850 được không?
- Category: high_risk_context
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Glucoform 850

### gen_high_risk_0093

- Question: Tôi bị suy gan có dùng Glucoform 850 được không?
- Category: high_risk_context
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Glucoform 850

### gen_high_risk_0094

- Question: Tôi bị suy thận có uống Glucoform 850 được không?
- Category: high_risk_context
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Glucoform 850

### gen_high_risk_0095

- Question: Tôi đang cho con bú dùng Glucoform 850 có an toàn không?
- Category: high_risk_context
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Glucoform 850

### gen_high_risk_0096

- Question: Tôi đang mang thai có dùng Donalium- DN được không?
- Category: high_risk_context
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 2
- First strict rank: 2
- Top result: `dav_all` / `drug_info` / `official_registry` / Donalium - DN

### gen_high_risk_0097

- Question: Trẻ em dùng Donalium- DN được không?
- Category: high_risk_context
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 2
- First strict rank: 2
- Top result: `dav_all` / `drug_info` / `official_registry` / Donalium - DN

### gen_high_risk_0098

- Question: Tôi bị suy gan có dùng Donalium- DN được không?
- Category: high_risk_context
- Hit@K: False | Strict Hit@K: False
- First relevant rank: None
- First strict rank: None
- Top result: `dav_pdf_ocr` / `drug_info` / `unverified_ocr` / Effer phazandol cafein 65

### gen_high_risk_0099

- Question: Tôi bị suy thận có uống Donalium- DN được không?
- Category: high_risk_context
- Hit@K: False | Strict Hit@K: False
- First relevant rank: None
- First strict rank: None
- Top result: `dav_all` / `drug_info` / `official_registry` / Donalium - DN

### gen_high_risk_0100

- Question: Tôi đang cho con bú dùng Donalium- DN có an toàn không?
- Category: high_risk_context
- Hit@K: False | Strict Hit@K: False
- First relevant rank: None
- First strict rank: None
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / Sử dụng metronidazol ở phụ nữ cho con bú

### gen_high_risk_0101

- Question: Tôi đang mang thai có dùng Agilosart - H 100/12,5 được không?
- Category: high_risk_context
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Agilosart - H 100/12,5

### gen_high_risk_0102

- Question: Trẻ em dùng Agilosart - H 100/12,5 được không?
- Category: high_risk_context
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Agilosart - H 100/12,5

### gen_high_risk_0103

- Question: Tôi bị suy gan có dùng Agilosart - H 100/12,5 được không?
- Category: high_risk_context
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 2
- First strict rank: 2
- Top result: `dav_pdf_ocr` / `dosage` / `unverified_ocr` / Effer phazandol cafein 65

### gen_high_risk_0104

- Question: Tôi bị suy thận có uống Agilosart - H 100/12,5 được không?
- Category: high_risk_context
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 2
- First strict rank: 2
- Top result: `dav_pdf_ocr` / `dosage` / `unverified_ocr` / Effer phazandol cafein 65

### gen_high_risk_0105

- Question: Tôi đang cho con bú dùng Agilosart - H 100/12,5 có an toàn không?
- Category: high_risk_context
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 4
- First strict rank: 4
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / Sử dụng metronidazol ở phụ nữ cho con bú

### gen_high_risk_0106

- Question: Tôi đang mang thai có dùng Alpodox được không?
- Category: high_risk_context
- Hit@K: False | Strict Hit@K: False
- First relevant rank: None
- First strict rank: None
- Top result: `dav_pdf_ocr` / `drug_info` / `unverified_ocr` / Levonorgestrel 
1,5 mg

### gen_high_risk_0107

- Question: Trẻ em dùng Alpodox được không?
- Category: high_risk_context
- Hit@K: False | Strict Hit@K: False
- First relevant rank: None
- First strict rank: None
- Top result: `dav_pdf_ocr` / `dosage` / `unverified_ocr` / Loratadin 10mg Kingphar

### gen_high_risk_0108

- Question: Tôi bị suy gan có dùng Alpodox được không?
- Category: high_risk_context
- Hit@K: False | Strict Hit@K: False
- First relevant rank: None
- First strict rank: None
- Top result: `dav_pdf_ocr` / `drug_info` / `unverified_ocr` / Effer phazandol cafein 65

### gen_high_risk_0109

- Question: Tôi bị suy thận có uống Alpodox được không?
- Category: high_risk_context
- Hit@K: False | Strict Hit@K: False
- First relevant rank: None
- First strict rank: None
- Top result: `dav_pdf_ocr` / `dosage` / `unverified_ocr` / Effer phazandol cafein 65

### gen_high_risk_0110

- Question: Tôi đang cho con bú dùng Alpodox có an toàn không?
- Category: high_risk_context
- Hit@K: False | Strict Hit@K: False
- First relevant rank: None
- First strict rank: None
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / Sử dụng metronidazol ở phụ nữ cho con bú

### gen_high_risk_0111

- Question: Tôi đang mang thai có dùng Lycoplan 200mg được không?
- Category: high_risk_context
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Lycoplan 200mg

### gen_high_risk_0112

- Question: Trẻ em dùng Lycoplan 200mg được không?
- Category: high_risk_context
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Lycoplan 200mg

### gen_high_risk_0113

- Question: Tôi bị suy gan có dùng Lycoplan 200mg được không?
- Category: high_risk_context
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 4
- First strict rank: 4
- Top result: `dav_pdf_ocr` / `drug_info` / `unverified_ocr` / Effer phazandol cafein 65

### gen_high_risk_0114

- Question: Tôi bị suy thận có uống Lycoplan 200mg được không?
- Category: high_risk_context
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 3
- First strict rank: 3
- Top result: `dav_pdf_ocr` / `dosage` / `unverified_ocr` / Effer phazandol cafein 65

### gen_high_risk_0115

- Question: Tôi đang cho con bú dùng Lycoplan 200mg có an toàn không?
- Category: high_risk_context
- Hit@K: False | Strict Hit@K: False
- First relevant rank: None
- First strict rank: None
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / Sử dụng metronidazol ở phụ nữ cho con bú

### gen_high_risk_0116

- Question: Tôi đang mang thai có dùng Dentgital được không?
- Category: high_risk_context
- Hit@K: False | Strict Hit@K: False
- First relevant rank: None
- First strict rank: None
- Top result: `dav_pdf_ocr` / `drug_info` / `unverified_ocr` / Levonorgestrel 
1,5 mg

### gen_high_risk_0117

- Question: Trẻ em dùng Dentgital được không?
- Category: high_risk_context
- Hit@K: False | Strict Hit@K: False
- First relevant rank: None
- First strict rank: None
- Top result: `dav_pdf_ocr` / `dosage` / `unverified_ocr` / Loratadin 10mg Kingphar

### gen_high_risk_0118

- Question: Tôi bị suy gan có dùng Dentgital được không?
- Category: high_risk_context
- Hit@K: False | Strict Hit@K: False
- First relevant rank: None
- First strict rank: None
- Top result: `dav_pdf_ocr` / `drug_info` / `unverified_ocr` / Effer phazandol cafein 65

### gen_high_risk_0119

- Question: Tôi bị suy thận có uống Dentgital được không?
- Category: high_risk_context
- Hit@K: False | Strict Hit@K: False
- First relevant rank: None
- First strict rank: None
- Top result: `dav_pdf_ocr` / `dosage` / `unverified_ocr` / Effer phazandol cafein 65

### gen_high_risk_0120

- Question: Tôi đang cho con bú dùng Dentgital có an toàn không?
- Category: high_risk_context
- Hit@K: False | Strict Hit@K: False
- First relevant rank: None
- First strict rank: None
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / Sử dụng metronidazol ở phụ nữ cho con bú

### gen_high_risk_0121

- Question: Tôi đang mang thai có dùng Xalexa 30 được không?
- Category: high_risk_context
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Xalexa 30

### gen_high_risk_0122

- Question: Trẻ em dùng Xalexa 30 được không?
- Category: high_risk_context
- Hit@K: False | Strict Hit@K: False
- First relevant rank: None
- First strict rank: None
- Top result: `dav_pdf_ocr` / `drug_info` / `unverified_ocr` / Loratadin

### gen_high_risk_0123

- Question: Tôi bị suy gan có dùng Xalexa 30 được không?
- Category: high_risk_context
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 5
- First strict rank: 5
- Top result: `dav_pdf_ocr` / `drug_info` / `unverified_ocr` / Effer phazandol cafein 65

### gen_high_risk_0124

- Question: Tôi bị suy thận có uống Xalexa 30 được không?
- Category: high_risk_context
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 3
- First strict rank: 3
- Top result: `dav_pdf_ocr` / `dosage` / `unverified_ocr` / Effer phazandol cafein 65

### gen_high_risk_0125

- Question: Tôi đang cho con bú dùng Xalexa 30 có an toàn không?
- Category: high_risk_context
- Hit@K: False | Strict Hit@K: False
- First relevant rank: None
- First strict rank: None
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / Sử dụng metronidazol ở phụ nữ cho con bú

### gen_high_risk_0126

- Question: Tôi đang mang thai có dùng Medotor - 10 được không?
- Category: high_risk_context
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 3
- First strict rank: 3
- Top result: `dav_pdf` / `drug_info` / `official_registry` / Shinmus

### gen_high_risk_0127

- Question: Trẻ em dùng Medotor - 10 được không?
- Category: high_risk_context
- Hit@K: False | Strict Hit@K: False
- First relevant rank: None
- First strict rank: None
- Top result: `dav_pdf_ocr` / `dosage` / `unverified_ocr` / Loratadin 10mg Kingphar

### gen_high_risk_0128

- Question: Tôi bị suy gan có dùng Medotor - 10 được không?
- Category: high_risk_context
- Hit@K: False | Strict Hit@K: False
- First relevant rank: None
- First strict rank: None
- Top result: `dav_pdf_ocr` / `drug_info` / `unverified_ocr` / Effer phazandol cafein 65

### gen_high_risk_0129

- Question: Tôi bị suy thận có uống Medotor - 10 được không?
- Category: high_risk_context
- Hit@K: False | Strict Hit@K: False
- First relevant rank: None
- First strict rank: None
- Top result: `dav_pdf_ocr` / `dosage` / `unverified_ocr` / Effer phazandol cafein 65

### gen_high_risk_0130

- Question: Tôi đang cho con bú dùng Medotor - 10 có an toàn không?
- Category: high_risk_context
- Hit@K: False | Strict Hit@K: False
- First relevant rank: None
- First strict rank: None
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / Sử dụng metronidazol ở phụ nữ cho con bú

### gen_high_risk_0131

- Question: Tôi đang mang thai có dùng Pletimizol được không?
- Category: high_risk_context
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 3
- First strict rank: 3
- Top result: `dav_pdf_ocr` / `drug_info` / `unverified_ocr` / Levonorgestrel 
1,5 mg

### gen_high_risk_0132

- Question: Trẻ em dùng Pletimizol được không?
- Category: high_risk_context
- Hit@K: False | Strict Hit@K: False
- First relevant rank: None
- First strict rank: None
- Top result: `dav_pdf_ocr` / `dosage` / `unverified_ocr` / Loratadin 10mg Kingphar

### gen_high_risk_0133

- Question: Tôi bị suy gan có dùng Pletimizol được không?
- Category: high_risk_context
- Hit@K: False | Strict Hit@K: False
- First relevant rank: None
- First strict rank: None
- Top result: `dav_pdf_ocr` / `drug_info` / `unverified_ocr` / Effer phazandol cafein 65

### gen_high_risk_0134

- Question: Tôi bị suy thận có uống Pletimizol được không?
- Category: high_risk_context
- Hit@K: False | Strict Hit@K: False
- First relevant rank: None
- First strict rank: None
- Top result: `dav_pdf_ocr` / `dosage` / `unverified_ocr` / Effer phazandol cafein 65

### gen_high_risk_0135

- Question: Tôi đang cho con bú dùng Pletimizol có an toàn không?
- Category: high_risk_context
- Hit@K: False | Strict Hit@K: False
- First relevant rank: None
- First strict rank: None
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / Sử dụng metronidazol ở phụ nữ cho con bú

### gen_high_risk_0136

- Question: Tôi đang mang thai có dùng Atigluco 500 được không?
- Category: high_risk_context
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 2
- First strict rank: 2
- Top result: `dav_pdf_ocr` / `dosage` / `unverified_ocr` / DH-Pacegan 500

### gen_high_risk_0137

- Question: Trẻ em dùng Atigluco 500 được không?
- Category: high_risk_context
- Hit@K: False | Strict Hit@K: False
- First relevant rank: None
- First strict rank: None
- Top result: `dav_pdf` / `drug_info` / `official_registry` / Shinmus

### gen_high_risk_0138

- Question: Tôi bị suy gan có dùng Atigluco 500 được không?
- Category: high_risk_context
- Hit@K: False | Strict Hit@K: False
- First relevant rank: None
- First strict rank: None
- Top result: `dav_pdf_ocr` / `drug_info` / `unverified_ocr` / Effer phazandol cafein 65

### gen_high_risk_0139

- Question: Tôi bị suy thận có uống Atigluco 500 được không?
- Category: high_risk_context
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 5
- First strict rank: 5
- Top result: `dav_pdf_ocr` / `dosage` / `unverified_ocr` / Effer phazandol cafein 65

### gen_high_risk_0140

- Question: Tôi đang cho con bú dùng Atigluco 500 có an toàn không?
- Category: high_risk_context
- Hit@K: False | Strict Hit@K: False
- First relevant rank: None
- First strict rank: None
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / Sử dụng metronidazol ở phụ nữ cho con bú

### gen_high_risk_0141

- Question: Tôi đang mang thai có dùng SaViPamol 650 được không?
- Category: high_risk_context
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / SaViPamol 650

### gen_high_risk_0142

- Question: Trẻ em dùng SaViPamol 650 được không?
- Category: high_risk_context
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / SaViPamol 650

### gen_high_risk_0143

- Question: Tôi bị suy gan có dùng SaViPamol 650 được không?
- Category: high_risk_context
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / SaViPamol 650

### gen_high_risk_0144

- Question: Tôi bị suy thận có uống SaViPamol 650 được không?
- Category: high_risk_context
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / SaViPamol 650

### gen_interaction_0001

- Question: Tôi uống AstaPadol 500 mg cùng Levical soft được không?
- Category: interaction
- Hit@K: True | Strict Hit@K: False
- First relevant rank: 2
- First strict rank: None
- Top result: `dav_all` / `drug_info` / `official_registry` / AstaPadol Caps 500 mg

### gen_interaction_0002

- Question: Tôi uống Cyclolife cùng Midatoren 160/25 được không?
- Category: interaction
- Hit@K: True | Strict Hit@K: False
- First relevant rank: 1
- First strict rank: None
- Top result: `dav_all` / `drug_info` / `official_registry` / Midatoren 160/25

### gen_interaction_0003

- Question: Tôi uống Cozaar 50mg (đóng gói tại PT Merck Sharp Dohme Pharma Tbk. Đại chỉ: JI. Raya Pandaan Km 48, Pandaan, Pasuruan, Jawwa Timur, Indonesia) cùng Terizidon được không?
- Category: interaction
- Hit@K: True | Strict Hit@K: False
- First relevant rank: 1
- First strict rank: None
- Top result: `dav_all` / `drug_info` / `official_registry` / Cozaar 50mg (đóng gói tại PT Merck Sharp Dohme Pharma Tbk. Đại chỉ: JI. Raya Pandaan Km 48, Pandaan, Pasuruan, Jawwa Timur, Indonesia)

### gen_interaction_0004

- Question: Tôi uống Cốm Calci cùng Vaco Allerf PE được không?
- Category: interaction
- Hit@K: True | Strict Hit@K: False
- First relevant rank: 1
- First strict rank: None
- Top result: `dav_all` / `drug_info` / `official_registry` / Vaco allerf PE

### gen_interaction_0005

- Question: Tôi uống Giải cảm Nhất Nhất cùng Vitamin B6 được không?
- Category: interaction
- Hit@K: True | Strict Hit@K: False
- First relevant rank: 1
- First strict rank: None
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / TGA: Cập nhật quy định mới nhằm giảm thiểu nguy cơ bệnh lý thần kinh ngoại biên khi sử dụng vitamin B6

### gen_interaction_0006

- Question: Tôi uống Smofen cùng Atiferolyte 150 mg được không?
- Category: interaction
- Hit@K: True | Strict Hit@K: False
- First relevant rank: 1
- First strict rank: None
- Top result: `dav_all` / `drug_info` / `official_registry` / Atiferolyte 150 mg

### gen_interaction_0007

- Question: Tôi uống Friburine 40mg cùng TS-One Capsule 25 được không?
- Category: interaction
- Hit@K: True | Strict Hit@K: False
- First relevant rank: 1
- First strict rank: None
- Top result: `dav_all` / `drug_info` / `official_registry` / TS-One capsule 25

### gen_interaction_0008

- Question: Tôi uống Sulfareptol 960 cùng Taginba được không?
- Category: interaction
- Hit@K: True | Strict Hit@K: False
- First relevant rank: 1
- First strict rank: None
- Top result: `dav_all` / `drug_info` / `official_registry` / Sulfareptol 960

### gen_interaction_0009

- Question: Tôi uống Glimepirid cùng Thysedow 5 mg được không?
- Category: interaction
- Hit@K: True | Strict Hit@K: False
- First relevant rank: 2
- First strict rank: None
- Top result: `dav_pdf_ocr` / `safety` / `unverified_ocr` / Fexosin 30

### gen_interaction_0010

- Question: Tôi uống Glucoform 850 cùng Donalium- DN được không?
- Category: interaction
- Hit@K: True | Strict Hit@K: False
- First relevant rank: 1
- First strict rank: None
- Top result: `dav_all` / `drug_info` / `official_registry` / Glucoform 850

### gen_interaction_0011

- Question: Tôi uống Agilosart - H 100/12,5 cùng Alpodox được không?
- Category: interaction
- Hit@K: True | Strict Hit@K: False
- First relevant rank: 1
- First strict rank: None
- Top result: `dav_all` / `drug_info` / `official_registry` / Agilosart - H 100/12,5

### gen_interaction_0012

- Question: Tôi uống Lycoplan 200mg cùng Dentgital được không?
- Category: interaction
- Hit@K: True | Strict Hit@K: False
- First relevant rank: 1
- First strict rank: None
- Top result: `dav_all` / `drug_info` / `official_registry` / Lycoplan 200mg

### gen_interaction_0013

- Question: Tôi uống Xalexa 30 cùng Medotor - 10 được không?
- Category: interaction
- Hit@K: True | Strict Hit@K: False
- First relevant rank: 1
- First strict rank: None
- Top result: `dav_all` / `drug_info` / `official_registry` / Xalexa 30

### gen_interaction_0014

- Question: Tôi uống Pletimizol cùng Atigluco 500 được không?
- Category: interaction
- Hit@K: True | Strict Hit@K: False
- First relevant rank: 1
- First strict rank: None
- Top result: `dav_all` / `drug_info` / `official_registry` / Atigluco 500

### gen_interaction_0015

- Question: Tôi uống SaViPamol 650 cùng Azzol-S 150 mg/cap được không?
- Category: interaction
- Hit@K: True | Strict Hit@K: False
- First relevant rank: 1
- First strict rank: None
- Top result: `dav_all` / `drug_info` / `official_registry` / Azzol-S 150 mg/cap

### gen_interaction_0016

- Question: Tôi uống Atromux 10 cùng Human Albumin Takeda 250g/l được không?
- Category: interaction
- Hit@K: True | Strict Hit@K: False
- First relevant rank: 1
- First strict rank: None
- Top result: `dav_all` / `drug_info` / `official_registry` / Human Albumin Takeda 250g/l

### gen_interaction_0017

- Question: Tôi uống VacoCipdex 0,3% cùng Vifamox 250 được không?
- Category: interaction
- Hit@K: True | Strict Hit@K: False
- First relevant rank: 1
- First strict rank: None
- Top result: `dav_all` / `drug_info` / `official_registry` / Vifamox 250

### gen_interaction_0018

- Question: Tôi uống Calcicar 500 Tablet cùng Sanfetil 200 được không?
- Category: interaction
- Hit@K: True | Strict Hit@K: False
- First relevant rank: 1
- First strict rank: None
- Top result: `dav_all` / `drug_info` / `official_registry` / Calcicar 500 Tablet

### gen_interaction_0019

- Question: Tôi uống Triamvirgri cùng Vorifend Forte được không?
- Category: interaction
- Hit@K: True | Strict Hit@K: False
- First relevant rank: 1
- First strict rank: None
- Top result: `dav_all` / `drug_info` / `official_registry` / Vorifend Forte

### gen_interaction_0020

- Question: Tôi uống Azaretin - H Cream cùng Heralopres H 25 được không?
- Category: interaction
- Hit@K: True | Strict Hit@K: False
- First relevant rank: 1
- First strict rank: None
- Top result: `dav_all` / `drug_info` / `official_registry` / Heralopres H 25

### gen_interaction_0021

- Question: Tôi uống Podus cùng Gabahasan 300 được không?
- Category: interaction
- Hit@K: True | Strict Hit@K: False
- First relevant rank: 1
- First strict rank: None
- Top result: `dav_all` / `drug_info` / `official_registry` / Gabahasan 300

### gen_interaction_0022

- Question: Tôi uống Calcitron cùng Acarbose DWP 25 mg được không?
- Category: interaction
- Hit@K: True | Strict Hit@K: False
- First relevant rank: 1
- First strict rank: None
- Top result: `dav_all` / `drug_info` / `official_registry` / Acarbose DWP 25 mg

### gen_interaction_0023

- Question: Tôi uống Pemetrexed Biovagen cùng Lorabipha Tab. được không?
- Category: interaction
- Hit@K: True | Strict Hit@K: False
- First relevant rank: 1
- First strict rank: None
- Top result: `dav_all` / `drug_info` / `official_registry` / Pemetrexed Biovagen

### gen_interaction_0024

- Question: Tôi uống Kupfolin cùng Fizoti Inj. được không?
- Category: interaction
- Hit@K: True | Strict Hit@K: False
- First relevant rank: 3
- First strict rank: None
- Top result: `dav_all` / `drug_info` / `official_registry` / Fizoti Inj

### gen_interaction_0025

- Question: Tôi uống Hadusim 20 cùng Degas được không?
- Category: interaction
- Hit@K: True | Strict Hit@K: False
- First relevant rank: 1
- First strict rank: None
- Top result: `dav_all` / `drug_info` / `official_registry` / Hadusim 20

### gen_interaction_0026

- Question: Tôi uống Ampicilin 500 mg cùng Nhuận gan lợi mật được không?
- Category: interaction
- Hit@K: True | Strict Hit@K: False
- First relevant rank: 1
- First strict rank: None
- Top result: `dav_all` / `drug_info` / `official_registry` / Nhuận gan lợi mật

### gen_interaction_0027

- Question: Tôi uống Thuốc tiêm Metronidazole cùng Avastin được không?
- Category: interaction
- Hit@K: False | Strict Hit@K: False
- First relevant rank: None
- First strict rank: None
- Top result: `dav_pdf_ocr` / `safety` / `unverified_ocr` / Fexosin 30

### gen_interaction_0028

- Question: Tôi uống Nefitaz cùng Imemoti tab được không?
- Category: interaction
- Hit@K: True | Strict Hit@K: False
- First relevant rank: 1
- First strict rank: None
- Top result: `dav_all` / `drug_info` / `official_registry` / Imemoti tab

### gen_interaction_0029

- Question: Tôi uống Danaroxime 1500mg cùng Uratonyl được không?
- Category: interaction
- Hit@K: True | Strict Hit@K: False
- First relevant rank: 1
- First strict rank: None
- Top result: `dav_all` / `drug_info` / `official_registry` / Danaroxime 1500mg

### gen_interaction_0030

- Question: Tôi uống Odistad 120 cùng Telfor được không?
- Category: interaction
- Hit@K: True | Strict Hit@K: False
- First relevant rank: 1
- First strict rank: None
- Top result: `dav_all` / `drug_info` / `official_registry` / Telfor 120

### gen_interaction_0031

- Question: Tôi uống Darunavir Tablets 600mg cùng Harnal Ocas 0,4mg được không?
- Category: interaction
- Hit@K: True | Strict Hit@K: False
- First relevant rank: 1
- First strict rank: None
- Top result: `dav_all` / `drug_info` / `official_registry` / Harnal Ocas 0,4mg

### gen_interaction_0032

- Question: Tôi uống Coolzz trẻ em cùng Amoxybiotic 500 được không?
- Category: interaction
- Hit@K: True | Strict Hit@K: False
- First relevant rank: 1
- First strict rank: None
- Top result: `dav_all` / `drug_info` / `official_registry` / Coolzz trẻ em

### gen_interaction_0033

- Question: Tôi uống Ribazole cùng Paluzine được không?
- Category: interaction
- Hit@K: True | Strict Hit@K: False
- First relevant rank: 2
- First strict rank: None
- Top result: `dav_pdf_ocr` / `safety` / `unverified_ocr` / Fexosin 30

### gen_interaction_0034

- Question: Tôi uống Carbocistein 100mg cùng Rohto Hydra R được không?
- Category: interaction
- Hit@K: True | Strict Hit@K: False
- First relevant rank: 1
- First strict rank: None
- Top result: `dav_all` / `drug_info` / `official_registry` / Rohto Hydra R

### gen_interaction_0035

- Question: Tôi uống Cosaraz cùng SPEEDA được không?
- Category: interaction
- Hit@K: True | Strict Hit@K: False
- First relevant rank: 3
- First strict rank: None
- Top result: `dav_pdf_ocr` / `safety` / `unverified_ocr` / Fexosin 30

### gen_interaction_0036

- Question: Tôi uống Ibufen D Oral Suspension cùng Simterol được không?
- Category: interaction
- Hit@K: True | Strict Hit@K: False
- First relevant rank: 1
- First strict rank: None
- Top result: `dav_all` / `drug_info` / `official_registry` / Ibufen D Oral Suspension

### gen_interaction_0037

- Question: Tôi uống Gentizone cùng Livethine Powder 3g được không?
- Category: interaction
- Hit@K: True | Strict Hit@K: False
- First relevant rank: 1
- First strict rank: None
- Top result: `dav_all` / `drug_info` / `official_registry` / Livethine Powder 3g

### gen_interaction_0038

- Question: Tôi uống Daygra 25 cùng Lobitzo được không?
- Category: interaction
- Hit@K: True | Strict Hit@K: False
- First relevant rank: 1
- First strict rank: None
- Top result: `dav_all` / `drug_info` / `official_registry` / Daygra 25

### gen_interaction_0039

- Question: Tôi uống Dopili 15 mg cùng Anigrine được không?
- Category: interaction
- Hit@K: True | Strict Hit@K: False
- First relevant rank: 1
- First strict rank: None
- Top result: `dav_all` / `drug_info` / `official_registry` / Dopili 15 mg

### gen_interaction_0040

- Question: Tôi uống Budolfen cùng Pitavas 4 được không?
- Category: interaction
- Hit@K: True | Strict Hit@K: False
- First relevant rank: 3
- First strict rank: None
- Top result: `dav_pdf_ocr` / `safety` / `unverified_ocr` / Fexosin 30

### gen_interaction_0041

- Question: Tôi uống Sosvomit 4 ODT cùng Linkotax 25mg được không?
- Category: interaction
- Hit@K: True | Strict Hit@K: False
- First relevant rank: 1
- First strict rank: None
- Top result: `dav_all` / `drug_info` / `official_registry` / Linkotax 25mg

### gen_interaction_0042

- Question: Tôi uống Miglocaln 15 cùng Nebstyle 5 được không?
- Category: interaction
- Hit@K: True | Strict Hit@K: False
- First relevant rank: 1
- First strict rank: None
- Top result: `dav_all` / `drug_info` / `official_registry` / Miglocaln 15

### gen_interaction_0043

- Question: Tôi uống Vadol Caps cùng Eptifiba Injection Angigo được không?
- Category: interaction
- Hit@K: True | Strict Hit@K: False
- First relevant rank: 1
- First strict rank: None
- Top result: `dav_all` / `drug_info` / `official_registry` / Eptifiba Injection Angigo

### gen_interaction_0044

- Question: Tôi uống Insulidd 30:70 cùng Apixa 5 được không?
- Category: interaction
- Hit@K: True | Strict Hit@K: False
- First relevant rank: 1
- First strict rank: None
- Top result: `dav_all` / `drug_info` / `official_registry` / Insulidd 30:70

### gen_interaction_0045

- Question: Tôi uống Irzinex 150 cùng ZinC - Kid được không?
- Category: interaction
- Hit@K: True | Strict Hit@K: False
- First relevant rank: 1
- First strict rank: None
- Top result: `dav_all` / `drug_info` / `official_registry` / Irzinex 150

### gen_interaction_0046

- Question: Tôi uống Alpathin cùng Dogracil được không?
- Category: interaction
- Hit@K: True | Strict Hit@K: False
- First relevant rank: 3
- First strict rank: None
- Top result: `dav_pdf_ocr` / `safety` / `unverified_ocr` / Fexosin 30

### gen_interaction_0047

- Question: Tôi uống Multivitamin cùng Stadloric 100 được không?
- Category: interaction
- Hit@K: True | Strict Hit@K: False
- First relevant rank: 1
- First strict rank: None
- Top result: `dav_all` / `drug_info` / `official_registry` / Stadloric 100

### gen_interaction_0048

- Question: Tôi uống Phytobebe cùng Lotusalic được không?
- Category: interaction
- Hit@K: True | Strict Hit@K: False
- First relevant rank: 1
- First strict rank: None
- Top result: `dav_all` / `drug_info` / `official_registry` / Phytobebe

### gen_interaction_0049

- Question: Tôi uống Midaxin 100 cùng SaVi Bromyst được không?
- Category: interaction
- Hit@K: True | Strict Hit@K: False
- First relevant rank: 1
- First strict rank: None
- Top result: `dav_all` / `drug_info` / `official_registry` / Midaxin 100

### gen_interaction_0050

- Question: Tôi uống Cetecocensamin cùng Hương sa lục quân được không?
- Category: interaction
- Hit@K: True | Strict Hit@K: False
- First relevant rank: 1
- First strict rank: None
- Top result: `dav_all` / `drug_info` / `official_registry` / Hương sa lục quân

### gen_interaction_0051

- Question: Tôi uống Lefnus 10 cùng Zecuf Herbal Cough lozenges (Orange flavour) được không?
- Category: interaction
- Hit@K: True | Strict Hit@K: False
- First relevant rank: 1
- First strict rank: None
- Top result: `dav_all` / `drug_info` / `official_registry` / Zecuf Herbal Cough lozenges (Orange flavour)

### gen_interaction_0052

- Question: Tôi uống Runor 10 cùng Quitide 100 được không?
- Category: interaction
- Hit@K: True | Strict Hit@K: False
- First relevant rank: 1
- First strict rank: None
- Top result: `dav_all` / `drug_info` / `official_registry` / Quitide 100

### gen_interaction_0053

- Question: Tôi uống Levemir Flexpen cùng Gelactive được không?
- Category: interaction
- Hit@K: True | Strict Hit@K: False
- First relevant rank: 1
- First strict rank: None
- Top result: `dav_all` / `drug_info` / `official_registry` / Levemir FlexPen

### gen_interaction_0054

- Question: Tôi uống Netlisan cùng Trimebutin được không?
- Category: interaction
- Hit@K: False | Strict Hit@K: False
- First relevant rank: None
- First strict rank: None
- Top result: `dav_pdf_ocr` / `safety` / `unverified_ocr` / Fexosin 30

### gen_interaction_0055

- Question: Tôi uống Thioheal 600 cùng Bestdocel 80 được không?
- Category: interaction
- Hit@K: True | Strict Hit@K: False
- First relevant rank: 1
- First strict rank: None
- Top result: `dav_all` / `drug_info` / `official_registry` / Thioheal 600

### gen_interaction_0056

- Question: Tôi uống Erythromycin 250 cùng Kim Ngân Hoa được không?
- Category: interaction
- Hit@K: True | Strict Hit@K: False
- First relevant rank: 1
- First strict rank: None
- Top result: `dav_all` / `drug_info` / `official_registry` / Erythromycin 250 mg

### gen_interaction_0057

- Question: Tôi uống Hafixim 200 tabs cùng Atidaf 250 được không?
- Category: interaction
- Hit@K: True | Strict Hit@K: False
- First relevant rank: 1
- First strict rank: None
- Top result: `dav_all` / `drug_info` / `official_registry` / Hafixim 200 tabs

### gen_interaction_0058

- Question: Tôi uống Esti-Tenofovir cùng Xynopine tablet 10mg được không?
- Category: interaction
- Hit@K: True | Strict Hit@K: False
- First relevant rank: 1
- First strict rank: None
- Top result: `dav_all` / `drug_info` / `official_registry` / Xynopine tablet 10mg

### gen_interaction_0059

- Question: Tôi uống Tricef 100 cùng Ancorixib 60 được không?
- Category: interaction
- Hit@K: True | Strict Hit@K: False
- First relevant rank: 1
- First strict rank: None
- Top result: `dav_all` / `drug_info` / `official_registry` / Ancorixib 60

### gen_interaction_0060

- Question: Tôi uống Metronidazol cùng Maxinject được không?
- Category: interaction
- Hit@K: False | Strict Hit@K: False
- First relevant rank: None
- First strict rank: None
- Top result: `dav_pdf_ocr` / `safety` / `unverified_ocr` / Fexosin 30

### gen_interaction_0061

- Question: Tôi uống An thần bổ tâm cùng Minderkey ODT Tablet 5mg được không?
- Category: interaction
- Hit@K: True | Strict Hit@K: False
- First relevant rank: 1
- First strict rank: None
- Top result: `dav_all` / `drug_info` / `official_registry` / Minderkey ODT Tablet 5mg

### gen_interaction_0062

- Question: Tôi uống Diasanté cùng Salonsip gel patch (SXNQ của Hisamitsu Nhật Bản) được không?
- Category: interaction
- Hit@K: True | Strict Hit@K: False
- First relevant rank: 1
- First strict rank: None
- Top result: `dav_all` / `drug_info` / `official_registry` / Salonsip gel patch (SXNQ của Hisamitsu Nhật Bản)

### gen_interaction_0063

- Question: Tôi uống Lansomac 30 cùng GETINO-B TABLETS 300mg được không?
- Category: interaction
- Hit@K: True | Strict Hit@K: False
- First relevant rank: 1
- First strict rank: None
- Top result: `dav_all` / `drug_info` / `official_registry` / GETINO-B TABLETS 300mg

### gen_interaction_0064

- Question: Tôi uống Cenpadol 250 cùng Bestdocel 80mg/4ml được không?
- Category: interaction
- Hit@K: True | Strict Hit@K: False
- First relevant rank: 1
- First strict rank: None
- Top result: `dav_all` / `drug_info` / `official_registry` / Bestdocel 80mg/4ml

### gen_interaction_0065

- Question: Tôi uống Rab-ulcer 20mg cùng Carvesyl được không?
- Category: interaction
- Hit@K: True | Strict Hit@K: False
- First relevant rank: 1
- First strict rank: None
- Top result: `dav_all` / `drug_info` / `official_registry` / Rab-ulcer 20mg

### gen_interaction_0066

- Question: Tôi uống Paracetamol 500 mg cùng Auroliza 20 được không?
- Category: interaction
- Hit@K: True | Strict Hit@K: False
- First relevant rank: 1
- First strict rank: None
- Top result: `dav_all` / `drug_info` / `official_registry` / DolAPC 500

### gen_interaction_0067

- Question: Tôi uống Blokheart 15 cùng Pulracef - CV 500 được không?
- Category: interaction
- Hit@K: True | Strict Hit@K: False
- First relevant rank: 1
- First strict rank: None
- Top result: `dav_all` / `drug_info` / `official_registry` / Pulracef - CV 500

### gen_interaction_0068

- Question: Tôi uống Molniplus Cream cùng Trotaxone 1g được không?
- Category: interaction
- Hit@K: True | Strict Hit@K: False
- First relevant rank: 1
- First strict rank: None
- Top result: `dav_all` / `drug_info` / `official_registry` / Trotaxone 1g

### gen_interaction_0069

- Question: Tôi uống Methyldopa 250mg cùng Dopamine Renaudin 40mg/ml được không?
- Category: interaction
- Hit@K: True | Strict Hit@K: False
- First relevant rank: 1
- First strict rank: None
- Top result: `dav_all` / `drug_info` / `official_registry` / Dopamine Renaudin 40mg/ml

### gen_interaction_0070

- Question: Tôi uống Ba kích cùng Glucose 20% được không?
- Category: interaction
- Hit@K: True | Strict Hit@K: False
- First relevant rank: 1
- First strict rank: None
- Top result: `dav_all` / `drug_info` / `official_registry` / Ba kích

### gen_interaction_0071

- Question: Tôi uống Bát trân cùng BV Loratab 10 được không?
- Category: interaction
- Hit@K: True | Strict Hit@K: False
- First relevant rank: 1
- First strict rank: None
- Top result: `dav_all` / `drug_info` / `official_registry` / BV Loratab 10

### gen_interaction_0072

- Question: Tôi uống Calcilinat F100 cùng Neustam 800 được không?
- Category: interaction
- Hit@K: True | Strict Hit@K: False
- First relevant rank: 1
- First strict rank: None
- Top result: `dav_all` / `drug_info` / `official_registry` / Calcilinat F100

### gen_interaction_0073

- Question: Tôi uống Kim tiền thảo vinacare cùng Dixirein được không?
- Category: interaction
- Hit@K: True | Strict Hit@K: False
- First relevant rank: 1
- First strict rank: None
- Top result: `dav_all` / `drug_info` / `official_registry` / Kim tiền thảo Vinacare 250

### gen_interaction_0074

- Question: Tôi uống Measles, Mumps and Rubella Vaccine Live, Attenuated (Freeze-Dried) cùng Hapa được không?
- Category: interaction
- Hit@K: True | Strict Hit@K: False
- First relevant rank: 1
- First strict rank: None
- Top result: `dav_all` / `drug_info` / `official_registry` / Measles, Mumps and Rubella Vaccine Live, Attenuated (Freeze-Dried)

### gen_interaction_0075

- Question: Tôi uống Carbidopa Levodopa 12.5/50 mg Tablets cùng Hetenol được không?
- Category: interaction
- Hit@K: True | Strict Hit@K: False
- First relevant rank: 1
- First strict rank: None
- Top result: `dav_all` / `drug_info` / `official_registry` / Carbidopa Levodopa 12.5/50 mg Tablets

### gen_interaction_0076

- Question: Tôi uống Viên nang cứng Lục vị cùng Atigintong ginseng được không?
- Category: interaction
- Hit@K: True | Strict Hit@K: False
- First relevant rank: 1
- First strict rank: None
- Top result: `dav_all` / `drug_info` / `official_registry` / Atigintong ginseng

### gen_interaction_0077

- Question: Tôi uống Oubapentin 150 cùng Gastro-kite được không?
- Category: interaction
- Hit@K: True | Strict Hit@K: False
- First relevant rank: 1
- First strict rank: None
- Top result: `dav_all` / `drug_info` / `official_registry` / Oubapentin 150

### gen_interaction_0078

- Question: Tôi uống Ohazit cùng Cốm trẻ việt được không?
- Category: interaction
- Hit@K: False | Strict Hit@K: False
- First relevant rank: None
- First strict rank: None
- Top result: `dav_pdf_ocr` / `safety` / `unverified_ocr` / Fexosin 30

### gen_interaction_0079

- Question: Tôi uống Bavui sup 125mg cùng Volden Fort được không?
- Category: interaction
- Hit@K: True | Strict Hit@K: False
- First relevant rank: 1
- First strict rank: None
- Top result: `dav_all` / `drug_info` / `official_registry` / Bavui sup 125mg

### gen_interaction_0080

- Question: Tôi uống Bamstad cùng Hoàn thấp khớp B/P được không?
- Category: interaction
- Hit@K: True | Strict Hit@K: False
- First relevant rank: 3
- First strict rank: None
- Top result: `dav_all` / `drug_info` / `official_registry` / Thấp khớp hoàn

### gen_interaction_0081

- Question: Tôi uống Pitavastatin SOHA 1 mg cùng Mediphylamin được không?
- Category: interaction
- Hit@K: True | Strict Hit@K: False
- First relevant rank: 3
- First strict rank: None
- Top result: `dav_all` / `drug_info` / `official_registry` / Pitavastatin SOHA 4 mg

### gen_interaction_0082

- Question: Tôi uống Henazepril 10 cùng Chondrasil được không?
- Category: interaction
- Hit@K: True | Strict Hit@K: False
- First relevant rank: 1
- First strict rank: None
- Top result: `dav_all` / `drug_info` / `official_registry` / Henazepril 10

### gen_interaction_0083

- Question: Tôi uống Bifitacine cùng Cefazolin 2g được không?
- Category: interaction
- Hit@K: True | Strict Hit@K: False
- First relevant rank: 1
- First strict rank: None
- Top result: `dav_all` / `drug_info` / `official_registry` / Cefazolin 2g

### gen_interaction_0084

- Question: Tôi uống Micindrop cùng Recombinant Streptokinase for injection được không?
- Category: interaction
- Hit@K: True | Strict Hit@K: False
- First relevant rank: 1
- First strict rank: None
- Top result: `dav_all` / `drug_info` / `official_registry` / Recombinant Streptokinase for injection

### gen_interaction_0085

- Question: Tôi uống Albenca 400 cùng pms- Sparenil được không?
- Category: interaction
- Hit@K: True | Strict Hit@K: False
- First relevant rank: 1
- First strict rank: None
- Top result: `dav_all` / `drug_info` / `official_registry` / Albenca 400

### gen_interaction_0086

- Question: Tôi uống Linezolid 600mg/300ml cùng Thần kinh tọa thống hoàn được không?
- Category: interaction
- Hit@K: True | Strict Hit@K: False
- First relevant rank: 1
- First strict rank: None
- Top result: `dav_all` / `drug_info` / `official_registry` / Linezolid 600mg/300ml

### gen_interaction_0087

- Question: Tôi uống Ciprofloxacin Polpharma cùng Puyol được không?
- Category: interaction
- Hit@K: True | Strict Hit@K: False
- First relevant rank: 1
- First strict rank: None
- Top result: `dav_all` / `drug_info` / `official_registry` / Ciprofloxacin Polpharma

### gen_interaction_0088

- Question: Tôi uống Glimepiride Stada 4 mg cùng Glumeform 500 được không?
- Category: interaction
- Hit@K: False | Strict Hit@K: False
- First relevant rank: None
- First strict rank: None
- Top result: `dav_pdf_ocr` / `interaction` / `unverified_ocr` / Redolvonkids

### gen_interaction_0089

- Question: Tôi uống Cilzobac cùng Rilpirant được không?
- Category: interaction
- Hit@K: True | Strict Hit@K: False
- First relevant rank: 2
- First strict rank: None
- Top result: `dav_pdf_ocr` / `safety` / `unverified_ocr` / Fexosin 30

### gen_interaction_0090

- Question: Tôi uống Gemcitabine Medac cùng Agi-Bromhexine 4 được không?
- Category: interaction
- Hit@K: True | Strict Hit@K: False
- First relevant rank: 1
- First strict rank: None
- Top result: `dav_all` / `drug_info` / `official_registry` / Gemcitabine Medac (CS đóng gói: Medac Gesellschaft fur klinische spezialpraparate mbH-Đ/c:Theaterstrasse 6-22880 Wedel, Germany)

### gen_interaction_0091

- Question: Tôi uống Lenvima 10mg cùng Sturizin 25 được không?
- Category: interaction
- Hit@K: True | Strict Hit@K: False
- First relevant rank: 1
- First strict rank: None
- Top result: `dav_all` / `drug_info` / `official_registry` / Lenvima 10mg

### gen_interaction_0092

- Question: Tôi uống Flumax Night Time cùng Ceverxyl 300 mg được không?
- Category: interaction
- Hit@K: True | Strict Hit@K: False
- First relevant rank: 1
- First strict rank: None
- Top result: `dav_all` / `drug_info` / `official_registry` / Ceverxyl 300 mg

### gen_interaction_0093

- Question: Tôi uống Para Max 160 cùng Irinotecan Hydrochloride Injection 40mg/2ml được không?
- Category: interaction
- Hit@K: True | Strict Hit@K: False
- First relevant rank: 1
- First strict rank: None
- Top result: `dav_all` / `drug_info` / `official_registry` / Irinotecan Hydrochloride Injection 40mg/2ml

### gen_interaction_0094

- Question: Tôi uống Mexiprim 4 cùng Aprodox 200 được không?
- Category: interaction
- Hit@K: True | Strict Hit@K: False
- First relevant rank: 1
- First strict rank: None
- Top result: `dav_all` / `drug_info` / `official_registry` / Aprodox 200

### gen_interaction_0095

- Question: Tôi uống Lanseva cùng Cholin alfoscerat được không?
- Category: interaction
- Hit@K: True | Strict Hit@K: False
- First relevant rank: 1
- First strict rank: None
- Top result: `dav_all` / `drug_info` / `official_registry` / Cholin alfoscerat 600 mg/7 ml

### gen_interaction_0096

- Question: Tôi uống Planifert cùng Etodax 400 được không?
- Category: interaction
- Hit@K: True | Strict Hit@K: False
- First relevant rank: 1
- First strict rank: None
- Top result: `dav_all` / `drug_info` / `official_registry` / Etodax 400

### gen_emergency_0001

- Question: Tôi bị khó thở sau khi uống thuốc thì làm sao?
- Category: emergency
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_pdf_ocr` / `dosage` / `unverified_ocr` / Jazxylo Baby & Kid Spray

### gen_emergency_0002

- Question: Tôi bị đau ngực sau khi uống thuốc thì làm sao?
- Category: emergency
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Tây Thi

### gen_emergency_0003

- Question: Tôi bị co giật sau khi dùng thuốc thì làm sao?
- Category: emergency
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_pdf_ocr` / `safety` / `unverified_ocr` / Parlodex

### gen_emergency_0004

- Question: Tôi bị lơ mơ sau khi uống nhầm thuốc thì làm sao?
- Category: emergency
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_pdf_ocr` / `drug_info` / `unverified_ocr` / Redolvonkids

### gen_emergency_0005

- Question: Tôi bị phù môi sau khi uống thuốc thì làm sao?
- Category: emergency
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_pdf_ocr` / `safety` / `unverified_ocr` / Parlodex

### gen_emergency_0006

- Question: Tôi bị nghi quá liều paracetamol thì làm sao?
- Category: emergency
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_pdf_ocr` / `drug_info` / `unverified_ocr` / Desloratadin MCN 5 ODT

### gen_emergency_0007

- Question: Tôi bị uống nhầm nhiều viên thuốc thì làm sao?
- Category: emergency
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Trần bì vi sao

### gen_emergency_0008

- Question: Tôi bị sốc phản vệ sau tiêm thuốc thì làm sao?
- Category: emergency
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Tây Thi

### gen_emergency_0009

- Question: khó thở sau khi uống thuốc, tôi nên dùng thuốc gì?
- Category: emergency
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_pdf_ocr` / `drug_info` / `unverified_ocr` / Levonorgestrel 
1,5 mg

### gen_emergency_0010

- Question: đau ngực sau khi uống thuốc, tôi nên dùng thuốc gì?
- Category: emergency
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_pdf_ocr` / `drug_info` / `unverified_ocr` / Levonorgestrel 
1,5 mg

### gen_emergency_0011

- Question: co giật sau khi dùng thuốc, tôi nên dùng thuốc gì?
- Category: emergency
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_pdf_ocr` / `safety` / `unverified_ocr` / Haristol

### gen_emergency_0012

- Question: lơ mơ sau khi uống nhầm thuốc, tôi nên dùng thuốc gì?
- Category: emergency
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_pdf_ocr` / `drug_info` / `unverified_ocr` / Redolvonkids

### gen_emergency_0013

- Question: phù môi sau khi uống thuốc, tôi nên dùng thuốc gì?
- Category: emergency
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_pdf_ocr` / `drug_info` / `unverified_ocr` / Levonorgestrel 
1,5 mg

### gen_emergency_0014

- Question: nghi quá liều paracetamol, tôi nên dùng thuốc gì?
- Category: emergency
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_pdf_ocr` / `safety` / `unverified_ocr` / Fexosin 30

### gen_emergency_0015

- Question: uống nhầm nhiều viên thuốc, tôi nên dùng thuốc gì?
- Category: emergency
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / "Never event" - những sai sót không được phép xảy ra: Thông tin từ Bản tin Cảnh giác Dược liên vùng Grand Est và Bourgogne/ Franche-Comté số 48

### gen_emergency_0016

- Question: sốc phản vệ sau tiêm thuốc, tôi nên dùng thuốc gì?
- Category: emergency
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / CBIP: Nguy cơ phản ứng dị ứng nghiêm trọng khi sử dụng clorhexidin

### gen_emergency_0017

- Question: Người nhà tôi khó thở sau khi uống thuốc, có cần đi viện không?
- Category: emergency
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_pdf_ocr` / `drug_info` / `unverified_ocr` / Levonorgestrel 
1,5 mg

### gen_emergency_0018

- Question: Người nhà tôi đau ngực sau khi uống thuốc, có cần đi viện không?
- Category: emergency
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_pdf_ocr` / `drug_info` / `unverified_ocr` / Levonorgestrel 
1,5 mg

### gen_emergency_0019

- Question: Người nhà tôi co giật sau khi dùng thuốc, có cần đi viện không?
- Category: emergency
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_pdf_ocr` / `drug_info` / `unverified_ocr` / Levonorgestrel 
1,5 mg

### gen_emergency_0020

- Question: Người nhà tôi lơ mơ sau khi uống nhầm thuốc, có cần đi viện không?
- Category: emergency
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_pdf_ocr` / `drug_info` / `unverified_ocr` / Levonorgestrel 
1,5 mg

### gen_emergency_0021

- Question: Người nhà tôi phù môi sau khi uống thuốc, có cần đi viện không?
- Category: emergency
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_pdf_ocr` / `drug_info` / `unverified_ocr` / Levonorgestrel 
1,5 mg

### gen_emergency_0022

- Question: Người nhà tôi nghi quá liều paracetamol, có cần đi viện không?
- Category: emergency
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_pdf_ocr` / `dosage` / `unverified_ocr` / Effer phazandol cafein 65

### gen_emergency_0023

- Question: Người nhà tôi uống nhầm nhiều viên thuốc, có cần đi viện không?
- Category: emergency
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_pdf_ocr` / `dosage` / `unverified_ocr` / DH-Pacegan 500

### gen_emergency_0024

- Question: Người nhà tôi sốc phản vệ sau tiêm thuốc, có cần đi viện không?
- Category: emergency
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_pdf_ocr` / `safety` / `unverified_ocr` / Fexosin 30

### gen_emergency_0025

- Question: Tôi bị khó thở sau khi uống thuốc thì làm sao?
- Category: emergency
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_pdf_ocr` / `dosage` / `unverified_ocr` / Jazxylo Baby & Kid Spray

### gen_emergency_0026

- Question: Tôi bị đau ngực sau khi uống thuốc thì làm sao?
- Category: emergency
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Tây Thi

### gen_emergency_0027

- Question: Tôi bị co giật sau khi dùng thuốc thì làm sao?
- Category: emergency
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_pdf_ocr` / `safety` / `unverified_ocr` / Parlodex

### gen_emergency_0028

- Question: Tôi bị lơ mơ sau khi uống nhầm thuốc thì làm sao?
- Category: emergency
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_pdf_ocr` / `drug_info` / `unverified_ocr` / Redolvonkids

### gen_emergency_0029

- Question: Tôi bị phù môi sau khi uống thuốc thì làm sao?
- Category: emergency
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_pdf_ocr` / `safety` / `unverified_ocr` / Parlodex

### gen_emergency_0030

- Question: Tôi bị nghi quá liều paracetamol thì làm sao?
- Category: emergency
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_pdf_ocr` / `drug_info` / `unverified_ocr` / Desloratadin MCN 5 ODT

### gen_emergency_0031

- Question: Tôi bị uống nhầm nhiều viên thuốc thì làm sao?
- Category: emergency
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Trần bì vi sao

### gen_emergency_0032

- Question: Tôi bị sốc phản vệ sau tiêm thuốc thì làm sao?
- Category: emergency
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Tây Thi

### gen_emergency_0033

- Question: khó thở sau khi uống thuốc, tôi nên dùng thuốc gì?
- Category: emergency
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_pdf_ocr` / `drug_info` / `unverified_ocr` / Levonorgestrel 
1,5 mg

### gen_emergency_0034

- Question: đau ngực sau khi uống thuốc, tôi nên dùng thuốc gì?
- Category: emergency
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_pdf_ocr` / `drug_info` / `unverified_ocr` / Levonorgestrel 
1,5 mg

### gen_emergency_0035

- Question: co giật sau khi dùng thuốc, tôi nên dùng thuốc gì?
- Category: emergency
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_pdf_ocr` / `safety` / `unverified_ocr` / Haristol

### gen_emergency_0036

- Question: lơ mơ sau khi uống nhầm thuốc, tôi nên dùng thuốc gì?
- Category: emergency
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_pdf_ocr` / `drug_info` / `unverified_ocr` / Redolvonkids

### gen_emergency_0037

- Question: phù môi sau khi uống thuốc, tôi nên dùng thuốc gì?
- Category: emergency
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_pdf_ocr` / `drug_info` / `unverified_ocr` / Levonorgestrel 
1,5 mg

### gen_emergency_0038

- Question: nghi quá liều paracetamol, tôi nên dùng thuốc gì?
- Category: emergency
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_pdf_ocr` / `safety` / `unverified_ocr` / Fexosin 30

### gen_emergency_0039

- Question: uống nhầm nhiều viên thuốc, tôi nên dùng thuốc gì?
- Category: emergency
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / "Never event" - những sai sót không được phép xảy ra: Thông tin từ Bản tin Cảnh giác Dược liên vùng Grand Est và Bourgogne/ Franche-Comté số 48

### gen_emergency_0040

- Question: sốc phản vệ sau tiêm thuốc, tôi nên dùng thuốc gì?
- Category: emergency
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `canhgiacduoc` / `safety_article` / `trusted_safety_article` / CBIP: Nguy cơ phản ứng dị ứng nghiêm trọng khi sử dụng clorhexidin

### gen_emergency_0041

- Question: Người nhà tôi khó thở sau khi uống thuốc, có cần đi viện không?
- Category: emergency
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_pdf_ocr` / `drug_info` / `unverified_ocr` / Levonorgestrel 
1,5 mg

### gen_emergency_0042

- Question: Người nhà tôi đau ngực sau khi uống thuốc, có cần đi viện không?
- Category: emergency
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_pdf_ocr` / `drug_info` / `unverified_ocr` / Levonorgestrel 
1,5 mg

### gen_emergency_0043

- Question: Người nhà tôi co giật sau khi dùng thuốc, có cần đi viện không?
- Category: emergency
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_pdf_ocr` / `drug_info` / `unverified_ocr` / Levonorgestrel 
1,5 mg

### gen_emergency_0044

- Question: Người nhà tôi lơ mơ sau khi uống nhầm thuốc, có cần đi viện không?
- Category: emergency
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_pdf_ocr` / `drug_info` / `unverified_ocr` / Levonorgestrel 
1,5 mg

### gen_emergency_0045

- Question: Người nhà tôi phù môi sau khi uống thuốc, có cần đi viện không?
- Category: emergency
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_pdf_ocr` / `drug_info` / `unverified_ocr` / Levonorgestrel 
1,5 mg

### gen_emergency_0046

- Question: Người nhà tôi nghi quá liều paracetamol, có cần đi viện không?
- Category: emergency
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_pdf_ocr` / `dosage` / `unverified_ocr` / Effer phazandol cafein 65

### gen_emergency_0047

- Question: Người nhà tôi uống nhầm nhiều viên thuốc, có cần đi viện không?
- Category: emergency
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_pdf_ocr` / `dosage` / `unverified_ocr` / DH-Pacegan 500

### gen_emergency_0048

- Question: Người nhà tôi sốc phản vệ sau tiêm thuốc, có cần đi viện không?
- Category: emergency
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_pdf_ocr` / `safety` / `unverified_ocr` / Fexosin 30

### gen_emergency_0049

- Question: Tôi bị khó thở sau khi uống thuốc thì làm sao?
- Category: emergency
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_pdf_ocr` / `dosage` / `unverified_ocr` / Jazxylo Baby & Kid Spray

### gen_emergency_0050

- Question: Tôi bị đau ngực sau khi uống thuốc thì làm sao?
- Category: emergency
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Tây Thi

### gen_emergency_0051

- Question: Tôi bị co giật sau khi dùng thuốc thì làm sao?
- Category: emergency
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_pdf_ocr` / `safety` / `unverified_ocr` / Parlodex

### gen_emergency_0052

- Question: Tôi bị lơ mơ sau khi uống nhầm thuốc thì làm sao?
- Category: emergency
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_pdf_ocr` / `drug_info` / `unverified_ocr` / Redolvonkids

### gen_emergency_0053

- Question: Tôi bị phù môi sau khi uống thuốc thì làm sao?
- Category: emergency
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_pdf_ocr` / `safety` / `unverified_ocr` / Parlodex

### gen_emergency_0054

- Question: Tôi bị nghi quá liều paracetamol thì làm sao?
- Category: emergency
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_pdf_ocr` / `drug_info` / `unverified_ocr` / Desloratadin MCN 5 ODT

### gen_emergency_0055

- Question: Tôi bị uống nhầm nhiều viên thuốc thì làm sao?
- Category: emergency
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Trần bì vi sao

### gen_emergency_0056

- Question: Tôi bị sốc phản vệ sau tiêm thuốc thì làm sao?
- Category: emergency
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_all` / `drug_info` / `official_registry` / Tây Thi

### gen_emergency_0057

- Question: khó thở sau khi uống thuốc, tôi nên dùng thuốc gì?
- Category: emergency
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_pdf_ocr` / `drug_info` / `unverified_ocr` / Levonorgestrel 
1,5 mg

### gen_emergency_0058

- Question: đau ngực sau khi uống thuốc, tôi nên dùng thuốc gì?
- Category: emergency
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_pdf_ocr` / `drug_info` / `unverified_ocr` / Levonorgestrel 
1,5 mg

### gen_emergency_0059

- Question: co giật sau khi dùng thuốc, tôi nên dùng thuốc gì?
- Category: emergency
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_pdf_ocr` / `safety` / `unverified_ocr` / Haristol

### gen_emergency_0060

- Question: lơ mơ sau khi uống nhầm thuốc, tôi nên dùng thuốc gì?
- Category: emergency
- Hit@K: True | Strict Hit@K: True
- First relevant rank: 1
- First strict rank: 1
- Top result: `dav_pdf_ocr` / `drug_info` / `unverified_ocr` / Redolvonkids

