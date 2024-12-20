# utils/user_management.py

import json
import hashlib
import os

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def add_user(username, password, role='user'):
    user = {
        "username": username,
        "password": hash_password(password),
        "role": role
    }
    users = load_users()
    users.append(user)
    save_users(users)

def load_users():
    if not os.path.exists('users.json'):
        return []
    with open('users.json', 'r') as f:
        return json.load(f)

def save_users(users):
    with open('users.json', 'w') as f:
        json.dump(users, f, indent=4)