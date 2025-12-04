"""Clean HTML for better AI extraction results."""

import re
from bs4 import BeautifulSoup, Comment


def clean_html(html: str, keep_structure: bool = True) -> str:
    soup = BeautifulSoup(html, "lxml")

    # Remove script, style, and other non-content tags
    for tag in soup(["script", "style", "nav", "footer", "header", "aside", "iframe", "noscript"]):
        tag.decompose()

    # Remove HTML comments
    for comment in soup.find_all(string=lambda t: isinstance(t, Comment)):
        comment.extract()

    # Remove hidden elements
    for tag in soup.find_all(attrs={"style": re.compile(r"display:\s*none")}):
        tag.decompose()
    for tag in soup.find_all(attrs={"hidden": True}):
        tag.decompose()

    if keep_structure:
        # Keep meaningful tags, remove attributes
        for tag in soup.find_all(True):
            allowed_attrs = {"href", "src", "alt", "title"}
            attrs = dict(tag.attrs)
            for attr in attrs:
                if attr not in allowed_attrs:
                    del tag[attr]
        return str(soup)
    else:
        return soup.get_text(separator="\n", strip=True)
