"""
CAS PDF Parser for CAMS/KFintech Mutual Fund Statements
Supports parsing of Consolidated Account Statements (CAS)
"""

import io
from datetime import datetime
from typing import Dict, List, Optional, Union
from dataclasses import dataclass, field
import casparser
from casparser.exceptions import CASParseError
import pandas as pd


@dataclass
class MFTransaction:
    """Single mutual fund transaction"""
    scheme_name: str
    folio_number: str
    amc: str
    transaction_type: str  # PURCHASE, REDEMPTION, DIVIDEND, etc.
    units: float
    nav: float
    amount: float
    date: datetime
    balance_units: float = 0.0
    

@dataclass  
class MFSchemeHolding:
    """Mutual fund scheme holding details"""
    scheme_name: str
    folio_number: str
    amc: str
    isin: str = ""
    advisor: str = ""
    open_units: float = 0.0
    close_units: float = 0.0
    current_nav: float = 0.0
    current_value: float = 0.0
    transactions: List[MFTransaction] = field(default_factory=list)
    

@dataclass
class CASData:
    """Parsed CAS statement data"""
    statement_period: str
    investor_name: str
    email: str = ""
    mobile: str = ""
    pan: str = ""
    address: str = ""
    holdings: List[MFSchemeHolding] = field(default_factory=list)
    total_value: float = 0.0
    parse_date: datetime = field(default_factory=datetime.now)
    

