import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from scipy.stats import linregress
from config import DATA_FILE, TICKER

# Page settings
st.set_page_config(page_title=f"{TICKER} Stock Dashboard", layout="wide")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv(DATA_FILE, parse_dates=["date"])
    df = df.sort_values("date")
    return df

df = load_data()

# --- KPI Calculations ---
latest_price = df['close'].iloc[-1]
start_price = df['close'].iloc[0]

# Total return %
total_return_pct = ((latest_price - start_price) / start_price) * 100

# Daily returns
df['daily_return'] = df['close'].pct_change()
volatility = df['daily_return'].std() * np.sqrt(252) * 100  # Annualized volatility %

# Trend (linear regression slope)
slope, intercept, r_value, p_value, std_err = linregress(range(len(df)), df['close'])
trend = "Uptrend 📈" if slope > 0 else "Downtrend 📉"

# --- Moving Averages ---
df['SMA_20'] = df['close'].rolling(window=20).mean()
df['SMA_50'] = df['close'].rolling(window=50).mean()
df['EMA_20'] = df['close'].ewm(span=20, adjust=False).mean()

# Display KPIs
col1, col2, col3, col4 = st.columns(4)
col1.metric("Latest Close Price", f"${latest_price:.2f}")
col2.metric("Total Return %", f"{total_return_pct:.2f}%")
col3.metric("Annualized Volatility %", f"{volatility:.2f}%")
col4.metric("Trend", trend)

# --- Chart Section ---
st.subheader("Stock Charts with Moving Averages")
chart_type = st.selectbox("Select Chart Type", ["Close Price", "High vs Low", "Volume", "Close + MA/EMA"])

if chart_type == "Close Price":
    fig = px.line(df, x="date", y="close", title="Daily Closing Price")
elif chart_type == "High vs Low":
    fig = px.line(df, x="date", y=["high", "low"], title="Daily High vs Low")
elif chart_type == "Volume":
    fig = px.bar(df, x="date", y="volume", title="Trading Volume")
else:
    fig = px.line(df, x="date", y=["close", "SMA_20", "SMA_50", "EMA_20"], 
                  title="Close Price with SMA & EMA")
    fig.update_layout(yaxis_title="Price ($)")

st.plotly_chart(fig, use_container_width=True)

# --- Data Preview ---
st.subheader("Latest Records")
st.dataframe(df.tail())
