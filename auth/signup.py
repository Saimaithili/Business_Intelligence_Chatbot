import streamlit as st
from database.database import create_user


def show_signup():

    st.subheader("📝 Create Account")

    full_name = st.text_input("Full Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    if st.button("Create Account", use_container_width=True):

        if (
            full_name == "" or
            email == "" or
            password == "" or
            confirm_password == ""
        ):
            st.error("Please fill all fields.")

        elif password != confirm_password:
            st.error("Passwords do not match.")

        else:

            success = create_user(full_name, email, password)

            if success:
                st.success("✅ Account Created Successfully!")
                st.info("Now login using your Email and Password.")

                if st.button("Go to Login"):
                    st.session_state["page"] = "login"
                    st.rerun()

            else:
                st.error("❌ Email already exists.")

    st.write("Already have an account?")

    if st.button("Login Here"):
        st.session_state["page"] = "login"
        st.rerun()