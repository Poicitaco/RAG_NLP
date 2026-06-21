// Copy generated CSV files from data/graph/neo4j_import into Neo4j import dir,
// then run this script after neo4j_schema.cypher.

LOAD CSV WITH HEADERS FROM 'file:///drugs.csv' AS row
MERGE (d:Drug {drug_id: row.drug_id})
SET d.name = row.name,
    d.normalized_name = row.normalized_name,
    d.source = row.source;

LOAD CSV WITH HEADERS FROM 'file:///ingredients.csv' AS row
MERGE (i:Ingredient {ingredient_id: row.ingredient_id})
SET i.name = row.name,
    i.normalized_name = row.normalized_name,
    i.source = row.source,
    i.source_url = row.source_url;

LOAD CSV WITH HEADERS FROM 'file:///products.csv' AS row
MERGE (p:Product {product_id: row.product_id})
SET p.registration_number = row.registration_number,
    p.name = row.name,
    p.active_ingredient_raw = row.active_ingredient_raw,
    p.strength = row.strength,
    p.dosage_form = row.dosage_form,
    p.manufacturer = row.manufacturer,
    p.source = row.source,
    p.source_url = row.source_url;

LOAD CSV WITH HEADERS FROM 'file:///conditions.csv' AS row
MERGE (c:Condition {condition_id: row.condition_id})
SET c.name = row.name,
    c.name_vi = row.name_vi,
    c.normalized_name = row.normalized_name;

LOAD CSV WITH HEADERS FROM 'file:///otc_categories.csv' AS row
MERGE (o:OTCCategory {category_id: row.category_id})
SET o.name = row.name,
    o.symptom_group = row.symptom_group;

LOAD CSV WITH HEADERS FROM 'file:///interacts_with.csv' AS row
MATCH (a:Drug {drug_id: row.from_id})
MATCH (b:Drug {drug_id: row.to_id})
MERGE (a)-[r:INTERACTS_WITH {interaction_id: row.interaction_id}]->(b)
SET r.level = row.level,
    r.source = row.source,
    r.source_url = row.source_url,
    r.license = row.license,
    r.requires_review = row.requires_review;

LOAD CSV WITH HEADERS FROM 'file:///product_has_ingredient.csv' AS row
MATCH (p:Product {product_id: row.from_id})
MATCH (i:Ingredient {ingredient_id: row.to_id})
MERGE (p)-[r:HAS_INGREDIENT]->(i)
SET r.source = row.source,
    r.registration_number = row.registration_number;

LOAD CSV WITH HEADERS FROM 'file:///ingredient_has_monograph.csv' AS row
MATCH (i:Ingredient {ingredient_id: row.from_id})
MERGE (m:Monograph {url: row.monograph_url})
SET m.title = row.title,
    m.section_count = row.section_count,
    m.trust_level = row.trust_level
MERGE (i)-[:HAS_MONOGRAPH]->(m);

LOAD CSV WITH HEADERS FROM 'file:///condition_caution_ingredient.csv' AS row
MATCH (c:Condition {condition_id: row.from_id})
MATCH (i:Ingredient {ingredient_id: row.to_id})
MERGE (c)-[r:CAUTION_FOR]->(i)
SET r.risk_level = row.risk_level,
    r.recommendation = row.recommendation,
    r.safer_options = row.safer_options,
    r.red_flags = row.red_flags,
    r.citations = row.citations,
    r.source = row.source;

LOAD CSV WITH HEADERS FROM 'file:///otc_category_caution_ingredient.csv' AS row
MATCH (o:OTCCategory {category_id: row.from_id})
MATCH (i:Ingredient {ingredient_id: row.to_id})
MERGE (o)-[r:COMMONLY_CONTAINS_CAUTION]->(i)
SET r.reason = row.reason,
    r.source = row.source;
