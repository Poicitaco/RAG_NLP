"""Optional LLM-backed intent planner for agent routing.

The planner is not allowed to answer medical questions. It only extracts
routing hints: intent, subject, missing context, retrieval focus, and agents.
Hard safety rules and evidence guardrails remain authoritative.
"""
from __future__ import annotations

import json
import re
import unicodedata
from typing import Any, Dict, List, Optional

import httpx

from backend.config.settings import settings


ALLOWED_INTENTS = {
    "drug_info",
    "otc_recommendation",
    "dosage",
    "interaction",
    "recall",
    "counterfeit",
    "high_risk_context",
    "pediatric_symptom",
    "emergency",
    "general_safety",
}


def normalize_text(text: str) -> str:
    value = (text or "").replace("Đ", "D").replace("đ", "d").lower()
    decomposed = unicodedata.normalize("NFD", value)
    stripped = "".join(ch for ch in decomposed if unicodedata.category(ch) != "Mn")
    return re.sub(r"\s+", " ", stripped).strip()


def contains_any(text: str, terms: List[str]) -> bool:
    normalized = normalize_text(text)
    return any(term in normalized for term in terms)


class LLMIntentPlanner:
    """LLM/fallback planner that decides what the pipeline should focus on."""

    def __init__(self) -> None:
        self.enabled = bool(settings.USE_LLM_PLANNER)
        self.provider = settings.LLM_PROVIDER.lower()
        self.model = settings.LLM_PLANNER_MODEL or settings.LLM_MODEL
        self.timeout = settings.LLM_TIMEOUT_SECONDS

    def is_available(self) -> bool:
        return self.enabled and self.provider == "gemini" and bool(settings.GEMINI_API_KEY)

    async def plan(
        self,
        question: str,
        fallback_intent: str,
        fallback_subtype: str = "",
    ) -> Dict[str, Any]:
        fallback = self._fallback_plan(question, fallback_intent, fallback_subtype)
        if not self.is_available():
            return fallback
        try:
            llm_plan = await self._gemini_plan(question, fallback_intent, fallback_subtype)
            return self._validated_plan(llm_plan, fallback)
        except Exception as exc:
            fallback["planner_error"] = exc.__class__.__name__
            return fallback

    def _fallback_plan(self, question: str, fallback_intent: str, fallback_subtype: str) -> Dict[str, Any]:
        normalized = normalize_text(question)
        is_child = contains_any(
            normalized,
            [
                "be",
                "tre",
                "con toi",
                "con trai toi",
                "con gai toi",
                "con tui",
                "con trai tui",
                "con gai tui",
                "chau toi",
                "chau tui",
                "nhoc",
                "so sinh",
            ],
        ) or bool(re.search(r"\b(?:[0-9]{1,2})\s*tuoi\b", normalized) and contains_any(normalized, ["sot", "ho", "tieu chay", "dau"]))
        fever = contains_any(normalized, ["sot", "ha sot", "nong dau"])
        buying_otc = contains_any(normalized, ["mua thuoc", "thuoc gi", "nen uong", "ha sot", "thuoc cam", "thuoc ho"])
        interaction = contains_any(normalized, ["uong chung", "dung chung", "tuong tac", "ket hop"])

        intent = fallback_intent if fallback_intent in ALLOWED_INTENTS else "drug_info"
        if is_child and (fever or buying_otc):
            intent = "pediatric_symptom"
        elif interaction:
            intent = "interaction"
        elif buying_otc:
            intent = "otc_recommendation"

        missing_focus: List[str] = []
        if intent == "pediatric_symptom":
            missing_focus.extend(["age_or_age_months", "weight_kg", "temperature", "red_flags"])
        elif intent in {"otc_recommendation", "dosage", "high_risk_context"}:
            missing_focus.extend(["age", "conditions", "current_medications", "allergies"])

        agents = ["safety_router"]
        if missing_focus:
            agents.append("patient_context_collector")
        if interaction:
            agents.append("graph_safety_agent")
        if intent in {"drug_info", "otc_recommendation", "dosage", "general_safety", "pediatric_symptom"}:
            agents.extend(["semantic_rule_mapper_agent", "retrieval_agent"])
        agents.append("evidence_guardrail_agent")

        return {
            "used": False,
            "provider": "deterministic_fallback",
            "intent": intent,
            "subtype": fallback_subtype,
            "subject": "child" if is_child else "unknown",
            "is_pediatric": is_child,
            "missing_context_focus": list(dict.fromkeys(missing_focus)),
            "retrieval_focus": "pediatric fever/OTC safety" if intent == "pediatric_symptom" else "",
            "agents": list(dict.fromkeys(agents)),
            "safety_notes": [],
            "confidence": 0.55,
        }

    async def _gemini_plan(self, question: str, fallback_intent: str, fallback_subtype: str) -> Dict[str, Any]:
        system_prompt = (
            "You are an intent planner for a Vietnamese medication-safety RAG system. "
            "You must NOT answer the medical question and must NOT recommend medicine or dose. "
            "Return only valid JSON. Your task is to identify intent, subject, missing context, "
            "retrieval focus, safety notes, and agents to call. Hard safety rules and evidence "
            "guardrails will decide the final answer."
        )
        user_payload = {
            "question": question,
            "fallback_intent": fallback_intent,
            "fallback_subtype": fallback_subtype,
            "allowed_intents": sorted(ALLOWED_INTENTS),
            "schema": {
                "intent": "one allowed intent",
                "subject": "self|child|pregnant_or_breastfeeding|elderly|unknown",
                "is_pediatric": "boolean",
                "missing_context_focus": "array of context keys to ask next",
                "retrieval_focus": "short Vietnamese or English search focus",
                "agents": "array of agent names",
                "safety_notes": "array of red flags or constraints",
                "confidence": "number 0..1",
            },
        }
        text = await self._gemini_generate(system_prompt, json.dumps(user_payload, ensure_ascii=False))
        if not text:
            return {}
        match = re.search(r"\{.*\}", text, re.DOTALL)
        return json.loads(match.group(0) if match else text)

    def _validated_plan(self, plan: Dict[str, Any], fallback: Dict[str, Any]) -> Dict[str, Any]:
        if not isinstance(plan, dict):
            return fallback
        intent = str(plan.get("intent") or fallback["intent"])
        if intent not in ALLOWED_INTENTS:
            intent = fallback["intent"]
        confidence = plan.get("confidence", fallback["confidence"])
        try:
            confidence = max(0.0, min(1.0, float(confidence)))
        except (TypeError, ValueError):
            confidence = fallback["confidence"]

        merged = dict(fallback)
        merged.update(
            {
                "used": True,
                "provider": self.provider,
                "intent": intent,
                "subject": str(plan.get("subject") or fallback["subject"]),
                "is_pediatric": bool(plan.get("is_pediatric", fallback["is_pediatric"])),
                "missing_context_focus": self._string_list(plan.get("missing_context_focus"))
                or fallback["missing_context_focus"],
                "retrieval_focus": str(plan.get("retrieval_focus") or fallback["retrieval_focus"]),
                "agents": self._string_list(plan.get("agents")) or fallback["agents"],
                "safety_notes": self._string_list(plan.get("safety_notes")),
                "confidence": confidence,
            }
        )
        if merged["is_pediatric"] and intent not in {"emergency", "pediatric_symptom"}:
            merged["intent"] = "pediatric_symptom"
        return merged

    @staticmethod
    def _string_list(value: Any) -> List[str]:
        if not isinstance(value, list):
            return []
        return [str(item) for item in value if str(item).strip()]

    async def _gemini_generate(self, system_prompt: str, user_payload: str) -> Optional[str]:
        url = (
            f"{settings.GEMINI_BASE_URL.rstrip('/')}/v1beta/models/"
            f"{self.model}:generateContent"
        )
        body = {
            "system_instruction": {"parts": [{"text": system_prompt}]},
            "contents": [{"role": "user", "parts": [{"text": user_payload}]}],
            "generationConfig": {
                "temperature": 0.0,
                "maxOutputTokens": 600,
                "responseMimeType": "application/json",
            },
        }
        headers = {
            "x-goog-api-key": settings.GEMINI_API_KEY,
            "Content-Type": "application/json",
        }
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(url, headers=headers, json=body)
            response.raise_for_status()
            data = response.json()
        parts = (((data.get("candidates") or [{}])[0].get("content") or {}).get("parts") or [])
        text = "\n".join(part.get("text") or "" for part in parts).strip()
        return text or None
