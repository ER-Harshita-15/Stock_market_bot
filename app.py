import streamlit as st
from charts import show_chart
from news import get_latest_news
from chatbot import get_bot_response

st.set_page_config(page_title="AI Stock Market Bot", layout="wide")
st.title("📈 AI Stock Market Bot")

symbol = st.text_input("🔎 Enter Stock Symbol or Topic (e.g. INFY.NS, Reliance, Nifty):")

if symbol:
    st.subheader("📊 Stock Price Chart")
    show_chart(symbol)

    st.subheader("📰 Latest News")
    for headline in get_latest_news(symbol):
        st.markdown(f"- {headline}")

    st.subheader("🤖 Ask AI about this stock/topic:")
    query = st.text_input("Type your question")

    @st.cache_data(show_spinner=False)
    def cached_response(q, s):
        return get_bot_response(q, s)

    if query:
        response = cached_response(query, symbol)
        st.success(response)
