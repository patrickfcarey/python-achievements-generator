"""Provider interface — each platform implements fetch(url) -> PlatformStats."""
from __future__ import annotations

import logging
from abc import ABC, abstractmethod

from bs4 import BeautifulSoup

from ..models import PlatformStats
from . import browser

log = logging.getLogger(__name__)


class ProviderError(Exception):
    """Controlled failure — scrape did not succeed."""


class Provider(ABC):
    platform: str = ""
    timeout: float = 30.0

    @abstractmethod
    def fetch(self, profile_url: str) -> PlatformStats: ...

    def _get_soup(self, url: str) -> BeautifulSoup:
        """Fetch HTML via the shared Playwright browser session."""
        try:
            html = browser.fetch_html(url, timeout_ms=int(self.timeout * 1000))
        except Exception as exc:  # Playwright raises its own errors; normalise
            raise ProviderError(f"{self.platform}: browser fetch error: {exc}") from exc
        if not html:
            raise ProviderError(f"{self.platform}: empty response")
        return BeautifulSoup(html, "html.parser")
