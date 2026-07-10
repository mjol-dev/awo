import json
import datetime

LOG_FILE = "awo_log.jsonl"

def log_metrics(metrics, tag="default"):
    """Log metrics to file."""
    entry = {
        "timestamp": datetime.datetime.now().isoformat(),
        "tag": tag,
        **metrics
    }
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(entry) + "\n")
