import requests
import pandas as pd
import time
import re
from bs4 import BeautifulSoup

class EdgarBot:
    def __init__(self):
        self.base_url = "https://data.sec.gov"
        self.edgar_url = "https://www.sec.gov"
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    
    def get_company_list(self):
        """Fetch list of all public companies with CIK numbers and tickers"""
        try:
            url = "https://www.sec.gov/files/company_tickers.json"
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            companies = response.json()
            return [(comp['cik_str'], comp['title'], comp['ticker']) for comp in companies.values()]
        except Exception as e:
            print(f"Error fetching company list: {e}")
            return []
    
    def get_company_facts(self, cik):
        """Try XBRL API for revenue"""
        try:
            url = f"{self.base_url}/api/xbrl/companyfacts/CIK{cik:010d}.json"
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            facts = response.json()
            
            revenue = None
            revenue_tags = [
                'Revenues', 
                'SalesRevenueNet', 
                'RevenueFromContractWithCustomerExcludingAssessedTax',
                'TotalRevenue'
            ]
            for tag in revenue_tags:
                if 'us-gaap' in facts['facts'] and tag in facts['facts']['us-gaap']:
                    rev_data = facts['facts']['us-gaap'][tag]['units'].get('USD', [])
                    if rev_data:
                        revenue = sorted(rev_data, key=lambda x: x['end'])[-1]['val']
                        break
            
            return revenue, facts['entityName']
        except Exception as e:
            print(f"Error fetching XBRL data for CIK {cik}: {e}")
            return None, None
    
    def get_company_data(self, cik, name, ticker):
        """Get company data including revenue and ticker"""
        revenue, entity_name = self.get_company_facts(cik)
        print(f"{name} (CIK {cik}, Ticker {ticker}): Revenue = {revenue}")
        return revenue, ticker
    
    def scrape_all_companies(self, limit=None):
        """Scrape data for all companies"""
        companies = self.get_company_list()
        if not companies:
            return None
        
        data = []
        for i, (cik, name, ticker) in enumerate(companies[:limit]):
            print(f"Fetching data for {name} ({i+1}/{len(companies[:limit])})...")
            revenue, ticker = self.get_company_data(cik, name, ticker)
            if revenue or ticker:
                data.append({
                    'Company': name,
                    'CIK': cik,
                    'Ticker': ticker,
                    'Revenue': revenue if revenue is not None else 'Not Found'
                })
            time.sleep(1)  # Rate limiting
        
        df = pd.DataFrame(data)
        return df
    
    def save_to_csv(self, df, filename):
        if df is not None and not df.empty:
            df.to_csv(filename, index=False)
            print(f"Data saved to {filename}")

def main():
    bot = EdgarBot()
    
    print("Scraping SEC EDGAR for company data...")
    df = bot.scrape_all_companies()  # Test with 10
    
    if df is not None:
        bot.save_to_csv(df, 'edgar_company_data.csv')
        print("\nSample of the data:")
        print(df.head())
        print(f"\nTotal companies: {len(df)}")
    else:
        print("Failed to fetch data.")

if __name__ == "__main__":
    main()