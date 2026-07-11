from .logio import load_logs
from datetime import datetime
from typing import Any, Optional
import matplotlib.pyplot as plt

def visualize(tag: Optional[str] = None, output: str = "awo_plot.png") -> None:
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
    
    def _as_unix_seconds(value: Any) -> Optional[float]:
        if isinstance(value, (int, float)):
            return float(value)
        if isinstance(value, str):
            try:
                return datetime.fromisoformat(value).timestamp()
            except ValueError:
                return None
        return None

    points = []
    for entry in logs:
        t = _as_unix_seconds(entry.get("timestamp"))
        cpu = entry.get("cpu_percent")
        mem = entry.get("memory_percent")
        if t is None:
            continue
        if not isinstance(cpu, (int, float)) or not isinstance(mem, (int, float)):
            continue
        points.append((t, float(cpu), float(mem)))
    if not points:
        print("No plottable CPU/memory samples.")
        return

    points.sort(key=lambda p: p[0])

    t0 = points[0][0]
    elapsed = [t - t0 for t, _, _ in points]
    cpu = [c for _, c, _ in points]
    memory = [m for _, _, m in points]

    plt.figure()
    plt.plot(elapsed, cpu, label="CPU %")
    plt.plot(elapsed, memory, label="Memory %")
    plt.xlabel("Seconds since start")
    plt.ylabel("Percent")
    plt.title("AWO metrics")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output)
    plt.close()
    print(f"Wrote {output}")