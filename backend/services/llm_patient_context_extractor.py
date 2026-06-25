"""Gemini-backed extraction of patient context from a user message."""
from __future__ import annotations

import json
from typing import Any, Dict, Optional

import httpx

from backend.config.settings import settings


class LLMPatientContextExtractor:
    """Extract structured patient context as JSON.

    The extractor is intentionally strict: callers decide how to recover from
    API or parsing failures. PatientContextService.assess_hybrid catches those
    failures and falls back to deterministic keyword extraction.
    """

    EXPECTED_KEYS = {
        "subject",
        "intent",
        "age",
        "age_months",
        "weight_kg",
        "conditions",
        "conditions_confirmed",
        "current_medications",
        "current_medications_confirmed",
        "allergies",
        "allergies_confirmed",
        "pregnant",
        "breastfeeding",
        "pregnancy_breastfeeding_confirmed",
        "red_flags",
        "missing_fields",
        "confidence",
    }

    def __init__(self, api_key: Optional[str] = None, model_name: Optional[str] = None) -> None:
        self.api_key = api_key if api_key is not None else settings.GEMINI_API_KEY
        self.model_name = model_name or settings.GEMINI_MODEL
        self.base_url = settings.GEMINI_BASE_URL.rstrip("/")
        self.timeout = settings.LLM_TIMEOUT_SECONDS

    async def extract(self, message: str) -> Dict[str, Any]:
        if not self.api_key:
            raise RuntimeError("GEMINI_API_KEY is not configured")

        payload = {
            "contents": [
                {
                    "role": "user",
                    "parts": [{"text": self._build_prompt(message)}],
                }
            ],
            "generationConfig": {
                "temperature": 0,
                "responseMimeType": "application/json",
            },
        }
        url = f"{self.base_url}/v1beta/models/{self.model_name}:generateContent"
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(
                url,
                params={"key": self.api_key},
                json=payload,
            )
            response.raise_for_status()
        data = response.json()
        text = self._extract_text(data)
        parsed = json.loads(text)
        if not isinstance(parsed, dict):
            raise ValueError("Gemini patient context response must be a JSON object")
        return self._normalize_result(parsed)

    def _build_prompt(self, message: str) -> str:
        schema = {
            "subject": None,
            "intent": None,
            "age": None,
            "age_months": None,
            "weight_kg": None,
            "conditions": [],
            "conditions_confirmed": None,
            "current_medications": [],
            "current_medications_confirmed": None,
            "allergies": [],
            "allergies_confirmed": None,
            "pregnant": None,
            "breastfeeding": None,
            "pregnancy_breastfeeding_confirmed": None,
            "red_flags": [],
            "missing_fields": [],
            "confidence": 0.0,
        }
        return (
            "Extract patient context from the Vietnamese medication-safety message. "
            "Return only valid JSON, no markdown, no explanation. Use null when a field is unknown. "
            "Use arrays for conditions, current_medications, allergies, red_flags, and missing_fields. "
            "Do not infer safety-critical facts unless explicitly stated. JSON schema:\n"
            f"{json.dumps(schema, ensure_ascii=False, indent=2)}\n\n"
            f"Message: {message}"
        )

    def _extract_text(self, data: Dict[str, Any]) -> str:
        try:
            parts = data["candidates"][0]["content"]["parts"]
            text = "".join(str(part.get("text", "")) for part in parts)
        except (KeyError, IndexError, TypeError) as exc:
            raise ValueError("Gemini response missing content text") from exc
        text = text.strip()
        if text.startswith("```"):
            text = text.strip("`").strip()
            if text.lower().startswith("json"):
                text = text[4:].strip()
        if not text:
            raise ValueError("Gemini response text is empty")
        return text

    def _normalize_result(self, parsed: Dict[str, Any]) -> Dict[str, Any]:
        result = {key: parsed.get(key) for key in self.EXPECTED_KEYS}
        for key in ("conditions", "current_medications", "allergies", "red_flags", "missing_fields"):
            value = result.get(key)
            if value is None:
                result[key] = []
            elif not isinstance(value, list):
                result[key] = [value]
        return result
