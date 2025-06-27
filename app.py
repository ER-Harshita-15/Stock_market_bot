import streamlit as st
from charts import show_chart
from news import get_latest_news
from chatbot import get_bot_response

# Page configuration
st.set_page_config(
    page_title="Stock Market Bot",
    page_icon="📈",
    layout="wide"
)

# Header
st.title("📈 Stock Market Bot")
st.caption("Your smart companion for stock analysis")

# Stock input with example
col_input, col_example = st.columns([3, 1])

with col_input:
    symbol = st.text_input(
        "🔍 Enter Stock Symbol:",
        placeholder="e.g., INFY.NS, TCS.NS, RELIANCE.NS",
        help="Enter NSE/BSE stock symbols or popular indices"
    )

with col_example:
    if st.button("📊 Try INFY.NS", type="secondary"):
        st.session_state.symbol = "INFY.NS"
        st.rerun()

# Use session state for symbol
if "symbol" in st.session_state:
    symbol = st.session_state.symbol

if symbol:
    # Display current analysis
    st.success(f"📊 Analyzing: **{symbol.upper()}**")
    
    # Chart and News layout
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.subheader("📈 Price Chart")
        with st.spinner("Loading chart..."):
            try:
                show_chart(symbol)
            except Exception as e:
                st.error(f"Error loading chart: {str(e)}")
                st.info("💡 Try checking the stock symbol or try again later")
    
    with col2:
        st.subheader("📰 Latest News")
        with st.spinner("Fetching news..."):
            try:
                news_items = get_latest_news(symbol)
                if news_items:
                    for i, headline in enumerate(news_items[:4]):
                        st.write(f"📄 **News {i+1}:** {headline}")
                        st.divider()
                else:
                    st.info("📭 No recent news found")
            except Exception as e:
                st.error(f"Error fetching news: {str(e)}")
    
    st.divider()
    
    # AI Assistant section
    st.subheader("🤖 AI Assistant")
    
    # Quick questions
    st.write("**💡 Quick Questions:**")
    col_q1, col_q2, col_q3 = st.columns(3)
    
    with col_q1:
        if st.button("📊 Current Trend", use_container_width=True):
            st.session_state.selected_query = f"What's the current trend for {symbol}?"
    
    with col_q2:
        if st.button("💰 Buy/Sell Signal", use_container_width=True):
            st.session_state.selected_query = f"Should I buy or sell {symbol}?"
    
    with col_q3:
        if st.button("⚠️ Risk Analysis", use_container_width=True):
            st.session_state.selected_query = f"What are the risks of investing in {symbol}?"
    
    # Query input
    default_query = st.session_state.get('selected_query', '')
    query = st.text_area(
        "💬 Ask about this stock:",
        value=default_query,
        placeholder="e.g., What's the price target? Is it a good long-term investment?",
        height=80
    )
    
    if st.button("🚀 Get AI Analysis", type="primary"):
        if query:
            with st.spinner("🤖 AI is analyzing..."):
                try:
                    response = get_bot_response(query, symbol)
                    st.success("🎯 **AI Response:**")
                    st.write(response)
                    
                    # Clear selected query after response
                    if 'selected_query' in st.session_state:
                        del st.session_state.selected_query
                        
                except Exception as e:
                    st.error(f"Error getting AI response: {str(e)}")
                    st.info("💡 Try rephrasing your question or check connection")
        else:
            st.warning("Please enter a question first!")

else:
    # Welcome section
    st.info("👆 **Get Started:** Enter a stock symbol above to begin analysis")
    
    with st.container():
        st.write("### 🌟 Features:")
        col_f1, col_f2, col_f3 = st.columns(3)
        
        with col_f1:
            st.write("📊 **Real-time Charts**")
            st.caption("Interactive price charts and technical indicators")
        
        with col_f2:
            st.write("📰 **Latest News**")
            st.caption("Up-to-date market news and updates")
        
        with col_f3:
            st.write("🤖 **AI Analysis**")
            st.caption("Intelligent insights and recommendations")
        
        st.divider()
        
        st.write("**💡 Popular Symbols to Try:**")
        popular_cols = st.columns(5)
        popular_stocks = ["INFY.NS", "TCS.NS", "RELIANCE.NS", "NIFTY", "SENSEX"]
        
        for i, stock in enumerate(popular_stocks):
            with popular_cols[i]:
                if st.button(stock, key=f"pop_{stock}", use_container_width=True):
                    st.session_state.symbol = stock
                    st.rerun()

# Initialize session states
if 'selected_query' not in st.session_state:
    st.session_state.selected_query = ""
if 'symbol' not in st.session_state:
    st.session_state.symbol = ""