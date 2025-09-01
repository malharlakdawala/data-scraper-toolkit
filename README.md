# data-scraper-toolkit

Configurable web scraping toolkit with anti-detection, proxy rotation, and AI-powered data extraction.

## Features

- **YAML Configs** - Define scraping targets in YAML
- **AI Extraction** - Use Claude to extract structured data from HTML
- **Proxy Rotation** - Built-in proxy management
- **Rate Limiting** - Configurable request throttling
- **Anti-Detection** - User-agent rotation, request delays
- **Export** - CSV and JSON output

## Setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

## Usage

```bash
# Run a scraping config
python cli.py run configs/example.yaml

# Extract data from a single URL
python cli.py extract "https://example.com" --prompt "Extract company name and description"

# List available configs
python cli.py list
```
