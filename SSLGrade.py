import time
import requests

def get_ssl_grade(domain):
    """
    Fetches the SSL grade for a given domain and returns a normalized score:
    - Grade A+ or A → Score = 1.0
    - Grade B or C → Score = 0.5
    - Grade D or lower → Score = 0.0
    """
    url = f"https://api.ssllabs.com/api/v3/analyze?host={domain}&fromCache=on&startNew=off"
    grade_to_score = {"A+": 1.0, "A": 1.0, "B": 0.5, "C": 0.5, "D": 0.0}
    ssl_details = {}

    while True:
        try:
            response = requests.get(url).json()
            status = response.get("status")

            if status == "READY":
                grade = response["endpoints"][0].get("grade", "D")  # Default to "D" if grade is missing
                ssl_details = {
                    "grade": grade,
                    "status_message": "Analysis complete",
                }
                score = grade_to_score.get(grade, 0.0)
                return {
                    "score": score,
                    "details": ssl_details
                }

            elif status == "ERROR":
                ssl_details = {"error": "Error in SSL Labs API analysis"}
                return {
                    "score": 0.0,
                    "details": ssl_details
                }

            print("Analysis in progress, waiting for 10 seconds...")
            time.sleep(10)

        except Exception as e:
            ssl_details = {"error": f"An exception occurred: {str(e)}"}
            return {
                "score": 0.0,
                "details": ssl_details
            }

if __name__ == "__main__":
    domain = input("Enter domain: ")
    result = get_ssl_grade(domain)
    print(result)
