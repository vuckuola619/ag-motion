import urllib.request
import json
import base64
import os

url = "http://127.0.0.1:20128/v1/images/generations"
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer sk-c4f2444795b190b3-kzvd4h-ea839762"
}
payload = {
    "model": "cx/gpt-5.5-image",
    "prompt": "Soviet military dosimeter DP-5V with handheld Geiger probe, vintage military olive drab equipment, transparent background, isolated icon cutout, no background shadows",
    "n": 1,
    "size": "1024x1024"
}
req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers)
print("Sending test generation to 9router cx/gpt-5.5-image...")
try:
    with urllib.request.urlopen(req, timeout=120) as res:
        data = json.loads(res.read().decode("utf-8"))
        print("Response keys:", list(data.keys()))
        if "data" in data and len(data["data"]) > 0:
            first = data["data"][0]
            if "b64_json" in first:
                print("Got b64_json, length:", len(first["b64_json"]))
            elif "url" in first:
                print("Got url:", first["url"][:50])
except Exception as e:
    print("Error:", e)
