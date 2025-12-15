"""Scraping run report generation."""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class ScrapeResult:
    url: str
    status: str  # "success", "error", "skipped"
    records_extracted: int = 0
    error_message: str = ""
    duration_ms: int = 0


@dataclass
class ScrapeReport:
    config_name: str
    started_at: datetime = field(default_factory=datetime.now)
    results: list[ScrapeResult] = field(default_factory=list)

    @property
    def total_urls(self) -> int:
        return len(self.results)

    @property
    def successful(self) -> int:
        return sum(1 for r in self.results if r.status == "success")

    @property
    def failed(self) -> int:
        return sum(1 for r in self.results if r.status == "error")

    @property
    def total_records(self) -> int:
        return sum(r.records_extracted for r in self.results)

    def summary(self) -> str:
        elapsed = (datetime.now() - self.started_at).total_seconds()
        return f"""Scrape Report: {self.config_name}
  URLs: {self.successful}/{self.total_urls} successful
  Records: {self.total_records} extracted
  Errors: {self.failed}
  Duration: {elapsed:.1f}s"""
