import datetime
import uuid
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
                deadline = input("Enter goal deadline (YYYY-MM-DD): ")
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