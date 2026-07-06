import streamlit as st
import pandas as pd


def show_home():

    # Sidebar
    with st.sidebar:

        st.markdown("## 🤖 AI BI Assistant")

        menu = st.radio(
            "Navigation",
            [
                "🏠 Home",
                "📊 Dashboard",
                "📈 Analytics",
                "🤖 AI Chat",
                "📄 Reports",
                "⚙️ Settings"
            ]
        )

    # Logout Button
    col1, col2 = st.columns([8, 1])

    with col2:
        if st.button("🚪 Logout"):
            st.session_state["logged_in"] = False
            st.session_state["page"] = "login"
            st.rerun()

    # Welcome
    st.write(f"### 👋 Welcome, {st.session_state['user_name']}")

    # Hero Section
    st.markdown("""
    <div style="
    background: linear-gradient(135deg,#0F172A,#1D4ED8,#7C3AED);
    padding:40px;
    border-radius:20px;
    color:white;
    text-align:center;
    box-shadow:0px 8px 25px rgba(0,0,0,0.35);
    ">

    <h1>🤖 AI Business Intelligence Assistant</h1>

    <h3>Transform Your Business Data Into Smart Decisions</h3>

    <p>
    Analyze sales, generate reports, visualize insights and ask questions using AI.
    </p>

    </div>
    """, unsafe_allow_html=True)

    # Search
    st.write("")

    search = st.text_input(
        "",
        placeholder="🔍 Search Dashboard, Reports, AI Insights..."
    )

    # KPI Cards
    st.divider()

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric("💰 Revenue", "₹49.7M", "+18%")

    with c2:
        st.metric("📈 Profit", "₹9.5M", "+12%")

    with c3:
        st.metric("🛒 Orders", "1,240", "+8%")

    with c4:
        st.metric("👥 Customers", "18,560", "+5%")

    # Sales Chart
    st.divider()

    chart = pd.DataFrame({
        "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
        "Sales": [15, 22, 28, 35, 42, 55]
    })

    st.subheader("📈 Sales Trend")

    st.line_chart(chart.set_index("Month"))
    st.divider()

st.subheader("📂 Upload Sales Data")

uploaded_file = st.file_uploader(
    "Upload a CSV File",
    type=["csv"]
)

if uploaded_file is not None:

    df = pd.read_csv(uploaded_file)

    st.success("✅ File Uploaded Successfully!")

    st.write("### Data Preview")

    st.dataframe(df)
    # Quick Actions
st.divider()

st.subheader("⚡ Quick Actions")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📂 Upload Sales Data", use_container_width=True):
        st.info("Upload feature will be added next.")

with col2:
    if st.button("🤖 Open AI Chat", use_container_width=True):
        st.info("AI Chat feature coming soon.")

with col3:
    if st.button("📄 Generate Report", use_container_width=True):
        st.info("Report generation coming soon.")
        st.divider()

st.subheader("🚀 Platform Features")

left, right = st.columns(2)

with left:
    st.success("📊 Interactive Dashboard")
    st.success("📈 Business Analytics")
    st.success("📄 PDF Reports")
    st.success("📊 Excel Reports")

with right:
    st.success("🤖 AI Assistant")
    st.success("🌍 Region Analysis")
    st.success("📦 Category Analysis")
    st.success("📈 Sales Forecast")
    st.divider()

st.subheader("📌 About Project")

st.write("""
The AI Business Intelligence Assistant helps businesses analyze sales data,
track KPIs, visualize trends, and interact with business information using AI.

It is built using Python, Streamlit, SQLite, Pandas, SQL, and Gemini AI.
""")
st.markdown("---")

st.markdown(
    """
    <center>
    ❤️ Made with Streamlit | AI Business Intelligence Assistant 2026
    </center>
    """,
    unsafe_allow_html=True
)