import requests
import json

# API endpoint URL
url = "http://127.0.0.1:5000/get-mythical-creature"

# Data to be sent in the POST request (birth month and gender)
data = {
    "birth_month": 5,
    "gender": "female"
}

# Headers to specify JSON content
headers = {
    "Content-Type": "application/json"
}

# Make the POST request
response = requests.post(url, data=json.dumps(data), headers=headers)

# Print the response from the server
if response.status_code == 200:
    print("Response from API:", response.json())
else:
    print(f"Failed to get a response. Status code: {response.status_code}")
