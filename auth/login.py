import streamlit as st
from database.database import login_user


def show_login():

    st.subheader("🔑 Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    remember = st.checkbox("Remember Me")

    if st.button("Login", use_container_width=True):

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

    if st.button("Create Account"):
        st.session_state["page"] = "signup"
        st.rerun()