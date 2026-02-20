# 📁 FILE: login.py

import streamlit as st
import hashlib
import json
import os

USER_DB = "users.json"

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    if not os.path.exists(USER_DB):
        return {}
    with open(USER_DB, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USER_DB, "w") as f:
        json.dump(users, f, indent=4)

def register_user(username, password):
    users = load_users()
    if username in users:
        return False, "Username already exists."
    users[username] = hash_password(password)
    save_users(users)
    return True, "Registration successful."

def login_user(username, password):
    users = load_users()
    hashed_pw = hash_password(password)
    if username in users and users[username] == hashed_pw:
        return True, "Login successful."
    return False, "Invalid username or password."

def run():
    st.markdown("## 🔐 Login / Register")
    option = st.radio("Choose an action:", ["Login", "Register"])

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if option == "Register":
        confirm = st.text_input("Confirm Password", type="password")
        if st.button("Register"):
            if password != confirm:
                st.error("Passwords do not match.")
            else:
                success, msg = register_user(username, password)
                if success:
                    st.success(msg)
                else:
                    st.error(msg)

    elif option == "Login":
        if st.button("Login"):
            success, msg = login_user(username, password)
            if success:
                st.success(msg)
                st.session_state["logged_in_user"] = username
                st.session_state.logged_in = True
                st.session_state.page = "🏠 Home"  # <- redirect target
                st.experimental_rerun()
            else:
                st.error(msg)

    if "logged_in_user" in st.session_state:
        st.info(f"✅ Logged in as: {st.session_state['logged_in_user']}")
