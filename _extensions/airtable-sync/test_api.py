import requests
import json

api_key = "patSoZ4kfvUsjRRrF.761267e621dd2cd92550c59807adbbb50ec764057a3d370a29965142003bc936"
base_id = "appGrYZCYxHs5mRxI"
table_name = "Games"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

# Try to list bases first
try:
    print("Testing API access...")
    response = requests.get(
        f"https://api.airtable.com/v0/meta/bases",
        headers=headers
    )
    print(f"Status: {response.status_code}")
    print("Response:", json.dumps(response.json(), indent=2))
except Exception as e:
    print(f"Error: {str(e)}")
