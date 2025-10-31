import json
import os
import hashlib
import getpass
import re
import uuid
from data_handler import save_users, load_users

SESSION_FILE = "data/session.json"

def get_logged_in_user():
    """Get the currently logged in user from the session file."""
    try:
        if os.path.exists(SESSION_FILE):
            with open(SESSION_FILE, 'r') as f:
                session = json.load(f)
                return session.get('username')
    except (json.JSONDecodeError, FileNotFoundError):
        pass
    return None

# Validate password strength
def is_strong_password(password):
    pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>\/?])[A-Za-z\d!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>\/?]{8,}$"
    return bool(re.match(pattern, password))

# Hash password using SHA-256
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Save current session (use key 'username' consistently)
def save_session(username):
    os.makedirs(os.path.dirname(SESSION_FILE), exist_ok=True)
    with open(SESSION_FILE, "w") as f:
        json.dump({"username": username}, f)

# Load current session (reads the same 'username' key)
def load_session():
    if not os.path.exists(SESSION_FILE):
        return None
    try:
        with open(SESSION_FILE, "r") as f:
            data = json.load(f)
            return data.get("username")
    except (json.JSONDecodeError, FileNotFoundError):
        return None

# Clear current session
def clear_session():
    if os.path.exists(SESSION_FILE):
        os.remove(SESSION_FILE)

# User registration
def register_user(username, password, full_name, currency):
    users = load_users()

    # Validate input data
    if not full_name or not re.match(r"^[A-Za-z\s]{2,50}$", full_name):
        return {"error": "Invalid full name. Must contain only letters and spaces (2-50 characters)."}

    if not username or len(username) < 3:
        return {"error": "Username must be at least 3 characters long."}

    if username in users:
        return {"error": "Username already exists!"}

    if not currency or not re.match(r"^[A-Z]{3}$", currency):
        return {"error": "Invalid currency format! Use 3-letter code (e.g., USD)."}

    if not is_strong_password(password):
        return {"error": "Password must be at least 8 characters with uppercase, lowercase, number and special character!"}

    password_hash = hash_password(password)
    
    # Store user data
    user_data = {
        "user_id": str(uuid.uuid4()),
        "full_name": full_name,
        "password_hash": password_hash,
        "currency": currency,
    }
    users[username] = user_data
    save_users(users)

    # Return user data without password hash
    return {
        "username": username,
        "user_id": user_data["user_id"],
        "full_name": user_data["full_name"],
        "currency": user_data["currency"]
    }

# User login
def login_user(username, password):
    users = load_users()
    
    # Check credentials
    if not username or not password:
        return None

    if username in users and users[username]["password_hash"] == hash_password(password):
        user_data = users[username]
        save_session(username)
        # Return user data without password hash
        return {
            "username": username,
            "user_id": user_data["user_id"],
            "full_name": user_data["full_name"],
            "currency": user_data["currency"]
        }
    return None

# User logout    
def logout_user(current_user):
    if current_user:
        print(f"User {current_user} logged out successfully.")
        clear_session()
        return None
    print("No user is currently logged in.")
    return None

# Change user password
def change_password(username):
    users = load_users()
    if username not in users:
        print("User does not exist.")
        return
    
    current_password = getpass.getpass("Enter current password: ")
    if users[username]["password_hash"] != hash_password(current_password):
        print("Current password is incorrect.")
        return
    
    new_password = getpass.getpass("Enter new password: ")
    if not is_strong_password(new_password):
        print("Password must be at least 8 characters with uppercase, lowercase, number and special character!")
        return
    
    confirm_password = getpass.getpass("Confirm new password: ")
    if new_password != confirm_password:
        print("Passwords do not match.")
        return
    
    users[username]["password_hash"] = hash_password(new_password)
    save_users(users)
    print("Password changed successfully.")