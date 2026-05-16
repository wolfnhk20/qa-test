from flask import Flask, request, jsonify
from payment_service import process_payment

app = Flask(__name__)

@app.route("/payment", methods=["POST"])
def payment():
    data = request.json

    result = process_payment(
        data.get("amount"),
        data.get("user_id")
    )

    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
