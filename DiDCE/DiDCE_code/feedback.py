# 📁 FILE: feedback.py

import streamlit as st
import json
import os
from datetime import datetime

FEEDBACK_FILE = "feedbacks.json"

def load_feedback():
    if os.path.exists(FEEDBACK_FILE):
        with open(FEEDBACK_FILE, "r") as f:
            return json.load(f)
    return []

def save_feedback(feedbacks):
    with open(FEEDBACK_FILE, "w") as f:
        json.dump(feedbacks, f, indent=4)

def run():
    if not st.session_state.get("logged_in", False):
        st.warning("🔐 Please login to access this page.")
        st.stop()  # ⛔ Stop execution of the rest of the page

    st.markdown("## 💬 Share Your Feedback")
    st.write("We value your input! Please let us know how we’re doing.")

    name = st.text_input("Your Name")
    email = st.text_input("Your Email")
    rating = st.slider("Rate the enhancement (1 - Worst, 5 - Best)", 1, 5, 3)
    comments = st.text_area("Comments or Suggestions")

    if st.button("Submit Feedback"):
        if not name or not email:
            st.error("Name and email are required.")
        else:
            feedbacks = load_feedback()
            feedbacks.append({
                "name": name,
                "email": email,
                "rating": rating,
                "comments": comments,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            save_feedback(feedbacks)
            st.success("✅ Thank you! Your feedback has been submitted.")

    st.markdown("---")
    if st.checkbox("📜 Show Previous Feedback"):
        feedbacks = load_feedback()
        for fb in reversed(feedbacks):
            st.markdown(f"""
            **🧑 {fb['name']}**  
            📧 {fb['email']}  
            ⭐ Rating: {fb['rating']}  
            🗒️ *"{fb['comments']}"*  
            🕒 {fb['timestamp']}
            ---
            """)
