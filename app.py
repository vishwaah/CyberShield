from flask import Flask, request, jsonify
import subprocess
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def run_script(script_name, arg):
    """
    Run a Python script with an argument and return the output.
    The script should return a JSON-formatted string.
    """
    try:
        result = subprocess.run(
            ['python', f'{script_name}.py', arg],
            capture_output=True,
            text=True
        )
        return json.loads(result.stdout)
    except Exception as e:
        return {"score": 0.0, "details": {"error": f"Error running {script_name}: {str(e)}"}}

@app.route('/api/check-url', methods=['POST'])
def check_url():
    if request.method == 'POST':
        data = request.get_json()
        url = data.get('url')
        return jsonify({"message": "POST received", "url": url})
    elif request.method == 'GET':
        return jsonify({"message": "GET received"})
    
    if not url:
        return jsonify({"error": "URL is required"}), 400
    
    # Run the five scripts
    scripts = ['blackListStatus', 'SSLGrade', 'domain', 'socialMedia', 'scrapingReviews']
    results = {script: run_script(script, url) for script in scripts}

    # Aggregate scores
    final_score = sum(results[script]['score'] for script in scripts if 'score' in results[script]) / len(scripts)
    
    return jsonify({
        "final_score": final_score,
        "details": results
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
