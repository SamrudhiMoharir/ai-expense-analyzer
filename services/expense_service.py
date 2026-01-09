from datetime import datetime
from services.database import get_connection, init_db

class ExpenseService:
    def __init__(self):
        init_db()

    def add_expense(self, date, description, category, amount):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO expenses (date, description, category, amount)
            VALUES (?, ?, ?, ?)
        """, (date, description, category, amount))

        conn.commit()
        conn.close()

    def monthly_summary(self, year, month):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT category, SUM(amount)
            FROM expenses
            WHERE strftime('%Y', date) = ?
              AND strftime('%m', date) = ?
            GROUP BY category
        """, (str(year), f"{month:02d}"))

        rows = cursor.fetchall()
        conn.close()

        return {category: total for category, total in rows}

    def saving_suggestion(self, year, month):
        summary = self.monthly_summary(year, month)

        if not summary:
            return "No expenses recorded for this month"

        total = sum(summary.values())

        for category, amount in summary.items():
            if amount / total > 0.4:
                return f"High spending on {category}. Consider setting a limit."

        return "Spending looks balanced"
