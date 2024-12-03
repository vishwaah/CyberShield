import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from textblob import TextBlob

def extract_domain(url):
    """Extracts the domain name from the URL."""
    parsed_url = urlparse(url)
    domain = parsed_url.netloc or parsed_url.path
    return domain.replace("www.", "")

def fetch_reviews(domain):
    """
    Scrapes reviews for the given domain from Trustpilot.
    """
    search_url = f"https://www.trustpilot.com/review/{domain}"
    try:
        response = requests.get(search_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        reviews = []
        review_containers = soup.find_all('section', class_='styles_reviewsContainer__3_GQw')
        for container in review_containers:
            review_texts = container.find_all('p')
            for review_text in review_texts:
                review = review_text.text.strip()

                # Filter irrelevant reviews
                if re.match(r'^\d{1,3}(,\d{3})*(\s?total)?$', review):  # Matches total review counts
                    continue
                if re.match(r'^\d+%$', review):  # Matches percentage reviews like "54%"
                    continue
                if re.match(r'Date of experience:', review):  # Matches "Date of experience" entries
                    continue
                if re.match(r'Filter|Most relevant', review):  # Matches "Filter" or "Most relevant"
                    continue
                if re.match(r'\d{1,2}-star', review):  # Matches star ratings like "5-star", "4-star"
                    continue
                
                reviews.append(review)
        
        return reviews
    except Exception as e:
        print(f"Error fetching reviews: {e}")
        return []

def analyze_reviews(reviews):
    """Performs sentiment analysis on reviews."""
    positive, negative, neutral = 0, 0, 0
    for review in reviews:
        sentiment = TextBlob(review).sentiment.polarity
        if sentiment > 0.1:
            positive += 1
        elif sentiment < -0.1:
            negative += 1
        else:
            neutral += 1
    
    total_reviews = len(reviews)
    return {
        "positive": positive / total_reviews * 100 if total_reviews else 0,
        "negative": negative / total_reviews * 100 if total_reviews else 0,
        "neutral": neutral / total_reviews * 100 if total_reviews else 0
    }

def calculate_review_score(sentiment_data):
    """
    Calculates a score based on sentiment analysis:
    - Positive > 50% → Score = 1.0
    - Negative > 50% → Score = 0.0
    - Otherwise → Score = 0.5
    """
    if sentiment_data["positive"] > 50:
        return 1.0
    elif sentiment_data["negative"] > 50:
        return 0.0
    else:
        return 0.5

def generate_report(domain, sentiment_data, reviews):
    """Generates a safety report for the website."""
    report = f"Safety Report for {domain}\n"
    report += "=" * 40 + "\n"
    report += f"Total Reviews Scraped: {len(reviews)}\n"
    report += f"Positive Reviews: {sentiment_data['positive']:.2f}%\n"
    report += f"Negative Reviews: {sentiment_data['negative']:.2f}%\n"
    report += f"Neutral Reviews: {sentiment_data['neutral']:.2f}%\n\n"
    
    if sentiment_data['negative'] > 50:
        report += "⚠️ High percentage of negative reviews! Proceed with caution.\n"
    else:
        report += "✅ Website appears to have a good reputation based on reviews.\n"
    
    return report

def main():
    url = input("Enter the website URL: ")
    domain = extract_domain(url)
    print(f"Checking reviews for {domain}...\n")
    
    reviews = fetch_reviews(domain)
    if not reviews:
        print("No reviews found or unable to scrape the website.")
        return {"score": 0, "details": {"error": "No reviews found"}}

    sentiment_data = analyze_reviews(reviews)
    review_score = calculate_review_score(sentiment_data)

    result = {
        "score": review_score,
        "details": {
            "domain": domain,
            "sentiment_data": sentiment_data,
            "review_count": len(reviews)
        }
    }
    
    return result

if __name__ == "__main__":
    result = main()
    if result:
        print(result)
