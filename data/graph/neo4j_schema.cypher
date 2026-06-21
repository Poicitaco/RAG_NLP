// Neo4j schema for the pharmaceutical safety knowledge graph.
// Run this before importing CSV files from data/graph/neo4j_import.

CREATE CONSTRAINT drug_id_unique IF NOT EXISTS
FOR (d:Drug) REQUIRE d.drug_id IS UNIQUE;

CREATE CONSTRAINT ingredient_id_unique IF NOT EXISTS
FOR (i:Ingredient) REQUIRE i.ingredient_id IS UNIQUE;

CREATE CONSTRAINT product_id_unique IF NOT EXISTS
FOR (p:Product) REQUIRE p.product_id IS UNIQUE;

CREATE CONSTRAINT condition_id_unique IF NOT EXISTS
FOR (c:Condition) REQUIRE c.condition_id IS UNIQUE;

CREATE CONSTRAINT otc_category_id_unique IF NOT EXISTS
FOR (o:OTCCategory) REQUIRE o.category_id IS UNIQUE;

CREATE INDEX drug_normalized_name IF NOT EXISTS
FOR (d:Drug) ON (d.normalized_name);

CREATE INDEX ingredient_normalized_name IF NOT EXISTS
FOR (i:Ingredient) ON (i.normalized_name);
