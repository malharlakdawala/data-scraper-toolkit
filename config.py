"""Configuration."""

import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    PROXY_URL = os.getenv("PROXY_URL")
    MAX_CONCURRENT = int(os.getenv("MAX_CONCURRENT", "5"))
    RATE_LIMIT = float(os.getenv("RATE_LIMIT", "2"))
    MODEL = os.getenv("MODEL", "claude-sonnet-4-20250514")
    USER_AGENT_ROTATE = os.getenv("USER_AGENT_ROTATE", "true").lower() == "true"
