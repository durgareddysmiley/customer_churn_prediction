def generate_data_profile():
    import pandas as pd
    import os

    # Load raw data
    df = pd.read_excel("data/raw/online_retail_II.xlsx")

    # Ensure directory exists
    os.makedirs("data/raw", exist_ok=True)

    profile_path = "data/raw/data_profile.txt"

    with open(profile_path, "w", encoding="utf-8") as f:
        f.write("DATA PROFILE REPORT\n")
        f.write("====================\n\n")

        f.write(f"Rows: {df.shape[0]}\n")
        f.write(f"Columns: {df.shape[1]}\n\n")

        f.write("COLUMN NAMES & TYPES:\n")
        f.write(str(df.dtypes))
        f.write("\n\n")

        f.write("MEMORY USAGE:\n")
        f.write(str(df.memory_usage(deep=True)))
        f.write("\n\n")

        f.write("FIRST 5 ROWS:\n")
        f.write(str(df.head()))

    print(f"Data profile saved to {profile_path}")
