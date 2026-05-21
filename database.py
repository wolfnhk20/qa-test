from datetime import datetime
from typing import Dict, List, Optional

DATA_STORE: Dict[str, List[dict]] = {
    "payments": [],
    "refunds": [],
}

CURRENCY_RATES = {
    "USD": 1.0,
    "EUR": 1.10,
    "INR": 0.012,
}


def current_time() -> datetime:
    return datetime.utcnow()


def save_payment(data: dict) -> dict:
    payment = {
        "payment_id": f"pay_{len(DATA_STORE['payments']) + 1}",
        "created_at": current_time(),
        "status": "completed",
        **data,
    }
    DATA_STORE["payments"].append(payment)
    return payment


def find_payment_by_idempotency(idempotency_key: str) -> Optional[dict]:
    if not idempotency_key:
        return None

    return next(
        (payment for payment in DATA_STORE["payments"] if payment.get("idempotency_key") == idempotency_key),
        None,
    )


def get_payment(payment_id: str) -> Optional[dict]:
    return next(
        (payment for payment in DATA_STORE["payments"] if payment["payment_id"] == payment_id),
        None,
    )


def payment_exists(payment_id: str) -> bool:
    return get_payment(payment_id) is not None


def save_refund(data: dict) -> dict:
    refund = {
        "refund_id": f"refund_{len(DATA_STORE['refunds']) + 1}",
        "requested_at": current_time(),
        "status": "processed",
        **data,
    }
    DATA_STORE["refunds"].append(refund)
    return refund


def refund_exists(payment_id: str) -> bool:
    return any(refund["payment_id"] == payment_id for refund in DATA_STORE["refunds"])


def get_refund_by_payment(payment_id: str) -> Optional[dict]:
    return next(
        (refund for refund in DATA_STORE["refunds"] if refund["payment_id"] == payment_id),
        None,
    )


def parse_iso_date(value: Optional[str]) -> datetime:
    if value is None:
        raise ValueError("Missing date string")
    return datetime.fromisoformat(value)


def query_payments(start_date: Optional[str] = None, end_date: Optional[str] = None) -> List[dict]:
    if not start_date and not end_date:
        return list(DATA_STORE["payments"])

    start_dt = parse_iso_date(start_date) if start_date else datetime.min
    end_dt = parse_iso_date(end_date) if end_date else datetime.max

    return [
        payment
        for payment in DATA_STORE["payments"]
        if start_dt <= payment["created_at"] <= end_dt
    ]


def query_refunds(start_date: Optional[str] = None, end_date: Optional[str] = None) -> List[dict]:
    if not start_date and not end_date:
        return list(DATA_STORE["refunds"])

    start_dt = parse_iso_date(start_date) if start_date else datetime.min
    end_dt = parse_iso_date(end_date) if end_date else datetime.max

    return [
        refund
        for refund in DATA_STORE["refunds"]
        if start_dt <= refund["requested_at"] <= end_dt
    ]


def get_analytics(start_date: Optional[str] = None, end_date: Optional[str] = None) -> dict:
    payments = query_payments(start_date, end_date)
    refunds = query_refunds(start_date, end_date)

    total_payments = len(payments)
    revenue = sum(payment.get("base_amount", 0) for payment in payments)
    average_payment = revenue / total_payments if total_payments else 0

    currency_breakdown = {}
    for payment in payments:
        currency = payment.get("currency", "unknown")
        totals = currency_breakdown.setdefault(currency, {"count": 0, "revenue": 0})
        totals["count"] += 1
        totals["revenue"] += payment.get("amount", 0)

    return {
        "total_payments": total_payments,
        "revenue": revenue,
        "average_payment": round(average_payment, 2),
        "currency_breakdown": currency_breakdown,
        "refund_count": len(refunds),
    }


def reset_store() -> None:
    DATA_STORE["payments"].clear()
    DATA_STORE["refunds"].clear()
