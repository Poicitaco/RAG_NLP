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

from typing import Any, Dict, List

from backend.models import Citation


def _citation_dict(citation: Citation) -> Dict[str, Any]:
    return citation.model_dump()


def _highest_graph_risk(graph_result: Dict[str, Any]) -> str:
    return str((graph_result or {}).get("highest_risk") or "none")


def _has_graph_warning(graph_result: Dict[str, Any]) -> bool:
    return bool((graph_result or {}).get("should_warn"))


def _graph_findings(graph_result: Dict[str, Any]) -> List[Dict[str, Any]]:
    return list((graph_result or {}).get("findings") or [])


def _safety_level(action: str, intent: str, graph_result: Dict[str, Any]) -> str:
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


def _safety_items(action: str, intent: str, graph_result: Dict[str, Any]) -> List[str]:
    findings = _graph_findings(graph_result)
    if action == "emergency":
        return [
            "Đây có thể là tình huống cần đi khám hoặc cấp cứu, không nên tự xử trí bằng thuốc tại nhà.",
            "Gọi 115 hoặc đến cơ sở y tế gần nhất nếu triệu chứng nặng, đột ngột, kéo dài hoặc liên quan trẻ nhỏ/người già.",
        ]

    items: List[str] = []
    for finding in findings:
        if finding.get("type") == "condition_otc_caution":
            ingredients = ", ".join(finding.get("ingredients_to_avoid_or_check") or [])
            items.append(f"Nên tránh hoặc hỏi dược sĩ/bác sĩ trước khi dùng: {ingredients}.")
        elif finding.get("type") == "drug_drug_interaction":
            items.append(
                "Không tự phối hợp "
                f"{finding.get('drug_a')} với {finding.get('drug_b')} "
                f"vì có tương tác mức {finding.get('severity')}."
            )

    if intent == "pediatric_symptom":
        items.append("Trẻ nhỏ có triệu chứng bệnh không nên tự chọn thuốc nếu chưa có tuổi, cân nặng và chẩn đoán phù hợp.")
    elif action in {"handoff", "insufficient_evidence"}:
        items.append("Chưa đủ bằng chứng an toàn để bot đưa khuyến nghị dùng thuốc cụ thể.")

    return items or ["Không phát hiện cảnh báo đỏ từ dữ liệu hiện có, nhưng vẫn cần đối chiếu nhãn thuốc/toa thuốc."]


def _core_action_items(action: str, intent: str, citations: List[Citation]) -> List[str]:
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
    if action in {"handoff", "insufficient_evidence"}:
        return [
            "Không tự đổi liều, phối hợp thuốc hoặc ngưng thuốc trong toa.",
            "Hỏi trực tiếp dược sĩ/bác sĩ với tên thuốc, hàm lượng, dạng dùng và bệnh nền.",
            "Có thể dùng các nguồn bên dưới để định danh, không dùng chúng để tự kết luận liều/tương tác.",
        ]
    if citations:
        return [
            "Chỉ xem đây là thông tin tham khảo dựa trên nguồn truy xuất.",
            "Đối chiếu đúng tên hoạt chất, biệt dược, hàm lượng và dạng dùng trên bao bì/toa thuốc.",
            "Hỏi dược sĩ/bác sĩ nếu đang mang thai, cho con bú, trẻ em, người già, bệnh gan/thận hoặc dùng nhiều thuốc.",
        ]
    return ["Chưa có nguồn đủ chắc để đưa hướng dẫn dùng thuốc cụ thể."]


def _clinical_reason_items(action: str, intent: str, graph_result: Dict[str, Any]) -> List[str]:
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
        reasons.append("Khuyến nghị được giới hạn ở mức thông tin chung vì bot không thay thế bác sĩ/dược sĩ.")

    return reasons


def _citation_items(citations: List[Citation]) -> List[str]:
    if not citations:
        return ["Chưa có nguồn đủ chuẩn để trích dẫn cho hướng dẫn dùng thuốc cụ thể."]
    items = []
    for citation in citations:
        title = citation.title or citation.source
        section = f", mục: {citation.section}" if citation.section else ""
        items.append(f"[{citation.id}] {title} - nguồn: {citation.source}{section}.")
    return items


def _is_bisphosphonate_context(citations: List[Citation]) -> bool:
    haystack = " ".join((citation.title or "") + " " + citation.source for citation in citations).lower()
    terms = ("alendronic", "alendronate", "alendron", "bisphosphonate")
    return any(term in haystack for term in terms)


def _filtered_citations(intent: str, action: str, citations: List[Citation]) -> List[Citation]:
    if action in {"handoff", "insufficient_evidence"}:
        return []
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


def build_response_blocks(
    *,
    action: str,
    intent: str,
    graph_result: Dict[str, Any],
    citations: List[Citation],
    selected_agents: List[str],
) -> Dict[str, Any]:
    citations = _filtered_citations(intent, action, citations)
    level = _safety_level(action, intent, graph_result)
    if _is_bisphosphonate_context(citations):
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
        core_items = _core_action_items(action, intent, citations)
        reason_items = _clinical_reason_items(action, intent, graph_result)
    return {
        "schema_version": "agent_response_v1",
        "render_order": ["safety_guardrail", "core_action", "clinical_reason", "citations"],
        "selected_agents": selected_agents,
        "blocks": {
            "safety_guardrail": {
                "title": "CẢNH BÁO AN TOÀN",
                "level": level,
                "items": _safety_items(action, intent, graph_result),
            },
            "core_action": {
                "title": "DẶN DÒ SIÊU NGẮN",
                "items": core_items,
            },
            "clinical_reason": {
                "title": "LÝ DO CHUYÊN KHOA DỄ HIỂU",
                "items": reason_items,
            },
            "citations": {
                "title": "DẪN NGUỒN ĐỐI SOÁT",
                "items": _citation_items(citations),
                "sources": [_citation_dict(citation) for citation in citations],
            },
        },
    }


def format_response_blocks(response_blocks: Dict[str, Any]) -> str:
    labels = {
        "safety_guardrail": "CẢNH BÁO AN TOÀN",
        "core_action": "DẶN DÒ SIÊU NGẮN",
        "clinical_reason": "LÝ DO CHUYÊN KHOA DỄ HIỂU",
        "citations": "DẪN NGUỒN ĐỐI SOÁT",
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
