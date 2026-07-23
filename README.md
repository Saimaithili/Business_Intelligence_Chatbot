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