# SafeRAG Pharma Full Defense Run Summary

Thoi diem chay: 2026-06-24, moi truong local Windows/PowerShell.

## Kaggle Embedding API

- Trang thai tong: OK.
- Endpoint embed: `/embed`.
- HTTP status: 200.
- Latency embed: 504.08 ms.
- So vector tra ve: 1.
- Chieu embedding: 1024.
- Health endpoint: `/health`.
- Health latency: 490.96 ms.
- Model: `BAAI/bge-m3`.
- Device: `cuda:0`.
- File bang chung: `data/evaluation/defense/kaggle_api_ping.json`.

## 100-Question SafeRAG Evaluation

- Tong so cau hoi: 100.
- Response block schema hop le: 100/100.
- Phan hoi khong co nguon: 0/100.
- LLM rewrite duoc tat trong lan benchmark: 0 lan dung LLM rewrite.
- Entity alignment duoc kich hoat: 13 lan.
- Graph warning duoc kich hoat: 3 lan.

### Action Counts

| Action | Count |
|---|---:|
| needs_clarification | 55 |
| allow | 26 |
| allow_with_caution | 4 |
| handoff | 2 |
| emergency | 12 |
| insufficient_evidence | 1 |

### Intent Counts

| Intent | Count |
|---|---:|
| drug_info | 40 |
| otc_recommendation | 29 |
| emergency | 12 |
| high_risk_context | 8 |
| pediatric_symptom | 6 |
| dosage | 3 |
| general_safety | 1 |
| interaction | 1 |

### First Source Counts

| First Source | Count |
|---|---:|
| system_safety_policy | 70 |
| trungtamthuoc_duocthu | 15 |
| dav_all | 11 |
| otc_condition_guardrail | 2 |
| canhgiacduoc | 1 |
| ddinter | 1 |

File bang chung:

- `data/evaluation/defense/safe_rag_100q_details.json`
- `data/evaluation/defense/safe_rag_100q_summary.json`
- `data/evaluation/defense/safe_rag_100q_compact_log.jsonl`
- `data/evaluation/defense/safe_rag_100q_summary.md`

## Latency Benchmark

- Tong so run: 8.
- Mean latency: 10319.45 ms.
- Median latency: 4043.79 ms.
- P95 latency: 40169.99 ms.
- Min latency: 88.86 ms.
- Max latency: 57701.37 ms.
- Phan hoi khong co nguon: 0/8.

### Latency Theo Nhom

| Group | Mean ms |
|---|---:|
| emergency | 88.86 |
| condition_guardrail | 459.37 |
| interaction | 2525.87 |
| dosage | 4034.93 |
| pediatric | 4052.65 |
| otc_advice | 6080.81 |
| misspelling | 7611.71 |
| drug_lookup | 57701.37 |

File bang chung:

- `data/evaluation/defense/latency_benchmark_details.json`
- `data/evaluation/defense/latency_benchmark_summary.json`
- `data/evaluation/defense/latency_benchmark_summary.md`

## LLM Thuong vs SafeRAG

- Tong case: 5.
- SafeRAG da chay: 5/5.
- SafeRAG khong co nguon: 0/5.
- SafeRAG co tin hieu an toan: 5/5.
- Baseline LLM thuong da do truc tiep bang Gemini 2.5 Flash: 5/5.
- Baseline Gemini co tin hieu an toan: 5/5.
- Baseline Gemini co citation/nguon doi soat: 0/5.
- Ket luan: Gemini co the tra loi hop ly, nhung khong co citation cau truc, khong co action trace va khong co guardrail audit nhu SafeRAG.

File bang chung:

- `data/evaluation/defense_gemini/llm_vs_saferag_comparison.json`
- `data/evaluation/defense_gemini/llm_vs_saferag_comparison.md`

## Live Demo 5 Scenarios

Da chay du 5 kich ban demo:

1. Qua lieu paracetamol.
2. Aspirin + diclofenac.
3. Tang huyet ap + pseudoephedrine.
4. Tre em bi sot thieu tuoi/can nang.
5. Omeprazole truoc/sau an.

File bang chung:

- `data/evaluation/defense/live_demo_5_results.json`
- `data/evaluation/defense/live_demo_5_results.md`

## Cach Dien Giai Khi Bao Ve

- Diem manh: he thong chay that, co corpus lon, co citation trong 100/100 cau benchmark, co emergency bypass va guardrail phan tang.
- Diem sang tao: Kaggle API tra embedding 1024 chieu tren GPU `cuda:0`, giam phu thuoc vao may local.
- Diem trung thuc khoa hoc: ket qua 0 response thieu nguon la ket qua tren benchmark 100 cau noi bo, chua thay the blind test/human evaluation.
- Diem can cai thien: latency con cao o mot so cau retrieval, nen tiep tuc toi uu cache, vector index va remote embedding pipeline.
