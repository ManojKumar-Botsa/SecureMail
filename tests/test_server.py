from fastapi.testclient import TestClient

from server.app import app


client = TestClient(app)


def test_reset_returns_observation():
    response = client.post("/reset", json={})
    assert response.status_code == 200
    body = response.json()
    assert "observation" in body
    assert "email_text" in body["observation"]


def test_step_returns_reward_and_info():
    reset_response = client.post("/reset", json={})
    assert reset_response.status_code == 200

    response = client.post("/step", json={"label": "safe"})
    assert response.status_code == 200
    body = response.json()
    assert body["done"] is True
    assert 0.0 < body["reward"] < 1.0
    assert body["info"]["expected_label"] in {"safe", "suspicious", "phishing"}


def test_step_rejects_invalid_label():
    reset_response = client.post("/reset", json={})
    assert reset_response.status_code == 200

    response = client.post("/step", json={"label": "unknown"})
    assert response.status_code == 422
