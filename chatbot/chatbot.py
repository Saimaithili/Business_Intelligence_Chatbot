import streamlit as st
import pandas as pd
import re
import calendar
from datetime import datetime, timedelta

from utils.helper import bar_chart, line_chart


# ----------------------------
# Helper Functions
# ----------------------------

def user(msg):
    st.session_state.messages.append(("user", msg))


def bot(msg):
    st.session_state.messages.append(("bot", msg))


def show_history():
    for role, message in st.session_state.messages:
        if role == "user":
            st.chat_message("user").write(message)
        else:
            st.chat_message("assistant").write(message)


# ----------------------------
# Date Query Helpers
# ----------------------------

MONTH_NAMES = {name.lower(): num for num, name in enumerate(calendar.month_name) if name}
MONTH_ABBR = {name.lower(): num for num, name in enumerate(calendar.month_abbr) if name}


def _month_bounds(year, month):
    start = datetime(year, month, 1)
    last_day = calendar.monthrange(year, month)[1]
    end = datetime(year, month, last_day, 23, 59, 59)
    return start, end


def extract_date_range(query, today=None):
    if today is None:
        today = datetime.now()

    q = query.lower().strip()

    if "today" in q:
        start = datetime(today.year, today.month, today.day)
        end = start + timedelta(hours=23, minutes=59, seconds=59)
        return start, end, "Today"

    if "yesterday" in q:
        y = today - timedelta(days=1)
        start = datetime(y.year, y.month, y.day)
        end = start + timedelta(hours=23, minutes=59, seconds=59)
        return start, end, "Yesterday"

    if "this week" in q:
        start = today - timedelta(days=today.weekday())
        start = datetime(start.year, start.month, start.day)
        end = start + timedelta(days=6, hours=23, minutes=59, seconds=59)
        return start, end, "This Week"

    if "last week" in q:
        this_week_start = today - timedelta(days=today.weekday())
        start = this_week_start - timedelta(days=7)
        start = datetime(start.year, start.month, start.day)
        end = start + timedelta(days=6, hours=23, minutes=59, seconds=59)
        return start, end, "Last Week"

    if "this month" in q:
        start, end = _month_bounds(today.year, today.month)
        return start, end, "This Month"

    if "last month" in q:
        first_of_this_month = datetime(today.year, today.month, 1)
        last_month_end = first_of_this_month - timedelta(days=1)
        start, end = _month_bounds(last_month_end.year, last_month_end.month)
        return start, end, "Last Month"

    if "this year" in q:
        start = datetime(today.year, 1, 1)
        end = datetime(today.year, 12, 31, 23, 59, 59)
        return start, end, "This Year"

    if "last year" in q:
        y = today.year - 1
        start = datetime(y, 1, 1)
        end = datetime(y, 12, 31, 23, 59, 59)
        return start, end, f"Year {y}"

    year_match = re.search(r"\b(20\d{2})\b", q)
    explicit_year = int(year_match.group(1)) if year_match else today.year

    for name_map in (MONTH_NAMES, MONTH_ABBR):
        for name, num in name_map.items():
            if re.search(rf"\b{name}\b", q):
                start, end = _month_bounds(explicit_year, num)
                return start, end, f"{calendar.month_name[num]} {explicit_year}"

    if year_match:
        y = int(year_match.group(1))
        start = datetime(y, 1, 1)
        end = datetime(y, 12, 31, 23, 59, 59)
        return start, end, f"Year {y}"

    iso_match = re.search(r"\b(\d{4})-(\d{1,2})-(\d{1,2})\b", q)
    if iso_match:
        y, m, d = map(int, iso_match.groups())
        start = datetime(y, m, d)
        end = start + timedelta(hours=23, minutes=59, seconds=59)
        return start, end, start.strftime("%d %b %Y")

    dmy_match = re.search(r"\b(\d{1,2})[/-](\d{1,2})[/-](\d{4})\b", q)
    if dmy_match:
        d, m, y = map(int, dmy_match.groups())
        start = datetime(y, m, d)
        end = start + timedelta(hours=23, minutes=59, seconds=59)
        return start, end, start.strftime("%d %b %Y")

    return None


def filter_by_date_range(df, date_col, start, end):
    temp = df.copy()
    temp[date_col] = pd.to_datetime(temp[date_col], errors="coerce")
    mask = (temp[date_col] >= start) & (temp[date_col] <= end)
    return temp.loc[mask]


# ----------------------------
# Main Chatbot
# ----------------------------

