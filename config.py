import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuration class for the Finance application."""
    
    # Flask Configuration
    SECRET_KEY = os.getenv("SECRET_KEY", "your_default_secret_key_change_this_in_production")
    DEBUG = os.getenv("FLASK_ENV") == "development"
    
    # API Configuration
    GOOGLE_API_KEY = os.getenv("Google_API")
    
    # Stock Configuration
    US_STOCKS = ["AAPL", "TSLA", "MSFT", "GOOGL", "NVDA", "AMZN"]
    
    # Top 100 Indian Stocks (NSE)
    INDIAN_STOCKS = [
        "RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "ICICIBANK.NS", "INFY.NS", "HUL.NS",
        "KOTAKBANK.NS", "LT.NS", "SBIN.NS", "BHARTIARTL.NS", "ITC.NS", "ASIANPAINT.NS",
        "BAJFINANCE.NS", "HCLTECH.NS", "MARUTI.NS", "TITAN.NS", "ULTRACEMCO.NS", "WIPRO.NS",
        "SUNPHARMA.NS", "ONGC.NS", "ADANIPORTS.NS", "POWERGRID.NS", "NTPC.NS", "COALINDIA.NS",
        "INDUSINDBK.NS", "TATAMOTORS.NS", "JSWSTEEL.NS", "HDFCLIFE.NS", "GRASIM.NS", "BPCL.NS",
        "EICHERMOT.NS", "SBILIFE.NS", "ADANIENT.NS", "IOC.NS", "TECHM.NS", "HINDALCO.NS",
        "DRREDDY.NS", "TATACONSUM.NS", "CIPLA.NS", "VEDL.NS", "BAJAJ-AUTO.NS", "UPL.NS",
        "HEROMOTOCO.NS", "SHREECEM.NS", "BRITANNIA.NS", "DIVISLAB.NS", "GAIL.NS", "BAJAJFINSV.NS",
        "M&M.NS", "DABUR.NS", "PIDILITIND.NS", "BIOCON.NS", "MOTHERSUMI.NS", "LUPIN.NS",
        "ACC.NS", "AMBUJACEM.NS", "PETRONET.NS", "GODREJCP.NS", "MARICO.NS", "SRF.NS",
        "PNB.NS", "BANDHANBNK.NS", "BOSCHLTD.NS", "ICICIGI.NS", "COLPAL.NS", "AUROPHARMA.NS",
        "HAVELLS.NS", "UBL.NS", "BEL.NS", "TATAPOWER.NS", "EXIDEIND.NS", "BANKBARODA.NS",
        "MFSL.NS", "INDIGO.NS", "TATACHEM.NS", "SIEMENS.NS", "RECLTD.NS", "TATACOMM.NS",
        "PGHH.NS", "TORNTPHARM.NS", "PIIND.NS", "LTI.NS", "HINDPETRO.NS", "NAVINFLUOR.NS",
        "BALKRISIND.NS", "MINDTREE.NS", "MGL.NS", "GMRINFRA.NS", "MRF.NS", "GICRE.NS",
        "VOLTAS.NS", "CONCOR.NS", "BERGEPAINT.NS", "IDFCFIRSTB.NS", "SUNTV.NS", "L&TFH.NS"
    ]
    
    # Finance Keywords for chatbot filtering
    FINANCE_KEY_WORDS = [
        # Stock Market & Investing
        "stock", "stocks", "share", "shares", "stock market", "nifty", "sensex", "bse", "nse",
        "bull market", "bear market", "ipo", "intraday", "technical analysis", "fundamental analysis",
        "blue chip stocks", "mid cap", "small cap", "large cap", "index fund", "dividends", "penny stocks",
        "short selling", "call option", "put option", "derivatives", "futures", "options", "hedging",
        "portfolio management", "market cap", "candlestick patterns", "rsi", "macd", "volume trading",
        "swing trading", "long-term investing", "day trading", "mutual funds", "ETF", "REIT", "SIP",
        "high-frequency trading", "algo trading", "financial news", "investment strategies", "arbitrage",
        
        # Banking & Loans
        "bank", "banking", "savings account", "fixed deposit", "current account", "interest rate",
        "loan", "personal loan", "home loan", "mortgage", "credit score", "CIBIL score",
        "debt consolidation", "lending", "EMI", "debt", "loan eligibility", "credit card", "credit limit",
        "secured loan", "unsecured loan", "gold loan", "student loan", "auto loan", "car loan",
        
        # Personal Finance & Budgeting
        "budget", "budgeting", "monthly budget", "savings", "emergency fund", "financial goals",
        "spending habits", "expense tracking", "income", "salary", "passive income", "side hustle",
        "financial independence", "early retirement", "FIRE movement", "cash flow", "financial discipline",
        "saving money", "money management", "frugal living", "how to save", "where to invest",
        "cost-cutting", "money-saving tips", "wealth building", "financial freedom",
        
        # Investment Types & Wealth Growth
        "investment", "investing", "compounding", "ROI", "net worth", "risk management", "capital gains",
        "asset allocation", "real estate investing", "gold investment", "silver investment", 
        "cryptocurrency", "bitcoin", "ethereum", "altcoins", "stablecoins", "NFT", "blockchain",
        
        # Economy & Macroeconomics
        "inflation", "deflation", "GDP", "economic growth", "recession", "depression", "stagflation",
        "fiscal policy", "monetary policy", "central bank", "RBI", "Fed", "federal reserve",
        "repo rate", "reverse repo rate", "yield curve", "interest rates", "exchange rate",
        "forex", "currency trading", "bond market", "government bonds", "treasury bonds",
        
        # Retirement & Taxation
        "retirement planning", "401k", "pension", "NPS", "EPF", "PPF", "gratuity", "tax planning",
        "income tax", "capital gains tax", "tax benefits", "tax deductions", "GST", "TDS", "tax rebate",
        "financial advisor", "investment planner", "wealth management", "estate planning", "inheritance",
        
        # Miscellaneous
        "money", "finance", "financial literacy", "money problems", "how to invest", "financial tips",
        "financial security", "how to manage money", "best investments", "economic trends",
        "financial crisis", "insurance", "health insurance", "life insurance", "term insurance",
        "ULIP", "annuity", "policyholder", "premium", "financial fraud", "Ponzi schemes",
        "how to avoid financial scams", "digital payments", "UPI", "NEFT", "RTGS", "IMPS",
        "payment gateways", "online banking"
    ] 