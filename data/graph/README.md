# Neo4j Knowledge Graph Export

This folder contains the first graph-ready export for the medicine safety agent.

## Generate CSV files

```powershell
.\.venv\Scripts\python.exe scripts\legacy\export_neo4j_graph.py
```

Generated CSV files are written to:

```text
data/graph/neo4j_import/
```

Latest local export:

- Drug nodes: 1,939
- Ingredient nodes: 14,023
- Product nodes: 54,064
- Condition nodes: 1
- OTC category nodes: 1
- DDInter `INTERACTS_WITH` relationships: 160,235
- Product `HAS_INGREDIENT` relationships: 79,068
- Ingredient monograph links: 1,772
- Condition `CAUTION_FOR` relationships: 3

## Import into Neo4j

1. Copy all CSV files from `data/graph/neo4j_import/` into Neo4j's import directory.
2. Run `neo4j_schema.cypher`.
3. Run `neo4j_import.cypher`.

## File-backed safety smoke test

This mirrors the planned Neo4j safety query without requiring a running Neo4j server:

```powershell
.\.venv\Scripts\python.exe scripts\legacy\graph_safety_check.py "Tui bị tiểu đường, giờ muốn mua thuốc cảm thì nên tránh loại nào?"
.\.venv\Scripts\python.exe scripts\legacy\graph_safety_check.py "Tôi đang dùng warfarin có uống aspirin được không?"
```

Expected behavior:

- Diabetes + cold medicine returns oral decongestants: pseudoephedrine, phenylephrine, ephedrine.
- Warfarin + aspirin returns DDInter Major interaction.

## Integrated Safe RAG Smoke

The API-facing `SafeRagService` now runs graph safety checks before building the
RAG answer. If graph findings exist, the answer starts with a structured safety
warning and the findings are stored in response metadata under `graph_safety`.

Latest smoke output:

```text
data/evaluation/safe_rag_graph_smoke.json
```

Current generation mode is deterministic: the backend does not call ChatGPT/LLM
to write medical advice. This is intentional for the safety milestone. A future
LLM layer should only rewrite the already-approved `graph_safety` findings and
RAG citations, not invent new dosage, interaction, or contraindication claims.
