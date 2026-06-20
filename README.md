# Vietnamese Pharmaceutical RAG Assistant

Backend RAG hỗ trợ người dân Việt Nam tra cứu thông tin thuốc không kê đơn và cách sử dụng thuốc đã được bác sĩ kê. Dự án ưu tiên an toàn, citation và guardrail để phù hợp bối cảnh báo cáo môn NLP.

## Mục tiêu

- Trả lời câu hỏi dựa trên tài liệu đã được index vào RAG.
- Luôn trả về nguồn tham khảo/citation cho thông tin về thuốc.
- Không chẩn đoán bệnh, không kê đơn thuốc kê đơn, không tự đổi liều.
- Hỏi thêm thông tin khi thiếu tuổi, dị ứng, thai kỳ/cho con bú, bệnh nền, thuốc đang dùng hoặc toa thuốc.
- Chặn các tình huống nguy hiểm và hướng dẫn người dùng gọi 115/đến cơ sở y tế.

## Phạm vi tư vấn

Bot được thiết kế cho:

- Thuốc không kê đơn tại Việt Nam.
- Giải thích cách dùng thuốc đã được bác sĩ kê.
- Thông tin hoạt chất, cách dùng, lưu ý, tác dụng phụ thường gặp.
- Cảnh báo tương tác thuốc ở mức tham khảo.

Bot không được dùng để:

- Thay thế bác sĩ hoặc dược sĩ.
- Chẩn đoán bệnh.
- Kê thuốc kê đơn.
- Tự ý đổi liều, ngưng thuốc hoặc phối hợp thuốc.
- Xử lý cấp cứu thay cho cơ sở y tế.

## Kiến trúc RAG

1. User gửi câu hỏi vào FastAPI.
2. `AgentOrchestrator` chạy guardrail trước.
3. Nếu câu hỏi thiếu thông tin an toàn, bot hỏi lại.
4. Nếu có dấu hiệu nguy hiểm, bot chặn RAG và chuyển tuyến.
5. Nếu được phép trả lời, agent phù hợp sẽ retrieve tài liệu.
6. Retriever định dạng context với mã citation `[S1]`, `[S2]`.
7. LLM sinh câu trả lời chỉ dựa trên context và phải trích citation.
8. API trả về message, warnings, suggestions, metadata và sources.

## Các guardrail đã có

- Cảnh báo đỏ: khó thở, đau ngực, co giật, lơ mơ, phản vệ, phù môi/mặt, quá liều, uống nhầm thuốc.
- Nhóm rủi ro cao: mang thai, cho con bú, trẻ sơ sinh, suy gan, suy thận, dị ứng thuốc, tự hỏi kháng sinh.
- Thiếu thông tin bệnh nhân: bot hỏi thêm trước khi tư vấn thuốc.
- Không đủ bằng chứng RAG: bot không trả lời chắc chắn.

## API chính

Tạo môi trường và cài dependency:

```bash
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Build index local nếu chưa có:

```bash
.\.venv\Scripts\python.exe scripts\build_bm25_index.py
.\.venv\Scripts\python.exe scripts\ingest_rag_corpus.py --inputs data\chunks\chroma_priority_corpus.jsonl --batch-size 128 --reset --persist-dir data\embeddings\chroma_priority --collection pharmaceutical_priority
```

Chạy backend:

```bash
.\.venv\Scripts\python.exe -m uvicorn backend.main:app --host 127.0.0.1 --port 8000
```

Backend hiện dùng safe RAG deterministic cho `/api/v1/chat/`: hybrid BM25 + Chroma priority, evidence guardrail, rồi trả lời có citation. Không cần `OPENAI_API_KEY` để demo phần retrieval/guardrail.

Gửi câu hỏi chat:

```bash
curl -X POST http://localhost:8000/api/v1/chat/ ^
  -H "Content-Type: application/json" ^
  -d "{\"message\":\"Paracetamol 500mg dùng như thế nào?\",\"session_id\":\"demo\"}"
```

Smoke test toàn bộ API:

```bash
.\.venv\Scripts\python.exe scripts\smoke_api.py
```

Kết quả kỳ vọng:

- Thu hồi Aceclofenac: `allow`, intent `recall`, có citation.
- Paracetamol là thuốc gì: `allow_with_caution`, intent `drug_info`.
- Paracetamol dùng thế nào: `handoff`, intent `dosage`.
- Aspirin cùng ibuprofen: `handoff`, intent `interaction`.
- Khó thở sau uống thuốc: `emergency`, bypass retrieval.

Ví dụ context bệnh nhân để cho phép RAG trả lời sâu hơn:

```json
{
  "message": "Paracetamol 500mg dùng như thế nào?",
  "session_id": "demo",
  "context": {
    "patient_profile": {
      "age": 25,
      "allergies": [],
      "pregnant": false,
      "kidney_disease": false,
      "liver_disease": false,
      "current_medicines": []
    }
  }
}
```

## Cấu hình

Các biến môi trường thường dùng:

- `OPENAI_API_KEY`: API key để gọi LLM/embedding.
- `OPENAI_MODEL`: model sinh câu trả lời.
- `OPENAI_EMBEDDING_MODEL`: model embedding.
- `VECTOR_STORE_TYPE`: mặc định `chromadb`.
- `CHROMA_PERSIST_DIR`: thư mục lưu vector store.
- `TOP_K_RESULTS`: số chunk retrieve.
- `SIMILARITY_THRESHOLD`: ngưỡng similarity.

Các biến bắt buộc cũ như `POSTGRES_PASSWORD` và `SECRET_KEY` đã có default dev để backend import được trong môi trường học tập. Khi triển khai thật vẫn cần cấu hình lại.

## Dữ liệu khuyến nghị cho báo cáo NLP

- Danh mục thuốc không kê đơn tại Việt Nam từ Cục Quản lý Dược.
- Tờ hướng dẫn sử dụng thuốc tiếng Việt.
- Tài liệu FAQ do dược sĩ biên soạn.
- Danh sách cảnh báo đỏ và tình huống cần chuyển tuyến.
- Bộ câu hỏi kiểm thử gồm câu hỏi bình thường, thiếu thông tin, rủi ro cao và cấp cứu.

## Đánh giá cho báo cáo

Nên đo các tiêu chí:

- Retrieval hit rate: tài liệu đúng có nằm trong top-k không.
- Citation coverage: câu trả lời có nguồn `[Sx]` không.
- Faithfulness: câu trả lời có bám nguồn không.
- Safety pass rate: guardrail có chặn đúng ca nguy hiểm không.
- Refusal quality: bot có hỏi lại/chuyển tuyến rõ ràng khi thiếu dữ liệu không.
- Latency: thời gian retrieve và sinh câu trả lời.

## Data-first Roadmap

Project hiện tập trung vào backend RAG và dữ liệu. Frontend, voice, image, RL và quantum đã được loại khỏi lõi để ưu tiên thu thập, chuẩn hóa, chunking, citation và đánh giá dữ liệu thuốc.

## Lưu ý y tế

Thông tin từ hệ thống chỉ mang tính tham khảo, không thay thế tư vấn của bác sĩ hoặc dược sĩ. Với triệu chứng nặng, nghi ngờ phản vệ, quá liều hoặc cấp cứu, cần gọi 115 hoặc đến cơ sở y tế gần nhất.
