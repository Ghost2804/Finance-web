"""
Stock Service for fetching and analyzing stock market data.
"""
import logging
from typing import Dict
import yfinance as yf

logger = logging.getLogger(__name__)

class StockService:
    """Service class for handling stock-related operations."""
    
    @staticmethod
    def get_stock_data() -> Dict[str, Dict]:
        """
        Fetch stock data for predefined US and Indian stocks.
        
        Returns:
            Dict containing stock data with ticker symbols as keys.
        """
        # US Stocks (Predefined)
        us_stocks = ["AAPL", "TSLA", "MSFT", "GOOGL", "NVDA", "AMZN"]
        
        # Top 100 Indian Stocks (NSE)
        indian_stocks = [
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

        # Combine US & Indian stocks
        stocks = us_stocks + indian_stocks
        stock_data = {}

        for stock in stocks:
            try:
                ticker = yf.Ticker(stock)
                history = ticker.history(period="5d")  # Fetch last 5 days of data

                if history.empty:
                    continue  # Skip if no data found

                latest_close = history["Close"].iloc[-1]
                previous_close = history["Close"].iloc[-2]

                stock_data[stock] = {
                    "name": ticker.info.get("shortName", stock),
                    "price": round(latest_close, 2),
                    "change": round(latest_close - previous_close, 2),
                    "change_percent": round(((latest_close - previous_close) / previous_close) * 100, 2)
                }
            except Exception as e:
                logger.error(f"Error fetching data for {stock}: {e}")

        return stock_data 