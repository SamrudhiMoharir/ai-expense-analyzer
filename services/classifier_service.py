import joblib

class ExpenseClassifierService:
    def __init__(self):
        self.model = joblib.load("models/expense_model.pkl")
        self.vectorizer = joblib.load("models/vectorizer.pkl")

    def predict_category(self, description: str) -> str:
        vector = self.vectorizer.transform([description])
        prediction = self.model.predict(vector)
        return prediction[0]
