import streamlit as st

from utils.helper import render_kpi_card
from reports.excel_report import generate_excel
from reports.pdf_report import generate_pdf


def show_reports(df):

    st.title("📄 Business Intelligence Reports")
    st.write("Generate professional reports and business summary.")

    st.divider()

    # ================= KPI =================

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

    # ================= Data Preview =================

    st.subheader("📋 Sales Data")
    st.dataframe(df, use_container_width=True)

    st.divider()

    # ================= Business Summary =================

    region_sales = df.groupby("Region")["Sales"].sum()
    category_sales = df.groupby("Category")["Sales"].sum()

    st.subheader("🤖 Business Summary")

    st.success(f"""
Highest Sales Region : {region_sales.idxmax()}

Best Category : {category_sales.idxmax()}

Average Rating : {df["Rating"].mean():.2f}

Total Profit : ₹{total_profit:,.0f}
""")

    st.divider()

    # ================= Download Options =================

    st.subheader("📥 Export Report")

    d1, d2, d3 = st.columns(3)

    with d1:
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "📄 Download CSV",
            csv,
            file_name="business_report.csv",
            mime="text/csv",
            use_container_width=True,
        )

    with d2:
        excel_bytes = generate_excel(df)
        st.download_button(
            "📊 Download Excel",
            excel_bytes,
            file_name="Sales_Report.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
        )

    with d3:
        pdf_bytes = generate_pdf(df)
        st.download_button(
            "📕 Download PDF",
            pdf_bytes,
            file_name="Business_Report.pdf",
            mime="application/pdf",
            use_container_width=True,
        )

    st.success("✅ Report Generated Successfully")