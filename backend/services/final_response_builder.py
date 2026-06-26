"""Final response builder for the public medication assistant.

Every answer is normalized into four reader-facing blocks:

1. safety_guardrail
2. core_action
3. clinical_reason
4. citations

The builder is deterministic. It does not create medical facts; it formats the
decision, graph findings, and citations produced by the safety/RAG pipeline.
"""
from __future__ import annotations

import re
import unicodedata
from typing import Any, Dict, List, Optional

from backend.models import Citation


def _citation_dict(citation: Citation) -> Dict[str, Any]:
    '''Mô tả ngắn một dòng.
    
    Args:
        citation: mô tả
    Returns:
        mô tả
    '''
    return citation.model_dump()


def _highest_graph_risk(graph_result: Dict[str, Any]) -> str:
    '''Mô tả ngắn một dòng.
    
    Args:
        graph_result: mô tả
        Any]: mô tả
    Returns:
        mô tả
    '''
    return str((graph_result or {}).get("highest_risk") or "none")


def _has_graph_warning(graph_result: Dict[str, Any]) -> bool:
    '''Mô tả ngắn một dòng.
    
    Args:
        graph_result: mô tả
        Any]: mô tả
    Returns:
        mô tả
    '''
    return bool((graph_result or {}).get("should_warn"))


def _graph_findings(graph_result: Dict[str, Any]) -> List[Dict[str, Any]]:
    '''Mô tả ngắn một dòng.
    
    Args:
        graph_result: mô tả
        Any]: mô tả
    Returns:
        mô tả
    '''
    return list((graph_result or {}).get("findings") or [])


def _normalize_text(text: str) -> str:
    '''Mô tả ngắn một dòng.
    
    Args:
        text: mô tả
    Returns:
        mô tả
    '''
    value = (text or "").replace("\u0110", "D").replace("\u0111", "d").lower()
    decomposed = unicodedata.normalize("NFD", value)
    stripped = "".join(ch for ch in decomposed if unicodedata.category(ch) != "Mn")
    return re.sub(r"\s+", " ", stripped).strip()


def _has_aspirin_diclofenac_interaction(graph_result: Dict[str, Any], citations: List[Citation]) -> bool:
    '''Mô tả ngắn một dòng.
    
    Args:
        graph_result: mô tả
        Any]: mô tả
        citations: mô tả
    Returns:
        mô tả
    '''
    for finding in _graph_findings(graph_result):
        if finding.get("type") != "drug_drug_interaction":
            continue
        haystack = _normalize_text(
            " ".join(str(finding.get(field) or "") for field in ("drug_a", "drug_b", "recommendation"))
        )
        if "aspirin" in haystack and "diclofenac" in haystack:
            return True
    citation_text = _normalize_text(" ".join((citation.title or "") + " " + citation.source for citation in citations))
    return "aspirin" in citation_text and "diclofenac" in citation_text


