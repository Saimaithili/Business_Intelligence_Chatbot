import streamlit as st

def show_chatbot(df):

    st.title("🤖 AI Business Assistant")

    question = st.text_input(
        "Ask your business question"
    )

    if question == "":
        return

    q = question.lower()

    # -----------------------------
    # Total Sales
    # -----------------------------

    if "total sales" in q:

        total = df["Sales"].sum()

        st.success(
            f"💰 Total Sales : ₹{total:,.0f}"
        )

    # -----------------------------
    # Highest Region
    # -----------------------------

    elif "highest sales" in q and "region" in q:

        region = (
            df.groupby("Region")["Sales"]
            .sum()
            .idxmax()
        )

        value = (
            df.groupby("Region")["Sales"]
            .sum()
            .max()
        )

        st.success(
            f"🏆 {region} generated highest sales.\n\n₹{value:,.0f}"
        )

    # -----------------------------
    # Top Products
    # -----------------------------

    elif "top" in q and "product" in q:

        top = (
            df.groupby("Product")["Sales"]
            .sum()
            .sort_values(ascending=False)
            .head(5)
        )

        st.dataframe(top)

    # -----------------------------
    # Highest Profit Category
    # -----------------------------

    elif "profit" in q:

        cat = (
            df.groupby("Category")["Profit"]
            .sum()
            .idxmax()
        )

        value = (
            df.groupby("Category")["Profit"]
            .sum()
            .max()
        )

        st.success(
            f"📦 {cat}\n\nProfit : ₹{value:,.0f}"
        )

    # -----------------------------
    # Rating
    # -----------------------------

    elif "rating" in q:

        rating = df["Rating"].mean()

        st.success(
            f"⭐ Average Rating : {rating:.2f}"
        )

    else:

        st.warning(
            "Sorry 😔 I don't understand this question."
        )