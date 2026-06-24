# Ke Hoach Tai Cau Truc RAG Bot Duoc Pham

**Muc tieu:** He thong tu van an toan thuoc OTC cho nguoi dan Viet Nam pho thong — Dung truoc, dep sau.

---

## Tra Loi Cau Hoi "Co Nen Xoa Toan Bo Khong?"

> [!IMPORTANT]
> **Khong nen xoa toan bo.** Data + embedding + BM25 index la tai san quy nhat, mat nhieu tuan de build. Backend core pipeline tuy nhieu logic nhung co the refactor. Chi nen xoa Frontend hien tai va cac scripts rac.

**Giu lai nguyen (khong cham vao):**
- `data/` — toan bo (209,077 chunks, BM25 80MB, Chroma 3.4GB SQLite)
- `backend/safety/` — evidence_guardrails.py da duoc tested
- `backend/services/graph_safety_service.py` — hoat dong tot
- `backend/config/settings.py` — da clean
- `backend/main.py` — FastAPI app chuan

**Xoa va viet lai tu dau:**
- `frontend/src/App.jsx` (922 dong, 1 file khong lo) → Tach thanh components
- `scripts/legacy/` → Xoa het
- `backend/rag/generator.py` → Xoa (dead code OpenAI/LangChain)

**Refactor (giu logic, don code):**
- `backend/services/safe_rag_service.py` (1933 dong) → Tach thanh 3 file nho hon
- `backend/api/routes/chat.py` → Them persist history

---

## Danh Gia Data Hien Tai

| Nguon | So chunks | Tinh trang | Can lam lai? |
|-------|-----------|-----------|--------------|
| `dav_all` | 12,000 | OK - chinh thuc | Khong |
| `dav_recall` | 84 | OK | Khong |
| `dav_otc_pdf_ocr` | 784 | OCR loi, da co ban `_corrected` | Xoa ban cu, giu ban corrected |
| `canhgiacduoc` | 1,200 | OK | Khong |
| `trungtamthuoc_duocthu` | 34,677 | OK | Khong |
| `ddinter` | 160,235 | OK — nguon DDI manh nhat | Khong |
| `otc_condition_guardrail` | **9** | **QUA IT — chi co 1 rule tieu duong** | Can viet them 6 nhom |

> [!WARNING]
> **Chroma SQLite (3.4GB) va BM25 index (80MB) KHONG can embedding lai.** Chi re-index neu them data moi. Kiem tra Chroma collection count truoc khi quyet dinh bat cu dieu gi.

**Khoang trong data can bo sung:**

OTC guardrails hien tai chi co 9 documents cho benh tieu duong + thuoc cam. Can them:
- Tang huyet ap + NSAIDs/thuoc cam
- Phu nu co thai / cho con bu
- Tre em (< 2 tuoi, < 6 tuoi, < 12 tuoi) — liet ke hoat chat cam
- Suy than / Suy gan + cac nhom thuoc OTC can tranh
- Da day / Xuat huyet tieu hoa + NSAIDs
- Hen suyen / COPD + beta-blocker nho mat, aspirin

---

## Giai Doan 1 — Kiem Tra Data + Don Dep Code Rac (2-3 ngay)

### Buoc 1: Kiem tra Chroma (5 phut — bat buoc lam truoc)

```bash
cd c:\Users\Poicitaco\Desktop\RAG_BOT-main\RAG_BOT-main
python -c "
import chromadb
client = chromadb.PersistentClient(path='data/embeddings/chroma_priority')
col = client.get_collection('pharmaceutical_local_bge_1024')
print('So luong documents trong Chroma:', col.count())
"
```
- Ket qua >= 200,000 → **Khong can re-embed**, di thang buoc 2
- Ket qua < 100,000 → **Can re-embed** tu `data/chunks/chroma_priority_corpus.jsonl`

### Buoc 2: Xoa file rac

```
scripts/legacy/                                   XOA TOAN BO
backend/rag/generator.py                          XOA (dead code, khong duoc goi)
data/chunks/dav_otc_pdf_ocr_chunks.jsonl          XOA (dung ban _corrected thay the)
data/embeddings/chroma/ (collection cu)           XOA neu khong dung
data/embeddings/chroma_priority_backup_*          XOA
```

### Buoc 3: Refactor safe_rag_service.py

1,933 dong qua lon, kho doc va test. Tach thanh 3 file:

#### [MODIFY] safe_rag_service.py
Chi giu ham `answer()` chinh va `__init__`. Muc tieu < 500 dong.

#### [NEW] retrieval_pipeline.py
Chua: ham `retrieve()`, `_hard_filter_results()`, `_apply_rule_retrieval_policy()`, `_apply_indication_retrieval_policy()`, `_quick_supporting_citations()`.

#### [NEW] response_assembly.py
Chua: `_selected_agents()`, `_clarification_response_blocks()`, `_with_citation_block_sources()`, `_baseline_safety_citations()`, `_citation_from_row()`, `_citations_from_graph_findings()`, `_renumber_citations()`, `_citation_dicts()`, `_agent_pipeline()`.

---

## Giai Doan 2 — On Dinh Backend (5-7 ngay)