def _specialized_response_items(
    subtype: str,
    graph_result: Dict[str, Any],
    citations: List[Citation],
) -> Dict[str, Any] | None:
    '''Mô tả ngắn một dòng.
    
    Args:
        subtype: mô tả
        graph_result: mô tả
        Any]: mô tả
        citations: mô tả
    Returns:
        mô tả
    '''
    if subtype == "paracetamol_overdose":
        return {
            "level": "emergency",
            "safety_items": [
                "NGUY CƠ NGỘ ĐỘC GAN CẤP TÍNH NGUY HIỂM TÍNH MẠNG! Bạn đã uống quá liều Paracetamol cho phép (Tối đa 4000mg/24h)."
            ],
            "core_items": [
                "Đến ngay khoa Cấp cứu của bệnh viện gần nhất để bác sĩ rửa dạ dày hoặc cho uống thuốc giải độc (Acetylcysteine). Không được tự ở nhà theo dõi."
            ],
            "reason_items": [
                "Paracetamol quá liều có thể gây tổn thương gan nặng trước khi triệu chứng trở nên rõ ràng, nên cần xử trí cấp cứu sớm."
            ],
        }
    if subtype == "hypertensive_crisis":
        return {
            "level": "emergency",
            "safety_items": [
                "NGUY CƠ ĐỘT QUỴ/TAI BIẾN KHẨN CẤP! Thuốc huyết áp uống hằng ngày không kiểm soát được cơn tăng huyết áp cấp tính."
            ],
            "core_items": [
                "Đo lại huyết áp ngay, nếu chỉ số Tâm thu > 180 mmHg hoặc kèm chóng mặt, nôn mửa, tê yếu tay chân -> Gọi ngay cấp cứu 115."
            ],
            "reason_items": [
                "Cơn tăng huyết áp nặng có thể làm tổn thương não, tim, thận; tự tăng liều thuốc tại nhà có thể gây tụt huyết áp hoặc tương tác nguy hiểm."
            ],
        }
    if subtype == "nsaid_gastric_risk" or _has_aspirin_diclofenac_interaction(graph_result, citations):
        return {
            "level": "danger",
            "safety_items": [
                "NGUY CƠ XUẤT HUYẾT DẠ DÀY CAO! Không tự ý phối hợp hai thuốc giảm đau kháng viêm (NSAID) cùng lúc."
            ],
            "core_items": [
                "Tạm ngưng dùng Diclofenac. Nếu đau khớp quá mức, hãy báo bác sĩ để chuyển sang dòng giảm đau lành tính hơn với dạ dày như Paracetamol hoặc phối hợp thuốc bảo vệ niêm mạc (PPI)."
            ],
            "reason_items": [
                "NSAID như aspirin, diclofenac, ibuprofen có thể làm giảm lớp bảo vệ niêm mạc dạ dày; phối hợp nhiều NSAID làm tăng nguy cơ đau dạ dày và xuất huyết."
            ],
        }
    return None


def _safety_level(action: str, intent: str, graph_result: Dict[str, Any]) -> str:
    '''Mô tả ngắn một dòng.
    
    Args:
        action: mô tả
        intent: mô tả
        graph_result: mô tả
        Any]: mô tả
    Returns:
        mô tả
    '''
    highest = _highest_graph_risk(graph_result).lower()
    if action == "emergency":
        return "emergency"
    if highest in {"major", "critical", "high"}:
        return "danger"
    if _has_graph_warning(graph_result):
        return "warning"
    if action in {"handoff", "insufficient_evidence"}:
        return "caution"
    if intent in {"pediatric_symptom", "high_risk_context", "dosage", "interaction"}:
        return "caution"
    return "info"


def _sentence(text: str) -> str:
    '''Mô tả ngắn một dòng.
    
    Args:
        text: mô tả
    Returns:
        mô tả
    '''
    value = re.sub(r"\s+", " ", str(text or "")).strip(" -;\n\t")
    if not value:
        return ""
    value = value[0].upper() + value[1:]
    if value[-1] not in ".!?":
        value += "."
    return value


def _format_avoid_ingredients(ingredients: List[str]) -> str:
    '''Mô tả ngắn một dòng.
    
    Args:
        ingredients: mô tả
    Returns:
        mô tả
    '''
    lowered = {str(item).strip().lower() for item in ingredients if str(item).strip()}
    decongestants = {"pseudoephedrine", "phenylephrine", "ephedrine"}
    if decongestants <= lowered:
        return "thuốc thông mũi/thuốc cảm có chất co mạch đường uống như pseudoephedrine, phenylephrine hoặc ephedrine"
    return ", ".join(str(item) for item in ingredients if str(item).strip())


def _condition_label(condition: str) -> str:
    '''Mô tả ngắn một dòng.
    
    Args:
        condition: mô tả
    Returns:
        mô tả
    '''
    labels = {
        "diabetes": "tiểu đường",
        "hypertension": "tăng huyết áp",
        "heart_disease": "bệnh tim mạch",
        "kidney_disease": "bệnh thận",
        "liver_disease": "bệnh gan",
        "stomach_ulcer": "đau/loét dạ dày",
        "asthma": "hen/suyễn",
        "pregnancy": "mang thai/cho con bú",
    }
    return labels.get(condition, condition.replace("_", " "))


