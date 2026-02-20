import streamlit as st

def run():
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.just_logged_out = True  # Set flag for app.py

    st.experimental_rerun()  # Trigger app rerun
