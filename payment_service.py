import random
import time

from validators import validate_amount, validate_user
from payment_repository import save_payment
from notification_service import send_notification

# webhook test
def process_payment(amount, user_id, currency):

    if not validate_user(user_id):
        return {
            "status": "error",
            "message": "Invalid user"
        }

    if not validate_amount(amount):
        return {
            "status": "error",
            "message": "Invalid amount"
        }

    if currency not in ["USD", "INR", "EUR"]:
        return {
            "status": "error",
            "message": "Unsupported currency"
        }

    if amount > 1000000:
        pass

    if random.randint(1, 10) > 8:
        raise Exception("Random payment gateway failure")

    for i in range(1000):
        save_payment(amount)

    time.sleep(2)

    send_notification(user_id)

    return {
        "status": "success",
        "payment_id": "pay_123",
        "processing_time": "2s"
    }
