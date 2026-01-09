from flask import Flask, request, jsonify
from services.classifier_service import ExpenseClassifierService
from services.expense_service import ExpenseService

app = Flask(__name__)

classifier = ExpenseClassifierService()
expense_service = ExpenseService()

@app.route("/add-expense", methods=["POST"])
def add_expense():
    data = request.get_json()

    required = ["description", "amount", "date"]
    if not all(k in data for k in required):
        return jsonify({"error": "description, amount, date required"}), 400

    category = classifier.predict_category(data["description"])

    expense_service.add_expense(
        date=data["date"],
        description=data["description"],
        category=category,
        amount=data["amount"]
    )

    return jsonify({
        "message": "Expense added",
        "category": category
    })

@app.route("/monthly-summary", methods=["GET"])
def summary():
    year = int(request.args.get("year"))
    month = int(request.args.get("month"))

    summary = expense_service.monthly_summary(year, month)
    return jsonify(summary)

@app.route("/saving-suggestion", methods=["GET"])
def suggestion():
    year = int(request.args.get("year"))
    month = int(request.args.get("month"))

    msg = expense_service.saving_suggestion(year, month)
    return jsonify({"suggestion": msg})

if __name__ == "__main__":
    app.run(debug=True)
