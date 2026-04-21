"""RetroAchievements public profile scraper (with API-key fallback)."""
from __future__ import annotations

import logging
import os
import re

import requests
from bs4 import BeautifulSoup

from ..models import PlatformStats, SubStat
from ..services.normalize import parse_float, parse_int
from .base import Provider, ProviderError

log = logging.getLogger(__name__)


class RetroAchievementsProvider(Provider):
    platform = "retroachievements"

    def fetch(self, profile_url: str) -> PlatformStats:
        api_user = os.environ.get("RA_API_USER") or os.environ.get("RETROACHIEVEMENTS_API_USER")
        api_key = os.environ.get("RA_API_KEY") or os.environ.get("RETROACHIEVEMENTS_API_KEY")
        if api_user and api_key:
            username = self._username_from_url(profile_url)
            if username:
                try:
                    return self._fetch_via_api(username, api_user, api_key)
                except ProviderError as exc:
                    log.warning("retroachievements: API fetch failed (%s), falling back to scrape", exc)

        soup = self._get_soup(profile_url)
        stats = PlatformStats(platform=self.platform, headline_label="Hardcore Points")
        stats.username = self._extract_username(soup, profile_url)
        stats.avatar_url = self._extract_avatar(soup)

        page_text = soup.get_text(" ", strip=True)

        softcore = self._find_number(page_text, r"(?:softcore|soft)\s*(?:points|score)?")
        hardcore = self._find_number(page_text, r"(?:hardcore|hard)\s*(?:points|score)?")
        true_ratio = self._find_float(page_text, r"(?:(?:site\s*)?ratio|true\s*ratio|retro\s*ratio)")
        masteries = self._find_number(page_text, r"master(?:ies|ed)")
        completions = self._find_number(page_text, r"completion(?:s|ist)?")
        beaten = self._find_number(page_text, r"beaten")

        stats.headline_value = hardcore if hardcore is not None else softcore

        # Field names mirror the RetroAchievements JSON API response so the
        # cache and renderer speak one vocabulary. HTML scrape can't produce
        # TotalTruePoints, so it's left unset here.
        stats.extra_fields = {
            "TotalPoints": hardcore,
            "TotalSoftcorePoints": softcore,
            "TotalTruePoints": None,
            "BeatenHardcoreAwardsCount": beaten,
            "CompletionAwardsCount": completions,
            "MasteryAwardsCount": masteries,
            "true_ratio": true_ratio,
        }
        stats.substats = [
            SubStat(label="RR", value=true_ratio or 0.0),
            SubStat(label="B", value=beaten or 0),
            SubStat(label="M", value=masteries or 0),
        ]
        if softcore is None and hardcore is None:
            raise ProviderError("retroachievements: no point totals found")
        return stats

    def _extract_username(self, soup: BeautifulSoup, url: str) -> str:
        h1 = soup.find("h1")
        if h1 and h1.get_text(strip=True):
            return h1.get_text(strip=True)
        m = re.search(r"/user/([^/?#]+)", url)
        return m.group(1) if m else ""

    def _extract_avatar(self, soup: BeautifulSoup) -> str | None:
        og = soup.find("meta", property="og:image")
        if og and og.get("content"):
            return og["content"]
        img = soup.select_one("img[src*='UserPic'], img[alt*='avatar' i]")
        if img and img.get("src"):
            return img["src"]
        return None

    def _find_number(self, text: str, label_pat: str) -> int | None:
        m = re.search(rf"{label_pat}[^0-9]{{0,20}}([\d,]+)", text, re.I)
        return parse_int(m.group(1)) if m else None

    def _find_float(self, text: str, label_pat: str) -> float | None:
        m = re.search(rf"{label_pat}[^0-9]{{0,20}}([\d,]+\.?\d*)", text, re.I)
        return parse_float(m.group(1)) if m else None

    def _username_from_url(self, url: str) -> str:
        m = re.search(r"/user/([^/?#]+)", url)
        return m.group(1) if m else ""

    def _fetch_via_api(self, username: str, api_user: str, api_key: str) -> PlatformStats:
        """Use the official JSON API — bypasses Cloudflare entirely."""
        base = "https://retroachievements.org/API"
        params = {"z": api_user, "y": api_key, "u": username}
        try:
            summary = requests.get(
                f"{base}/API_GetUserSummary.php", params=params, timeout=self.timeout
            )
            summary.raise_for_status()
            summary_j = summary.json()
            profile = requests.get(
                f"{base}/API_GetUserProfile.php", params=params, timeout=self.timeout
            )
            profile.raise_for_status()
            profile_j = profile.json()
            awards = requests.get(
                f"{base}/API_GetUserAwards.php", params=params, timeout=self.timeout
            )
            awards.raise_for_status()
            awards_j = awards.json()
        except (requests.RequestException, ValueError) as exc:
            raise ProviderError(f"retroachievements: API error: {exc}") from exc

        hardcore = parse_int(summary_j.get("TotalPoints"))
        softcore = parse_int(summary_j.get("TotalSoftcorePoints"))
        true_points = parse_int(summary_j.get("TotalTruePoints"))
        true_ratio = None
        if true_points and hardcore:
            true_ratio = round(true_points / hardcore, 2)
        # Use the explicit field — do NOT fall through on falsy (0) values.
        masteries = parse_int(awards_j.get("MasteryAwardsCount"))
        completions = parse_int(awards_j.get("CompletionAwardsCount"))
        beaten = parse_int(awards_j.get("BeatenHardcoreAwardsCount"))

        avatar = profile_j.get("UserPic") or summary_j.get("UserPic")
        avatar_url = None
        if avatar:
            avatar_url = (
                avatar if avatar.startswith("http")
                else f"https://retroachievements.org{avatar}"
            )

        stats = PlatformStats(platform=self.platform, headline_label="Hardcore Points")
        stats.username = profile_j.get("User") or summary_j.get("User") or username
        stats.avatar_url = avatar_url
        stats.headline_value = hardcore if hardcore is not None else softcore
        # Field names mirror the RetroAchievements JSON API response so the
        # cache and renderer speak one vocabulary.
        stats.extra_fields = {
            "TotalPoints": hardcore,
            "TotalSoftcorePoints": softcore,
            "TotalTruePoints": true_points,
            "BeatenHardcoreAwardsCount": beaten,
            "CompletionAwardsCount": completions,
            "MasteryAwardsCount": masteries,
            "true_ratio": true_ratio,
        }
        stats.substats = [
            SubStat(label="RR", value=true_ratio or 0.0),
            SubStat(label="B", value=beaten or 0),
            SubStat(label="M", value=masteries or 0),
        ]
        if hardcore is None and softcore is None:
            raise ProviderError("retroachievements: API returned no point totals")
        return stats
