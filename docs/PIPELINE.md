# Vietnamese Medication Safety RAG Pipeline

This document is the current canonical map for submission and maintenance. It separates the stable pipeline from exploratory scripts so the system does not keep growing through one-off rule patches.

## Runtime Flow

1. API receives `POST /api/v1/chat/`.
2. `backend/safety/evidence_guardrails.py` decides the first `intent`, `action`, and `subtype`.
3. Clinical routing rules are read from `data/config/clinical_policy.json` through `backend/policy/safety_policy_engine.py`.
4. Emergency and handoff decisions bypass full RAG, but still attach baseline safety citations and quick BM25 support citations when possible.
5. Clear interaction questions with at least two detected medicines and interaction cues go to `graph_safety_agent` before semantic mapping, patient-context collection, name alignment, or full RAG.
6. `semantic_rule_mapper_agent` maps OTC symptom/product questions to matrix rules before retrieval.
7. `patient_context_collector` asks follow-up questions before medication advice when age, disease, pregnancy, allergy, or current medication context is missing.
8. `graph_safety_agent` checks structured DDInter and OTC condition guardrails.
9. If graph safety already has structured warnings and citations, `graph_fast_path_bypass_retrieval` returns immediately without Chroma vector search.
10. Full Hybrid RAG runs only when the fast paths do not have enough evidence. Retrieval uses BM25 plus Chroma collection `pharmaceutical_local_bge_1024`; vector failures must fall back to BM25.
11. `evidence_guardrail_agent` validates retrieved evidence before answer generation.
12. Final response builder renders the 4 clinical blocks and passes `action`/`subtype`/`sources` to the frontend.

## RAG Control Rules

- Every response must return at least one citation in `sources`.
- Bypass responses use `system_safety_policy` citations and may add quick BM25 citations for the detected drug.
- Interaction precheck uses detected medicines plus cues such as `uong chung`, `dung chung`, `phoi hop`, or `tuong tac`; when DDInter has cited evidence, it bypasses semantic mapper, alignment, Chroma, and LLM rewrite.
- Graph/DDInter warnings with source URLs use `graph_fast_path` and do not wait for Chroma.
- Hybrid retrieval is for evidence discovery, not for overriding higher-priority safety policy or graph warnings.
- Chroma failures must degrade to BM25, not HTTP 500.

## Policy Layer

Add or tune clinical routing in `data/config/clinical_policy.json`.

Current policy categories:

- `paracetamol_overdose`: emergency subtype for overdose wording.
- `hypertensive_crisis`: emergency subtype for uncontrolled high blood pressure wording.
- `nsaid_gastric_risk`: high-risk context for NSAID or analgesic gastric symptoms.
- `pediatric_symptom`: pediatric symptom handoff.

Do not add a new Python branch for every new clinical phrase unless the rule requires new matching mechanics. Prefer adding terms, regex patterns, or grouped conditions to the policy file.

## Data And Indexing

Core data steps:

- `scripts/prepare_trungtamthuoc_duocthu_chunks.py`: prepares field-aware medical chunks.
- `scripts/count_chunks.py`: counts chunks with the same splitter/filter rules.
- `scripts/build_bm25_index.py`: builds BM25 index.
- `scripts/ingest_rag_corpus.py`: ingests chunks into Chroma, with skip-existing support.

Current Chroma target:

```powershell
.\.venv\Scripts\python.exe scripts\ingest_rag_corpus.py --persist-dir data/embeddings/chroma_priority --collection pharmaceutical_local_bge_1024 --provider sentence-transformers --model BAAI/bge-m3
```

## QA Entry Point

Use one orchestrator for submission checks:

```powershell
.\.venv\Scripts\python.exe scripts\eval_submission.py all
```

Fast checks:

```powershell
.\.venv\Scripts\python.exe scripts\eval_submission.py compile pipeline-smoke api-smoke
```

The orchestrator records a JSON report at `data/evaluation/submission_report.json`.

## Legacy Script Policy

Collection, OCR, profile, old smoke, and experiment scripts are stored under `scripts/legacy/`.

Do not use legacy scripts for the current submission path unless a data rebuild explicitly needs them. If a legacy command is revived, update the command path and check imports because those scripts are no longer on the default active pipeline path.
