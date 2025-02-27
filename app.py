from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

# Postavi endpoint i API ključ
AZURE_ML_ENDPOINT = "http://b73a5ed0-5a44-4896-985e-69680dc267bf.northeurope.azurecontainer.io/score"
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
    data = request.get_json()
    input_data = {"data": [[data['param1'], data['param2'], data['param3']]]}
    
    response = requests.post(AZURE_ML_ENDPOINT, 
                            json=input_data, 
                            headers=headers)
    
    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({'error': 'API request failed'}), 500

if __name__ == '__main__':
    app.run(debug=True)