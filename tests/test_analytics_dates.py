from datetime import datetime, timedelta
import database
from analytics_service import generate_analytics


def test_analytics_date_range_filters_payments(monkeypatch):
    database.reset_store()

    # set fixed times for payments
    base = datetime.utcnow()
    t1 = base - timedelta(days=2)
    t2 = base - timedelta(days=1)
    t3 = base

    monkeypatch.setattr(database, "current_time", lambda: t1)
    database.save_payment({"amount": 10, "base_amount": 10, "currency": "USD"})

    monkeypatch.setattr(database, "current_time", lambda: t2)
    database.save_payment({"amount": 20, "base_amount": 20, "currency": "USD"})

    monkeypatch.setattr(database, "current_time", lambda: t3)
    database.save_payment({"amount": 30, "base_amount": 30, "currency": "USD"})

    start = (base - timedelta(days=1, hours=12)).isoformat()
    end = (base + timedelta(hours=1)).isoformat()

    result = generate_analytics(start_date=start, end_date=end)

    assert result["status"] == "success"
    assert result["total_payments"] == 2
    assert result["revenue"] == 50
