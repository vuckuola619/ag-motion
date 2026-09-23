import urllib.request
import json
import time
import sys

url = "http://127.0.0.1:20128/v1/images/generations"
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer sk-c4f2444795b190b3-kzvd4h-ea839762",
    "User-Agent": "BangMotion/1.0"
}
payload = {
    "model": "cx/gpt-5.5-image",
    "prompt": "vintage yellowed archival paper texture background",
    "n": 1,
    "size": "1024x1024",
    "response_format": "b64_json"
}

data = json.dumps(payload).encode("utf-8")
req = urllib.request.Request(url, data=data, headers=headers)
print("Sending request to 9router...", flush=True)
t0 = time.time()
try:
    with urllib.request.urlopen(req, timeout=120) as resp:
        print(f"Status code: {resp.status} in {time.time() - t0:.1f}s", flush=True)
        res_data = json.loads(resp.read().decode("utf-8"))
        print("Data entries:", len(res_data.get("data", [])), flush=True)
        if res_data.get("data"):
            b64 = res_data["data"][0]["b64_json"]
            print("b64 length:", len(b64), flush=True)
except Exception as e:
    print(f"Error after {time.time() - t0:.1f}s:", type(e), e, flush=True)
