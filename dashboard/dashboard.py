import streamlit as st
import pandas as pd


def show_dashboard():

    st.title("📊 Business Dashboard")

    uploaded_file = st.file_uploader(
        "Upload Sales CSV",
        type=["csv"]
    )

    if uploaded_file is not None:

        df = pd.read_csv(uploaded_file)

        st.success("File Uploaded Successfully ✅")

        st.dataframe(df)

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Total Sales",
                f"₹ {df['Sales'].sum():,.0f}"
            )

        with col2:
            st.metric(
                "Total Profit",
                f"₹ {df['Profit'].sum():,.0f}"
            )

        st.subheader("Sales Trend")

        st.line_chart(df["Sales"])