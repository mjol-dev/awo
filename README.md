# AI Workload Observability Tool (AWO)

A lightweight CLI for collecting system (and optional NVIDIA GPU) metrics during AI workloads, then summarizing and plotting a run.

## Pipeline

`start` → `analyze` → `visualize`

Metrics are appended to `awo_log.jsonl` in the current working directory.

## Setup
```bash
pip install -e .
- Development 
pip install -e ".[dev]"
python -m pytest -q
```

## Usage
```bash
# Collect (Ctrl+C to stop)
awo start --tag my-experiment
awo start --tag my-experiment --interval 5
# Summarize
awo analyze
awo analyze --tag my-experiment
# Plot CPU and memory vs seconds since start
awo visualize
awo visualize --tag my-experiment --output my_run.png
```

## Commands 
- `start` - Poll CPU, memory, disk, and GPU (if available); append JSONL rows tagged with `--tag`

- `analyze` - Print entry counts and min/avg/max for numeric metrics; optional `--tag` filter

- `visualize` - Write a PNG of CPU % and memory % vs elapsed seconds; `--tag` and `--output` optional

## Notes 
- Visualization uses elapsed time (seconds since the first sample), not calendar dates, so short runs plot clearly.
- Default log file: `awo_log.jsonl`. Default plot: `awo_plot.png`. 
- Each JSONL row is an **envelope** plus **metrics**: `timestamp` (ISO, set by the logger) and `tag`, then fields like `cpu_percent`, `memory_percent`, `disk_usage_percent`, and optional GPU keys. The collector does not set `timestamp`.
- `--interval` is the sleep between samples; CPU is sampled without an extra blocking 1s wait so the flag matches the poll cadence.