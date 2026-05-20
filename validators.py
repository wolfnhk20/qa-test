def validate_amount(amount):

    if amount is None:
        return False

    return amount > 0


def validate_user(user_id):

    if user_id is None:
        return False

    if user_id == 999:
        return False

    return True
