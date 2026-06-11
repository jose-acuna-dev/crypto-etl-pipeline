# crypto-etl-pipeline

# Automated Crypto ETL Pipeline & Analytics Dashboard

## 📊 Project Overview
An end-to-end data engineering pipeline that automates the daily extraction of cryptocurrency pricing data, loads it into a persistent relational database, and exposes the metrics via an interactive Tableau dashboard. 

## 🏗️ Architecture & Tech Stack
* **Data Source:** Live extraction from the CoinGecko API.
* **Cloud Automation:** Serverless cron-job scheduling via **GitHub Actions**.
* **Database:** **SQLite** (Persistent time-series data storage).
* **ETL Processing:** **Python** (`requests`, `sqlite3`, `csv` libraries).
* **Data Visualization:** **Tableau Public** (Small Multiples layout, independent axis scaling, live KPI metrics).

## ⚙️ Pipeline Flow
1. **Extract:** A GitHub Action triggers `crypto_pipeline.py` every 24 hours to ping the CoinGecko API for Bitcoin, Ethereum, Solana, and XRP prices.
2. **Load:** The raw JSON data is parsed and securely loaded into `crypto_portfolio.db`. The updated database is automatically committed back to the repository.
3. **Transform:** Locally, `crypto_to_csv.py` queries the database, extracts the complete historical timeline, and flattens it into a normalized CSV format.
4. **Visualize:** Tableau consumes the clean CSV to dynamically update the interactive dashboard and recalculate the live KPI scoreboard.

## 🔗 Live Dashboard
https://public.tableau.com/views/Crypto_Asset_Trendlines/Dashboard1?:language=en-US&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link