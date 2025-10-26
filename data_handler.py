import os
import json
import csv
import shutil

USERS_FILE = "data/users.json"
TRANSACTION_FILE = 'data/transactions.csv'
BACKUP = "data/backup/"
GOALS_FILE = "data/goals.json"
REMINDERS_FILE = "data/reminders.json"

# Save users to the JSON file
def save_users(users):
    """Save all users to json file"""
    try:
        if not os.path.exists("data"):
            os.makedirs("data")
        
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
def auto_save(users, transactions, goals, reminders):
    """Automatically save users and transactions, then create a backup"""
    try:
        save_users(users)
        save_transactions(transactions)
        save_goals(goals)
        save_reminders(reminders)
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
        
        # Backup Goals file
        if os.path.exists(GOALS_FILE):
            shutil.copy2(GOALS_FILE, os.path.join(BACKUP, "goals_backup.csv"))
            print("Goals backup updated.")
        else:
            print("No goals file found to backup.")
        
        # Backup bills reminder file
        if os.path.exists(REMINDERS_FILE):
            shutil.copy2(REMINDERS_FILE, os.path.join(BACKUP, "reminders_backup.csv"))
            print("Reminders backup updated.")
        else:
            print("No reminders file found to backup.")
        
        return True
    
    except Exception as e:
        print(f"Error during backup: {e}")
        return False
    
# Save reminders to the JSON file
def save_reminders(reminders):
    """Save all reminders to json file"""
    try:
        if not os.path.exists("data"):
            os.makedirs("data")
        
        with open(REMINDERS_FILE, "w") as file:
            json.dump(reminders, file, indent=2)
    except Exception as e:
        print(f"Error saving reminders: {e}")
        
# Load reminders from the JSON file
def load_reminders():
    """Load all reminders from json file"""
    try:
        if not os.path.exists("data"):
            os.makedirs("data")
            
        if not os.path.exists(REMINDERS_FILE):
            with open(REMINDERS_FILE, "w") as f:
                json.dump([], f)
            return []
        
        with open(REMINDERS_FILE, "r") as file:
            if os.path.getsize(REMINDERS_FILE) == 0:
                return []
            return json.load(file)
    except json.JSONDecodeError:
        print("Corrupted reminders file detected. Starting fresh...")
        return []
    except PermissionError:
        print("Permission denied when accessing reminders data.")
        return []
    except Exception as e:
        print(f"Unexpected error: {e}")
        return []
    
# Save goals to the JSON file
def save_goals(goals):
    """Save all goals to json file"""
    try:
        if not os.path.exists("data"):
            os.makedirs("data")
            
        with open(GOALS_FILE, "w") as file:
            json.dump(goals, file, indent=2)
    except Exception as e:
        print(f"Error saving goals: {e}")
        
# Load goals from the JSON file
def load_goals():
    """Load all goals from json file"""
    try:
        if not os.path.exists("data"):
            os.makedirs("data")
            
        if not os.path.exists(GOALS_FILE):
            with open(GOALS_FILE, "w") as f:
                json.dump([], f)
            return []
        
        with open(GOALS_FILE, "r") as file:
            if os.path.getsize(GOALS_FILE) == 0:
                return []
            return json.load(file)
    except json.JSONDecodeError:
        print("Corrupted goals file detected. Starting fresh...")
        return []
    except PermissionError:
        print("Permission denied when accessing goal data.")
        return []
    except Exception as e:
        print(f"Unexpected error: {e}")
        return []

def import_transactions(username, import_path):
    """Import user's transactions from a CSV file."""
    try:
        if not os.path.exists(import_path):
            print(f"File not found: {import_path}")
            return
        
        transactions = load_transactions()
        with open(import_path, mode="r", newline='', encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                row["username"] = username
                row["amount"] = float(row.get("amount", 0))
                transactions.append(row)

        save_transactions(transactions)
        print(f"Transactions imported successfully for {username}.")
    except Exception as e:
        print(f"Error importing user transactions: {e}")


def export_transactions(username, output_path=None):
    """Export only the given user's transactions to a CSV file."""
    try:
        transactions = load_transactions()
        user_tx = [t for t in transactions if t["username"] == username]
        if not user_tx:
            print(f"No transactions found for user {username}.")
            return
        
        if not output_path:
            if not os.path.exists("exports"):
                os.makedirs("exports")
            output_path = f"exports/{username}_transactions.csv"

        with open(output_path, "w", newline='', encoding="utf-8") as file:
            fieldnames = [
                "id", "username", "amount", "currency",
                "category", "date", "description", "type", "payment"
            ]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(user_tx)

        print(f"Transactions for {username} exported to {output_path}")
    except Exception as e:
        print(f"Error exporting user transactions: {e}")