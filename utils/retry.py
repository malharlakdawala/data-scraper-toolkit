"""Retry utilities for scraping operations."""

import asyncio
import functools
import logging
from typing import Callable, TypeVar

logger = logging.getLogger(__name__)
T = TypeVar("T")


def retry_async(max_retries: int = 3, base_delay: float = 1.0, max_delay: float = 30.0):
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(max_retries + 1):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_retries:
                        delay = min(base_delay * (2 ** attempt), max_delay)
                        logger.warning(f"Attempt {attempt + 1} failed: {e}. Retrying in {delay:.1f}s")
                        await asyncio.sleep(delay)
            raise last_exception
        return wrapper
    return decorator
