import sys, json
try:
    sys.stdin.read()
    print(json.dumps({"decision": "allow"}))
except Exception:
    print(json.dumps({}))
