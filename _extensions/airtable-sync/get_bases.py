from pyairtable import Api
from dotenv import load_dotenv
import os


load_dotenv()
api_key = os.getenv("AIRTABLE_API_KEY")
api = Api(api_key)

try:
    # Get metadata about the API key
    print("Attempting to list available bases...")
    workspace = api.get_workspace()
    print(f"Workspace info: {workspace}")
except Exception as e:
    print(f"Error: {str(e)}")