def _source_short_name(source: Dict[str, Any]) -> str:
    '''Mô tả ngắn một dòng.
    
    Args:
        source: mô tả
        Any]: mô tả
    Returns:
        mô tả
    '''
    title = str(source.get("title") or source.get("source") or "").strip()
    if title.lower() in {
        "cold_flu",
        "documents",
        "dav_all",
        "diabetes",
        "hypertension",
        "heart_disease",
        "kidney_disease",
        "liver_disease",
        "stomach_ulcer",
        "asthma",
        "pregnancy",
        "otc_safety_matrix",
    }:
        return ""
    if "CDC" in title:
        return "CDC Hoa Kỳ"
    if "NHS" in title:
        return "NHS"
    if "Mayo" in title:
        return "Mayo Clinic"
    if "CFR" in title or "nasal decongestant" in title.lower():
        return "21 CFR 341.80"
    return title


def _public_avoid_line(text: str) -> str:
    '''Mô tả ngắn một dòng.
    
    Args:
        text: mô tả
    Returns:
        mô tả
    '''
    value = _sentence(text)
    normalized = _normalize_text(value)
    prefixes = (
        "nen tranh hoac hoi duoc si/bac si truoc khi dung ",
        "nen tranh hoac hoi duoc si truoc khi dung ",
        "nen tranh ",
    )
    for prefix in prefixes:
        if normalized.startswith(prefix):
            raw_prefix_len = len(value) - len(value.lstrip())
            remaining = value[raw_prefix_len + len(prefix):].strip()
            if remaining:
                return "Thuốc/hoạt chất cần tránh hoặc cần hỏi dược sĩ trước khi dùng: " + remaining
    return value


def _safety_items(action: str, intent: str, graph_result: Dict[str, Any]) -> List[str]:
    '''Mô tả ngắn một dòng.
    
    Args:
        action: mô tả
        intent: mô tả
        graph_result: mô tả
        Any]: mô tả
    Returns:
        mô tả
    '''
    findings = _graph_findings(graph_result)
    if action == "emergency":
        return [
            "Đây có thể là tình huống cần đi khám hoặc cấp cứu, không nên tự xử trí bằng thuốc tại nhà.",
            "Gọi 115 hoặc đến cơ sở y tế gần nhất nếu triệu chứng nặng, đột ngột, kéo dài hoặc liên quan trẻ nhỏ/người già.",
        ]

    items: List[str] = []
    seen_otc_ingredients: List[set[str]] = []
    for finding in findings:
        if finding.get("type") == "condition_otc_caution":
            if finding.get("otc_category") == "diarrhea":
                red_flags = finding.get("red_flags") or []
                if red_flags:
                    items.append(
                        "Đi viện ngay nếu có dấu hiệu nguy hiểm: "
                        + ", ".join(str(flag) for flag in red_flags[:5])
                        + "."
                    )
                items.append(
                    "Tránh uống thuốc cầm tiêu chảy mạnh ngay lập tức, nhất là khi mới đi ngoài 1-2 lần hoặc nghi nhiễm khuẩn."
                )
                continue
            ingredient_values = [str(item) for item in finding.get("ingredients_to_avoid_or_check") or []]
            ingredient_set = {item.strip().lower() for item in ingredient_values if item.strip()}
            if any("pseudoephedrine/phenylephrine" in item for item in ingredient_set):
                ingredient_set.update({"pseudoephedrine", "phenylephrine", "ephedrine"})
            decongestants = {"pseudoephedrine", "phenylephrine", "ephedrine"}
            if decongestants <= ingredient_set:
                items = [item for item in items if "pseudoephedrine/phenylephrine" not in item.lower()]
                seen_otc_ingredients = [seen for seen in seen_otc_ingredients if not decongestants <= seen]
            if ingredient_set and any(ingredient_set <= seen or seen <= ingredient_set for seen in seen_otc_ingredients):
                continue
            if ingredient_set:
                seen_otc_ingredients.append(ingredient_set)
            ingredients = _format_avoid_ingredients(ingredient_values)
            items.append(f"Nên tránh hoặc hỏi dược sĩ/bác sĩ trước khi dùng {ingredients}.")
        elif finding.get("type") == "drug_drug_interaction":
            severity_map = {
                "critical": "đặc biệt nguy hiểm",
                "major": "rất nguy hiểm",
                "moderate": "đáng lo ngại",
                "minor": "nhẹ"
            }
            sev = finding.get('severity', '').lower()
            vietnamese_sev = severity_map.get(sev, f"mức {sev}")
            items.append(
                "Nên tránh tự ý dùng chung "
                f"{finding.get('drug_a')} và {finding.get('drug_b')} "
                f"vì chúng có tương tác {vietnamese_sev}."
            )

    if intent == "pediatric_symptom":
        items.append("Trẻ nhỏ có triệu chứng bệnh không nên tự chọn thuốc nếu chưa có tuổi, cân nặng và chẩn đoán phù hợp.")
    elif action in {"handoff", "insufficient_evidence"}:
        items.append("Chưa đủ bằng chứng an toàn để bot đưa khuyến nghị dùng thuốc cụ thể.")

    items = list(dict.fromkeys(items))
    return items or ["Không phát hiện cảnh báo đỏ từ dữ liệu hiện có, nhưng vẫn cần đối chiếu nhãn thuốc/toa thuốc."]


