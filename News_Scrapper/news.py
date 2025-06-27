import requests
from bs4 import BeautifulSoup

def get_latest_news(query):
    try:
        # Build Google News URL for search
        url = f"https://www.google.com/search?q={query}+stock+news&hl=en&tbm=nws"
        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract news headlines
        headlines = [h.text for h in soup.select("div.BNeawe.vvjwJb.AP7Wnd")][:5]

        if not headlines:
            return ["No recent news found."]
        
        return headlines

    except Exception as e:
        return [f"Error fetching news: {e}"]
