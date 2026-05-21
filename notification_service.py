import random


class NotificationError(Exception):
    pass


def send_notification(user_id: int) -> bool:
    if random.randint(1, 10) > 8:
        raise NotificationError(f"Notification delivery failed for user {user_id}")

    return True
