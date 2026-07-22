import streamlit as st
import pandas as pd

from dashboard.dashboard import show_dashboard
from dashboard.analytics import show_analytics
from chatbot.chatbot import show_chatbot
from reports.report_page import show_reports
from settings.settings import show_settings
from utils.helper import render_kpi_card, line_chart


def go_to(page_label):
    st.session_state.nav_redirect = page_label
    st.rerun()


def load_default_dataset():
    if "df" not in st.session_state:
        try:
            st.session_state["df"] = pd.read_csv("data/sales_data.csv")
        except FileNotFoundError:
            pass


def show_home():

    load_default_dataset()

    # ---------------- Sidebar ---------------- #

    with st.sidebar:

        st.markdown("## 🤖 AI BI Assistant")

        if "nav_menu" not in st.session_state:
            st.session_state.nav_menu = "🏠 Home"

        if "nav_redirect" in st.session_state:
            st.session_state.nav_menu = st.session_state.pop("nav_redirect")

        menu = st.radio(
            "Navigation",
            [
                "🏠 Home",
                "📊 Dashboard",
                "📈 Analytics",
                "🤖 AI Chat",
                "📄 Reports",
                "⚙️ Settings"
            ],
            key="nav_menu"
        )

    # ---------------- Navigation ---------------- #

    if menu == "📊 Dashboard":
        show_dashboard()
        return

    elif menu == "📈 Analytics":
        show_analytics()
        return

    elif menu == "🤖 AI Chat":
        show_chatbot(st.session_state["df"])
        return

    elif menu == "📄 Reports":
        show_reports(st.session_state["df"])
        return

    elif menu == "⚙️ Settings":
        show_settings()
        return

    # ---------------- Logout ---------------- #

    col1, col2 = st.columns([8, 1])

    with col2:
        if st.button("🚪 Logout"):
            st.session_state["logged_in"] = False
            st.session_state["page"] = "login"
            st.rerun()

    # ---------------- Welcome ---------------- #

    user = st.session_state.get("user_name", "User")

    st.write(f"## 👋 Welcome, {user}")

    # ---------------- Hero ---------------- #

    st.markdown(
        """
        <div class="hero">
          <div class="hero-inner">
            <span class="hero-eyebrow">Sales Intelligence Platform</span>
            <h1>🤖 AI Business Intelligence Assistant</h1>
            <h3>Transform Your Business Data Into Smart Decisions</h3>
            <p>Analyze Sales • Generate Reports • Natural Language Queries • Dashboard Analytics</p>
          </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    # ---------------- Search Bar ---------------- #

    with st.form(key="home_search_form", clear_on_submit=False):
        s1, s2 = st.columns([6, 1])

        with s1:
            search_query = st.text_input(
                "",
                placeholder="🔍 Search reports, dashboard, analytics, or type a product/region/category...",
                label_visibility="collapsed"
            )

        with s2:
            search_submitted = st.form_submit_button("Search", use_container_width=True)

    if search_submitted and search_query.strip():
        q = search_query.lower().strip()

        page_keywords = {
            "📊 Dashboard": ["dashboard"],
            "📈 Analytics": ["analytic", "analysis"],
            "🤖 AI Chat": ["chat", "ai chat", "assistant"],
            "📄 Reports": ["report"],
            "⚙️ Settings": ["setting"],
        }

        matched_page = None
        for page, keywords in page_keywords.items():
            if any(k in q for k in keywords):
                matched_page = page
                break

        if matched_page:
            go_to(matched_page)

        elif "df" in st.session_state:
            df = st.session_state["df"]
            search_cols = [c for c in ["Product", "Category", "Region", "Customer"] if c in df.columns]

            if search_cols:
                mask = pd.Series(False, index=df.index)
                for col in search_cols:
                    mask = mask | df[col].astype(str).str.lower().str.contains(q, na=False)

                results = df[mask]

                if not results.empty:
                    st.success(f"Found {len(results)} matching row(s) for \"{search_query}\"")
                    st.dataframe(results.head(20), use_container_width=True)
                else:
                    st.warning(f"No matches found for \"{search_query}\".")
            else:
                st.warning("Dataset doesn't have searchable columns (Product/Category/Region/Customer).")

        else:
            st.warning("No dataset loaded to search. Try 'dashboard', 'analytics', 'reports', 'chat', or 'settings'.")

    st.divider()

    # ---------------- KPI (real data) ---------------- #

    if "df" in st.session_state:

        df = st.session_state["df"]

        total_sales = df["Sales"].sum()
        total_profit = df["Profit"].sum()
        total_orders = len(df)
        total_customers = df["Customer"].nunique() if "Customer" in df.columns else "-"

        c1, c2, c3, c4 = st.columns(4)

        with c1:
            render_kpi_card("💰", "Revenue", f"₹{total_sales:,.0f}", accent="#2DD4BF")

        with c2:
            render_kpi_card("📈", "Profit", f"₹{total_profit:,.0f}", accent="#34D399")

        with c3:
            render_kpi_card("🛒", "Orders", f"{total_orders:,}", accent="#F5A524")

        with c4:
            render_kpi_card("👥", "Customers", f"{total_customers}", accent="#8B7CF6")

        st.divider()

        if "Date" in df.columns:
            chart_df = df.copy()
            chart_df["Date"] = pd.to_datetime(chart_df["Date"])
            monthly = (
                chart_df.groupby(chart_df["Date"].dt.to_period("M"))["Sales"]
                .sum()
            )
            monthly.index = monthly.index.astype(str)

            st.subheader("📈 Sales Trend")
            line_chart(monthly)

            st.divider()

    else:
        st.info("📂 Open **Dashboard** and upload your sales data to see live stats here.")
        st.divider()

    # ---------------- Quick Actions ---------------- #

    st.subheader("⚡ Quick Actions")

    b1, b2, b3 = st.columns(3)

    with b1:
        if st.button("📂 Upload Sales Data", use_container_width=True):
            go_to("📊 Dashboard")

    with b2:
        if st.button("🤖 Open AI Chat", use_container_width=True):
            go_to("🤖 AI Chat")

    with b3:
        if st.button("📄 Generate Report", use_container_width=True):
            go_to("📄 Reports")

    st.divider()

    # ---------------- Features ---------------- #

    st.subheader("🚀 Platform Features")

    left, right = st.columns(2)

    with left:
        if st.button("📊 Interactive Dashboard", use_container_width=True):
            go_to("📊 Dashboard")

        if st.button("📈 Analytics", use_container_width=True):
            go_to("📈 Analytics")

        if st.button("📄 Reports", use_container_width=True):
            go_to("📄 Reports")

        if st.button("📥 CSV Upload", use_container_width=True):
            go_to("📊 Dashboard")

    with right:
        if st.button("🤖 AI Chat", use_container_width=True):
            go_to("🤖 AI Chat")

        if st.button("🌍 Region Analysis", use_container_width=True):
            go_to("📈 Analytics")

        if st.button("📦 Category Analysis", use_container_width=True):
            go_to("📊 Dashboard")

        st.button("📈 Forecast (Coming Soon)", use_container_width=True, disabled=True)

    st.markdown("---")

    st.markdown(
        """
        <center>
        ❤️ AI Business Intelligence Assistant | 2026
        </center>
        """,
        unsafe_allow_html=True
    )