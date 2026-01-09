import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report
import joblib

# 1. Load dataset
df = pd.read_csv("data/expenses.csv")

X = df["description"]
y = df["category"]

# 2. Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 3. Convert text to numbers
vectorizer = CountVectorizer()
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# 4. Train model
model = MultinomialNB()
model.fit(X_train_vec, y_train)
joblib.dump(model, "models/expense_model.pkl")
joblib.dump(vectorizer, "models/vectorizer.pkl")
print("Model and vectorizer saved successfully")
# 5. Evaluate
y_pred = model.predict(X_test_vec)
print(classification_report(y_test, y_pred))

# test_sentences = [
#     "Paid charges at hospital counter",
#     "Bought food items while shopping",
#     "Subscription payment done",
#     "Travel expenses during vacation",
#     "Purchased course materials online"
# ]

# test_vec = vectorizer.transform(test_sentences)
# predictions = model.predict(test_vec)

# for s, p in zip(test_sentences, predictions):
#     print(f"{s} --> {p}")