def show_chatbot(df):

    if "messages" not in st.session_state:
        st.session_state.messages = []

    st.title("🤖 AI Business Intelligence Chatbot")
    st.write("Ask questions about your business data.")

    with st.form(key="ask_form", clear_on_submit=True):
        col1, col2 = st.columns([6, 1])
        with col1:
            question = st.text_input(
                "Ask your question",
                placeholder="Example: Top 5 products",
                key="question"
            )
        with col2:
            ask = st.form_submit_button("🚀 Ask AI")

    if st.button("🗑 Clear Chat"):
        st.session_state.messages = []
        st.rerun()

    show_history()

    if ask and question.strip():
        user(question)
        q = question.lower().strip()

        date_col = None
        if "Date" in df.columns:
            date_col = "Date"
        elif "Order Date" in df.columns:
            date_col = "Order Date"

        if date_col:
            df[date_col] = pd.to_datetime(df[date_col], errors="coerce")

        try:
            date_range = extract_date_range(q) if date_col else None

            if date_range is not None:
                start, end, label = date_range
                filtered = filter_by_date_range(df, date_col, start, end)

                if "profit" in q:
                    value = filtered["Profit"].sum()
                    bot(f"📈 {label} Profit : ₹{value:,.2f}")
                elif "sales" in q:
                    value = filtered["Sales"].sum()
                    bot(f"💰 {label} Sales : ₹{value:,.2f}")
                elif "orders" in q:
                    bot(f"📦 {label} Orders : {len(filtered)}")
                else:
                    sales = filtered["Sales"].sum()
                    profit = filtered["Profit"].sum()
                    bot(
                        f"📅 {label} — Sales: ₹{sales:,.2f} | "
                        f"Profit: ₹{profit:,.2f} | Orders: {len(filtered)}"
                    )

            elif any(x in q for x in ["total sales", "sales", "overall sales"]):
                sales = df["Sales"].sum()
                bot(f"💰 Total Sales : ₹{sales:,.2f}")

            elif any(x in q for x in ["total profit", "overall profit"]):
                profit = df["Profit"].sum()
                bot(f"📈 Total Profit : ₹{profit:,.2f}")

            elif "average sales" in q:
                avg = df["Sales"].mean()
                bot(f"Average Sales : ₹{avg:,.2f}")

            elif "average profit" in q:
                avg = df["Profit"].mean()
                bot(f"Average Profit : ₹{avg:,.2f}")

            elif "orders" in q and "category" not in q:
                bot(f"📦 Total Orders : {len(df)}")

            elif "customer" in q:
                if "Customer" in df.columns:
                    bot(f"👥 Total Customers : {df['Customer'].nunique()}")
                else:
                    bot("Customer column not available.")

            elif any(x in q for x in ["show data", "dataset", "show dataset"]):
                bot("Displaying Dataset 👇")
                st.dataframe(df)

            elif ("top 5" in q or "top five" in q) and "product" in q:
                top = df.groupby("Product")["Sales"].sum().sort_values(ascending=False).head(5).reset_index()
                bot("🏆 Top 5 Products")
                st.dataframe(top)

            elif ("top 10" in q or "top ten" in q) and "product" in q:
                top = df.groupby("Product")["Sales"].sum().sort_values(ascending=False).head(10).reset_index()
                bot("🏆 Top 10 Products")
                st.dataframe(top)

            elif "top product" in q or "best product" in q:
                product = df.groupby("Product")["Sales"].sum().idxmax()
                sales = df.groupby("Product")["Sales"].sum().max()
                bot(f"🏆 Top Product: **{product}** (₹{sales:,.2f})")

            elif "lowest product" in q or "worst product" in q:
                product = df.groupby("Product")["Sales"].sum().idxmin()
                sales = df.groupby("Product")["Sales"].sum().min()
                bot(f"📉 Lowest Product: **{product}** (₹{sales:,.2f})")

            elif "Category" in df.columns and any(
                str(cat).lower() in q for cat in df["Category"].dropna().unique()
            ) and ("profit" in q or "sales" in q or "loss" in q):

                matched_cat = next(
                    cat for cat in df["Category"].dropna().unique()
                    if str(cat).lower() in q
                )
                cat_df = df[df["Category"] == matched_cat]

                if "sales" in q:
                    value = cat_df["Sales"].sum()
                    bot(f"🛍 {matched_cat} Sales : ₹{value:,.2f}")
                else:
                    value = cat_df["Profit"].sum()
                    if value < 0:
                        bot(f"📉 {matched_cat} Loss : ₹{abs(value):,.2f}")
                    else:
                        bot(f"💹 {matched_cat} Profit : ₹{value:,.2f}")

            elif "loss" in q and "category" in q:
                category_profit = df.groupby("Category")["Profit"].sum().sort_values()
                losses = category_profit[category_profit < 0]

                if not losses.empty:
                    bot("📉 Categories in Loss")
                    bar_chart(losses, single_color="#FB7185")
                    st.dataframe(losses.reset_index())
                else:
                    bot("✅ No category is currently in loss.")

            elif "sales by region" in q or "region sales" in q:
                region_sales = df.groupby("Region")["Sales"].sum().sort_values(ascending=False)
                bot("📊 Sales by Region")
                bar_chart(region_sales)
                st.dataframe(region_sales.reset_index())

            elif "profit by region" in q or "region profit" in q:
                region_profit = df.groupby("Region")["Profit"].sum().sort_values(ascending=False)
                bot("📈 Profit by Region")
                bar_chart(region_profit)
                st.dataframe(region_profit.reset_index())

            elif "sales by category" in q or "category sales" in q:
                category_sales = df.groupby("Category")["Sales"].sum().sort_values(ascending=False)
                bot("🛍 Sales by Category")
                bar_chart(category_sales)
                st.dataframe(category_sales.reset_index())

            elif "profit by category" in q or "category profit" in q:
                category_profit = df.groupby("Category")["Profit"].sum().sort_values(ascending=False)
                bot("💹 Profit by Category")
                bar_chart(category_profit)
                st.dataframe(category_profit.reset_index())

            elif "top customers" in q:
                if "Customer" in df.columns:
                    customers = df.groupby("Customer")["Sales"].sum().sort_values(ascending=False).head(10)
                    bot("👥 Top 10 Customers")
                    bar_chart(customers, horizontal=True)
                    st.dataframe(customers.reset_index())
                else:
                    bot("Customer column not found.")

            elif "monthly sales" in q or "sales trend" in q:
                if date_col:
                    temp = df.copy()
                    monthly = temp.groupby(temp[date_col].dt.to_period("M"))["Sales"].sum()
                    monthly.index = monthly.index.astype(str)
                    bot("📅 Monthly Sales Trend")
                    line_chart(monthly)
                    st.dataframe(monthly.reset_index())
                else:
                    bot("Date column not available.")

            else:
                bot("🤖 I couldn't understand your question.")

        except Exception as e:
            bot(f"❌ Error : {e}")

        st.rerun()