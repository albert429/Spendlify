import uuid
import datetime
from data_handler import load_transactions, save_transactions

def add_transaction(username):
    """ Add a new transaction for a specific user """
    try:
        transactions = load_transactions()
        
        while True:
            amount_input = input("Enter transaction amount: ")
            try:
                amount = float(amount_input)
                if amount <= 0:
                    print("Amount must be greater than 0")
                    continue
                break
            except ValueError:
                print("Invalid amount. Please enter a numeric value")

        # Validate currency
        valid_currencies = ["USD", "EUR", "EGP", "GBP", "JPY"]
        while True:
            currency = input("Enter transaction currency (e.g., USD, EGP): ").upper()
            if currency in valid_currencies:
                break
            else:
                print(f"Invalid currency. Choose from: {', '.join(valid_currencies)}")

        # Validate category
        valid_categories = ["Food", "Transport", "Bills", "Shopping", "Other"]
        while True:
            category = input("Enter transaction category [Food, Transport, Bills, Shopping, Other]: ").capitalize()
            if category:
                if category not in valid_categories:
                    print(f"Note: '{category}' is not a known category. Using 'Other'")
                    category = "Other"
                break
            else:
                print("Category cannot be empty")

        # Validate date
        while True:
            date_str = input("Enter transaction date (YYYY-MM-DD): ")
            try:
                datetime.datetime.strptime(date_str, "%Y-%m-%d")
                date = date_str
                break
            except ValueError:
                print("Invalid date format. Please use YYYY-MM-DD.")

        # Validate description
        while True:
            description = input("Enter transaction description: ").strip()
            if len(description) > 100:
                print("Description too long (max 100 characters).")
            elif not description:
                print("Description cannot be empty.")
            else:
                break

        # Validate type
        while True:
            t_type = input("Enter transaction type (income/expense): ").lower()
            if t_type in ["income", "expense"]:
                break
            else:
                print("Invalid type. Must be 'income' or 'expense'")
                
        while True:
            payment = input("Enter payment (cash / credit card): ")
            if payment.lower() in ["cash", "credit card"]:
                break
            else:
                print("Invalid payment method. Must be 'Cash' or 'Credit Card'")
        
        transaction = {
            "id": str(uuid.uuid4()),
            "username": username,
            "amount": amount,
            "currency": currency,
            "category": category,
            "date": date,
            "description": description,
            "type": t_type,
            "payment": payment
        }
        transactions.append(transaction)
        save_transactions(transactions)
        print("Transaction saved successfully!")
    
    except Exception as e:
        print(f"Error adding transaction: {e}")

def view_transactions(username):
    """ Display all transactions belonging to a given user """
    transactions = load_transactions()
    user_transactions = [t for t in transactions if t["username"] == username]

    if not user_transactions:
        print("No transactions found for this user.")
        return
    
    print(f"{'ID':<36} | {'Amount':<10} | {'Currency':<7} | {'Category':<12} | {'Date':<12} | {'Description':<20} | {'Type':<7} | {'Payment':<10}")
    print()
    
    for t in user_transactions:
        print(f"{t['id']:<5} | {t['amount']:<10} | {t['currency']:<8} | {t['category']:<12} | {t['date']:<12} | {t['description']:<20} | {t['type']:<7} | {t['payment']}")

def delete_transaction(username):
    """ Delete a transaction by its unique ID """
    try:
        transactions = load_transactions()
        user_transactions = [t for t in transactions if t["username"] == username]

        if not user_transactions:
            print("No transactions found for this user.")
            return
        
        view_transactions(username)
        print()
        
        target = None
        id = input("Enter transaction id: ")
        for t in user_transactions:
            if t["id"].startswith(id):
                target = t
                break
        
        if not target:
            print("Transaction not found.")
            return
        
        des = input("Are you sure you want to delete this transaction? (y/n): ").lower()
        
        if des == 'y':
            transactions.remove(target)
            save_transactions(transactions)
            print("Transaction deleted successfully.")
        elif des == 'n':
            print("Skipping deleting transaction...")
        else:
            print("Invalid choice.")
    
    except Exception as e:
        print(f"Error deleting transaction: {e}")

def edit_transaction(username):
    """Edit an existing transaction for the specified user."""
    try:
        transactions = load_transactions()
        user_transactions = [t for t in transactions if t["username"] == username]

        if not user_transactions:
            print("No transactions found to edit.")
            return

        print("\nYour Transactions:")
        view_transactions(username)

        transaction_id = input("\nEnter the transaction ID to edit: ").strip()

        target_transaction = None
        for t in user_transactions:
            if t["id"].startswith(transaction_id):
                target_transaction = t
                break

        if not target_transaction:
            print("Transaction not found.")
            return

        print("\nLeave a field empty to keep the current value.\n")

        new_amount = input(f"New amount ({target_transaction['amount']}): ").strip()
        if new_amount:
            try:
                val = float(new_amount)
                if val > 0:
                    target_transaction["amount"] = val
                else:
                    print("Amount must be greater than 0. Keeping old value.")
            except ValueError:
                print("Invalid amount. Keeping old value.")

        new_currency = input(f"New currency ({target_transaction['currency']}): ").strip()
        if new_currency:
            target_transaction["currency"] = new_currency

        new_category = input(f"New category ({target_transaction['category']}): ").strip()
        if new_category:
            target_transaction["category"] = new_category

        new_date = input(f"New date ({target_transaction['date']}) (YYYY-MM-DD): ").strip()
        if new_date:
            try:
                datetime.datetime.strptime(new_date, "%Y-%m-%d")
                target_transaction["date"] = new_date
            except ValueError:
                print("Invalid date format. Keeping old value.")

        new_description = input(f"New description ({target_transaction['description']}): ").strip()
        if new_description:
            target_transaction["description"] = new_description

        new_type = input(f"New type ({target_transaction['type']}) [income/expense]: ").strip().lower()
        if new_type in ["income", "expense"]:
            target_transaction["type"] = new_type
        elif new_type:
            print("Invalid type. Keeping old value.")

        new_payment = input(f"New payment method ({target_transaction['payment']}): ").strip()
        if new_payment:
            target_transaction["payment"] = new_payment

        save_transactions(transactions)
        print("Transaction updated successfully!")

    except Exception as e:
        print(f"Error editing transaction: {e}")

def get_user_summary(username):
    """Compute total income, total expenses and net per currency for a user.

    Returns a dict keyed by currency with {'income': float, 'expense': float, 'net': float}
    """
    try:
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

def get_top_categories(username, currency=None, top_n=3):
    """Return top N spending categories for a user in the given currency.

    Returns a list of tuples: (category, amount, percent_of_total_expense)
    """
    try:
        transactions = load_transactions()
        user_transactions = [t for t in transactions if t.get('username') == username]

        # Filter expenses and by currency if provided
        expenses = [t for t in user_transactions if t.get('type', '').lower() == 'expense' and (currency is None or t.get('currency') == currency)]

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

        # Create sorted list
        sorted_cats = sorted(totals.items(), key=lambda x: x[1], reverse=True)

        result = []
        for cat, amt in sorted_cats[:top_n]:
            pct = (amt / total_expense * 100) if total_expense > 0 else 0.0
            result.append((cat, amt, pct))

        return result
    except Exception as e:
        print(f"Error computing top categories: {e}")
        return []

def category_breakdown(username, currency=None):
    try:
        transactions = load_transactions()
        user_transactions = [t for t in transactions if t.get('username') == username]

        # Filter expenses and by currency if provided
        expenses = [t for t in user_transactions if t.get('type', '').lower() == 'expense' and (currency is None or t.get('currency') == currency)]

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