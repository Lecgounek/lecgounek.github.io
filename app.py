from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)
CORS(app)

@app.route('/')
def home():
    return send_from_directory('static', 'index.html')

@app.route('/api/random')
def random_article():
    try:
        response = requests.get('https://en.wikipedia.org/w/api.php', params={
            'action': 'query',
            'list': 'random',
            'format': 'json',
            'rnnamespace': 0,
            'rnlimit': 1
        })
        response.raise_for_status()
        return jsonify(response.json())
    except requests.RequestException as e:
        app.logger.error(f"Error fetching random article: {str(e)}")
        return jsonify({"error": f"Failed to fetch random article: {str(e)}"}), 500

@app.route('/api/article')
def get_article():
    title = request.args.get('title')
    if not title:
        return jsonify({"error": "No title provided"}), 400
    
    try:
        response = requests.get('https://en.wikipedia.org/w/api.php', params={
            'action': 'parse',
            'page': title,
            'format': 'json',
            'prop': 'text|styles'
        })
        response.raise_for_status()
        data = response.json()
        if 'error' in data:
            return jsonify({"error": f"Wikipedia API error: {data['error']['info']}"}), 400
        return jsonify(data)
    except requests.RequestException as e:
        app.logger.error(f"Error fetching article {title}: {str(e)}")
        return jsonify({"error": f"Failed to fetch article {title}: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
