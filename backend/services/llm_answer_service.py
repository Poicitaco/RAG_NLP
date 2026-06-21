"""Constrained LLM answer rewriting for Safe RAG responses.

The LLM is optional and never acts as the source of medical truth. It only
rewrites approved graph findings and retrieved citations into clearer language.
"""
from __future__ import annotations

import json
from typing import Any, Dict, List, Optional

import httpx

from backend.config.settings import settings
from backend.models import Citation


class LLMAnswerService:
    """Optional Gemini-backed rewriter with deterministic fallback behavior."""

    def __init__(self) -> None:
        self.enabled = bool(settings.USE_LLM_ANSWER)
        self.provider = settings.LLM_PROVIDER.lower()
        self.model = settings.LLM_MODEL
        self.timeout = settings.LLM_TIMEOUT_SECONDS

    def is_available(self) -> bool:
        if not self.enabled:
            return False
        if self.provider == "gemini":
            return bool(settings.GEMINI_API_KEY)
        return False

    async def rewrite(
        self,
        question: str,
        deterministic_answer: str,
        graph_safety: Dict[str, Any],
        snippets: List[Dict[str, Any]],
        citations: List[Citation],
    ) -> Optional[str]:
        if not self.is_available():
            return None
        if self.provider != "gemini":
            return None

        prompt = self._build_prompt(
            question=question,
            deterministic_answer=deterministic_answer,
            graph_safety=graph_safety,
            snippets=snippets,
            citations=citations,
        )
        try:
            return await self._gemini_generate(prompt)
        except Exception:
            return None

    def _build_prompt(
        self,
        question: str,
        deterministic_answer: str,
        graph_safety: Dict[str, Any],
        snippets: List[Dict[str, Any]],
        citations: List[Citation],
    ) -> str:
        evidence = []
        for index, row in enumerate(snippets[:5], 1):
            metadata = row.get("metadata") or {}
            evidence.append(
                {
                    "id": f"S{index}",
                    "title": metadata.get("title")
                    or metadata.get("drug_name")
                    or row.get("title_or_drug"),
                    "source": metadata.get("source")
                    or metadata.get("source_dataset")
                    or row.get("source"),
                    "section": metadata.get("section") or metadata.get("type"),
                    "snippet": (row.get("document_preview") or row.get("document") or "")[:900],
                }
            )

        payload = {
            "question": question,
            "deterministic_answer": deterministic_answer,
            "graph_safety": graph_safety,
            "evidence_snippets": evidence,
            "citations": [citation.model_dump() for citation in citations[:5]],
        }
        return (
            "You are a constrained answer rewriting layer for a Vietnamese "
            "medication-safety assistant.\n"
            "MANDATORY RULES:\n"
            "1. Use only the facts in the JSON payload below.\n"
            "2. Do not invent dosage, contraindications, interactions, diagnoses, "
            "or recommendations that are not present in the JSON.\n"
            "3. If graph_safety has findings, start with a clear safety warning.\n"
            "4. Answer in simple, cautious Vietnamese for the general public.\n"
            "5. Keep evidence citations in the form [S1], [S2] when discussing evidence.\n"
            "6. Always advise asking a doctor or pharmacist for prescription drugs, "
            "high-risk interactions, pregnancy, children, liver/kidney disease, or "
            "important comorbidities.\n"
            "7. If evidence is insufficient, say that the data is insufficient and "
            "recommend asking a doctor or pharmacist.\n\n"
            "JSON payload:\n"
            f"{json.dumps(payload, ensure_ascii=False, indent=2)}"
        )

    async def _gemini_generate(self, prompt: str) -> Optional[str]:
        url = (
            f"{settings.GEMINI_BASE_URL.rstrip('/')}/v1beta/models/"
            f"{self.model}:generateContent"
        )
        body = {
            "contents": [{"role": "user", "parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": settings.LLM_TEMPERATURE,
                "maxOutputTokens": settings.LLM_MAX_OUTPUT_TOKENS,
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

        candidates = data.get("candidates") or []
        if not candidates:
            return None
        parts = ((candidates[0].get("content") or {}).get("parts") or [])
        text = "\n".join(part.get("text") or "" for part in parts).strip()
        return text or None
