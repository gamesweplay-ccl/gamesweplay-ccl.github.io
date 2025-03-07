import requests
import json

api_key = "patSoZ4kfvUsjRRrF.761267e621dd2cd92550c59807adbbb50ec764057a3d370a29965142003bc936"
base_id = "appz6D97kDKNboXOW"
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
