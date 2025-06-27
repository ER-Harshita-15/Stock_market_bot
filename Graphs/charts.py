import yfinance as yf
import matplotlib.pyplot as plt
import streamlit as st
import seaborn as sns
sns.set_style("whitegrid")

import pandas as pd
import numpy as np
from chatbot import get_bot_response

def calculate_macd(data, fast=12, slow=26, signal=9):
    exp1 = data['Close'].ewm(span=fast, adjust=False).mean()
    exp2 = data['Close'].ewm(span=slow, adjust=False).mean()
    macd = exp1 - exp2
    signal_line = macd.ewm(span=signal, adjust=False).mean()
    return macd, signal_line

def calculate_rsi(data, period=14):
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def generate_signals(data):
    buy = []
    sell = []
    flag = -1
    for i in range(len(data)):
        if data['MACD'].iloc[i] > data['Signal'].iloc[i] and data['RSI'].iloc[i] < 70:
            if flag != 1:
                buy.append(data['Close'].iloc[i])
                sell.append(np.nan)
                flag = 1
            else:
                buy.append(np.nan)
                sell.append(np.nan)
        elif data['MACD'].iloc[i] < data['Signal'].iloc[i] and data['RSI'].iloc[i] > 30:
            if flag != 0:
                buy.append(np.nan)
                sell.append(data['Close'].iloc[i])
                flag = 0
            else:
                buy.append(np.nan)
                sell.append(np.nan)
        else:
            buy.append(np.nan)
            sell.append(np.nan)
    return buy, sell

def show_chart(ticker):
    try:
        # Fetch 3-month historical stock data for better indicator calculation
        data = yf.Ticker(ticker).history(period="3mo")
        if data.empty:
            st.warning("No data found. Please check the symbol or try a different one.")
            return

        # Calculate indicators
        data['MACD'], data['Signal'] = calculate_macd(data)
        data['RSI'] = calculate_rsi(data)
        data['Buy'], data['Sell'] = generate_signals(data)

        # Bollinger Bands
        data['BB_Middle'] = data['Close'].rolling(window=20).mean()
        data['BB_Std'] = data['Close'].rolling(window=20).std()
        data['BB_Upper'] = data['BB_Middle'] + (2 * data['BB_Std'])
        data['BB_Lower'] = data['BB_Middle'] - (2 * data['BB_Std'])

        # 1. Price with Buy/Sell and Bollinger Bands
        fig1, ax1 = plt.subplots(figsize=(14, 5))
        ax1.plot(data.index, data['Close'], label='Close Price', color='blue')
        ax1.plot(data.index, data['BB_Upper'], label='Bollinger Upper', color='magenta', linestyle='--', linewidth=1)
        ax1.plot(data.index, data['BB_Middle'], label='Bollinger Middle', color='black', linestyle='--', linewidth=1)
        ax1.plot(data.index, data['BB_Lower'], label='Bollinger Lower', color='magenta', linestyle='--', linewidth=1)
        ax1.scatter(data.index, data['Buy'], label='Buy Signal', marker='^', color='green', s=100)
        ax1.scatter(data.index, data['Sell'], label='Sell Signal', marker='v', color='red', s=100)
        ax1.set_title(f"{ticker} - Price, Bollinger Bands & Buy/Sell Signals")
        ax1.set_ylabel("Price")
        ax1.legend()
        ax1.grid(True)
        st.pyplot(fig1)

        # 2. MACD
        fig2, ax2 = plt.subplots(figsize=(14, 3))
        ax2.plot(data.index, data['MACD'], label='MACD', color='purple')
        ax2.plot(data.index, data['Signal'], label='Signal Line', color='orange')
        ax2.set_title("MACD")
        ax2.legend()
        ax2.grid(True)
        st.pyplot(fig2)

        # 3. RSI
        fig3, ax3 = plt.subplots(figsize=(14, 3))
        ax3.plot(data.index, data['RSI'], label='RSI', color='brown')
        ax3.axhline(70, color='red', linestyle='--', linewidth=1)
        ax3.axhline(30, color='green', linestyle='--', linewidth=1)
        ax3.set_title("RSI (14)")
        ax3.set_ylabel("RSI")
        ax3.legend()
        ax3.grid(True)
        st.pyplot(fig3)

        # 4. Volume
        fig4, ax4 = plt.subplots(figsize=(14, 2.5))
        ax4.bar(data.index, data['Volume'], color='grey', label='Volume')
        ax4.set_title("Volume")
        ax4.set_ylabel("Volume")
        ax4.legend()
        ax4.grid(True)
        st.pyplot(fig4)

                # Show table of last few values
        st.dataframe(data[['Close', 'MACD', 'Signal', 'RSI', 'BB_Upper', 'BB_Middle', 'BB_Lower', 'Volume']].tail())

        # Generate and display AI insights
        st.subheader("🧠 AI Insights from Chart")
        with st.spinner("Generating insights..."):
            latest = data.tail(1)
            context = (
                f"Latest close: {latest['Close'].values[0]:.2f}, "
                f"MACD: {latest['MACD'].values[0]:.2f}, "
                f"RSI: {latest['RSI'].values[0]:.2f}, "
                f"Bollinger Upper: {latest['BB_Upper'].values[0]:.2f}, "
                f"Bollinger Lower: {latest['BB_Lower'].values[0]:.2f}, "
                f"Volume: {latest['Volume'].values[0]:.0f}"
            )
            insight = get_bot_response(
                f"Give a short, clear insight for the following stock chart data: {context}", 
                stock=ticker
            )
        st.info(insight)

    except Exception as e:
        st.error(f"Error fetching or plotting stock data: {e}")