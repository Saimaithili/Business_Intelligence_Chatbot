from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
import io


def generate_pdf(df):
    total_sales = df["Sales"].sum()
    total_profit = df["Profit"].sum()
    total_orders = len(df)
    total_categories = df["Category"].nunique()
    highest_region = df.groupby("Region")["Sales"].sum().idxmax()
    best_category = df.groupby("Category")["Sales"].sum().idxmax()

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()

    story = []

    story.append(Paragraph("<b>Business Intelligence Report</b>", styles["Title"]))
    story.append(Spacer(1, 0.25 * inch))

    story.append(Paragraph(f"Total Sales : Rs. {total_sales:,.0f}", styles["Normal"]))
    story.append(Paragraph(f"Total Profit : Rs. {total_profit:,.0f}", styles["Normal"]))
    story.append(Paragraph(f"Total Orders : {total_orders}", styles["Normal"]))
    story.append(Paragraph(f"Categories : {total_categories}", styles["Normal"]))
    story.append(Paragraph(f"Highest Sales Region : {highest_region}", styles["Normal"]))
    story.append(Paragraph(f"Best Category : {best_category}", styles["Normal"]))

    if "Rating" in df.columns:
        story.append(Paragraph(f"Average Rating : {df['Rating'].mean():.2f}", styles["Normal"]))

    doc.build(story)

    return buffer.getvalue()