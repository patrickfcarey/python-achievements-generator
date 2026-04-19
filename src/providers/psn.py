"""PSNProfiles scraper for PlayStation trophy counts."""
from __future__ import annotations

import logging
import re

from bs4 import BeautifulSoup

from ..models import PlatformStats, SubStat
from ..services.normalize import parse_int
from .base import Provider, ProviderError

log = logging.getLogger(__name__)


_TIERS = ("platinum", "gold", "silver", "bronze")


class PsnProvider(Provider):
    platform = "psn"

    def fetch(self, profile_url: str) -> PlatformStats:
        soup = self._get_soup(profile_url)
        stats = PlatformStats(platform=self.platform, headline_label="Trophies")
        stats.username = self._extract_username(soup, profile_url)
        stats.avatar_url = self._extract_avatar(soup)

        counts = self._extract_trophy_counts(soup)
        stats.substats = [SubStat(label=tier, value=counts.get(tier, 0)) for tier in _TIERS]

        plat = counts.get("platinum", 0)
        stats.headline_value = f"{plat:,} Platinums" if plat is not None else None

        if not any(counts.values()):
            raise ProviderError("psn: no trophy counts found")
        return stats

    def _extract_username(self, soup: BeautifulSoup, url: str) -> str:
        name_el = soup.select_one("span.username") or soup.find("h1")
        if name_el and name_el.get_text(strip=True):
            return name_el.get_text(strip=True)
        m = re.search(r"psnprofiles\.com/([^/?#]+)", url)
        return m.group(1) if m else ""

    def _extract_avatar(self, soup: BeautifulSoup) -> str | None:
        og = soup.find("meta", property="og:image")
        if og and og.get("content"):
            return og["content"]
        img = soup.select_one("img.avatar, div.avatar img")
        if img and img.get("src"):
            return img["src"]
        return None

    def _extract_trophy_counts(self, soup: BeautifulSoup) -> dict[str, int]:
        counts: dict[str, int] = {}
        # PSNProfiles uses <li class="platinum">123</li> style markers in several places
        for tier in _TIERS:
            el = soup.select_one(f"li.{tier}, span.{tier}, div.{tier}")
            if el:
                n = parse_int(el.get_text(" ", strip=True))
                if n is not None:
                    counts[tier] = n
                    continue

            m = re.search(rf"\b{tier}\b[^0-9]{{0,12}}([\d,]+)", soup.get_text(" ", strip=True), re.I)
            if m:
                n = parse_int(m.group(1))
                if n is not None:
                    counts[tier] = n
        return counts
