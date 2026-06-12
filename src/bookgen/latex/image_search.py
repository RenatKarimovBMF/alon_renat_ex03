"""Fetch chapter images from the public web (keyless APIs, no bundled files).

Wikimedia Commons is searched first (generic topics, free licenses); the NASA
Image Library is the fallback (rich space imagery, public domain). The HTTP
client is injectable so tests run fully offline with ``httpx.MockTransport``.
"""

from __future__ import annotations

from pathlib import Path

import httpx

_UA = {"User-Agent": "bookgen-ex03/1.0 (university exercise; contact: course submission)"}
_COMMONS = "https://commons.wikimedia.org/w/api.php"
_NASA = "https://images-api.nasa.gov/search"
_MIN_BYTES = 30_000
_MIN_WIDTH = 640


def _download(client: httpx.Client, url: str, target: Path) -> bool:
    try:
        resp = client.get(url)
    except httpx.HTTPError:
        return False
    if resp.status_code != 200 or len(resp.content) < _MIN_BYTES:
        return False
    target.write_bytes(resp.content)
    return True


def _commons_candidates(client: httpx.Client, query: str) -> list[str]:
    params = {
        "action": "query", "format": "json", "generator": "search",
        "gsrsearch": f"filetype:bitmap {query}", "gsrnamespace": 6, "gsrlimit": 8,
        "prop": "imageinfo", "iiprop": "url|size|mime",
    }
    try:
        resp = client.get(_COMMONS, params=params)
        pages = resp.json().get("query", {}).get("pages", {})
    except (httpx.HTTPError, ValueError):
        return []
    urls: list[str] = []
    for page in pages.values():
        for info in page.get("imageinfo", []):
            good_mime = info.get("mime") in ("image/jpeg", "image/png")
            if good_mime and info.get("width", 0) >= _MIN_WIDTH:
                urls.append(info["url"])
    return urls


def _nasa_candidates(client: httpx.Client, query: str) -> list[str]:
    try:
        resp = client.get(_NASA, params={"q": query, "media_type": "image"})
        items = resp.json().get("collection", {}).get("items", [])
    except (httpx.HTTPError, ValueError):
        return []
    urls: list[str] = []
    for item in items[:6]:
        nasa_id = (item.get("data") or [{}])[0].get("nasa_id")
        if nasa_id:
            urls.append(f"https://images-assets.nasa.gov/image/{nasa_id}/{nasa_id}~orig.jpg")
    return urls


def fetch_web_image(
    query: str,
    target: Path,
    *,
    client: httpx.Client | None = None,
) -> bool:
    """Search the web for ``query`` and save the first usable image to ``target``."""
    own_client = client is None
    client = client or httpx.Client(follow_redirects=True, timeout=60.0, headers=_UA)
    try:
        for url in _commons_candidates(client, query) + _nasa_candidates(client, query):
            if _download(client, url, target):
                return True
        return False
    finally:
        if own_client:
            client.close()
