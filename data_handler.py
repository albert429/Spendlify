import os
import json
import shutil

USERS_FILE = "data/users.json"
TRANSACTION_FILE = 'data/transactions.csv'
BACKUP = "data/backup/"

# Save users to the JSON file
def save_users(users):
    try:
        with open(USERS_FILE, "w") as file:
            json.dump(users, file, indent=2)
    except Exception as e:
        print(f"Error saving users: {e}")
        
# Load users from the JSON file
def load_users():
    try:
        if not os.path.exists("data"):
            os.makedirs("data")
            
        if not os.path.exists(USERS_FILE):
            with open(USERS_FILE, "w") as f:
                json.dump({}, f)
            return {}
        
        with open(USERS_FILE, "r") as file:
            if os.path.getsize(USERS_FILE) == 0:
                return {}
            return json.load(file)
    except json.JSONDecodeError:
        print("Corrupted users file detected. Starting fresh...")
        return {}
    except PermissionError:
        print("Permission denied when accessing user data.")
        return {}
    except Exception as e:
        print(f"Unexpected error: {e}")
        return {}

# Save transactions in csv file
def save_transactions(transactions):
    try:
        with open(TRANSACTION_FILE, "w") as file:
            file.write("id,username,amount,currency,category,date,description,type\n")
            for t in transactions:
                line = f"{t['id']},{t['username']},{t['amount']},{t['currency']},{t['category']},{t['date']},{t['description']},{t['type']}\n"
                file.write(line)
    except Exception as e:
        print(f"Error saving transactions: {e}")

# Load transactions from csv file
def load_transactions():
    try:
        if not os.path.exists("data"):
            os.makedirs("data")
            
        if not os.path.exists(TRANSACTION_FILE):
            with open(TRANSACTION_FILE, "w") as f:
                f.write("id,username,amount,currency,category,date,description,type\n")
            return []
        with open(TRANSACTION_FILE, "r") as file:
            lines = file.readlines()[1:]  # Skip header
            transactions = []
            for line in lines:
                parts = line.strip().split(',')
                if len(parts) == 8:
                    transaction = {
                        "id": parts[0],
                        "username": parts[1],
                        "amount": float(parts[2]),
                        "currency": parts[3],
                        "category": parts[4],
                        "date": parts[5],
                        "description": parts[6],
                        "type": parts[7]
                    }
                    transactions.append(transaction)
            return transactions
    except Exception as e:
        print(f"Error loading transactions: {e}")
        return []

# Auto saving and backup the users and transactions
def auto_save(users, transactions):
    try:
        save_users(users)
        save_transactions(transactions)
        backup()
        print("Auto-save and backup completed successfully")
    except Exception as e:
        print(f"Failed to auto save or backup: {e}")

# Backup users and transactions files
def backup():
    try:
        if not os.path.exists(BACKUP):
            os.makedirs(BACKUP)
        
        # Backup users file
        if os.path.exists(USERS_FILE):
            shutil.copy2(USERS_FILE, os.path.join(BACKUP, "users_backup.json"))
            print("Users backup updated.")
        else:
            print("No users file found to backup.")
        
        # Backup transactions file
        if os.path.exists(TRANSACTION_FILE):
            shutil.copy2(TRANSACTION_FILE, os.path.join(BACKUP, "transactions_backup.csv"))
            print("Transactions backup updated.")
        else:
            print("No transactions file found to backup.")
        
        return True
    
    except Exception as e:
        print(f"Error during backup: {e}")
        return False