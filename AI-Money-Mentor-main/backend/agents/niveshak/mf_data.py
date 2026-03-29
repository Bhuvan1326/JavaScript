"""
Mutual Fund Data Fetcher
Fetches NAV data and scheme info from mfapi.in and mftool
"""

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import requests
import pandas as pd
from mftool import Mftool
import json


@dataclass
class NAVData:
    """NAV data point"""
    scheme_name: str
    scheme_code: str
    date: datetime
    nav: float
    
@dataclass
class SchemeInfo:
    """Mutual Fund scheme information"""
    scheme_code: str
    scheme_name: str
    amc: str
    isin: str
    scheme_type: str  # EQUITY, DEBT, HYBRID, etc.
    category: str
    sub_category: str
    launch_date: Optional[datetime] = None


class MFDataFetcher:
    """
    Fetches mutual fund data from multiple sources:
    - mfapi.in (primary, free REST API)
    - mftool (fallback, scrapes AMFI)
    """
    
    MFAPI_BASE = "https://api.mfapi.in/mf"
    
    # Cache for scheme master list
    _scheme_master: Optional[List[Dict]] = None
    _scheme_master_time: Optional[datetime] = None
    _cache_duration = timedelta(hours=6)
    
    def __init__(self):
        self.mftool = Mftool()
        self.last_error: Optional[str] = None
        
    def get_all_schemes(self, force_refresh: bool = False) -> List[Dict]:
        """
        Get list of all mutual fund schemes in India
        
        Returns:
            List of dicts with scheme_code, scheme_name
        """
        # Check cache
        if not force_refresh and self._scheme_master is not None:
            if self._scheme_master_time:
                if datetime.now() - self._scheme_master_time < self._cache_duration:
                    return self._scheme_master
                    
        try:
            # Try mftool first
            schemes = self.mftool.get_scheme_codes()
            if schemes and len(schemes) > 1000:  # Sanity check
                self._scheme_master = schemes
                self._scheme_master_time = datetime.now()
                return schemes
        except Exception as e:
            self.last_error = f"Mftool error: {str(e)}"
            
        return []
    
    def search_schemes(self, query: str, limit: int = 10) -> List[Dict]:
        """
        Search for schemes by name
        
        Args:
            query: Search query (scheme name or part)
            limit: Maximum results to return
            
        Returns:
            List of matching schemes
        """
        all_schemes = self.get_all_schemes()
        if not all_schemes:
            return []
            
        query_lower = query.lower()
        matches = []
        
        for scheme in all_schemes:
            name = scheme.get('schemeName', '').lower()
            if query_lower in name:
                matches.append({
                    'scheme_code': scheme.get('schemeCode'),
                    'scheme_name': scheme.get('schemeName')
                })
                if len(matches) >= limit:
                    break
                    
        return matches
        
    def get_current_nav(self, scheme_code: str) -> Optional[float]:
        """
        Get current NAV for a scheme
        
        Args:
            scheme_code: AMFI scheme code
            
        Returns:
            Current NAV as float, or None on error
        """
        try:
            # Try mfapi.in first
            url = f"{self.MFAPI_BASE}/{scheme_code}"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if 'data' in data and len(data['data']) > 0:
                    # Get most recent NAV
                    nav_str = data['data'][0].get('nav', '0')
                    return float(nav_str)
        except Exception as e:
            self.last_error = f"API error: {str(e)}"
            
        # Fallback to mftool
        try:
            nav = self.mftool.get_scheme_quote(scheme_code)
            if nav and 'current_nav' in nav:
                return float(nav['current_nav'])
        except Exception as e:
            self.last_error = f"Mftool error: {str(e)}"
            
        return None
        
    def get_historical_nav(
        self, 
        scheme_code: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        force_mftool: bool = False
    ) -> List[NAVData]:
        """
        Get historical NAV data for a scheme
        
        Args:
            scheme_code: AMFI scheme code
            start_date: Start date (default: 1 year ago)
            end_date: End date (default: today)
            force_mftool: Force using mftool instead of mfapi
            
        Returns:
            List of NAVData objects
        """
        if start_date is None:
            start_date = datetime.now() - timedelta(days=365)
        if end_date is None:
            end_date = datetime.now()
            
        historical_navs = []
        
        if not force_mftool:
            # Try mfapi.in
            try:
                url = f"{self.MFAPI_BASE}/{scheme_code}"
                response = requests.get(url, timeout=15)
                
                if response.status_code == 200:
                    data = response.json()
                    scheme_name = data.get('meta', {}).get('scheme_name', '')
                    
                    for nav_entry in data.get('data', []):
                        try:
                            date_str = nav_entry.get('date', '')
                            nav_str = nav_entry.get('nav', '0')
                            
                            # Parse date (format: DD-MM-YYYY)
                            nav_date = datetime.strptime(date_str, '%d-%m-%Y')
                            nav = float(nav_str)
                            
                            # Filter by date range
                            if start_date <= nav_date <= end_date:
                                historical_navs.append(NAVData(
                                    scheme_name=scheme_name,
                                    scheme_code=scheme_code,
                                    date=nav_date,
                                    nav=nav
                                ))
                        except (ValueError, KeyError):
                            continue
                            
            except Exception as e:
                self.last_error = f"MFAPI error: {str(e)}"
                
        # If no data from mfapi, try mftool
        if not historical_navs:
            try:
                df = self.mftool.get_scheme_historical_nav(
                    scheme_code,
                    self._format_date(start_date),
                    self._format_date(end_date)
                )
                
                if df is not None and not df.empty:
                    scheme_name = self._get_scheme_name(scheme_code)
                    
                    for _, row in df.iterrows():
                        try:
                            nav_date = row.get('date')
                            nav = float(row.get('nav', 0))
                            
                            historical_navs.append(NAVData(
                                scheme_name=scheme_name,
                                scheme_code=scheme_code,
                                date=nav_date,
                                nav=nav
                            ))
                        except (ValueError, KeyError):
                            continue
                            
            except Exception as e:
                self.last_error = f"Mftool error: {str(e)}"
                
        return sorted(historical_navs, key=lambda x: x.date)
        
    def get_scheme_info(self, scheme_code: str) -> Optional[SchemeInfo]:
        """
        Get detailed scheme information
        
        Args:
            scheme_code: AMFI scheme code
            
        Returns:
            SchemeInfo object or None
        """
        try:
            url = f"{self.MFAPI_BASE}/{scheme_code}"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                meta = data.get('meta', {})
                
                return SchemeInfo(
                    scheme_code=scheme_code,
                    scheme_name=meta.get('scheme_name', ''),
                    amc=meta.get('fund_house', ''),
                    isin=meta.get('isin', ''),
                    scheme_type=self._categorize_scheme(meta.get('scheme_name', '')),
                    category=self._get_category(meta.get('scheme_name', '')),
                    sub_category=''
                )
        except Exception as e:
            self.last_error = f"Error fetching scheme info: {str(e)}"
            
        return None
        
    def get_nav_dataframe(
        self, 
        scheme_code: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> pd.DataFrame:
        """
        Get historical NAV as pandas DataFrame
        
        Args:
            scheme_code: AMFI scheme code
            start_date: Start date
            end_date: End date
            
        Returns:
            DataFrame with columns: date, nav
        """
        navs = self.get_historical_nav(scheme_code, start_date, end_date)
        
        if not navs:
            return pd.DataFrame()
            
        df = pd.DataFrame([
            {'date': n.date, 'nav': n.nav}
            for n in navs
        ])
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date')
        return df
        
    def _format_date(self, dt: datetime) -> str:
        """Format date for mftool"""
        return dt.strftime('%d-%m-%Y')
        
    def _categorize_scheme(self, name: str) -> str:
        """Categorize scheme by type"""
        name_lower = name.lower()
        
        if any(x in name_lower for x in ['equity', 'smallcap', 'midcap', 'largecap', 'flexi', 'bluechip']):
            return 'EQUITY'
        elif any(x in name_lower for x in ['debt', 'bond', 'income', 'liquid', 'money']):
            return 'DEBT'
        elif any(x in name_lower for x in ['hybrid', 'balanced', 'aggressive']):
            return 'HYBRID'
        elif any(x in name_lower for x in ['index', 'nifty', 'sensex']):
            return 'INDEX'
        else:
            return 'OTHER'
            
    def _get_category(self, name: str) -> str:
        """Get scheme category"""
        name_lower = name.lower()
        
        if 'largecap' in name_lower or 'bluechip' in name_lower:
            return 'Large Cap'
        elif 'midcap' in name_lower:
            return 'Mid Cap'
        elif 'smallcap' in name_lower:
            return 'Small Cap'
        elif 'flexi' in name_lower:
            return 'Flexi Cap'
        elif 'index' in name_lower or 'nifty' in name_lower:
            return 'Index Fund'
        elif 'liquid' in name_lower:
            return 'Liquid Fund'
        elif 'technology' in name_lower or 'it' in name_lower:
            return 'Sectoral - Technology'
        else:
            return 'Other'
            
    def _get_scheme_name(self, scheme_code: str) -> str:
        """Get scheme name from code"""
        info = self.get_scheme_info(scheme_code)
        return info.scheme_name if info else ''


# Sample scheme codes for testing (Indian MFs)
SAMPLE_SCHEMES = {
    'axis_bluechip': '119551',  # Axis Bluechip Fund
    'parag_parikh_flexi': '122639',  # Parag Parikh Flexi Cap Fund
    'mirae_largecap': '118989',  # Mirae Asset Large Cap Fund
    'icici_tech': '120505',  # ICICI Prudential Technology Fund
    'hdfc_nifty50': '118960',  # HDFC Index Fund Nifty 50
}


def get_sample_nav_data() -> Dict[str, List[NAVData]]:
    """
    Generate sample NAV data for testing without API calls
    
    Returns:
        Dict mapping scheme names to list of NAVData
    """
    import random
    
    base_date = datetime.now() - timedelta(days=730)
    sample_data = {}
    
    for name, code in SAMPLE_SCHEMES.items():
        navs = []
        current_nav = random.uniform(50, 200)
        
        for i in range(730):  # 2 years
            date = base_date + timedelta(days=i)
            # Random walk NAV
            change = random.gauss(0.001, 0.02)
            current_nav = current_nav * (1 + change)
            
            navs.append(NAVData(
                scheme_name=name.replace('_', ' ').title(),
                scheme_code=code,
                date=date,
                nav=current_nav
            ))
            
        sample_data[name] = navs
        
    return sample_data


if __name__ == "__main__":
    # Demo usage
    fetcher = MFDataFetcher()
    
    print("=== Testing MF Data Fetcher ===")
    print()
    
    # Search for schemes
    print("Searching for 'Axis Bluechip'...")
    results = fetcher.search_schemes("Axis Bluechip", limit=3)
    for r in results:
        print(f"  {r['scheme_code']}: {r['scheme_name']}")
    print()
    
    # Generate sample data for testing
    print("Generating sample NAV data...")
    sample = get_sample_nav_data()
    for scheme, navs in sample.items():
        print(f"  {scheme}: {len(navs)} NAV points, latest: ₹{navs[-1].nav:.2f}")
