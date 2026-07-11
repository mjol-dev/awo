from collections import defaultdict
from typing import Any, Dict, List, Optional

from .logio import load_logs

METRIC_KEYS = (
    "cpu_percent",
    "memory_percent",
    "disk_usage_percent",
    "gpu_utilization",
    "gpu_memory_used_mb",
)

def _stats(values: List[float]) -> Dict[str, float]:
    return {
        "min": min(values),
        "max": max(values),
        "avg": sum(values) / len(values),
    }

def analyze_logs(tag: Optional[str] = None) -> None:
    try:
        logs = load_logs()
    except FileNotFoundError:
        print("No log file found yet.")
        return
    
    if tag is not None:
        logs = [entry for entry in logs if entry.get("tag") == tag]

    if not logs:
        label = f" for tag '{tag}'" if tag is not None else ""
        print(f"No log entries{label}.")
        return

    print(f"Total entries: {len(logs)}")

    by_tag: Dict[Any, int] = defaultdict(int)
    for entry in logs:
        by_tag[entry.get("tag", "unknown")] += 1
    print("Entries by tag:")
    for name, count in sorted(by_tag.items(), key=lambda item: str(item[0])):
        print(f"  {name}: {count}")

    print("Metric summary:")
    for key in METRIC_KEYS:
        values = [float(entry[key]) for entry in logs if isinstance(entry.get(key), (int, float))]
        if not values:
            continue
        summary = _stats(values)
        print(
            f"  {key}: min={summary['min']:.2f}  "
            f"avg={summary['avg']:.2f}  max={summary['max']:.2f}"
        )