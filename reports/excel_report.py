import pandas as pd
import io


def generate_excel(df):
    buffer = io.BytesIO()

    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Sales Report")

    return buffer.getvalue()