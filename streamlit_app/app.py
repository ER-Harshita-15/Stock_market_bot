import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from Graphs.charts import show_chart
from News_Scrapper.news import get_latest_news
from Chat_bot.chatbot import get_bot_response
from dotenv import load_dotenv
load_dotenv()

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
    ).strip()

with col_example:
    if st.button("📊 Try INFY.NS", type="secondary"):
        st.session_state.symbol = "INFY.NS".strip()
        st.rerun()

# Use session state for symbol
if "symbol" in st.session_state:
    symbol = st.session_state.symbol.strip()

if symbol:
    # Display current analysis
    st.success(f"📊 Analyzing: **{symbol.upper()}**")
    
    # Chart and News layout
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.subheader("📈 Price Chart")
        with st.spinner("Loading chart..."):
            try:
                show_chart(symbol.strip())
            except Exception as e:
                st.error(f"Error loading chart: {str(e)}")
                st.info("💡 Try checking the stock symbol or try again later")
    
    with col2:
        st.subheader("📰 Latest News")
        with st.spinner("Fetching news..."):
            try:
                news_items = get_latest_news(symbol.strip())
                if news_items:
                    for i, news_item in enumerate(news_items[:4]):
                        # Check if it's the new enhanced format (dict) or legacy format (string)
                        if isinstance(news_item, dict):
                            # New enhanced format with structured data
                            st.markdown(f"**{news_item['title']}**")
                            st.caption(f"*Source: {news_item['source']} ({news_item['api']})*")
                            
                            if news_item['summary']:
                                st.write(news_item['summary'])
                            
                            # Add clickable link if URL is available
                            if news_item.get('url') and news_item['url'].startswith('http'):
                                st.markdown(f"🔗 [Read Full Article]({news_item['url']})")
                            else:
                                st.caption("🔗 Full article link not available")
                                
                        else:
                            # Legacy format - simple text (for backward compatibility)
                            if isinstance(news_item, str):
                                # Check if it contains the old formatted structure
                                if "📰 **" in news_item and "*Source:" in news_item:
                                    st.markdown(news_item)
                                    st.caption("🔗 Full article link not available")
                                else:
                                    st.write(f"📄 **News {i+1}:** {news_item}")
                        
                        if i < len(news_items) - 1:  # Don't add divider after last item
                            st.divider()
                else:
                    st.info("📭 No recent news found")
                    
            except Exception as e:
                st.error(f"Error fetching news: {str(e)}")
                st.info("💡 This might be due to API limits or network issues. Try again in a moment.")
        
        # Add refresh button
        if st.button("🔄 Refresh News", key="refresh_news", help="Get the latest news updates"):
            st.rerun()
        
        # Show configured APIs status
        st.caption("📡 **News Sources:** Finnhub, NewsAPI, Alpha Vantage with fallback")

        # Debugging info (you can remove this section after everything works properly)
        with st.expander("🔧 Debug Info", expanded=False):
            st.write("**Environment Variables Status:**")
            apis_status = {
                "FINNHUB_API_KEY": "✅ Set" if os.environ.get("FINNHUB_API_KEY") else "❌ Not Set",
                "NEWSAPI_KEY": "✅ Set" if os.environ.get("NEWSAPI_KEY") else "❌ Not Set", 
                "ALPHA_VANTAGE_API_KEY": "✅ Set" if os.environ.get("ALPHA_VANTAGE_API_KEY") else "❌ Not Set"
            }
            for api, status in apis_status.items():
                st.write(f"- {api}: {status}")
            
            if news_items and len(news_items) > 0:
                st.write("**Last News Item Structure:**")
                st.json(news_items[0] if isinstance(news_items[0], dict) else {"legacy_format": str(news_items[0])[:100]})
    
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
                    response = get_bot_response(query, symbol.strip())
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
            st.caption("Up-to-date market news with clickable links")
        
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
                    st.session_state.symbol = stock.strip()
                    st.rerun()

        # API Setup Instructions
        st.write("### 🔧 Setup Instructions:")
        st.info("""
        **To get real news (instead of fallback links):**
        1. Get a free API key from [Finnhub](https://finnhub.io/) (recommended - 60 calls/minute)
        2. Add `FINNHUB_API_KEY=your_key` to your `.env` file
        3. Restart the app to see real financial news with clickable links
        
        **Optional:** You can also add NewsAPI or Alpha Vantage keys for more coverage.
        """)

# Initialize session states only if not set
if 'selected_query' not in st.session_state:
    st.session_state.selected_query = ""

# Do NOT overwrite symbol if user has typed something
if 'symbol' not in st.session_state and symbol:
    st.session_state.symbol = symbol.strip()