### 2.1 Fix Logic Con Lai
- `[x]` FIX 1: Dead code `_build_prompt()` — DA XONG
- `[x]` FIX 2: PatientContext goi 2 lan — DA XONG
- `[x]` FIX 3: Citation title=None — DA XONG
- `[x]` FIX 4: Silent fail LLM rewrite — DA XONG
- `[x]` FIX 5: MIN_HYBRID_SCORE vao settings — DA XONG
- `[ ]` FIX 6: Tach `classify_question_intent()` khoi `evaluate_evidence()` buoc som
- `[ ]` FIX 7: Xoa `rag/generator.py`
- `[ ]` FIX 8: Persist chat history voi SQLite/JSON

### 2.2 Mo Rong OTC Guardrail Rules
Them 6 nhom benh nen vao `scripts/prepare_otc_condition_guardrails.py` roi re-generate:
```bash
python scripts/prepare_otc_condition_guardrails.py
python scripts/build_chroma_priority_corpus.py
python scripts/build_bm25_index.py
```

### 2.3 Chay Test Baseline
```bash
# Chay bo test co san voi cac cau hoi mau
python scripts/evaluate_test_questions_safe_rag.py --output output/baseline_results.json
```
So sanh ket qua truoc/sau refactor.

### 2.4 Chuan Hoa API Schema
Dam bao moi response `/api/v1/chat/` luon tra ve dung:
```json
{
  "message": "string (Markdown)",
  "conversation_id": "string",
  "confidence": 0.0,
  "sources": [{"id": "S1", "title": "...", "source": "...", "url": null}],
  "warnings": ["string"],
  "suggestions": ["string"],
  "metadata": {
    "rag_action": "allowed|allow_with_caution|needs_clarification|emergency|handoff",
    "intent": "string",
    "response_blocks": { "blocks": {}, "render_order": [] },
    "agent_pipeline": []
  }
}
```

### 2.5 Persist Chat History
Dung file JSON don gian trong `data/sessions/{session_id}.json` cho v1 (khong can setup PostgreSQL/Redis ngay):
```python
# Cau truc moi session
{
  "session_id": "...",
  "created_at": "...",
  "messages": [
    {"role": "user", "message": "...", "timestamp": "..."},
    {"role": "assistant", "message": "...", "metadata": {...}, "timestamp": "..."}
  ]
}
```

---

## Giai Doan 3 — Frontend Moi (4-5 ngay)

> [!NOTE]
> Frontend hien tai (App.jsx 922 dong) HOAT DONG DUOC nhung kho maintain va expand. Viet lai theo component architecture, giu nguyen UX da tested.

**Giu nguyen (da tot):**
- Layout 3 cot (left rail + chat + right rail)
- ClarificationForm — form hoi patient context
- Badge mau theo action tone (danger / caution / safe / question)
- Quick example cards

**Viet lai theo component architecture:**

```
frontend/src/
  components/
    ChatShell.jsx          Vung chat chinh + message list
    MessageBubble.jsx      1 tin nhan (user hoac bot)
    ClarificationForm.jsx  Form hoi them benh nen/tuoi
    PatientContextCard.jsx Rail trai — thong tin benh nhan
    AgentTrace.jsx         Debug panel rail phai
    QuickExamples.jsx      4 nut vi du nhanh
    SourceStrip.jsx        Danh sach nguon trich dan
  hooks/
    useChat.js             Logic gui/nhan, state messages
    useBackendStatus.js    Health check, polling
    useSession.js          Session ID, localStorage history
  App.jsx                  Layout + routing (< 80 dong)
  styles.css               Giu nguyen
```

**Tinh nang bo sung:**
- Luu lich su trong localStorage (khong mat sau khi F5)
- Nut sao chep cau tra loi
- Mobile responsive tot hon
- Dark mode toggle

---

## Giai Doan 4 — Deploy + Monitor (2-3 ngay)

### 4.1 Dockerfile Don Gian Hoa
Update `Dockerfile` hien tai:
- Khong copy `scripts/legacy/`, `data/raw/`, `data/chunks/` vao image
- Mount `data/embeddings/` tu volume ngoai (do qua lon cho image)

### 4.2 Structured Logging
Moi request log 1 dong JSON:
```json
{"ts": "...", "session_id": "...", "intent": "...", "action": "...", "confidence": 0.87, "duration_ms": 1240, "llm_used": true}
```

### 4.3 Metrics Endpoint
```
GET /api/v1/metrics
```
Tra ve JSON thong ke 24h: so luong request, phan bo intent, ty le LLM rewrite thanh cong, ty le retrieval empty.

---

## Open Questions Can Xac Nhan

> [!IMPORTANT]
> Vui long tra loi 3 cau hoi nay truoc khi bat dau Giai Doan 3:

1. **Chat history storage**: Dung file JSON don gian trong `data/sessions/` (nhanh, khong can DB setup) hay can PostgreSQL/Redis ngay tu dau?

2. **Frontend framework**: Giu Vite + React hien tai hay chuyen sang Next.js (tot hon cho SEO + SSR neu muon deploy public)?

3. **Tinh nang OCR anh hop thuoc**: Co muon them chuc nang nguoi dung chup anh → bot nhan dang ten thuoc → tu van khong? (Tang scope Giai Doan 3 them 3-4 ngay)
