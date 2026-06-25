"""Groq-backed extraction of patient context from a user message."""
from __future__ import annotations

import asyncio
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
        self.api_key = api_key if api_key is not None else settings.GROQ_API_KEY
        self.model_name = model_name or "llama-3.1-8b-instant"
        self.base_url = "https://api.groq.com/openai/v1"
        self.timeout = settings.LLM_TIMEOUT_SECONDS

    async def extract(self, message: str) -> Dict[str, Any]:
        if not self.api_key:
            raise RuntimeError("GROQ_API_KEY is not configured")

        payload = {
            "model": self.model_name,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You extract patient context for a Vietnamese medication-safety assistant. "
                        "Return only valid JSON matching the requested schema."
                    ),
                },
                {
                    "role": "user",
                    "content": self._build_prompt(message),
                }
            ],
            "temperature": 0,
            "response_format": {"type": "json_object"},
        }
        url = f"{self.base_url}/chat/completions"
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await self._post_with_retry(client, url, payload)
        data = response.json()
        text = self._extract_text(data)
        parsed = json.loads(text)
        if not isinstance(parsed, dict):
            raise ValueError("Groq patient context response must be a JSON object")
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
            text = str(data["choices"][0]["message"]["content"])
        except (KeyError, IndexError, TypeError) as exc:
            raise ValueError("Groq response missing content text") from exc
        text = text.strip()
        if text.startswith("```"):
            text = text.strip("`").strip()
            if text.lower().startswith("json"):
                text = text[4:].strip()
        if not text:
            raise ValueError("Groq response text is empty")
        return text

    async def _post_with_retry(
        self,
        client: httpx.AsyncClient,
        url: str,
        payload: Dict[str, Any],
    ) -> httpx.Response:
        last_response: Optional[httpx.Response] = None
        for attempt in range(3):
            response = await client.post(
                url,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                json=payload,
            )
            if response.status_code != 429:
                response.raise_for_status()
                return response
            last_response = response
            if attempt < 2:
                await asyncio.sleep(1)
        assert last_response is not None
        last_response.raise_for_status()
        return last_response

    def _normalize_result(self, parsed: Dict[str, Any]) -> Dict[str, Any]:
        result = {key: parsed.get(key) for key in self.EXPECTED_KEYS}
        for key in ("conditions", "current_medications", "allergies", "red_flags", "missing_fields"):
            value = result.get(key)
            if value is None:
                result[key] = []
            elif not isinstance(value, list):
                result[key] = [value]
        return result
