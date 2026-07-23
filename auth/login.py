import streamlit as st
from database.database import login_user


def show_login():

    with st.container(key="login_page"):

        left, center, right = st.columns([1, 1.3, 1])

        with center:

            st.markdown(
                """
                <div class="login-brand">
                    <div class="login-logo">🤖</div>
                    <h1>Welcome Back</h1>
                    <p>Sign in to your AI Business Intelligence Assistant</p>
                </div>
                """,
                unsafe_allow_html=True
            )

            email = st.text_input("Email")
            password = st.text_input("Password", type="password")

            remember = st.checkbox("Remember Me")

            if st.button("Login", use_container_width=True, type="primary"):

                if email == "" or password == "":
                    st.error("Please fill all fields.")

                else:
                    user = login_user(email, password)

                    if user:
                        st.session_state["logged_in"] = True
                        st.session_state["user_id"] = user[0]
                        st.session_state["user_name"] = user[1]
                        st.session_state["user_email"] = user[2]

                        st.success(f"Welcome {user[1]} 🎉")

                        st.session_state["page"] = "home"
                        st.rerun()

                    else:
                        st.error("Invalid Email or Password")

            st.write("Don't have an account?")

            if st.button("Create Account", use_container_width=True):
                st.session_state["page"] = "signup"
                st.rerun()