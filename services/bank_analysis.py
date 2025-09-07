"""
Bank Health Analysis Service
Analyzes bank performance, financial health, and provides early warning indicators.
"""
import logging
import yfinance as yf
import pandas as pd
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
import numpy as np

logger = logging.getLogger(__name__)

class BankHealthAnalyzer:
    """Service for analyzing bank financial health and performance."""
    
    # Major Indian Banks with their stock symbols
    INDIAN_BANKS = {
        "HDFC Bank": "HDFCBANK.NS",
        "ICICI Bank": "ICICIBANK.NS", 
        "State Bank of India": "SBIN.NS",
        "Kotak Mahindra Bank": "KOTAKBANK.NS",
        "Axis Bank": "AXISBANK.NS",
        "Bank of Baroda": "BANKBARODA.NS",
        "Punjab National Bank": "PNB.NS",
        "Canara Bank": "CANBK.NS",
        "Union Bank": "UNIONBANK.NS",
        "IDBI Bank": "IDBI.NS"
    }
    
    # Key Financial Ratios for Bank Health Assessment
    HEALTH_INDICATORS = {
        "capital_adequacy": "Capital Adequacy Ratio (CAR)",
        "npl_ratio": "Non-Performing Loan (NPL) Ratio", 
        "liquidity_ratio": "Liquidity Coverage Ratio (LCR)",
        "net_interest_margin": "Net Interest Margin (NIM)",
        "return_on_assets": "Return on Assets (ROA)",
        "return_on_equity": "Return on Equity (ROE)",
        "cost_to_income": "Cost to Income Ratio",
        "provision_coverage": "Provision Coverage Ratio"
    }
    
    def __init__(self):
        self.bank_data = {}
        self.health_scores = {}
    
    def get_bank_stock_data(self, bank_name: str) -> Dict:
        """
        Fetch stock data for a specific bank.
        
        Args:
            bank_name: Name of the bank
            
        Returns:
            Dictionary containing stock performance data
        """
        try:
            symbol = self.INDIAN_BANKS.get(bank_name)
            if not symbol:
                return {"error": f"Bank {bank_name} not found in database"}
            
            ticker = yf.Ticker(symbol)
            
            # Get historical data for analysis
            hist_data = ticker.history(period="1y")
            info = ticker.info
            
            if hist_data.empty:
                return {"error": f"No data available for {bank_name}"}
            
            # Calculate key metrics
            current_price = hist_data['Close'].iloc[-1]
            price_change = hist_data['Close'].iloc[-1] - hist_data['Close'].iloc[-2]
            price_change_pct = (price_change / hist_data['Close'].iloc[-2]) * 100
            
            # Calculate volatility (standard deviation of returns)
            returns = hist_data['Close'].pct_change().dropna()
            volatility = returns.std() * np.sqrt(252) * 100  # Annualized volatility
            
            # Calculate moving averages
            ma_20 = hist_data['Close'].rolling(window=20).mean().iloc[-1]
            ma_50 = hist_data['Close'].rolling(window=50).mean().iloc[-1]
            
            return {
                "bank_name": bank_name,
                "symbol": symbol,
                "current_price": round(current_price, 2),
                "price_change": round(price_change, 2),
                "price_change_pct": round(price_change_pct, 2),
                "volatility": round(volatility, 2),
                "ma_20": round(ma_20, 2),
                "ma_50": round(ma_50, 2),
                "market_cap": str(info.get('marketCap', 'N/A')),
                "volume": int(hist_data['Volume'].iloc[-1]),
                "avg_volume": int(hist_data['Volume'].rolling(window=20).mean().iloc[-1]),
                "high_52w": float(hist_data['High'].max()),
                "low_52w": float(hist_data['Low'].min()),
                "pe_ratio": float(info.get('trailingPE', 0)) if info.get('trailingPE') else 'N/A',
                "pb_ratio": float(info.get('priceToBook', 0)) if info.get('priceToBook') else 'N/A',
                "dividend_yield": float(info.get('dividendYield', 0) * 100) if info.get('dividendYield') else 0
            }
            
        except Exception as e:
            logger.error(f"Error fetching data for {bank_name}: {e}")
            return {"error": f"Failed to fetch data for {bank_name}"}
    
    def calculate_bank_health_score(self, bank_data: Dict) -> Dict:
        """
        Calculate a comprehensive health score for a bank based on multiple factors.
        
        Args:
            bank_data: Bank performance data
            
        Returns:
            Dictionary containing health score and analysis
        """
        if "error" in bank_data:
            return {"error": bank_data["error"]}
        
        score = 0
        max_score = 100
        analysis = []
        
        # Price Performance (20 points)
        if bank_data["price_change_pct"] > 0:
            score += min(20, abs(bank_data["price_change_pct"]) * 2)
            analysis.append(f"✅ Positive price performance: {bank_data['price_change_pct']:.2f}%")
        else:
            analysis.append(f"⚠️ Negative price performance: {bank_data['price_change_pct']:.2f}%")
        
        # Volatility Assessment (15 points)
        if bank_data["volatility"] < 20:
            score += 15
            analysis.append(f"✅ Low volatility: {bank_data['volatility']:.2f}%")
        elif bank_data["volatility"] < 30:
            score += 10
            analysis.append(f"⚠️ Moderate volatility: {bank_data['volatility']:.2f}%")
        else:
            analysis.append(f"❌ High volatility: {bank_data['volatility']:.2f}%")
        
        # Moving Average Analysis (15 points)
        if bank_data["current_price"] > bank_data["ma_20"] > bank_data["ma_50"]:
            score += 15
            analysis.append("✅ Strong uptrend: Price above both moving averages")
        elif bank_data["current_price"] > bank_data["ma_20"]:
            score += 10
            analysis.append("⚠️ Moderate trend: Price above 20-day MA")
        else:
            analysis.append("❌ Downtrend: Price below moving averages")
        
        # Valuation Metrics (20 points)
        pe_score = 0
        if isinstance(bank_data["pe_ratio"], (int, float)):
            if 10 <= bank_data["pe_ratio"] <= 20:
                pe_score = 10
                analysis.append(f"✅ Reasonable P/E ratio: {bank_data['pe_ratio']:.2f}")
            elif bank_data["pe_ratio"] < 10:
                pe_score = 15
                analysis.append(f"✅ Undervalued P/E ratio: {bank_data['pe_ratio']:.2f}")
            else:
                analysis.append(f"⚠️ High P/E ratio: {bank_data['pe_ratio']:.2f}")
        
        pb_score = 0
        if isinstance(bank_data["pb_ratio"], (int, float)):
            if bank_data["pb_ratio"] <= 2:
                pb_score = 10
                analysis.append(f"✅ Good P/B ratio: {bank_data['pb_ratio']:.2f}")
            else:
                analysis.append(f"⚠️ High P/B ratio: {bank_data['pb_ratio']:.2f}")
        
        score += pe_score + pb_score
        
        # Dividend Analysis (10 points)
        if bank_data["dividend_yield"] > 3:
            score += 10
            analysis.append(f"✅ High dividend yield: {bank_data['dividend_yield']:.2f}%")
        elif bank_data["dividend_yield"] > 1:
            score += 5
            analysis.append(f"⚠️ Moderate dividend yield: {bank_data['dividend_yield']:.2f}%")
        else:
            analysis.append(f"❌ Low dividend yield: {bank_data['dividend_yield']:.2f}%")
        
        # Volume Analysis (10 points)
        current_volume = bank_data["volume"]
        avg_volume = bank_data["avg_volume"]
        if current_volume > avg_volume * 1.5:
            score += 10
            analysis.append("✅ High trading volume indicates strong interest")
        elif current_volume > avg_volume:
            score += 5
            analysis.append("⚠️ Above average trading volume")
        else:
            analysis.append("❌ Below average trading volume")
        
        # Market Position (10 points)
        if isinstance(bank_data["market_cap"], (int, float)) and bank_data["market_cap"] > 100000000000:  # 100B
            score += 10
            analysis.append("✅ Large-cap bank with strong market position")
        elif isinstance(bank_data["market_cap"], (int, float)) and bank_data["market_cap"] > 10000000000:  # 10B
            score += 5
            analysis.append("⚠️ Mid-cap bank")
        else:
            analysis.append("❌ Small-cap bank")
        
        # Determine health status
        if score >= 80:
            status = "Excellent"
            status_color = "green"
        elif score >= 60:
            status = "Good"
            status_color = "blue"
        elif score >= 40:
            status = "Fair"
            status_color = "orange"
        else:
            status = "Poor"
            status_color = "red"
        
        return {
            "health_score": score,
            "max_score": max_score,
            "status": status,
            "status_color": status_color,
            "analysis": analysis,
            "recommendation": self._get_recommendation(score, bank_data)
        }
    
    def _get_recommendation(self, score: int, bank_data: Dict) -> str:
        """Generate investment recommendation based on health score."""
        if score >= 80:
            return "Strong Buy - Excellent financial health and performance"
        elif score >= 60:
            return "Buy - Good fundamentals with potential for growth"
        elif score >= 40:
            return "Hold - Monitor closely, consider reducing exposure"
        else:
            return "Sell - Poor performance, consider alternatives"
    
    def get_banking_sector_overview(self) -> Dict:
        """
        Get comprehensive overview of the Indian banking sector.
        
        Returns:
            Dictionary containing sector analysis
        """
        sector_data = {}
        total_score = 0
        bank_count = 0
        
        for bank_name in self.INDIAN_BANKS.keys():
            bank_data = self.get_bank_stock_data(bank_name)
            if "error" not in bank_data:
                health_analysis = self.calculate_bank_health_score(bank_data)
                if "error" not in health_analysis:
                    sector_data[bank_name] = {
                        "stock_data": bank_data,
                        "health_analysis": health_analysis
                    }
                    total_score += health_analysis["health_score"]
                    bank_count += 1
        
        if bank_count > 0:
            avg_sector_score = total_score / bank_count
            
            # Sector sentiment analysis
            if avg_sector_score >= 70:
                sector_sentiment = "Bullish"
                sentiment_color = "green"
            elif avg_sector_score >= 50:
                sector_sentiment = "Neutral"
                sentiment_color = "blue"
            else:
                sector_sentiment = "Bearish"
                sentiment_color = "red"
            
            return {
                "sector_overview": sector_data,
                "average_sector_score": round(avg_sector_score, 2),
                "sector_sentiment": sector_sentiment,
                "sentiment_color": sentiment_color,
                "total_banks_analyzed": bank_count,
                "analysis_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        
        return {"error": "Unable to fetch banking sector data"}
    
    def get_early_warning_indicators(self) -> Dict:
        """
        Generate early warning indicators for banking sector stress.
        
        Returns:
            Dictionary containing warning indicators
        """
        warnings = []
        
        # Get sector data
        sector_data = self.get_banking_sector_overview()
        if "error" in sector_data:
            return {"error": sector_data["error"]}
        
        # Analyze sector health
        avg_score = sector_data["average_sector_score"]
        
        if avg_score < 50:
            warnings.append({
                "level": "High",
                "indicator": "Low Sector Health Score",
                "description": f"Sector average health score is {avg_score}, indicating potential stress",
                "recommendation": "Monitor closely, consider defensive positions"
            })
        
        # Count banks with poor health
        poor_banks = 0
        for bank_name, data in sector_data["sector_overview"].items():
            if data["health_analysis"]["health_score"] < 40:
                poor_banks += 1
        
        if poor_banks > len(sector_data["sector_overview"]) * 0.3:  # More than 30% banks in poor health
            warnings.append({
                "level": "Medium",
                "indicator": "Multiple Banks Under Stress",
                "description": f"{poor_banks} out of {len(sector_data['sector_overview'])} banks show poor health",
                "recommendation": "Diversify across sectors, avoid concentrated banking exposure"
            })
        
        return {
            "warnings": warnings,
            "sector_health_score": avg_score,
            "analysis_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        } 