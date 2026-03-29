"""
Stock Data Fetcher for Indian Markets
Uses free APIs with fallback to mock data for reliability
"""

import requests
from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta
import random
import yfinance as yf


@dataclass
class StockQuote:
    """Stock quote data"""
    symbol: str
    name: str
    price: float
    change: float
    change_percent: float
    open: float
    high: float
    low: float
    volume: int
    pe_ratio: Optional[float] = None
    market_cap: Optional[float] = None
    fifty_two_week_high: Optional[float] = None
    fifty_two_week_low: Optional[float] = None
    
    def to_dict(self):
        return {
            'symbol': self.symbol,
            'name': self.name,
            'price': self.price,
            'change': self.change,
            'change_percent': self.change_percent,
            'open': self.open,
            'high': self.high,
            'low': self.low,
            'volume': self.volume,
            'pe_ratio': self.pe_ratio,
            'market_cap': self.market_cap,
            'fifty_two_week_high': self.fifty_two_week_high,
            'fifty_two_week_low': self.fifty_two_week_low
        }


# Mock data for popular stocks (fallback when API unavailable)
MOCK_STOCKS = {
    'RELIANCE': {'name': 'Reliance Industries Ltd', 'base_price': 2456, 'pe': 28.5},
    'TCS': {'name': 'Tata Consultancy Services Ltd', 'base_price': 3845, 'pe': 32.1},
    'INFY': {'name': 'Infosys Ltd', 'base_price': 1456, 'pe': 25.8},
    'HDFCBANK': {'name': 'HDFC Bank Ltd', 'base_price': 1623, 'pe': 19.2},
    'ICICIBANK': {'name': 'ICICI Bank Ltd', 'base_price': 1087, 'pe': 16.5},
    'HINDUNILVR': {'name': 'Hindustan Unilever Ltd', 'base_price': 2456, 'pe': 55.2},
    'BHARTIARTL': {'name': 'Bharti Airtel Ltd', 'base_price': 1234, 'pe': 48.3},
    'ITC': {'name': 'ITC Ltd', 'base_price': 423, 'pe': 22.1},
    'KOTAKBANK': {'name': 'Kotak Mahindra Bank Ltd', 'base_price': 1678, 'pe': 21.8},
    'LT': {'name': 'Larsen & Toubro Ltd', 'base_price': 3456, 'pe': 26.4},
    'SBIN': {'name': 'State Bank of India', 'base_price': 756, 'pe': 12.3},
    'BAJFINANCE': {'name': 'Bajaj Finance Ltd', 'base_price': 7234, 'pe': 35.2},
    'MARUTI': {'name': 'Maruti Suzuki India Ltd', 'base_price': 10234, 'pe': 28.9},
    'ASIANPAINT': {'name': 'Asian Paints Ltd', 'base_price': 2987, 'pe': 62.5},
    'SUNPHARMA': {'name': 'Sun Pharmaceutical Industries Ltd', 'base_price': 1567, 'pe': 32.1},
    'TITAN': {'name': 'Titan Company Ltd', 'base_price': 3234, 'pe': 78.5},
    'DMART': {'name': 'Avenue Supermarts Ltd', 'base_price': 3876, 'pe': 95.2},
    'WIPRO': {'name': 'Wipro Ltd', 'base_price': 456, 'pe': 21.3},
    'HCLTECH': {'name': 'HCL Technologies Ltd', 'base_price': 1345, 'pe': 23.7},
    'TECHM': {'name': 'Tech Mahindra Ltd', 'base_price': 1234, 'pe': 18.9},
}


def get_mock_quote(symbol: str) -> Optional[StockQuote]:
    """Generate mock quote with realistic variation"""
    symbol = symbol.upper()
    
    if symbol not in MOCK_STOCKS:
        # Try to find partial match
        for key in MOCK_STOCKS:
            if key in symbol or symbol in key:
                symbol = key
                break
        else:
            return None
    
    stock = MOCK_STOCKS[symbol]
    base_price = stock['base_price']
    
    # Add random variation (-3% to +3%)
    change_pct = random.uniform(-3, 3)
    price = base_price * (1 + change_pct / 100)
    change = price - base_price
    
    # Generate day range
    high = price * (1 + random.uniform(0.5, 2) / 100)
    low = price * (1 - random.uniform(0.5, 2) / 100)
    
    # 52-week range
    week_high = base_price * 1.15  # 15% above base
    week_low = base_price * 0.85   # 15% below base
    
    return StockQuote(
        symbol=symbol,
        name=stock['name'],
        price=round(price, 2),
        change=round(change, 2),
        change_percent=round(change_pct, 2),
        open=round(base_price * (1 + random.uniform(-1, 1) / 100), 2),
        high=round(high, 2),
        low=round(low, 2),
        volume=random.randint(500000, 5000000),
        pe_ratio=stock['pe'],
        market_cap=base_price * random.randint(500000000, 2000000000),
        fifty_two_week_high=round(week_high, 2),
        fifty_two_week_low=round(week_low, 2)
    )


