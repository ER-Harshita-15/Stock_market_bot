import os
import requests
import streamlit as st
from dotenv import load_dotenv
import re
load_dotenv()

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

headers = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json"
}

def query_groq(messages, model="llama-3.3-70b-versatile"):
    try:
        payload = {
            "model": model,
            "messages": messages,
            "max_tokens": 1000,
            "temperature": 0.3,
            "top_p": 0.9,
        }
        response = requests.post(GROQ_API_URL, headers=headers, json=payload, timeout=30)
        return response.json()
    except Exception as e:
        return {"error": str(e)}
    
# 5th Point: Post-Processing Improvements
def format_response(response):
    """Enhanced formatting for better readability"""
    if not response:
        return response
    
    # Fix double line breaks and spacing
    response = re.sub(r'\n{3,}', '\n\n', response)
    
    # Ensure proper header formatting with spacing
    response = re.sub(r'(?<!\n)(#{1,3})', r'\n\1', response)
    response = re.sub(r'(#{1,3}[^\n]+)', r'\1\n', response)
    
    # Add spacing around bullet points
    response = re.sub(r'(?<!\n)(\s*[-*•]\s)', r'\n\1', response)
    
    # Clean up multiple spaces
    response = re.sub(r' {2,}', ' ', response)
    
    # Ensure sections are properly separated
    response = re.sub(r'(📊|📈|💼|🎯)', r'\n\1', response)
    
    return response.strip()

def display_enhanced_response(response):
    """6th Point: Advanced Organization with Streamlit"""
    
    # Split response into sections
    sections = response.split('###')
    
    if len(sections) > 1:
        # Display first part (intro) if exists
        if sections[0].strip():
            st.markdown(sections[0].strip())
            st.divider()
        
        # Process each section
        for i, section in enumerate(sections[1:], 1):
            if section.strip():
                lines = section.strip().split('\n')
                title = lines[0].strip()
                content = '\n'.join(lines[1:]).strip()
                
                # Create expandable sections for better organization
                with st.expander(f"**{title}**", expanded=True):
                    st.markdown(content)
                
                # Add visual separator between sections
                if i < len(sections) - 1:
                    st.divider()
    else:
        # Fallback for responses without clear sections
        st.markdown(response)

def display_metrics_in_columns(rsi, macd_signal, sma_signal, insights):
    """6th Point: Display metrics in organized columns"""
    
    st.subheader("📊 Technical Indicators Overview")
    
    # Create columns for metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="RSI", 
            value=f"{rsi:.2f}" if isinstance(rsi, (int, float)) else str(rsi),
            delta="Overbought" if isinstance(rsi, (int, float)) and rsi > 70 else "Oversold" if isinstance(rsi, (int, float)) and rsi < 30 else "Neutral"
        )
    
    with col2:
        st.metric(
            label="MACD Signal", 
            value=str(macd_signal),
            delta="Bullish" if "bullish" in str(macd_signal).lower() else "Bearish" if "bearish" in str(macd_signal).lower() else "Neutral"
        )
    
    with col3:
        st.metric(
            label="SMA Signal", 
            value=str(sma_signal),
            delta="Uptrend" if "up" in str(sma_signal).lower() else "Downtrend" if "down" in str(sma_signal).lower() else "Sideways"
        )
    
    st.divider()
    
    # Display AI insights in an organized way
    if insights:
        st.subheader("🤖 AI Technical Insights")
        with st.expander("View Detailed Analysis", expanded=False):
            st.markdown(insights)

def get_bot_response(user_query, stock="stock market"):
    system_prompt = (
       f"You are a professional stock market analyst specializing in {stock}. Your role is to provide comprehensive, "
        "objective analysis based on technical indicators, fundamental metrics, and market sentiment. "
        
        "IMPORTANT GUIDELINES:\n"
        "- NEVER provide buy, sell, or hold recommendations\n"
        "- If asked for investment advice or recommendations, politely explain that you can provide detailed analysis "
        "but cannot recommend specific investment actions\n"
        "- Focus on presenting factual data, trends, and analytical insights\n"
        "- Use clear, professional language while avoiding complex jargon\n"
        "- Present information objectively without bias toward bullish or bearish sentiment\n\n"
        "- Use professional language while keeping explanations accessible\n"

        "Structure your response in 3 clear sections:\n"
        "1. MARKET SENTIMENT & EXPERT VIEWS: Current market perception, analyst opinions, and overall sentiment\n"
        "2. TECHNICAL ANALYSIS: Key technical indicators (moving averages, RSI, MACD, volume, price patterns, support/resistance levels)\n"
        "3. FUNDAMENTAL ANALYSIS: Financial metrics, earnings data, valuation ratios, company performance, and industry factors\n\n"
        
        "Key Insights:\n"
        "- Most significant factors currently affecting the stock"
        "- Potential catalysts or risk factors to monitor"
        "- Technical and fundamental convergence/divergence"
        "\n\n"
        "If someone asks for investment recommendations, respond with: "
        "'I can provide you with comprehensive technical and fundamental analysis to help you understand the stock's current position, "
        "but I cannot recommend whether you should buy, sell, or hold. Investment decisions should be made based on your own "
        "research, risk tolerance, and financial goals, preferably with consultation from a licensed financial advisor.'\n\n"

        # Enhanced system prompt additions:
        "- Use specific data points and percentages when available"
        "- Explain technical terms in parentheses for clarity"
        "- Prioritize the most recent and relevant information"
        "- Use comparative analysis (vs. sector, vs. historical performance)"
        "- Include risk assessment and volatility analysis"
        "- Mention key dates for earnings, events, or announcements"
        
        "End your analysis with: 'This analysis is for informational purposes only and should not be considered as investment advice.'")
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_query}
    ]
    with st.spinner("🤖 Generating AI recommendation..."):
        result = query_groq(messages)
    if "error" in result:
        return f"Error from API: {result['error']}"
    try:
        return result["choices"][0]["message"]["content"].strip()
    except:
        return "⚠️ Unable to generate a complete answer."

def generate_ai_insights(rsi, macd_signal, sma_signal):
    prompt = (
        f"You are a financial assistant. Based on these:\n"
        f"- RSI: {rsi}\n"
        f"- SMA Signal: {sma_signal}\n"
        f"- MACD Signal: {macd_signal}\n\n"
        "Write short, user-friendly insights for each indicator in one line. Avoid technical jargon."
    )
    messages = [
        {"role": "system", "content": "You are a financial assistant."},
        {"role": "user", "content": prompt}
    ]
    result = query_groq(messages, model="llama-3.3-70b-versatile")
    if "error" in result:
        return f"Error: {result['error']}"
    try:
        return result["choices"][0]["message"]["content"].strip()
    except:
        return "⚠️ AI couldn't generate insights."