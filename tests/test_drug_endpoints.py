from fastapi.testclient import TestClient

from backend.main import app


client = TestClient(app)


def test_drug_search_returns_dav_registry_matches():
    response = client.post("/api/v1/drug/search", json={"query": "paracetamol", "limit": 5})

    assert response.status_code == 200
    payload = response.json()
    assert payload["success"] is True
    assert payload["data"]["total"] > 0
    first = payload["data"]["drugs"][0]
    assert first["drug_id"]
    assert first["name"]
    assert first["source"] in {"dav_otc", "dav_all"}
    assert first["citation"]["source"] in {"dav_otc", "dav_all"}


def test_drug_detail_can_lookup_search_result_id():
    search = client.post("/api/v1/drug/search", json={"query": "paracetamol", "limit": 1}).json()
    drug_id = search["data"]["drugs"][0]["drug_id"]

    response = client.get(f"/api/v1/drug/{drug_id}")

    assert response.status_code == 200
    payload = response.json()
    assert payload["success"] is True
    assert payload["data"]["drug_id"] == drug_id
    assert payload["data"]["citation"]["section"] == "drug_registry"


def test_drug_interaction_endpoint_uses_ddinter_graph_data():
    response = client.post(
        "/api/v1/drug/check-interaction",
        json={"drugs": ["aspirin", "diclofenac"]},
    )

    assert response.status_code == 200
    payload = response.json()
    data = payload["data"]
    assert data["has_interactions"] is True
    assert data["total_interactions"] > 0
    assert data["sources"]
    assert data["severity"] in {"moderate", "high", "critical"}


def test_dosage_endpoint_is_safety_lookup_not_generated_dose():
    response = client.post(
        "/api/v1/drug/dosage-advice",
        json={"drug_name": "paracetamol", "age": 30},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["metadata"]["dosage_generated"] is False
    assert payload["metadata"]["requires_clinician_or_pharmacist"] is True
    assert payload["data"]["warnings"]
    assert payload["data"]["matched_drugs"]
