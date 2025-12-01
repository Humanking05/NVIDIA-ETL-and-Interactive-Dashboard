import yfinance as yf
import pandas as pd
from config import TICKER, START_DATE, END_DATE

def extract_stock_data(start_date=None):
    """
    Extract stock data from Yahoo Finance.
    If start_date is provided, fetch data from that date to END_DATE.
    """
    if start_date is None:
        start_date = START_DATE

    ticker = yf.Ticker(TICKER)
    df = ticker.history(start=start_date, end=END_DATE)
    df.reset_index(inplace=True)
    return df
