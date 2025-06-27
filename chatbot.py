import os
import requests
import streamlit as st
from dotenv import load_dotenv
load_dotenv()

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
}

def query_groq(messages, model="llama3-70b-8192"):
    try:
        payload = {
            "model": model,
            "messages": messages,
            "max_tokens": 2000,
            "temperature": 0.7
        }
        response = requests.post(GROQ_API_URL, headers=headers, json=payload, timeout=30)
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def get_bot_response(user_query, stock="stock market"):
    system_prompt = (
        f"You are a financial advisor. The user is asking about the stock: {stock}. "
        "Provide a structured and complete recommendation using clear, simple language. "
        "Include any relevant technical indicators, fundamental stats, or expert sentiment. "
        "Avoid financial jargon. Output should be in 3 short paragraphs and end your response with 'Thank you.':\n\n"
        "1. Overview of expert sentiment and market view.\n"
        "2. Technical indicators (moving average, RSI, price action, etc.).\n"
        "3. Key fundamental metrics and your buy/sell/hold recommendation.\n"
    )
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
    result = query_groq(messages, model="llama3-70b-8192")
    if "error" in result:
        return f"Error: {result['error']}"
    try:
        return result["choices"][0]["message"]["content"].strip()
    except:
        return "⚠️ AI couldn't generate insights."