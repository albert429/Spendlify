import re
from auth import load_users, save_users, change_password

# Delete user account    
def delete_user(username):
    users = load_users()
    if username not in users:
        print("User does not exist.")
        return
    
    confirm = input(f"Are you sure you want to delete '{username}'? (y/n): ").strip().lower()
    if confirm == 'y':
        del users[username]
        save_users(users)
        print("User account deleted successfully.")
    else:
        print("Account deletion cancelled.")
        
# Edit user profile
def edit_user_profile(username):
    users = load_users()
    if username not in users:
        print("User does not exist.")
        return
    
    print("\n=== Edit Profile ===")
    print("1. Full Name")
    print("2. Password")
    print("3. Preferred Currency")
    
    field = input("Select field to edit (1-3): ").strip()
    
    if field == "1":
        full_name = input("Enter new full name (leave blank to keep current): ").strip()
        if full_name:
            if not re.match(r"^[A-Za-z\s]{2,50}$", full_name):
                print("Full name must contain only letters and spaces (2–50 characters).")
                return
            users[username]["full_name"] = full_name
    
    elif field == "2":
        change_password(username)
        return
    
    elif field == "3":
        currency = input("Enter new preferred currency (e.g., USD, EUR, EGP) (leave blank to keep current): ").strip().upper()
        if currency:
            if not re.match(r"^[A-Z]{3}$", currency):
                print("Invalid currency format! Use 3-letter code (e.g., USD).")
                return
            users[username]["currency"] = currency
    
    else:
        print("Invalid choice!")
        return
    
    save_users(users)
    print("Profile updated successfully.")
    
def view_user_profile(username):
    users = load_users()
    if username not in users:
        print("User does not exist.")
        return
    user = users[username]
    print("\n=== User Profile ===")
    print(f"Full Name: {user['full_name']}")
    print(f"Username: {username}")
    print(f"Preferred Currency: {user['currency']}")
    return

