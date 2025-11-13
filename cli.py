"""CLI for data-scraper-toolkit."""

import asyncio
import click
from rich.console import Console
from rich.table import Table

from scraper import Scraper
from extractors.ai_extractor import AIExtractor
from extractors.css_extractor import CSSExtractor
from exporters.csv_exporter import CSVExporter
from exporters.json_exporter import JSONExporter
from config_parser import load_config

console = Console()


@click.group()
def cli():
    """Data Scraper Toolkit - AI-powered web scraping."""
    pass


@cli.command()
@click.argument("url")
@click.option("--prompt", "-p", required=True, help="Extraction prompt")
@click.option("--output", "-o", default=None, help="Output file")
def extract(url: str, prompt: str, output: str | None):
    """Extract data from a single URL using AI."""
    scraper = Scraper()
    extractor = AIExtractor()

    console.print(f"Fetching: {url}")
    html = asyncio.run(scraper.fetch(url))

    console.print("Extracting data...")
    data = extractor.extract(html, prompt)

    if output:
        if output.endswith(".csv"):
            CSVExporter().export(data if isinstance(data, list) else [data], output)
        else:
            JSONExporter().export(data if isinstance(data, list) else [data], output)
        console.print(f"[green]Saved to {output}[/green]")
    else:
        console.print_json(data=data)


@cli.command()
@click.argument("config_file")
def run(config_file: str):
    """Run a scraping configuration."""
    config = load_config(config_file)
    console.print(f"[bold]Running: {config.name}[/bold]")

    scraper = Scraper()
    ai_extractor = AIExtractor()

    for target in config.targets:
        console.print(f"\nTarget: {target.name}")

        urls = [target.url]
        if target.pagination:
            start = target.pagination.get("start", 1)
            end = target.pagination.get("end", 1)
            param = target.pagination.get("param", "page")
            urls = [target.url.replace(f"{{{{{param}}}}}", str(i)) for i in range(start, end + 1)]

        console.print(f"  Fetching {len(urls)} pages...")
        pages = asyncio.run(scraper.fetch_many(urls))

        all_data = []
        for html in pages:
            if not html:
                continue
            data = ai_extractor.extract(html, target.extraction["prompt"])
            if isinstance(data, list):
                all_data.extend(data)
            else:
                all_data.append(data)

        console.print(f"  Extracted {len(all_data)} records")

        output_path = target.output["file"]
        fmt = target.output.get("format", "json")
        if fmt == "csv":
            CSVExporter().export(all_data, output_path)
        else:
            JSONExporter().export(all_data, output_path)
        console.print(f"  [green]Saved to {output_path}[/green]")


@cli.command(name="list")
def list_configs():
    """List available scraping configs."""
    from pathlib import Path
    configs_dir = Path("configs")
    if not configs_dir.exists():
        console.print("No configs directory found")
        return

    table = Table(title="Available Configs")
    table.add_column("File")
    table.add_column("Name")

    for f in sorted(configs_dir.glob("*.yaml")):
        try:
            config = load_config(str(f))
            table.add_row(f.name, config.name)
        except Exception:
            table.add_row(f.name, "[red]Invalid[/red]")

    console.print(table)


if __name__ == "__main__":
    cli()
