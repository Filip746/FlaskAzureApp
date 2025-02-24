from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

# Postavi endpoint i API ključ
AZURE_ML_ENDPOINT = "http://08e78837-60ea-43a3-a2e1-7d03089f3c06.northeurope.azurecontainer.io/score"
AZURE_ML_API_KEY = "zqd2QDPCjH1nR9ofFn8mHF6ucgzVbUpZ"

headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {AZURE_ML_API_KEY}'
}

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