"""Deduplicate scraped records."""

import hashlib
import json
import logging

logger = logging.getLogger(__name__)


def deduplicate(records: list[dict], key_fields: list[str] | None = None) -> list[dict]:
    seen = set()
    unique = []

    for record in records:
        if key_fields:
            key_data = {k: record.get(k) for k in key_fields}
        else:
            key_data = record

        key = hashlib.md5(json.dumps(key_data, sort_keys=True).encode()).hexdigest()

        if key not in seen:
            seen.add(key)
            unique.append(record)

    removed = len(records) - len(unique)
    if removed:
        logger.info(f"Removed {removed} duplicate records")
    return unique
