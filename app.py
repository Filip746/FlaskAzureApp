from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

AZURE_ML_ENDPOINT = "https://b73a5ed0-5a44-4896-985e-69680dc267bf.northeurope.azurecontainer.io/score"
AZURE_ML_API_KEY = "JqS3yTa93SKn8YYsqPI5bCuYHb9rzK7g"

headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {AZURE_ML_API_KEY}'
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get JSON data from frontend
        data = request.get_json()
        
        # Convert input into the expected format for Azure ML
        input_data = {
            "data": [[float(data['param1']), float(data['param2']), float(data['param3'])]]  # Ensure numeric values
        }
        
        # Send request to Azure ML
        response = requests.post(AZURE_ML_ENDPOINT, json=input_data, headers=headers)
        
        # Handle Azure response
        if response.status_code == 200:
            prediction = response.json()
            return jsonify({"prediction": prediction})  # Ensure correct key

        return jsonify({'error': 'Azure API request failed'}), response.status_code

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)