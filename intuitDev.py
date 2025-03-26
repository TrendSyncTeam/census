import requests
import json
import sys
from time import sleep
import csv

username = 'gentlejason'
apiKey = 'WUiHKzcoaZlUweMgakZozFb5B'
scraper = 'linkedinCompanyProfile'

# List of 100 famous e-commerce and trading companies with their LinkedIn URLs
urls = [
    "https://www.linkedin.com/company/amazon/",  # E-commerce giant
    "https://www.linkedin.com/company/walmart/",  # Retail and e-commerce
    "https://www.linkedin.com/company/ebay/",  # Online marketplace
    "https://www.linkedin.com/company/alibaba-com/",  # E-commerce and trading
    "https://www.linkedin.com/company/jd.com/",  # Chinese e-commerce
    "https://www.linkedin.com/company/rakuten/",  # Japanese e-commerce
    "https://www.linkedin.com/company/shopify/",  # E-commerce platform
    "https://www.linkedin.com/company/etsy/",  # Handmade goods marketplace
    "https://www.linkedin.com/company/target/",  # Retail and e-commerce
    "https://www.linkedin.com/company/best-buy/",  # Electronics retail
    "https://www.linkedin.com/company/overstock/",  # Online retailer
    "https://www.linkedin.com/company/zalando/",  # European fashion e-commerce
    "https://www.linkedin.com/company/asos-plc/",  # Online fashion retailer
    "https://www.linkedin.com/company/wayfair/",  # Home goods e-commerce
    "https://www.linkedin.com/company/newegg/",  # Electronics e-commerce
    "https://www.linkedin.com/company/flipkart/",  # Indian e-commerce
    "https://www.linkedin.com/company/mercadolibre/",  # Latin American marketplace
    "https://www.linkedin.com/company/shopee/",  # Southeast Asian e-commerce
    "https://www.linkedin.com/company/lazada/",  # Southeast Asian e-commerce
    "https://www.linkedin.com/company/pinduoduo/",  # Chinese group buying
    "https://www.linkedin.com/company/costco-wholesale/",  # Wholesale retail
    "https://www.linkedin.com/company/kroger/",  # Grocery retail
    "https://www.linkedin.com/company/home-depot/",  # Home improvement retail
    "https://www.linkedin.com/company/lowes-companies-inc/",  # Home improvement retail
    "https://www.linkedin.com/company/macys/",  # Department store and e-commerce
    "https://www.linkedin.com/company/nordstrom/",  # Fashion retail
    "https://www.linkedin.com/company/sephora/",  # Beauty products retail
    "https://www.linkedin.com/company/ulta-beauty/",  # Beauty products retail
    "https://www.linkedin.com/company/qvc/",  # TV and online shopping
    "https://www.linkedin.com/company/hsn/",  # Home shopping network
    "https://www.linkedin.com/company/ Tractor-supply/",  # Rural lifestyle retail
    "https://www.linkedin.com/company/dicks-sporting-goods/",  # Sporting goods retail
    "https://www.linkedin.com/company/gap-inc-/",  # Apparel retail
    "https://www.linkedin.com/company/hm/",  # Fast fashion retail
    "https://www.linkedin.com/company/zara/",  # Fast fashion retail
    "https://www.linkedin.com/company/uniqlo/",  # Apparel retail
    "https://www.linkedin.com/company/shein/",  # Fast fashion e-commerce
    "https://www.linkedin.com/company/boohoo-com/",  # Online fashion retailer
    "https://www.linkedin.com/company/forever-21/",  # Fashion retail
    "https://www.linkedin.com/company/bonobos/",  # Online menswear
    "https://www.linkedin.com/company/cargill/",  # Agricultural trading
    "https://www.linkedin.com/company/glencore/",  # Commodities trading
    "https://www.linkedin.com/company/vitol-group/",  # Energy trading
    "https://www.linkedin.com/company/trafigura/",  # Commodities trading
    "https://www.linkedin.com/company/koch-industries/",  # Trading and manufacturing
    "https://www.linkedin.com/company/archer-daniels-midland/",  # Agricultural trading
    "https://www.linkedin.com/company/bunge/",  # Agricultural trading
    "https://www.linkedin.com/company/louis-dreyfus-company/",  # Agricultural trading
    "https://www.linkedin.com/company/olam-international/",  # Food trading
    "https://www.linkedin.com/company/sygenta/",  # Agricultural trading
    "https://www.linkedin.com/company/mercuria-energy-trading/",  # Energy trading
    "https://www.linkedin.com/company/gunvor/",  # Energy trading
    "https://www.linkedin.com/company/phillips-66/",  # Energy trading
    "https://www.linkedin.com/company/marathon-petroleum-corporation/",  # Energy trading
    "https://www.linkedin.com/company/valero-energy-corporation/",  # Energy trading
    "https://www.linkedin.com/company/ reliance-industries-limited/",  # Trading and retail
    "https://www.linkedin.com/company/tesco/",  # Grocery retail
    "https://www.linkedin.com/company/aldi-stores/",  # Grocery retail
    "https://www.linkedin.com/company/lidl/",  # Grocery retail
    "https://www.linkedin.com/company/carrefour/",  # Retail and e-commerce
    "https://www.linkedin.com/company/aeon-co-ltd/",  # Japanese retail
    "https://www.linkedin.com/company/seven-&-i-holdings-co-ltd/",  # Retail (7-Eleven)
    "https://www.linkedin.com/company/woolworths-group/",  # Australian retail
    "https://www.linkedin.com/company/sainsburys/",  # UK grocery retail
    "https://www.linkedin.com/company/ikea/",  # Furniture retail
    "https://www.linkedin.com/company/decathlon/",  # Sporting goods retail
    "https://www.linkedin.com/company/pepkor/",  # South African retail
    "https://www.linkedin.com/company/falabella/",  # Latin American retail
    "https://www.linkedin.com/company/coupang/",  # South Korean e-commerce
    "https://www.linkedin.com/company/trendyol/",  # Turkish e-commerce
    "https://www.linkedin.com/company/jumia-group/",  # African e-commerce
    "https://www.linkedin.com/company/allegro/",  # Polish e-commerce
    "https://www.linkedin.com/company/ozon-ru/",  # Russian e-commerce
    "https://www.linkedin.com/company/wildberries/",  # Russian e-commerce
    "https://www.linkedin.com/company/tokopedia/",  # Indonesian e-commerce
    "https://www.linkedin.com/company/bukalapak/",  # Indonesian e-commerce
    "https://www.linkedin.com/company/americanas/",  # Brazilian e-commerce
    "https://www.linkedin.com/company/magazine-luiza/",  # Brazilian retail
    "https://www.linkedin.com/company/otto-group/",  # German e-commerce
    "https://www.linkedin.com/company/john-lewis-partnership/",  # UK retail
    "https://www.linkedin.com/company/marks-and-spencer/",  # UK retail
    "https://www.linkedin.com/company/foot-locker/",  # Footwear retail
    "https://www.linkedin.com/company/chewy-inc/",  # Pet products e-commerce
    "https://www.linkedin.com/company/stitch-fix/",  # Online personal styling
    "https://www.linkedin.com/company/rent-the-runway/",  # Fashion rental
    "https://www.linkedin.com/company/thredup/",  # Second-hand clothing
    "https://www.linkedin.com/company/vinted/",  # Second-hand marketplace
    "https://www.linkedin.com/company/poshmark/",  # Social commerce
    "https://www.linkedin.com/company/revolve/",  # Fashion e-commerce
    "https://www.linkedin.com/company/farfetch/",  # Luxury fashion e-commerce
    "https://www.linkedin.com/company/ssense/",  # Luxury e-commerce
    "https://www.linkedin.com/company/net-a-porter/",  # Luxury fashion
    "https://www.linkedin.com/company/groupon/",  # Deals marketplace
    "https://www.linkedin.com/company/living-social/",  # Deals marketplace
    "https://www.linkedin.com/company/dollar-general/",  # Discount retail
    "https://www.linkedin.com/company/dollar-tree/",  # Discount retail
    "https://www.linkedin.com/company/big-lots-stores/",  # Discount retail
    "https://www.linkedin.com/company/ross-stores-inc/",  # Off-price retail
    "https://www.linkedin.com/company/tjx-companies/",  # Off-price retail
]

apiEndPoint = "http://api.scraping-bot.io/scrape/data-scraper"
apiEndPointResponse = "http://api.scraping-bot.io/scrape/data-scraper-response?"

scrapignData = {}

# Create scraping data for each URL
for url in urls:
    scrapignData[url] = {
        'pending': True,
        'responseId': None,
        'response': None,
        'error': None
    }

# Ask all response ID
for url in urls:
    payload = json.dumps({"url": url, "scraper": scraper})
    headers = {
        'Content-Type': "application/json"
    }

    response = requests.request("POST", apiEndPoint, data=payload, auth=(username, apiKey), headers=headers)
    if response.status_code == 200:
        print(response.json())
        print(response.json()["responseId"])
        scrapignData[url]['responseId'] = response.json()["responseId"]
    else:
        scrapignData[url]['error'] = response.text

# All responseId are asked, now ask for each result
pendingQueries = len(urls)
while pendingQueries > 0:
    sleep(5)  # sleep 5s between each loop

    for url in urls:
        if scrapignData[url]["pending"]:
            finalApiCall = apiEndPointResponse + "scraper=" + scraper + "&responseId=" + str(scrapignData[url]["responseId"])
            print(finalApiCall)
            finalResponse = requests.request("GET", finalApiCall, auth=(username, apiKey))
            result = finalResponse.json()
            if type(result) is list:
                scrapignData[url]["pending"] = False
                scrapignData[url]["response"] = finalResponse.text
                print(url + " : is Done")
            elif type(result) is dict:
                if "status" in result and result["status"] == "pending":
                    print(result["message"])
                    print(url + " : is still pending")
                    continue
                elif result["error"] is not None:
                    scrapignData[url]["pending"] = False
                    scrapignData[url]["error"] = json.dumps(result, indent=4)
                    print(url + " : got an error")
                    print(json.dumps(result, indent=4))

            if scrapignData[url]["pending"] == False:
                pendingQueries -= 1

print("All Scrapings are done!")

# Save results to CSV
csv_filename = "ecommerce_trading_results.csv"
with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['URL', 'ResponseID', 'Response', 'Error']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    writer.writeheader()
    for url, data in scrapignData.items():
        writer.writerow({
            'URL': url,
            'ResponseID': data['responseId'],
            'Response': data['response'],
            'Error': data['error']
        })

print(f"Results have been saved to {csv_filename}")
# print(json.dumps(scrapignData, indent=4))