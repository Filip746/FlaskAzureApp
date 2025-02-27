from flask import Flask, request, jsonify, render_template
import requests
import traceback  # Import traceback to print detailed errors

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
        data = request.get_json()

        # Log received data
        print("Received data:", data)

        # Ensure all parameters are present
        if 'param1' not in data or 'param2' not in data or 'param3' not in data:
            print("Error: Missing input parameters")
            return jsonify({'error': 'Missing input parameters'}), 400

        # Convert input to float values (ensure they are numeric)
        try:
            param1 = float(data['param1'])
            param2 = float(data['param2'])
            param3 = float(data['param3'])
        except ValueError:
            print("Error: Invalid input type")
            return jsonify({'error': 'Invalid input: all parameters must be numbers'}), 400

        # Prepare request data
        input_data = {"data": [[param1, param2, param3]]}

        # Log request before sending
        print("Sending request to Azure ML:", input_data)

        # Send request to Azure ML
        response = requests.post(AZURE_ML_ENDPOINT, json=input_data, headers=headers)

        # Log Azure response
        print("Azure ML Response:", response.status_code, response.text)

        # Handle Azure response
        if response.status_code == 200:
            prediction = response.json()
            return jsonify({"prediction": prediction})
        else:
            return jsonify({
                'error': f'Azure API request failed with status {response.status_code}',
                'details': response.text
            }), response.status_code

    except Exception as e:
        print("Internal Server Error:", str(e))
        traceback.print_exc()  # Print full error traceback in the console
        return jsonify({'error': 'Internal Server Error', 'details': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
