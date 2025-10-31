"""CSV data export."""

import csv
import os
from typing import Any


class CSVExporter:
    def export(self, data: list[dict], output_path: str):
        if not data:
            return

        os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)

        fieldnames = list(data[0].keys())
        with open(output_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
