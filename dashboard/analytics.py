import streamlit as st
import plotly.express as px


def show_analytics(df):

    st.title("📈 Business Analytics Dashboard")
    st.markdown("---")

    # ============================
    # Top Products
    # ============================

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("🏆 Top 10 Products")

        top_products = (
            df.groupby("Product")["Sales"]
            .sum()
            .sort_values(ascending=False)
            .head(10)
            .reset_index()
        )

        fig1 = px.bar(
            top_products,
            x="Product",
            y="Sales",
            color="Sales",
            text_auto=True
        )

        fig1.update_layout(
            template="plotly_dark",
            height=450
        )

        st.plotly_chart(fig1, use_container_width=True)

    # ============================
    # Top Sales Persons
    # ============================

    with col2:

        st.subheader("👨‍💼 Top Sales Persons")

        top_salesperson = (
            df.groupby("Sales_Person")["Sales"]
            .sum()
            .sort_values(ascending=False)
            .reset_index()
        )

        fig2 = px.bar(
            top_salesperson,
            x="Sales_Person",
            y="Sales",
            color="Sales",
            text_auto=True
        )

        fig2.update_layout(
            template="plotly_dark",
            height=450
        )

        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")

    # ============================
    # Payment Analysis
    # ============================

    col3, col4 = st.columns(2)

    with col3:

        st.subheader("💳 Payment Mode Analysis")

        payment = (
            df.groupby("Payment_Mode")
            .size()
            .reset_index(name="Count")
        )

        fig3 = px.pie(
            payment,
            names="Payment_Mode",
            values="Count",
            hole=0.5
        )

        fig3.update_layout(
            template="plotly_dark",
            height=420
        )

        st.plotly_chart(fig3, use_container_width=True)

    # ============================
    # Rating Analysis
    # ============================

    with col4:

        st.subheader("⭐ Customer Ratings")

        rating = (
            df.groupby("Rating")
            .size()
            .reset_index(name="Count")
        )

        fig4 = px.bar(
            rating,
            x="Rating",
            y="Count",
            color="Rating",
            text_auto=True
        )

        fig4.update_layout(
            template="plotly_dark",
            height=420
        )

        st.plotly_chart(fig4, use_container_width=True)

    st.markdown("---")

    # ============================
    # City Wise Sales
    # ============================

    st.subheader("🌆 Top 10 Cities by Sales")

    city_sales = (
        df.groupby("City")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig5 = px.bar(
        city_sales,
        x="City",
        y="Sales",
        color="Sales",
        text_auto=True
    )

    fig5.update_layout(
        template="plotly_dark",
        height=500
    )

    st.plotly_chart(fig5, use_container_width=True)