# SafeRAG Latency Benchmark

- Total runs: 8
- Mean latency: 10319.45 ms
- Median latency: 4043.79 ms
- P95 latency: 40169.99 ms
- No-source responses: 0

## Per Case

| ID | Group | Action | Sources | Latency ms |
|---|---|---:|---:|---:|
| lat_001 | drug_lookup | allow | 5 | 57701.37 |
| lat_002 | dosage | needs_clarification | 2 | 4034.93 |
| lat_003 | interaction | allow_with_caution | 1 | 2525.87 |
| lat_004 | condition_guardrail | needs_clarification | 2 | 459.37 |
| lat_005 | pediatric | needs_clarification | 2 | 4052.65 |
| lat_006 | emergency | emergency | 2 | 88.86 |
| lat_007 | misspelling | needs_clarification | 2 | 7611.71 |
| lat_008 | otc_advice | needs_clarification | 2 | 6080.81 |

## Pipeline Node Mean Latency

| Node | Mean ms |
|---|---:|
| hybrid_rag_retrieval_agent | 35485.6 |
| drug_name_alignment_agent | 6289.93 |
| patient_context_collector | 3111.4 |
| graph_safety_agent | 2778.4 |
| reranker_agent | 2282.11 |
| semantic_rule_mapper_agent | 1872.68 |
| ambiguity_checker | 4.35 |
| safety_router | 2.57 |
| evidence_guardrail_agent | 0.93 |
| llm_intent_planner | 0.24 |
