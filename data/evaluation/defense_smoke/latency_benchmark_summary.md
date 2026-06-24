# SafeRAG Latency Benchmark

- Total runs: 1
- Mean latency: 53216.32 ms
- Median latency: 53216.32 ms
- P95 latency: 53216.32 ms
- No-source responses: 0

## Per Case

| ID | Group | Action | Sources | Latency ms |
|---|---|---:|---:|---:|
| lat_001 | drug_lookup | allow | 5 | 53216.32 |

## Pipeline Node Mean Latency

| Node | Mean ms |
|---|---:|
| hybrid_rag_retrieval_agent | 24155.82 |
| semantic_rule_mapper_agent | 14416.41 |
| drug_name_alignment_agent | 5873.2 |
| patient_context_collector | 4018.36 |
| reranker_agent | 3370.7 |
| graph_safety_agent | 1351.45 |
| safety_router | 16.16 |
| evidence_guardrail_agent | 0.71 |
| llm_intent_planner | 0.22 |
| ambiguity_checker | 0.09 |
