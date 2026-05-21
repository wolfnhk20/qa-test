import random
from typing import Any, Optional

from database import get_payment, payment_exists, refund_exists, save_refund
from validators import validate_payment_id, validate_refund_type


class RefundProcessor:
    def __init__(self, random_module=random):
        self.random = random_module

    def process_refund(
        self,
        payment_id: Any,
        amount: Any,
        refund_type: Optional[str] = "full",
        reason: Optional[str] = None,
    ) -> dict:
        if not validate_payment_id(payment_id):
            return {"status": "error", "message": "Invalid payment id"}

        if amount is None:
            return {"status": "error", "message": "Invalid refund amount"}

        try:
            amount_value = float(amount)
        except (TypeError, ValueError):
            return {"status": "error", "message": "Invalid refund amount"}

        if amount_value <= 0:
            return {"status": "error", "message": "Invalid refund amount"}

        if not validate_refund_type(refund_type):
            return {"status": "error", "message": "Invalid refund type"}

        if not payment_exists(payment_id):
            return {"status": "error", "message": "Payment not found"}

        if refund_exists(payment_id):
            return {"status": "error", "message": "Refund already processed"}

        payment = get_payment(payment_id)
        if refund_type == "partial" and amount_value >= payment.get("amount", 0):
            return {
                "status": "error",
                "message": "Partial refund must be less than payment amount",
            }

        refund = save_refund(
            {
                "payment_id": payment_id,
                "amount": amount_value,
                "refund_type": refund_type,
                "reason": reason or "general",
            }
        )

        result = {
            "status": "success",
            "refund_id": refund["refund_id"],
            "refund_type": refund_type,
        }

        if refund_type == "store_credit":
            result["store_credit"] = round(amount_value * 1.05, 2)

        if self.random.randint(1, 10) > 8:
            result["message"] = "Refund is under manual review"
            result["status"] = "pending"

        return result


def process_refund(payment_id, amount, refund_type="full", reason=None):
    processor = RefundProcessor()
    return processor.process_refund(payment_id, amount, refund_type=refund_type, reason=reason)
