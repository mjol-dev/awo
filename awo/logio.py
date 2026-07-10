import json
from typing import Any, Dict, List, Optional

from .config import LOG_FILE


def load_logs(path: Optional[str] = None) -> List[Dict[str, Any]]:
    """Load JSONL metrics. Raises FileNotFoundError if missing."""
    log_path = path or LOG_FILE
    with open(log_path, "r") as f:
        return [json.loads(line) for line in f if line.strip()]