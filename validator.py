"""Validate and clean extracted data."""

import re
import logging

logger = logging.getLogger(__name__)


class DataValidator:
    def validate_email(self, value: str) -> bool:
        return bool(re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", value))

    def validate_url(self, value: str) -> bool:
        return bool(re.match(r"^https?://[\w.-]+", value))

    def validate_phone(self, value: str) -> bool:
        cleaned = re.sub(r"[^\d+]", "", value)
        return len(cleaned) >= 7

    def clean_text(self, value: str) -> str:
        value = re.sub(r"\s+", " ", value)
        return value.strip()

    def validate_records(self, records: list[dict], schema: dict) -> list[dict]:
        valid = []
        for record in records:
            is_valid = True
            for field, rules in schema.items():
                value = record.get(field)
                if rules.get("required") and not value:
                    is_valid = False
                    break
                if value and rules.get("type") == "email" and not self.validate_email(str(value)):
                    record[field] = None
            if is_valid:
                valid.append(record)
        logger.info(f"Validated {len(valid)}/{len(records)} records")
        return valid
