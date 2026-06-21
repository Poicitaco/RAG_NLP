# Safe RAG Evaluation on `test_q.json`

Run command:

```powershell
$env:PYTHONIOENCODING='utf-8'
.\.venv\Scripts\python.exe scripts\evaluate_test_questions_safe_rag.py --quiet --output data\evaluation\test_q_safe_rag_results.json --summary-output data\evaluation\test_q_safe_rag_summary.json
```

Evaluation mode:

- 100 public-user Vietnamese questions from `test_q.json`.
- Gemini disabled for the full batch to keep the test deterministic and avoid API quota/cost.
- Chroma disabled for the full batch to avoid slow local telemetry/runtime noise; this measures the BM25 + graph + guardrail core.
- Full answers are stored in `data/evaluation/test_q_safe_rag_results.json`.
- Aggregate summary is stored in `data/evaluation/test_q_safe_rag_summary.json`.

## Summary

Total questions: 100.

RAG actions:

- `needs_clarification`: 41
- `allow`: 45
- `allow_with_caution`: 2
- `emergency`: 12

Detected intents:

- `drug_info`: 56
- `pediatric_symptom`: 6
- `high_risk_context`: 18
- `dosage`: 3
- `general_safety`: 2
- `interaction`: 1
- `counterfeit`: 2
- `emergency`: 12

Agent pipeline metrics:

- 100/100 questions include `metadata.agent_pipeline`.
- 41/100 questions triggered `needs_clarification` and bypassed retrieval until the user confirms safety context.
- 17/100 questions used deterministic drug-name alignment.
- 1/100 questions triggered graph warnings and graph-over-RAG override in the no-extra-context batch.
- Pipeline nodes observed: `safety_router`, `patient_context_collector`, `drug_name_alignment_agent`, `graph_safety_agent`, `hybrid_rag_retrieval_agent`, `evidence_guardrail_agent`, `graph_rag_join_node`, `final_response_builder`, plus emergency/clarification bypass nodes.

Graph warnings:

- 1/100 questions triggered graph warnings in this batch because the new patient-context collector stops many high-risk questions before retrieval/graph answer generation.
- Good cases:
  - ID 59: aspirin + diclofenac triggered DDInter interaction warning.
  - Diabetes + cold medicine still triggers OTC condition guardrail when patient context is provided.

Response contract:

- 100/100 responses include `metadata.response_blocks`.
- Schema version: `agent_response_v1`.
- Required render order: `safety_guardrail`, `core_action`, `clinical_reason`, `citations`.
- Each response records `selected_agents`, for example `triage_risk_agent`, `graph_safety_agent`, `pediatric_safety_agent`, `retrieval_agent`, and `final_response_builder`.

Source distribution by first citation:

- `trungtamthuoc_duocthu`: 27
- `dav_all`: 13
- `canhgiacduoc`: 6
- `ddinter`: 1
- no source: 53

## What Works

1. The system can run through all 100 questions without crashing.
2. Graph safety works for the curated diabetes/cold medicine rule.
3. Graph safety catches at least one real drug-drug interaction case: aspirin + diclofenac.
4. Emergency bypass works for explicit seizure/high-risk wording and many red flags.
5. Handoff now works for pediatric symptom requests such as ID 1, ID 7, ID 25, ID 74, and ID 83.
6. The final answer now follows the required four-block structure for every evaluated question.
7. ID 94 now uses a bisphosphonate/alendronic-acid response template when retrieved evidence supports it.
8. Deterministic name alignment now handles common public-user spellings such as Panadol/Pa-na-don and Lipitor/Li-pi-to before graph and retrieval.
9. The graph safety layer now caches DDInter and uses a normalized pair index instead of scanning the file on every interaction check.
10. The patient-context collector now asks for age, weight, disease background, allergies, and current medicines before answering high-risk OTC/dosage questions.

## Main Problems

1. The first version was too permissive; this run includes the first fix.

Before the fix, ID 1 asked for cough syrup for a 3-year-old but retrieved an
irrelevant disinfectant monograph. The current run classifies ID 1 as
`pediatric_symptom`, returns `handoff`, bypasses retrieval, and does not cite
irrelevant sources.

The emergency/pathology group improved from mostly `allow` to:

- `emergency`: 10/20
- `handoff`: 4/20
- `allow_with_caution`: 2/20
- `allow`: 4/20

2. Intent classification is still incomplete.

56/100 questions are still classified as `drug_info`, even though some may need:

- emergency triage,
- symptom red flags,
- pediatric advice,
- dosing requests,
- drug interaction checks,
- chronic disease medication safety.

This means the guardrail often treats risky questions as normal lookup questions.

3. Retrieval can still find semantically irrelevant evidence when the safety router allows retrieval.

Examples:

- ID 60 asks stomach pain after painkillers, but intent became `counterfeit` and retrieval returned unrelated sources.
- Some handoff cases still show retrieved sources in the explanation when they were not bypassed early.

4. Current graph coverage is narrow.

Graph warnings only fired on 1/100 questions in the no-extra-context batch. This is expected after adding clarification-first behavior because many risky questions now stop before graph/RAG answer generation.

Current graph coverage still only covers:

- DDInter drug-drug pairs when both drugs are detected,
- the curated diabetes + cold medicine OTC guardrail.

It does not yet cover broad symptom triage, pediatric contraindications, pregnancy, liver/kidney disease, alcohol interactions, duplicate paracetamol products, or disease-drug cautions beyond the first curated rule.

## Recommendation

Before improving UI or adding more Gemini behavior, the next engineering step should be a stronger medical-safety router before retrieval:

1. Persist patient context across turns so the second user answer continues the same consultation.
2. Expand the deterministic alignment dictionary with Vietnamese brand names and slang names from DAV/trungtamthuoc logs.
3. Convert the current keyword safety router into a labeled triage classifier and evaluate precision/recall.
4. Add curated pediatric, pregnancy, liver/kidney, diabetes, hypertension, and older-adult rules.
5. Add duplicate-ingredient and common OTC rules, especially paracetamol, NSAIDs, antihistamines, decongestants, cough/cold combinations.
6. Only allow RAG answers when retrieved evidence matches the key entities in the question.

This result is useful for the NLP report because it clearly shows why a plain RAG retriever is not enough for public medication advice: a safety router and knowledge graph must control the answer path.
