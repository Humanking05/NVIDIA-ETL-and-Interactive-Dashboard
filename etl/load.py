import pandas as pd
import os
from config import DATA_FILE, DATA_FOLDER

def load_to_csv(df):
    """
    Save DataFrame to CSV. If file exists, append new rows.
    """
    if not os.path.exists(DATA_FOLDER):
        os.makedirs(DATA_FOLDER)

    if os.path.exists(DATA_FILE):
        # Read existing data to avoid duplicates
        existing_df = pd.read_csv(DATA_FILE)
        # Merge and drop duplicates
        df = pd.concat([existing_df, df]).drop_duplicates(subset=['date'])
    df.to_csv(DATA_FILE, index=False)
    print(f"Data saved/updated at {DATA_FILE}")
