import streamlit as st

def create_card(title, value):

    st.markdown(f"""
    <div class="card">
        <div class="card-title">{title}</div>
        <div class="card-value">{value}</div>
    </div>
    """, unsafe_allow_html=True)


def show_cards(df):

    total_sales = df["Sales"].sum()
    total_profit = df["Profit"].sum()
    total_orders = len(df)
    total_customers = df["Customer"].nunique()

    c1,c2,c3,c4 = st.columns(4)

    with c1:
        create_card(
            "💰 Total Sales",
            f"₹{total_sales:,.0f}"
        )

    with c2:
        create_card(
            "📈 Profit",
            f"₹{total_profit:,.0f}"
        )

    with c3:
        create_card(
            "🛒 Orders",
            total_orders
        )

    with c4:
        create_card(
            "👥 Customers",
            total_customers
        )