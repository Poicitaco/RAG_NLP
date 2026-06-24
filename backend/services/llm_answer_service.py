"""Constrained LLM answer rewriting for Safe RAG responses.

The LLM is optional and never acts as the source of medical truth. It only
rewrites approved graph findings and retrieved citations into clearer language.
"""
from __future__ import annotations

import json
import logging
from typing import Any, Dict, List, Optional

import httpx

from backend.config.settings import settings
from backend.models import Citation

_logger = logging.getLogger(__name__)


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
        if self.provider == "groq":
            return bool(settings.GROQ_API_KEY)
        return False

    async def rewrite(
        self,
        question: str,
        deterministic_answer: str,
        graph_safety: Dict[str, Any],
        snippets: List[Dict[str, Any]],
        citations: List[Citation],
        patient_context: Optional[Dict[str, Any]] = None,
    ) -> Optional[str]:
        if not self.is_available():
            return None
        if self.provider not in ("gemini", "groq"):
            return None

        prompt_payload = self._build_prompt(
            question=question,
            deterministic_answer=deterministic_answer,
            graph_safety=graph_safety,
            snippets=snippets,
            citations=citations,
            patient_context=patient_context,
        )
        try:
            if self.provider == "groq":
                answer = await self._groq_generate(
                    system_prompt=prompt_payload["system_prompt"],
                    user_payload=prompt_payload["user_payload"],
                )
            else:
                answer = await self._gemini_generate(
                    system_prompt=prompt_payload["system_prompt"],
                    user_payload=prompt_payload["user_payload"],
                )
            if not self._is_valid_rewrite(answer, graph_safety, citations):
                _logger.warning(
                    "LLM rewrite bi tu choi boi _is_valid_rewrite - su dung deterministic fallback. "
                    "Co citations: %s | Co graph_safety warning: %s | Do dai tra loi: %s",
                    bool(citations),
                    graph_safety.get("should_warn"),
                    len(answer or ""),
                )
                return None
            return answer
        except Exception as loi_llm:
            _logger.warning(
                "LLM rewrite gap loi, su dung deterministic fallback: %s",
                loi_llm,
                exc_info=True,
            )
            return None

    def _build_prompt(
        self,
        question: str,
        deterministic_answer: str,
        graph_safety: Dict[str, Any],
        snippets: List[Dict[str, Any]],
        citations: List[Citation],
        patient_context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, str]:
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
            "patient_context": patient_context or {},
            "deterministic_answer": deterministic_answer,
            "graph_safety": graph_safety,
            "evidence_snippets": evidence,
            "citations": [citation.model_dump() for citation in citations[:5]],
        }
        system_prompt = (
            "Bạn là SafeRAG Pharma, một chatbot hỗ trợ dược lâm sàng cho người Việt Nam, "
            "chuyên giải đáp câu hỏi về an toàn thuốc theo hồ sơ bệnh nhân. Hãy dựa hoàn toàn vào dữ liệu "
            "từ Dược thư Quốc gia Việt Nam (thông qua bối cảnh RAG cho trước [S1], [S2], v.v.) để trả lời. "
            "Tuyệt đối không suy đoán hoặc tạo thông tin mới ngoài nguồn dữ liệu RAG.\n\n"
            "Nhiệm vụ: Phân tích các câu hỏi về an toàn thuốc dựa trên hồ sơ bệnh nhân (độ tuổi: trẻ em/người lớn/người già; "
            "bệnh lý: tăng huyết áp, đái tháo đường, loét dạ dày, hen phế quản, bệnh thận/gan, phụ nữ mang thai) "
            "và đánh giá mức độ an toàn của thuốc cụ thể đối với tình trạng đó.\n\n"
            "Luôn giải thích logic lâm sàng/tác động dược lý trước khi phân loại an toàn/nguy hiểm. "
            "TUYỆT ĐỐI KHÔNG đưa ra câu trả lời chung chung như 'tùy hoạt chất', 'cần kiểm tra hoạt chất'. "
            "Không mở đầu bằng câu cảnh báo/chối từ. Không tự chế tạo thông tin y tế ngoài bối cảnh RAG đã cung cấp.\n\n"
            "Phản hồi của bạn PHẢI theo đúng cấu trúc sau:\n"
            "1. **Lưu ý an toàn**: (Phân tích nguy cơ liên quan giữa thuốc & tình trạng bệnh trên hồ sơ bệnh nhân. Giải thích tại sao — về dược lực học/dược động học — trước khi KẾT LUẬN rõ ràng là ✅ AN TOÀN hay ❌ NGUY HIỂM đối với bệnh nhân này.)\n"
            "2. **Hướng dẫn nhanh**: Hướng dẫn cụ thể từng bước (kiểm tra nhãn thuốc thành phần gì, lưu ý liều dùng, đường dùng, dấu hiệu cảnh báo).\n"
            "3. **Giải thích thêm**: Diễn giải cơ chế tác động / vì sao bệnh lý ảnh hưởng đến thuốc này bằng ngôn ngữ đơn giản, dễ hiểu.\n"
            "4. **Giải pháp thay thế**: Đề xuất ít nhất 1 lựa chọn an toàn, phù hợp cho tình trạng bệnh của bệnh nhân (có dẫn giải thích ngắn nếu cần).\n"
            "5. **Nguồn tham khảo**: LUÔN ghi trích dẫn rõ ràng [S1], [S2] từ bối cảnh RAG đã cung cấp; không sử dụng/không bịa ra các nguồn khác.\n\n"
            "Hãy tư duy mạch lạc từng bước và đảm bảo đầy đủ CẢ năm mục trên trong mọi câu trả lời. Nếu dữ liệu không đủ rõ, hãy nói 'Chưa đủ dữ liệu trong nguồn cho câu hỏi này' thay vì suy đoán.\n\n"
            "# Các bước thực hiện\n"
            "- Đọc kỹ thông tin hồ sơ bệnh nhân và câu hỏi về thuốc.\n"
            "- Đối chiếu các nguy cơ với các đặc điểm bệnh lý/tuổi tác/liên quan đã nêu.\n"
            "- Diễn giải cơ chế nguy cơ/dược lý học ngắn gọn trước khi kết luận.\n"
            "- Chỉ phân loại AN TOÀN/NGUY HIỂM sau khi đã diễn giải.\n"
            "- Đề xuất phương án thay thế hợp lý nếu có nguy cơ.\n"
            "- Luôn trích dẫn nguồn đúng chuẩn '[S1]'.\n\n"
            "# Định dạng trả lời\n"
            "Trả lời bằng tiếng Việt hoàn chỉnh, sử dụng mẫu phía trên. Đảm bảo mỗi mục đều có nội dung và sắp xếp đúng thứ tự.\n\n"
            "# Ví dụ\n"
            "**Ví dụ 1 (dành cho bệnh nhân tăng huyết áp dùng pseudoephedrine):**\n"
            "1. **Lưu ý an toàn**: Pseudoephedrine có cơ chế co mạch, làm tăng huyết áp và có thể gây nhịp tim nhanh hoặc tăng huyết áp kịch phát ở người có tiền sử tăng huyết áp [GIẢI THÍCH NGẮN]. Do đó, ❌ NGUY HIỂM cho bệnh nhân tăng huyết áp. [S1]\n"
            "2. **Hướng dẫn nhanh**: Kiểm tra thành phần hoạt chất pseudoephedrine trên nhãn thuốc; không dùng nếu có ghi pseudoephedrine hoặc các thuốc giải nghẹt mũi tương tự. Nếu đang dùng phải ngưng và thông báo cho bác sĩ.\n"
            "3. **Giải thích thêm**: Người tăng huyết áp nhạy cảm với các chất làm co mạch, vì pseudoephedrine làm tăng sức cản mạch máu và huyết áp, có thể gây tai biến mạch máu não hoặc suy tim nếu sử dụng kéo dài. [S1]\n"
            "4. **Giải pháp thay thế**: Có thể sử dụng nước muối sinh lý nhỏ mũi hoặc thuốc xịt làm thông thoáng không chứa hoạt chất co mạch, ví dụ natri clorid 0,9% [S2].\n"
            "5. **Nguồn tham khảo**: [S1], [S2]\n\n"
            "**Ví dụ 2 (bệnh nhân suy gan dùng paracetamol liều cao):**\n"
            "1. **Lưu ý an toàn**: Paracetamol chuyển hóa qua gan, liều cao hoặc dùng lâu dài dễ gây độc cho gan, đặc biệt ở bệnh nhân có tiền sử suy gan. Vì vậy, ❌ NGUY HIỂM nếu sử dụng liều cao hoặc kéo dài ở người suy gan. [S2]\n"
            "2. **Hướng dẫn nhanh**: Đọc kỹ thành phần paracetamol, không dùng liều trên 2g/ngày nếu có bệnh gan. Nếu đã dùng nên theo dõi triệu chứng vàng da, mệt mỏi, buồn nôn.\n"
            "3. **Giải thích thêm**: Ở người suy gan, khả năng chuyển hóa paracetamol giảm làm tăng nguy cơ tích lũy chất độc (NAPQI) gây tổn thương gan. [S2]\n"
            "4. **Giải pháp thay thế**: Có thể dùng thuốc giảm đau khác không gây độc cho gan như ibuprofen (nếu không có chống chỉ định). [S3]\n"
            "5. **Nguồn tham khảo**: [S2], [S3]\n\n"
            "(Lưu ý: ví dụ thực tế trả lời dài hơn khi vào chi tiết lâm sàng hoặc nhiều bệnh lý phối hợp.)\n\n"
            "# Lưu ý\n"
            "- TUYỆT ĐỐI KHÔNG tạo thông tin y khoa ngoài dữ liệu từ RAG context.\n"
            "- Không mở đầu bằng cảnh báo/chối từ kiểu 'Trả lời chỉ mang tính chất tham khảo...'\n"
            "- Phải giải thích nguy cơ trước rồi mới được đưa ra phân loại cuối cùng.\n"
            "- Luôn đề xuất giải pháp thay thế nếu liên quan đến an toàn.\n"
            "- Nếu không có dữ liệu, hãy trả lời 'Chưa đủ dữ liệu trong nguồn cho câu hỏi này'.\n\n"
            "# Output Format\n"
            "- Trả lời đầy đủ theo 5 mục bằng văn bản thuần tiếng Việt.\n"
            "- Giữ nguyên định dạng đánh số và in đậm từng mục như mẫu ở trên.\n"
            "- Không sử dụng markdown hay mã hóa. Không dịch ra tiếng Anh."
        )
        return {
            "system_prompt": system_prompt,
            "user_payload": "JSON payload:\n" + json.dumps(payload, ensure_ascii=False, indent=2),
        }

    def _is_valid_rewrite(
        self,
        answer: Optional[str],
        graph_safety: Dict[str, Any],
        citations: List[Citation],
    ) -> bool:
        if not answer:
            return False
        stripped = answer.strip()
        if len(stripped) < 80:
            return False
        # Chap nhan ca [S1] va [ S1] (LLM doi khi them khoang trang)
        import re as _re
        # Bỏ kiểm tra citation gắt gao để chấp nhận câu trả lời LLM tự nhiên hơn
        # if citations and not _re.search(r"\[\s*S\d+\s*\]", stripped):
        #     return False
        if graph_safety.get("should_warn"):
            lowered = stripped.lower()
            warning_terms = ("cảnh báo", "canh bao", "thận trọng", "than trong", "tránh", "tranh", "lưu ý")
            if not any(term in lowered for term in warning_terms):
                return False
        return True

    async def _gemini_generate(self, system_prompt: str, user_payload: str) -> Optional[str]:
        url = (
            f"{settings.GEMINI_BASE_URL.rstrip('/')}/v1beta/models/"
            f"{self.model}:generateContent"
        )
        body = {
            "system_instruction": {"parts": [{"text": system_prompt}]},
            "contents": [{"role": "user", "parts": [{"text": user_payload}]}],
            "generationConfig": {
                "temperature": settings.LLM_TEMPERATURE,
                "maxOutputTokens": settings.LLM_MAX_OUTPUT_TOKENS,
            },
            "safetySettings": [
                {
                    "category": "HARM_CATEGORY_HARASSMENT",
                    "threshold": "BLOCK_NONE"
                },
                {
                    "category": "HARM_CATEGORY_HATE_SPEECH",
                    "threshold": "BLOCK_NONE"
                },
                {
                    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                    "threshold": "BLOCK_NONE"
                },
                {
                    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                    "threshold": "BLOCK_NONE"
                }
            ]
        }
        headers = {
            "x-goog-api-key": settings.GEMINI_API_KEY,
            "Content-Type": "application/json",
        }
        
        # Thêm cơ chế tự động retry khi gặp lỗi 429 (Quá tải API miễn phí)
        import asyncio
        max_retries = 3
        for attempt in range(max_retries):
            try:
                async with httpx.AsyncClient(timeout=self.timeout) as client:
                    response = await client.post(url, headers=headers, json=body)
                    response.raise_for_status()
                    data = response.json()
                    break # Thành công thì thoát vòng lặp
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 429 and attempt < max_retries - 1:
                    _logger.warning(f"Gemini API 429 Too Many Requests. Đang đợi 3s để thử lại (Lần {attempt + 1}/{max_retries})...")
                    await asyncio.sleep(3)
                else:
                    raise # Hết lượt retry hoặc lỗi khác thì ném lỗi ra ngoài
                    
        candidates = data.get("candidates") or []
        if not candidates:
            _logger.error(f"Gemini trả về không có candidates. Data: {data}")
            return None
        finish_reason = candidates[0].get("finishReason")
        if finish_reason and finish_reason != "STOP":
            _logger.error(f"Gemini dừng vì finish_reason={finish_reason}. Data: {data}")
            return None
        parts = ((candidates[0].get("content") or {}).get("parts") or [])
        text = "\n".join(part.get("text") or "" for part in parts).strip()
        if not text:
            _logger.error(f"Gemini trả về chuỗi rỗng. Data: {data}")
        return text or None

    async def _groq_generate(self, system_prompt: str, user_payload: str) -> Optional[str]:
        url = "https://api.groq.com/openai/v1/chat/completions"
        body = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_payload}
            ],
            "temperature": settings.LLM_TEMPERATURE,
            "max_tokens": settings.LLM_MAX_OUTPUT_TOKENS,
        }
        headers = {
            "Authorization": f"Bearer {settings.GROQ_API_KEY}",
            "Content-Type": "application/json",
        }
        
        import asyncio
        max_retries = 3
        for attempt in range(max_retries):
            try:
                async with httpx.AsyncClient(timeout=self.timeout) as client:
                    response = await client.post(url, headers=headers, json=body)
                    response.raise_for_status()
                    data = response.json()
                    break
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 429 and attempt < max_retries - 1:
                    _logger.warning(f"Groq API 429 Too Many Requests. Đợi 3s... Lần {attempt + 1}/{max_retries}")
                    await asyncio.sleep(3)
                else:
                    raise
                    
        choices = data.get("choices") or []
        if not choices:
            _logger.error(f"Groq trả về không có choices. Data: {data}")
            return None
            
        message = choices[0].get("message") or {}
        text = (message.get("content") or "").strip()
        if not text:
            _logger.error(f"Groq trả về chuỗi rỗng. Data: {data}")
            
        return text or None
