import streamlit as st
import pandas as pd
import io


def show_excel_report(df):

    st.title("📊 Excel Report")

    buffer = io.BytesIO()

    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Sales Report")

    st.download_button(
        "📥 Download Excel",
        data=buffer.getvalue(),
        file_name="Sales_Report.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )