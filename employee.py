import requests
import json
import csv
from time import sleep

# Census API base URL for ACS 5-year data (2022)
BASE_URL = "https://api.census.gov/data/2022/acs/acs5"

# Optional: Add your Census API key here (remove if not using)
API_KEY = None  # Replace with "YOUR_API_KEY" if you have one

# List of all state FIPS codes (50 states + DC)
STATE_FIPS = [
    "01", "02", "04", "05", "06", "08", "09", "10", "11", "12", "13", "15", "16",
    "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29",
    "30", "31", "32", "33", "34", "35", "36", "37", "38", "39", "40", "41", "42",
    "44", "45", "46", "47", "48", "49", "50", "51", "53", "54", "55", "56"
]

def fetch_employee_data(state_code):
    """
    Fetch employed civilian population data for all places in a given state.
    :param state_code: 2-digit FIPS code
    :return: List of dictionaries with city data
    """
    params = {
        "get": "NAME,B23025_003E",  # NAME = city name, B23025_003E = employed civilians
        "for": "place:*",           # All places (cities/towns)
        "in": f"state:{state_code}" # Restrict to specified state
    }
    
    if API_KEY:
        params["key"] = API_KEY

    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        
        data = response.json()
        headers = data[0]
        rows = data[1:]
        
        results = []
        for row in rows:
            city_data = {
                "city_name": row[0],
                "employed_count": row[1],
                "state_code": row[2],
                "place_code": row[3]
            }
            results.append(city_data)
        
        return results
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for state {state_code}: {e}")
        return []

def save_to_csv(data, filename="employee_data_all_cities.csv"):
    """
    Append data to a CSV file.
    :param data: List of dictionaries with city data
    :param filename: Output CSV file name
    """
    fieldnames = ["city_name", "employed_count", "state_code", "place_code"]
    
    # Open file in append mode
    with open(filename, "a", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        # Write header only if file is empty
        if csvfile.tell() == 0:
            writer.writeheader()
        
        # Write data rows
        writer.writerows(data)

def fetch_all_cities():
    """
    Fetch employee data for all cities across all states and save to CSV.
    """
    print("Starting to fetch employee data for all cities in the U.S...")
    print("This may take a while due to API rate limits and the number of states.")
    
    total_cities = 0
    
    # Clear the output file if it exists (optional: comment out to append instead)
    open("employee_data_all_cities.csv", "w").close()
    
    # Iterate over all states
    for state_code in STATE_FIPS:
        print(f"Fetching data for state {state_code}...")
        data = fetch_employee_data(state_code)
        
        if data:
            total_cities += len(data)
            save_to_csv(data)
            print(f"  Found {len(data)} cities in state {state_code}")
        else:
            print(f"  No data retrieved for state {state_code}")
        
        # Sleep to avoid hitting API rate limits (500 requests/day without key)
        sleep(1)  # Adjust as needed
    
    print(f"\nDone! Total cities processed: {total_cities}")
    print("Data saved to 'employee_data_all_cities.csv'")

def main():
    print("Welcome to the Census Employee Data Bot!")
    print("This bot will fetch employee data for all cities in all U.S. states.")
    confirm = input("Do you want to proceed? (yes/no): ").strip().lower()
    
    if confirm == "yes":
        fetch_all_cities()
    else:
        print("Operation canceled.")

if __name__ == "__main__":
    main()