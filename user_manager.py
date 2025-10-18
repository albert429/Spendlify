import json
import os
import hashlib
import getpass
import re

USERS_FILE = "data/users.json"

def load_users():
    if not os.path.exists("data"):
        os.makedirs("data")
    
    if not os.path.exists(USERS_FILE):
        return {}
    
    try:
        with open(USERS_FILE, 'r') as file:
            if os.path.getsize(USERS_FILE) == 0:
                return {}
            return json.load(file)
    except (json.JSONDecodeError, Exception) as e:
        print(f"Error loading users file: {e}")
        print("Creating new users file...")
        return {}

def is_strong_password(password):
    pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>\/?])[A-Za-z\d!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>\/?]{8,}$"
    return bool(re.match(pattern, password))

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def save_users(users):
    with open(USERS_FILE, 'w') as file:
        json.dump(users, file, indent=2)

def register_user():
    users = load_users()
    
    username = input("Enter username: ").strip()
    
    if username in users:
        print("Username already exists!")
        return
    
    password = getpass.getpass("Enter password: ")

    if not is_strong_password(password):
        print("Password must be at least 8 characters with uppercase, lowercase, number and special character!")
        return None
    
    password_hash = hash_password(password)
    
    users[username] = {
        "password_hash": password_hash
    }
    
    save_users(users)
    print("Registration successful!")
    return username

def login_user():
    users = load_users()
    
    username = input("Username: ").strip()
    password = getpass.getpass("Password: ")
    
    if username in users and users[username]["password_hash"] == hash_password(password):
        print("Login successful!")
        return username
    else:
        print("Invalid username or password!")
        return