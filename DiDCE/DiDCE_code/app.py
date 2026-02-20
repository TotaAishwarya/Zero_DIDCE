# 📁 FILE: app.py
import streamlit as st
import home
import enhance
import feedback
import login

if "redirect_to_login" not in st.session_state:
    st.session_state.redirect_to_login = False

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

# All pages
PAGES = {
    "🏠 Home": home,
    "✨ Enhance": enhance,
    "💬 Feedback": feedback,
    "🔐 Login/Register": login
}

# Configure page
st.set_page_config(page_title="Zero-DiDCE App", layout="wide")

# 🌸 Pastel Theme Styling
st.markdown("""
<style>
/* Fade-in animation */
.fade-container {
    animation: fadeIn 0.6s ease-in-out;
}
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}
.stApp {
    background: linear-gradient(to bottom right, #e8e6f2, #fceefc);
    color: #2f2f2f;
    font-family: 'Segoe UI', sans-serif;
}
.stRadio > div {
    display: flex;
    flex-direction: row;
    justify-content: center;
    gap: 2rem;
    background-color: #ffffffcc;
    border-radius: 12px;
    padding: 15px 20px;
    border: 1px solid #c7b1dd;
    margin-bottom: 25px;
}
.stRadio label {
    font-weight: bold;
    color: #3f3d56;
    font-size: 1.1rem;
}
.stRadio div[role='radiogroup'] > div:hover {
    background-color: #f5e6ff;
    border-radius: 8px;
}
.stButton>button {
    background-color: #cdb4db;
    color: black;
    font-weight: 500;
    border-radius: 8px;
    border: none;
}
.stButton>button:hover {
    background-color: #b197c5;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# 🔐 Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# 🧭 Navigation Bar
nav_items = list(PAGES.keys())
if st.session_state.logged_in:
    nav_items.append("🔓 Logout")

# Display top horizontal nav
selection = st.radio("🔗 Navigate to", nav_items, horizontal=True, label_visibility="collapsed")

# Route logic
import streamlit.components.v1 as components

import streamlit.components.v1 as components

import streamlit.components.v1 as components

if selection == "🔓 Logout":
    st.session_state.logged_in = False
    st.session_state.redirect_to_login = True

    # Redirect listener MUST come BEFORE stop
    components.html("""
    <script>
    window.addEventListener("message", (event) => {
        if (event.data === "redirectLogin") {
            window.parent.location.href = "/?page=🔐+Login/Register";
        }
    });
    </script>
    """, height=0)

    # Show logout toast
    components.html("""
    <div style="
        position: fixed;
        top: 40%;
        left: 50%;
        transform: translate(-50%, -50%);
        background-color: #eacff9;
        color: #5c5470;
        padding: 20px 30px;
        border-radius: 12px;
        box-shadow: 0 6px 20px rgba(0,0,0,0.15);
        font-weight: bold;
        font-size: 1.1rem;
        z-index: 9999;
        text-align: center;
    ">
        ✅ Logged out successfully!
    </div>
    <script>
        setTimeout(function() {
            window.parent.postMessage("redirectLogin", "*");
        }, 2000);
    </script>
    """, height=150)

    st.stop()


    # stop to wait before rerun
    st.stop()
    components.html("""
    <script>
    window.addEventListener("message", (event) => {
        if (event.data === "redirectLogin") {
            window.parent.location.href = "/?page=🔐+Login/Register";
        }
    });
    </script>
    """, height=0)
else:
    st.session_state.page = selection
    page = PAGES[selection]
    page.run()

