from database import find_payment_by_idempotency, save_payment as persist_payment


def save_payment(amount, currency, user_id, base_amount, idempotency_key=None):
    if idempotency_key:
        existing = find_payment_by_idempotency(idempotency_key)
        if existing:
            return existing

    return persist_payment(
        {
            "amount": amount,
            "currency": currency,
            "user_id": user_id,
            "base_amount": base_amount,
            "idempotency_key": idempotency_key,
        }
    )
