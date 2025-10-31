"""JSON data export."""

import json
import os


class JSONExporter:
    def export(self, data: list[dict], output_path: str, indent: int = 2):
        os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=indent, ensure_ascii=False)
