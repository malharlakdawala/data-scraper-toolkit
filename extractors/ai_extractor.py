"""AI-powered data extraction using Claude."""

import anthropic
import json
import re
import logging
from config import Config

logger = logging.getLogger(__name__)


class AIExtractor:
    SYSTEM_PROMPT = """You are a data extraction assistant. Given HTML content and an extraction prompt,
extract the requested data and return it as a JSON object or JSON array.
Only return valid JSON, no markdown or explanation."""

    def __init__(self):
        self.client = anthropic.Anthropic(api_key=Config.ANTHROPIC_API_KEY)

    def extract(self, html: str, prompt: str) -> dict | list:
        # Truncate HTML to avoid token limits
        if len(html) > 50000:
            html = html[:50000] + "\n... (truncated)"

        response = self.client.messages.create(
            model=Config.MODEL,
            max_tokens=2048,
            system=self.SYSTEM_PROMPT,
            messages=[{
                "role": "user",
                "content": f"Extract data from this HTML based on the following instruction:\n\nInstruction: {prompt}\n\nHTML:\n{html}",
            }],
        )
        text = response.content[0].text

        try:
            json_match = re.search(r"```(?:json)?\s*(.+?)```", text, re.DOTALL)
            raw = json_match.group(1) if json_match else text

            start = raw.find("[") if raw.find("[") < raw.find("{") or raw.find("{") == -1 else raw.find("{")
            if start == -1:
                start = 0
            return json.loads(raw[start:])
        except json.JSONDecodeError:
            logger.warning("Failed to parse AI extraction result as JSON")
            return {"raw_text": text}
