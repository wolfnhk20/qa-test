from flask import Flask, request, jsonify
from payment_service import process_payment
from refund_service import process_refund
from analytics_service import generate_analytics
from utils import generate_request_id

app = Flask(__name__)


@app.route("/payment", methods=["POST"])
def payment():
    data = request.get_json(silent=True) or {}
    result = process_payment(
        amount=data.get("amount"),
        user_id=data.get("user_id"),
        currency=data.get("currency"),
        idempotency_key=data.get("idempotency_key"),
        metadata=data.get("metadata"),
    )
    status_code = 200 if result.get("status") == "success" else 400
    return jsonify(result), status_code

@app.route("/refund", methods=["POST"])
def refund():
    data = request.get_json(silent=True) or {}
    result = process_refund(
        payment_id=data.get("payment_id"),
        amount=data.get("amount"),
        refund_type=data.get("refund_type", "full"),
        reason=data.get("reason"),
    )
    status_code = 200 if result.get("status") == "success" else 400
    return jsonify(result), status_code


@app.route("/analytics", methods=["GET"])
def analytics():
    start = request.args.get("start")
    end = request.args.get("end")
    result = generate_analytics(start_date=start, end_date=end)
    return jsonify(result), 200


@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "request_id": generate_request_id(),
        "timestamp": request.environ.get("REQUEST_TIME", None),
    }), 200


if __name__ == "__main__":
    app.run(debug=True)
