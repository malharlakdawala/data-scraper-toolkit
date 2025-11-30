"""Core scraping engine."""

import httpx
import asyncio
import logging
from fake_useragent import UserAgent
from config import Config
from rate_limiter import RateLimiter
from proxy_manager import ProxyManager

logger = logging.getLogger(__name__)


class Scraper:
    def __init__(self, proxy_file: str | None = None):
        self.ua = UserAgent() if Config.USER_AGENT_ROTATE else None
        self.rate_limiter = RateLimiter(Config.RATE_LIMIT)
        self.proxy_manager = ProxyManager(proxy_file)
        self._client: httpx.AsyncClient | None = None

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

    async def _get_client(self) -> httpx.AsyncClient:
        if self._client is None or self._client.is_closed:
            proxy = self.proxy_manager.get_proxy() or Config.PROXY_URL
            self._client = httpx.AsyncClient(
                proxies=proxy,
                timeout=30.0,
                follow_redirects=True,
            )
        return self._client

    async def fetch(self, url: str, retries: int = 3) -> str:
        await self.rate_limiter.acquire()

        for attempt in range(retries):
            try:
                client = await self._get_client()
                response = await client.get(url, headers=self._get_headers())
                response.raise_for_status()
                return response.text
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 429:
                    wait = 2 ** (attempt + 1)
                    logger.warning(f"Rate limited on {url}, waiting {wait}s")
                    await asyncio.sleep(wait)
                elif e.response.status_code >= 500:
                    logger.warning(f"Server error {e.response.status_code} on {url}, retrying...")
                    await asyncio.sleep(1)
                else:
                    raise
            except httpx.RequestError as e:
                logger.error(f"Request failed for {url}: {e}")
                if attempt < retries - 1:
                    await asyncio.sleep(1)

        raise RuntimeError(f"Failed to fetch {url} after {retries} retries")

    async def fetch_many(self, urls: list[str]) -> list[str]:
        semaphore = asyncio.Semaphore(Config.MAX_CONCURRENT)

        async def fetch_with_sem(url: str) -> str:
            async with semaphore:
                try:
                    return await self.fetch(url)
                except Exception as e:
                    logger.error(f"Failed to fetch {url}: {e}")
                    return ""

        return await asyncio.gather(*[fetch_with_sem(url) for url in urls])

    async def close(self):
        if self._client and not self._client.is_closed:
            await self._client.aclose()
