"""URL discovery from sitemaps and page links."""

import httpx
import asyncio
import xml.etree.ElementTree as ET
import logging
from urllib.parse import urljoin, urlparse

logger = logging.getLogger(__name__)


async def fetch_sitemap_urls(base_url: str, limit: int = 1000) -> list[str]:
    sitemap_url = urljoin(base_url, "/sitemap.xml")

    async with httpx.AsyncClient(timeout=15.0, follow_redirects=True) as client:
        try:
            response = await client.get(sitemap_url)
            if response.status_code != 200:
                logger.info(f"No sitemap found at {sitemap_url}")
                return []

            root = ET.fromstring(response.text)
            ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}

            urls = []
            for url_elem in root.findall(".//sm:url/sm:loc", ns):
                if url_elem.text:
                    urls.append(url_elem.text)
                if len(urls) >= limit:
                    break

            logger.info(f"Found {len(urls)} URLs in sitemap")
            return urls

        except Exception as e:
            logger.error(f"Sitemap fetch failed: {e}")
            return []


def filter_urls_by_pattern(urls: list[str], patterns: list[str]) -> list[str]:
    import re
    compiled = [re.compile(p) for p in patterns]
    return [url for url in urls if any(p.search(url) for p in compiled)]
