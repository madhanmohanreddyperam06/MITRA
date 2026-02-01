from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_add_and_get_qa_pair():
    # Add a new Q&A pair
    qa_data = {
        "question": "What is the admission eligibility?",
        "answer": "12th standard with minimum 60% marks"
    }
    response = client.post("/qa", json=qa_data)
    assert response.status_code == 200
    json_response = response.json()
    assert "id" in json_response
    assert json_response["message"] == "Q&A pair added successfully"

    # Get all Q&A pairs and check the added one is present
    response = client.get("/qa")
    assert response.status_code == 200
    qa_pairs = response.json()
    assert any(q["question"] == qa_data["question"] and q["answer"] == qa_data["answer"] for q in qa_pairs)

    # Get Q&A pairs filtered by question
    response = client.get("/qa", params={"question": "admission eligibility"})
    assert response.status_code == 200
    filtered_pairs = response.json()
    assert all("admission eligibility" in q["question"].lower() for q in filtered_pairs)
