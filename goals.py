import datetime
import uuid
from data_handler import save_goals, load_goals

def add_goal(username):
    """ Add a new goal for a specific user """
    try:
        goals = load_goals()
        while True:
            title = input("Enter goal title: ")
            if title:
                break
            else:
                print("Title cannot be empty.")

        while True:
            t_amount = input("Enter target amount: ")
            try:
                target_amount = float(t_amount)
                if target_amount <= 0:
                    print("Target must be greater than 0")
                    continue
                break
            except ValueError:
                print("Invalid target amount. Please enter a numeric value")

        while True:
            c_amount = input("Enter current savings: ")
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
        
def view_goals(username):
    """ Display all goals belonging to a given user """
    try:
        goals = load_goals()   
        user_goals = [g for g in goals if g["username"] == username]

        if len(user_goals) == 0:
            print(f"No goals found for this user {username}")
            return
        else:
            print("ID | Title | Target | Current | Progress | Deadline | Status")
            print()

            for goal in user_goals:
                progress = min((goal["current_amount"] / goal["target_amount"]) * 100, 100)
                print(f"{goal['id'][:5]:<6} | {goal['title']:<15} | {goal['target_amount']:<10.2f} | {goal['current_amount']:<10.2f} | {progress:>6.1f}% | {goal['deadline']:<12} | {goal['status']}")
    
    except Exception as e:
        print(f"Error displaying goals: {e}")
