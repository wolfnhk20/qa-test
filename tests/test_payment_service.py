import pytest

import payment_service
from payment_service import process_payment
from notification_service import NotificationError


def test_process_payment_success(monkeypatch):
    monkeypatch.setattr(payment_service, "random", type("R", (), {"randint": staticmethod(lambda a, b: 1)})())
    monkeypatch.setattr(payment_service, "send_notification", lambda user_id: True)

    result = process_payment(100, 10, "USD")

    assert result["status"] == "success"
    assert result["payment_id"] == "pay_1"
    assert "warning" not in result


def test_process_payment_rejects_unsupported_currency():
    result = process_payment(100, 10, "GBP")

    assert result["status"] == "error"
    assert result["message"] == "Unsupported currency"


def test_process_payment_rejects_invalid_amount():
    result = process_payment(0, 10, "USD")

    assert result["status"] == "error"
    assert result["message"] == "Invalid amount"


def test_process_payment_rejects_invalid_user():
    result = process_payment(100, None, "USD")

    assert result["status"] == "error"
    assert result["message"] == "Invalid user"


def test_process_payment_amount_exceeds_limit():
    result = process_payment(1_000_001, 10, "USD")

    assert result["status"] == "error"
    assert result["message"] == "Amount exceeds daily limit"


def test_process_payment_notification_failure_returns_warning(monkeypatch):
    monkeypatch.setattr(payment_service, "random", type("R", (), {"randint": staticmethod(lambda a, b: 1)})())
    def raise_notification(user_id):
        raise NotificationError("Notification delivery failed")

    monkeypatch.setattr(payment_service, "send_notification", raise_notification)

    result = process_payment(100, 10, "USD")

    assert result["status"] == "success"
    assert result["payment_id"] == "pay_1"
    assert "warning" in result
    assert "Notification delivery failed" in result["warning"]


def test_process_payment_gateway_warning(monkeypatch):
    monkeypatch.setattr(payment_service, "random", type("R", (), {"randint": staticmethod(lambda a, b: 10)})())
    monkeypatch.setattr(payment_service, "send_notification", lambda user_id: True)

    result = process_payment(100, 10, "USD")

    assert result["status"] == "success"
    assert "warning" in result
    assert "Payment gateway had a transient issue" in result["warning"]
