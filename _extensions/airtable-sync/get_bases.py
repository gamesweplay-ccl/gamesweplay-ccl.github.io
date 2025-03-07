from pyairtable import Api

api_key = "patSoZ4kfvUsjRRrF.761267e621dd2cd92550c59807adbbb50ec764057a3d370a29965142003bc936"
api = Api(api_key)

try:
    # Get metadata about the API key
    print("Attempting to list available bases...")
    workspace = api.get_workspace()
    print(f"Workspace info: {workspace}")
except Exception as e:
    print(f"Error: {str(e)}")
