from flask import Flask, render_template, request, jsonify
import requests
import json

app = Flask(__name__)

# Azure ML endpoint and API key
endpoint = "http://b73a5ed0-5a44-4896-985e-69680dc267bf.northeurope.azurecontainer.io/score"
api_key = "JqS3yTa93SKn8YYsqPI5bCuYHb9rzK7g"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = {
        "Inputs": {
            "input1": [
                {
                    "Name": request.form['Name'],
                    "Author": request.form['Author'],
                    "User Rating": float(request.form['User Rating']),
                    "Reviews": int(request.form['Reviews']),
                    "Price": int(request.form['Price']),
                    "Year": int(request.form['Year']),
                    "Genre": request.form['Genre'],                    
                }
            ]
        },
        "GlobalParameters": {}
    }

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }

    response = requests.post(endpoint, headers=headers, data=json.dumps(data))
    result = response.json()
    
    print(json.dumps(result, indent=4))

    scored_labels = result['Results']['WebServiceOutput0'][0]['Scored Labels']
    scored_probabilities = result['Results']['WebServiceOutput0'][0]['Scored Probabilities']

    prediction_text = "Dobra knjiga" if scored_labels == 0.9 else "Prosječna knjiga"
    
    return render_template('result.html', prediction=prediction_text, probability=scored_probabilities)


if __name__ == '__main__':
    app.run(debug=True)