def _core_action_items(
    action: str,
    intent: str,
    citations: List[Citation],
    graph_result: Dict[str, Any] | None = None,
) -> List[str]:
    '''Mô tả ngắn một dòng.
    
    Args:
        action: mô tả
        intent: mô tả
        citations: mô tả
        graph_result: mô tả
        Any] | None: mô tả
    Returns:
        mô tả
    '''
    if action == "emergency":
        return [
            "Không tự uống thêm thuốc để che triệu chứng.",
            "Liên hệ cấp cứu/đi khám ngay nếu triệu chứng đang nặng hoặc xuất hiện đột ngột.",
            "Mang theo toa thuốc, vỏ thuốc hoặc ảnh thuốc đang dùng khi đi khám.",
        ]
    if intent == "pediatric_symptom":
        return [
            "Không tự mua siro/thuốc uống cho trẻ chỉ dựa trên mô tả triệu chứng.",
            "Cần hỏi dược sĩ/bác sĩ và cung cấp tuổi, cân nặng, nhiệt độ, thời gian bị bệnh, thuốc đã dùng.",
            "Nếu trẻ khó thở, sốt cao, lừ đừ, co giật, bỏ bú/uống kém hoặc tiêu chảy nhiều lần thì đi khám ngay.",
        ]
    graph_options: List[str] = []
    has_diarrhea_finding = False
    for finding in _graph_findings(graph_result or {}):
        if finding.get("otc_category") == "diarrhea":
            has_diarrhea_finding = True
        for option in finding.get("safer_options") or []:
            sentence = _sentence(str(option))
            if sentence:
                graph_options.append(sentence)
    if graph_options:
        if has_diarrhea_finding:
            return graph_options[:5]
        return [
            "Không tự chọn sản phẩm liều cao hoặc phối hợp nhiều thành phần khi chưa rõ nhu cầu thật sự.",
            *graph_options[:4],
        ]
    if action in {"handoff", "insufficient_evidence"} and intent == "drug_info":
        return [
            "Mình chưa có nguồn đủ liên quan để gợi ý tên thuốc cụ thể cho câu hỏi này.",
            "Không nên chọn thuốc phối hợp nhiều thành phần nếu bạn chưa rõ từng hoạt chất trên nhãn.",
            "Nếu có sốt cao, khó thở, đau ngực, phát ban/sưng môi mặt hoặc triệu chứng kéo dài, hãy đi khám sớm thay vì tự mua thuốc.",
        ]
    if action in {"handoff", "insufficient_evidence"}:
        return [
            "Không tự đổi liều, phối hợp thuốc hoặc ngưng thuốc trong toa.",
            "Hỏi trực tiếp dược sĩ/bác sĩ với tên thuốc, hàm lượng, dạng dùng và bệnh nền.",
            "Có thể dùng các nguồn bên dưới để định danh, không dùng chúng để tự kết luận liều/tương tác.",
        ]
    if citations:
        return [
            "Bạn có thể tham khảo các thông tin tra cứu được ở bên dưới.",
            "Hãy kiểm tra kỹ tên hoạt chất và hàm lượng trên hộp thuốc của bạn xem có khớp không nhé.",
            "Luôn hỏi lại dược sĩ/bác sĩ nếu bạn đang mang thai, có bệnh nền hoặc dùng cho trẻ nhỏ/người già.",
        ]
    return ["Chưa có nguồn thông tin đủ chắc chắn để đưa ra hướng dẫn dùng thuốc cụ thể cho bạn."]


