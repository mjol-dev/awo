import json
import datetime
from .config import LOG_FILE

def log_metrics(metrics, tag="default"):
    """Log metrics to file."""
    entry = {
        "timestamp": datetime.datetime.now().isoformat(),
        "tag": tag,
        **metrics
    }
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(entry) + "\n")
