import yaml
import hashlib
import os

USERS_FILE = "users.yaml"

# Hash password for security
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Load users from YAML
def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r") as file:
        return yaml.safe_load(file) or {}

# Save users to YAML
def save_users(users):
    with open(USERS_FILE, "w") as file:
        yaml.dump(users, file)

# Register new user
def register_user(username, password):
    users = load_users()
    if username in users:
        return False  # Already exists
    users[username] = hash_password(password)
    save_users(users)
    return True

# Authenticate login
def authenticate_user(username, password):
    users = load_users()
    if username in users and users[username] == hash_password(password):
        return True
    return False
