"""CSS selector based data extraction."""

from bs4 import BeautifulSoup


class CSSExtractor:
    def extract(self, html: str, selectors: dict[str, str]) -> list[dict]:
        soup = BeautifulSoup(html, "lxml")
        results = []

        # Find the repeating container
        first_selector = list(selectors.values())[0]
        elements = soup.select(first_selector)

        if not elements:
            return results

        for element in elements:
            row = {}
            for field_name, selector in selectors.items():
                found = element.select_one(selector) if element != soup else soup.select_one(selector)
                row[field_name] = found.get_text(strip=True) if found else None
            results.append(row)

        return results
