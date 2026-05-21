from database import get_analytics


def generate_analytics(start_date=None, end_date=None):
    stats = get_analytics(start_date=start_date, end_date=end_date)
    return {
        "status": "success",
        "total_payments": stats["total_payments"],
        "revenue": stats["revenue"],
        "average_payment": stats["average_payment"],
        "currency_breakdown": stats["currency_breakdown"],
        "refund_count": stats["refund_count"],
    }
