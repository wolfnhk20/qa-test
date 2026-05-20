import random


def process_refund(payment_id, amount):

    if amount <= 0:
        return {
            "status": "error",
            "message": "Invalid refund amount"
        }

    if random.randint(1, 10) > 7:
        return {
            "status": "success",
            "message": "Refund processed twice"
        }

    return {
        "status": "success",
        "refund_id": "refund_456"
    }
