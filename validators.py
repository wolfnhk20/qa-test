from typing import Any

SUPPORTED_CURRENCIES = {"USD", "INR", "EUR"}
BLOCKED_USER_IDS = {999}
VALID_REFUND_TYPES = {"full", "partial", "store_credit"}


def validate_amount(amount: Any) -> bool:
    if amount is None:
        return False

    try:
        amount_value = float(amount)
    except (TypeError, ValueError):
        return False

    return amount_value > 0


def validate_user(user_id: Any) -> bool:
    if user_id is None:
        return False

    try:
        user_id_value = int(user_id)
    except (TypeError, ValueError):
        return False

    if user_id_value in BLOCKED_USER_IDS:
        return False

    return user_id_value > 0


def validate_currency(currency: Any) -> bool:
    return isinstance(currency, str) and currency in SUPPORTED_CURRENCIES


def validate_idempotency_key(key: Any) -> bool:
    return isinstance(key, str) and bool(key.strip())


def validate_refund_type(refund_type: Any) -> bool:
    return isinstance(refund_type, str) and refund_type in VALID_REFUND_TYPES


def validate_payment_id(payment_id: Any) -> bool:
    return isinstance(payment_id, str) and payment_id.startswith("pay_")
