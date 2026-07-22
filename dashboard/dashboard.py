import streamlit as st
import pandas as pd

from utils.helper import render_kpi_card, bar_chart, line_chart


def show_dashboard():

    st.title("📊 Business Dashboard")

    uploaded_file = st.file_uploader(
        "📂 Upload New Sales CSV (Optional)",
        type=["csv"]
    )

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.success("✅ Using Uploaded Dataset")
    else:
        df = pd.read_csv("data/sales_data.csv")
        st.info("📊 Using Default Dataset")

    st.session_state["df"] = df

    # ---------------- KPI Cards ---------------- #

    total_sales = df["Sales"].sum()
    total_profit = df["Profit"].sum()
    total_orders = len(df)
    total_categories = df["Category"].nunique()

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        render_kpi_card("💰", "Total Sales", f"₹{total_sales:,.0f}", accent="#2DD4BF")

    with c2:
        render_kpi_card("📈", "Total Profit", f"₹{total_profit:,.0f}", accent="#34D399")

    with c3:
        render_kpi_card("🛒", "Orders", f"{total_orders:,}", accent="#F5A524")

    with c4:
        render_kpi_card("📦", "Categories", f"{total_categories}", accent="#8B7CF6")

    st.divider()

    # ---------------- Dataset Preview ---------------- #

    st.subheader("📄 Sales Dataset")
    st.dataframe(df, use_container_width=True)

    st.divider()

    # ---------------- Sales Trend ---------------- #

    if "Date" in df.columns:
        st.subheader("📈 Sales Trend")

        chart = df.copy()
        chart["Date"] = pd.to_datetime(chart["Date"])
        chart = chart.sort_values("Date")
        trend = chart.groupby(chart["Date"].dt.to_period("M"))["Sales"].sum()
        trend.index = trend.index.astype(str)

        line_chart(trend)
        st.divider()

    # ---------------- Region Sales ---------------- #

    if "Region" in df.columns:
        st.subheader("🌍 Region-wise Sales")

        region_sales = (
            df.groupby("Region")["Sales"]
            .sum()
            .sort_values(ascending=False)
        )

        bar_chart(region_sales)
        st.dataframe(region_sales.reset_index(), use_container_width=True)
        st.divider()

    # ---------------- Category Sales ---------------- #

    if "Category" in df.columns:
        st.subheader("📦 Category-wise Sales")

        category_sales = (
            df.groupby("Category")["Sales"]
            .sum()
            .sort_values(ascending=False)
        )

        bar_chart(category_sales)
        st.dataframe(category_sales.reset_index(), use_container_width=True)
        st.divider()

    # ---------------- Category Profit ---------------- #

    if "Category" in df.columns:
        st.subheader("💹 Category-wise Profit")

        category_profit = (
            df.groupby("Category")["Profit"]
            .sum()
            .sort_values(ascending=False)
        )

        bar_chart(category_profit)
        st.dataframe(category_profit.reset_index(), use_container_width=True)
        st.divider()

    # ---------------- Top 10 Products ---------------- #

    if "Product" in df.columns:
        st.subheader("🏆 Top 10 Products")

        top_products = (
            df.groupby("Product")["Sales"]
            .sum()
            .sort_values(ascending=False)
            .head(10)
        )

        bar_chart(top_products, horizontal=True)
        st.divider()

    # ---------------- Download ---------------- #

    st.download_button(
        "📥 Download Current Dataset",
        df.to_csv(index=False),
        file_name="sales_data.csv",
        mime="text/csv"
    )