from validators import (
    validate_amount,
    validate_currency,
    validate_idempotency_key,
    validate_payment_id,
    validate_refund_type,
    validate_user,
)


def test_validate_amount_accepts_positive_values():
    assert validate_amount(1)
    assert validate_amount("10.5")


def test_validate_amount_rejects_invalid_values():
    assert not validate_amount(0)
    assert not validate_amount(-1)
    assert not validate_amount(None)
    assert not validate_amount("abc")


def test_validate_user_accepts_valid_users():
    assert validate_user(1)
    assert validate_user("42")


def test_validate_user_rejects_invalid_users():
    assert not validate_user(None)
    assert not validate_user("abc")
    assert not validate_user(999)


def test_validate_currency():
    assert validate_currency("USD")
    assert validate_currency("EUR")
    assert not validate_currency("GBP")


def test_validate_idempotency_key():
    assert validate_idempotency_key("abc123")
    assert not validate_idempotency_key(123)
    assert not validate_idempotency_key("   ")


def test_validate_payment_id():
    assert validate_payment_id("pay_1")
    assert not validate_payment_id("payment1")


def test_validate_refund_type():
    assert validate_refund_type("partial")
    assert not validate_refund_type("double")
