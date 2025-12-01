def transform_stock_data(df):
    """
    Clean and transform stock data.
    """
    df = df[['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Dividends', 'Stock Splits']]
    df.columns = [col.lower() for col in df.columns]
    df = df.fillna(0)
    return df
