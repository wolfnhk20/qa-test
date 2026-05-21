import datetime

import payment_service
from payment_service import PaymentProcessor
from database import save_payment, DATA_STORE, reset_store


class DummyRepo:
    def __init__(self):
        self.calls = []

    def __call__(self, amount, currency, user_id, base_amount, idempotency_key=None):
        payment = {
            "payment_id": f"pay_{len(DATA_STORE['payments']) + 1}",
            "amount": amount,
            "currency": currency,
            "user_id": user_id,
            "base_amount": base_amount,
            "idempotency_key": idempotency_key,
        }
        DATA_STORE["payments"].append(payment)
        self.calls.append(payment)
        return payment


def test_idempotency_key_prevents_duplicate_payment(monkeypatch):
    reset_store()
    monkeypatch.setattr(payment_service, "random", type("R", (), {"randint": staticmethod(lambda a, b: 1)})())
    repo = DummyRepo()
    processor = PaymentProcessor(repository=repo, notifier=lambda u: True, random_module=payment_service.random)

    key = "idem-123"
    first = processor.process_payment(100, 2, "USD", idempotency_key=key)
    second = processor.process_payment(100, 2, "USD", idempotency_key=key)

    assert first["status"] == "success"
    assert second["status"] == "success"
    assert first["payment_id"] == second["payment_id"]
    assert len(repo.calls) == 1


def test_high_risk_detection_blocks_odd_user_ids(monkeypatch):
    reset_store()
    repo = DummyRepo()
    processor = PaymentProcessor(repository=repo, notifier=lambda u: True, random_module=payment_service.random)

    # odd user id should be considered high risk by default logic
    result = processor.process_payment(50, 3, "USD")
    assert result["status"] == "error"
    assert result.get("risk_code") == "HIGH_RISK"

    # even user id and small amount should pass
    result2 = processor.process_payment(50, 4, "USD")
    assert result2["status"] == "success"


def test_promotion_discount_applies_at_threshold(monkeypatch):
    reset_store()
    repo = DummyRepo()
    processor = PaymentProcessor(repository=repo, notifier=lambda u: True, random_module=payment_service.random)

    result = processor.process_payment(1500, 2, "USD")
    assert result["status"] == "success"
    assert result["amount"] < 1500
