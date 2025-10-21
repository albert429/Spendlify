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