import csv
from datetime import datetime
from pathlib import Path

DATA_FILE = Path("data/expenses_log.csv")

class ExpenseService:
    def __init__(self):
        if not DATA_FILE.exists():
            with open(DATA_FILE, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["date", "description", "category", "amount"])

    def add_expense(self, date, description, category, amount):
        with open(DATA_FILE, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([date, description, category, amount])

    def monthly_summary(self, year, month):
        totals = {}

        with open(DATA_FILE, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                d = datetime.strptime(row["date"], "%Y-%m-%d")
                if d.year == year and d.month == month:
                    cat = row["category"]
                    amt = float(row["amount"])
                    totals[cat] = totals.get(cat, 0) + amt

        return totals
