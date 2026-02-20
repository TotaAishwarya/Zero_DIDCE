# 📁 FILE: home.py
import streamlit as st
import streamlit.components.v1 as components

def run():
    # Custom Styles
    st.markdown("""
    <style>
        .hero {
            text-align: center;
            padding: 4em 2em 2em 2em;
            color: white;
        }
        .hero h1 {
            font-size: 3.2em;
            font-weight: 700;
            margin-bottom: 10px;
        }
        .hero p {
            font-size: 1.3em;
            color: #ddd;
            margin-bottom: 30px;
        }
        .logo-bar {
            display: flex;
            justify-content: center;
            gap: 60px;
            margin-top: 60px;
            flex-wrap: wrap;
            filter: grayscale(1);
            opacity: 0.8;
        }
        .logo-bar img {
            height: 40px;
        }
    </style>
    """, unsafe_allow_html=True)

    # 🌟 Hero section
    st.markdown("""
    <div class="hero">
        <h1>Maximize Your Image Quality</h1>
    </div>
    """, unsafe_allow_html=True)

    # ✅ Show enhancement button only if logged in
    # ✅ Show enhancement button only if logged in
    if st.session_state.get("logged_in", False):
        # Center button using columns
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            components.html("""
                <button style="
                    background-color: #5f27cd;
                    border: none;
                    padding: 0.75em 2em;
                    color: white;
                    font-weight: bold;
                    border-radius: 5px;
                    font-size: 1em;
                    width: 100%;
                    cursor: not-allowed;
                    opacity: 0.6;
                " disabled>✨ Try Enhancement</button>
            """, height=80)

    else:
        # Display styled warning
        st.markdown("""
        <div class="fade-container" style="
            background-color: #ffe6f0;
            border-left: 6px solid #ff6b81;
            padding: 15px 20px;
            border-radius: 10px;
            margin-top: 30px;
            text-align: center;
            color: #6f1e51;
            font-weight: 600;
            font-size: 1.1rem;
        ">
            🔒 You must <a href="#" onclick="window.parent.postMessage('go_to_login', '*'); return false;" style="color: #6f1e51; text-decoration: underline;">login</a> or 
            <a href="#" onclick="window.parent.postMessage('go_to_login', '*'); return false;" style="color: #6f1e51; text-decoration: underline;">register</a> to use the image enhancement feature.
        </div>
        """, unsafe_allow_html=True)

        components.html("""
        <script>
        window.addEventListener("message", (event) => {
            if (event.data === "go_to_login") {
                window.location.href = "/?page=🔐+Login/Register";
            }
        });
        </script>
        """, height=0)
