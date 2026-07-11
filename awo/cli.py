import click
import time
import datetime
from .collector import collect_all_metrics
from .logger import log_metrics
from .analyzer import analyze_logs

@click.group()
def cli():
    pass

@cli.command()
@click.option("--tag", default="default", help="Tag for the logging session")
@click.option("--interval", default=5, help="Polling interval in seconds")
def start(tag, interval):
    """Start collecting metrics."""
    click.echo(f"Starting observability with tag: {tag}")
    try:
        while True:
            metrics = collect_all_metrics()
            log_metrics(metrics, tag=tag)
            click.echo(f"Logged metrics at {datetime.datetime.now()}")
            time.sleep(interval)
    except KeyboardInterrupt:
        click.echo("\nStopped by user.")


@cli.command()
@click.option("--tag", default=None, help="Filter by tag")
def analyze(tag):
    """Analyze collected metrics."""
    analyze_logs(tag)

if __name__ == "__main__":
    cli()
