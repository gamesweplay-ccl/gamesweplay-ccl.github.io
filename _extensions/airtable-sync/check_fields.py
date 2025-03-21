from pyairtable import Api
import json
from dotenv import load_dotenv
import os


load_dotenv()
api_key = os.getenv("AIRTABLE_API_KEY")
base_id = os.getenv("AIRTABLE_BASE_ID")
table_name = "Games"

api = Api(api_key)
table = api.table(base_id, table_name)

# Get all records to see all possible fields
records = table.all()
all_fields = set()
for record in records:
    all_fields.update(record['fields'].keys())

print("All available fields:")
for field in sorted(all_fields):
    print(f"- {field}")

print("\nSample records:")
for record in records[:3]:  # Show first 3 records
    print(f"\n{record['fields']['Game Name']}:")
    print(json.dumps(record['fields'], indent=2))
