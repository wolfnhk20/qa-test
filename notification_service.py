import random


def send_notification(user_id):

    if random.randint(1, 10) > 8:
        raise Exception("Notification delivery failed")

    print(f"Notification sent to user {user_id}")
# webhook test