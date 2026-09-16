import json

with open(r"C:\Users\Administrator\.gemini\antigravity\brain\5c73666c-ec9d-4af6-a4dd-abd836770ff8\.system_generated\logs\transcript.jsonl", "r", encoding="utf-8") as f:
    for line in f:
        data = json.loads(line)
        if data.get("type") == "USER_INPUT" and ("metronome" in data.get("content", "").lower() or "nelpon" in data.get("content", "").lower()):
            print(f"USER: {data['content']}")
