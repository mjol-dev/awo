from .logio import load_logs

def analyze_logs():
    """Basic log analysis."""
    try:
        logs = load_logs()
        print(f"Total entries: {len(logs)}")
    except FileNotFoundError:
        print("No log file found yet.")
