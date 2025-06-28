import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from Graphs.charts import show_chart
from News_Scrapper.news import get_latest_news
from Chat_bot.chatbot import get_bot_response, generate_ai_insights, display_enhanced_response, display_metrics_in_columns
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
    
    # Technical Indicators Section (New Enhanced Section)
    with st.expander("📊 Technical Indicators Analysis", expanded=False):
        st.subheader("🔍 Quick Technical Overview")
        
        # Example technical indicators - replace with your actual calculations
        # You can integrate with your charts.py or create separate functions
        col_tech1, col_tech2, col_tech3 = st.columns(3)
        
        with col_tech1:
            if st.button("📈 RSI Analysis", use_container_width=True):
                st.session_state.tech_query = f"What is the RSI analysis for {symbol}?"
        
        with col_tech2:
            if st.button("📊 MACD Signal", use_container_width=True):
                st.session_state.tech_query = f"Explain MACD signals for {symbol}"
        
        with col_tech3:
            if st.button("📉 Moving Averages", use_container_width=True):
                st.session_state.tech_query = f"Analyze moving averages for {symbol}"
        
        # Sample technical indicators display (replace with real data)
        if st.checkbox("Show Sample Technical Indicators"):
            # These should be replaced with real calculations from your data
            sample_rsi = 65.5
            sample_macd = "Bullish Crossover"
            sample_sma = "Above 50-day SMA"
            
            # Generate insights for the technical indicators
            with st.spinner("🤖 Generating technical insights..."):
                try:
                    insights = generate_ai_insights(sample_rsi, sample_macd, sample_sma)
                    display_metrics_in_columns(sample_rsi, sample_macd, sample_sma, insights)
                except Exception as e:
                    st.error(f"Error generating technical insights: {str(e)}")
    
    st.divider()
    
    # AI Assistant section (Enhanced)
    st.subheader("🤖 AI Stock Market Analyst")
    st.caption("Get professional market analysis without investment recommendations")
    
    # Quick questions
    st.write("**💡 Quick Analysis Questions:**")
    col_q1, col_q2, col_q3, col_q4 = st.columns(4)
    
    with col_q1:
        if st.button("📊 Market Sentiment", use_container_width=True):
            st.session_state.selected_query = f"What's the current market sentiment for {symbol}?"
    
    with col_q2:
        if st.button("📈 Technical Analysis", use_container_width=True):
            st.session_state.selected_query = f"Provide technical analysis for {symbol}"
    
    with col_q3:
        if st.button("💼 Fundamental Analysis", use_container_width=True):
            st.session_state.selected_query = f"What are the fundamental metrics for {symbol}?"
    
    with col_q4:
        if st.button("⚠️ Risk Factors", use_container_width=True):
            st.session_state.selected_query = f"What are the key risk factors for {symbol}?"
    
    # Handle technical query if set
    if st.session_state.get('tech_query'):
        st.session_state.selected_query = st.session_state.tech_query
        del st.session_state.tech_query
    
    # Query input
    default_query = st.session_state.get('selected_query', '')
    query = st.text_area(
        "💬 Ask for detailed stock analysis:",
        value=default_query,
        placeholder="e.g., Analyze the financial health of this company, What are the key technical indicators showing?",
        height=80
    )
    
    # Analysis type selector
    analysis_type = st.selectbox(
        "🎯 Select Analysis Focus:",
        ["Comprehensive Analysis", "Technical Analysis Only", "Fundamental Analysis Only", "Market Sentiment Only"],
        help="Choose the type of analysis you want"
    )
    
    if st.button("🚀 Get Professional Analysis", type="primary"):
        if query:
            # Modify query based on analysis type
            if analysis_type == "Technical Analysis Only":
                enhanced_query = f"Focus only on technical analysis: {query}"
            elif analysis_type == "Fundamental Analysis Only":
                enhanced_query = f"Focus only on fundamental analysis: {query}"
            elif analysis_type == "Market Sentiment Only":
                enhanced_query = f"Focus only on market sentiment and expert opinions: {query}"
            else:
                enhanced_query = query
            
            with st.spinner("🤖 AI Analyst is preparing comprehensive analysis..."):
                try:
                    response = get_bot_response(enhanced_query, symbol.strip())
                    
                    # Enhanced display with proper formatting
                    st.success("🎯 **Professional Market Analysis:**")
                    display_enhanced_response(response)  # ✅ NEW: Enhanced display instead of st.write()
                    
                    # Add analysis metadata
                    st.divider()
                    st.caption(f"📅 Analysis generated on {st.session_state.get('analysis_time', 'now')} | 📊 Stock: {symbol.upper()} | 🎯 Focus: {analysis_type}")
                    
                    # Clear selected query after response
                    if 'selected_query' in st.session_state:
                        del st.session_state.selected_query
                        
                except Exception as e:
                    st.error(f"Error getting AI response: {str(e)}")
                    st.info("💡 Try rephrasing your question or check connection")
        else:
            st.warning("Please enter a question first!")
    
    # Additional Analysis Tools
    with st.expander("🔧 Advanced Analysis Tools", expanded=False):
        st.write("**Coming Soon:**")
        st.info("• Portfolio analysis • Sector comparison • Historical performance • Risk assessment")

else:
    # Welcome section (Enhanced)
    st.info("👆 **Get Started:** Enter a stock symbol above to begin professional analysis")
    
    with st.container():
        st.write("### 🌟 Enhanced Features:")
        col_f1, col_f2, col_f3, col_f4 = st.columns(4)
        
        with col_f1:
            st.write("📊 **Real-time Charts**")
            st.caption("Interactive price charts and technical indicators")
        
        with col_f2:
            st.write("📰 **Latest News**")
            st.caption("Up-to-date market news with clickable links")
        
        with col_f3:
            st.write("🤖 **AI Analysis**")
            st.caption("Professional insights without investment advice")
        
        with col_f4:
            st.write("📈 **Technical Tools**")
            st.caption("RSI, MACD, Moving Averages analysis")
        
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
        
        # Sample Analysis Preview
        with st.expander("🎯 See Sample Analysis Format", expanded=False):
            st.write("**Professional Analysis Structure:**")
            st.markdown("""
            ### 📊 MARKET SENTIMENT & OVERVIEW
            - Current market perception and expert consensus
            - Recent news impact and sector performance
            
            ### 📈 TECHNICAL ANALYSIS
            - Key technical indicators and chart patterns
            - Support/resistance levels and momentum
            
            ### 💼 FUNDAMENTAL ANALYSIS
            - Financial metrics and earnings performance
            - Industry comparison and competitive position
            
            ### 🎯 KEY INSIGHTS
            - Most significant factors and potential catalysts
            """)

# Initialize session states
if 'selected_query' not in st.session_state:
    st.session_state.selected_query = ""

if 'tech_query' not in st.session_state:
    st.session_state.tech_query = ""

# Store analysis time
import datetime
if 'analysis_time' not in st.session_state:
    st.session_state.analysis_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

# Do NOT overwrite symbol if user has typed something
if 'symbol' not in st.session_state and symbol:
    st.session_state.symbol = symbol.strip()