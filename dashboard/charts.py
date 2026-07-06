import streamlit as st
import plotly.express as px
import pandas as pd


def show_charts(df):

    # -----------------------------
    # Convert Date
    # -----------------------------
    df = df.copy()
    df["Date"] = pd.to_datetime(df["Date"])

    # -----------------------------
    # Monthly Sales
    # -----------------------------
    monthly_sales = (
        df.groupby(df["Date"].dt.to_period("M"))["Sales"]
        .sum()
        .reset_index()
    )

    monthly_sales["Date"] = monthly_sales["Date"].astype(str)

    # -----------------------------
    # Region Wise Sales
    # -----------------------------
    region_sales = (
        df.groupby("Region")["Sales"]
        .sum()
        .reset_index()
    )

    # -----------------------------
    # Category Wise Sales
    # -----------------------------
    category_sales = (
        df.groupby("Category")["Sales"]
        .sum()
        .reset_index()
    )

    # -----------------------------
    # Layout
    # -----------------------------
    col1, col2 = st.columns(2)

    # =============================
    # Line Chart
    # =============================
    with col1:

        st.subheader("📈 Monthly Sales Trend")

        line_fig = px.line(
            monthly_sales,
            x="Date",
            y="Sales",
            markers=True,
            title="Monthly Sales"
        )

        line_fig.update_layout(
            template="plotly_dark",
            height=450,
            title_x=0.25
        )

        st.plotly_chart(
            line_fig,
            use_container_width=True
        )

    # =============================
    # Pie Chart
    # =============================
    with col2:

        st.subheader("🌍 Sales by Region")

        pie_fig = px.pie(
            region_sales,
            names="Region",
            values="Sales",
            hole=0.55
        )

        pie_fig.update_layout(
            template="plotly_dark",
            height=450
        )

        st.plotly_chart(
            pie_fig,
            use_container_width=True
        )

    # =============================
    # Bar Chart
    # =============================

    st.subheader("📦 Sales by Category")

    bar_fig = px.bar(
        category_sales,
        x="Category",
        y="Sales",
        color="Category",
        text_auto=True
    )

    bar_fig.update_layout(
        template="plotly_dark",
        height=500,
        showlegend=False
    )

    st.plotly_chart(
        bar_fig,
        use_container_width=True
    )