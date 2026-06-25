# SafeRAG Defense Scripts

Bo script nay dung de tao so lieu bao ve ma khong can sua them pipeline chinh.
Mac dinh cac script tat final LLM rewrite de ket qua on dinh; them `--use-llm`
neu muon do dung cau hinh co LLM.

## 0. Ping Kaggle Embedding API

```powershell
.\.venv\Scripts\python.exe scripts\defense_ping_kaggle_api.py
```

Output:

- `data/evaluation/defense/kaggle_api_ping.json`

Dung khi bao ve: chung minh Kaggle/Cloudflare tunnel dang tra embedding that,
co dimension 1024 va co health check GPU.

## A. Latency benchmark tu dong

```powershell
.\.venv\Scripts\python.exe scripts\defense_latency_benchmark.py --repeat 3 --use-chroma
```

Output:

- `data/evaluation/defense/latency_benchmark_details.json`
- `data/evaluation/defense/latency_benchmark_summary.json`
- `data/evaluation/defense/latency_benchmark_summary.md`

Dung khi bao ve: noi ro latency la do end-to-end SafeRAG, gom router, retrieval,
guardrail, response builder va citation.

## B. So sanh LLM thuong vs SafeRAG

Che do trung thuc mac dinh chi tao prompt baseline, khong tu nhan diem baseline:

```powershell
.\.venv\Scripts\python.exe scripts\defense_compare_llm_vs_saferag.py --baseline-mode prompt_only --use-chroma
```

Neu co `OPENAI_API_KEY` va muon chay baseline do duoc:

```powershell
$env:OPENAI_API_KEY="..."
.\.venv\Scripts\python.exe scripts\defense_compare_llm_vs_saferag.py --baseline-mode openai --openai-model gpt-4o-mini --use-chroma
```

Output:

- `data/evaluation/defense/llm_vs_saferag_comparison.json`
- `data/evaluation/defense/llm_vs_saferag_comparison.md`

Dung khi bao ve: nhan manh SafeRAG co structured citation, retrieval evidence va
guardrail; LLM thuong chi la baseline can blind/human evaluation neu muon cham diem
thuc nghiem.

## C. Chay 100 cau hoi va luu log

```powershell
.\.venv\Scripts\python.exe scripts\defense_run_100_questions.py --use-chroma
```

Output:

- `data/evaluation/defense/safe_rag_100q_details.json`
- `data/evaluation/defense/safe_rag_100q_summary.json`
- `data/evaluation/defense/safe_rag_100q_compact_log.jsonl`
- `data/evaluation/defense/safe_rag_100q_summary.md`

Dung khi bao ve: dua cac con so nhu so cau emergency, so cau can hoi lai, so phan
hoi khong co nguon, so lan graph guardrail can thiep.

## D. Failure case analysis trong LaTeX

Noi dung da nam trong:

```text
report/chapters/chapter-06.tex
```

Cac muc can chi khi bao ve:

- Gioi han benchmark va can blind test/human evaluation.
- So sanh voi baseline LLM thuan.
- Failure case analysis va cach cai thien.
- Ablation study giua BM25, hybrid retrieval, evidence guardrail va SafeRAG day du.

## E. Demo live 5 kich ban

Chay truc tiep bang FastAPI TestClient, khong can mo server:

```powershell
.\.venv\Scripts\python.exe scripts\defense_demo_live_5.py
```

Hoac neu backend dang chay:

```powershell
.\.venv\Scripts\python.exe scripts\defense_demo_live_5.py --base-url http://127.0.0.1:9998/api/v1/chat
```

Output:

- `data/evaluation/defense/live_demo_5_results.json`
- `data/evaluation/defense/live_demo_5_results.md`

Nam kich ban nen demo:

1. Qua lieu paracetamol: emergency guardrail.
2. Aspirin + diclofenac: interaction/citation.
3. Tang huyet ap + pseudoephedrine: condition guardrail.
4. Tre em bi sot: missing context, hoi lai tuoi/can nang.
5. Omeprazole truoc/sau an: cau hoi routine co nguon.
