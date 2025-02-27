from flask import Flask, render_template, request, jsonify
import urllib.request
import json
import ssl
import os

def allowSelfSignedHttps(allowed):
    if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
        ssl._create_default_https_context = ssl._create_unverified_context

allowSelfSignedHttps(True)

app = Flask(__name__)

API_URL = 'http://b73a5ed0-5a44-4896-985e-69680dc267bf.northeurope.azurecontainer.io/score'
API_KEY = 'JqS3yTa93SKn8YYsqPI5bCuYHb9rzK7g'  # Replace with your API key

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        input_data = request.json  # JSON iz zahtjeva

        # Prepravi strukturu JSON-a kako bi odgovarao očekivanom formatu
        formatted_data = {
            "Inputs": {
                "input1": [input_data]  # Azure ML očekuje listu unutar "input1"
            }
        }

        body = json.dumps(formatted_data).encode('utf-8')  # Encode u JSON format
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + API_KEY
        }

        req = urllib.request.Request(API_URL, body, headers)
        response = urllib.request.urlopen(req)
        result = json.loads(response.read())

        return jsonify(result)

    except urllib.error.HTTPError as e:
        return jsonify({"error": e.read().decode("utf-8")}), e.code


if __name__ == '__main__':
    app.run(debug=True)