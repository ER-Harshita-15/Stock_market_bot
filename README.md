# 📈 Stock Market Bot

> **🚀 Your intelligent companion for professional stock market analysis**

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://stockmarketbot-wus6mtpbsysibc5qbrtdsk.streamlit.app/)

An advanced stock market analysis platform that combines real-time data visualization, AI-powered insights, and comprehensive news aggregation to provide professional-grade market analysis without investment recommendations.

## 🌟 Live Demo

**Try it now:** [Stock Market Bot Live App](https://stockmarketbot-wus6mtpbsysibc5qbrtdsk.streamlit.app/)

## ✨ Key Features

### 📊 **Real-Time Technical Analysis**
- Interactive price charts with Bollinger Bands
- Technical indicators: RSI, MACD, Moving Averages
- Buy/sell signal generation
- Volume analysis and market trends

### 📰 **Multi-Source News Aggregation**
- **Finnhub API**: Real-time financial news with generous free tier
- **NewsAPI**: Comprehensive market coverage
- **Alpha Vantage**: Professional financial data
- **Smart Fallback**: Reliable financial portal links when APIs are unavailable

### 🤖 **AI-Powered Market Analyst**
- Professional market sentiment analysis
- Technical and fundamental analysis
- Risk assessment and trend identification
- Structured insights without investment advice

### 📈 **Enhanced User Experience**
- Clean, modern interface with organized sections
- Quick-access buttons for common analysis types
- Real-time data updates and interactive charts
- Mobile-friendly responsive design

## 🚀 Getting Started

### 📋 Prerequisites

```bash
Python 3.8+
```

### 🔧 Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/stock-market-bot.git
cd stock-market-bot
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your API keys (optional but recommended)
nano .env
```

4. **Run the application**
```bash
streamlit run streamlit_app/app.py
```

## 🔑 API Configuration

### 🎯 Recommended Setup (Free Tier)

**Finnhub API** (Highly Recommended - 60 calls/minute free)
1. Register at [Finnhub.io](https://finnhub.io/)
2. Get your free API key
3. Add to `.env`: `FINNHUB_API_KEY=your_key_here`

### 📈 Optional APIs for Enhanced Coverage

**NewsAPI** (Free: 1000 requests/month)
1. Register at [NewsAPI.org](https://newsapi.org/)
2. Add to `.env`: `NEWSAPI_KEY=your_key_here`

**Alpha Vantage** (Free: 5 calls/minute)
1. Register at [Alpha Vantage](https://www.alphavantage.co/)
2. Add to `.env`: `ALPHA_VANTAGE_API_KEY=your_key_here`

**GROQ API** (Required for AI Analysis)
1. Register at [GROQ](https://groq.com/)
2. Add to `.env`: `GROQ_API_KEY=your_key_here`

## 📁 Project Structure

```
stock-market-bot/
├── 📱 streamlit_app/
│   ├── __init__.py
│   └── app.py                 # Main Streamlit application
├── 📊 Graphs/
│   ├── __init__.py
│   └── charts.py              # Chart generation and technical indicators
├── 📰 News_Scrapper/
│   ├── __init__.py
│   └── news.py                # Multi-source news aggregation
├── 🤖 Chat_bot/
│   ├── __init__.py
│   └── chatbot.py             # AI analysis engine
├── 📋 requirements.txt        # Python dependencies
├── 🔧 .env.example           # Environment variables template
├── 📝 .gitignore             # Git ignore rules
└── 📖 README.md              # This file
```

## 🎯 Usage Examples

### 📊 Basic Stock Analysis
```python
# Enter stock symbol: INFY.NS, TCS.NS, RELIANCE.NS
# Get instant charts, news, and AI insights
```

### 🤖 AI Analysis Queries
- "What's the current market sentiment for INFY.NS?"
- "Provide technical analysis for TCS.NS"
- "What are the key risk factors for RELIANCE.NS?"
- "Analyze the financial health of this company"

### 📈 Supported Stock Formats
- **Indian Stocks**: `INFY.NS`, `TCS.NS`, `RELIANCE.NS`
- **US Stocks**: `AAPL`, `GOOGL`, `MSFT`
- **Indices**: `NIFTY`, `SENSEX`

## 🔧 Technical Features

### 📊 Chart Analysis
- **Price Charts**: Candlestick with volume
- **Technical Indicators**: 
  - RSI (Relative Strength Index)
  - MACD (Moving Average Convergence Divergence)
  - Bollinger Bands
  - Simple Moving Averages
- **Buy/Sell Signals**: Algorithmic signal generation
- **Volume Analysis**: Trading volume visualization

### 🤖 AI Analysis Engine
- **Market Sentiment Analysis**: Expert opinion aggregation
- **Technical Analysis**: Pattern recognition and trend analysis
- **Fundamental Analysis**: Financial metrics evaluation
- **Risk Assessment**: Volatility and risk factor identification

### 📰 News Intelligence
- **Real-time Updates**: Latest market news and events
- **Source Diversity**: Multiple financial news sources
- **Relevance Filtering**: Company-specific news filtering
- **Clickable Links**: Direct access to full articles

## 🛡️ Important Disclaimers

- **No Investment Advice**: This tool provides analysis only, not investment recommendations
- **Educational Purpose**: Designed for learning and research
- **Professional Consultation**: Always consult licensed financial advisors for investment decisions
- **Data Accuracy**: Market data is provided as-is; verify important information

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/AmazingFeature`)
3. **Commit your changes** (`git commit -m 'Add AmazingFeature'`)
4. **Push to the branch** (`git push origin feature/AmazingFeature`)
5. **Open a Pull Request**

### 🎯 Areas for Contribution
- Additional technical indicators
- More news sources integration
- Enhanced AI analysis models
- Mobile app development
- Portfolio analysis features

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support & Issues

- **🐛 Bug Reports**: [Create an issue](https://github.com/yourusername/stock-market-bot/issues)
- **💡 Feature Requests**: [Submit a suggestion](https://github.com/yourusername/stock-market-bot/issues)
- **❓ Questions**: [Start a discussion](https://github.com/yourusername/stock-market-bot/discussions)

## 📈 Roadmap

### 🔮 Upcoming Features
- [ ] **Portfolio Analysis**: Multi-stock portfolio tracking
- [ ] **Sector Comparison**: Industry-wise performance analysis
- [ ] **Historical Backtesting**: Strategy performance testing
- [ ] **Alert System**: Price and news alerts
- [ ] **Mobile App**: React Native mobile application
- [ ] **API Endpoints**: REST API for developers

### 🎯 Current Focus
- [x] Real-time data integration
- [x] AI-powered analysis
- [x] Multi-source news aggregation
- [x] Professional UI/UX design
- [x] Technical indicator calculations

## 🏆 Acknowledgments

- **📊 Data Providers**: Yahoo Finance, Finnhub, NewsAPI, Alpha Vantage
- **🤖 AI Engine**: GROQ API for intelligent analysis
- **📱 Framework**: Streamlit for rapid web app development
- **📈 Visualization**: Matplotlib, Seaborn, Plotly for charts
- **🔧 Libraries**: yfinance, pandas, numpy for data processing

## 📞 Contact

**Developer**: [Your Name]
- 📧 Email: your.email@example.com
- 🐦 Twitter: [@yourusername](https://twitter.com/yourusername)
- 💼 LinkedIn: [Your LinkedIn](https://linkedin.com/in/yourusername)

---

### 🌟 Star this repository if you find it useful!

**Made with ❤️ for the trading community**
