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
