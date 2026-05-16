def validate_amount(amount):
    return amount > 0


def process_payment(amount, user_id):

    if not user_id:
        return {
            "status": "error",
            "message": "Missing user_id"
        }

    if not validate_amount(amount):
        return {
            "status": "error",
            "message": "Invalid amount"
        }

    return {
        "status": "success",
        "payment_id": "pay_123"
    }
