import json
from collections import defaultdict

def analyze_logs():
    """Basic log analysis."""
    try:
        with open("awo_log.jsonl", "r") as f:
            logs = [json.loads(line) for line in f]
        print(f"Total entries: {len(logs)}")
    except FileNotFoundError:
        print("No log file found yet.")
