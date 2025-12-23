import pandas as pd
import os

DATA_PATH = os.path.join("..", "data", "raw", "online_retail_II.xlsx")

def load_data():
    df = pd.read_excel(
        DATA_PATH,
        sheet_name="Year 2009-2010"
    )
    return df

if __name__ == "__main__":
    df = load_data()
    print("Data loaded successfully")
    print("Shape:", df.shape)
    print("Columns:", df.columns.tolist())
