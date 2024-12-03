import time
from whoisapi import *
import json
from datetime import datetime

# Initialize the WHOIS API client
client = Client(api_key='at_V3Q1KmRuKRGx7J5EwGUPQqkq25ZPL')

def calculate_age_score(created_date):
    """
    Calculates a score based on the domain age.
    Older domains are considered more trustworthy.
    """
    try:
        created_date_obj = datetime.strptime(created_date, '%Y-%m-%dT%H:%M:%SZ')  # Parse WHOIS date format
        age_years = (datetime.now() - created_date_obj).days / 365

        if age_years > 3:
            return 1  # High score for domains older than 5 years
        elif 1 <= age_years <= 3:
            return 0.5  # Medium score for domains 2-5 years old
        else:
            return 0  # Low score for domains younger than 2 years
    except Exception as e:
        print(f"Error calculating domain age: {e}")
        return 0  # Default to 0 if there's an error

def domainAge(domain):
    try:
        # Fetch raw WHOIS data
        resp_str = client.raw_data(domain)
        resp_json = json.loads(resp_str)
        
        # Extract the required fields
        registry_data = resp_json.get('WhoisRecord', {}).get('registryData', {})
        created_date = registry_data.get('createdDate', 'N/A')
        
        # Calculate score
        if created_date != 'N/A':
            age_score = calculate_age_score(created_date)
        else:
            age_score = 0  # If creation date is unavailable, default to 0
        
        # Prepare output
        result = {
            "score": age_score,
            "details": {
                "created_date": created_date,
                "domain": domain
            }
        }
        return result
    
    except json.JSONDecodeError:
        print("Error: Unable to parse the response as JSON.")
        return {"score": 0, "details": {"error": "JSON decode error"}}
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return {"score": 0, "details": {"error": str(e)}}

# Get domain input from the user
if __name__ == "__main__":
    domain = input("Enter domain: ")
    output = domainAge(domain)
    print(json.dumps(output, indent=4))
