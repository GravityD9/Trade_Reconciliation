# Middle Office Automation

## Overview
This repository contains Python-based operational tools designed to automate daily fund administration workflows, specifically simulating Prime Broker to Internal Ledger reconciliations. It is built to demonstrate programmatic efficiency in identifying position, pricing, and unbooked trade breaks—a core function of Middle Office and Fund Accounting teams.

## Project 1: Prime Broker Position Reconciliation Engine
**Files:** `generate_ledgers.py`, `recon_engine.py`  
**Framework:** Pandas Data Manipulation & Outer Joins

Hedge fund accounting relies on the daily matching of an internal book (e.g., Morgan Stanley Portfolio Accounting - MSPA) against prime broker/custodian records. This engine automates that manual VLOOKUP process.

*   **Ledger Generation:** Generates mock internal and external trade ledgers populated with intentional discrepancies (ghost trades, unbooked trades, share quantity breaks, and price variances).
*   **Automated Reconciliation:** Utilizes `pandas.merge` to perform an outer join, instantly isolating mismatched rows.
*   **Exception Reporting:** Categorizes breaks by operational risk type and outputs a clean `daily_exceptions_report.csv` for Account Manager review and adjustment.

## Technology Stack
*   **Language:** Python 3.x
*   **Data Processing:** `pandas`, `numpy`

## How to Run Locally
1. Clone the repository.
2. Activate a virtual environment and `pip install pandas numpy`.
3. Run `python generate_ledgers.py` to create the raw ledger files.
4. Run `python recon_engine.py` to execute the reconciliation logic and output the daily breaks report.