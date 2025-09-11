"""Core scraping engine."""

import httpx
import asyncio
import logging
from fake_useragent import UserAgent
from config import Config
from rate_limiter import RateLimiter

logger = logging.getLogger(__name__)


class Scraper:
    def __init__(self):
        self.ua = UserAgent() if Config.USER_AGENT_ROTATE else None
        self.rate_limiter = RateLimiter(Config.RATE_LIMIT)
        self.proxy = Config.PROXY_URL

    def _get_headers(self) -> dict:
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
        }
        if self.ua:
            headers["User-Agent"] = self.ua.random
        return headers

    async def fetch(self, url: str) -> str:
        await self.rate_limiter.acquire()

        async with httpx.AsyncClient(
            proxies=self.proxy,
            timeout=30.0,
            follow_redirects=True,
        ) as client:
            response = await client.get(url, headers=self._get_headers())
            response.raise_for_status()
            return response.text

    async def fetch_many(self, urls: list[str]) -> list[str]:
        semaphore = asyncio.Semaphore(Config.MAX_CONCURRENT)

        async def fetch_with_sem(url: str) -> str:
            async with semaphore:
                try:
                    return await self.fetch(url)
                except Exception as e:
                    logger.error(f"Failed to fetch {url}: {e}")
                    return ""

        tasks = [fetch_with_sem(url) for url in urls]
        return await asyncio.gather(*tasks)
