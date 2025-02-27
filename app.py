import urllib.request
import json
import os
import ssl

def allowSelfSignedHttps(allowed):
    # bypass the server certificate verification on client side
    if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
        ssl._create_default_https_context = ssl._create_unverified_context

allowSelfSignedHttps(True) # this line is needed if you use self-signed certificate in your scoring service.

# Request data goes here
# The example below assumes JSON formatting which may be updated
# depending on the format your endpoint expects.
# More information can be found here:
# https://docs.microsoft.com/azure/machine-learning/how-to-deploy-advanced-entry-script
data = {"Inputs": {
          "input1": [
            {
              "Name": "10-Day Green Smoothie Cleanse",
              "Author": "JJ Smith",
              "User Rating": 4.7,
              "Reviews": 17350,
              "Price": 8,
              "Year": 2016,
              "Genre": "Non Fiction"
            },
            {
              "Name": "11/22/63: A Novel",
              "Author": "Stephen King",
              "User Rating": 4.6,
              "Reviews": 2052,
              "Price": 22,
              "Year": 2011,
              "Genre": "Fiction"
            },
            {
              "Name": "12 Rules for Life: An Antidote to Chaos",
              "Author": "Jordan B. Peterson",
              "User Rating": 4.7,
              "Reviews": 18979,
              "Price": 15,
              "Year": 2018,
              "Genre": "Non Fiction"
            },
            {
              "Name": "1984 (Signet Classics)",
              "Author": "George Orwell",
              "User Rating": 4.7,
              "Reviews": 21424,
              "Price": 6,
              "Year": 2017,
              "Genre": "Fiction"
            },
            {
              "Name": "5,000 Awesome Facts (About Everything!) (National Geographic Kids)",
              "Author": "National Geographic Kids",
              "User Rating": 4.8,
              "Reviews": 7665,
              "Price": 12,
              "Year": 2019,
              "Genre": "Non Fiction"
            }
          ]
        },
        "GlobalParameters": {

        }}

body = str.encode(json.dumps(data))

url = 'http://b73a5ed0-5a44-4896-985e-69680dc267bf.northeurope.azurecontainer.io/score'
# Replace this with the primary/secondary key, AMLToken, or Microsoft Entra ID token for the endpoint
api_key = 'JqS3yTa93SKn8YYsqPI5bCuYHb9rzK7g'
if not api_key:
    raise Exception("A key should be provided to invoke the endpoint")


headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}

req = urllib.request.Request(url, body, headers)

try:
    response = urllib.request.urlopen(req)

    result = response.read()
    print(result)
except urllib.error.HTTPError as error:
    print("The request failed with status code: " + str(error.code))

    # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
    print(error.info())
    print(error.read().decode("utf8", 'ignore'))