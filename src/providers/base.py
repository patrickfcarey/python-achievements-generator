"""Provider interface — each platform implements fetch(url) -> PlatformStats."""
from __future__ import annotations

import logging
from abc import ABC, abstractmethod

import requests
from bs4 import BeautifulSoup

try:
    import cloudscraper  # type: ignore
except ImportError:  # pragma: no cover - optional dep
    cloudscraper = None  # type: ignore

from ..models import PlatformStats

log = logging.getLogger(__name__)


class ProviderError(Exception):
    """Controlled failure — scrape did not succeed."""


_SCRAPER = None


def _get_scraper():
    """Shared cloudscraper session (falls back to plain requests)."""
    global _SCRAPER
    if _SCRAPER is not None:
        return _SCRAPER
    if cloudscraper is not None:
        _SCRAPER = cloudscraper.create_scraper(
            browser={"browser": "chrome", "platform": "linux", "mobile": False}
        )
    else:
        _SCRAPER = requests.Session()
    return _SCRAPER


class Provider(ABC):
    platform: str = ""
    user_agent: str = (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/120.0 Safari/537.36"
    )
    timeout: float = 30.0

    @abstractmethod
    def fetch(self, profile_url: str) -> PlatformStats: ...

    def _get_soup(self, url: str) -> BeautifulSoup:
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Upgrade-Insecure-Requests": "1",
        }
        try:
            resp = _get_scraper().get(url, timeout=self.timeout, headers=headers)
            resp.raise_for_status()
        except requests.RequestException as exc:
            raise ProviderError(f"{self.platform}: HTTP error: {exc}") from exc
        return BeautifulSoup(resp.text, "html.parser")
