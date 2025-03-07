import requests
import json

api_key = "patSoZ4kfvUsjRRrF.761267e621dd2cd92550c59807adbbb50ec764057a3d370a29965142003bc936"
base_id = "appz6D97kDKNboXOW"
table_name = "Games"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

# Get table metadata including views
url = f"https://api.airtable.com/v0/meta/bases/{base_id}/tables"
response = requests.get(url, headers=headers)
data = response.json()

if 'tables' in data:
    for table in data['tables']:
        if table['name'] == table_name:
            print(f"Fields in {table_name} table:")
            for field in table['fields']:
                print(f"- {field['name']} ({field['type']})")
            
            print("\nViews:")
            for view in table['views']:
                print(f"- {view['name']}")