class CASParser:
    """
    Parser for CAMS/KFintech Consolidated Account Statement (CAS) PDFs
    
    Usage:
        parser = CASParser()
        data = parser.parse("statement.pdf", password="YOUR_PASSWORD")
    """
    
    def __init__(self):
        self.last_error: Optional[str] = None
        
    def parse(
        self, 
        pdf_path: Union[str, io.IOBase], 
        password: str,
        force_pdfminer: bool = False
    ) -> Optional[CASData]:
        """
        Parse a CAS PDF file
        
        Args:
            pdf_path: Path to PDF file or file-like object
            password: PDF password (typically PAN in uppercase)
            force_pdfminer: Force using pdfminer instead of mupdf
            
        Returns:
            CASData object with parsed holdings, or None on error
        """
        try:
            # Parse using casparser
            data = casparser.read_cas_pdf(
                pdf_path,
                password=password,
                output='dict',
                force_pdfminer=force_pdfminer
            )
            
            return self._convert_to_cas_data(data)
            
        except CASParseError as e:
            self.last_error = f"CAS Parse Error: {str(e)}"
            return None
        except Exception as e:
            self.last_error = f"Error parsing PDF: {str(e)}"
            return None
            
    def _convert_to_cas_data(self, data: dict) -> CASData:
        """Convert casparser dict output to our CASData format"""
        
        # Extract investor info
        investor_info = data.get('investor_info', {})
        
        cas_data = CASData(
            statement_period=data.get('statement_period', ''),
            investor_name=investor_info.get('name', ''),
            email=investor_info.get('email', ''),
            mobile=investor_info.get('mobile', ''),
            pan=investor_info.get('pan', ''),
            address=investor_info.get('address', ''),
        )
        
        total_value = 0.0
        
        # Process each folio and scheme
        for folio in data.get('folios', []):
            folio_number = folio.get('folio', '')
            amc = folio.get('amc', '')
            advisor = folio.get('advisor', '')
            
            for scheme in folio.get('schemes', []):
                holding = self._parse_scheme(scheme, folio_number, amc, advisor)
                if holding:
                    cas_data.holdings.append(holding)
                    total_value += holding.current_value
                    
        cas_data.total_value = total_value
        return cas_data
        
    def _parse_scheme(
        self, 
        scheme: dict, 
        folio_number: str, 
        amc: str,
        advisor: str
    ) -> Optional[MFSchemeHolding]:
        """Parse individual scheme data"""
        try:
            holding = MFSchemeHolding(
                scheme_name=scheme.get('scheme', ''),
                folio_number=folio_number,
                amc=amc,
                isin=scheme.get('isin', ''),
                advisor=advisor,
                open_units=float(scheme.get('open_units', 0) or 0),
                close_units=float(scheme.get('close_units', 0) or 0),
            )
            
            # Parse transactions
            transactions = scheme.get('transactions', [])
            for txn in transactions:
                mf_txn = self._parse_transaction(txn, holding.scheme_name, folio_number, amc)
                if mf_txn:
                    holding.transactions.append(mf_txn)
                    
            # Get latest NAV and value
            nav_data = scheme.get('nav', {})
            if nav_data:
                holding.current_nav = float(nav_data.get('nav', 0) or 0)
                holding.current_value = float(nav_data.get('value', 0) or 0)
            else:
                # Calculate from closing units if NAV not provided
                holding.current_value = holding.close_units * holding.current_nav
                
            return holding
            
        except Exception as e:
            print(f"Error parsing scheme: {e}")
            return None
            
    def _parse_transaction(
        self, 
        txn: dict, 
        scheme_name: str,
        folio_number: str,
        amc: str
    ) -> Optional[MFTransaction]:
        """Parse individual transaction"""
        try:
            # Parse date
            date_str = txn.get('date', '')
            if isinstance(date_str, str):
                try:
                    date = datetime.strptime(date_str, '%d-%b-%Y')
                except:
                    date = datetime.now()
            else:
                date = date_str
                
            return MFTransaction(
                scheme_name=scheme_name,
                folio_number=folio_number,
                amc=amc,
                transaction_type=txn.get('type', '').upper(),
                units=float(txn.get('units', 0) or 0),
                nav=float(txn.get('nav', 0) or 0),
                amount=float(txn.get('amount', 0) or 0),
                date=date,
                balance_units=float(txn.get('balance', 0) or 0)
            )
        except Exception as e:
            print(f"Error parsing transaction: {e}")
            return None
            
    def get_transactions_dataframe(self, cas_data: CASData) -> pd.DataFrame:
        """Convert all transactions to a pandas DataFrame"""
        all_transactions = []
        for holding in cas_data.holdings:
            for txn in holding.transactions:
                all_transactions.append({
                    'scheme_name': txn.scheme_name,
                    'folio_number': txn.folio_number,
                    'amc': txn.amc,
                    'type': txn.transaction_type,
                    'date': txn.date,
                    'units': txn.units,
                    'nav': txn.nav,
                    'amount': txn.amount,
                    'balance': txn.balance_units
                })
                
        if not all_transactions:
            return pd.DataFrame()
            
        df = pd.DataFrame(all_transactions)
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date')
        return df
        
    def get_holdings_summary(self, cas_data: CASData) -> pd.DataFrame:
        """Get summary of all holdings"""
        holdings_data = []
        for holding in cas_data.holdings:
            holdings_data.append({
                'scheme_name': holding.scheme_name,
                'folio_number': holding.folio_number,
                'amc': holding.amc,
                'isin': holding.isin,
                'units': holding.close_units,
                'nav': holding.current_nav,
                'current_value': holding.current_value,
                'transaction_count': len(holding.transactions)
            })
            
        if not holdings_data:
            return pd.DataFrame()
            
        df = pd.DataFrame(holdings_data)
        df = df.sort_values('current_value', ascending=False)
        return df


