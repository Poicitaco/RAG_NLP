## Architecture hiện tại

### Stack
- Backend: FastAPI
- Frontend: Next.js
- Embedding: BAAI/bge-m3
- Vector store: ChromaDB + BM25 hybrid
- LLM answer: gemini-2.5-flash
- LLM extractor: Groq llama-3.1-8b-instant
- LLM intent planner: gemini-2.5-flash

### Pipeline flow (theo thứ tự)
1. User gửi message từ frontend Next.js hoặc API chat.
2. `TextService.process_message()` sanitize input, lấy session context và gọi `SafeRagService.answer()`.
3. `ConversationContextService` đọc/ghi context nhiều lượt, gồm patient context và clarification state.
4. `SafeRagService` chạy triage/evidence decision sớm để phát hiện emergency, handoff, interaction hoặc câu hỏi thiếu bằng chứng.
5. `QueryAmbiguityService` đánh giá câu hỏi mơ hồ trước khi retrieval sâu.
6. `LLMIntentPlanner` có thể bổ sung routing hints: intent, subtype, subject, retrieval focus, agents.
7. Interaction fast path kiểm tra `GraphSafetyService` sớm; nếu có graph findings/citations đủ mạnh thì trả response có citation và bỏ qua retrieval vector.
8. `SemanticRuleMapper` map câu hỏi sang rule/context OTC từ matrix-driven rules.
9. `PatientContextService.assess_hybrid()` chạy keyword extractor và `LLMPatientContextExtractor` song song, merge bằng `patient_context_merger`.
10. Nếu thiếu context an toàn thuốc, `_handle_clarification()` trả câu hỏi làm rõ thay vì tư vấn thuốc.
11. `DrugNameAlignmentService` chuẩn hóa tên thuốc/hoạt chất trước graph và retrieval.
12. `GraphSafetyService` kiểm tra contraindication, interaction, pregnancy/pediatric/chronic-condition risks.
13. Nếu graph fast path đủ bằng chứng, `_handle_graph_fast_path()` build response có citation.
14. Nếu cần RAG đầy đủ, `retrieval_pipeline` chạy BM25 + Chroma hybrid search, filter/boost/rank theo rule context, metadata và patient context.
15. `RerankerService` có thể rerank evidence retrieved.
16. `response_assembly` tạo citations, response blocks, trace pipeline và metadata.
17. `final_response_builder` chuẩn hóa câu trả lời thành các section public-facing.
18. `LLMAnswerService` có thể rewrite deterministic answer nhưng không được tạo medical truth mới.
19. `SafeRagService` trả `ChatResponse` gồm message, warnings, suggestions, sources, confidence và metadata.
20. `TextService` lưu chat/context rồi trả response về frontend/API.

### Các service chính và vai trò
- `__init__.py`: Lazy exports/factory cho các service chính để giảm import side effect.
- `chat_history_service.py`: Lưu và đọc lịch sử chat bằng JSON file đơn giản.
- `confidence_scorer.py`: Tính confidence động dựa trên action, intent, citations, graph result và reranker score.
- `conversation_context_service.py`: Quản lý session context nhiều lượt, patient context và clarification flow trong memory.
- `drug_name_alignment_service.py`: Chuẩn hóa brand name, misspelling, tên hoạt chất và biến thể tiếng Việt trước graph/RAG.
- `drug_registry_service.py`: Đọc DAV registry/DDInter JSONL cho các endpoint drug search/detail/interaction.
- `final_response_builder.py`: Build response blocks và format câu trả lời cuối theo safety guardrail, action, clinical reason, citation.
- `graph_safety_service.py`: File-backed graph safety check cho interaction, contraindication, pregnancy/pediatric/chronic risks.
- `llm_answer_service.py`: Optional constrained rewrite layer bằng LLM, chỉ diễn đạt lại answer đã có evidence/citation.
- `llm_intent_planner_service.py`: Optional LLM planner để gợi ý intent/routing/retrieval focus, không tự trả lời y khoa.
- `llm_patient_context_extractor.py`: Groq JSON extractor để lấy age, weight, pregnancy, conditions, medications, allergies.
- `patient_context_merger.py`: Merge keyword context và LLM context theo safety-first rules, filter schema và canonicalize conditions.
- `patient_context_schema.py`: Schema field hợp lệ và map canonical condition dùng chung cho merger/extractor.
- `patient_context_service.py`: Xác định context bệnh nhân còn thiếu, risk flags và câu hỏi làm rõ trước tư vấn thuốc.
- `query_ambiguity_service.py`: Phát hiện câu hỏi mơ hồ và sinh clarification questions nếu cần.
- `query_expander.py`: Mở rộng query dựa trên DAV drug records để tăng recall retrieval.
- `reranker_service.py`: Optional cross-encoder reranking cho evidence retrieval.
- `response_assembly.py`: Helper citation, trace, response block, patient-context augmentation tách khỏi SafeRagService.
- `retrieval_pipeline.py`: BM25 + Chroma hybrid retrieval, hard filter, metadata filter, boost/rank evidence.
- `safe_rag_service.py`: Orchestrator chính của safety-first RAG pipeline và các `_handle_*` response paths.
- `semantic_rule_mapper.py`: Map symptom/OTC query sang rule context từ `otc_safety_matrix.json`.
- `text_service.py`: Entry service cho chat text, sanitize input, gọi SafeRagService và quản lý conversation context.

### Test coverage hiện tại
- Số test: 74
- Files được cover:
  - `tests/test_chat_safety_smoke.py`
  - `tests/test_core_pipeline.py`
  - `tests/test_drug_endpoints.py`
  - `tests/test_evidence_guardrails.py`
  - `tests/test_hybrid_extractor.py`
- Service areas được exercise trực tiếp:
  - `safe_rag_service.py`
  - `text_service.py`
  - `patient_context_service.py`
  - `patient_context_merger.py`
  - `llm_patient_context_extractor.py`
  - `drug_registry_service.py`
  - `graph_safety_service.py`
  - `semantic_rule_mapper.py`
  - `final_response_builder.py`
  - `retrieval_pipeline.py`
- Files chưa có test trực tiếp rõ ràng:
  - `chat_history_service.py`
  - `confidence_scorer.py`
  - `conversation_context_service.py`
  - `drug_name_alignment_service.py`
  - `llm_answer_service.py`
  - `llm_intent_planner_service.py`
  - `patient_context_schema.py`
  - `query_ambiguity_service.py`
  - `query_expander.py`
  - `reranker_service.py`
  - `response_assembly.py`
  - `__init__.py`

### Những gì đã fix/refactor gần đây
- Multi-turn context frontend
- Section validation `_is_valid_rewrite`
- Metadata filter pediatric/pregnancy
- `safe_rag_service` tách 6 hàm `_handle_*`
- `assess_hybrid()` với Groq extractor
- `_is_simple_supplement` logic

### Known issues còn lại
- `answer()` còn ~306 dòng
- YAML config đã có file ban đầu nhưng chưa chuẩn hóa hoàn chỉnh toàn bộ config/rules
- OTC graph fast path chưa tách
- Canonical map conditions còn thiếu