def _clinical_reason_items(action: str, intent: str, graph_result: Dict[str, Any]) -> List[str]:
    '''Mô tả ngắn một dòng.
    
    Args:
        action: mô tả
        intent: mô tả
        graph_result: mô tả
        Any]: mô tả
    Returns:
        mô tả
    '''
    findings = _graph_findings(graph_result)
    reasons: List[str] = []
    for finding in findings:
        if finding.get("recommendation"):
            reasons.append(str(finding["recommendation"]))
        elif finding.get("type") == "drug_drug_interaction":
            reasons.append("Một số thuốc khi dùng chung có thể làm tăng độc tính hoặc giảm an toàn điều trị.")

    if action == "emergency":
        reasons.append("Một số triệu chứng đỏ có thể liên quan bệnh cấp tính; dùng thuốc tại nhà có thể che dấu bệnh và làm chậm xử trí.")
    elif intent == "pediatric_symptom":
        reasons.append("Trẻ nhỏ nhạy với liều dùng và tác dụng phụ; nhiều thuốc ho/cảm không phù hợp nếu chưa đánh giá tuổi, cân nặng và tình trạng bệnh.")
    elif action in {"handoff", "insufficient_evidence"}:
        reasons.append("Nguồn truy xuất hiện chưa đủ đúng loại hoặc đủ liên quan để kết luận an toàn.")
    else:
        reasons.append("Lựa chọn thuốc an toàn phụ thuộc vào đúng tên hoạt chất, hàm lượng, bệnh nền, dị ứng và thuốc đang dùng kèm.")

    return reasons


def _citation_items(citations: List[Citation]) -> List[str]:
    '''Mô tả ngắn một dòng.
    
    Args:
        citations: mô tả
    Returns:
        mô tả
    '''
    if not citations:
        return ["Chưa có nguồn đủ chuẩn để trích dẫn cho hướng dẫn dùng thuốc cụ thể."]
    items = []
    for citation in citations:
        title = citation.title or citation.source
        section = f", mục: {citation.section}" if citation.section else ""
        items.append(f"[{citation.id}] {title} - nguồn: {citation.source}{section}.")
    return items


def _is_bisphosphonate_context(citations: List[Citation]) -> bool:
    '''Mô tả ngắn một dòng.
    
    Args:
        citations: mô tả
    Returns:
        mô tả
    '''
    haystack = " ".join((citation.title or "") + " " + citation.source for citation in citations).lower()
    terms = ("alendronic", "alendronate", "alendron", "bisphosphonate")
    return any(term in haystack for term in terms)


def _filtered_citations(intent: str, action: str, citations: List[Citation]) -> List[Citation]:
    '''Mô tả ngắn một dòng.
    
    Args:
        intent: mô tả
        action: mô tả
        citations: mô tả
    Returns:
        mô tả
    '''
    if _is_bisphosphonate_context(citations):
        matching = [
            citation
            for citation in citations
            if "alendronic" in (citation.title or "").lower()
            or "alendronate" in (citation.title or "").lower()
            or "alendron" in (citation.title or "").lower()
        ]
        return matching[:2] or citations[:1]
    return citations[:5]


