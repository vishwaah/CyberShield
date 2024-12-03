import os
import requests
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
GOOGLE_SAFE_BROWSING_API_KEY = os.getenv("GOOGLE_API_KEY")

def is_url_blacklisted(url):
    """
    Check if a URL is blacklisted using Google Safe Browsing API.
    Returns a normalized score and details:
    - Blacklisted → Score = 0.0
    - Safe → Score = 1.0
    """
    api_url = "https://safebrowsing.googleapis.com/v4/threatMatches:find"
    payload = {
        "client": {
            "clientId": "your_client_id",
            "clientVersion": "1.0"
        },
        "threatInfo": {
            "threatTypes": ["MALWARE", "SOCIAL_ENGINEERING", "UNWANTED_SOFTWARE", "POTENTIALLY_HARMFUL_APPLICATION"],
            "platformTypes": ["ANY_PLATFORM"],
            "threatEntryTypes": ["URL"],
            "threatEntries": [{"url": url}]
        }
    }

    headers = {"Content-Type": "application/json"}
    try:
        response = requests.post(f"{api_url}?key={GOOGLE_SAFE_BROWSING_API_KEY}", json=payload, headers=headers)
        if response.status_code == 200:
            threats = response.json().get("matches", [])
            if threats:
                return {
                    "score": 0.0,
                    "details": {
                        "url": url,
                        "blacklisted": True,
                        "threats": threats
                    }
                }
            else:
                return {
                    "score": 1.0,
                    "details": {
                        "url": url,
                        "blacklisted": False,
                        "message": "The URL is safe and not blacklisted."
                    }
                }
        else:
            return {
                "score": 0.0,
                "details": {
                    "error": f"API error: {response.status_code}, {response.text}"
                }
            }
    except Exception as e:
        return {
            "score": 0.0,
            "details": {
                "error": f"Exception occurred: {str(e)}"
            }
        }

def does_url_exist(url):
    """
    Check if a URL exists by making an HTTP GET request.
    Returns a boolean indicating existence.
    """
    try:
        response = requests.get(url, timeout=5)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

if __name__ == "__main__":
    website_url = input("Enter the URL to check: ").strip()

    if does_url_exist(website_url):
        print(f"The URL '{website_url}' exists.")
        blacklist_result = is_url_blacklisted(website_url)
        print(blacklist_result)
    else:
        print(f"The URL '{website_url}' does not exist or is unreachable.")
