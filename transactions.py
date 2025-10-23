import uuid
from data_handler import load_transactions, save_transactions

def add_transaction(username, amount, currency, category, date, description, type):
    """ Add a new transaction for a specific user """
    try:
        transactions = load_transactions()
        transaction = {
          "id": str(uuid.uuid4()),
          "username": username,
          "amount": amount,
          "currency": currency,
          "category": category,
          "date": date,
          "description": description,
          "type": type
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
        else:
            print("Invalid choice.")
                
    except Exception as e:
        print(f"Error editing transaction: {e}")