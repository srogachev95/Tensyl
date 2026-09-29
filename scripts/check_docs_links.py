"""Check built HTML links and the handbook's previously published heading URLs."""

from __future__ import annotations

import argparse
import json
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


class Page(HTMLParser):
    def __init__(self, text: str) -> None:
        super().__init__()
        self.ids: set[str] = set()
        self.links: list[str] = []
        self.feed(text)

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if identifier := values.get("id"):
            self.ids.add(identifier)
        if tag == "a" and (href := values.get("href")):
            self.links.append(href)


def check(site: Path) -> list[str]:
    site = site.resolve()
    pages = {path: Page(path.read_text()) for path in site.rglob("*.html")}
    errors = []
    baseline = Path(__file__).resolve().parents[1] / "tests/data/docs_public_anchors.json"
    for relative, anchors in json.loads(baseline.read_text()).items():
        page = pages.get(site / relative)
        if page is None:
            errors.append(f"Removed public page: {relative}")
        else:
            errors.extend(
                f"Removed public anchor: {relative}#{anchor}"
                for anchor in anchors
                if anchor not in page.ids
            )
    for path, page in pages.items():
        for href in page.links:
            url = urlsplit(href)
            if url.scheme or url.netloc or href.startswith("/"):
                continue
            target = (path.parent / unquote(url.path)).resolve() if url.path else path
            if target.is_dir():
                target /= "index.html"
            if not target.exists():
                errors.append(f"{path.relative_to(site)}: missing {href}")
            elif (
                url.fragment and target in pages and unquote(url.fragment) not in pages[target].ids
            ):
                errors.append(f"{path.relative_to(site)}: missing anchor {href}")
    return errors


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("site", type=Path)
    failures = check(parser.parse_args().site)
    for failure in failures:
        print(failure)
    if failures:
        raise SystemExit(1)
    print("Local links and preserved public anchors passed.")
