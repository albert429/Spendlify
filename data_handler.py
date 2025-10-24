import os
import json
import csv
import shutil

USERS_FILE = "data/users.json"
TRANSACTION_FILE = 'data/transactions.csv'
BACKUP = "data/backup/"

# Save users to the JSON file
def save_users(users):
    """Save all users to json file"""
    try:
        with open(USERS_FILE, "w") as file:
            json.dump(users, file, indent=2)
    except Exception as e:
        print(f"Error saving users: {e}")
        
# Load users from the JSON file
def load_users():
    """Load all users from json file"""
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
    """Save all transactions to CSV using DictWriter"""
    try:
        if not os.path.exists("data"):
            os.makedirs("data")
            
        fieldnames = [
            "id", "username", "amount", "currency",
            "category", "date", "description", "type", "payment"
        ]
        with open(TRANSACTION_FILE, mode="w", newline='', encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(transactions)
        
    except Exception as e:
        print(f"Error saving transactions: {e}")

# Load transactions from csv file
def load_transactions():
    """Load all transactions from CSV using DictReader"""
    try:
        if not os.path.exists("data"):
            os.makedirs("data")
            
        if not os.path.exists(TRANSACTION_FILE):
            with open(TRANSACTION_FILE, "w", newline='', encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow([
                    "id", "username", "amount", "currency",
                    "category", "date", "description", "type", "payment"
                ])
            return []
        
        transactions = []
        with open(TRANSACTION_FILE, mode="r", newline='', encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                row.setdefault("payment", "cash")
                row["amount"] = float(row["amount"]) if row["amount"] else 0.0
                transactions.append(row)
        return transactions
    except Exception as e:
        print(f"Error loading transactions: {e}")
        return []

# Auto saving and backup the users and transactions
def auto_save(users, transactions):
    """Automatically save users and transactions, then create a backup"""
    try:
        save_users(users)
        save_transactions(transactions)
        backup()
        print("Auto-save and backup completed successfully")
    except Exception as e:
        print(f"Failed to auto save or backup: {e}")

# Backup users and transactions files
def backup():
    """Create backup copies of the users and transactions data files"""
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