from flask import Flask, request, jsonify
from payment_service import process_payment
from refund_service import process_refund
from analytics_service import generate_analytics
from utils import generate_request_id

app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False


def _json_error(message, status_code=400):
    return jsonify({"status": "error", "message": message}), status_code


def _parse_json_body():
    if not request.is_json:
        return None, _json_error("Request body must be JSON")

    data = request.get_json(silent=True)
    if data is None:
        return None, _json_error("Invalid JSON payload")

    return data, None


@app.route("/payment", methods=["POST"])
def payment():
    data, error = _parse_json_body()
    if error:
        return error

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
    data, error = _parse_json_body()
    if error:
        return error

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
    result = generate_analytics(
        start_date=request.args.get("start"),
        end_date=request.args.get("end"),
    )
    return jsonify(result), 200


@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "request_id": generate_request_id(),
    }), 200


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
