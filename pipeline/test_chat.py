import urllib.request
import json

url = 'http://127.0.0.1:20128/v1/chat/completions'
headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer sk-c4f2444795b190b3-kzvd4h-ea839762'}
data = {'model': 'cx/gpt-5.5', 'messages': [{'role': 'user', 'content': 'ping'}], 'max_tokens': 5}
req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers=headers)
try:
    with urllib.request.urlopen(req, timeout=10) as r:
        print('Chat status:', r.status)
        print(r.read().decode('utf-8')[:100])
except Exception as e:
    print('Chat error:', e)
