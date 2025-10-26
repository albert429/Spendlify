import datetime
import uuid
from data_handler import save_goals, load_goals

# function to add goal for specific user
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
                deadline = input("Enter goal deadline (YYYY-MM-DD): ")
                try:
                    datetime.datetime.strptime(deadline, "%Y-%m-%d")
                    break
                except ValueError:
                    print("Invalid date format. Please use YYYY-MM-DD.")
        
        if current_amount >= target_amount:
            status = "completed"
        else:
            status = "active"
            
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

# function to view all user goals      
def view_goals(username):
    """ Display all goals belonging to a given user """
    try:
        goals = load_goals()   
        user_goals = [g for g in goals if g["username"] == username]

        if len(user_goals) == 0:
            print(f"No goals found for this user {username}")
            return
        else:
            print(f"{'ID':<6} | {'Title':<15} | {'Target':<10} | {'Current':<10} | {'Progress':<7} | {'Deadline':<12} | Status")
            print()

            for goal in user_goals:
                progress = min((goal["current_amount"] / goal["target_amount"]) * 100, 100)
                print(f"{goal['id'][:5]:<6} | {goal['title']:<15} | {goal['target_amount']:<10.2f} | {goal['current_amount']:<10.2f} | {progress:>7.1f}% | {goal['deadline']:<12} | {goal['status']}")
    
    except Exception as e:
        print(f"Error displaying goals: {e}")

# function to delete user goal by username
def delete_goal(username):
    """Delete a specific goal for a user using its ID (short or full)."""
    try:
        goals = load_goals()
        user_goals = [g for g in goals if g["username"] == username]
        
        if not user_goals:
            print("No goals found to delete.")
            return

        print("\nYour Goals:")
        view_goals(username)
        
        goal_id = input("\nEnter the goal ID to delete: ").strip()
        
        target = None
        
        for g in user_goals:
            # Short ID
            if g["id"].startswith(goal_id):
                target = g
                break
        
        if not target:
            print("Goal not found.")
            return
        
        des = input(f"Are you sure you want to delete this goal: {target['title']}? (y/n): ").lower()
        
        if des == 'y':
            goals.remove(target)
            save_goals(goals)
            print("Goal deleted successfully.")
        elif des == 'n':
            print("Skipping deleting goal...")
        else:
            print("Invalid choice.")
    
    except Exception as e:
        print(f"Error deleting goal: {e}")

# Function to edit user goal
def edit_goal(username):
    """Edit an existing goal for the specified user"""
    try:
        goals = load_goals()
        user_goals = [g for g in goals if g["username"] == username]

        if not user_goals:
            print("No goals found to edit")
            return

        print("\nYour Goals:")
        view_goals(username)

        goal_id = input("\nEnter the goal ID to edit: ").strip()

        target_goal = None
        for g in user_goals:
            if g["id"].startswith(goal_id):
                target_goal = g
                break

        if not target_goal:
            print("Goal not found.")
            return

        print("\nLeave a field empty to keep the current value\n")

        new_title = input(f"New title ({target_goal['title']}): ").strip()
        if new_title:
            target_goal["title"] = new_title

        new_target = input(f"New target amount ({target_goal['target_amount']}): ").strip()
        if new_target:
            try:
                val = float(new_target)
                if val > 0:
                    target_goal["target_amount"] = val
                else:
                    print("Target amount must be greater than 0. Keeping old value")
            except ValueError:
                print("Invalid number. Keeping old value")

        new_current = input(f"New current savings ({target_goal['current_amount']}): ").strip()
        if new_current:
            try:
                val = float(new_current)
                if val >= 0:
                    target_goal["current_amount"] = val
                else:
                    print("Current amount must be >= 0. Keeping old value")
            except ValueError:
                print("Invalid number. Keeping old value")

        if target_goal["current_amount"] >= target_goal["target_amount"]:
            target_goal["status"] = "completed"
            print("This goal is now marked as completed")

        new_deadline = input(f"New deadline ({target_goal['deadline']}) (YYYY-MM-DD): ").strip()
        if new_deadline:
            try:
                datetime.datetime.strptime(new_deadline, "%Y-%m-%d")
                target_goal["deadline"] = new_deadline
            except ValueError:
                print("Invalid date format. Keeping old value")

        new_status = input(f"New status ({target_goal['status']}) [active/completed]: ").strip().lower()
        if new_status in ["active", "completed"]:
            target_goal["status"] = new_status
        elif new_status:
            print("Invalid status. Keeping old value")

        save_goals(goals)
        print("Goal updated successfully")

    except Exception as e:
        print(f"Error editing goal: {e}")
