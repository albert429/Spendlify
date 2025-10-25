import json
import os
import hashlib
import getpass
import re
import uuid
from data_handler import save_users, load_users

SESSION_FILE = "data/session.json"

# Validate password strength
def is_strong_password(password):
    pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>\/?])[A-Za-z\d!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>\/?]{8,}$"
    return bool(re.match(pattern, password))

# Hash password using SHA-256
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Save current session
def save_session(username):
    with open(SESSION_FILE, "w") as f:
        json.dump({"current_user": username}, f)

# Load current session
def load_session():
    if not os.path.exists(SESSION_FILE):
        return None
    with open(SESSION_FILE, "r") as f:
        data = json.load(f)
        return data.get("current_user")

# Clear current session
def clear_session():
    if os.path.exists(SESSION_FILE):
        os.remove(SESSION_FILE)

# User registration
def register_user():
    users = load_users()

    full_name = input("Enter full name: ").strip()
    if not full_name:
        print("Full name cannot be empty.")
        return
    if not re.match(r"^[A-Za-z\s]{2,50}$", full_name):
        print("Full name must contain only letters and spaces (2–50 characters).")
        return

    username = input("Enter username: ").strip()
    if not username:
        print("Username cannot be empty.")
        return
    if username in users:
        print("Username already exists!")
        return
    if len(username) < 3:
        print("Username must be at least 3 characters long.")
        return
    
    currency = input("Enter preferred currency (e.g., USD, EUR, EGP): ").strip().upper()
    if not re.match(r"^[A-Z]{3}$", currency):
        print("Invalid currency format! Use 3-letter code (e.g., USD).")
        return
    
    password = getpass.getpass("Enter password: ")
    if not is_strong_password(password):
        print("Password must be at least 8 characters with uppercase, lowercase, number and special character!")
        return None
    
    confirm_password = getpass.getpass("Confirm password: ")
    if password != confirm_password:
        print("Passwords do not match.")
        return
    
    password_hash = hash_password(password)
    
    # Store user data
    users[username] = {
        "user_id": str(uuid.uuid4()),
        "full_name": full_name,
        "password_hash": password_hash,
        "currency": currency,
    }
    
    save_users(users)
    print("Registration successful!")
    return username

# User login
def login_user():
    users = load_users()
    
    # Check the username is not empty
    username = input("Username: ").strip()
    if not username:
        print("Username cannot be empty.")
        return
    
    password = getpass.getpass("Password: ")
    
    # Verify credentials
    if username in users and users[username]["password_hash"] == hash_password(password):
        print("Login successful!")
        save_session(username)
        return username
    else:
        print("Invalid username or password!")
        return

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