import pandas as pd  ## What is Pandas? Pandas is a Python library used to work with data. It helps you: -> Read CSV files -> Read Excel files
import requests     ## This imports the requests library, which is used to communicate with websites and APIs over HTTP.
import os       ## Python's built-in Operating System module -> Work with files and folders , -> Create directories
from datetime import datetime   ## It lets you work with the current date and time. we can extract only year , only month specifically 
import io  ## he io module is used to work with data as if it were a file, even when the data is stored in memory instead of on disk.sometimes you have data in memory (a string or bytes)
           ## and want to treat it like a file. That's where io helps.
 
def download_dataset():
    """
    Download the Online Retail dataset
    Save to data/raw/online_retail.csv
    """ 
    
    # URL for the Online Retail II dataset (UCI ML Repository)
    # Using the direct link to the excel file
    url = "https://archive.ics.uci.edu/ml/machine-learning-databases/00502/online_retail_II.xlsx"
    
    print(f"Starting download from {url}...")
    
    # Create directory structure
    os.makedirs('data/raw', exist_ok=True) ## to create one or more dictionary folders
    
    try:
        response = requests.get(url, timeout=60)
        response.raise_for_status()
        
        print("Download complete. Converting to CSV...")
        
        # Read Excel file from memory
        # The dataset typically has two sheets: "Year 2009-2010" and "Year 2010-2011"
        # We need to combine them or stick to one. The instructions mention ~541k rows which usually corresponds to 2010-2011.
        # However, to be thorough, let's load the 2010-2011 sheet which matches the standard "Online Retail" dataset often used.
        # But wait, Online Retail II contains two years. 
        # Metric check: 541,909 rows matches the 2010-2011 dataset usually found in "Online Retail.xlsx".
        # Let's try to load both and see, or just load the one that matches the expected count.
        # Standard "Online Retail" dataset (541909 rows) is usually the 2010-2011 data.
        
        with io.BytesIO(response.content) as fh:
            df = pd.read_excel(fh, sheet_name="Year 2010-2011")
        
        # Save as CSV
        output_path = 'data/raw/online_retail.csv'
        df.to_csv(output_path, index=False)
        
        print(f"Dataset downloaded: {datetime.now()}")
        print(f"Saved to: {output_path}")
        print(f"Rows: {len(df)}")
        
        return True
        
    except Exception as e:
        print(f"Error downloading dataset: {e}")
        # Fallback mechanisms could go here
        return False

def load_raw_data():
    """
    Load the raw dataset and return DataFrame
    
    Returns:
        pd.DataFrame: Raw dataset
    """
    if not os.path.exists('data/raw/online_retail.csv'):
        print("File not found. Downloading...")
        download_dataset()
        
    df = pd.read_csv('data/raw/online_retail.csv')
    return df

def generate_data_profile():
    """
    Generate initial data profile and save to data/raw/data_profile.txt
    """
    df = load_raw_data()
    
    profile = []
    profile.append(f"Dataset Shape: {df.shape}")
    profile.append("\nColumn Info:")
    profile.append(str(df.dtypes))
    profile.append("\nMissing Values:")
    profile.append(str(df.isnull().sum()))
    profile.append("\nFirst 5 Rows:")
    profile.append(str(df.head()))
    
    with open('data/raw/data_profile.txt', 'w') as f:
        f.write('\n'.join(profile))
        
    print("Data profile generated at data/raw/data_profile.txt")

if __name__ == "__main__":
    download_dataset()
    df = load_raw_data()
    generate_data_profile()
