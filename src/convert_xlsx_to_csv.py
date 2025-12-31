import pandas as pd
import os

def convert_excel_to_csv():
    xlsx_path = 'data/raw/online_retail_II.xlsx'
    csv_path = 'data/raw/online_retail.csv'
    
    if os.path.exists(csv_path):
        print(f"{csv_path} already exists.")
        return

    if not os.path.exists(xlsx_path):
        print(f"{xlsx_path} not found. Cannot convert.")
        return

    print(f"Reading {xlsx_path}...")
    # Read the second sheet which corresponds to 2010-2011 (usually the target dataset)
    # The dataset typically has "Year 2009-2010" and "Year 2010-2011"
    try:
        df = pd.read_excel(xlsx_path, sheet_name="Year 2010-2011")
    except ValueError:
        print("Sheet 'Year 2010-2011' not found, trying default...")
        df = pd.read_excel(xlsx_path)

    print(f"Converting to {csv_path}...")
    df.to_csv(csv_path, index=False)
    print("Conversion complete.")
    print(f"Rows: {len(df)}")

if __name__ == "__main__":
    convert_excel_to_csv()
