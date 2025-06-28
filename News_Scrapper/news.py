import requests
import os
from dotenv import load_dotenv
import yfinance as yf
from datetime import datetime, timedelta

# Load environment variables from .env file
load_dotenv()

class NewsAggregator:
    def __init__(self):
        # API Keys from environment
        self.alpha_vantage_key = os.environ.get("ALPHA_VANTAGE_API_KEY")
        self.finnhub_key = os.environ.get("FINNHUB_API_KEY")
        self.newsapi_key = os.environ.get("NEWSAPI_KEY")
        
    def get_company_name_from_symbol(self, symbol):
        """Extract company name from stock symbol using yfinance"""
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            # Try different possible name fields
            company_name = (
                info.get('longName') or 
                info.get('shortName') or 
                info.get('displayName') or
                symbol.replace('.NS', '').replace('.BO', '')
            )
            
            return company_name
        except Exception as e:
            print(f"Error getting company name: {e}")
            return symbol.replace('.NS', '').replace('.BO', '')

    def get_finnhub_news(self, symbol, company_name):
        """Get news from Finnhub API - Very generous free tier"""
        if not self.finnhub_key:
            return []
            
        try:
            # Convert Indian symbols to base symbol for Finnhub
            base_symbol = symbol.replace('.NS', '').replace('.BO', '')
            
            # Finnhub company news endpoint
            url = "https://finnhub.io/api/v1/company-news"
            
            # Date range - last 30 days
            to_date = datetime.now().strftime('%Y-%m-%d')
            from_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
            
            params = {
                'symbol': base_symbol,
                'from': from_date,
                'to': to_date,
                'token': self.finnhub_key
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            news_articles = []
            
            for article in data[:5]:  # Limit to 5 articles
                title = article.get('headline', 'No Title')
                source = article.get('source', 'Finnhub')
                summary = article.get('summary', '')[:100] + '...' if article.get('summary') else ''
                url_link = article.get('url', '')
                
                news_articles.append({
                    'title': title,
                    'source': source,
                    'summary': summary,
                    'url': url_link,
                    'api': 'Finnhub'
                })
                
            return news_articles
            
        except Exception as e:
            print(f"Finnhub API error: {e}")
            return []
    
    def get_alpha_vantage_news(self, symbol, company_name):
        """Get news from Alpha Vantage API"""
        if not self.alpha_vantage_key:
            return []
            
        try:
            url = "https://www.alphavantage.co/query"
            params = {
                'function': 'NEWS_SENTIMENT',
                'tickers': symbol.replace('.NS', '').replace('.BO', ''),
                'apikey': self.alpha_vantage_key,
                'limit': 5
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            news_articles = []
            
            if 'feed' in data:
                for article in data['feed'][:5]:
                    title = article.get('title', 'No Title')
                    source = article.get('source', 'Alpha Vantage')
                    summary = article.get('summary', '')[:100] + '...' if article.get('summary') else ''
                    url_link = article.get('url', '')
                    
                    news_articles.append({
                        'title': title,
                        'source': source,
                        'summary': summary,
                        'url': url_link,
                        'api': 'Alpha Vantage'
                    })
                    
            return news_articles
            
        except Exception as e:
            print(f"Alpha Vantage API error: {e}")
            return []
    
    def get_newsapi_news(self, symbol, company_name):
        """Get news from NewsAPI - Good for general company news"""
        if not self.newsapi_key:
            return []
            
        try:
            url = "https://newsapi.org/v2/everything"
            
            # Create search query with company name and stock-related keywords
            query = f'"{company_name}" AND (stock OR shares OR trading OR market OR financial OR earnings OR revenue)'
            
            params = {
                'q': query,
                'language': 'en',
                'sortBy': 'publishedAt',
                'pageSize': 5,
                'apiKey': self.newsapi_key
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            news_articles = []
            
            if data.get('status') == 'ok' and 'articles' in data:
                for article in data['articles']:
                    title = article.get('title', 'No Title')
                    source = article.get('source', {}).get('name', 'NewsAPI')
                    description = article.get('description', '')
                    summary = description[:100] + '...' if description else ''
                    url_link = article.get('url', '')
                    
                    news_articles.append({
                        'title': title,
                        'source': source,
                        'summary': summary,
                        'url': url_link,
                        'api': 'NewsAPI'
                    })
                    
            return news_articles
            
        except Exception as e:
            print(f"NewsAPI error: {e}")
            return []
    
    def get_fallback_news(self, symbol, company_name):
        """Fallback method that provides useful financial links"""
        try:
            # Clean symbol for different platforms
            clean_symbol = symbol.replace('.NS', '').replace('.BO', '')
            
            fallback_news = [
                {
                    'title': f"Latest {company_name} Stock Analysis",
                    'source': 'Yahoo Finance',
                    'summary': f"Get comprehensive stock analysis, charts, and financial data for {company_name}",
                    'url': f"https://finance.yahoo.com/quote/{symbol}",
                    'api': 'Fallback'
                },
                {
                    'title': f"{company_name} Market News & Updates",
                    'source': 'Google Finance',
                    'summary': f"Stay updated with the latest market news and performance data for {company_name}",
                    'url': f"https://www.google.com/finance/quote/{clean_symbol}:NSE",
                    'api': 'Fallback'
                },
                {
                    'title': f"{company_name} Company Profile & News",
                    'source': 'MoneyControl',
                    'summary': f"Detailed company information, financial results, and market news for {company_name}",
                    'url': f"https://www.moneycontrol.com/india/stockpricequote/{clean_symbol.lower()}",
                    'api': 'Fallback'
                }
            ]
            
            return fallback_news[:2]  # Return 2 fallback links
            
        except Exception as e:
            print(f"Fallback error: {e}")
            return [{
                'title': f"Market Information for {company_name}",
                'source': 'Financial Portal',
                'summary': f"General market information and analysis for {company_name}",
                'url': f"https://finance.yahoo.com/quote/{symbol}",
                'api': 'Fallback'
            }]

def get_latest_news(query):
    """
    Main function to get latest news with improved relevance and multiple API support
    """
    news_aggregator = NewsAggregator()
    
    # Clean the query (remove common stock suffixes)
    symbol = query.strip().upper()
    
    # Get company name for better search
    company_name = news_aggregator.get_company_name_from_symbol(symbol)
    
    all_news = []
    
    # Try different APIs in order of preference
    # 1. Finnhub (most generous free tier)
    finnhub_news = news_aggregator.get_finnhub_news(symbol, company_name)
    if finnhub_news:
        all_news.extend(finnhub_news)
    
    # 2. NewsAPI (good for general news)
    if len(all_news) < 3:
        newsapi_news = news_aggregator.get_newsapi_news(symbol, company_name)
        all_news.extend(newsapi_news)
    
    # 3. Alpha Vantage (limited but good quality)
    if len(all_news) < 2:
        av_news = news_aggregator.get_alpha_vantage_news(symbol, company_name)
        all_news.extend(av_news)
    
    # 4. Fallback if no APIs work
    if not all_news:
        fallback_news = news_aggregator.get_fallback_news(symbol, company_name)
        all_news.extend(fallback_news)
    
    # Format for display
    if all_news:
        formatted_news = []
        for article in all_news[:5]:  # Limit to 5 total articles
            if isinstance(article, dict):
                # Create formatted news with clickable link
                title = article['title']
                source = article['source']
                api = article['api']
                summary = article['summary']
                url = article.get('url', '')
                
                if url and url.startswith('http'):
                    # If we have a valid URL, make it clickable
                    formatted_news.append({
                        'title': title,
                        'source': source,
                        'api': api,
                        'summary': summary,
                        'url': url,
                        'display': f"📰 **{title}**\n*Source: {source} ({api})*\n{summary}"
                    })
                else:
                    # No URL available
                    formatted_news.append({
                        'title': title,
                        'source': source,
                        'api': api,
                        'summary': summary,
                        'url': None,
                        'display': f"📰 **{title}**\n*Source: {source} ({api})*\n{summary}"
                    })
            else:
                # Handle legacy string format
                formatted_news.append({
                    'title': str(article),
                    'source': 'Unknown',
                    'api': 'Legacy',
                    'summary': '',
                    'url': None,
                    'display': str(article)
                })
        
        return formatted_news
    else:
        return [{
            'title': f"No recent news found for '{company_name}' ({symbol})",
            'source': 'System',
            'api': 'Info',
            'summary': 'The stock symbol might be incorrect or there might be no recent news coverage.',
            'url': None,
            'display': f"No recent news found for '{company_name}' ({symbol}). The stock symbol might be incorrect or there might be no recent news coverage."
        }]

# Backward compatibility function
def get_latest_news_legacy(query):
    """Legacy function for backward compatibility"""
    return get_latest_news(query)

