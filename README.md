# Automated Prime Broker Reconciliation Engine

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Pandas-Data%20Processing-green)](https://pandas.pydata.org/)

This repository contains a programmatic operational tool designed to automate daily T+1 fund administration workflows, specifically simulating Prime Broker (Custodian) to Internal Book (e.g., Morgan Stanley Portfolio Accounting - MSPA) reconciliations. 

Built to replace manual Excel VLOOKUPs, this engine automates the identification of position breaks, pricing discrepancies, and unbooked trades to ensure accurate daily Net Asset Value (NAV) strikes.

## Business Value
Hedge fund accounting relies on the daily matching of internal records against external prime broker data. This engine reduces a multi-hour manual process to seconds by:
*   **Automating Exception Management:** Categorizes breaks by operational risk type (Ghost Trades, Unbooked Trades, Quantity Breaks).
*   **Reducing Operational Risk:** Eliminates human error inherent in manual spreadsheet comparisons.
*   **Generating Audit Trails:** Outputs a structured, timestamped exception report for Account Manager review and adjustment.

## System Architecture

*   **`generate_ledgers.py`**: A mock data pipeline that generates T+1 internal and external trade ledgers, intentionally seeded with structural anomalies.
*   **`recon_engine.py`**: The core reconciliation logic. Utilizes `pandas.merge` (outer joins) to instantly isolate orphaned rows and calculate price/quantity variances across matched trades.

## Sample Output (Exception Report)
When the engine runs, it automatically flags the breaks and exports a clean `daily_exceptions_report.csv` for the Middle Office team:

| Trade_ID | Ticker | Break_Type | Internal_Value | Custodian_Value | Variance |
| :--- | :--- | :--- | :--- | :--- | :--- |
| T104 | GOOGL | Missing from Custodian | Present | Missing | N/A |
| T105 | META | Missing from Internal | Missing | Present | N/A |
| T102 | TSLA | Share Quantity Break | 200 | 250 | -50 |
| T103 | AMZN | Price Mismatch Break | 135.0 | 134.5 | 0.5 |

## Quick Start / Local Deployment

**1. Clone the repository:**
```bash
git clone https://github.com/GravityD9/MSFS.git
cd Automated_Trade_Reconciliation