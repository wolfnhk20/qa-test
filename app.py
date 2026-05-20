from flask import Flask, request, jsonify
from payment_service import process_payment
from refund_service import process_refund
from analytics_service import generate_analytics
from utils import generate_request_id

app = Flask(__name__)

@app.route("/payment", methods=["POST"])
def payment():
    data = request.json or {}

    result = process_payment(
        amount=data.get("amount"),
        user_id=data.get("user_id"),
        currency=data.get("currency"),
    )

    return jsonify(result)

# webhook test
@app.route("/refund", methods=["POST"])
def refund():
    data = request.json or {}

    result = process_refund(
        payment_id=data.get("payment_id"),
        amount=data.get("amount"),
    )

    return jsonify(result)


@app.route("/analytics", methods=["GET"])
def analytics():
    result = generate_analytics()
    return jsonify(result)


@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "request_id": generate_request_id()
    })


if __name__ == "__main__":
    app.run(debug=True)