def create_sample_cas_data() -> CASData:
    """
    Create sample CAS data for testing without real PDFs
    
    This returns realistic sample data for Indian mutual funds
    """
    from datetime import datetime, timedelta
    import random
    
    sample_holdings = []
    schemes = [
        {
            'name': 'Axis Bluechip Fund - Direct Plan - Growth',
            'amc': 'Axis Asset Management Co. Ltd.',
            'isin': 'INF846K011N2',
            'nav': 52.34,
            'units': 1500.50,
        },
        {
            'name': 'Parag Parikh Flexi Cap Fund - Direct Plan - Growth',
            'amc': 'PPFAS Asset Management Co. Pvt. Ltd.',
            'isin': 'INF223J011Y9',
            'nav': 68.92,
            'units': 800.25,
        },
        {
            'name': 'Mirae Asset Large Cap Fund - Direct Plan - Growth',
            'amc': 'Mirae Asset Investment Managers (India) Pvt. Ltd.',
            'isin': 'INF602I010XX',
            'nav': 85.45,
            'units': 600.75,
        },
        {
            'name': 'ICICI Prudential Technology Fund - Direct Plan - Growth',
            'amc': 'ICICI Prudential Asset Management Co. Ltd.',
            'isin': 'INF459K01EH6',
            'nav': 168.23,
            'units': 350.50,
        },
        {
            'name': 'HDFC Index Fund - Nifty 50 Plan - Direct Plan - Growth',
            'amc': 'HDFC Asset Management Co. Ltd.',
            'isin': 'INF17VJ011X3',
            'nav': 185.67,
            'units': 500.00,
        },
    ]
    
    base_date = datetime(2023, 1, 1)
    
    for scheme in schemes:
        # Generate sample SIP transactions
        transactions = []
        current_units = scheme['units'] * 0.3  # Start with some initial investment
        
        for i in range(24):  # 2 years of SIP
            txn_date = base_date + timedelta(days=i*30)
            
            # Monthly SIP purchase
            sip_amount = random.choice([5000, 10000, 15000, 25000])
            nav = scheme['nav'] * (0.85 + random.random() * 0.3)  # Nav variation
            units_bought = sip_amount / nav
            current_units += units_bought
            
            txn = MFTransaction(
                scheme_name=scheme['name'],
                folio_number=f"ABC123456/{random.randint(100,999)}",
                amc=scheme['amc'],
                transaction_type='PURCHASE',
                units=units_bought,
                nav=nav,
                amount=sip_amount,
                date=txn_date,
                balance_units=current_units
            )
            transactions.append(txn)
            
        # Final holding
        holding = MFSchemeHolding(
            scheme_name=scheme['name'],
            folio_number=f"ABC123456/{random.randint(100,999)}",
            amc=scheme['amc'],
            isin=scheme['isin'],
            open_units=scheme['units'] * 0.3,
            close_units=scheme['units'],
            current_nav=scheme['nav'],
            current_value=scheme['nav'] * scheme['units'],
            transactions=transactions
        )
        sample_holdings.append(holding)
        
    # Calculate total value
    total_value = sum(h.current_value for h in sample_holdings)
    
    return CASData(
        statement_period='01-Jan-2023 to 31-Dec-2024',
        investor_name='Sample Investor',
        email='investor@example.com',
        mobile='+91-9876543210',
        pan='ABCDE1234F',
        address='123 Sample Street, Mumbai, Maharashtra 400001',
        holdings=sample_holdings,
        total_value=total_value
    )


if __name__ == "__main__":
    # Demo with sample data
    parser = CASParser()
    sample_data = create_sample_cas_data()
    
    print("=== Sample CAS Data ===")
    print(f"Investor: {sample_data.investor_name}")
    print(f"Statement Period: {sample_data.statement_period}")
    print(f"Total Portfolio Value: ₹{sample_data.total_value:,.2f}")
    print(f"Number of Holdings: {len(sample_data.holdings)}")
    print()
    
    print("=== Holdings ===")
    for holding in sample_data.holdings:
        print(f"{holding.scheme_name}")
        print(f"  Units: {holding.close_units:.2f} | NAV: ₹{holding.current_nav:.2f} | Value: ₹{holding.current_value:,.2f}")
        print(f"  Transactions: {len(holding.transactions)}")

    def create_sample_portfolio(self):
        """Create a sample portfolio for testing"""
        from dataclasses import dataclass
        from datetime import datetime
        
        @dataclass
        class SampleHolding:
            scheme_name: str
            folio: str
            units: float
            nav: float
            value: float
        
        @dataclass  
        class SamplePortfolio:
            investor_name: str
            holdings: list
            total_value: float
        
        holdings = [
            SampleHolding("Parag Parikh Flexi Cap Fund", "123456", 500.0, 65.0, 32500),
            SampleHolding("Mirae Asset Large Cap Fund", "234567", 300.0, 85.0, 25500),
            SampleHolding("Axis Small Cap Fund", "345678", 200.0, 120.0, 24000),
        ]
        
        return SamplePortfolio(
            investor_name="Test Investor",
            holdings=holdings,
            total_value=82000
        )
