import requests
import pandas as pd
import time
from bs4 import BeautifulSoup

class EdgarBot:
    def __init__(self):
        self.base_url = "https://data.sec.gov"
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    
    def get_company_list(self):
        """Fetch list of all public companies with CIK numbers"""
        try:
            url = "https://www.sec.gov/files/company_tickers.json"
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            companies = response.json()
            return [(comp['cik_str'], comp['title']) for comp in companies.values()]
        except Exception as e:
            print(f"Error fetching company list: {e}")
            return []
    
    def get_company_facts(self, cik):
        """Get revenue and employee data for a specific company by CIK"""
        try:
            url = f"{self.base_url}/api/xbrl/companyfacts/CIK{cik:010d}.json"
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            facts = response.json()
            
            # Extract latest revenue (e.g., 'Revenues' or 'SalesRevenueNet')
            revenue = None
            employee_count = None
            
            # Look for revenue in facts
            for concept in ['Revenues', 'SalesRevenueNet', 'RevenueFromContractWithCustomerExcludingAssessedTax']:
                if concept in facts['facts'].get('us-gaap', {}):
                    rev_data = facts['facts']['us-gaap'][concept]['units']['USD']
                    revenue = sorted(rev_data, key=lambda x: x['end'])[-1]['val']  # Latest value
                    break
            
            # Look for employee count
            if 'NumberOfEmployees' in facts['facts'].get('us-gaap', {}):
                emp_data = facts['facts']['us-gaap']['NumberOfEmployees']['units']['pure']
                employee_count = sorted(emp_data, key=lambda x: x['end'])[-1]['val']
            
            return revenue, employee_count
        except Exception as e:
            print(f"Error fetching data for CIK {cik}: {e}")
            return None, None
    
    def scrape_all_companies(self, limit=None):
        """Scrape data for all companies (or up to a limit)"""
        companies = self.get_company_list()
        if not companies:
            return None
        
        data = []
        for i, (cik, name) in enumerate(companies[:limit]):
            print(f"Fetching data for {name} ({i+1}/{len(companies[:limit])})...")
            revenue, employees = self.get_company_facts(cik)
            if revenue or employees:
                data.append({
                    'Company': name,
                    'CIK': cik,
                    'Revenue': revenue,
                    'Employees': employees
                })
            time.sleep(1)  # Rate limiting (SEC allows 10 requests/sec, but let’s be safe)
        
        df = pd.DataFrame(data)
        return df
    
    def save_to_csv(self, df, filename):
        if df is not None and not df.empty:
            df.to_csv(filename, index=False)
            print(f"Data saved to {filename}")

def main():
    bot = EdgarBot()
    
    # Scrape data (limit to 50 companies for testing; remove limit for all)
    print("Scraping SEC EDGAR for company data...")
    df = bot.scrape_all_companies(limit=50)  # Set limit=None for all companies
    
    if df is not None:
        bot.save_to_csv(df, 'edgar_company_data.csv')
        print("\nSample of the data:")
        print(df.head())
        print(f"\nTotal companies: {len(df)}")
    else:
        print("Failed to fetch data.")

if __name__ == "__main__":
    main()