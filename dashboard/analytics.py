import streamlit as st
import pandas as pd

from utils.helper import render_kpi_card, bar_chart, scatter_chart


def show_analytics():

    st.title("📈 Business Analytics")

    if "df" not in st.session_state:
        st.warning("⚠ Please open Dashboard first.")
        return

    df = st.session_state["df"]

    st.success("Dataset Loaded Successfully ✅")

    # ---------------- Sales Summary ---------------- #

    st.subheader("📊 Sales Summary")

    c1, c2 = st.columns(2)

    with c1:
        render_kpi_card("📊", "Average Sales", f"₹{df['Sales'].mean():,.0f}", accent="#2DD4BF")

    with c2:
        render_kpi_card("🚀", "Maximum Sale", f"₹{df['Sales'].max():,.0f}", accent="#F5A524")

    st.divider()

    # ---------------- Profit by Category ---------------- #

    if "Category" in df.columns:
        st.subheader("📦 Profit by Category")
        category_profit = df.groupby("Category")["Profit"].sum()
        bar_chart(category_profit)

    st.divider()

    # ---------------- Sales by Region ---------------- #

    if "Region" in df.columns:
        st.subheader("🌍 Sales by Region")
        region_sales = df.groupby("Region")["Sales"].sum()
        bar_chart(region_sales)

    st.divider()

    # ---------------- Correlation ---------------- #

    st.subheader("📉 Sales vs Profit")
    scatter_chart(df[["Sales", "Profit"]], "Sales", "Profit")

    st.divider()

    # ---------------- Raw Data ---------------- #

    with st.expander("📄 View Dataset"):
        st.dataframe(df)