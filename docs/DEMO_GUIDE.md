# Demo Guide - Vietnamese Medication Safety Agent

This demo shows the current backend direction:

```text
Safety Router
-> Patient Context Collector
-> Drug Name Alignment
-> Graph Safety
-> Hybrid RAG
-> Evidence Guardrail
-> Final Response Builder
```

## 1. Start API

```powershell
.\.venv\Scripts\python.exe -m uvicorn backend.main:app --host 127.0.0.1 --port 8001
```

Open another PowerShell window for the demo commands.

## 2. Start Frontend

```powershell
cd frontend
npm install
npm run dev
```

Open:

```text
http://127.0.0.1:5173
```

The frontend uses `http://127.0.0.1:8001` by default. To point it at another API:

```powershell
$env:VITE_API_BASE_URL='http://127.0.0.1:8000'
npm run dev
```

## 3. Run Main Demo Flow

```powershell
$env:PYTHONIOENCODING='utf-8'
.\.venv\Scripts\python.exe scripts\demo_chat_flow.py --base-url http://127.0.0.1:8001
```

Expected scenarios:

- OTC question without context -> `needs_clarification`
- User provides age + diabetes -> bot resumes original question and warns about oral decongestants
- Aspirin + ibuprofen -> DDInter interaction warning
- Kidney disease + pain reliever -> NSAID caution
- Hypertension + cold medicine -> decongestant caution
- Shortness of breath after medicine -> emergency bypass

## 4. Full System Check

Run this before showing the demo:

```powershell
$env:PYTHONIOENCODING='utf-8'
.\.venv\Scripts\python.exe scripts\system_check.py --api-base-url http://127.0.0.1:8001 --frontend-url http://127.0.0.1:5173
```

This checks:

- API health
- Frontend shell
- CORS from frontend to backend
- Emergency guardrail
- Patient-context clarification
- Interaction warning
- Condition warning

## 5. Fast API Smoke Test

```powershell
$env:PYTHONIOENCODING='utf-8'
.\.venv\Scripts\python.exe scripts\smoke_api.py --base-url http://127.0.0.1:8001
```

## 6. Evaluation

```powershell
$env:PYTHONIOENCODING='utf-8'
.\.venv\Scripts\python.exe scripts\evaluate_test_questions_safe_rag.py --quiet --input test_q.json --output data\evaluation\test_q_safe_rag_results.json --summary-output data\evaluation\test_q_safe_rag_summary.json
```

The evaluation report is at:

```text
data/evaluation/test_q_safe_rag_report.md
```

## Demo Talking Points

- The system is not a plain RAG chatbot.
- It asks for missing patient context before risky medication advice.
- Structured graph safety warnings can override RAG evidence.
- RAG is used for evidence and citations, not as the sole safety brain.
- The LLM layer is optional and must not invent medical facts.
