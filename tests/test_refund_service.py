import refund_service
from database import save_payment
from refund_service import process_refund


def test_process_refund_success(monkeypatch):
    payment = save_payment({"amount": 250})
    monkeypatch.setattr(refund_service, "random", type("R", (), {"randint": staticmethod(lambda a, b: 1)})())

    result = process_refund(payment["payment_id"], 50)

    assert result["status"] == "success"
    assert result["refund_id"] == "refund_1"


def test_process_refund_invalid_amount():
    result = process_refund("pay_1", 0)

    assert result["status"] == "error"
    assert result["message"] == "Invalid refund amount"


def test_process_refund_payment_not_found():
    result = process_refund("pay_999", 20)

    assert result["status"] == "error"
    assert result["message"] == "Payment not found"


def test_process_refund_duplicate_refund(monkeypatch):
    payment = save_payment({"amount": 125})
    monkeypatch.setattr(refund_service, "random", type("R", (), {"randint": staticmethod(lambda a, b: 1)})())
    first_result = process_refund(payment["payment_id"], 25)

    assert first_result["status"] == "success"

    second_result = process_refund(payment["payment_id"], 25)

    assert second_result["status"] == "error"
    assert second_result["message"] == "Refund already processed"


def test_process_refund_processed_twice_message(monkeypatch):
    payment = save_payment({"amount": 300})
    monkeypatch.setattr(refund_service, "random", type("R", (), {"randint": staticmethod(lambda a, b: 8)})())

    result = process_refund(payment["payment_id"], 50)

    assert result["status"] == "success"
    assert result["refund_id"] == "refund_1"
    assert result["message"] == "Refund processed twice"
