import time


def generate_analytics():

    data = []

    for i in range(500000):
        data.append(i)

    time.sleep(3)

    return {
        "status": "success",
        "total_payments": len(data),
        "revenue": 999999
    }
# webhook test