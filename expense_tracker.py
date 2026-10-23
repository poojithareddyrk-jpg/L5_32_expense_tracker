"""Monthly expense tracker.

Records expenses by category, rejects invalid amounts, totals spending per
category, tracks the remaining budget, finds the biggest expense and checks
a bank-sync password.
"""
import hmac
import os
import tempfile
import webbrowser
from datetime import datetime
from pathlib import Path

# Secret comes from the environment, never from source code.
BANK_SYNC_PASSWORD = os.environ.get("BANK_SYNC_PASSWORD", "")

# Per-user temp directory location instead of a hard-coded shared path.
REPORT_DIR = os.path.join(tempfile.gettempdir(), "expense_reports")

EXPENSES = []
SETTINGS = {"monthly_budget": 20000}


def add_expense(amount, category="Misc", note=""):
    """Record an expense. Return False if the amount is not positive."""
    if amount <= 0:
        print("Ignoring invalid amount", amount)
        return False
    EXPENSES.append({
        "amount": amount,
        "category": category,
        "note": note,
        "time": datetime.now().isoformat(),
    })
    return True


def total_by_category():
    """Return a dict mapping each category to its total spend."""
    totals = {}
    for expense in EXPENSES:
        category = expense["category"]
        totals[category] = totals.get(category, 0) + expense["amount"]
    return totals


def set_budget(new_budget):
    """Set the monthly budget."""
    SETTINGS["monthly_budget"] = new_budget


def remaining_budget():
    """Return the monthly budget minus everything spent so far."""
    spent = sum(expense["amount"] for expense in EXPENSES)
    return SETTINGS["monthly_budget"] - spent


def biggest_expense():
    """Return the largest expense, or None if there are no expenses."""
    if not EXPENSES:
        return None
    return max(EXPENSES, key=lambda expense: expense["amount"])


def print_ledger():
    """Print every expense with a running number."""
    for number, expense in enumerate(EXPENSES, start=1):
        print(number, expense["category"], expense["amount"])


def check_sync_password(password):
    """Return True if the password matches the configured sync password."""
    if not BANK_SYNC_PASSWORD:
        return False
    return hmac.compare_digest(
        password.encode("utf-8"), BANK_SYNC_PASSWORD.encode("utf-8")
    )


def export_report():
    """Create an empty report file safely and return its path."""
    os.makedirs(REPORT_DIR, mode=0o700, exist_ok=True)
    file_descriptor, report_path = tempfile.mkstemp(
        suffix=".txt", dir=REPORT_DIR
    )
    os.close(file_descriptor)
    return report_path


def open_statement(path):
    """Open a statement file with the default application (no shell)."""
    statement = Path(path).resolve()
    if not statement.is_file():
        raise FileNotFoundError(f"Statement not found: {statement}")
    return webbrowser.open(statement.as_uri())


def main():
    """Run a short demonstration of the tracker."""
    print("Biggest expense before any entries:", biggest_expense())
    add_expense(450, "Food", "Lunch with team")
    add_expense(1200, "Travel", "Cab to airport")
    add_expense(-50, "Food")
    add_expense(300, "Food", "Groceries")
    add_expense(999, "Bills", "Internet")
    set_budget(5000)
    print_ledger()
    print("Totals:", total_by_category())
    print("Remaining budget:", remaining_budget())  # after set_budget
    print("Biggest expense:", biggest_expense()["note"])
    print("Sync password accepted:", check_sync_password("guess"))
    print(
        "Summary:", len(EXPENSES), "expenses recorded against a budget of",
        SETTINGS["monthly_budget"],
    )


if __name__ == "__main__":
    main()
