# Data Source Gap Analysis

This project is moving from a plain RAG chatbot toward a drug-safety agent with
Hybrid RAG, LangGraph orchestration, and a Neo4j knowledge graph. The data
strategy must therefore cover both unstructured evidence and structured safety
relations.

## Current Sources

| Source | Current Use | Strength | Limitation |
|---|---|---|---|
| DAV registry | Drug identity, registration number, ingredient, strength, dosage form | Official Vietnam drug registry | Does not provide clinical interaction graph |
| DAV recall | Recall/safety warning | Official recall evidence | Limited to recall/circulation safety |
| CanhGiacDuoc | Safety articles, ADR, counterfeit warnings | Vietnam safety context | Not a complete interaction database |
| DAV leaflet/PDF/OCR | Label/HDSD sections | Product-specific use information | OCR can corrupt numbers/units; requires review |
| TrungTamThuoc Dược thư pages | Dược thư-style monographs and general safety chapters | Covers indications, contraindications, dose, interaction, pregnancy/lactation, liver/kidney, pediatric topics | Secondary web source; critical claims must be cited and cross-checked |

## New TrungTamThuoc Dược Thư Snapshot

Collected with `scripts/collect_trungtamthuoc_duocthu.py` from the public
`sitemap_hoatchat.xml` and Dược thư landing page.

- Monograph rows: 1,800.
- Active ingredient rows: 1,772.
- General Dược thư chapters: 28.
- RAG chunks: 34,677.
- Interaction chunks: 1,467.
- Safety chunks: 6,137.
- Dosage chunks: 2,801.

Trust policy: use as `secondary_duocthu_reference`. For high-risk claims such as
dosing, drug-drug interaction, pregnancy, liver/kidney disease, pediatric use,
and overdose, keep guardrails active and prefer cross-checking with official or
curated structured sources.

## Missing Data For The Target Architecture

### 1. Structured Drug-Drug Interactions

Needed schema:

```json
{
  "ingredient_a": "Itraconazole",
  "ingredient_b": "Atorvastatin",
  "severity": "major",
  "mechanism": "...",
  "effect": "...",
  "recommendation": "...",
  "source": "...",
  "trust_level": "curated_verified"
}
```

Recommended sources:

1. DDInter 2.0: open-access DDI database with mechanism descriptions, risk
   levels, management strategies, and drug-food/drug-disease extensions.
2. DailyMed/FDA labels: official labeling sections for contraindications,
   warnings, drug interactions, pregnancy, pediatric and geriatric use.
3. DrugBank: very strong interaction data, but requires academic/commercial
   licensing for complete structured use.
4. TWOSIDES/nSIDES: large research safety-signal datasets; useful for research
   discussion, not direct patient-facing recommendations without curation.

### 2. Contraindication By Condition / Special Population

Needed entities:

- Pregnancy.
- Breastfeeding.
- Child/pediatric.
- Older adult.
- Liver impairment.
- Kidney impairment.
- Allergy/hypersensitivity.
- Peptic ulcer/bleeding risk.

Recommended sources:

1. Dược thư general chapters and monographs from the collected TrungTamThuoc
   snapshot.
2. DailyMed/FDA label sections: contraindications, warnings, use in specific
   populations.
3. DAV HDSD/PDF product labels for Vietnam-specific marketed products.

### 3. Drug Name Normalization

Needed mapping:

- Vietnamese brand name -> DAV registration.
- DAV drug -> active ingredient.
- Ingredient synonyms Vietnamese/English.
- RxNorm/RxCUI for international mappings when using foreign datasets.

Recommended sources:

1. DAV registry for Vietnam products.
2. RxNorm/RxNav APIs for normalized international drug concepts.
3. Dược thư monograph title/synonym strings.

### 4. Multimodal Recognition Data

Needed inputs:

- Product box/label images.
- Blister images.
- Prescription images.
- OCR confidence and user confirmation.

Recommended approach:

1. Start with OCR text extraction from user-uploaded image.
2. Match OCR text against DAV registry with fuzzy search.
3. Always ask user to confirm the candidate drug before safety advice.

## Recommended Next Data Milestones

1. Build drug identification layer from DAV + Dược thư synonyms.
2. Import current DAV and Dược thư monographs into Neo4j nodes.
3. Create a small curated DDI/contraindication table for the most common public
   questions.
4. Evaluate whether DDInter can be downloaded and normalized into the graph.
5. Add DailyMed as an English cross-check source for high-risk interaction and
   contraindication evidence.

## Newly Added Structured Safety Data

### DDInter public drug-drug interactions

- Source: `https://ddinter.scbdd.com/download/`
- Raw files: `data/raw/ddinter/ddinter_downloads_code_*.csv`
- Processed edges: `data/processed/ddinter_interaction_edges.jsonl`
- RAG chunks: `data/chunks/ddinter_interaction_chunks.jsonl`
- Unique edges: 160,235
- Level counts: Major 26,914; Moderate 96,675; Minor 6,833; Unknown 29,813
- License note: DDInter public downloads are marked CC-BY-NC-SA-4.0.

This is the strongest current source for Neo4j `(:Drug)-[:INTERACTS_WITH]->(:Drug)`
relationships.

### Curated OTC condition guardrails

- Source file: `data/processed/otc_condition_guardrails.jsonl`
- RAG chunks: `data/chunks/otc_condition_guardrail_chunks.jsonl`
- Initial rule: diabetes + cold/flu OTC medicines.

This rule supports public questions like: "Tui bi tieu duong, gio muon mua
thuoc cam thi nen tranh loai nao?" It flags oral decongestants such as
pseudoephedrine, phenylephrine, and ephedrine as ingredients the user should not
self-select without pharmacist/doctor advice.

Next expansion should add condition-aware OTC guardrails for hypertension,
pregnancy, breastfeeding, children, kidney disease, liver disease, peptic
ulcer/bleeding risk, asthma/COPD, and allergy history.
