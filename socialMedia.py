import requests
import re
from html.parser import HTMLParser

# Social media domain regex pattern
SOCIAL_MEDIA_PATTERN = re.compile(
    r"(facebook\.com|twitter\.com|linkedin\.com|instagram\.com|youtube\.com|"
    r"tiktok\.com|pinterest\.com|snapchat\.com|reddit\.com)", re.IGNORECASE
)

class SocialMediaLinkFinder(HTMLParser):
    def __init__(self):
        super().__init__()
        self.social_links = []

    def handle_starttag(self, tag, attrs):
        # Look for <a> tags with "href" attributes
        if tag == "a":
            for attr_name, attr_value in attrs:
                if attr_name == "href" and attr_value:
                    # Check if the href matches the social media pattern
                    if SOCIAL_MEDIA_PATTERN.search(attr_value):
                        self.social_links.append(attr_value)

def check_any_social_media_presence(url, max_links=100):
    """
    Checks for social media presence on the website and returns a normalized score:
    - Presence detected → Score = 1.0
    - No presence detected → Score = 0.0
    """
    try:
        # Send a GET request with a timeout
        response = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status()

        # Use the custom HTML parser
        parser = SocialMediaLinkFinder()
        parser.feed(response.text)

        # Get the detected social media links
        social_media_links = parser.social_links[:max_links]  # Limit to max_links

        # Calculate score
        if social_media_links:
            return {
                "score": 1.0,
                "details": {
                    "social_media_links": social_media_links,
                    "message": "Social media presence detected"
                }
            }
        else:
            return {
                "score": 0.0,
                "details": {
                    "social_media_links": [],
                    "message": "No social media presence found"
                }
            }

    except requests.exceptions.RequestException as e:
        return {
            "score": 0.0,
            "details": {
                "error": f"Failed to retrieve {url}: {str(e)}"
            }
        }

if __name__ == "__main__":
    website_url = input("Enter the website URL: ")
    result = check_any_social_media_presence(website_url)
    print(result)

