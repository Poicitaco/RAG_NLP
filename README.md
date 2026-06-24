# 🏥 SafeRAG Pharma - Vietnamese Pharmaceutical RAG Assistant

<div align="center">
  <p>Hệ thống AI Tư vấn Dược phẩm an toàn dành cho người Việt, được thiết kế đặc biệt với kiến trúc <strong>Multi-Agent RAG</strong> và <strong>Hybrid Safety Guardrails</strong> để đảm bảo thông tin chính xác, minh bạch và an toàn tuyệt đối (Zero Hallucination).</p>
</div>

---

## 🌟 Tính Năng Nổi Bật (Key Features)

- 🛡️ **Kiến trúc An toàn Kép (Hybrid Safety Guardrails):**
  - **Luật Cứng (Rule-based):** Tự động chặn các tư vấn nguy hiểm liên quan đến 6 nhóm rủi ro cao (Tăng HA, Tiểu đường, Hen suyễn, Phụ nữ mang thai, Trẻ sơ sinh, Suy gan/thận).
  - **Vector Retrieval:** Chỉ trả lời dựa trên bằng chứng (evidence) trích xuất từ **Dược Thư Quốc Gia Việt Nam**.
- 🤖 **Điều phối Đa Tác tử (Multi-Agent Orchestrator):** Phân luồng câu hỏi thông minh tới các agent chuyên biệt (Dosage, Interaction, Drug Info, Safety Monitor).
- 🔍 **Trích dẫn Minh bạch (Transparent Citations):** Mọi thông tin y tế sinh ra đều kèm theo nguồn gốc `[S1]`, `[S2]` và audit logs chi tiết cho phép truy xuất ngược.
- 🚀 **Giao diện & Trải nghiệm Đẳng cấp:** Tích hợp Frontend Next.js hiện đại, quản lý hồ sơ bệnh nhân (Patient Context) ngay trên UI để cá nhân hóa tư vấn.

## 🏗️ Kiến trúc Hệ thống (System Architecture)

Dự án tuân theo mô hình Client-Server hiện đại:
- **Backend (Core RAG):** `FastAPI`, `LangChain`, `ChromaDB` (Vector Database), BM25 (Hybrid Search).
- **Frontend (Web UI):** `Next.js`, `TailwindCSS`, `React`, `Lucide Icons`.

**Luồng Xử Lý RAG (RAG Pipeline):**
1. **Tiếp nhận:** Người dùng gửi câu hỏi kèm *Hồ sơ Bệnh nhân*.
2. **Kiểm tra An toàn (Guardrails):** Chặn các từ khóa cấp cứu hoặc yêu cầu bổ sung dữ kiện thiết yếu.
3. **Phân luồng (Orchestrator):** Chuyển hướng đến Agent phù hợp với intent.
4. **Truy xuất (Retrieval):** Hybrid Search (Vector + BM25) vào Dược thư Quốc gia.
5. **Tổng hợp (Generation):** LLM sinh câu trả lời kèm citation minh bạch.

---

## 🚀 Hướng Dẫn Khởi Chạy (Getting Started)

Dự án bao gồm hai phần độc lập. Cần khởi chạy cả hai để hệ thống hoạt động hoàn chỉnh.

### 1. Cài đặt Backend (FastAPI)

```bash
# Clone dự án và di chuyển vào thư mục gốc
git clone <repo-url>
cd RAG_BOT-main

# Khởi tạo môi trường ảo và cài đặt thư viện
python -m venv .venv
# Trên Windows:
.venv\Scripts\activate
# Trên macOS/Linux:
# source .venv/bin/activate

pip install -r requirements.txt

# (Tùy chọn) Cấu hình biến môi trường
# cp .env.example .env
# Thêm OPENAI_API_KEY vào file .env
```

**Khởi tạo Cơ sở Dữ liệu & Chạy Server:**

```bash
# Build BM25 Index và Ingest Dữ liệu vào ChromaDB
python scripts/build_bm25_index.py
python scripts/ingest_rag_corpus.py --inputs data/chunks/chroma_priority_corpus.jsonl --batch-size 128 --reset --persist-dir data/embeddings/chroma_priority --collection pharmaceutical_priority

# Khởi chạy server Backend (tại http://localhost:8000)
python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

### 2. Cài đặt Frontend (Next.js)

Mở một Terminal thứ 2:

```bash
cd frontend-next

# Cài đặt các gói phụ thuộc
npm install

# Khởi chạy giao diện người dùng
npm run dev
```

Giao diện sẽ có mặt tại: **http://localhost:3000**

---

## 📊 Tiêu Chí Đánh Giá (NLP Metrics)

Đồ án được thiết kế để đạt độ chuẩn xác cao nhất theo các tiêu chuẩn đánh giá hệ thống NLP Y tế hiện hành:
- **Retrieval Hit Rate:** Tỷ lệ tài liệu chuẩn xác nằm trong top-k khi truy xuất.
- **Citation Coverage:** Mức độ phủ của các trích dẫn `[Sx]` minh bạch trong câu trả lời.
- **Faithfulness:** Tính trung thực, không suy diễn vượt quá phạm vi ngữ cảnh truy xuất được.
- **Safety Pass Rate:** Tỷ lệ hệ thống từ chối hoặc chuyển tuyến thành công trong các tình huống nguy hiểm/thiếu dữ kiện.
- **Latency:** Thời gian phản hồi tối ưu hóa nhờ thiết kế Hybrid Search song song.

---

## ⚠️ Tuyên Bố Miễn Trừ Trách Nhiệm (Medical Disclaimer)

*Hệ thống RAG này được phát triển thuần túy cho mục đích học thuật và nghiên cứu học phần NLP.*

**Tuyệt đối không sử dụng thay thế chẩn đoán chuyên môn của bác sĩ.** Hệ thống có thể từ chối trả lời nếu phát hiện rủi ro cao. Trong các trường hợp cấp cứu (như phản vệ, khó thở, quá liều), hệ thống mặc định yêu cầu người dùng gọi **115** hoặc tới cơ sở y tế gần nhất.
