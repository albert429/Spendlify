import uuid
import datetime
from auth import get_logged_in_user
from data_handler import load_transactions, save_transactions


def _require_login():
    """Ensure user is logged in before performing any operation."""
    username = get_logged_in_user()
    if not username:
        raise PermissionError("User not logged in. Please log in first.")
    return username


def get_user_transactions(username=None):
    """Return a list of all transactions for the given username.

    If username is None, require a logged-in user via session.
    """
    try:
        if username is None:
            username = _require_login()
        transactions = load_transactions()
        user_transactions = [t for t in transactions if t.get("username") == username]
        return sorted(user_transactions, key=lambda x: x.get("date", ""), reverse=True)
    except PermissionError:
        # Not logged in
        raise
    except Exception as e:
        print(f"Error fetching transactions: {e}")
        return []


def add_transaction(data):
    """Add a new transaction for the logged-in user."""
    try:
        username = _require_login()
        transactions = load_transactions()

        # Attach username automatically
        data["username"] = username

        # Validate required fields
        required_fields = ["amount", "category", "description", "type", "currency", "date"]
        if not all(field in data for field in required_fields):
            raise ValueError("Missing required transaction fields")

        # Validate amount
        try:
            amount = float(data["amount"])
            if amount <= 0:
                raise ValueError("Amount must be greater than 0")
        except (ValueError, TypeError):
            raise ValueError("Invalid amount value")

        # Validate type
        if data["type"] not in ["income", "expense"]:
            raise ValueError("Type must be 'income' or 'expense'")

        # Create new transaction
        transaction = {
            "id": str(uuid.uuid4()),
            "timestamp": datetime.datetime.now().isoformat(),
            **data
        }

        transactions.append(transaction)
        save_transactions(transactions)
        return transaction

    except Exception as e:
        print(f"Error adding transaction: {e}")
        raise


def delete_transaction(transaction_id):
    """Delete a transaction by ID."""
    try:
        username = _require_login()
        transactions = load_transactions()
        user_transactions = [t for t in transactions if t.get("username") == username]
        remaining = [t for t in transactions if t.get("id") != transaction_id]

        if len(remaining) == len(transactions):
            print("Transaction not found or not authorized.")
            return False

        save_transactions(remaining)
        return True

    except Exception as e:
        print(f"Error deleting transaction: {e}")
        return False


def get_user_summary():
    """Compute total income, total expenses and net per currency for the logged-in user."""
    try:
        username = _require_login()
        transactions = load_transactions()
        user_transactions = [t for t in transactions if t.get('username') == username]

        summary = {}
        for t in user_transactions:
            cur = t.get('currency', 'USD')
            try:
                amt = float(t.get('amount', 0.0))
            except (TypeError, ValueError):
                amt = 0.0
            typ = t.get('type', '').lower()

            if cur not in summary:
                summary[cur] = {'income': 0.0, 'expense': 0.0, 'net': 0.0}

            if typ == 'income':
                summary[cur]['income'] += amt
                summary[cur]['net'] += amt
            else:
                summary[cur]['expense'] += amt
                summary[cur]['net'] -= amt

        return summary
    except Exception as e:
        print(f"Error computing user summary: {e}")
        return {}

def get_top_categories(currency=None, top_n=3):
    """Return top N spending categories for the logged-in user."""
    try:
        username = _require_login()
        transactions = load_transactions()
        user_transactions = [t for t in transactions if t.get('username') == username]

        # Filter expenses and by currency if provided
        expenses = [
            t for t in user_transactions
            if t.get('type', '').lower() == 'expense'
            and (currency is None or t.get('currency') == currency)
        ]

        totals = {}
        total_expense = 0.0
        for t in expenses:
            cat = t.get('category', 'Other')
            try:
                amt = float(t.get('amount', 0.0))
            except (TypeError, ValueError):
                amt = 0.0
            totals[cat] = totals.get(cat, 0.0) + amt
            total_expense += amt
            
        sorted_cats = sorted(totals.items(), key=lambda x: x[1], reverse=True)
        result = [(cat, amt, (amt / total_expense * 100) if total_expense > 0 else 0.0)
                  for cat, amt in sorted_cats[:top_n]]
        return result
    except Exception as e:
        print(f"Error computing top categories: {e}")
        return []


def category_breakdown(currency=None):
    """Get breakdown of spending by category."""
    try:
        username = _require_login()
        transactions = load_transactions()
        user_transactions = [t for t in transactions if t.get('username') == username]

        expenses = [
            t for t in user_transactions
            if t.get('type', '').lower() == 'expense'
            and (currency is None or t.get('currency') == currency)
        ]

        breakdown = {}
        for t in expenses:
            cat = t.get('category', 'Other')
            try:
                amt = float(t.get('amount', 0.0))
            except (TypeError, ValueError):
                amt = 0.0
            breakdown[cat] = breakdown.get(cat, 0.0) + amt

        return breakdown
    except Exception as e:
        print(f"Error computing category breakdown: {e}")
        return {}
