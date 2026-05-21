import random
from typing import Any, Dict, Optional

from database import find_payment_by_idempotency
from notification_service import NotificationError, send_notification
from payment_repository import save_payment
from validators import (
    validate_amount,
    validate_currency,
    validate_idempotency_key,
    validate_user,
)

MAX_PAYMENT_AMOUNT = 1_000_000
HIGH_RISK_BASE_AMOUNT = 250_000
PROMOTION_THRESHOLD = 1_000
PROMOTION_DISCOUNT = 0.05
CURRENCY_CONVERSION = {"USD": 1.0, "EUR": 1.10, "INR": 0.012}


class PaymentProcessor:
    def __init__(self, repository=save_payment, notifier=send_notification, random_module=random):
        self.repository = repository
        self.notifier = notifier
        self.random = random_module

    def convert_to_base(self, amount: float, currency: str) -> float:
        return round(amount * CURRENCY_CONVERSION.get(currency, 1.0), 2)

    def apply_discount(self, amount: float) -> float:
        if amount >= PROMOTION_THRESHOLD:
            return round(amount * (1 - PROMOTION_DISCOUNT), 2)
        return amount

    def is_high_risk(self, user_id: int, base_amount: float) -> bool:
        return base_amount >= HIGH_RISK_BASE_AMOUNT or user_id % 2 == 1

    def process_payment(
        self,
        amount: Any,
        user_id: Any,
        currency: str,
        idempotency_key: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        if not validate_user(user_id):
            return {"status": "error", "message": "Invalid user"}

        if not validate_amount(amount):
            return {"status": "error", "message": "Invalid amount"}

        if not validate_currency(currency):
            return {"status": "error", "message": "Unsupported currency"}

        if idempotency_key is not None and not validate_idempotency_key(idempotency_key):
            return {"status": "error", "message": "Invalid idempotency key"}

        amount_value = float(amount)
        base_amount = self.convert_to_base(amount_value, currency)

        if base_amount > MAX_PAYMENT_AMOUNT:
            return {"status": "error", "message": "Amount exceeds daily limit"}

        if self.is_high_risk(int(user_id), base_amount):
            return {
                "status": "error",
                "message": "High risk transaction detected",
                "risk_code": "HIGH_RISK",
            }

        existing_payment = None
        if idempotency_key:
            existing_payment = find_payment_by_idempotency(idempotency_key)

        if existing_payment:
            return {
                "status": "success",
                "payment_id": existing_payment["payment_id"],
                "cached": True,
                "amount": existing_payment["amount"],
            }

        discounted_amount = self.apply_discount(amount_value)
        payment = self.repository(
            discounted_amount,
            currency,
            int(user_id),
            base_amount,
            idempotency_key,
        )

        response = {
            "status": "success",
            "payment_id": payment["payment_id"],
            "currency": currency,
            "amount": discounted_amount,
            "base_amount": base_amount,
        }

        if metadata:
            response["metadata"] = metadata

        try:
            self.notifier(int(user_id))
        except NotificationError as exc:
            response["warning"] = str(exc)

        if self.random.randint(1, 10) > 9:
            response["warning"] = response.get("warning", "") or "Payment gateway had a transient issue, but payment was recorded."

        return response


def process_payment(amount: Any, user_id: Any, currency: str, idempotency_key: Optional[str] = None, metadata: Optional[Dict[str, Any]] = None):
    processor = PaymentProcessor()
    return processor.process_payment(amount, user_id, currency, idempotency_key=idempotency_key, metadata=metadata)
