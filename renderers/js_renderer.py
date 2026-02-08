"""JavaScript rendering for dynamic pages."""

import asyncio
import logging

logger = logging.getLogger(__name__)


class JSRenderer:
    """Render JavaScript-heavy pages using playwright."""

    def __init__(self):
        self._browser = None

    async def render(self, url: str, wait_for: str | None = None, timeout: int = 30000) -> str:
        try:
            from playwright.async_api import async_playwright

            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page()

                await page.goto(url, timeout=timeout, wait_until="networkidle")

                if wait_for:
                    await page.wait_for_selector(wait_for, timeout=10000)

                content = await page.content()
                await browser.close()
                return content

        except ImportError:
            logger.warning("playwright not installed, falling back to httpx")
            import httpx
            async with httpx.AsyncClient() as client:
                resp = await client.get(url, timeout=timeout / 1000)
                return resp.text
        except Exception as e:
            logger.error(f"JS rendering failed for {url}: {e}")
            raise