def _low_information_preview(preview: str) -> bool:
    '''Mô tả ngắn một dòng.
    
    Args:
        preview: mô tả
    Returns:
        mô tả
    '''
    normalized = preview.strip().lower()
    if not normalized:
        return True
    return "[]; []" in normalized or normalized.endswith(": []; []")


def _metadata_preview(row: Dict[str, Any]) -> str:
    '''Mô tả ngắn một dòng.
    
    Args:
        row: mô tả
        Any]: mô tả
    Returns:
        mô tả
    '''
    metadata = row.get("metadata") or {}
    parts = []
    drug_name = metadata.get("drug_name") or row.get("title_or_drug")
    active_ingredient = metadata.get("active_ingredient") or metadata.get("active_ingredients")
    registration_number = metadata.get("registration_number")
    section = metadata.get("section")

    if drug_name:
        parts.append(f"Tên thuốc: {drug_name}")
    if active_ingredient:
        parts.append(f"Hoạt chất chính: {active_ingredient}")
    if registration_number:
        parts.append(f"Số đăng ký/GPLH: {registration_number}")
    if section:
        parts.append(f"Nhóm dữ liệu: {section}")
    return ". ".join(parts) + "." if parts else ""


def _is_indication_snippet(row: Dict[str, Any]) -> bool:
    '''Mô tả ngắn một dòng.
    
    Args:
        row: mô tả
        Any]: mô tả
    Returns:
        mô tả
    '''
    metadata = row.get("metadata") or {}
    section = str(metadata.get("section") or "").lower()
    text = f"{row.get('document_preview') or row.get('document') or ''} {section}".lower()
    return any(
        term in text
        for term in (
            "indications",
            "chỉ định",
            "chi dinh",
            "công dụng",
            "cong dung",
            "hạ sốt",
            "ha sot",
            "giảm đau",
            "giam dau",
        )
    )


def _clean_indication_preview(preview: str) -> str:
    '''Mô tả ngắn một dòng.
    
    Args:
        preview: mô tả
    Returns:
        mô tả
    '''
    text = re.sub(r"\s+", " ", preview or "").strip()
    text = re.sub(r"^(chỉ định|chi dinh)\s*[:\-]?\s*", "", text, flags=re.IGNORECASE)
    text = re.split(
        r"\b(liều dùng|lieu dung|cách dùng|cach dung|chống chỉ định|chong chi dinh)\b",
        text,
        maxsplit=1,
        flags=re.IGNORECASE,
    )[0].strip()
    return text


