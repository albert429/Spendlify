import uuid
from data_handler import load_transactions, save_transactions

def add_transaction(username, amount, currency, category, date, description, type):
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
    
def view_transactions(username):
    transactions = load_transactions()
    user_transactions = [t for t in transactions if t["username"] == username]

    if not user_transactions:
        print("No transactions found for this user.")
        return
    
    print("id | amount | currency | category | date | description | type")
    print()
    
    for t in user_transactions:
        print(f"{t['id']:<5} | {t['amount']:<10} | {t['currency']:<8} | {t['category']:<12} | {t['date']:<12} | {t['description']:<20} | {t['type']}")
    