
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
import warnings

warnings.filterwarnings("ignore")

# Load dataset
df = pd.read_csv('precious_metals_futures.csv')

# Convert date column to datetime
df['date'] = pd.to_datetime(df['date'])

# Sidebar dropdowns
st.sidebar.header("Filter Data")
selected_metal = st.sidebar.selectbox("Select Metal:", df['commodity'].unique())
selected_chart = st.sidebar.selectbox("Select Chart Type:", ["OHLC", "Candlestick", "Line", "Bar"])
selected_range = st.sidebar.selectbox("Select Time Range:", ["24h", "7d", "1mo", "1yr"])

# Filter data based on selection
df_filtered = df[df['commodity'] == selected_metal].copy()
latest_date = df_filtered['date'].max()

if selected_range == "24h":
    df_filtered = df_filtered[df_filtered['date'] >= latest_date - pd.Timedelta(days=1)]
elif selected_range == "7d":
    df_filtered = df_filtered[df_filtered['date'] >= latest_date - pd.Timedelta(weeks=1)]
elif selected_range == "1mo":
    df_filtered = df_filtered[df_filtered['date'] >= latest_date - pd.Timedelta(weeks=4)]
elif selected_range == "1yr":
    df_filtered = df_filtered[df_filtered['date'] >= latest_date - pd.Timedelta(weeks=52)]

# Plot based on selection
st.title(f"{selected_metal} Price Chart")

if selected_chart == "OHLC":
    fig = go.Figure(data=[go.Ohlc(x=df_filtered['date'],
                                  open=df_filtered['open'],
                                  high=df_filtered['high'],
                                  low=df_filtered['low'],
                                  close=df_filtered['close'])])
elif selected_chart == "Candlestick":
    fig = go.Figure(data=[go.Candlestick(x=df_filtered['date'],
                                         open=df_filtered['open'],
                                         high=df_filtered['high'],
                                         low=df_filtered['low'],
                                         close=df_filtered['close'])])
elif selected_chart == "Line":
    fig = px.line(df_filtered, x='date', y='close', title=f"{selected_metal} Price Over Time")
elif selected_chart == "Bar":
    fig = px.bar(df_filtered, x='date', y='close', title=f"{selected_metal} Closing Prices")

st.plotly_chart(fig)
