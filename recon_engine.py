import pandas as pd

# ingesting daily data
print("Loading internal MSPA ledger and Custodian ledger...")
mspa_df = pd.read_csv('mspa_internal_ledger.csv')
cust_df = pd.read_csv('custodian_ledger.csv')

# reconciliation merge, joining the Trade ID & Ticker. 'indicator=True' indicates which file the trade originated from
recon = pd.merge(mspa_df, cust_df, on=['Trade_ID', 'Ticker'], 
                 how='outer', suffixes=('_MSPA', '_Cust'), indicator=True)

breaks = []

# identifying missing trades (unbooked/ ghost trades) 
# trades in the company (like MSPA) but missing from Custodian
missing_cust = recon[recon['_merge'] == 'left_only']
for _, row in missing_cust.iterrows():
    breaks.append({
        'Trade_ID': row['Trade_ID'], 'Ticker': row['Ticker'], 
        'Break_Type': 'Missing from Custodian', 
        'MSPA_Value': 'Present', 'Cust_Value': 'Missing', 'Variance': 'N/A'
    })

# trades at Custodian but missing from internal company (MSPA)
missing_mspa = recon[recon['_merge'] == 'right_only']
for _, row in missing_mspa.iterrows():
    breaks.append({
        'Trade_ID': row['Trade_ID'], 'Ticker': row['Ticker'], 
        'Break_Type': 'Missing from MSPA', 
        'MSPA_Value': 'Missing', 'Cust_Value': 'Present', 'Variance': 'N/A'
    })

# idenitifying quantity and price breaks
# checking trades which exist in both books
matched = recon[recon['_merge'] == 'both']

# finding shre mismatches
share_breaks = matched[matched['Shares_MSPA'] != matched['Shares_Cust']]
for _, row in share_breaks.iterrows():
    breaks.append({
        'Trade_ID': row['Trade_ID'], 'Ticker': row['Ticker'], 
        'Break_Type': 'Share Quantity Break', 
        'MSPA_Value': row['Shares_MSPA'], 'Cust_Value': row['Shares_Cust'], 
        'Variance': row['Shares_MSPA'] - row['Shares_Cust']
    })

# finding price mismatches
price_breaks = matched[matched['Price_MSPA'] != matched['Price_Cust']]
for _, row in price_breaks.iterrows():
    breaks.append({
        'Trade_ID': row['Trade_ID'], 'Ticker': row['Ticker'], 
        'Break_Type': 'Price Mismatch Break', 
        'MSPA_Value': row['Price_MSPA'], 'Cust_Value': row['Price_Cust'], 
        'Variance': round(row['Price_MSPA'] - row['Price_Cust'], 2)
    })

# exception report 
report_df = pd.DataFrame(breaks)

print("\n--- 🛑 DAILY EXCEPTIONS REPORT (ACTION REQUIRED) ---")
print(report_df.to_string(index=False))

report_df.to_csv('daily_exceptions_report.csv', index=False)
print("\n✅ Report successfully exported to 'daily_exceptions_report.csv'")