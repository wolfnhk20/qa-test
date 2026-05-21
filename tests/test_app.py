from app import app
from database import save_payment


def test_health_endpoint_returns_ok():
    client = app.test_client()
    response = client.get("/health")

    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "ok"
    assert "request_id" in data


def test_payment_endpoint_success(monkeypatch):
    monkeypatch.setattr("payment_service.random", type("R", (), {"randint": staticmethod(lambda a, b: 1)})())
    monkeypatch.setattr("payment_service.send_notification", lambda user_id: True)

    client = app.test_client()
    response = client.post("/payment", json={"amount": 125, "user_id": 5, "currency": "USD"})

    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "success"
    assert data["payment_id"] == "pay_1"


def test_refund_endpoint_fails_for_unknown_payment():
    client = app.test_client()
    response = client.post("/refund", json={"payment_id": "pay_999", "amount": 10})

    assert response.status_code == 400
    data = response.get_json()
    assert data["status"] == "error"
    assert data["message"] == "Payment not found"


def test_analytics_endpoint_returns_totals():
    save_payment({"amount": 10})
    save_payment({"amount": 20})

    client = app.test_client()
    response = client.get("/analytics")

    assert response.status_code == 200
    data = response.get_json()
    assert data["total_payments"] == 2
    assert data["revenue"] == 30
