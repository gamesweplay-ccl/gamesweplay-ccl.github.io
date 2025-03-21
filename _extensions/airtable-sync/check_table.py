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

# Get table schema and records
url = f"https://api.airtable.com/v0/{base_id}/{table_name}"
response = requests.get(url, headers=headers)
data = response.json()

if 'records' in data:
    all_fields = set()
    for record in data['records']:
        all_fields.update(record['fields'].keys())
    
    print("All fields in table:")
    for field in sorted(all_fields):
        print(f"- {field}")
    
    print("\nFirst few records with all fields:")
    for record in data['records'][:3]:
        print(f"\n{record['fields'].get('Game Name', 'Unknown')}:")
        print(json.dumps(record['fields'], indent=2))
