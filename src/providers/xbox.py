"""TrueAchievements scraper for Xbox gamerscore + achievement tiers."""
from __future__ import annotations

import logging
import re

from bs4 import BeautifulSoup

from ..models import PlatformStats, SubStat
from ..services.normalize import parse_int
from .base import Provider, ProviderError

log = logging.getLogger(__name__)


class XboxProvider(Provider):
    platform = "xbox"

    def fetch(self, profile_url: str) -> PlatformStats:
        soup = self._get_soup(profile_url)
        stats = PlatformStats(platform=self.platform, headline_label="Gamerscore")
        stats.username = self._extract_username(soup, profile_url)
        stats.avatar_url = self._extract_avatar(soup)
        stats.headline_value = self._extract_gamerscore(soup)
        ta = self._extract_ta_score(soup)
        stats.extra_fields = {"ta_score": ta}
        stats.substats = [SubStat(label="TA", value=ta or 0)]
        if stats.headline_value is None and ta is None:
            raise ProviderError("xbox: no recognizable stats on page")
        return stats

    def _extract_username(self, soup: BeautifulSoup, url: str) -> str:
        h1 = soup.find("h1")
        if h1 and h1.get_text(strip=True):
            return h1.get_text(strip=True).split()[0]
        m = re.search(r"/gamer/([^/?#]+)", url)
        return m.group(1) if m else ""

    def _extract_avatar(self, soup: BeautifulSoup) -> str | None:
        og = soup.find("meta", property="og:image")
        if og and og.get("content"):
            return og["content"]
        img = soup.select_one("img.gamer-avatar, img.avatar, img[alt*='avatar' i]")
        if img and img.get("src"):
            return img["src"]
        return None

    def _extract_gamerscore(self, soup: BeautifulSoup) -> int | None:
        # TrueAchievements labels the site's own score and the raw gamerscore
        # separately. Prefer the row labelled with "Gamerscore".
        for row in soup.select("li, tr, div"):
            text = row.get_text(" ", strip=True)
            if re.search(r"\bGamerscore\b", text, re.I):
                n = parse_int(text.replace("Gamerscore", ""))
                if n:
                    return n
        return parse_int(soup.get_text(" ", strip=True))

    def _extract_ta_score(self, soup: BeautifulSoup) -> int | None:
        """TrueAchievements site score (TA). Usually 2-3x raw Gamerscore."""
        for row in soup.select("li, tr, div, span"):
            text = row.get_text(" ", strip=True)
            if re.search(r"TrueAchievement\s*Score|\bTA\s*Score\b", text, re.I):
                m = re.search(r"([\d,]{3,})", text)
                if m:
                    n = parse_int(m.group(1))
                    if n is not None:
                        return n
        page = soup.get_text(" ", strip=True)
        m = re.search(r"\bTA\b[^0-9]{0,12}([\d,]+)", page)
        return parse_int(m.group(1)) if m else None