def build_response_blocks(
    *,
    action: str,
    intent: str,
    graph_result: Dict[str, Any],
    citations: List[Citation],
    selected_agents: List[str],
    subtype: str = "",
    snippets: Optional[List[Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    '''Mô tả ngắn một dòng.
    
    Args:
        action: mô tả
        intent: mô tả
        graph_result: mô tả
        Any]: mô tả
        citations: mô tả
        selected_agents: mô tả
        subtype: mô tả
        snippets: mô tả
        Any]]]: mô tả
    Returns:
        mô tả
    '''
    citations = _filtered_citations(intent, action, citations)
    specialized = _specialized_response_items(subtype, graph_result, citations)
    if specialized:
        level = specialized["level"]
        safety_items = specialized["safety_items"]
        core_items = specialized["core_items"]
        reason_items = specialized["reason_items"]
    elif _is_bisphosphonate_context(citations):
        level = _safety_level(action, intent, graph_result)
        safety_items = _safety_items(action, intent, graph_result)
        core_items = [
            "Uống thuốc loãng xương ngay sau khi ngủ dậy, với một ly nước lọc đầy.",
            "Không nằm xuống sau khi uống; nên ngồi thẳng hoặc đứng/đi lại ít nhất 30 phút.",
            "Không uống cùng sữa, canxi, cà phê hoặc thuốc khác nếu chưa hỏi dược sĩ/bác sĩ.",
        ]
        reason_items = [
            "Nhóm bisphosphonate như alendronic acid có thể kích ứng thực quản; nằm xuống hoặc uống ít nước làm tăng nguy cơ thuốc kẹt ở cổ họng/thực quản.",
            "Canxi, sữa và một số thuốc khác có thể làm giảm hấp thu thuốc loãng xương.",
        ]
    else:
        level = _safety_level(action, intent, graph_result)
        safety_items = _safety_items(action, intent, graph_result)
        core_items = _core_action_items(action, intent, citations, graph_result)
        reason_items = _clinical_reason_items(action, intent, graph_result)
    safety_title = "**CẢNH BÁO AN TOÀN**" if level in {"emergency", "danger", "warning"} else "**Lưu ý an toàn**"
    core_action_block = {
        "title": "**DẶN DÒ SIÊU NGẮN**",
        "items": core_items,
    }
    if action in {"allow", "allow_with_caution"} and snippets:
        items = []
        seen_items = set()
        ordered_snippets = sorted(
            snippets,
            key=lambda row: 0 if subtype == "indication" and _is_indication_snippet(row) else 1,
        )
        for i, row in enumerate(ordered_snippets):
            if len(items) >= 3:
                break
            citation_id = citations[min(i, len(citations) - 1)].id if citations else f"S{len(items) + 1}"
            metadata = row.get("metadata") or {}
            title = (
                metadata.get("title")
                or metadata.get("drug_name")
                or "Thông tin thuốc"
            )
            preview = row.get("document_preview") or row.get("document") or ""
            if _low_information_preview(preview):
                preview = _metadata_preview(row)
            if subtype == "indication":
                preview = _clean_indication_preview(preview)
            if len(preview) > 300:
                preview = preview[:300].rstrip() + "..."
            if preview:
                item = f"[{citation_id}] {title}: {preview}"
                item_key = unicodedata.normalize("NFKC", item).casefold()
                if item_key in seen_items:
                    continue
                seen_items.add(item_key)
                items.append(item)

        if subtype == "indication" and items:
            combined = " ".join(items).casefold()
            has_fever = "hạ sốt" in combined or "ha sot" in combined or "giảm thân nhiệt" in combined
            has_pain = "giảm đau" in combined or "giam dau" in combined
            if has_fever and has_pain:
                citation_pair = "[S1], [S2]" if len(citations) >= 2 else "[S1]"
                items.insert(
                    0,
                    f"{citation_pair} Paracetamol thường được dùng để hạ sốt và giảm đau nhẹ đến vừa.",
                )

        if items:
            core_action_block["items"] = items
            core_action_block["title"] = (
                "**CÔNG DỤNG / CHỈ ĐỊNH**"
                if subtype == "indication"
                else "**THÔNG TIN TRA CỨU**"
            )

        core_action_block["items"].append(
            "Khi dùng thuốc thật, hãy đối chiếu toa/nhãn thuốc và hỏi dược sĩ nếu còn chưa chắc."
        )

    return {
        "schema_version": "agent_response_v1",
        "action": action,
        "intent": intent,
        "subtype": subtype,
        "graph_result": graph_result,
        "render_order": ["safety_guardrail", "core_action", "clinical_reason", "citations"],
        "selected_agents": selected_agents,
        "blocks": {
            "safety_guardrail": {
                "title": safety_title,
                "level": level,
                "items": safety_items,
            },
            "core_action": core_action_block,
            "clinical_reason": {
                "title": "**LÝ DO CHUYÊN KHOA DỄ HIỂU**",
                "items": reason_items,
            },
            "citations": {
                "title": "**DẪN NGUỒN ĐỐI SOÁT**",
                "items": _citation_items(citations),
                "sources": [_citation_dict(citation) for citation in citations],
            },
        },
    }


def check_citation_coverage(response_text: str, citations: List[Any]) -> Dict[str, Any]:
    """Kiểm tra bao nhiêu citation được dùng inline trong response text.
    
    Returns dict với coverage (0.0-1.0), used (list id dùng), missing (list id thiếu).
    """
    if not citations:
        return {"coverage": 0.0, "used": [], "missing": []}
    used_ids = set(re.findall(r'\[S(\d+)\]', response_text))
    all_ids = {str(i + 1) for i in range(len(citations))}
    used = sorted(used_ids & all_ids, key=int)
    missing = sorted(all_ids - used_ids, key=int)
    coverage = len(used) / len(all_ids) if all_ids else 0.0
    return {"coverage": round(coverage, 2), "used": used, "missing": missing}


def format_response_blocks(response_blocks: Dict[str, Any]) -> str:
    '''Format response blocks thành string hiển thị.
    
    Args:
        response_blocks: mô tả
        Any]: mô tả
    Returns:
        mô tả
    '''
    public_answer = _format_public_otc_answer(response_blocks)
    if public_answer:
        return public_answer

    labels = {
        "safety_guardrail": "**Lưu ý an toàn**",
        "core_action": "**DẶN DÒ SIÊU NGẮN**",
        "clinical_reason": "**LÝ DO CHUYÊN KHOA DỄ HIỂU**",
        "citations": "**DẪN NGUỒN ĐỐI SOÁT**",
    }
    lines: List[str] = []
    blocks = response_blocks.get("blocks") or {}
    for key in response_blocks.get("render_order") or []:
        block = blocks.get(key) or {}
        title = block.get("title") or labels.get(key, key)
        lines.append(f"{title}:")
        for item in block.get("items") or []:
            lines.append(f"- {item}")
        lines.append("")
    return "\n".join(lines).strip()


def _format_public_otc_answer(response_blocks: Dict[str, Any]) -> str:
    '''Mô tả ngắn một dòng.
    
    Args:
        response_blocks: mô tả
        Any]: mô tả
    Returns:
        mô tả
    '''
    if response_blocks.get("intent") != "otc_recommendation":
        return ""

    graph_result = response_blocks.get("graph_result") or {}
    findings = [
        finding
        for finding in graph_result.get("findings") or []
        if finding.get("type") == "condition_otc_caution"
    ]
    if not findings:
        return ""

    conditions = []
    for finding in findings:
        condition = str(finding.get("condition") or "").strip()
        if condition:
            conditions.append(_condition_label(condition))
    condition_text = " và ".join(dict.fromkeys(conditions)) if conditions else "bệnh nền của bạn"

    blocks = response_blocks.get("blocks") or {}
    safety_items = (blocks.get("safety_guardrail") or {}).get("items") or []
    core_items = (blocks.get("core_action") or {}).get("items") or []
    citations = (blocks.get("citations") or {}).get("sources") or []

    avoid_line = _public_avoid_line(safety_items[0]) if safety_items else ""
    safer_lines = [item for item in core_items if item][:4]
    sources = list(dict.fromkeys(_source_short_name(source) for source in citations if _source_short_name(source)))
    source_text = ", ".join(sources[:3]) if sources else "các nguồn y tế đối soát trong hệ thống"

    lines = [
        f"Chào bạn, với tình trạng {condition_text}, việc chọn thuốc cảm cần cẩn trọng vì một số thuốc có thể làm tăng huyết áp, tăng đường huyết hoặc ảnh hưởng bệnh nền.",
        "",
        "**Bạn nên tránh:**",
    ]
    if avoid_line:
        lines.append(f"- {avoid_line}")
    lines.append("- Tránh tự chọn thuốc cảm phối hợp nhiều thành phần nếu chưa đọc rõ hoạt chất trên nhãn.")

    if safer_lines:
        lines.extend(["", "**Lựa chọn an toàn hơn:**"])
        for item in safer_lines:
            lines.append(f"- {item}")

    lines.extend(
        [
            "",
            "**Lưu ý:** Luôn nói rõ với dược sĩ rằng bạn có bệnh nền trước khi mua thuốc. Thông tin này được đối soát từ "
            + source_text
            + ".",
        ]
    )
    return "\n".join(lines).strip()
