import datetime
import uuid
from data_handler import save_goals, load_goals

def add_goal(username):
    """ Add a new goa; for a specific user """
    try:
        goals = load_goals()
        while True:
            title = input("Enter goal title: ")
            if title:
                break
            else:
                print("Title cannot be empty.")

        while True:
            t_amount = float(input("Enter target amount: "))
            try:
                target_amount = float(t_amount)
                if target_amount <= 0:
                    print("Target must be greater than 0")
                    continue
                break
            except ValueError:
                print("Invalid target amount. Please enter a numeric value")

        while True:
            c_amount = float(input("Enter current savings: "))
            try:
                current_amount = float(c_amount)
                if current_amount < 0:
                    print("Current Amount must >= 0")
                    continue
                break
            except ValueError:
                print("Invalid current amount. Please enter a numeric value")

        while True:
                deadline = input("Enter transaction date (YYYY-MM-DD): ")
                try:
                    datetime.strptime(deadline, "%Y-%m-%d")
                    date = deadline
                    break
                except ValueError:
                    print("Invalid date format. Please use YYYY-MM-DD.")
        while True:
                status = input("Enter goal type (active/completed): ").lower()
                if status in ["active", "completed"]:
                    break
                else:
                    print("Invalid type. Must be 'active' or 'completed'")

        goal = {
        "id": str(uuid.uuid4()),
        "username": username,
        "title": title,
        "target_amount": target_amount,
        "current_amount": current_amount,
        "deadline": deadline,
        "status": status
        }
        
        goals.append(goal)
        save_goals(goals)
        print("Goals saved successfully!")
        
    except Exception as e:
        print(f"Error adding goal: {e}")