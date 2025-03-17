import requests
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
    Fetch employee data (total, male, female) and population for all places in a state.
    :param state_code: 2-digit FIPS code
    :return: List of dictionaries with city data
    """
    params = {
        "get": "NAME,B23025_003E,B23025_004E,B23025_005E,B01001_001E",  # Variables: total employed, male, female, population
        "for": "place:*",           # All places (cities/towns)
        "in": f"state:{state_code}" # Restrict to specified state
    }
    
    if API_KEY:
        params["key"] = API_KEY

    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        
        data = response.json()
        headers = data[0]  # Headers: ["NAME", "B23025_003E", "B23025_004E", "B23025_005E", "B01001_001E", "state", "place"]
        rows = data[1:]
        
        results = []
        for row in rows:
            city_data = {
                "city_name": row[0],
                "employed_total": row[1],    # B23025_003E: Total employed
                "employed_male": row[2],     # B23025_004E: Male employed
                "employed_female": row[3],   # B23025_005E: Female employed
                "population": row[4],        # B01001_001E: Total population
                "state_code": row[5],
                "place_code": row[6]
            }
            results.append(city_data)
        
        return results
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for state {state_code}: {e}")
        return []

def save_to_csv(data, filename="employee_data_all_cities_gender.csv"):
    """
    Append data to a CSV file.
    :param data: List of dictionaries with city data
    :param filename: Output CSV file name
    """
    fieldnames = ["city_name", "employed_total", "employed_male", "employed_female", "population", "state_code", "place_code"]
    
    with open(filename, "a", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        if csvfile.tell() == 0:
            writer.writeheader()
        
        writer.writerows(data)

def fetch_all_cities():
    """
    Fetch employee data (total, male, female) and population for all cities across all states.
    """
    print("Starting to fetch employee data (by gender) and population for all cities in the U.S...")
    print("This may take a while due to API rate limits and the number of states.")
    
    total_cities = 0
    
    # Clear the output file (optional: comment out to append instead)
    open("employee_data_all_cities_gender.csv", "w").close()
    
    for state_code in STATE_FIPS:
        print(f"Fetching data for state {state_code}...")
        data = fetch_employee_data(state_code)
        
        if data:
            total_cities += len(data)
            save_to_csv(data)
            print(f"  Found {len(data)} cities in state {state_code}")
        else:
            print(f"  No data retrieved for state {state_code}")
        
        # Sleep to respect API rate limits
        sleep(1)  # Adjust as needed
    
    print(f"\nDone! Total cities processed: {total_cities}")
    print("Data saved to 'employee_data_all_cities_gender.csv'")

def main():
    print("Welcome to the Census Employee Data Bot!")
    print("This bot will fetch employee data (total, male, female) and population for all cities in all U.S. states.")
    confirm = input("Do you want to proceed? (yes/no): ").strip().lower()
    
    if confirm == "yes":
        fetch_all_cities()
    else:
        print("Operation canceled.")

if __name__ == "__main__":
    main()