class StockData:
    """Main class for stock data operations"""
    
    NIFTY_50 = [
        'RELIANCE', 'TCS', 'HDFCBANK', 'INFY', 'HINDUNILVR',
        'ICICIBANK', 'HDFC', 'KOTAKBANK', 'BHARTIARTL', 'ITC',
        'SBIN', 'BAJFINANCE', 'MARUTI', 'AXISBANK', 'LT',
        'DMART', 'ASIANPAINT', 'SUNPHARMA', 'TITAN', 'BAJAJFINSV'
    ]
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json',
        })
        self.use_mock = False
    
    def get_quote(self, symbol: str) -> Optional[StockQuote]:
        """
        Get stock quote - tries yfinance first, falls back to mock data
        """
        original_symbol = symbol.upper().strip()
        
        # Determine yfinance symbol (add .NS for Indian stocks if not present)
        yf_symbol = original_symbol
        if not yf_symbol.endswith('.NS') and not yf_symbol.endswith('.BO'):
            yf_symbol = f"{yf_symbol}.NS"
            
        try:
            ticker = yf.Ticker(yf_symbol)
            info = ticker.info
            
            # Extract current price safely
            price = info.get('currentPrice') or info.get('regularMarketPrice') or info.get('previousClose', 0)
            if price:
                prev_close = info.get('previousClose', price)
                change = price - prev_close
                change_percent = (change / prev_close * 100) if prev_close else 0
                
                # Yahoo Finance uses pure numeric Market Cap directly (e.g. 2894906754672).
                # Convert explicitly to Crores (Cr) so it fits beautifully into the UI without looking bizarrely huge.
                market_cap_raw = info.get('marketCap')
                market_cap_cr = round(market_cap_raw / 10**7, 2) if market_cap_raw else None
                
                return StockQuote(
                    symbol=original_symbol,
                    name=info.get('longName', original_symbol),
                    price=round(float(price), 2),
                    change=round(float(change), 2),
                    change_percent=round(float(change_percent), 2),
                    open=round(float(info.get('open', price)), 2),
                    high=round(float(info.get('dayHigh', price)), 2),
                    low=round(float(info.get('dayLow', price)), 2),
                    volume=int(info.get('volume', 0)),
                    pe_ratio=round(float(info.get('trailingPE')), 2) if info.get('trailingPE') else None,
                    market_cap=market_cap_cr,
                    fifty_two_week_high=round(float(info.get('fiftyTwoWeekHigh', 0)), 2),
                    fifty_two_week_low=round(float(info.get('fiftyTwoWeekLow', 0)), 2)
                )
        except Exception:
            pass
            
        # Fallback to mock data ONLY if yfinance fails
        return get_mock_quote(original_symbol)
    
    def get_market_overview(self) -> Dict:
        """Get market overview (NIFTY, SENSEX)"""
        # Mock market data
        return {
            'nifty': {
                'value': 22456.80,
                'change': 267.45,
                'change_percent': 1.2
            },
            'sensex': {
                'value': 73876.54,
                'change': 589.23,
                'change_percent': 0.8
            },
            'usd_inr': {
                'value': 83.25,
                'change': -0.15,
                'change_percent': -0.18
            },
            'gold': {
                'value': 72500,
                'change': 350,
                'change_percent': 0.48
            }
        }
    
    def get_top_gainers(self, limit: int = 5) -> List[StockQuote]:
        """Get top gaining stocks (mock)"""
        gainers = []
        symbols = random.sample(list(MOCK_STOCKS.keys()), min(10, len(MOCK_STOCKS)))
        
        for symbol in symbols:
            quote = get_mock_quote(symbol)
            if quote and quote.change_percent > 0:
                gainers.append(quote)
        
        return sorted(gainers, key=lambda x: x.change_percent, reverse=True)[:limit]
    
    def get_top_losers(self, limit: int = 5) -> List[StockQuote]:
        """Get top losing stocks (mock)"""
        losers = []
        symbols = random.sample(list(MOCK_STOCKS.keys()), min(10, len(MOCK_STOCKS)))
        
        for symbol in symbols:
            quote = get_mock_quote(symbol)
            if quote and quote.change_percent < 0:
                losers.append(quote)
        
        return sorted(losers, key=lambda x: x.change_percent)[:limit]
    
    def search_stocks(self, query: str) -> List[Dict]:
        """Search for stocks by name or symbol"""
        query = query.upper()
        results = []
        
        for symbol, data in MOCK_STOCKS.items():
            if query in symbol or query in data['name'].upper():
                quote = get_mock_quote(symbol)
                if quote:
                    results.append(quote.to_dict())
        
        return results


# Convenience function
def get_stock_quote(symbol: str) -> Optional[StockQuote]:
    """Quick function to get stock quote"""
    stock = StockData()
    return stock.get_quote(symbol)
