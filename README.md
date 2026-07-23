# 🤖 AI Business Intelligence Assistant

A full-stack Streamlit web application for analyzing sales data through
interactive dashboards, natural-language style querying, and exportable
business reports.

**Live Demo:** _(add your Streamlit Cloud link here after deployment)_

---

## ✨ Features

- 🔐 **Secure Authentication** — Sign up / log in with bcrypt password hashing (SQLite-backed)
- 📊 **Interactive Dashboard** — KPIs, sales trends, region/category breakdowns, top products
- 📈 **Analytics** — Sales summary stats, profit-by-category, sales-vs-profit correlation
- 🤖 **AI Chat Assistant** — Ask questions in plain English ("June profit?", "top 5 products",
  "sales by region") and get instant answers, parsed with a custom NLP-style date/keyword engine
- 📄 **Reports** — Export business summaries as CSV, Excel, or PDF
- ⚙️ **Settings** — Editable profile, password change, dataset/chat reset, app info
- 🎨 **Custom UI Theme** — Dark, data-terminal inspired design with Plotly-powered charts

---

## 🛠 Tech Stack

| Layer | Tools |
|---|---|
| Frontend / App | Streamlit |
| Data | Pandas |
| Charts | Plotly |
| Auth & DB | SQLite, bcrypt |
| Reports | ReportLab (PDF), OpenPyXL (Excel) |

---

## 📂 Project Structure

Business_Intelligence_Chatbot/
├── app.py # Entry point — session state & routing
├── home.py # Home page — hero, KPIs, search, navigation
├── auth/
│ ├── login.py
│ └── signup.py
├── database/
│ └── database.py # SQLite + bcrypt user auth
├── dashboard/
│ ├── dashboard.py
│ └── analytics.py
├── chatbot/
│ └── chatbot.py # Rule-based NLP query engine
├── reports/
│ ├── report_page.py
│ ├── excel_report.py
│ └── pdf_report.py
├── settings/
│ └── settings.py
├── utils/
│ └── helper.py # CSS loader, Plotly chart helpers, KPI cards
├── static/
│ └── style.css
├── data/
│ └── sales_data.csv # Sample dataset
└── requirements.txt

---

## 🚀 Run Locally

```bash
git clone <your-repo-url>
cd Business_Intelligence_Chatbot

python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS/Linux

pip install -r requirements.txt

streamlit run app.py
```

App opens at `http://localhost:8501`.

---

## 📊 Sample Dataset

`data/sales_data.csv` is a synthetic dataset (1000 rows) with columns:
`Order_ID, Date, Region, City, Category, Product, Sales, Profit, Quantity,
Customer, Payment_Mode, Sales_Person, Rating`. You can also upload your own
CSV from the Dashboard page, as long as it has similar columns.

---

## 🔒 Security Notes

- Passwords are hashed with `bcrypt` before being stored — never stored in plain text
- No API keys or secrets are required to run this project

---

## 📌 Roadmap / Possible Extensions

- Forecast module (currently a placeholder)
- Optional LLM integration for more flexible natural-language queries
- Multi-user role-based access (admin vs viewer)

---

## 👤 Author

Built by Maithili as a portfolio project.