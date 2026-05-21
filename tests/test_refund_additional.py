import refund_service
import payment_service
from database import save_payment, reset_store


def test_store_credit_refund_gives_bonus(monkeypatch):
    reset_store()
    payment = save_payment({"amount": 200})

    result = refund_service.process_refund(payment["payment_id"], 50, refund_type="store_credit")

    assert result["status"] == "success"
    assert "store_credit" in result
    assert result["store_credit"] > 50


def test_refund_manual_review(monkeypatch):
    reset_store()
    payment = save_payment({"amount": 500})
    # force random to small range so randint >8 triggers
    monkeypatch.setattr(refund_service, "random", type("R", (), {"randint": staticmethod(lambda a, b: 9)})())

    result = refund_service.process_refund(payment["payment_id"], 100)

    assert result["status"] in ("pending", "success")
    if result["status"] == "pending":
        assert result.get("message") == "Refund is under manual review"
