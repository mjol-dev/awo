from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

from .logio import load_logs
import matplotlib.pyplot as plt


def _as_unix_seconds(value: Any) -> Optional[float]:
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        try:
            return datetime.fromisoformat(value).timestamp()
        except ValueError:
            return None
    return None


def _build_plot_series(
    logs: List[Dict[str, Any]],
) -> Optional[Tuple[List[float], List[float], List[float]]]:
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
        return None

    points.sort(key=lambda p: p[0])
    t0 = points[0][0]
    elapsed = [t - t0 for t, _, _ in points]
    cpu_vals = [c for _, c, _ in points]
    memory_vals = [m for _, _, m in points]
    return elapsed, cpu_vals, memory_vals


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

    series = _build_plot_series(logs)
    if series is None:
        print("No plottable CPU/memory samples.")
        return

    elapsed, cpu, memory = series

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