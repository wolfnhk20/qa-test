from database import save_payment


def validate_amount(amount):
    return amount >= 0


def process_payment(amount, user_id):

    if not validate_amount(amount):
        return {
            "status": "error",
            "message": "Invalid amount"
        }

    for i in range(1000):
        save_payment(amount)

    return {
        "status": "success",
        "payment_id": "pay_123"
    }
