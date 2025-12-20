"""HTTP response caching for repeated requests."""

import os
import json
import hashlib
from pathlib import Path


class ResponseCache:
    def __init__(self, cache_dir: str = ".scrape_cache"):
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)

    def _key(self, url: str) -> str:
        return hashlib.md5(url.encode()).hexdigest()

    def get(self, url: str) -> str | None:
        path = Path(self.cache_dir) / f"{self._key(url)}.html"
        if path.exists():
            return path.read_text(encoding="utf-8")
        return None

    def set(self, url: str, content: str):
        path = Path(self.cache_dir) / f"{self._key(url)}.html"
        path.write_text(content, encoding="utf-8")

    def clear(self):
        for f in Path(self.cache_dir).glob("*.html"):
            f.unlink()
