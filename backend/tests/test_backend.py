import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_endpoint():
    """Check if the backend server is running."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "LL(1) Parser Backend is running."

def test_upload_grammar():
    """Check grammar upload and parsing logic."""
    grammar_text = """E -> T E'
E' -> + T E' | eps
T -> F T'
T' -> * F T' | eps
F -> ( E ) | id"""

    response = client.post("/upload_grammar", json={"grammar": grammar_text})
    data = response.json()

    assert response.status_code == 200
    assert "FIRST" in data
    assert "FOLLOW" in data
    assert "table" in data
    assert data["grammar"]["E"][0] == "T E'"

def test_parse_input():
    """Check parsing of input string using uploaded grammar."""
    grammar_text = """E -> T E'
E' -> + T E' | eps
T -> F T'
T' -> * F T' | eps
F -> ( E ) | id"""

    # Step 1: upload grammar
    client.post("/upload_grammar", json={"grammar": grammar_text})

    # Step 2: parse input string
    response = client.post("/parse_input", json={"input": "id + id * id"})
    data = response.json()

    assert response.status_code == 200
    assert "trace" in data
    assert "parse_tree" in data
    assert "result" in data
    assert data["result"] == "Accepted"
