import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_latest_news(query):
    # Marketaux API key is usually named 'MARKETAUX_API_KEY' in .env
    api_key = os.environ.get("MARKETAUX_API_KEY") 
    
    if not api_key:
        return ["Marketaux API key not found. Please set MARKETAUX_API_KEY in your .env file."]
    
    # Marketaux API endpoint for all news
    BASE_URL = "https://api.marketaux.com/v1/news/all"
    
    # Marketaux uses 'search' or 'symbols' for queries.
    # For a general company name like "Manali Petrochemicals", 'search' is more appropriate.
    # If you have a stock symbol (e.g., "MPCL" for Manali Petrochemicals), you could use 'symbols' parameter.
    
    params = {
        "api_token": api_key,
        "search": query,  # Use 'search' for general queries
        "language": "en", # Specify language (Marketaux supports many)
        "limit": 5        # Limit the number of articles
    }

    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
        
        data = response.json()
        
        # Marketaux API response structure has a "data" key containing a list of articles
        if "data" in data and data["data"]:
            news_articles = []
            for article in data["data"]:
                title = article.get('title', 'No Title')
                source = article.get('source', 'Unknown Source')
                news_articles.append(f"{title} ({source})")
            return news_articles
        elif "meta" in data and data["meta"].get("found") == 0:
            return [f"No recent news found for '{query}'."]
        elif "error" in data:
            return [f"Marketaux API error: {data['error']}"]
        else:
            return ["No recent news found or unexpected API response format."]
            
    except requests.exceptions.RequestException as e:
        # Catch specific request exceptions (network issues, invalid URL, etc.)
        return [f"Error fetching news from Marketaux API: {e}"]
    except Exception as e:
        # Catch any other unexpected errors
        return [f"An unexpected error occurred: {e}"]