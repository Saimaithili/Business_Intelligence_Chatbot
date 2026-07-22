import streamlit as st
from database.database import login_user, update_password, update_profile


def show_settings():

    st.title("⚙️ Settings")

    tab1, tab2, tab3, tab4 = st.tabs(
        ["👤 Profile", "🔒 Password", "🗂 Data", "ℹ️ About"]
    )

    # ---------------- Profile ---------------- #

    with tab1:
        st.subheader("Account Information")

        current_name = st.session_state.get("user_name", "")
        current_email = st.session_state.get("user_email", "")

        with st.form("profile_form"):
            c1, c2 = st.columns(2)

            with c1:
                name_input = st.text_input("Full Name", value=current_name)

            with c2:
                email_input = st.text_input("Email", value=current_email)

            save = st.form_submit_button("💾 Save Changes")

        if save:
            name_input = name_input.strip()
            email_input = email_input.strip()

            if not name_input or not email_input:
                st.error("Name and email can't be empty.")

            elif "user_id" not in st.session_state:
                st.error("Session expired. Please log out and log in again.")

            else:
                success = update_profile(
                    st.session_state["user_id"],
                    name_input,
                    email_input
                )

                if success:
                    st.session_state["user_name"] = name_input
                    st.session_state["user_email"] = email_input
                    st.success("✅ Profile updated successfully.")
                    st.rerun()
                else:
                    st.error("That email is already used by another account.")

    # ---------------- Change Password ---------------- #

    with tab2:
        st.subheader("Change Password")

        with st.form("change_password_form", clear_on_submit=True):
            current_pw = st.text_input("Current Password", type="password")
            new_pw = st.text_input("New Password", type="password")
            confirm_pw = st.text_input("Confirm New Password", type="password")

            submitted = st.form_submit_button("Update Password")

        if submitted:
            email = st.session_state.get("user_email")

            if not current_pw or not new_pw or not confirm_pw:
                st.error("Please fill all fields.")

            elif new_pw != confirm_pw:
                st.error("New passwords do not match.")

            elif len(new_pw) < 6:
                st.error("New password should be at least 6 characters.")

            elif login_user(email, current_pw) is None:
                st.error("Current password is incorrect.")

            else:
                update_password(email, new_pw)
                st.success("✅ Password updated successfully.")

    # ---------------- Data Management ---------------- #

    with tab3:
        st.subheader("Uploaded Dataset")

        if "df" in st.session_state:
            df = st.session_state["df"]
            st.write(f"Currently loaded: **{len(df)} rows**, **{len(df.columns)} columns**")

            if st.button("🗑 Clear Uploaded Data", use_container_width=True):
                del st.session_state["df"]
                st.success("Dataset cleared. Upload a new one from Dashboard.")
                st.rerun()
        else:
            st.info("No dataset loaded yet. Go to Dashboard to upload one.")

        st.divider()

        if st.button("🧹 Clear Chat History", use_container_width=True):
            st.session_state["messages"] = []
            st.success("Chat history cleared.")

    # ---------------- About ---------------- #

    with tab4:
        st.subheader("About This App")

        st.markdown("""
**AI Business Intelligence Assistant**
Version 1.0.0

A dashboard platform for analyzing sales data through interactive
dashboards, natural-language style querying, and exportable reports.

**Tech Stack**
- Python & Streamlit
- Pandas (data analysis)
- SQLite + bcrypt (authentication)
- ReportLab & OpenPyXL (PDF / Excel report generation)
""")

        st.caption("© 2026 AI Business Intelligence Assistant")