"""Proxy rotation and management."""

import random
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class ProxyManager:
    def __init__(self, proxy_file: str | None = None):
        self.proxies: list[str] = []
        self._index = 0

        if proxy_file and Path(proxy_file).exists():
            self._load_proxies(proxy_file)

    def _load_proxies(self, path: str):
        with open(path) as f:
            self.proxies = [line.strip() for line in f if line.strip() and not line.startswith("#")]
        logger.info(f"Loaded {len(self.proxies)} proxies")

    def get_proxy(self) -> str | None:
        if not self.proxies:
            return None
        proxy = self.proxies[self._index % len(self.proxies)]
        self._index += 1
        return proxy

    def get_random_proxy(self) -> str | None:
        if not self.proxies:
            return None
        return random.choice(self.proxies)

    def remove_proxy(self, proxy: str):
        if proxy in self.proxies:
            self.proxies.remove(proxy)
            logger.info(f"Removed proxy: {proxy} ({len(self.proxies)} remaining)")
