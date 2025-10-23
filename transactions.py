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
            category = input("Enter transaction category: ").capitalize()
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
                datetime.strptime(date_str, "%Y-%m-%d")
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
                print("Invalid type. Must be 'income' or 'expense'.")
        
        transaction = {
          "id": str(uuid.uuid4()),
          "username": username,
          "amount": amount,
          "currency": currency,
          "category": category,
          "date": date,
          "description": description,
          "type": t_type
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
    
    print("id | amount | currency | category | date | description | type")
    print()
    
    for t in user_transactions:
        print(f"{t['id']:<5} | {t['amount']:<10} | {t['currency']:<8} | {t['category']:<12} | {t['date']:<12} | {t['description']:<20} | {t['type']}")

def delete_transaction(id):
    """ Delete a transaction by its unique ID """
    try:
        transactions = load_transactions()
        target = None
        
        for t in transactions:
            if t["id"] == id:
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

def edit_transaction(id):
    """ Edit a specific field of a transaction by its ID """
    try: 
        target = None
        transactions = load_transactions()
        for t in transactions:
            if t["id"] == id:
                target = t
                break
            
        if not target:
            print("Transaction not found.")
            return

        view_transactions(target["username"])
        print()

        fields = {
            1: "amount",
            2: "currency",
            3: "category",
            4: "date",
            5: "description",
            6: "type"
        }
        
        print("Select a field to edit:")
        for key, value in fields.items():
            print(f"{key}. {value}")
        
        try:
            choice = int(input("Value: "))
        except ValueError:
            print("Invalid input. Please enter a number.")
            return
        field = fields.get(choice)

        if field:
            new_value = input(f"Enter new {field} value: ")
            target[field] = new_value
            save_transactions(transactions)
            print("Transaction updated.")
            view_transactions(target["username"])
        else:
            print("Invalid choice.")
            
                
    except Exception as e:
        print(f"Error editing transaction: {e}")