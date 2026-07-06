import streamlit as st

from auth.login import show_login
from auth.signup import show_signup
from home import show_home

st.set_page_config(
    page_title="AI Business Intelligence Assistant",
    page_icon="🤖",
    layout="wide",
)

# Session State
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "page" not in st.session_state:
    st.session_state.page = "login"

if "user_name" not in st.session_state:
    st.session_state.user_name = ""

# Navigation
if st.session_state.logged_in:
    show_home()
else:
    if st.session_state.page == "login":
        show_login()
    else:
        show_signup()