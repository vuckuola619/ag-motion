import json
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

creds = Credentials.from_authorized_user_file('token.json')
service = build('drive', 'v3', credentials=creds)

results = service.files().list(
    q="trashed = false and (name contains 'AG-Bang' or name contains 'azorian' or name contains 'episode6')",
    fields='files(id, name, mimeType, modifiedTime)'
).execute()

files = results.get('files', [])
print(f"Total found: {len(files)}")
for f in files:
    print(f"- {f['name']} ({f['mimeType']}) [modified: {f.get('modifiedTime')}]")
