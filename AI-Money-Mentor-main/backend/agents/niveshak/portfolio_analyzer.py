"""
Portfolio Analyzer for MF Portfolio
Calculates XIRR, CAGR, and risk metrics
"""

import math
from typing import List, Dict, Optional
from datetime import datetime


class PortfolioAnalyzer:
    """Analyze mutual fund portfolio"""
    
    def __init__(self):
        self.risk_free_rate = 0.06  # 6% risk-free rate
    
    def calculate_xirr(self, transactions: List[Dict]) -> float:
        """
        Calculate XIRR (Extended Internal Rate of Return)
        
        Args:
            transactions: List of {'date': 'YYYY-MM-DD', 'amount': float, 'units': float}
                          Negative amounts for investments, positive for redemptions
        
        Returns:
            XIRR as percentage
        """
        if not transactions or len(transactions) < 2:
            return 0.0
        
        # Convert dates to days from first transaction
        first_date = datetime.strptime(transactions[0]['date'], '%Y-%m-%d')
        amounts = []
        days = []
        
        for t in transactions:
            date = datetime.strptime(t['date'], '%Y-%m-%d')
            day = (date - first_date).days
            amount = t.get('amount', 0)
            amounts.append(amount)
            days.append(day)
        
        # Newton-Raphson method for XIRR
        rate = 0.1  # Initial guess 10%
        
        for _ in range(100):
            npv = sum(a / ((1 + rate) ** (d / 365)) for a, d in zip(amounts, days))
            
            if abs(npv) < 0.01:
                break
            
            # Derivative of NPV
            dnpv = sum(-a * d / 365 / ((1 + rate) ** ((d / 365) + 1)) for a, d in zip(amounts, days) if d > 0)
            
            if dnpv != 0:
                rate = rate - npv / dnpv
            
            rate = max(-0.99, min(rate, 10))  # Bounds
        
        return rate * 100  # Return as percentage
    
    def calculate_cagr(self, start_value: float, end_value: float, years: float) -> float:
        """
        Calculate CAGR (Compound Annual Growth Rate)
        
        Args:
            start_value: Initial investment
            end_value: Final value
            years: Investment period in years
        
        Returns:
            CAGR as percentage
        """
        if start_value <= 0 or end_value <= 0 or years <= 0:
            return 0.0
        
        cagr = (end_value / start_value) ** (1 / years) - 1
        return cagr * 100
    
    def calculate_sharpe_ratio(self, nav_data: List[float], risk_free_rate: float = 0.06) -> float:
        """
        Calculate Sharpe Ratio
        
        Args:
            nav_data: List of NAV values
            risk_free_rate: Annual risk-free rate (default 6%)
        
        Returns:
            Sharpe ratio
        """
        if len(nav_data) < 2:
            return 0.0
        
        # Calculate returns
        returns = [(nav_data[i] - nav_data[i-1]) / nav_data[i-1] for i in range(1, len(nav_data))]
        
        if not returns:
            return 0.0
        
        # Mean return
        mean_return = sum(returns) / len(returns)
        
        # Standard deviation
        variance = sum((r - mean_return) ** 2 for r in returns) / len(returns)
        std_dev = variance ** 0.5
        
        if std_dev == 0:
            return 0.0
        
        # Annualized Sharpe ratio
        annual_mean = mean_return * 252  # Trading days
        annual_std = std_dev * (252 ** 0.5)
        
        sharpe = (annual_mean - risk_free_rate) / annual_std
        return round(sharpe, 2)
    
    def calculate_sortino_ratio(self, nav_data: List[float], risk_free_rate: float = 0.06) -> float:
        """
        Calculate Sortino Ratio (downside deviation only)
        
        Args:
            nav_data: List of NAV values
            risk_free_rate: Annual risk-free rate
        
        Returns:
            Sortino ratio
        """
        if len(nav_data) < 2:
            return 0.0
        
        # Calculate returns
        returns = [(nav_data[i] - nav_data[i-1]) / nav_data[i-1] for i in range(1, len(nav_data))]
        
        if not returns:
            return 0.0
        
        mean_return = sum(returns) / len(returns)
        
        # Downside deviation (negative returns only)
        negative_returns = [r for r in returns if r < 0]
        
        if not negative_returns:
            return float('inf')  # Perfect - no downside
        
        downside_variance = sum((r ** 2) for r in negative_returns) / len(returns)
        downside_std = downside_variance ** 0.5
        
        if downside_std == 0:
            return 0.0
        
        # Annualized
        annual_mean = mean_return * 252
        annual_downside_std = downside_std * (252 ** 0.5)
        
        sortino = (annual_mean - risk_free_rate) / annual_downside_std
        return round(sortino, 2)
    
    def get_risk_metrics(self, nav_data: List[float]) -> Dict:
        """Get all risk metrics"""
        return {
            'sharpe_ratio': self.calculate_sharpe_ratio(nav_data),
            'sortino_ratio': self.calculate_sortino_ratio(nav_data),
            'volatility': self._calculate_volatility(nav_data),
            'max_drawdown': self._calculate_max_drawdown(nav_data)
        }
    
    def _calculate_volatility(self, nav_data: List[float]) -> float:
        """Calculate annualized volatility"""
        if len(nav_data) < 2:
            return 0.0
        
        returns = [(nav_data[i] - nav_data[i-1]) / nav_data[i-1] for i in range(1, len(nav_data))]
        mean_return = sum(returns) / len(returns)
        variance = sum((r - mean_return) ** 2 for r in returns) / len(returns)
        daily_std = variance ** 0.5
        annual_std = daily_std * (252 ** 0.5)
        return round(annual_std * 100, 2)
    
    def _calculate_max_drawdown(self, nav_data: List[float]) -> float:
        """Calculate maximum drawdown"""
        if len(nav_data) < 2:
            return 0.0
        
        peak = nav_data[0]
        max_dd = 0.0
        
        for nav in nav_data:
            if nav > peak:
                peak = nav
            dd = (peak - nav) / peak
            if dd > max_dd:
                max_dd = dd
        
        return round(max_dd * 100, 2)
