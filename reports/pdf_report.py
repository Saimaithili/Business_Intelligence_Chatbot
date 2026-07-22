import streamlit as st
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import io


def show_pdf_report(df):

    st.title("📄 PDF Report")

    total_sales = df["Sales"].sum()
    total_profit = df["Profit"].sum()
    total_orders = len(df)
    total_categories = df["Category"].nunique()
    highest_region = df.groupby("Region")["Sales"].sum().idxmax()

    st.metric("💰 Total Sales", f"₹{total_sales:,.0f}")
    st.metric("📈 Total Profit", f"₹{total_profit:,.0f}")

    buffer = io.BytesIO()

    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()

    story = []

    story.append(Paragraph("<b>Business Intelligence Report</b>", styles["Title"]))
    story.append(Paragraph(f"Total Sales : ₹{total_sales:,.0f}", styles["Normal"]))
    story.append(Paragraph(f"Total Profit : ₹{total_profit:,.0f}", styles["Normal"]))
    story.append(Paragraph(f"Total Orders : {total_orders}", styles["Normal"]))
    story.append(Paragraph(f"Categories : {total_categories}", styles["Normal"]))
    story.append(Paragraph(f"Highest Sales Region : {highest_region}", styles["Normal"]))

    doc.build(story)

    pdf = buffer.getvalue()

    st.download_button(
        "📥 Download PDF",
        pdf,
        file_name="Business_Report.pdf",
        mime="application/pdf"
    )