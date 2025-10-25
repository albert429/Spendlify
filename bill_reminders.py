import datetime
import uuid
from datetime import date
from data_handler import load_reminders, save_reminders

# Function to add new reminder
def add_reminder(username):
    """ Add a new reminder for a specific user """
    try:
        reminders = load_reminders()
        while True:
            title = input("Enter reminder title: ")
            if title:
                break
            else:
                print("Title cannot be empty.")
        
        while True:
            amount = input("Enter amount: ")
            try:
                amount = float(amount)
                if amount <= 0:
                    print("Amount must be greater than 0")
                    continue
                break
            except ValueError:
                print("Invalid amount. Please enter a numeric value")
                
        while True:
                deadline = input("Enter reminder deadline (YYYY-MM-DD): ")
                try:
                    datetime.strptime(deadline, "%Y-%m-%d")
                    break
                except ValueError:
                    print("Invalid date format. Please use YYYY-MM-DD.")
        
        reminder = {
            "id": str(uuid.uuid4()),
            "username": username,
            "title": title,
            "amount": amount,
            "deadline": deadline
        }
        
        reminders.append(reminder)
        save_reminders(reminders)
        print("Reminder saved successfully!")
    
    except Exception as e:
        print(f"Error adding new reminder: {e}")
    
# Function to view all user reminders
def view_reminders(username):
    """ Display all reminders belonging to a given user """
    try:
        reminders = load_reminders()   
        user_reminders = [r for r in reminders if r["username"] == username]

        if len(user_reminders) == 0:
            print(f"No reminders found for this user {username}")
            return
        else:
            print("ID | Title | Amount | Deadline")
            print()

            for reminder in user_reminders:
                print(f"{reminder['id'][:5]:<6} | {reminder['title']:<15} | {reminder['amount']:<10.2f} | {reminder['deadline']:<12}")
    
    except Exception as e:
        print(f"Error displaying reminders: {e}")
        
# function to delete reminder by username
def delete_reminder(username):
    """Delete a specific reminder for a user using its ID (short or full)."""
    try:
        reminders = load_reminders()
        user_reminders = [r for r in reminders if r["username"] == username]
        
        if not user_reminders:
            print("No reminders found to delete.")
            return

        print("\nYour Reminders:")
        view_reminders(username)

        reminder_id = input("\nEnter the reminder ID to delete: ").strip()
        
        target = None
        
        for r in user_reminders:
            # Short ID
            if r["id"].startswith(reminder_id):
                target = r
                break
        
        if not target:
            print("Reminder not found.")
            return
        
        des = input(f"Are you sure you want to delete this reminder: {target['title']}? (y/n): ").lower()
        
        if des == 'y':
            reminders.remove(target)
            save_reminders(reminders)
            print("Reminder deleted successfully.")
        elif des == 'n':
            print("Skipping deleting reminder...")
        else:
            print("Invalid choice.")
    
    except Exception as e:
        print(f"Error deleting reminder: {e}")

# Function to check reminders due automatically
def check_due_reminders(username):
    """Remind the user with the bills due date"""
    try:
        reminders = load_reminders()
        user_reminders = [r for r in reminders if r["username"] == username]
        
        if not user_reminders:
            print("No reminders found.")
            return

        today = date.today()
        
        for reminder in user_reminders:
            duedate = datetime.datetime.strptime(reminder["deadline"], "%Y-%m-%d").date()
            days_left = (duedate - today).days
            if days_left <= 5 and days_left > 1:
                print(f"{reminder['title']} due in {days_left}.")
            
            elif days_left == 0:
                print(f"{reminder['title']} due today.")
            
            elif days_left < 0:
                print(f"Overdue by {abs(days_left)}")
        
    except Exception as e:
        print(f"Error getting reminders: {e}")