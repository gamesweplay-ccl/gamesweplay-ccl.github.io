import requests
import json
from dotenv import load_dotenv
import os


load_dotenv()
api_key = os.getenv("AIRTABLE_API_KEY")
base_id = os.getenv("AIRTABLE_BASE_ID")
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
