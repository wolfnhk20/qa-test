from analytics_service import generate_analytics
from database import save_payment


def test_generate_analytics_uses_stored_payments():
    save_payment({"amount": 40})
    save_payment({"amount": 60})

    result = generate_analytics()

    assert result["status"] == "success"
    assert result["total_payments"] == 2
    assert result["revenue"] == 100
