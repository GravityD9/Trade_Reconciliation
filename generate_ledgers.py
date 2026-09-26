import pandas as pd

# internal book, what a company thinks the fund owns
internal_data = {
    'Trade_ID': ['T100', 'T101', 'T102', 'T103', 'T104'],
    'Ticker': ['AAPL', 'MSFT', 'TSLA', 'AMZN', 'GOOGL'],
    'Shares': [1000, 500, 200, 300, 400],
    'Price': [175.50, 330.00, 210.00, 135.00, 140.00]
}
internal_df = pd.DataFrame(internal_data)

# custodian book, what the prime broker holding the assets actually reports
custodian_data = {
    # T104 is missing (Unbooked trade), T105 is unexpected (Ghost trade)
    'Trade_ID': ['T100', 'T101', 'T102', 'T103', 'T105'], 
    'Ticker': ['AAPL', 'MSFT', 'TSLA', 'AMZN', 'META'],
    # TSLA shares mismatch (200 internal vs 250 custodian)
    'Shares': [1000, 500, 250, 300, 150], 
    # AMZN price mismatch ($135.00 internal vs $134.50 custodian)
    'Price': [175.50, 330.00, 210.00, 134.50, 300.00] 
}
custodian_df = pd.DataFrame(custodian_data)

# Export to CSV so our reconciliation engine can process them like real-world files
internal_df.to_csv('mspa_internal_ledger.csv', index=False)
custodian_df.to_csv('custodian_ledger.csv', index=False)

print("Successfully generated 'mspa_internal_ledger.csv' and 'custodian_ledger.csv'.")
print("Intentional trade breaks have been seeded in the data.")