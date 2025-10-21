"""Parse YAML scraping configurations."""

import yaml
from pathlib import Path
from pydantic import BaseModel
from typing import Optional


class ScrapeTarget(BaseModel):
    name: str
    url: str
    pagination: Optional[dict] = None
    extraction: dict
    output: dict


class ScrapeConfig(BaseModel):
    name: str
    targets: list[ScrapeTarget]
    settings: dict = {}


def load_config(path: str) -> ScrapeConfig:
    with open(path) as f:
        data = yaml.safe_load(f)
    return ScrapeConfig(**data)
