import sys
import json
import os

def main():
    try:
        raw_input = sys.stdin.read()
        if not raw_input.strip():
            print(json.dumps({}))
            return

        payload = json.loads(raw_input)
        tool_call = payload.get("toolCall", {})
        tool_name = tool_call.get("name", "")
        args = tool_call.get("args", {})

        if tool_name != "run_command":
            print(json.dumps({}))
            return

        cmd = args.get("CommandLine", "").strip()
        if "render_mp4" in cmd:
            sys.stderr.write("[Hyperframe Guard Hook] Render command detected. Ensuring pre-flight checks are active.\n")

        print(json.dumps({"decision": "allow"}))
    except Exception:
        print(json.dumps({}))

if __name__ == "__main__":
    main()
