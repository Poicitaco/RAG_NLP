"""Create curated OTC condition guardrail chunks for common public questions."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, Iterable, List


RULES: List[Dict[str, Any]] = [
    {
        "id": "otc-supplement:general:zinc:weakness",
        "condition": "general",
        "condition_vi": "người lớn nói chung",
        "otc_category": "zinc_supplement",
        "symptom_group": "mệt/yếu hoặc muốn bổ sung kẽm",
        "ingredients_to_avoid_or_check": [
            "kẽm liều cao dùng kéo dài",
            "kẽm dùng cùng kháng sinh nhóm quinolone/tetracycline",
            "kẽm dùng cùng penicillamine",
            "kẽm dạng xịt mũi",
        ],
        "risk_level": "caution",
        "recommendation": (
            "Nếu chỉ thấy yếu/mệt, không nên tự xem kẽm là cách điều trị chính vì mệt có thể do thiếu ngủ, thiếu máu, "
            "nhiễm trùng, bệnh tuyến giáp, đường huyết hoặc nhiều nguyên nhân khác. Nếu người lớn vẫn muốn bổ sung, "
            "nên chọn sản phẩm ghi rõ lượng kẽm nguyên tố (elemental zinc), ưu tiên liều thấp gần nhu cầu hằng ngày "
            "khoảng 8-11 mg/ngày cho người lớn, và không tự dùng liều cao hoặc kéo dài. Không vượt 40 mg kẽm nguyên tố/ngày "
            "ở người lớn nếu không có chỉ định. Tránh kẽm dạng xịt mũi; kẽm uống có thể gây buồn nôn, đau bụng, tiêu chảy "
            "và dùng liều cao lâu ngày có thể gây thiếu đồng."
        ),
        "safer_options": [
            "ăn đa dạng thực phẩm giàu kẽm như thịt, hải sản, trứng, sữa, đậu/hạt nếu phù hợp",
            "chọn viên kẽm liều thấp, ghi rõ elemental zinc, không phối hợp quá nhiều vitamin/khoáng chất không cần thiết",
            "uống sau ăn nếu bị cồn cào/buồn nôn",
            "đi khám hoặc xét nghiệm nếu mệt/yếu kéo dài, sụt cân, sốt, khó thở, chóng mặt nhiều hoặc ăn uống kém",
        ],
        "red_flags": [
            "mệt/yếu kéo dài nhiều ngày hoặc nặng dần",
            "khó thở, đau ngực, choáng/ngất",
            "sụt cân không rõ lý do, sốt kéo dài",
            "đang mang thai, bệnh thận/gan, đang dùng kháng sinh, penicillamine hoặc thuốc lợi tiểu thiazide",
        ],
        "citations": [
            {
                "title": "NIH Office of Dietary Supplements: Zinc Fact Sheet for Health Professionals",
                "url": "https://ods.od.nih.gov/factsheets/Zinc-HealthProfessional/",
                "note": "RDA for adult zinc is 8 mg/day for women and 11 mg/day for men; adult tolerable upper intake level is 40 mg/day; excess zinc may cause adverse effects and copper deficiency.",
            },
            {
                "title": "NHS: Vitamins and minerals - Others",
                "url": "https://www.nhs.uk/conditions/vitamins-and-minerals/others/",
                "note": "NHS advises a varied diet should provide needed zinc and not taking more than 25 mg/day from supplements unless advised by a doctor.",
            },
            {
                "title": "NIH Office of Dietary Supplements: Zinc Fact Sheet for Consumers",
                "url": "https://ods.od.nih.gov/factsheets/Zinc-Consumer/",
                "note": "Zinc can interact with quinolone/tetracycline antibiotics, penicillamine, and thiazide diuretics; spacing from some antibiotics is recommended.",
            },
        ],
    },
    {
        "id": "otc-symptom:general:cold_flu:self_care",
        "condition": "",
        "condition_vi": "người lớn nói chung",
        "otc_category": "cold_flu",
        "symptom_group": "cảm/cúm nhẹ, sổ mũi, nghẹt mũi, đau nhức hoặc sốt nhẹ",
        "ingredients_to_avoid_or_check": [
            "kháng sinh tự mua",
            "thuốc cảm phối hợp nhiều thành phần",
            "uống trùng paracetamol trong nhiều thuốc cảm",
            "pseudoephedrine/phenylephrine nếu có huyết áp cao, tiểu đường hoặc bệnh tim",
        ],
        "risk_level": "caution",
        "recommendation": (
            "Với cảm/cúm nhẹ ở người lớn, thường ưu tiên nghỉ ngơi, uống đủ nước và xử lý theo triệu chứng. "
            "Nếu sốt hoặc đau nhức có thể cân nhắc nhóm hạ sốt/giảm đau phù hợp; nếu nghẹt mũi nên ưu tiên rửa/xịt mũi nước muối. "
            "Không tự mua kháng sinh cho cảm thông thường vì cảm thường do virus. Cần đọc nhãn thuốc cảm phối hợp để tránh uống trùng hoạt chất, "
            "đặc biệt là paracetamol."
        ),
        "safer_options": [
            "nghỉ ngơi, uống đủ nước, rửa mũi bằng nước muối sinh lý",
            "nếu sốt/đau nhức: cân nhắc nhóm hạ sốt giảm đau phù hợp và kiểm tra không uống trùng hoạt chất",
            "nếu nghẹt mũi: ưu tiên nước muối/xịt mũi trước; thận trọng với thuốc thông mũi đường uống",
            "không tự dùng kháng sinh cho cảm thông thường",
        ],
        "red_flags": [
            "khó thở, đau ngực, tím tái hoặc lơ mơ",
            "sốt cao hoặc sốt kéo dài",
            "triệu chứng nặng dần, người già, trẻ nhỏ, mang thai hoặc có bệnh nền nặng",
        ],
        "citations": [
            {
                "title": "NHS: Common cold",
                "url": "https://www.nhs.uk/conditions/common-cold/",
                "note": "NHS lists pharmacist-advised options including paracetamol/ibuprofen for aches or temperature and decongestants for blocked nose, with age cautions.",
            },
            {
                "title": "CDC: Manage Common Cold",
                "url": "https://www.cdc.gov/common-cold/treatment/index.html",
                "note": "CDC states the common cold has no cure, improves on its own, and antibiotics do not work against viruses.",
            },
        ],
    },
    {
        "id": "otc-symptom:general:diarrhea:oral_rehydration",
        "condition": "",
        "condition_vi": "người lớn nói chung",
        "otc_category": "diarrhea",
        "symptom_group": "tiêu chảy/đi ngoài/đau bụng quặn",
        "ingredients_to_avoid_or_check": [
            "tự dùng thuốc cầm tiêu chảy mạnh ngay khi mới đi ngoài 1-2 lần",
            "tự dùng thuốc cầm tiêu chảy khi sốt cao, nôn liên tục, đau bụng dữ dội hoặc đi ngoài ra máu",
            "loperamide nếu nghi nhiễm khuẩn nặng hoặc có dấu hiệu cảnh báo",
            "kháng sinh tự mua",
        ],
        "risk_level": "caution",
        "recommendation": (
            "Khi đi ngoài kèm đau bụng, việc cần làm trước là bù nước và điện giải bằng Oresol pha đúng tỷ lệ trên gói/bao bì, uống rải rác. "
            "Không nên vội dùng thuốc cầm tiêu chảy mạnh như loperamide nếu mới đi ngoài 1-2 lần, vì cơ thể có thể đang đào thải tác nhân gây kích ứng/nhiễm khuẩn. "
            "Nếu đau bụng quặn từng cơn và không có dấu hiệu nguy hiểm, có thể hỏi dược sĩ về thuốc giảm co thắt như drotaverin hoặc mebeverine; không tự mua kháng sinh khi chưa được khám."
        ),
        "safer_options": [
            "mua Oresol/dung dịch bù nước điện giải, pha đúng tỷ lệ theo gói hoặc bao bì và uống rải rác thay nước lọc",
            "nếu bụng quặn đau từng cơn và không có dấu hiệu nguy hiểm, hỏi dược sĩ về thuốc giảm co thắt như drotaverin hoặc mebeverine",
            "có thể hỏi dược sĩ về men vi sinh/probiotics để hỗ trợ cân bằng hệ khuẩn ruột",
            "không dùng loperamide nếu sốt cao, phân máu, nôn liên tục, đau bụng dữ dội hoặc nghi nhiễm khuẩn",
            "ăn nhẹ, tránh rượu bia và đồ nhiều dầu mỡ trong lúc đang tiêu chảy",
        ],
        "red_flags": [
            "buồn nôn hoặc nôn mửa liên tục",
            "sốt cao",
            "đi ngoài ra máu hoặc phân đen",
            "đau bụng dữ dội không giảm hoặc đau tăng dần",
            "dấu mất nước, lừ đừ, tiểu rất ít",
            "trẻ nhỏ, người già, phụ nữ mang thai hoặc người có bệnh nền",
        ],
        "citations": [
            {
                "title": "CDC: Treatment of Diarrhea",
                "url": "https://www.cdc.gov/diarrhea/treatment/index.html",
                "note": "CDC emphasizes fluids and oral rehydration for diarrhea and seeking care for severe symptoms.",
            },
            {
                "title": "NHS: Diarrhoea and vomiting",
                "url": "https://www.nhs.uk/conditions/diarrhoea-and-vomiting/",
                "note": "NHS advises fluids and highlights red flags such as blood in stool and dehydration.",
            },
            {
                "title": "NHS: Common questions about mebeverine",
                "url": "https://www.nhs.uk/medicines/mebeverine/common-questions-about-mebeverine/",
                "note": "NHS describes mebeverine as an antispasmodic that relaxes intestine muscles to relieve cramps and pain.",
            },
            {
                "title": "Drotaverin - Trung Tâm Thuốc",
                "url": "https://trungtamthuoc.com/hoat-chat/drotaverine",
                "note": "Trung Tâm Thuốc lists drotaverin for painful cramps related to smooth muscle spasm, including digestive tract spasm.",
            },
        ],
    },
    {
        "id": "otc-supplement:general:vitamin_c:high_dose",
        "condition": "",
        "condition_vi": "người lớn nói chung",
        "otc_category": "vitamin_c",
        "symptom_group": "mệt hoặc muốn uống vitamin C liều cao",
        "ingredients_to_avoid_or_check": [
            "vitamin C liều cao kéo dài",
            "uống nhiều sản phẩm cùng chứa vitamin C",
            "vitamin C liều cao nếu có tiền sử sỏi thận hoặc bệnh thận",
        ],
        "risk_level": "caution",
        "recommendation": (
            "Không nên xem vitamin C liều cao là cách làm khỏe nhanh khi chỉ thấy mệt. Người lớn không nên vượt quá 2.000 mg vitamin C/ngày. "
            "Liều cao có thể gây tiêu chảy, buồn nôn, đau quặn bụng và có thể không phù hợp nếu có bệnh thận hoặc tiền sử sỏi thận."
        ),
        "safer_options": [
            "ưu tiên ăn trái cây/rau giàu vitamin C và ngủ nghỉ đủ",
            "nếu dùng viên uống, chọn liều vừa phải và tránh dùng nhiều sản phẩm trùng vitamin C",
            "không tự dùng liều cao kéo dài để trị mệt",
            "đi khám nếu mệt kéo dài, sụt cân, sốt, khó thở, chóng mặt nhiều hoặc ăn uống kém",
        ],
        "red_flags": [
            "mệt kéo dài hoặc nặng dần",
            "đau hông lưng, tiểu buốt/tiểu máu, tiền sử sỏi thận",
            "khó thở, đau ngực, choáng/ngất",
        ],
        "citations": [
            {
                "title": "Mayo Clinic: Too much vitamin C",
                "url": "https://www.mayoclinic.org/healthy-lifestyle/nutrition-and-healthy-eating/expert-answers/vitamin-c/faq-20058030",
                "note": "Mayo Clinic states adults should not exceed 2,000 mg/day and high doses may cause diarrhea, nausea and cramps.",
            },
            {
                "title": "NIH Office of Dietary Supplements: Vitamin C Fact Sheet",
                "url": "https://ods.od.nih.gov/factsheets/VitaminC-HealthProfessional/",
                "note": "NIH ODS provides intake and upper limit information for vitamin C.",
            },
        ],
    },
    {
        "id": "otc-symptom:general:cough:screening",
        "condition": "",
        "condition_vi": "người lớn nói chung",
        "otc_category": "cough",
        "symptom_group": "ho khan/ho có đờm",
        "ingredients_to_avoid_or_check": [
            "thuốc ức chế ho khi ho nhiều đờm chưa rõ nguyên nhân",
            "siro ho phối hợp nhiều thành phần",
            "thuốc ho cho trẻ nhỏ nếu chưa có tuổi/cân nặng",
        ],
        "risk_level": "caution",
        "recommendation": (
            "Cần phân biệt ho khan, ho có đờm, ho kèm sốt/khó thở và thời gian ho trước khi chọn thuốc. "
            "Không nên tự chọn siro ho phối hợp nhiều thành phần nếu chưa rõ loại ho, bệnh nền và thuốc đang dùng."
        ),
        "safer_options": [
            "uống đủ nước, giữ ẩm họng, tránh khói thuốc",
            "nếu ho có đờm: không tự ức chế ho mạnh khi chưa rõ nguyên nhân",
            "nếu ho khan nhiều: cần kiểm tra thành phần thuốc ho và bệnh nền/thuốc đang dùng",
            "đi khám nếu khó thở, đau ngực, sốt cao, ho ra máu hoặc ho kéo dài",
        ],
        "red_flags": [
            "khó thở, đau ngực, tím tái",
            "ho ra máu",
            "sốt cao hoặc ho kéo dài",
            "trẻ nhỏ, người già, mang thai hoặc bệnh phổi/tim nền",
        ],
        "citations": [
            {
                "title": "NHS: Cough",
                "url": "https://www.nhs.uk/conditions/cough/",
                "note": "NHS gives self-care advice and red flags for cough.",
            }
        ],
    },
    {
        "id": "otc-condition:diabetes:cold:oral-decongestants",
        "condition": "diabetes",
        "condition_vi": "tiểu đường/đái tháo đường",
        "otc_category": "cold_flu",
        "symptom_group": "nghẹt mũi/cảm cúm",
        "ingredients_to_avoid_or_check": ["pseudoephedrine", "phenylephrine", "ephedrine"],
        "risk_level": "caution",
        "recommendation": (
            "Người có tiểu đường nên tránh tự mua thuốc cảm/nghẹt mũi có thuốc co mạch đường uống như "
            "pseudoephedrine, phenylephrine hoặc ephedrine nếu chưa hỏi bác sĩ/dược sĩ, vì nhóm này có thể làm tăng "
            "đường huyết, tăng huyết áp hoặc ảnh hưởng bệnh nền/thuốc đang dùng."
        ),
        "safer_options": [
            "xịt/rửa mũi bằng nước muối sinh lý",
            "thuốc chỉ chứa paracetamol để hạ sốt/đau nếu không có chống chỉ định và không dùng quá liều",
            "hỏi dược sĩ để chọn thuốc không đường nếu cần siro",
        ],
        "red_flags": [
            "sốt cao hoặc kéo dài",
            "khó thở, đau ngực",
            "đường huyết tăng cao bất thường",
            "đang dùng nhiều thuốc điều trị tiểu đường/tim mạch/huyết áp",
        ],
        "citations": [
            {
                "title": "21 CFR 341.80 OTC nasal decongestant warnings",
                "url": "https://www.law.cornell.edu/cfr/text/21/341.80",
                "note": "US OTC monograph warnings mention diabetes for decongestant products unless directed by a doctor.",
            },
            {
                "title": "Mayo Clinic Q and A: Decongestants can sometimes cause more harm than good",
                "url": "https://newsnetwork.mayoclinic.org/discussion/mayo-clinic-q-and-a-decongestants-can-sometimes-cause-more-harm-than-good/",
                "note": "Oral decongestants can raise blood pressure and blood sugar and may affect diabetes medicines.",
            },
            {
                "title": "FDA proposes ending oral phenylephrine as OTC nasal decongestant",
                "url": "https://www.fda.gov/news-events/press-announcements/fda-proposes-ending-use-oral-phenylephrine-otc-monograph-nasal-decongestant-active-ingredient-after",
                "note": "FDA states oral phenylephrine is proposed for removal from OTC monograph due to lack of effectiveness.",
            },
        ],
    },
    {
        "id": "otc-condition:hypertension:pain_cold:nsaids_decongestants",
        "condition": "hypertension",
        "condition_vi": "cao huyết áp/tăng huyết áp",
        "otc_category": "pain_cold",
        "symptom_group": "đau nhức/cảm cúm/nghẹt mũi",
        "ingredients_to_avoid_or_check": ["ibuprofen", "diclofenac", "naproxen", "pseudoephedrine", "phenylephrine", "ephedrine"],
        "risk_level": "caution",
        "recommendation": (
            "Người có tiền sử huyết áp cao nên thận trọng khi dùng các thuốc giảm đau kháng viêm không steroid (NSAIDs) "
            "như ibuprofen, diclofenac, naproxen và thuốc co mạch trị nghẹt mũi như pseudoephedrine. "
            "Các thuốc này có thể làm tăng huyết áp và giảm tác dụng của thuốc hạ huyết áp đang dùng."
        ),
        "safer_options": [
            "paracetamol để giảm đau, hạ sốt",
            "xịt mũi nước muối sinh lý thay vì thuốc co mạch đường uống",
            "hỏi ý kiến bác sĩ/dược sĩ trước khi dùng bất kỳ thuốc cảm cúm kết hợp nào"
        ],
        "red_flags": [
            "huyết áp tăng cao đột ngột (đo tại nhà)",
            "đau đầu dữ dội, hoa mắt, chóng mặt",
            "khó thở, đau tức ngực",
            "mặt phù, sưng phù chân tay"
        ],
        "citations": [
            {
                "title": "High blood pressure and cold remedies: Which are safe?",
                "url": "https://www.mayoclinic.org/diseases-conditions/high-blood-pressure/expert-answers/blood-pressure/faq-20058254",
                "note": "Decongestants and some pain relievers like NSAIDs can increase blood pressure."
            }
        ],
    },
    {
        "id": "otc-condition:peptic_ulcer:pain:nsaids",
        "condition": "peptic_ulcer",
        "condition_vi": "viêm loét dạ dày tá tràng",
        "otc_category": "pain_inflammation",
        "symptom_group": "đau nhức/viêm/sốt",
        "ingredients_to_avoid_or_check": ["ibuprofen", "diclofenac", "naproxen", "aspirin", "piroxicam", "meloxicam", "celecoxib", "corticosteroid"],
        "risk_level": "high_risk",
        "recommendation": (
            "Người có tiền sử hoặc đang bị viêm loét dạ dày tá tràng cần ĐẶC BIỆT LƯU Ý tránh tự ý dùng thuốc giảm đau "
            "kháng viêm không steroid (NSAIDs) hoặc Aspirin mà không có chỉ định của bác sĩ. "
            "Nhóm thuốc này gây tổn thương niêm mạc dạ dày và tăng nguy cơ xuất huyết tiêu hóa nghiêm trọng."
        ),
        "safer_options": [
            "paracetamol để giảm đau, hạ sốt (không gây loét dạ dày ở liều thông thường)",
            "chườm ấm/lạnh để giảm đau cơ khớp",
            "khám bác sĩ để được kê đơn thuốc bảo vệ dạ dày kèm theo nếu bắt buộc phải dùng NSAID"
        ],
        "red_flags": [
            "đau vùng thượng vị (trên rốn) dữ dội",
            "nôn ra máu hoặc dịch màu bã cà phê",
            "đi ngoài phân đen như nhựa đường hoặc có máu tươi",
            "chóng mặt, mệt lả do nghi ngờ mất máu"
        ],
        "citations": [
            {
                "title": "NSAIDs and Peptic Ulcer Disease",
                "url": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3891040/",
                "note": "NSAIDs are a major risk factor for peptic ulcer bleeding and perforation."
            }
        ],
    },
    {
        "id": "otc-condition:pregnancy:pain_fever:nsaids",
        "condition": "pregnancy",
        "condition_vi": "mang thai/có bầu",
        "otc_category": "pain_fever",
        "symptom_group": "đau nhức/sốt/viêm",
        "ingredients_to_avoid_or_check": ["ibuprofen", "diclofenac", "naproxen", "aspirin"],
        "risk_level": "high_risk",
        "recommendation": (
            "Phụ nữ có thai KHÔNG TỰ Ý sử dụng các thuốc giảm đau kháng viêm NSAIDs (như ibuprofen, diclofenac) "
            "đặc biệt là từ tuần thứ 20 của thai kỳ trở đi, do nguy cơ gây thiểu ối và các vấn đề về thận cho thai nhi. "
            "Dùng trong 3 tháng cuối thai kỳ có thể gây đóng sớm ống động mạch của thai."
        ),
        "safer_options": [
            "paracetamol được xem là lựa chọn an toàn hơn để giảm đau, hạ sốt trong thai kỳ (nhưng vẫn cần dùng liều thấp nhất có hiệu quả)",
            "tham khảo ý kiến bác sĩ sản khoa trước khi dùng bất kỳ loại thuốc nào"
        ],
        "red_flags": [
            "sốt cao không hạ",
            "đau bụng dưới, ra máu âm đạo",
            "thai nhi ít đạp/cử động (nếu ở 3 tháng cuối)",
            "phát ban, sưng phù mặt và tay chân"
        ],
        "citations": [
            {
                "title": "FDA Recommends Avoiding Use of NSAIDs in Pregnancy at 20 Weeks or Later",
                "url": "https://www.fda.gov/drugs/drug-safety-and-availability/fda-recommends-avoiding-use-nsaids-pregnancy-20-weeks-or-later-because-they-can-result-low-amniotic",
                "note": "FDA warns against using NSAIDs from 20 weeks of pregnancy due to rare but serious kidney problems in an unborn baby."
            }
        ],
    },
    {
        "id": "otc-condition:pediatric:cold_cough",
        "condition": "pediatric",
        "condition_vi": "trẻ em/trẻ nhỏ",
        "otc_category": "cold_cough",
        "symptom_group": "cảm cúm/ho/sổ mũi",
        "ingredients_to_avoid_or_check": [
            "thuốc ho cảm phối hợp",
            "kháng histamine thế hệ 1 (chlorpheniramine, diphenhydramine) cho trẻ <2 tuổi",
            "thuốc co mạch (xylometazoline) cho trẻ <2 tuổi"
        ],
        "risk_level": "high_risk",
        "recommendation": (
            "Không tự ý dùng các loại siro ho/cảm phối hợp nhiều thành phần cho trẻ nhỏ dưới 2 tuổi (hoặc dưới 6 tuổi tùy thuốc) "
            "vì nguy cơ tác dụng phụ nghiêm trọng như ức chế hô hấp, co giật. Thuốc nhỏ mũi co mạch cũng chống chỉ định cho trẻ dưới 2 tuổi."
        ),
        "safer_options": [
            "rửa mũi bằng nước muối sinh lý",
            "uống đủ nước",
            "paracetamol đơn chất hạ sốt theo cân nặng (10-15mg/kg/lần)",
            "đi khám bác sĩ nhi khoa"
        ],
        "red_flags": [
            "trẻ thở nhanh, thở rút lõm lồng ngực",
            "sốt cao khó hạ, lừ đừ",
            "bỏ bú, nôn trớ liên tục"
        ],
        "citations": [
            {
                "title": "FDA: Should You Give Kids Medicine for Coughs and Colds?",
                "url": "https://www.fda.gov/consumers/consumer-updates/should-you-give-kids-medicine-coughs-and-colds",
                "note": "FDA does not recommend OTC cold/cough medicines for children under 2."
            }
        ],
    },
    {
        "id": "otc-condition:kidney_liver:pain:nsaids_paracetamol",
        "condition": "kidney_liver_disease",
        "condition_vi": "suy thận/suy gan",
        "otc_category": "pain_fever",
        "symptom_group": "đau nhức/sốt",
        "ingredients_to_avoid_or_check": [
            "ibuprofen",
            "diclofenac",
            "naproxen (đối với suy thận)",
            "paracetamol liều cao (đối với suy gan)"
        ],
        "risk_level": "high_risk",
        "recommendation": (
            "Người suy thận tuyệt đối tránh NSAIDs (ibuprofen, diclofenac) vì có thể gây suy thận cấp. "
            "Người suy gan cần tránh hoặc giảm liều paracetamol (thường không quá 2g/ngày) và không uống rượu."
        ),
        "safer_options": [
            "người suy thận có thể dùng paracetamol liều chuẩn",
            "đi khám để bác sĩ kê đơn theo độ thanh thải thận/gan"
        ],
        "red_flags": [
            "phù nề tay chân, tiểu ít",
            "vàng da, vàng mắt",
            "mệt mỏi lừ đừ"
        ],
        "citations": [
            {
                "title": "Kidney Disease and OTC Medicines",
                "url": "https://www.kidney.org/atoz/content/painmeds",
                "note": "NSAIDs can cause acute kidney injury."
            }
        ],
    },
    {
        "id": "otc-condition:asthma:pain:nsaids",
        "condition": "asthma_copd",
        "condition_vi": "hen suyễn/COPD",
        "otc_category": "pain_fever",
        "symptom_group": "đau nhức/sốt",
        "ingredients_to_avoid_or_check": [
            "aspirin",
            "ibuprofen",
            "diclofenac",
            "thuốc nhỏ mắt chứa beta-blocker (timolol)"
        ],
        "risk_level": "high_risk",
        "recommendation": (
            "Người bị hen suyễn cần thận trọng với Aspirin và các NSAIDs (ibuprofen, diclofenac) do nguy cơ kích hoạt cơn hen cấp tính "
            "(AERD). Thuốc nhỏ mắt trị tăng nhãn áp nhóm beta-blocker cũng có thể gây co thắt phế quản."
        ),
        "safer_options": [
            "paracetamol thường an toàn cho người hen suyễn để giảm đau/hạ sốt",
            "hỏi bác sĩ khi cần dùng thuốc nhỏ mắt"
        ],
        "red_flags": [
            "khó thở, thở khò khè tăng lên",
            "cơn hen cấp không đáp ứng với thuốc xịt cắt cơn"
        ],
        "citations": [
            {
                "title": "Asthma and aspirin",
                "url": "https://www.aafa.org/asthma-and-aspirin/",
                "note": "Aspirin and NSAIDs can trigger asthma attacks in 10-20% of adults with asthma."
            }
        ],
    }
]


def rule_to_chunk(rule: Dict[str, Any]) -> Dict[str, Any]:
    ingredients = ", ".join(rule["ingredients_to_avoid_or_check"])
    options = "; ".join(rule["safer_options"])
    red_flags = "; ".join(rule["red_flags"])
    citation_titles = "; ".join(citation["title"] for citation in rule["citations"])
    category_titles = {
        "zinc_supplement": "bổ sung kẽm cần thận trọng",
        "vitamin_c": "vitamin C liều cao cần thận trọng",
        "diarrhea": "tiêu chảy cần ưu tiên bù nước",
        "cough": "ho cần phân loại trước khi chọn thuốc",
        "cold_flu": "thuốc cảm cần thận trọng",
        "pain_cold": "thuốc cảm cần thận trọng",
        "pain_fever": "giảm đau hạ sốt cần thận trọng",
        "pain_inflammation": "giảm đau kháng viêm cần thận trọng",
    }
    if rule["condition"]:
        need_line = f"Nhu cầu: mua thuốc OTC, đặc biệt khi có {rule['symptom_group']}."
    else:
        need_line = f"Nhu cầu: {rule['symptom_group']}."
    title = f"{rule['condition_vi']} - {category_titles.get(rule['otc_category'], 'tư vấn OTC cần thận trọng')}"
    document = (
        f"Hỏi đáp OTC theo bệnh nền\n"
        f"Bệnh nền: {rule['condition_vi']} ({rule['condition']}).\n"
        f"{need_line}\n"
        f"Hoạt chất cần tránh hoặc hỏi dược sĩ/bác sĩ trước: {ingredients}.\n"
        f"Khuyến nghị: {rule['recommendation']}\n"
        f"Lựa chọn thường an toàn hơn để hỏi dược sĩ: {options}.\n"
        f"Dấu hiệu cần đi khám/gọi hỗ trợ y tế: {red_flags}.\n"
        f"Nguồn đối chiếu: {citation_titles}."
    )
    return {
        "id": rule["id"],
        "document": document,
        "metadata": {
            "source": "otc_condition_guardrail",
            "source_url": rule["citations"][0]["url"],
            "title": title,
            "condition": rule["condition"],
            "condition_vi": rule["condition_vi"],
            "otc_category": rule["otc_category"],
            "ingredients": json.dumps(rule["ingredients_to_avoid_or_check"], ensure_ascii=False),
            "section": "condition_otc_safety",
            "type": "condition_guardrail",
            "risk_level": rule["risk_level"],
            "trust_level": "curated_condition_guardrail",
            "requires_review": True,
        },
    }


def write_jsonl(path: Path, rows: Iterable[Dict[str, Any]]) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    count = 0
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
            count += 1
    return count


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--rules-output", default="data/processed/otc_condition_guardrails.jsonl")
    parser.add_argument("--chunks-output", default="data/chunks/otc_condition_guardrail_chunks.jsonl")
    parser.add_argument("--manifest", default="data/processed/otc_condition_guardrails_manifest.json")
    args = parser.parse_args()

    rule_count = write_jsonl(Path(args.rules_output), RULES)
    chunk_count = write_jsonl(Path(args.chunks_output), (rule_to_chunk(rule) for rule in RULES))
    manifest = {
        "rules_output": args.rules_output,
        "chunks_output": args.chunks_output,
        "rule_count": rule_count,
        "chunk_count": chunk_count,
        "scope": "Initial curated OTC guardrails for condition-aware public medication advice.",
    }
    Path(args.manifest).write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(manifest, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
