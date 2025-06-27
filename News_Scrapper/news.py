import requests
import os
from dotenv import load_dotenv
load_dotenv()

def get_latest_news(query):
    api_key = os.environ.get("NEWSAPI_KEY")  # Store your API key in an environment variable
    if not api_key:
        return ["News API key not found. Please set NEWSAPI_KEY in your environment."]
    url = (
        f"https://newsapi.org/v2/everything?"
        f"q={query}&"
        f"sortBy=publishedAt&"
        f"language=en&"
        f"apiKey={api_key}"
    )
    try:
        response = requests.get(url)
        data = response.json()
        print(data)
        if "articles" in data and data["articles"]:
            return [f"{article['title']} ({article['source']['name']})" for article in data["articles"][:5]]
        elif "message" in data:
            return [f"News API error: {data['message']}"]
        else:
            return ["No recent news found."]
    except Exception as e:
        return [f"Error fetching news: {e}"]
    
get_latest_news("Manali Petrochemicals")