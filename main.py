from etl.extract import extract_stock_data
from etl.transform import transform_stock_data
from etl.load import load_to_csv
import pandas as pd
import os
from config import DATA_FILE, START_DATE

def run_etl():
    # Determine start date for incremental update
    if os.path.exists(DATA_FILE):
        existing_df = pd.read_csv(DATA_FILE)
        last_date = pd.to_datetime(existing_df['date']).max() + pd.Timedelta(days=1)
        start_date = last_date.strftime("%Y-%m-%d")
    else:
        start_date = START_DATE

    # Extract
    df = extract_stock_data(start_date=start_date)
    if df.empty:
        print("No new data to update.")
        return

    # Transform
    df = transform_stock_data(df)

    # Show preview
    print("\nPreview of new data (first 5 rows):")
    print(df.head())

    # Load
    load_to_csv(df)
    print("\nETL completed successfully.")

if __name__ == "__main__":
    run_etl()
