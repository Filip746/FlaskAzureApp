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
        print("📩 Received Data from Frontend:", data)

        # Ensure all parameters exist
        if not data or 'param1' not in data or 'param2' not in data or 'param3' not in data:
            print("❌ Missing input parameters")
            return jsonify({'error': 'Missing input parameters'}), 400

        # Convert to numbers
        try:
            param1 = float(data['param1'])
            param2 = float(data['param2'])
            param3 = float(data['param3'])
        except ValueError:
            print("❌ Invalid input type (non-numeric value detected)")
            return jsonify({'error': 'Invalid input: all parameters must be numbers'}), 400

        # Prepare request for Azure ML
        input_data = {"data": [[param1, param2, param3]]}
        print("📤 Sending Request to Azure ML:", input_data)

        # Call Azure ML API
        response = requests.post(AZURE_ML_ENDPOINT, json=input_data, headers=headers)
        print("📨 Azure ML Response:", response.status_code, response.text)

        # Handle Azure ML response
        if response.status_code == 200:
            prediction = response.json()
            print("✅ Prediction Success:", prediction)
            return jsonify({"prediction": prediction})
        else:
            print("❌ Azure ML API Failed:", response.status_code, response.text)
            return jsonify({
                'error': f'Azure API request failed with status {response.status_code}',
                'details': response.text
            }), response.status_code

    except Exception as e:
        print("❌ Internal Server Error:", str(e))
        import traceback
        traceback.print_exc()  # Print detailed error trace
        return jsonify({'error': 'Internal Server Error', 'details': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
