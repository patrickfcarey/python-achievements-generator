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
from inspect import signature as _mutmut_signature
from typing import Annotated
from typing import Callable
from typing import ClassVar


MutantDict = Annotated[dict[str, Callable], "Mutant"]


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg = None):
    """Forward call to original or mutated function, depending on the environment"""
    import os
    mutant_under_test = os.environ['MUTANT_UNDER_TEST']
    if mutant_under_test == 'fail':
        from mutmut.__main__ import MutmutProgrammaticFailException
        raise MutmutProgrammaticFailException('Failed programmatically')      
    elif mutant_under_test == 'stats':
        from mutmut.__main__ import record_trampoline_hit
        record_trampoline_hit(orig.__module__ + '.' + orig.__name__)
        result = orig(*call_args, **call_kwargs)
        return result
    prefix = orig.__module__ + '.' + orig.__name__ + '__mutmut_'
    if not mutant_under_test.startswith(prefix):
        result = orig(*call_args, **call_kwargs)
        return result
    mutant_name = mutant_under_test.rpartition('.')[-1]
    if self_arg:
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs)
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs)
    return result


class RetroAchievementsProvider(Provider):
    platform = "retroachievements"

    def xǁRetroAchievementsProviderǁfetch__mutmut_orig(self, profile_url: str) -> PlatformStats:
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

    def xǁRetroAchievementsProviderǁfetch__mutmut_1(self, profile_url: str) -> PlatformStats:
        api_user = None
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

    def xǁRetroAchievementsProviderǁfetch__mutmut_2(self, profile_url: str) -> PlatformStats:
        api_user = os.environ.get("RA_API_USER") and os.environ.get("RETROACHIEVEMENTS_API_USER")
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

    def xǁRetroAchievementsProviderǁfetch__mutmut_3(self, profile_url: str) -> PlatformStats:
        api_user = os.environ.get(None) or os.environ.get("RETROACHIEVEMENTS_API_USER")
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

    def xǁRetroAchievementsProviderǁfetch__mutmut_4(self, profile_url: str) -> PlatformStats:
        api_user = os.environ.get("XXRA_API_USERXX") or os.environ.get("RETROACHIEVEMENTS_API_USER")
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

    def xǁRetroAchievementsProviderǁfetch__mutmut_5(self, profile_url: str) -> PlatformStats:
        api_user = os.environ.get("ra_api_user") or os.environ.get("RETROACHIEVEMENTS_API_USER")
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

    def xǁRetroAchievementsProviderǁfetch__mutmut_6(self, profile_url: str) -> PlatformStats:
        api_user = os.environ.get("RA_API_USER") or os.environ.get(None)
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

    def xǁRetroAchievementsProviderǁfetch__mutmut_7(self, profile_url: str) -> PlatformStats:
        api_user = os.environ.get("RA_API_USER") or os.environ.get("XXRETROACHIEVEMENTS_API_USERXX")
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

    def xǁRetroAchievementsProviderǁfetch__mutmut_8(self, profile_url: str) -> PlatformStats:
        api_user = os.environ.get("RA_API_USER") or os.environ.get("retroachievements_api_user")
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

    def xǁRetroAchievementsProviderǁfetch__mutmut_9(self, profile_url: str) -> PlatformStats:
        api_user = os.environ.get("RA_API_USER") or os.environ.get("RETROACHIEVEMENTS_API_USER")
        api_key = None
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

    def xǁRetroAchievementsProviderǁfetch__mutmut_10(self, profile_url: str) -> PlatformStats:
        api_user = os.environ.get("RA_API_USER") or os.environ.get("RETROACHIEVEMENTS_API_USER")
        api_key = os.environ.get("RA_API_KEY") and os.environ.get("RETROACHIEVEMENTS_API_KEY")
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

    def xǁRetroAchievementsProviderǁfetch__mutmut_11(self, profile_url: str) -> PlatformStats:
        api_user = os.environ.get("RA_API_USER") or os.environ.get("RETROACHIEVEMENTS_API_USER")
        api_key = os.environ.get(None) or os.environ.get("RETROACHIEVEMENTS_API_KEY")
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

    def xǁRetroAchievementsProviderǁfetch__mutmut_12(self, profile_url: str) -> PlatformStats:
        api_user = os.environ.get("RA_API_USER") or os.environ.get("RETROACHIEVEMENTS_API_USER")
        api_key = os.environ.get("XXRA_API_KEYXX") or os.environ.get("RETROACHIEVEMENTS_API_KEY")
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

    def xǁRetroAchievementsProviderǁfetch__mutmut_13(self, profile_url: str) -> PlatformStats:
        api_user = os.environ.get("RA_API_USER") or os.environ.get("RETROACHIEVEMENTS_API_USER")
        api_key = os.environ.get("ra_api_key") or os.environ.get("RETROACHIEVEMENTS_API_KEY")
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

    def xǁRetroAchievementsProviderǁfetch__mutmut_14(self, profile_url: str) -> PlatformStats:
        api_user = os.environ.get("RA_API_USER") or os.environ.get("RETROACHIEVEMENTS_API_USER")
        api_key = os.environ.get("RA_API_KEY") or os.environ.get(None)
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

    def xǁRetroAchievementsProviderǁfetch__mutmut_15(self, profile_url: str) -> PlatformStats:
        api_user = os.environ.get("RA_API_USER") or os.environ.get("RETROACHIEVEMENTS_API_USER")
        api_key = os.environ.get("RA_API_KEY") or os.environ.get("XXRETROACHIEVEMENTS_API_KEYXX")
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

    def xǁRetroAchievementsProviderǁfetch__mutmut_16(self, profile_url: str) -> PlatformStats:
        api_user = os.environ.get("RA_API_USER") or os.environ.get("RETROACHIEVEMENTS_API_USER")
        api_key = os.environ.get("RA_API_KEY") or os.environ.get("retroachievements_api_key")
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

    def xǁRetroAchievementsProviderǁfetch__mutmut_17(self, profile_url: str) -> PlatformStats:
        api_user = os.environ.get("RA_API_USER") or os.environ.get("RETROACHIEVEMENTS_API_USER")
        api_key = os.environ.get("RA_API_KEY") or os.environ.get("RETROACHIEVEMENTS_API_KEY")
        if api_user or api_key:
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

    def xǁRetroAchievementsProviderǁfetch__mutmut_18(self, profile_url: str) -> PlatformStats:
        api_user = os.environ.get("RA_API_USER") or os.environ.get("RETROACHIEVEMENTS_API_USER")
        api_key = os.environ.get("RA_API_KEY") or os.environ.get("RETROACHIEVEMENTS_API_KEY")
        if api_user and api_key:
            username = None
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

    def xǁRetroAchievementsProviderǁfetch__mutmut_19(self, profile_url: str) -> PlatformStats:
        api_user = os.environ.get("RA_API_USER") or os.environ.get("RETROACHIEVEMENTS_API_USER")
        api_key = os.environ.get("RA_API_KEY") or os.environ.get("RETROACHIEVEMENTS_API_KEY")
        if api_user and api_key:
            username = self._username_from_url(None)
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

    def xǁRetroAchievementsProviderǁfetch__mutmut_20(self, profile_url: str) -> PlatformStats:
        api_user = os.environ.get("RA_API_USER") or os.environ.get("RETROACHIEVEMENTS_API_USER")
        api_key = os.environ.get("RA_API_KEY") or os.environ.get("RETROACHIEVEMENTS_API_KEY")
        if api_user and api_key:
            username = self._username_from_url(profile_url)
            if username:
                try:
                    return self._fetch_via_api(None, api_user, api_key)
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

    def xǁRetroAchievementsProviderǁfetch__mutmut_21(self, profile_url: str) -> PlatformStats:
        api_user = os.environ.get("RA_API_USER") or os.environ.get("RETROACHIEVEMENTS_API_USER")
        api_key = os.environ.get("RA_API_KEY") or os.environ.get("RETROACHIEVEMENTS_API_KEY")
        if api_user and api_key:
            username = self._username_from_url(profile_url)
            if username:
                try:
                    return self._fetch_via_api(username, None, api_key)
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

    def xǁRetroAchievementsProviderǁfetch__mutmut_22(self, profile_url: str) -> PlatformStats:
        api_user = os.environ.get("RA_API_USER") or os.environ.get("RETROACHIEVEMENTS_API_USER")
        api_key = os.environ.get("RA_API_KEY") or os.environ.get("RETROACHIEVEMENTS_API_KEY")
        if api_user and api_key:
            username = self._username_from_url(profile_url)
            if username:
                try:
                    return self._fetch_via_api(username, api_user, None)
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

    def xǁRetroAchievementsProviderǁfetch__mutmut_23(self, profile_url: str) -> PlatformStats:
        api_user = os.environ.get("RA_API_USER") or os.environ.get("RETROACHIEVEMENTS_API_USER")
        api_key = os.environ.get("RA_API_KEY") or os.environ.get("RETROACHIEVEMENTS_API_KEY")
        if api_user and api_key:
            username = self._username_from_url(profile_url)
            if username:
                try:
                    return self._fetch_via_api(api_user, api_key)
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

    def xǁRetroAchievementsProviderǁfetch__mutmut_24(self, profile_url: str) -> PlatformStats:
        api_user = os.environ.get("RA_API_USER") or os.environ.get("RETROACHIEVEMENTS_API_USER")
        api_key = os.environ.get("RA_API_KEY") or os.environ.get("RETROACHIEVEMENTS_API_KEY")
        if api_user and api_key:
            username = self._username_from_url(profile_url)
            if username:
                try:
                    return self._fetch_via_api(username, api_key)
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

    def xǁRetroAchievementsProviderǁfetch__mutmut_25(self, profile_url: str) -> PlatformStats:
        api_user = os.environ.get("RA_API_USER") or os.environ.get("RETROACHIEVEMENTS_API_USER")
        api_key = os.environ.get("RA_API_KEY") or os.environ.get("RETROACHIEVEMENTS_API_KEY")
        if api_user and api_key:
            username = self._username_from_url(profile_url)
            if username:
                try:
                    return self._fetch_via_api(username, api_user, )
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

    def xǁRetroAchievementsProviderǁfetch__mutmut_26(self, profile_url: str) -> PlatformStats:
        api_user = os.environ.get("RA_API_USER") or os.environ.get("RETROACHIEVEMENTS_API_USER")
        api_key = os.environ.get("RA_API_KEY") or os.environ.get("RETROACHIEVEMENTS_API_KEY")
        if api_user and api_key:
            username = self._username_from_url(profile_url)
            if username:
                try:
                    return self._fetch_via_api(username, api_user, api_key)
                except ProviderError as exc:
                    log.warning(None, exc)

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

    def xǁRetroAchievementsProviderǁfetch__mutmut_27(self, profile_url: str) -> PlatformStats:
        api_user = os.environ.get("RA_API_USER") or os.environ.get("RETROACHIEVEMENTS_API_USER")
        api_key = os.environ.get("RA_API_KEY") or os.environ.get("RETROACHIEVEMENTS_API_KEY")
        if api_user and api_key:
            username = self._username_from_url(profile_url)
            if username:
                try:
                    return self._fetch_via_api(username, api_user, api_key)
                except ProviderError as exc:
                    log.warning("retroachievements: API fetch failed (%s), falling back to scrape", None)

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

    def xǁRetroAchievementsProviderǁfetch__mutmut_28(self, profile_url: str) -> PlatformStats:
        api_user = os.environ.get("RA_API_USER") or os.environ.get("RETROACHIEVEMENTS_API_USER")
        api_key = os.environ.get("RA_API_KEY") or os.environ.get("RETROACHIEVEMENTS_API_KEY")
        if api_user and api_key:
            username = self._username_from_url(profile_url)
            if username:
                try:
                    return self._fetch_via_api(username, api_user, api_key)
                except ProviderError as exc:
                    log.warning(exc)

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

    def xǁRetroAchievementsProviderǁfetch__mutmut_29(self, profile_url: str) -> PlatformStats:
        api_user = os.environ.get("RA_API_USER") or os.environ.get("RETROACHIEVEMENTS_API_USER")
        api_key = os.environ.get("RA_API_KEY") or os.environ.get("RETROACHIEVEMENTS_API_KEY")
        if api_user and api_key:
            username = self._username_from_url(profile_url)
            if username:
                try:
                    return self._fetch_via_api(username, api_user, api_key)
                except ProviderError as exc:
                    log.warning("retroachievements: API fetch failed (%s), falling back to scrape", )

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

    def xǁRetroAchievementsProviderǁfetch__mutmut_30(self, profile_url: str) -> PlatformStats:
        api_user = os.environ.get("RA_API_USER") or os.environ.get("RETROACHIEVEMENTS_API_USER")
        api_key = os.environ.get("RA_API_KEY") or os.environ.get("RETROACHIEVEMENTS_API_KEY")
        if api_user and api_key:
            username = self._username_from_url(profile_url)
            if username:
                try:
                    return self._fetch_via_api(username, api_user, api_key)
                except ProviderError as exc:
                    log.warning("XXretroachievements: API fetch failed (%s), falling back to scrapeXX", exc)

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

    def xǁRetroAchievementsProviderǁfetch__mutmut_31(self, profile_url: str) -> PlatformStats:
        api_user = os.environ.get("RA_API_USER") or os.environ.get("RETROACHIEVEMENTS_API_USER")
        api_key = os.environ.get("RA_API_KEY") or os.environ.get("RETROACHIEVEMENTS_API_KEY")
        if api_user and api_key:
            username = self._username_from_url(profile_url)
            if username:
                try:
                    return self._fetch_via_api(username, api_user, api_key)
                except ProviderError as exc:
                    log.warning("retroachievements: api fetch failed (%s), falling back to scrape", exc)

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

    def xǁRetroAchievementsProviderǁfetch__mutmut_32(self, profile_url: str) -> PlatformStats:
        api_user = os.environ.get("RA_API_USER") or os.environ.get("RETROACHIEVEMENTS_API_USER")
        api_key = os.environ.get("RA_API_KEY") or os.environ.get("RETROACHIEVEMENTS_API_KEY")
        if api_user and api_key:
            username = self._username_from_url(profile_url)
            if username:
                try:
                    return self._fetch_via_api(username, api_user, api_key)
                except ProviderError as exc:
                    log.warning("RETROACHIEVEMENTS: API FETCH FAILED (%S), FALLING BACK TO SCRAPE", exc)

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

    def xǁRetroAchievementsProviderǁfetch__mutmut_33(self, profile_url: str) -> PlatformStats:
        api_user = os.environ.get("RA_API_USER") or os.environ.get("RETROACHIEVEMENTS_API_USER")
        api_key = os.environ.get("RA_API_KEY") or os.environ.get("RETROACHIEVEMENTS_API_KEY")
        if api_user and api_key:
            username = self._username_from_url(profile_url)
            if username:
                try:
                    return self._fetch_via_api(username, api_user, api_key)
                except ProviderError as exc:
                    log.warning("retroachievements: API fetch failed (%s), falling back to scrape", exc)

        soup = None
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

    def xǁRetroAchievementsProviderǁfetch__mutmut_34(self, profile_url: str) -> PlatformStats:
        api_user = os.environ.get("RA_API_USER") or os.environ.get("RETROACHIEVEMENTS_API_USER")
        api_key = os.environ.get("RA_API_KEY") or os.environ.get("RETROACHIEVEMENTS_API_KEY")
        if api_user and api_key:
            username = self._username_from_url(profile_url)
            if username:
                try:
                    return self._fetch_via_api(username, api_user, api_key)
                except ProviderError as exc:
                    log.warning("retroachievements: API fetch failed (%s), falling back to scrape", exc)

        soup = self._get_soup(None)
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

    def xǁRetroAchievementsProviderǁfetch__mutmut_35(self, profile_url: str) -> PlatformStats:
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
        stats = None
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

    def xǁRetroAchievementsProviderǁfetch__mutmut_36(self, profile_url: str) -> PlatformStats:
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
        stats = PlatformStats(platform=None, headline_label="Hardcore Points")
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

    def xǁRetroAchievementsProviderǁfetch__mutmut_37(self, profile_url: str) -> PlatformStats:
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
        stats = PlatformStats(platform=self.platform, headline_label=None)
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

    def xǁRetroAchievementsProviderǁfetch__mutmut_38(self, profile_url: str) -> PlatformStats:
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
        stats = PlatformStats(headline_label="Hardcore Points")
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

    def xǁRetroAchievementsProviderǁfetch__mutmut_39(self, profile_url: str) -> PlatformStats:
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
        stats = PlatformStats(platform=self.platform, )
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

    def xǁRetroAchievementsProviderǁfetch__mutmut_40(self, profile_url: str) -> PlatformStats:
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
        stats = PlatformStats(platform=self.platform, headline_label="XXHardcore PointsXX")
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

    def xǁRetroAchievementsProviderǁfetch__mutmut_41(self, profile_url: str) -> PlatformStats:
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
        stats = PlatformStats(platform=self.platform, headline_label="hardcore points")
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

    def xǁRetroAchievementsProviderǁfetch__mutmut_42(self, profile_url: str) -> PlatformStats:
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
        stats = PlatformStats(platform=self.platform, headline_label="HARDCORE POINTS")
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

    def xǁRetroAchievementsProviderǁfetch__mutmut_43(self, profile_url: str) -> PlatformStats:
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
        stats.username = None
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

    def xǁRetroAchievementsProviderǁfetch__mutmut_44(self, profile_url: str) -> PlatformStats:
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
        stats.username = self._extract_username(None, profile_url)
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

    def xǁRetroAchievementsProviderǁfetch__mutmut_45(self, profile_url: str) -> PlatformStats:
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
        stats.username = self._extract_username(soup, None)
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

    def xǁRetroAchievementsProviderǁfetch__mutmut_46(self, profile_url: str) -> PlatformStats:
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
        stats.username = self._extract_username(profile_url)
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

    def xǁRetroAchievementsProviderǁfetch__mutmut_47(self, profile_url: str) -> PlatformStats:
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
        stats.username = self._extract_username(soup, )
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

    def xǁRetroAchievementsProviderǁfetch__mutmut_48(self, profile_url: str) -> PlatformStats:
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
        stats.avatar_url = None

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

    def xǁRetroAchievementsProviderǁfetch__mutmut_49(self, profile_url: str) -> PlatformStats:
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
        stats.avatar_url = self._extract_avatar(None)

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

    def xǁRetroAchievementsProviderǁfetch__mutmut_50(self, profile_url: str) -> PlatformStats:
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

        page_text = None

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

    def xǁRetroAchievementsProviderǁfetch__mutmut_51(self, profile_url: str) -> PlatformStats:
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

        page_text = soup.get_text(None, strip=True)

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

    def xǁRetroAchievementsProviderǁfetch__mutmut_52(self, profile_url: str) -> PlatformStats:
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

        page_text = soup.get_text(" ", strip=None)

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

    def xǁRetroAchievementsProviderǁfetch__mutmut_53(self, profile_url: str) -> PlatformStats:
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

        page_text = soup.get_text(strip=True)

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

    def xǁRetroAchievementsProviderǁfetch__mutmut_54(self, profile_url: str) -> PlatformStats:
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

        page_text = soup.get_text(" ", )

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

    def xǁRetroAchievementsProviderǁfetch__mutmut_55(self, profile_url: str) -> PlatformStats:
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

        page_text = soup.get_text("XX XX", strip=True)

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

    def xǁRetroAchievementsProviderǁfetch__mutmut_56(self, profile_url: str) -> PlatformStats:
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

        page_text = soup.get_text(" ", strip=False)

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

    def xǁRetroAchievementsProviderǁfetch__mutmut_57(self, profile_url: str) -> PlatformStats:
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

        softcore = None
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

    def xǁRetroAchievementsProviderǁfetch__mutmut_58(self, profile_url: str) -> PlatformStats:
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

        softcore = self._find_number(None, r"(?:softcore|soft)\s*(?:points|score)?")
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

    def xǁRetroAchievementsProviderǁfetch__mutmut_59(self, profile_url: str) -> PlatformStats:
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

        softcore = self._find_number(page_text, None)
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

    def xǁRetroAchievementsProviderǁfetch__mutmut_60(self, profile_url: str) -> PlatformStats:
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

        softcore = self._find_number(r"(?:softcore|soft)\s*(?:points|score)?")
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

    def xǁRetroAchievementsProviderǁfetch__mutmut_61(self, profile_url: str) -> PlatformStats:
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

        softcore = self._find_number(page_text, )
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

    def xǁRetroAchievementsProviderǁfetch__mutmut_62(self, profile_url: str) -> PlatformStats:
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

        softcore = self._find_number(page_text, r"XX(?:softcore|soft)\s*(?:points|score)?XX")
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

    def xǁRetroAchievementsProviderǁfetch__mutmut_63(self, profile_url: str) -> PlatformStats:
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

    def xǁRetroAchievementsProviderǁfetch__mutmut_64(self, profile_url: str) -> PlatformStats:
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

        softcore = self._find_number(page_text, r"(?:SOFTCORE|SOFT)\s*(?:POINTS|SCORE)?")
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

    def xǁRetroAchievementsProviderǁfetch__mutmut_65(self, profile_url: str) -> PlatformStats:
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
        hardcore = None
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

    def xǁRetroAchievementsProviderǁfetch__mutmut_66(self, profile_url: str) -> PlatformStats:
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
        hardcore = self._find_number(None, r"(?:hardcore|hard)\s*(?:points|score)?")
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

    def xǁRetroAchievementsProviderǁfetch__mutmut_67(self, profile_url: str) -> PlatformStats:
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
        hardcore = self._find_number(page_text, None)
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

    def xǁRetroAchievementsProviderǁfetch__mutmut_68(self, profile_url: str) -> PlatformStats:
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
        hardcore = self._find_number(r"(?:hardcore|hard)\s*(?:points|score)?")
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

    def xǁRetroAchievementsProviderǁfetch__mutmut_69(self, profile_url: str) -> PlatformStats:
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
        hardcore = self._find_number(page_text, )
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

    def xǁRetroAchievementsProviderǁfetch__mutmut_70(self, profile_url: str) -> PlatformStats:
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
        hardcore = self._find_number(page_text, r"XX(?:hardcore|hard)\s*(?:points|score)?XX")
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

    def xǁRetroAchievementsProviderǁfetch__mutmut_71(self, profile_url: str) -> PlatformStats:
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

    def xǁRetroAchievementsProviderǁfetch__mutmut_72(self, profile_url: str) -> PlatformStats:
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
        hardcore = self._find_number(page_text, r"(?:HARDCORE|HARD)\s*(?:POINTS|SCORE)?")
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

    def xǁRetroAchievementsProviderǁfetch__mutmut_73(self, profile_url: str) -> PlatformStats:
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
        true_ratio = None
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

    def xǁRetroAchievementsProviderǁfetch__mutmut_74(self, profile_url: str) -> PlatformStats:
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
        true_ratio = self._find_float(None, r"(?:(?:site\s*)?ratio|true\s*ratio|retro\s*ratio)")
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

    def xǁRetroAchievementsProviderǁfetch__mutmut_75(self, profile_url: str) -> PlatformStats:
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
        true_ratio = self._find_float(page_text, None)
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

    def xǁRetroAchievementsProviderǁfetch__mutmut_76(self, profile_url: str) -> PlatformStats:
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
        true_ratio = self._find_float(r"(?:(?:site\s*)?ratio|true\s*ratio|retro\s*ratio)")
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

    def xǁRetroAchievementsProviderǁfetch__mutmut_77(self, profile_url: str) -> PlatformStats:
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
        true_ratio = self._find_float(page_text, )
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

    def xǁRetroAchievementsProviderǁfetch__mutmut_78(self, profile_url: str) -> PlatformStats:
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
        true_ratio = self._find_float(page_text, r"XX(?:(?:site\s*)?ratio|true\s*ratio|retro\s*ratio)XX")
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

    def xǁRetroAchievementsProviderǁfetch__mutmut_79(self, profile_url: str) -> PlatformStats:
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

    def xǁRetroAchievementsProviderǁfetch__mutmut_80(self, profile_url: str) -> PlatformStats:
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
        true_ratio = self._find_float(page_text, r"(?:(?:SITE\s*)?RATIO|TRUE\s*RATIO|RETRO\s*RATIO)")
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

    def xǁRetroAchievementsProviderǁfetch__mutmut_81(self, profile_url: str) -> PlatformStats:
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
        masteries = None
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

    def xǁRetroAchievementsProviderǁfetch__mutmut_82(self, profile_url: str) -> PlatformStats:
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
        masteries = self._find_number(None, r"master(?:ies|ed)")
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

    def xǁRetroAchievementsProviderǁfetch__mutmut_83(self, profile_url: str) -> PlatformStats:
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
        masteries = self._find_number(page_text, None)
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

    def xǁRetroAchievementsProviderǁfetch__mutmut_84(self, profile_url: str) -> PlatformStats:
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
        masteries = self._find_number(r"master(?:ies|ed)")
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

    def xǁRetroAchievementsProviderǁfetch__mutmut_85(self, profile_url: str) -> PlatformStats:
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
        masteries = self._find_number(page_text, )
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

    def xǁRetroAchievementsProviderǁfetch__mutmut_86(self, profile_url: str) -> PlatformStats:
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
        masteries = self._find_number(page_text, r"XXmaster(?:ies|ed)XX")
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

    def xǁRetroAchievementsProviderǁfetch__mutmut_87(self, profile_url: str) -> PlatformStats:
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

    def xǁRetroAchievementsProviderǁfetch__mutmut_88(self, profile_url: str) -> PlatformStats:
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
        masteries = self._find_number(page_text, r"MASTER(?:IES|ED)")
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

    def xǁRetroAchievementsProviderǁfetch__mutmut_89(self, profile_url: str) -> PlatformStats:
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
        completions = None
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

    def xǁRetroAchievementsProviderǁfetch__mutmut_90(self, profile_url: str) -> PlatformStats:
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
        completions = self._find_number(None, r"completion(?:s|ist)?")
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

    def xǁRetroAchievementsProviderǁfetch__mutmut_91(self, profile_url: str) -> PlatformStats:
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
        completions = self._find_number(page_text, None)
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

    def xǁRetroAchievementsProviderǁfetch__mutmut_92(self, profile_url: str) -> PlatformStats:
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
        completions = self._find_number(r"completion(?:s|ist)?")
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

    def xǁRetroAchievementsProviderǁfetch__mutmut_93(self, profile_url: str) -> PlatformStats:
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
        completions = self._find_number(page_text, )
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

    def xǁRetroAchievementsProviderǁfetch__mutmut_94(self, profile_url: str) -> PlatformStats:
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
        completions = self._find_number(page_text, r"XXcompletion(?:s|ist)?XX")
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

    def xǁRetroAchievementsProviderǁfetch__mutmut_95(self, profile_url: str) -> PlatformStats:
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

    def xǁRetroAchievementsProviderǁfetch__mutmut_96(self, profile_url: str) -> PlatformStats:
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
        completions = self._find_number(page_text, r"COMPLETION(?:S|IST)?")
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

    def xǁRetroAchievementsProviderǁfetch__mutmut_97(self, profile_url: str) -> PlatformStats:
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
        beaten = None

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

    def xǁRetroAchievementsProviderǁfetch__mutmut_98(self, profile_url: str) -> PlatformStats:
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
        beaten = self._find_number(None, r"beaten")

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

    def xǁRetroAchievementsProviderǁfetch__mutmut_99(self, profile_url: str) -> PlatformStats:
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
        beaten = self._find_number(page_text, None)

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

    def xǁRetroAchievementsProviderǁfetch__mutmut_100(self, profile_url: str) -> PlatformStats:
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
        beaten = self._find_number(r"beaten")

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

    def xǁRetroAchievementsProviderǁfetch__mutmut_101(self, profile_url: str) -> PlatformStats:
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
        beaten = self._find_number(page_text, )

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

    def xǁRetroAchievementsProviderǁfetch__mutmut_102(self, profile_url: str) -> PlatformStats:
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
        beaten = self._find_number(page_text, r"XXbeatenXX")

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

    def xǁRetroAchievementsProviderǁfetch__mutmut_103(self, profile_url: str) -> PlatformStats:
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

    def xǁRetroAchievementsProviderǁfetch__mutmut_104(self, profile_url: str) -> PlatformStats:
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
        beaten = self._find_number(page_text, r"BEATEN")

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

    def xǁRetroAchievementsProviderǁfetch__mutmut_105(self, profile_url: str) -> PlatformStats:
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

        stats.headline_value = None

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

    def xǁRetroAchievementsProviderǁfetch__mutmut_106(self, profile_url: str) -> PlatformStats:
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

        stats.headline_value = hardcore if hardcore is None else softcore

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

    def xǁRetroAchievementsProviderǁfetch__mutmut_107(self, profile_url: str) -> PlatformStats:
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
        stats.extra_fields = None
        stats.substats = [
            SubStat(label="RR", value=true_ratio or 0.0),
            SubStat(label="B", value=beaten or 0),
            SubStat(label="M", value=masteries or 0),
        ]
        if softcore is None and hardcore is None:
            raise ProviderError("retroachievements: no point totals found")
        return stats

    def xǁRetroAchievementsProviderǁfetch__mutmut_108(self, profile_url: str) -> PlatformStats:
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
            "XXTotalPointsXX": hardcore,
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

    def xǁRetroAchievementsProviderǁfetch__mutmut_109(self, profile_url: str) -> PlatformStats:
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
            "totalpoints": hardcore,
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

    def xǁRetroAchievementsProviderǁfetch__mutmut_110(self, profile_url: str) -> PlatformStats:
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
            "TOTALPOINTS": hardcore,
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

    def xǁRetroAchievementsProviderǁfetch__mutmut_111(self, profile_url: str) -> PlatformStats:
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
            "XXTotalSoftcorePointsXX": softcore,
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

    def xǁRetroAchievementsProviderǁfetch__mutmut_112(self, profile_url: str) -> PlatformStats:
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
            "totalsoftcorepoints": softcore,
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

    def xǁRetroAchievementsProviderǁfetch__mutmut_113(self, profile_url: str) -> PlatformStats:
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
            "TOTALSOFTCOREPOINTS": softcore,
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

    def xǁRetroAchievementsProviderǁfetch__mutmut_114(self, profile_url: str) -> PlatformStats:
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
            "XXTotalTruePointsXX": None,
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

    def xǁRetroAchievementsProviderǁfetch__mutmut_115(self, profile_url: str) -> PlatformStats:
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
            "totaltruepoints": None,
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

    def xǁRetroAchievementsProviderǁfetch__mutmut_116(self, profile_url: str) -> PlatformStats:
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
            "TOTALTRUEPOINTS": None,
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

    def xǁRetroAchievementsProviderǁfetch__mutmut_117(self, profile_url: str) -> PlatformStats:
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
            "XXBeatenHardcoreAwardsCountXX": beaten,
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

    def xǁRetroAchievementsProviderǁfetch__mutmut_118(self, profile_url: str) -> PlatformStats:
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
            "beatenhardcoreawardscount": beaten,
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

    def xǁRetroAchievementsProviderǁfetch__mutmut_119(self, profile_url: str) -> PlatformStats:
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
            "BEATENHARDCOREAWARDSCOUNT": beaten,
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

    def xǁRetroAchievementsProviderǁfetch__mutmut_120(self, profile_url: str) -> PlatformStats:
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
            "XXCompletionAwardsCountXX": completions,
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

    def xǁRetroAchievementsProviderǁfetch__mutmut_121(self, profile_url: str) -> PlatformStats:
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
            "completionawardscount": completions,
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

    def xǁRetroAchievementsProviderǁfetch__mutmut_122(self, profile_url: str) -> PlatformStats:
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
            "COMPLETIONAWARDSCOUNT": completions,
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

    def xǁRetroAchievementsProviderǁfetch__mutmut_123(self, profile_url: str) -> PlatformStats:
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
            "XXMasteryAwardsCountXX": masteries,
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

    def xǁRetroAchievementsProviderǁfetch__mutmut_124(self, profile_url: str) -> PlatformStats:
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
            "masteryawardscount": masteries,
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

    def xǁRetroAchievementsProviderǁfetch__mutmut_125(self, profile_url: str) -> PlatformStats:
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
            "MASTERYAWARDSCOUNT": masteries,
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

    def xǁRetroAchievementsProviderǁfetch__mutmut_126(self, profile_url: str) -> PlatformStats:
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
            "XXtrue_ratioXX": true_ratio,
        }
        stats.substats = [
            SubStat(label="RR", value=true_ratio or 0.0),
            SubStat(label="B", value=beaten or 0),
            SubStat(label="M", value=masteries or 0),
        ]
        if softcore is None and hardcore is None:
            raise ProviderError("retroachievements: no point totals found")
        return stats

    def xǁRetroAchievementsProviderǁfetch__mutmut_127(self, profile_url: str) -> PlatformStats:
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
            "TRUE_RATIO": true_ratio,
        }
        stats.substats = [
            SubStat(label="RR", value=true_ratio or 0.0),
            SubStat(label="B", value=beaten or 0),
            SubStat(label="M", value=masteries or 0),
        ]
        if softcore is None and hardcore is None:
            raise ProviderError("retroachievements: no point totals found")
        return stats

    def xǁRetroAchievementsProviderǁfetch__mutmut_128(self, profile_url: str) -> PlatformStats:
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
        stats.substats = None
        if softcore is None and hardcore is None:
            raise ProviderError("retroachievements: no point totals found")
        return stats

    def xǁRetroAchievementsProviderǁfetch__mutmut_129(self, profile_url: str) -> PlatformStats:
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
            SubStat(label=None, value=true_ratio or 0.0),
            SubStat(label="B", value=beaten or 0),
            SubStat(label="M", value=masteries or 0),
        ]
        if softcore is None and hardcore is None:
            raise ProviderError("retroachievements: no point totals found")
        return stats

    def xǁRetroAchievementsProviderǁfetch__mutmut_130(self, profile_url: str) -> PlatformStats:
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
            SubStat(label="RR", value=None),
            SubStat(label="B", value=beaten or 0),
            SubStat(label="M", value=masteries or 0),
        ]
        if softcore is None and hardcore is None:
            raise ProviderError("retroachievements: no point totals found")
        return stats

    def xǁRetroAchievementsProviderǁfetch__mutmut_131(self, profile_url: str) -> PlatformStats:
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
            SubStat(value=true_ratio or 0.0),
            SubStat(label="B", value=beaten or 0),
            SubStat(label="M", value=masteries or 0),
        ]
        if softcore is None and hardcore is None:
            raise ProviderError("retroachievements: no point totals found")
        return stats

    def xǁRetroAchievementsProviderǁfetch__mutmut_132(self, profile_url: str) -> PlatformStats:
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
            SubStat(label="RR", ),
            SubStat(label="B", value=beaten or 0),
            SubStat(label="M", value=masteries or 0),
        ]
        if softcore is None and hardcore is None:
            raise ProviderError("retroachievements: no point totals found")
        return stats

    def xǁRetroAchievementsProviderǁfetch__mutmut_133(self, profile_url: str) -> PlatformStats:
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
            SubStat(label="XXRRXX", value=true_ratio or 0.0),
            SubStat(label="B", value=beaten or 0),
            SubStat(label="M", value=masteries or 0),
        ]
        if softcore is None and hardcore is None:
            raise ProviderError("retroachievements: no point totals found")
        return stats

    def xǁRetroAchievementsProviderǁfetch__mutmut_134(self, profile_url: str) -> PlatformStats:
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
            SubStat(label="rr", value=true_ratio or 0.0),
            SubStat(label="B", value=beaten or 0),
            SubStat(label="M", value=masteries or 0),
        ]
        if softcore is None and hardcore is None:
            raise ProviderError("retroachievements: no point totals found")
        return stats

    def xǁRetroAchievementsProviderǁfetch__mutmut_135(self, profile_url: str) -> PlatformStats:
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
            SubStat(label="RR", value=true_ratio and 0.0),
            SubStat(label="B", value=beaten or 0),
            SubStat(label="M", value=masteries or 0),
        ]
        if softcore is None and hardcore is None:
            raise ProviderError("retroachievements: no point totals found")
        return stats

    def xǁRetroAchievementsProviderǁfetch__mutmut_136(self, profile_url: str) -> PlatformStats:
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
            SubStat(label="RR", value=true_ratio or 1.0),
            SubStat(label="B", value=beaten or 0),
            SubStat(label="M", value=masteries or 0),
        ]
        if softcore is None and hardcore is None:
            raise ProviderError("retroachievements: no point totals found")
        return stats

    def xǁRetroAchievementsProviderǁfetch__mutmut_137(self, profile_url: str) -> PlatformStats:
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
            SubStat(label=None, value=beaten or 0),
            SubStat(label="M", value=masteries or 0),
        ]
        if softcore is None and hardcore is None:
            raise ProviderError("retroachievements: no point totals found")
        return stats

    def xǁRetroAchievementsProviderǁfetch__mutmut_138(self, profile_url: str) -> PlatformStats:
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
            SubStat(label="B", value=None),
            SubStat(label="M", value=masteries or 0),
        ]
        if softcore is None and hardcore is None:
            raise ProviderError("retroachievements: no point totals found")
        return stats

    def xǁRetroAchievementsProviderǁfetch__mutmut_139(self, profile_url: str) -> PlatformStats:
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
            SubStat(value=beaten or 0),
            SubStat(label="M", value=masteries or 0),
        ]
        if softcore is None and hardcore is None:
            raise ProviderError("retroachievements: no point totals found")
        return stats

    def xǁRetroAchievementsProviderǁfetch__mutmut_140(self, profile_url: str) -> PlatformStats:
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
            SubStat(label="B", ),
            SubStat(label="M", value=masteries or 0),
        ]
        if softcore is None and hardcore is None:
            raise ProviderError("retroachievements: no point totals found")
        return stats

    def xǁRetroAchievementsProviderǁfetch__mutmut_141(self, profile_url: str) -> PlatformStats:
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
            SubStat(label="XXBXX", value=beaten or 0),
            SubStat(label="M", value=masteries or 0),
        ]
        if softcore is None and hardcore is None:
            raise ProviderError("retroachievements: no point totals found")
        return stats

    def xǁRetroAchievementsProviderǁfetch__mutmut_142(self, profile_url: str) -> PlatformStats:
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
            SubStat(label="b", value=beaten or 0),
            SubStat(label="M", value=masteries or 0),
        ]
        if softcore is None and hardcore is None:
            raise ProviderError("retroachievements: no point totals found")
        return stats

    def xǁRetroAchievementsProviderǁfetch__mutmut_143(self, profile_url: str) -> PlatformStats:
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
            SubStat(label="B", value=beaten and 0),
            SubStat(label="M", value=masteries or 0),
        ]
        if softcore is None and hardcore is None:
            raise ProviderError("retroachievements: no point totals found")
        return stats

    def xǁRetroAchievementsProviderǁfetch__mutmut_144(self, profile_url: str) -> PlatformStats:
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
            SubStat(label="B", value=beaten or 1),
            SubStat(label="M", value=masteries or 0),
        ]
        if softcore is None and hardcore is None:
            raise ProviderError("retroachievements: no point totals found")
        return stats

    def xǁRetroAchievementsProviderǁfetch__mutmut_145(self, profile_url: str) -> PlatformStats:
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
            SubStat(label=None, value=masteries or 0),
        ]
        if softcore is None and hardcore is None:
            raise ProviderError("retroachievements: no point totals found")
        return stats

    def xǁRetroAchievementsProviderǁfetch__mutmut_146(self, profile_url: str) -> PlatformStats:
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
            SubStat(label="M", value=None),
        ]
        if softcore is None and hardcore is None:
            raise ProviderError("retroachievements: no point totals found")
        return stats

    def xǁRetroAchievementsProviderǁfetch__mutmut_147(self, profile_url: str) -> PlatformStats:
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
            SubStat(value=masteries or 0),
        ]
        if softcore is None and hardcore is None:
            raise ProviderError("retroachievements: no point totals found")
        return stats

    def xǁRetroAchievementsProviderǁfetch__mutmut_148(self, profile_url: str) -> PlatformStats:
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
            SubStat(label="M", ),
        ]
        if softcore is None and hardcore is None:
            raise ProviderError("retroachievements: no point totals found")
        return stats

    def xǁRetroAchievementsProviderǁfetch__mutmut_149(self, profile_url: str) -> PlatformStats:
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
            SubStat(label="XXMXX", value=masteries or 0),
        ]
        if softcore is None and hardcore is None:
            raise ProviderError("retroachievements: no point totals found")
        return stats

    def xǁRetroAchievementsProviderǁfetch__mutmut_150(self, profile_url: str) -> PlatformStats:
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
            SubStat(label="m", value=masteries or 0),
        ]
        if softcore is None and hardcore is None:
            raise ProviderError("retroachievements: no point totals found")
        return stats

    def xǁRetroAchievementsProviderǁfetch__mutmut_151(self, profile_url: str) -> PlatformStats:
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
            SubStat(label="M", value=masteries and 0),
        ]
        if softcore is None and hardcore is None:
            raise ProviderError("retroachievements: no point totals found")
        return stats

    def xǁRetroAchievementsProviderǁfetch__mutmut_152(self, profile_url: str) -> PlatformStats:
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
            SubStat(label="M", value=masteries or 1),
        ]
        if softcore is None and hardcore is None:
            raise ProviderError("retroachievements: no point totals found")
        return stats

    def xǁRetroAchievementsProviderǁfetch__mutmut_153(self, profile_url: str) -> PlatformStats:
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
        if softcore is None or hardcore is None:
            raise ProviderError("retroachievements: no point totals found")
        return stats

    def xǁRetroAchievementsProviderǁfetch__mutmut_154(self, profile_url: str) -> PlatformStats:
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
        if softcore is not None and hardcore is None:
            raise ProviderError("retroachievements: no point totals found")
        return stats

    def xǁRetroAchievementsProviderǁfetch__mutmut_155(self, profile_url: str) -> PlatformStats:
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
        if softcore is None and hardcore is not None:
            raise ProviderError("retroachievements: no point totals found")
        return stats

    def xǁRetroAchievementsProviderǁfetch__mutmut_156(self, profile_url: str) -> PlatformStats:
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
            raise ProviderError(None)
        return stats

    def xǁRetroAchievementsProviderǁfetch__mutmut_157(self, profile_url: str) -> PlatformStats:
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
            raise ProviderError("XXretroachievements: no point totals foundXX")
        return stats

    def xǁRetroAchievementsProviderǁfetch__mutmut_158(self, profile_url: str) -> PlatformStats:
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
            raise ProviderError("RETROACHIEVEMENTS: NO POINT TOTALS FOUND")
        return stats
    
    xǁRetroAchievementsProviderǁfetch__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁRetroAchievementsProviderǁfetch__mutmut_1': xǁRetroAchievementsProviderǁfetch__mutmut_1, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_2': xǁRetroAchievementsProviderǁfetch__mutmut_2, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_3': xǁRetroAchievementsProviderǁfetch__mutmut_3, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_4': xǁRetroAchievementsProviderǁfetch__mutmut_4, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_5': xǁRetroAchievementsProviderǁfetch__mutmut_5, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_6': xǁRetroAchievementsProviderǁfetch__mutmut_6, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_7': xǁRetroAchievementsProviderǁfetch__mutmut_7, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_8': xǁRetroAchievementsProviderǁfetch__mutmut_8, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_9': xǁRetroAchievementsProviderǁfetch__mutmut_9, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_10': xǁRetroAchievementsProviderǁfetch__mutmut_10, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_11': xǁRetroAchievementsProviderǁfetch__mutmut_11, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_12': xǁRetroAchievementsProviderǁfetch__mutmut_12, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_13': xǁRetroAchievementsProviderǁfetch__mutmut_13, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_14': xǁRetroAchievementsProviderǁfetch__mutmut_14, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_15': xǁRetroAchievementsProviderǁfetch__mutmut_15, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_16': xǁRetroAchievementsProviderǁfetch__mutmut_16, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_17': xǁRetroAchievementsProviderǁfetch__mutmut_17, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_18': xǁRetroAchievementsProviderǁfetch__mutmut_18, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_19': xǁRetroAchievementsProviderǁfetch__mutmut_19, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_20': xǁRetroAchievementsProviderǁfetch__mutmut_20, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_21': xǁRetroAchievementsProviderǁfetch__mutmut_21, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_22': xǁRetroAchievementsProviderǁfetch__mutmut_22, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_23': xǁRetroAchievementsProviderǁfetch__mutmut_23, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_24': xǁRetroAchievementsProviderǁfetch__mutmut_24, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_25': xǁRetroAchievementsProviderǁfetch__mutmut_25, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_26': xǁRetroAchievementsProviderǁfetch__mutmut_26, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_27': xǁRetroAchievementsProviderǁfetch__mutmut_27, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_28': xǁRetroAchievementsProviderǁfetch__mutmut_28, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_29': xǁRetroAchievementsProviderǁfetch__mutmut_29, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_30': xǁRetroAchievementsProviderǁfetch__mutmut_30, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_31': xǁRetroAchievementsProviderǁfetch__mutmut_31, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_32': xǁRetroAchievementsProviderǁfetch__mutmut_32, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_33': xǁRetroAchievementsProviderǁfetch__mutmut_33, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_34': xǁRetroAchievementsProviderǁfetch__mutmut_34, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_35': xǁRetroAchievementsProviderǁfetch__mutmut_35, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_36': xǁRetroAchievementsProviderǁfetch__mutmut_36, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_37': xǁRetroAchievementsProviderǁfetch__mutmut_37, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_38': xǁRetroAchievementsProviderǁfetch__mutmut_38, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_39': xǁRetroAchievementsProviderǁfetch__mutmut_39, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_40': xǁRetroAchievementsProviderǁfetch__mutmut_40, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_41': xǁRetroAchievementsProviderǁfetch__mutmut_41, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_42': xǁRetroAchievementsProviderǁfetch__mutmut_42, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_43': xǁRetroAchievementsProviderǁfetch__mutmut_43, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_44': xǁRetroAchievementsProviderǁfetch__mutmut_44, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_45': xǁRetroAchievementsProviderǁfetch__mutmut_45, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_46': xǁRetroAchievementsProviderǁfetch__mutmut_46, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_47': xǁRetroAchievementsProviderǁfetch__mutmut_47, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_48': xǁRetroAchievementsProviderǁfetch__mutmut_48, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_49': xǁRetroAchievementsProviderǁfetch__mutmut_49, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_50': xǁRetroAchievementsProviderǁfetch__mutmut_50, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_51': xǁRetroAchievementsProviderǁfetch__mutmut_51, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_52': xǁRetroAchievementsProviderǁfetch__mutmut_52, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_53': xǁRetroAchievementsProviderǁfetch__mutmut_53, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_54': xǁRetroAchievementsProviderǁfetch__mutmut_54, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_55': xǁRetroAchievementsProviderǁfetch__mutmut_55, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_56': xǁRetroAchievementsProviderǁfetch__mutmut_56, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_57': xǁRetroAchievementsProviderǁfetch__mutmut_57, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_58': xǁRetroAchievementsProviderǁfetch__mutmut_58, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_59': xǁRetroAchievementsProviderǁfetch__mutmut_59, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_60': xǁRetroAchievementsProviderǁfetch__mutmut_60, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_61': xǁRetroAchievementsProviderǁfetch__mutmut_61, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_62': xǁRetroAchievementsProviderǁfetch__mutmut_62, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_63': xǁRetroAchievementsProviderǁfetch__mutmut_63, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_64': xǁRetroAchievementsProviderǁfetch__mutmut_64, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_65': xǁRetroAchievementsProviderǁfetch__mutmut_65, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_66': xǁRetroAchievementsProviderǁfetch__mutmut_66, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_67': xǁRetroAchievementsProviderǁfetch__mutmut_67, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_68': xǁRetroAchievementsProviderǁfetch__mutmut_68, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_69': xǁRetroAchievementsProviderǁfetch__mutmut_69, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_70': xǁRetroAchievementsProviderǁfetch__mutmut_70, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_71': xǁRetroAchievementsProviderǁfetch__mutmut_71, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_72': xǁRetroAchievementsProviderǁfetch__mutmut_72, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_73': xǁRetroAchievementsProviderǁfetch__mutmut_73, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_74': xǁRetroAchievementsProviderǁfetch__mutmut_74, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_75': xǁRetroAchievementsProviderǁfetch__mutmut_75, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_76': xǁRetroAchievementsProviderǁfetch__mutmut_76, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_77': xǁRetroAchievementsProviderǁfetch__mutmut_77, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_78': xǁRetroAchievementsProviderǁfetch__mutmut_78, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_79': xǁRetroAchievementsProviderǁfetch__mutmut_79, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_80': xǁRetroAchievementsProviderǁfetch__mutmut_80, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_81': xǁRetroAchievementsProviderǁfetch__mutmut_81, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_82': xǁRetroAchievementsProviderǁfetch__mutmut_82, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_83': xǁRetroAchievementsProviderǁfetch__mutmut_83, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_84': xǁRetroAchievementsProviderǁfetch__mutmut_84, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_85': xǁRetroAchievementsProviderǁfetch__mutmut_85, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_86': xǁRetroAchievementsProviderǁfetch__mutmut_86, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_87': xǁRetroAchievementsProviderǁfetch__mutmut_87, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_88': xǁRetroAchievementsProviderǁfetch__mutmut_88, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_89': xǁRetroAchievementsProviderǁfetch__mutmut_89, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_90': xǁRetroAchievementsProviderǁfetch__mutmut_90, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_91': xǁRetroAchievementsProviderǁfetch__mutmut_91, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_92': xǁRetroAchievementsProviderǁfetch__mutmut_92, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_93': xǁRetroAchievementsProviderǁfetch__mutmut_93, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_94': xǁRetroAchievementsProviderǁfetch__mutmut_94, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_95': xǁRetroAchievementsProviderǁfetch__mutmut_95, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_96': xǁRetroAchievementsProviderǁfetch__mutmut_96, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_97': xǁRetroAchievementsProviderǁfetch__mutmut_97, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_98': xǁRetroAchievementsProviderǁfetch__mutmut_98, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_99': xǁRetroAchievementsProviderǁfetch__mutmut_99, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_100': xǁRetroAchievementsProviderǁfetch__mutmut_100, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_101': xǁRetroAchievementsProviderǁfetch__mutmut_101, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_102': xǁRetroAchievementsProviderǁfetch__mutmut_102, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_103': xǁRetroAchievementsProviderǁfetch__mutmut_103, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_104': xǁRetroAchievementsProviderǁfetch__mutmut_104, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_105': xǁRetroAchievementsProviderǁfetch__mutmut_105, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_106': xǁRetroAchievementsProviderǁfetch__mutmut_106, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_107': xǁRetroAchievementsProviderǁfetch__mutmut_107, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_108': xǁRetroAchievementsProviderǁfetch__mutmut_108, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_109': xǁRetroAchievementsProviderǁfetch__mutmut_109, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_110': xǁRetroAchievementsProviderǁfetch__mutmut_110, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_111': xǁRetroAchievementsProviderǁfetch__mutmut_111, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_112': xǁRetroAchievementsProviderǁfetch__mutmut_112, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_113': xǁRetroAchievementsProviderǁfetch__mutmut_113, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_114': xǁRetroAchievementsProviderǁfetch__mutmut_114, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_115': xǁRetroAchievementsProviderǁfetch__mutmut_115, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_116': xǁRetroAchievementsProviderǁfetch__mutmut_116, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_117': xǁRetroAchievementsProviderǁfetch__mutmut_117, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_118': xǁRetroAchievementsProviderǁfetch__mutmut_118, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_119': xǁRetroAchievementsProviderǁfetch__mutmut_119, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_120': xǁRetroAchievementsProviderǁfetch__mutmut_120, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_121': xǁRetroAchievementsProviderǁfetch__mutmut_121, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_122': xǁRetroAchievementsProviderǁfetch__mutmut_122, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_123': xǁRetroAchievementsProviderǁfetch__mutmut_123, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_124': xǁRetroAchievementsProviderǁfetch__mutmut_124, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_125': xǁRetroAchievementsProviderǁfetch__mutmut_125, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_126': xǁRetroAchievementsProviderǁfetch__mutmut_126, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_127': xǁRetroAchievementsProviderǁfetch__mutmut_127, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_128': xǁRetroAchievementsProviderǁfetch__mutmut_128, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_129': xǁRetroAchievementsProviderǁfetch__mutmut_129, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_130': xǁRetroAchievementsProviderǁfetch__mutmut_130, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_131': xǁRetroAchievementsProviderǁfetch__mutmut_131, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_132': xǁRetroAchievementsProviderǁfetch__mutmut_132, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_133': xǁRetroAchievementsProviderǁfetch__mutmut_133, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_134': xǁRetroAchievementsProviderǁfetch__mutmut_134, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_135': xǁRetroAchievementsProviderǁfetch__mutmut_135, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_136': xǁRetroAchievementsProviderǁfetch__mutmut_136, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_137': xǁRetroAchievementsProviderǁfetch__mutmut_137, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_138': xǁRetroAchievementsProviderǁfetch__mutmut_138, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_139': xǁRetroAchievementsProviderǁfetch__mutmut_139, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_140': xǁRetroAchievementsProviderǁfetch__mutmut_140, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_141': xǁRetroAchievementsProviderǁfetch__mutmut_141, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_142': xǁRetroAchievementsProviderǁfetch__mutmut_142, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_143': xǁRetroAchievementsProviderǁfetch__mutmut_143, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_144': xǁRetroAchievementsProviderǁfetch__mutmut_144, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_145': xǁRetroAchievementsProviderǁfetch__mutmut_145, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_146': xǁRetroAchievementsProviderǁfetch__mutmut_146, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_147': xǁRetroAchievementsProviderǁfetch__mutmut_147, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_148': xǁRetroAchievementsProviderǁfetch__mutmut_148, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_149': xǁRetroAchievementsProviderǁfetch__mutmut_149, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_150': xǁRetroAchievementsProviderǁfetch__mutmut_150, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_151': xǁRetroAchievementsProviderǁfetch__mutmut_151, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_152': xǁRetroAchievementsProviderǁfetch__mutmut_152, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_153': xǁRetroAchievementsProviderǁfetch__mutmut_153, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_154': xǁRetroAchievementsProviderǁfetch__mutmut_154, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_155': xǁRetroAchievementsProviderǁfetch__mutmut_155, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_156': xǁRetroAchievementsProviderǁfetch__mutmut_156, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_157': xǁRetroAchievementsProviderǁfetch__mutmut_157, 
        'xǁRetroAchievementsProviderǁfetch__mutmut_158': xǁRetroAchievementsProviderǁfetch__mutmut_158
    }
    
    def fetch(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁRetroAchievementsProviderǁfetch__mutmut_orig"), object.__getattribute__(self, "xǁRetroAchievementsProviderǁfetch__mutmut_mutants"), args, kwargs, self)
        return result 
    
    fetch.__signature__ = _mutmut_signature(xǁRetroAchievementsProviderǁfetch__mutmut_orig)
    xǁRetroAchievementsProviderǁfetch__mutmut_orig.__name__ = 'xǁRetroAchievementsProviderǁfetch'

    def xǁRetroAchievementsProviderǁ_extract_username__mutmut_orig(self, soup: BeautifulSoup, url: str) -> str:
        h1 = soup.find("h1")
        if h1 and h1.get_text(strip=True):
            return h1.get_text(strip=True)
        m = re.search(r"/user/([^/?#]+)", url)
        return m.group(1) if m else ""

    def xǁRetroAchievementsProviderǁ_extract_username__mutmut_1(self, soup: BeautifulSoup, url: str) -> str:
        h1 = None
        if h1 and h1.get_text(strip=True):
            return h1.get_text(strip=True)
        m = re.search(r"/user/([^/?#]+)", url)
        return m.group(1) if m else ""

    def xǁRetroAchievementsProviderǁ_extract_username__mutmut_2(self, soup: BeautifulSoup, url: str) -> str:
        h1 = soup.find(None)
        if h1 and h1.get_text(strip=True):
            return h1.get_text(strip=True)
        m = re.search(r"/user/([^/?#]+)", url)
        return m.group(1) if m else ""

    def xǁRetroAchievementsProviderǁ_extract_username__mutmut_3(self, soup: BeautifulSoup, url: str) -> str:
        h1 = soup.rfind("h1")
        if h1 and h1.get_text(strip=True):
            return h1.get_text(strip=True)
        m = re.search(r"/user/([^/?#]+)", url)
        return m.group(1) if m else ""

    def xǁRetroAchievementsProviderǁ_extract_username__mutmut_4(self, soup: BeautifulSoup, url: str) -> str:
        h1 = soup.find("XXh1XX")
        if h1 and h1.get_text(strip=True):
            return h1.get_text(strip=True)
        m = re.search(r"/user/([^/?#]+)", url)
        return m.group(1) if m else ""

    def xǁRetroAchievementsProviderǁ_extract_username__mutmut_5(self, soup: BeautifulSoup, url: str) -> str:
        h1 = soup.find("H1")
        if h1 and h1.get_text(strip=True):
            return h1.get_text(strip=True)
        m = re.search(r"/user/([^/?#]+)", url)
        return m.group(1) if m else ""

    def xǁRetroAchievementsProviderǁ_extract_username__mutmut_6(self, soup: BeautifulSoup, url: str) -> str:
        h1 = soup.find("h1")
        if h1 or h1.get_text(strip=True):
            return h1.get_text(strip=True)
        m = re.search(r"/user/([^/?#]+)", url)
        return m.group(1) if m else ""

    def xǁRetroAchievementsProviderǁ_extract_username__mutmut_7(self, soup: BeautifulSoup, url: str) -> str:
        h1 = soup.find("h1")
        if h1 and h1.get_text(strip=None):
            return h1.get_text(strip=True)
        m = re.search(r"/user/([^/?#]+)", url)
        return m.group(1) if m else ""

    def xǁRetroAchievementsProviderǁ_extract_username__mutmut_8(self, soup: BeautifulSoup, url: str) -> str:
        h1 = soup.find("h1")
        if h1 and h1.get_text(strip=False):
            return h1.get_text(strip=True)
        m = re.search(r"/user/([^/?#]+)", url)
        return m.group(1) if m else ""

    def xǁRetroAchievementsProviderǁ_extract_username__mutmut_9(self, soup: BeautifulSoup, url: str) -> str:
        h1 = soup.find("h1")
        if h1 and h1.get_text(strip=True):
            return h1.get_text(strip=None)
        m = re.search(r"/user/([^/?#]+)", url)
        return m.group(1) if m else ""

    def xǁRetroAchievementsProviderǁ_extract_username__mutmut_10(self, soup: BeautifulSoup, url: str) -> str:
        h1 = soup.find("h1")
        if h1 and h1.get_text(strip=True):
            return h1.get_text(strip=False)
        m = re.search(r"/user/([^/?#]+)", url)
        return m.group(1) if m else ""

    def xǁRetroAchievementsProviderǁ_extract_username__mutmut_11(self, soup: BeautifulSoup, url: str) -> str:
        h1 = soup.find("h1")
        if h1 and h1.get_text(strip=True):
            return h1.get_text(strip=True)
        m = None
        return m.group(1) if m else ""

    def xǁRetroAchievementsProviderǁ_extract_username__mutmut_12(self, soup: BeautifulSoup, url: str) -> str:
        h1 = soup.find("h1")
        if h1 and h1.get_text(strip=True):
            return h1.get_text(strip=True)
        m = re.search(None, url)
        return m.group(1) if m else ""

    def xǁRetroAchievementsProviderǁ_extract_username__mutmut_13(self, soup: BeautifulSoup, url: str) -> str:
        h1 = soup.find("h1")
        if h1 and h1.get_text(strip=True):
            return h1.get_text(strip=True)
        m = re.search(r"/user/([^/?#]+)", None)
        return m.group(1) if m else ""

    def xǁRetroAchievementsProviderǁ_extract_username__mutmut_14(self, soup: BeautifulSoup, url: str) -> str:
        h1 = soup.find("h1")
        if h1 and h1.get_text(strip=True):
            return h1.get_text(strip=True)
        m = re.search(url)
        return m.group(1) if m else ""

    def xǁRetroAchievementsProviderǁ_extract_username__mutmut_15(self, soup: BeautifulSoup, url: str) -> str:
        h1 = soup.find("h1")
        if h1 and h1.get_text(strip=True):
            return h1.get_text(strip=True)
        m = re.search(r"/user/([^/?#]+)", )
        return m.group(1) if m else ""

    def xǁRetroAchievementsProviderǁ_extract_username__mutmut_16(self, soup: BeautifulSoup, url: str) -> str:
        h1 = soup.find("h1")
        if h1 and h1.get_text(strip=True):
            return h1.get_text(strip=True)
        m = re.search(r"XX/user/([^/?#]+)XX", url)
        return m.group(1) if m else ""

    def xǁRetroAchievementsProviderǁ_extract_username__mutmut_17(self, soup: BeautifulSoup, url: str) -> str:
        h1 = soup.find("h1")
        if h1 and h1.get_text(strip=True):
            return h1.get_text(strip=True)
        m = re.search(r"/user/([^/?#]+)", url)
        return m.group(1) if m else ""

    def xǁRetroAchievementsProviderǁ_extract_username__mutmut_18(self, soup: BeautifulSoup, url: str) -> str:
        h1 = soup.find("h1")
        if h1 and h1.get_text(strip=True):
            return h1.get_text(strip=True)
        m = re.search(r"/USER/([^/?#]+)", url)
        return m.group(1) if m else ""

    def xǁRetroAchievementsProviderǁ_extract_username__mutmut_19(self, soup: BeautifulSoup, url: str) -> str:
        h1 = soup.find("h1")
        if h1 and h1.get_text(strip=True):
            return h1.get_text(strip=True)
        m = re.search(r"/user/([^/?#]+)", url)
        return m.group(None) if m else ""

    def xǁRetroAchievementsProviderǁ_extract_username__mutmut_20(self, soup: BeautifulSoup, url: str) -> str:
        h1 = soup.find("h1")
        if h1 and h1.get_text(strip=True):
            return h1.get_text(strip=True)
        m = re.search(r"/user/([^/?#]+)", url)
        return m.group(2) if m else ""

    def xǁRetroAchievementsProviderǁ_extract_username__mutmut_21(self, soup: BeautifulSoup, url: str) -> str:
        h1 = soup.find("h1")
        if h1 and h1.get_text(strip=True):
            return h1.get_text(strip=True)
        m = re.search(r"/user/([^/?#]+)", url)
        return m.group(1) if m else "XXXX"
    
    xǁRetroAchievementsProviderǁ_extract_username__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁRetroAchievementsProviderǁ_extract_username__mutmut_1': xǁRetroAchievementsProviderǁ_extract_username__mutmut_1, 
        'xǁRetroAchievementsProviderǁ_extract_username__mutmut_2': xǁRetroAchievementsProviderǁ_extract_username__mutmut_2, 
        'xǁRetroAchievementsProviderǁ_extract_username__mutmut_3': xǁRetroAchievementsProviderǁ_extract_username__mutmut_3, 
        'xǁRetroAchievementsProviderǁ_extract_username__mutmut_4': xǁRetroAchievementsProviderǁ_extract_username__mutmut_4, 
        'xǁRetroAchievementsProviderǁ_extract_username__mutmut_5': xǁRetroAchievementsProviderǁ_extract_username__mutmut_5, 
        'xǁRetroAchievementsProviderǁ_extract_username__mutmut_6': xǁRetroAchievementsProviderǁ_extract_username__mutmut_6, 
        'xǁRetroAchievementsProviderǁ_extract_username__mutmut_7': xǁRetroAchievementsProviderǁ_extract_username__mutmut_7, 
        'xǁRetroAchievementsProviderǁ_extract_username__mutmut_8': xǁRetroAchievementsProviderǁ_extract_username__mutmut_8, 
        'xǁRetroAchievementsProviderǁ_extract_username__mutmut_9': xǁRetroAchievementsProviderǁ_extract_username__mutmut_9, 
        'xǁRetroAchievementsProviderǁ_extract_username__mutmut_10': xǁRetroAchievementsProviderǁ_extract_username__mutmut_10, 
        'xǁRetroAchievementsProviderǁ_extract_username__mutmut_11': xǁRetroAchievementsProviderǁ_extract_username__mutmut_11, 
        'xǁRetroAchievementsProviderǁ_extract_username__mutmut_12': xǁRetroAchievementsProviderǁ_extract_username__mutmut_12, 
        'xǁRetroAchievementsProviderǁ_extract_username__mutmut_13': xǁRetroAchievementsProviderǁ_extract_username__mutmut_13, 
        'xǁRetroAchievementsProviderǁ_extract_username__mutmut_14': xǁRetroAchievementsProviderǁ_extract_username__mutmut_14, 
        'xǁRetroAchievementsProviderǁ_extract_username__mutmut_15': xǁRetroAchievementsProviderǁ_extract_username__mutmut_15, 
        'xǁRetroAchievementsProviderǁ_extract_username__mutmut_16': xǁRetroAchievementsProviderǁ_extract_username__mutmut_16, 
        'xǁRetroAchievementsProviderǁ_extract_username__mutmut_17': xǁRetroAchievementsProviderǁ_extract_username__mutmut_17, 
        'xǁRetroAchievementsProviderǁ_extract_username__mutmut_18': xǁRetroAchievementsProviderǁ_extract_username__mutmut_18, 
        'xǁRetroAchievementsProviderǁ_extract_username__mutmut_19': xǁRetroAchievementsProviderǁ_extract_username__mutmut_19, 
        'xǁRetroAchievementsProviderǁ_extract_username__mutmut_20': xǁRetroAchievementsProviderǁ_extract_username__mutmut_20, 
        'xǁRetroAchievementsProviderǁ_extract_username__mutmut_21': xǁRetroAchievementsProviderǁ_extract_username__mutmut_21
    }
    
    def _extract_username(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁRetroAchievementsProviderǁ_extract_username__mutmut_orig"), object.__getattribute__(self, "xǁRetroAchievementsProviderǁ_extract_username__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _extract_username.__signature__ = _mutmut_signature(xǁRetroAchievementsProviderǁ_extract_username__mutmut_orig)
    xǁRetroAchievementsProviderǁ_extract_username__mutmut_orig.__name__ = 'xǁRetroAchievementsProviderǁ_extract_username'

    def xǁRetroAchievementsProviderǁ_extract_avatar__mutmut_orig(self, soup: BeautifulSoup) -> str | None:
        og = soup.find("meta", property="og:image")
        if og and og.get("content"):
            return og["content"]
        img = soup.select_one("img[src*='UserPic'], img[alt*='avatar' i]")
        if img and img.get("src"):
            return img["src"]
        return None

    def xǁRetroAchievementsProviderǁ_extract_avatar__mutmut_1(self, soup: BeautifulSoup) -> str | None:
        og = None
        if og and og.get("content"):
            return og["content"]
        img = soup.select_one("img[src*='UserPic'], img[alt*='avatar' i]")
        if img and img.get("src"):
            return img["src"]
        return None

    def xǁRetroAchievementsProviderǁ_extract_avatar__mutmut_2(self, soup: BeautifulSoup) -> str | None:
        og = soup.find(None, property="og:image")
        if og and og.get("content"):
            return og["content"]
        img = soup.select_one("img[src*='UserPic'], img[alt*='avatar' i]")
        if img and img.get("src"):
            return img["src"]
        return None

    def xǁRetroAchievementsProviderǁ_extract_avatar__mutmut_3(self, soup: BeautifulSoup) -> str | None:
        og = soup.find("meta", property=None)
        if og and og.get("content"):
            return og["content"]
        img = soup.select_one("img[src*='UserPic'], img[alt*='avatar' i]")
        if img and img.get("src"):
            return img["src"]
        return None

    def xǁRetroAchievementsProviderǁ_extract_avatar__mutmut_4(self, soup: BeautifulSoup) -> str | None:
        og = soup.find(property="og:image")
        if og and og.get("content"):
            return og["content"]
        img = soup.select_one("img[src*='UserPic'], img[alt*='avatar' i]")
        if img and img.get("src"):
            return img["src"]
        return None

    def xǁRetroAchievementsProviderǁ_extract_avatar__mutmut_5(self, soup: BeautifulSoup) -> str | None:
        og = soup.find("meta", )
        if og and og.get("content"):
            return og["content"]
        img = soup.select_one("img[src*='UserPic'], img[alt*='avatar' i]")
        if img and img.get("src"):
            return img["src"]
        return None

    def xǁRetroAchievementsProviderǁ_extract_avatar__mutmut_6(self, soup: BeautifulSoup) -> str | None:
        og = soup.rfind("meta", property="og:image")
        if og and og.get("content"):
            return og["content"]
        img = soup.select_one("img[src*='UserPic'], img[alt*='avatar' i]")
        if img and img.get("src"):
            return img["src"]
        return None

    def xǁRetroAchievementsProviderǁ_extract_avatar__mutmut_7(self, soup: BeautifulSoup) -> str | None:
        og = soup.find("XXmetaXX", property="og:image")
        if og and og.get("content"):
            return og["content"]
        img = soup.select_one("img[src*='UserPic'], img[alt*='avatar' i]")
        if img and img.get("src"):
            return img["src"]
        return None

    def xǁRetroAchievementsProviderǁ_extract_avatar__mutmut_8(self, soup: BeautifulSoup) -> str | None:
        og = soup.find("META", property="og:image")
        if og and og.get("content"):
            return og["content"]
        img = soup.select_one("img[src*='UserPic'], img[alt*='avatar' i]")
        if img and img.get("src"):
            return img["src"]
        return None

    def xǁRetroAchievementsProviderǁ_extract_avatar__mutmut_9(self, soup: BeautifulSoup) -> str | None:
        og = soup.find("meta", property="XXog:imageXX")
        if og and og.get("content"):
            return og["content"]
        img = soup.select_one("img[src*='UserPic'], img[alt*='avatar' i]")
        if img and img.get("src"):
            return img["src"]
        return None

    def xǁRetroAchievementsProviderǁ_extract_avatar__mutmut_10(self, soup: BeautifulSoup) -> str | None:
        og = soup.find("meta", property="OG:IMAGE")
        if og and og.get("content"):
            return og["content"]
        img = soup.select_one("img[src*='UserPic'], img[alt*='avatar' i]")
        if img and img.get("src"):
            return img["src"]
        return None

    def xǁRetroAchievementsProviderǁ_extract_avatar__mutmut_11(self, soup: BeautifulSoup) -> str | None:
        og = soup.find("meta", property="og:image")
        if og or og.get("content"):
            return og["content"]
        img = soup.select_one("img[src*='UserPic'], img[alt*='avatar' i]")
        if img and img.get("src"):
            return img["src"]
        return None

    def xǁRetroAchievementsProviderǁ_extract_avatar__mutmut_12(self, soup: BeautifulSoup) -> str | None:
        og = soup.find("meta", property="og:image")
        if og and og.get(None):
            return og["content"]
        img = soup.select_one("img[src*='UserPic'], img[alt*='avatar' i]")
        if img and img.get("src"):
            return img["src"]
        return None

    def xǁRetroAchievementsProviderǁ_extract_avatar__mutmut_13(self, soup: BeautifulSoup) -> str | None:
        og = soup.find("meta", property="og:image")
        if og and og.get("XXcontentXX"):
            return og["content"]
        img = soup.select_one("img[src*='UserPic'], img[alt*='avatar' i]")
        if img and img.get("src"):
            return img["src"]
        return None

    def xǁRetroAchievementsProviderǁ_extract_avatar__mutmut_14(self, soup: BeautifulSoup) -> str | None:
        og = soup.find("meta", property="og:image")
        if og and og.get("CONTENT"):
            return og["content"]
        img = soup.select_one("img[src*='UserPic'], img[alt*='avatar' i]")
        if img and img.get("src"):
            return img["src"]
        return None

    def xǁRetroAchievementsProviderǁ_extract_avatar__mutmut_15(self, soup: BeautifulSoup) -> str | None:
        og = soup.find("meta", property="og:image")
        if og and og.get("content"):
            return og["XXcontentXX"]
        img = soup.select_one("img[src*='UserPic'], img[alt*='avatar' i]")
        if img and img.get("src"):
            return img["src"]
        return None

    def xǁRetroAchievementsProviderǁ_extract_avatar__mutmut_16(self, soup: BeautifulSoup) -> str | None:
        og = soup.find("meta", property="og:image")
        if og and og.get("content"):
            return og["CONTENT"]
        img = soup.select_one("img[src*='UserPic'], img[alt*='avatar' i]")
        if img and img.get("src"):
            return img["src"]
        return None

    def xǁRetroAchievementsProviderǁ_extract_avatar__mutmut_17(self, soup: BeautifulSoup) -> str | None:
        og = soup.find("meta", property="og:image")
        if og and og.get("content"):
            return og["content"]
        img = None
        if img and img.get("src"):
            return img["src"]
        return None

    def xǁRetroAchievementsProviderǁ_extract_avatar__mutmut_18(self, soup: BeautifulSoup) -> str | None:
        og = soup.find("meta", property="og:image")
        if og and og.get("content"):
            return og["content"]
        img = soup.select_one(None)
        if img and img.get("src"):
            return img["src"]
        return None

    def xǁRetroAchievementsProviderǁ_extract_avatar__mutmut_19(self, soup: BeautifulSoup) -> str | None:
        og = soup.find("meta", property="og:image")
        if og and og.get("content"):
            return og["content"]
        img = soup.select_one("XXimg[src*='UserPic'], img[alt*='avatar' i]XX")
        if img and img.get("src"):
            return img["src"]
        return None

    def xǁRetroAchievementsProviderǁ_extract_avatar__mutmut_20(self, soup: BeautifulSoup) -> str | None:
        og = soup.find("meta", property="og:image")
        if og and og.get("content"):
            return og["content"]
        img = soup.select_one("img[src*='userpic'], img[alt*='avatar' i]")
        if img and img.get("src"):
            return img["src"]
        return None

    def xǁRetroAchievementsProviderǁ_extract_avatar__mutmut_21(self, soup: BeautifulSoup) -> str | None:
        og = soup.find("meta", property="og:image")
        if og and og.get("content"):
            return og["content"]
        img = soup.select_one("IMG[SRC*='USERPIC'], IMG[ALT*='AVATAR' I]")
        if img and img.get("src"):
            return img["src"]
        return None

    def xǁRetroAchievementsProviderǁ_extract_avatar__mutmut_22(self, soup: BeautifulSoup) -> str | None:
        og = soup.find("meta", property="og:image")
        if og and og.get("content"):
            return og["content"]
        img = soup.select_one("img[src*='UserPic'], img[alt*='avatar' i]")
        if img or img.get("src"):
            return img["src"]
        return None

    def xǁRetroAchievementsProviderǁ_extract_avatar__mutmut_23(self, soup: BeautifulSoup) -> str | None:
        og = soup.find("meta", property="og:image")
        if og and og.get("content"):
            return og["content"]
        img = soup.select_one("img[src*='UserPic'], img[alt*='avatar' i]")
        if img and img.get(None):
            return img["src"]
        return None

    def xǁRetroAchievementsProviderǁ_extract_avatar__mutmut_24(self, soup: BeautifulSoup) -> str | None:
        og = soup.find("meta", property="og:image")
        if og and og.get("content"):
            return og["content"]
        img = soup.select_one("img[src*='UserPic'], img[alt*='avatar' i]")
        if img and img.get("XXsrcXX"):
            return img["src"]
        return None

    def xǁRetroAchievementsProviderǁ_extract_avatar__mutmut_25(self, soup: BeautifulSoup) -> str | None:
        og = soup.find("meta", property="og:image")
        if og and og.get("content"):
            return og["content"]
        img = soup.select_one("img[src*='UserPic'], img[alt*='avatar' i]")
        if img and img.get("SRC"):
            return img["src"]
        return None

    def xǁRetroAchievementsProviderǁ_extract_avatar__mutmut_26(self, soup: BeautifulSoup) -> str | None:
        og = soup.find("meta", property="og:image")
        if og and og.get("content"):
            return og["content"]
        img = soup.select_one("img[src*='UserPic'], img[alt*='avatar' i]")
        if img and img.get("src"):
            return img["XXsrcXX"]
        return None

    def xǁRetroAchievementsProviderǁ_extract_avatar__mutmut_27(self, soup: BeautifulSoup) -> str | None:
        og = soup.find("meta", property="og:image")
        if og and og.get("content"):
            return og["content"]
        img = soup.select_one("img[src*='UserPic'], img[alt*='avatar' i]")
        if img and img.get("src"):
            return img["SRC"]
        return None
    
    xǁRetroAchievementsProviderǁ_extract_avatar__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁRetroAchievementsProviderǁ_extract_avatar__mutmut_1': xǁRetroAchievementsProviderǁ_extract_avatar__mutmut_1, 
        'xǁRetroAchievementsProviderǁ_extract_avatar__mutmut_2': xǁRetroAchievementsProviderǁ_extract_avatar__mutmut_2, 
        'xǁRetroAchievementsProviderǁ_extract_avatar__mutmut_3': xǁRetroAchievementsProviderǁ_extract_avatar__mutmut_3, 
        'xǁRetroAchievementsProviderǁ_extract_avatar__mutmut_4': xǁRetroAchievementsProviderǁ_extract_avatar__mutmut_4, 
        'xǁRetroAchievementsProviderǁ_extract_avatar__mutmut_5': xǁRetroAchievementsProviderǁ_extract_avatar__mutmut_5, 
        'xǁRetroAchievementsProviderǁ_extract_avatar__mutmut_6': xǁRetroAchievementsProviderǁ_extract_avatar__mutmut_6, 
        'xǁRetroAchievementsProviderǁ_extract_avatar__mutmut_7': xǁRetroAchievementsProviderǁ_extract_avatar__mutmut_7, 
        'xǁRetroAchievementsProviderǁ_extract_avatar__mutmut_8': xǁRetroAchievementsProviderǁ_extract_avatar__mutmut_8, 
        'xǁRetroAchievementsProviderǁ_extract_avatar__mutmut_9': xǁRetroAchievementsProviderǁ_extract_avatar__mutmut_9, 
        'xǁRetroAchievementsProviderǁ_extract_avatar__mutmut_10': xǁRetroAchievementsProviderǁ_extract_avatar__mutmut_10, 
        'xǁRetroAchievementsProviderǁ_extract_avatar__mutmut_11': xǁRetroAchievementsProviderǁ_extract_avatar__mutmut_11, 
        'xǁRetroAchievementsProviderǁ_extract_avatar__mutmut_12': xǁRetroAchievementsProviderǁ_extract_avatar__mutmut_12, 
        'xǁRetroAchievementsProviderǁ_extract_avatar__mutmut_13': xǁRetroAchievementsProviderǁ_extract_avatar__mutmut_13, 
        'xǁRetroAchievementsProviderǁ_extract_avatar__mutmut_14': xǁRetroAchievementsProviderǁ_extract_avatar__mutmut_14, 
        'xǁRetroAchievementsProviderǁ_extract_avatar__mutmut_15': xǁRetroAchievementsProviderǁ_extract_avatar__mutmut_15, 
        'xǁRetroAchievementsProviderǁ_extract_avatar__mutmut_16': xǁRetroAchievementsProviderǁ_extract_avatar__mutmut_16, 
        'xǁRetroAchievementsProviderǁ_extract_avatar__mutmut_17': xǁRetroAchievementsProviderǁ_extract_avatar__mutmut_17, 
        'xǁRetroAchievementsProviderǁ_extract_avatar__mutmut_18': xǁRetroAchievementsProviderǁ_extract_avatar__mutmut_18, 
        'xǁRetroAchievementsProviderǁ_extract_avatar__mutmut_19': xǁRetroAchievementsProviderǁ_extract_avatar__mutmut_19, 
        'xǁRetroAchievementsProviderǁ_extract_avatar__mutmut_20': xǁRetroAchievementsProviderǁ_extract_avatar__mutmut_20, 
        'xǁRetroAchievementsProviderǁ_extract_avatar__mutmut_21': xǁRetroAchievementsProviderǁ_extract_avatar__mutmut_21, 
        'xǁRetroAchievementsProviderǁ_extract_avatar__mutmut_22': xǁRetroAchievementsProviderǁ_extract_avatar__mutmut_22, 
        'xǁRetroAchievementsProviderǁ_extract_avatar__mutmut_23': xǁRetroAchievementsProviderǁ_extract_avatar__mutmut_23, 
        'xǁRetroAchievementsProviderǁ_extract_avatar__mutmut_24': xǁRetroAchievementsProviderǁ_extract_avatar__mutmut_24, 
        'xǁRetroAchievementsProviderǁ_extract_avatar__mutmut_25': xǁRetroAchievementsProviderǁ_extract_avatar__mutmut_25, 
        'xǁRetroAchievementsProviderǁ_extract_avatar__mutmut_26': xǁRetroAchievementsProviderǁ_extract_avatar__mutmut_26, 
        'xǁRetroAchievementsProviderǁ_extract_avatar__mutmut_27': xǁRetroAchievementsProviderǁ_extract_avatar__mutmut_27
    }
    
    def _extract_avatar(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁRetroAchievementsProviderǁ_extract_avatar__mutmut_orig"), object.__getattribute__(self, "xǁRetroAchievementsProviderǁ_extract_avatar__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _extract_avatar.__signature__ = _mutmut_signature(xǁRetroAchievementsProviderǁ_extract_avatar__mutmut_orig)
    xǁRetroAchievementsProviderǁ_extract_avatar__mutmut_orig.__name__ = 'xǁRetroAchievementsProviderǁ_extract_avatar'

    def xǁRetroAchievementsProviderǁ_find_number__mutmut_orig(self, text: str, label_pat: str) -> int | None:
        m = re.search(rf"{label_pat}[^0-9]{{0,20}}([\d,]+)", text, re.I)
        return parse_int(m.group(1)) if m else None

    def xǁRetroAchievementsProviderǁ_find_number__mutmut_1(self, text: str, label_pat: str) -> int | None:
        m = None
        return parse_int(m.group(1)) if m else None

    def xǁRetroAchievementsProviderǁ_find_number__mutmut_2(self, text: str, label_pat: str) -> int | None:
        m = re.search(None, text, re.I)
        return parse_int(m.group(1)) if m else None

    def xǁRetroAchievementsProviderǁ_find_number__mutmut_3(self, text: str, label_pat: str) -> int | None:
        m = re.search(rf"{label_pat}[^0-9]{{0,20}}([\d,]+)", None, re.I)
        return parse_int(m.group(1)) if m else None

    def xǁRetroAchievementsProviderǁ_find_number__mutmut_4(self, text: str, label_pat: str) -> int | None:
        m = re.search(rf"{label_pat}[^0-9]{{0,20}}([\d,]+)", text, None)
        return parse_int(m.group(1)) if m else None

    def xǁRetroAchievementsProviderǁ_find_number__mutmut_5(self, text: str, label_pat: str) -> int | None:
        m = re.search(text, re.I)
        return parse_int(m.group(1)) if m else None

    def xǁRetroAchievementsProviderǁ_find_number__mutmut_6(self, text: str, label_pat: str) -> int | None:
        m = re.search(rf"{label_pat}[^0-9]{{0,20}}([\d,]+)", re.I)
        return parse_int(m.group(1)) if m else None

    def xǁRetroAchievementsProviderǁ_find_number__mutmut_7(self, text: str, label_pat: str) -> int | None:
        m = re.search(rf"{label_pat}[^0-9]{{0,20}}([\d,]+)", text, )
        return parse_int(m.group(1)) if m else None

    def xǁRetroAchievementsProviderǁ_find_number__mutmut_8(self, text: str, label_pat: str) -> int | None:
        m = re.search(rf"{label_pat}[^0-9]{{0,20}}([\d,]+)", text, re.I)
        return parse_int(None) if m else None

    def xǁRetroAchievementsProviderǁ_find_number__mutmut_9(self, text: str, label_pat: str) -> int | None:
        m = re.search(rf"{label_pat}[^0-9]{{0,20}}([\d,]+)", text, re.I)
        return parse_int(m.group(None)) if m else None

    def xǁRetroAchievementsProviderǁ_find_number__mutmut_10(self, text: str, label_pat: str) -> int | None:
        m = re.search(rf"{label_pat}[^0-9]{{0,20}}([\d,]+)", text, re.I)
        return parse_int(m.group(2)) if m else None
    
    xǁRetroAchievementsProviderǁ_find_number__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁRetroAchievementsProviderǁ_find_number__mutmut_1': xǁRetroAchievementsProviderǁ_find_number__mutmut_1, 
        'xǁRetroAchievementsProviderǁ_find_number__mutmut_2': xǁRetroAchievementsProviderǁ_find_number__mutmut_2, 
        'xǁRetroAchievementsProviderǁ_find_number__mutmut_3': xǁRetroAchievementsProviderǁ_find_number__mutmut_3, 
        'xǁRetroAchievementsProviderǁ_find_number__mutmut_4': xǁRetroAchievementsProviderǁ_find_number__mutmut_4, 
        'xǁRetroAchievementsProviderǁ_find_number__mutmut_5': xǁRetroAchievementsProviderǁ_find_number__mutmut_5, 
        'xǁRetroAchievementsProviderǁ_find_number__mutmut_6': xǁRetroAchievementsProviderǁ_find_number__mutmut_6, 
        'xǁRetroAchievementsProviderǁ_find_number__mutmut_7': xǁRetroAchievementsProviderǁ_find_number__mutmut_7, 
        'xǁRetroAchievementsProviderǁ_find_number__mutmut_8': xǁRetroAchievementsProviderǁ_find_number__mutmut_8, 
        'xǁRetroAchievementsProviderǁ_find_number__mutmut_9': xǁRetroAchievementsProviderǁ_find_number__mutmut_9, 
        'xǁRetroAchievementsProviderǁ_find_number__mutmut_10': xǁRetroAchievementsProviderǁ_find_number__mutmut_10
    }
    
    def _find_number(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁRetroAchievementsProviderǁ_find_number__mutmut_orig"), object.__getattribute__(self, "xǁRetroAchievementsProviderǁ_find_number__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _find_number.__signature__ = _mutmut_signature(xǁRetroAchievementsProviderǁ_find_number__mutmut_orig)
    xǁRetroAchievementsProviderǁ_find_number__mutmut_orig.__name__ = 'xǁRetroAchievementsProviderǁ_find_number'

    def xǁRetroAchievementsProviderǁ_find_float__mutmut_orig(self, text: str, label_pat: str) -> float | None:
        m = re.search(rf"{label_pat}[^0-9]{{0,20}}([\d,]+\.?\d*)", text, re.I)
        return parse_float(m.group(1)) if m else None

    def xǁRetroAchievementsProviderǁ_find_float__mutmut_1(self, text: str, label_pat: str) -> float | None:
        m = None
        return parse_float(m.group(1)) if m else None

    def xǁRetroAchievementsProviderǁ_find_float__mutmut_2(self, text: str, label_pat: str) -> float | None:
        m = re.search(None, text, re.I)
        return parse_float(m.group(1)) if m else None

    def xǁRetroAchievementsProviderǁ_find_float__mutmut_3(self, text: str, label_pat: str) -> float | None:
        m = re.search(rf"{label_pat}[^0-9]{{0,20}}([\d,]+\.?\d*)", None, re.I)
        return parse_float(m.group(1)) if m else None

    def xǁRetroAchievementsProviderǁ_find_float__mutmut_4(self, text: str, label_pat: str) -> float | None:
        m = re.search(rf"{label_pat}[^0-9]{{0,20}}([\d,]+\.?\d*)", text, None)
        return parse_float(m.group(1)) if m else None

    def xǁRetroAchievementsProviderǁ_find_float__mutmut_5(self, text: str, label_pat: str) -> float | None:
        m = re.search(text, re.I)
        return parse_float(m.group(1)) if m else None

    def xǁRetroAchievementsProviderǁ_find_float__mutmut_6(self, text: str, label_pat: str) -> float | None:
        m = re.search(rf"{label_pat}[^0-9]{{0,20}}([\d,]+\.?\d*)", re.I)
        return parse_float(m.group(1)) if m else None

    def xǁRetroAchievementsProviderǁ_find_float__mutmut_7(self, text: str, label_pat: str) -> float | None:
        m = re.search(rf"{label_pat}[^0-9]{{0,20}}([\d,]+\.?\d*)", text, )
        return parse_float(m.group(1)) if m else None

    def xǁRetroAchievementsProviderǁ_find_float__mutmut_8(self, text: str, label_pat: str) -> float | None:
        m = re.search(rf"{label_pat}[^0-9]{{0,20}}([\d,]+\.?\d*)", text, re.I)
        return parse_float(None) if m else None

    def xǁRetroAchievementsProviderǁ_find_float__mutmut_9(self, text: str, label_pat: str) -> float | None:
        m = re.search(rf"{label_pat}[^0-9]{{0,20}}([\d,]+\.?\d*)", text, re.I)
        return parse_float(m.group(None)) if m else None

    def xǁRetroAchievementsProviderǁ_find_float__mutmut_10(self, text: str, label_pat: str) -> float | None:
        m = re.search(rf"{label_pat}[^0-9]{{0,20}}([\d,]+\.?\d*)", text, re.I)
        return parse_float(m.group(2)) if m else None
    
    xǁRetroAchievementsProviderǁ_find_float__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁRetroAchievementsProviderǁ_find_float__mutmut_1': xǁRetroAchievementsProviderǁ_find_float__mutmut_1, 
        'xǁRetroAchievementsProviderǁ_find_float__mutmut_2': xǁRetroAchievementsProviderǁ_find_float__mutmut_2, 
        'xǁRetroAchievementsProviderǁ_find_float__mutmut_3': xǁRetroAchievementsProviderǁ_find_float__mutmut_3, 
        'xǁRetroAchievementsProviderǁ_find_float__mutmut_4': xǁRetroAchievementsProviderǁ_find_float__mutmut_4, 
        'xǁRetroAchievementsProviderǁ_find_float__mutmut_5': xǁRetroAchievementsProviderǁ_find_float__mutmut_5, 
        'xǁRetroAchievementsProviderǁ_find_float__mutmut_6': xǁRetroAchievementsProviderǁ_find_float__mutmut_6, 
        'xǁRetroAchievementsProviderǁ_find_float__mutmut_7': xǁRetroAchievementsProviderǁ_find_float__mutmut_7, 
        'xǁRetroAchievementsProviderǁ_find_float__mutmut_8': xǁRetroAchievementsProviderǁ_find_float__mutmut_8, 
        'xǁRetroAchievementsProviderǁ_find_float__mutmut_9': xǁRetroAchievementsProviderǁ_find_float__mutmut_9, 
        'xǁRetroAchievementsProviderǁ_find_float__mutmut_10': xǁRetroAchievementsProviderǁ_find_float__mutmut_10
    }
    
    def _find_float(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁRetroAchievementsProviderǁ_find_float__mutmut_orig"), object.__getattribute__(self, "xǁRetroAchievementsProviderǁ_find_float__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _find_float.__signature__ = _mutmut_signature(xǁRetroAchievementsProviderǁ_find_float__mutmut_orig)
    xǁRetroAchievementsProviderǁ_find_float__mutmut_orig.__name__ = 'xǁRetroAchievementsProviderǁ_find_float'

    def xǁRetroAchievementsProviderǁ_username_from_url__mutmut_orig(self, url: str) -> str:
        m = re.search(r"/user/([^/?#]+)", url)
        return m.group(1) if m else ""

    def xǁRetroAchievementsProviderǁ_username_from_url__mutmut_1(self, url: str) -> str:
        m = None
        return m.group(1) if m else ""

    def xǁRetroAchievementsProviderǁ_username_from_url__mutmut_2(self, url: str) -> str:
        m = re.search(None, url)
        return m.group(1) if m else ""

    def xǁRetroAchievementsProviderǁ_username_from_url__mutmut_3(self, url: str) -> str:
        m = re.search(r"/user/([^/?#]+)", None)
        return m.group(1) if m else ""

    def xǁRetroAchievementsProviderǁ_username_from_url__mutmut_4(self, url: str) -> str:
        m = re.search(url)
        return m.group(1) if m else ""

    def xǁRetroAchievementsProviderǁ_username_from_url__mutmut_5(self, url: str) -> str:
        m = re.search(r"/user/([^/?#]+)", )
        return m.group(1) if m else ""

    def xǁRetroAchievementsProviderǁ_username_from_url__mutmut_6(self, url: str) -> str:
        m = re.search(r"XX/user/([^/?#]+)XX", url)
        return m.group(1) if m else ""

    def xǁRetroAchievementsProviderǁ_username_from_url__mutmut_7(self, url: str) -> str:
        m = re.search(r"/user/([^/?#]+)", url)
        return m.group(1) if m else ""

    def xǁRetroAchievementsProviderǁ_username_from_url__mutmut_8(self, url: str) -> str:
        m = re.search(r"/USER/([^/?#]+)", url)
        return m.group(1) if m else ""

    def xǁRetroAchievementsProviderǁ_username_from_url__mutmut_9(self, url: str) -> str:
        m = re.search(r"/user/([^/?#]+)", url)
        return m.group(None) if m else ""

    def xǁRetroAchievementsProviderǁ_username_from_url__mutmut_10(self, url: str) -> str:
        m = re.search(r"/user/([^/?#]+)", url)
        return m.group(2) if m else ""

    def xǁRetroAchievementsProviderǁ_username_from_url__mutmut_11(self, url: str) -> str:
        m = re.search(r"/user/([^/?#]+)", url)
        return m.group(1) if m else "XXXX"
    
    xǁRetroAchievementsProviderǁ_username_from_url__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁRetroAchievementsProviderǁ_username_from_url__mutmut_1': xǁRetroAchievementsProviderǁ_username_from_url__mutmut_1, 
        'xǁRetroAchievementsProviderǁ_username_from_url__mutmut_2': xǁRetroAchievementsProviderǁ_username_from_url__mutmut_2, 
        'xǁRetroAchievementsProviderǁ_username_from_url__mutmut_3': xǁRetroAchievementsProviderǁ_username_from_url__mutmut_3, 
        'xǁRetroAchievementsProviderǁ_username_from_url__mutmut_4': xǁRetroAchievementsProviderǁ_username_from_url__mutmut_4, 
        'xǁRetroAchievementsProviderǁ_username_from_url__mutmut_5': xǁRetroAchievementsProviderǁ_username_from_url__mutmut_5, 
        'xǁRetroAchievementsProviderǁ_username_from_url__mutmut_6': xǁRetroAchievementsProviderǁ_username_from_url__mutmut_6, 
        'xǁRetroAchievementsProviderǁ_username_from_url__mutmut_7': xǁRetroAchievementsProviderǁ_username_from_url__mutmut_7, 
        'xǁRetroAchievementsProviderǁ_username_from_url__mutmut_8': xǁRetroAchievementsProviderǁ_username_from_url__mutmut_8, 
        'xǁRetroAchievementsProviderǁ_username_from_url__mutmut_9': xǁRetroAchievementsProviderǁ_username_from_url__mutmut_9, 
        'xǁRetroAchievementsProviderǁ_username_from_url__mutmut_10': xǁRetroAchievementsProviderǁ_username_from_url__mutmut_10, 
        'xǁRetroAchievementsProviderǁ_username_from_url__mutmut_11': xǁRetroAchievementsProviderǁ_username_from_url__mutmut_11
    }
    
    def _username_from_url(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁRetroAchievementsProviderǁ_username_from_url__mutmut_orig"), object.__getattribute__(self, "xǁRetroAchievementsProviderǁ_username_from_url__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _username_from_url.__signature__ = _mutmut_signature(xǁRetroAchievementsProviderǁ_username_from_url__mutmut_orig)
    xǁRetroAchievementsProviderǁ_username_from_url__mutmut_orig.__name__ = 'xǁRetroAchievementsProviderǁ_username_from_url'

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_orig(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_1(self, username: str, api_user: str, api_key: str) -> PlatformStats:
        """Use the official JSON API — bypasses Cloudflare entirely."""
        base = None
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

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_2(self, username: str, api_user: str, api_key: str) -> PlatformStats:
        """Use the official JSON API — bypasses Cloudflare entirely."""
        base = "XXhttps://retroachievements.org/APIXX"
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

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_3(self, username: str, api_user: str, api_key: str) -> PlatformStats:
        """Use the official JSON API — bypasses Cloudflare entirely."""
        base = "https://retroachievements.org/api"
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

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_4(self, username: str, api_user: str, api_key: str) -> PlatformStats:
        """Use the official JSON API — bypasses Cloudflare entirely."""
        base = "HTTPS://RETROACHIEVEMENTS.ORG/API"
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

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_5(self, username: str, api_user: str, api_key: str) -> PlatformStats:
        """Use the official JSON API — bypasses Cloudflare entirely."""
        base = "https://retroachievements.org/API"
        params = None
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

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_6(self, username: str, api_user: str, api_key: str) -> PlatformStats:
        """Use the official JSON API — bypasses Cloudflare entirely."""
        base = "https://retroachievements.org/API"
        params = {"XXzXX": api_user, "y": api_key, "u": username}
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

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_7(self, username: str, api_user: str, api_key: str) -> PlatformStats:
        """Use the official JSON API — bypasses Cloudflare entirely."""
        base = "https://retroachievements.org/API"
        params = {"Z": api_user, "y": api_key, "u": username}
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

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_8(self, username: str, api_user: str, api_key: str) -> PlatformStats:
        """Use the official JSON API — bypasses Cloudflare entirely."""
        base = "https://retroachievements.org/API"
        params = {"z": api_user, "XXyXX": api_key, "u": username}
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

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_9(self, username: str, api_user: str, api_key: str) -> PlatformStats:
        """Use the official JSON API — bypasses Cloudflare entirely."""
        base = "https://retroachievements.org/API"
        params = {"z": api_user, "Y": api_key, "u": username}
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

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_10(self, username: str, api_user: str, api_key: str) -> PlatformStats:
        """Use the official JSON API — bypasses Cloudflare entirely."""
        base = "https://retroachievements.org/API"
        params = {"z": api_user, "y": api_key, "XXuXX": username}
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

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_11(self, username: str, api_user: str, api_key: str) -> PlatformStats:
        """Use the official JSON API — bypasses Cloudflare entirely."""
        base = "https://retroachievements.org/API"
        params = {"z": api_user, "y": api_key, "U": username}
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

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_12(self, username: str, api_user: str, api_key: str) -> PlatformStats:
        """Use the official JSON API — bypasses Cloudflare entirely."""
        base = "https://retroachievements.org/API"
        params = {"z": api_user, "y": api_key, "u": username}
        try:
            summary = None
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

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_13(self, username: str, api_user: str, api_key: str) -> PlatformStats:
        """Use the official JSON API — bypasses Cloudflare entirely."""
        base = "https://retroachievements.org/API"
        params = {"z": api_user, "y": api_key, "u": username}
        try:
            summary = requests.get(
                None, params=params, timeout=self.timeout
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

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_14(self, username: str, api_user: str, api_key: str) -> PlatformStats:
        """Use the official JSON API — bypasses Cloudflare entirely."""
        base = "https://retroachievements.org/API"
        params = {"z": api_user, "y": api_key, "u": username}
        try:
            summary = requests.get(
                f"{base}/API_GetUserSummary.php", params=None, timeout=self.timeout
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

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_15(self, username: str, api_user: str, api_key: str) -> PlatformStats:
        """Use the official JSON API — bypasses Cloudflare entirely."""
        base = "https://retroachievements.org/API"
        params = {"z": api_user, "y": api_key, "u": username}
        try:
            summary = requests.get(
                f"{base}/API_GetUserSummary.php", params=params, timeout=None
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

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_16(self, username: str, api_user: str, api_key: str) -> PlatformStats:
        """Use the official JSON API — bypasses Cloudflare entirely."""
        base = "https://retroachievements.org/API"
        params = {"z": api_user, "y": api_key, "u": username}
        try:
            summary = requests.get(
                params=params, timeout=self.timeout
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

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_17(self, username: str, api_user: str, api_key: str) -> PlatformStats:
        """Use the official JSON API — bypasses Cloudflare entirely."""
        base = "https://retroachievements.org/API"
        params = {"z": api_user, "y": api_key, "u": username}
        try:
            summary = requests.get(
                f"{base}/API_GetUserSummary.php", timeout=self.timeout
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

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_18(self, username: str, api_user: str, api_key: str) -> PlatformStats:
        """Use the official JSON API — bypasses Cloudflare entirely."""
        base = "https://retroachievements.org/API"
        params = {"z": api_user, "y": api_key, "u": username}
        try:
            summary = requests.get(
                f"{base}/API_GetUserSummary.php", params=params, )
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

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_19(self, username: str, api_user: str, api_key: str) -> PlatformStats:
        """Use the official JSON API — bypasses Cloudflare entirely."""
        base = "https://retroachievements.org/API"
        params = {"z": api_user, "y": api_key, "u": username}
        try:
            summary = requests.get(
                f"{base}/API_GetUserSummary.php", params=params, timeout=self.timeout
            )
            summary.raise_for_status()
            summary_j = None
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

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_20(self, username: str, api_user: str, api_key: str) -> PlatformStats:
        """Use the official JSON API — bypasses Cloudflare entirely."""
        base = "https://retroachievements.org/API"
        params = {"z": api_user, "y": api_key, "u": username}
        try:
            summary = requests.get(
                f"{base}/API_GetUserSummary.php", params=params, timeout=self.timeout
            )
            summary.raise_for_status()
            summary_j = summary.json()
            profile = None
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

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_21(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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
                None, params=params, timeout=self.timeout
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

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_22(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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
                f"{base}/API_GetUserProfile.php", params=None, timeout=self.timeout
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

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_23(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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
                f"{base}/API_GetUserProfile.php", params=params, timeout=None
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

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_24(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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
                params=params, timeout=self.timeout
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

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_25(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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
                f"{base}/API_GetUserProfile.php", timeout=self.timeout
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

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_26(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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
                f"{base}/API_GetUserProfile.php", params=params, )
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

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_27(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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
            profile_j = None
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

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_28(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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
            awards = None
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

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_29(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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
                None, params=params, timeout=self.timeout
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

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_30(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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
                f"{base}/API_GetUserAwards.php", params=None, timeout=self.timeout
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

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_31(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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
                f"{base}/API_GetUserAwards.php", params=params, timeout=None
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

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_32(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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
                params=params, timeout=self.timeout
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

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_33(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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
                f"{base}/API_GetUserAwards.php", timeout=self.timeout
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

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_34(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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
                f"{base}/API_GetUserAwards.php", params=params, )
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

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_35(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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
            awards_j = None
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

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_36(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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
            raise ProviderError(None) from exc

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

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_37(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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

        hardcore = None
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

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_38(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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

        hardcore = parse_int(None)
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

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_39(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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

        hardcore = parse_int(summary_j.get(None))
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

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_40(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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

        hardcore = parse_int(summary_j.get("XXTotalPointsXX"))
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

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_41(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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

        hardcore = parse_int(summary_j.get("totalpoints"))
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

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_42(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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

        hardcore = parse_int(summary_j.get("TOTALPOINTS"))
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

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_43(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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
        softcore = None
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

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_44(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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
        softcore = parse_int(None)
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

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_45(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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
        softcore = parse_int(summary_j.get(None))
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

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_46(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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
        softcore = parse_int(summary_j.get("XXTotalSoftcorePointsXX"))
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

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_47(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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
        softcore = parse_int(summary_j.get("totalsoftcorepoints"))
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

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_48(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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
        softcore = parse_int(summary_j.get("TOTALSOFTCOREPOINTS"))
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

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_49(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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
        true_points = None
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

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_50(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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
        true_points = parse_int(None)
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

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_51(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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
        true_points = parse_int(summary_j.get(None))
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

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_52(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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
        true_points = parse_int(summary_j.get("XXTotalTruePointsXX"))
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

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_53(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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
        true_points = parse_int(summary_j.get("totaltruepoints"))
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

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_54(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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
        true_points = parse_int(summary_j.get("TOTALTRUEPOINTS"))
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

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_55(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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
        true_ratio = ""
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

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_56(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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
        if true_points or hardcore:
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

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_57(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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
            true_ratio = None
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

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_58(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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
            true_ratio = round(None, 2)
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

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_59(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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
            true_ratio = round(true_points / hardcore, None)
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

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_60(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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
            true_ratio = round(2)
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

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_61(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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
            true_ratio = round(true_points / hardcore, )
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

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_62(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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
            true_ratio = round(true_points * hardcore, 2)
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

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_63(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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
            true_ratio = round(true_points / hardcore, 3)
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

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_64(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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
        masteries = None
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

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_65(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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
        masteries = parse_int(None)
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

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_66(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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
        masteries = parse_int(awards_j.get(None))
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

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_67(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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
        masteries = parse_int(awards_j.get("XXMasteryAwardsCountXX"))
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

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_68(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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
        masteries = parse_int(awards_j.get("masteryawardscount"))
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

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_69(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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
        masteries = parse_int(awards_j.get("MASTERYAWARDSCOUNT"))
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

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_70(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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
        completions = None
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

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_71(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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
        completions = parse_int(None)
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

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_72(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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
        completions = parse_int(awards_j.get(None))
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

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_73(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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
        completions = parse_int(awards_j.get("XXCompletionAwardsCountXX"))
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

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_74(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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
        completions = parse_int(awards_j.get("completionawardscount"))
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

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_75(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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
        completions = parse_int(awards_j.get("COMPLETIONAWARDSCOUNT"))
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

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_76(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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
        beaten = None

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

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_77(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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
        beaten = parse_int(None)

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

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_78(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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
        beaten = parse_int(awards_j.get(None))

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

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_79(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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
        beaten = parse_int(awards_j.get("XXBeatenHardcoreAwardsCountXX"))

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

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_80(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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
        beaten = parse_int(awards_j.get("beatenhardcoreawardscount"))

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

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_81(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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
        beaten = parse_int(awards_j.get("BEATENHARDCOREAWARDSCOUNT"))

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

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_82(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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

        avatar = None
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

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_83(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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

        avatar = profile_j.get("UserPic") and summary_j.get("UserPic")
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

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_84(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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

        avatar = profile_j.get(None) or summary_j.get("UserPic")
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

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_85(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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

        avatar = profile_j.get("XXUserPicXX") or summary_j.get("UserPic")
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

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_86(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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

        avatar = profile_j.get("userpic") or summary_j.get("UserPic")
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

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_87(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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

        avatar = profile_j.get("USERPIC") or summary_j.get("UserPic")
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

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_88(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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

        avatar = profile_j.get("UserPic") or summary_j.get(None)
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

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_89(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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

        avatar = profile_j.get("UserPic") or summary_j.get("XXUserPicXX")
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

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_90(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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

        avatar = profile_j.get("UserPic") or summary_j.get("userpic")
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

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_91(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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

        avatar = profile_j.get("UserPic") or summary_j.get("USERPIC")
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

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_92(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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
        avatar_url = ""
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

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_93(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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
            avatar_url = None

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

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_94(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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
                avatar if avatar.startswith(None)
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

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_95(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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
                avatar if avatar.startswith("XXhttpXX")
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

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_96(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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
                avatar if avatar.startswith("HTTP")
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

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_97(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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

        stats = None
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

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_98(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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

        stats = PlatformStats(platform=None, headline_label="Hardcore Points")
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

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_99(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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

        stats = PlatformStats(platform=self.platform, headline_label=None)
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

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_100(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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

        stats = PlatformStats(headline_label="Hardcore Points")
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

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_101(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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

        stats = PlatformStats(platform=self.platform, )
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

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_102(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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

        stats = PlatformStats(platform=self.platform, headline_label="XXHardcore PointsXX")
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

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_103(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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

        stats = PlatformStats(platform=self.platform, headline_label="hardcore points")
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

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_104(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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

        stats = PlatformStats(platform=self.platform, headline_label="HARDCORE POINTS")
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

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_105(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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
        stats.username = None
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

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_106(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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
        stats.username = profile_j.get("User") or summary_j.get("User") and username
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

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_107(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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
        stats.username = profile_j.get("User") and summary_j.get("User") or username
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

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_108(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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
        stats.username = profile_j.get(None) or summary_j.get("User") or username
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

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_109(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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
        stats.username = profile_j.get("XXUserXX") or summary_j.get("User") or username
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

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_110(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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
        stats.username = profile_j.get("user") or summary_j.get("User") or username
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

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_111(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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
        stats.username = profile_j.get("USER") or summary_j.get("User") or username
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

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_112(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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
        stats.username = profile_j.get("User") or summary_j.get(None) or username
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

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_113(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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
        stats.username = profile_j.get("User") or summary_j.get("XXUserXX") or username
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

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_114(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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
        stats.username = profile_j.get("User") or summary_j.get("user") or username
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

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_115(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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
        stats.username = profile_j.get("User") or summary_j.get("USER") or username
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

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_116(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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
        stats.avatar_url = None
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

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_117(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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
        stats.headline_value = None
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

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_118(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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
        stats.headline_value = hardcore if hardcore is None else softcore
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

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_119(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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
        stats.extra_fields = None
        stats.substats = [
            SubStat(label="RR", value=true_ratio or 0.0),
            SubStat(label="B", value=beaten or 0),
            SubStat(label="M", value=masteries or 0),
        ]
        if hardcore is None and softcore is None:
            raise ProviderError("retroachievements: API returned no point totals")
        return stats

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_120(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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
            "XXTotalPointsXX": hardcore,
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

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_121(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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
            "totalpoints": hardcore,
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

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_122(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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
            "TOTALPOINTS": hardcore,
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

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_123(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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
            "XXTotalSoftcorePointsXX": softcore,
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

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_124(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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
            "totalsoftcorepoints": softcore,
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

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_125(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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
            "TOTALSOFTCOREPOINTS": softcore,
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

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_126(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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
            "XXTotalTruePointsXX": true_points,
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

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_127(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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
            "totaltruepoints": true_points,
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

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_128(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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
            "TOTALTRUEPOINTS": true_points,
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

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_129(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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
            "XXBeatenHardcoreAwardsCountXX": beaten,
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

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_130(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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
            "beatenhardcoreawardscount": beaten,
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

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_131(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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
            "BEATENHARDCOREAWARDSCOUNT": beaten,
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

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_132(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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
            "XXCompletionAwardsCountXX": completions,
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

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_133(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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
            "completionawardscount": completions,
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

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_134(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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
            "COMPLETIONAWARDSCOUNT": completions,
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

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_135(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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
            "XXMasteryAwardsCountXX": masteries,
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

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_136(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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
            "masteryawardscount": masteries,
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

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_137(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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
            "MASTERYAWARDSCOUNT": masteries,
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

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_138(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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
            "XXtrue_ratioXX": true_ratio,
        }
        stats.substats = [
            SubStat(label="RR", value=true_ratio or 0.0),
            SubStat(label="B", value=beaten or 0),
            SubStat(label="M", value=masteries or 0),
        ]
        if hardcore is None and softcore is None:
            raise ProviderError("retroachievements: API returned no point totals")
        return stats

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_139(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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
            "TRUE_RATIO": true_ratio,
        }
        stats.substats = [
            SubStat(label="RR", value=true_ratio or 0.0),
            SubStat(label="B", value=beaten or 0),
            SubStat(label="M", value=masteries or 0),
        ]
        if hardcore is None and softcore is None:
            raise ProviderError("retroachievements: API returned no point totals")
        return stats

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_140(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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
        stats.substats = None
        if hardcore is None and softcore is None:
            raise ProviderError("retroachievements: API returned no point totals")
        return stats

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_141(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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
            SubStat(label=None, value=true_ratio or 0.0),
            SubStat(label="B", value=beaten or 0),
            SubStat(label="M", value=masteries or 0),
        ]
        if hardcore is None and softcore is None:
            raise ProviderError("retroachievements: API returned no point totals")
        return stats

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_142(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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
            SubStat(label="RR", value=None),
            SubStat(label="B", value=beaten or 0),
            SubStat(label="M", value=masteries or 0),
        ]
        if hardcore is None and softcore is None:
            raise ProviderError("retroachievements: API returned no point totals")
        return stats

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_143(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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
            SubStat(value=true_ratio or 0.0),
            SubStat(label="B", value=beaten or 0),
            SubStat(label="M", value=masteries or 0),
        ]
        if hardcore is None and softcore is None:
            raise ProviderError("retroachievements: API returned no point totals")
        return stats

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_144(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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
            SubStat(label="RR", ),
            SubStat(label="B", value=beaten or 0),
            SubStat(label="M", value=masteries or 0),
        ]
        if hardcore is None and softcore is None:
            raise ProviderError("retroachievements: API returned no point totals")
        return stats

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_145(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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
            SubStat(label="XXRRXX", value=true_ratio or 0.0),
            SubStat(label="B", value=beaten or 0),
            SubStat(label="M", value=masteries or 0),
        ]
        if hardcore is None and softcore is None:
            raise ProviderError("retroachievements: API returned no point totals")
        return stats

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_146(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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
            SubStat(label="rr", value=true_ratio or 0.0),
            SubStat(label="B", value=beaten or 0),
            SubStat(label="M", value=masteries or 0),
        ]
        if hardcore is None and softcore is None:
            raise ProviderError("retroachievements: API returned no point totals")
        return stats

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_147(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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
            SubStat(label="RR", value=true_ratio and 0.0),
            SubStat(label="B", value=beaten or 0),
            SubStat(label="M", value=masteries or 0),
        ]
        if hardcore is None and softcore is None:
            raise ProviderError("retroachievements: API returned no point totals")
        return stats

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_148(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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
            SubStat(label="RR", value=true_ratio or 1.0),
            SubStat(label="B", value=beaten or 0),
            SubStat(label="M", value=masteries or 0),
        ]
        if hardcore is None and softcore is None:
            raise ProviderError("retroachievements: API returned no point totals")
        return stats

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_149(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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
            SubStat(label=None, value=beaten or 0),
            SubStat(label="M", value=masteries or 0),
        ]
        if hardcore is None and softcore is None:
            raise ProviderError("retroachievements: API returned no point totals")
        return stats

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_150(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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
            SubStat(label="B", value=None),
            SubStat(label="M", value=masteries or 0),
        ]
        if hardcore is None and softcore is None:
            raise ProviderError("retroachievements: API returned no point totals")
        return stats

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_151(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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
            SubStat(value=beaten or 0),
            SubStat(label="M", value=masteries or 0),
        ]
        if hardcore is None and softcore is None:
            raise ProviderError("retroachievements: API returned no point totals")
        return stats

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_152(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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
            SubStat(label="B", ),
            SubStat(label="M", value=masteries or 0),
        ]
        if hardcore is None and softcore is None:
            raise ProviderError("retroachievements: API returned no point totals")
        return stats

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_153(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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
            SubStat(label="XXBXX", value=beaten or 0),
            SubStat(label="M", value=masteries or 0),
        ]
        if hardcore is None and softcore is None:
            raise ProviderError("retroachievements: API returned no point totals")
        return stats

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_154(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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
            SubStat(label="b", value=beaten or 0),
            SubStat(label="M", value=masteries or 0),
        ]
        if hardcore is None and softcore is None:
            raise ProviderError("retroachievements: API returned no point totals")
        return stats

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_155(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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
            SubStat(label="B", value=beaten and 0),
            SubStat(label="M", value=masteries or 0),
        ]
        if hardcore is None and softcore is None:
            raise ProviderError("retroachievements: API returned no point totals")
        return stats

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_156(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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
            SubStat(label="B", value=beaten or 1),
            SubStat(label="M", value=masteries or 0),
        ]
        if hardcore is None and softcore is None:
            raise ProviderError("retroachievements: API returned no point totals")
        return stats

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_157(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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
            SubStat(label=None, value=masteries or 0),
        ]
        if hardcore is None and softcore is None:
            raise ProviderError("retroachievements: API returned no point totals")
        return stats

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_158(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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
            SubStat(label="M", value=None),
        ]
        if hardcore is None and softcore is None:
            raise ProviderError("retroachievements: API returned no point totals")
        return stats

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_159(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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
            SubStat(value=masteries or 0),
        ]
        if hardcore is None and softcore is None:
            raise ProviderError("retroachievements: API returned no point totals")
        return stats

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_160(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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
            SubStat(label="M", ),
        ]
        if hardcore is None and softcore is None:
            raise ProviderError("retroachievements: API returned no point totals")
        return stats

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_161(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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
            SubStat(label="XXMXX", value=masteries or 0),
        ]
        if hardcore is None and softcore is None:
            raise ProviderError("retroachievements: API returned no point totals")
        return stats

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_162(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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
            SubStat(label="m", value=masteries or 0),
        ]
        if hardcore is None and softcore is None:
            raise ProviderError("retroachievements: API returned no point totals")
        return stats

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_163(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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
            SubStat(label="M", value=masteries and 0),
        ]
        if hardcore is None and softcore is None:
            raise ProviderError("retroachievements: API returned no point totals")
        return stats

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_164(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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
            SubStat(label="M", value=masteries or 1),
        ]
        if hardcore is None and softcore is None:
            raise ProviderError("retroachievements: API returned no point totals")
        return stats

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_165(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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
        if hardcore is None or softcore is None:
            raise ProviderError("retroachievements: API returned no point totals")
        return stats

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_166(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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
        if hardcore is not None and softcore is None:
            raise ProviderError("retroachievements: API returned no point totals")
        return stats

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_167(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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
        if hardcore is None and softcore is not None:
            raise ProviderError("retroachievements: API returned no point totals")
        return stats

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_168(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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
            raise ProviderError(None)
        return stats

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_169(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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
            raise ProviderError("XXretroachievements: API returned no point totalsXX")
        return stats

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_170(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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
            raise ProviderError("retroachievements: api returned no point totals")
        return stats

    def xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_171(self, username: str, api_user: str, api_key: str) -> PlatformStats:
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
            raise ProviderError("RETROACHIEVEMENTS: API RETURNED NO POINT TOTALS")
        return stats
    
    xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_1': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_1, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_2': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_2, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_3': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_3, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_4': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_4, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_5': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_5, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_6': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_6, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_7': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_7, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_8': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_8, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_9': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_9, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_10': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_10, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_11': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_11, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_12': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_12, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_13': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_13, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_14': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_14, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_15': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_15, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_16': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_16, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_17': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_17, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_18': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_18, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_19': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_19, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_20': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_20, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_21': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_21, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_22': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_22, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_23': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_23, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_24': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_24, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_25': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_25, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_26': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_26, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_27': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_27, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_28': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_28, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_29': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_29, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_30': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_30, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_31': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_31, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_32': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_32, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_33': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_33, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_34': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_34, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_35': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_35, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_36': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_36, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_37': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_37, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_38': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_38, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_39': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_39, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_40': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_40, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_41': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_41, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_42': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_42, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_43': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_43, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_44': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_44, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_45': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_45, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_46': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_46, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_47': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_47, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_48': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_48, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_49': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_49, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_50': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_50, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_51': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_51, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_52': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_52, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_53': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_53, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_54': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_54, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_55': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_55, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_56': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_56, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_57': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_57, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_58': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_58, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_59': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_59, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_60': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_60, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_61': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_61, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_62': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_62, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_63': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_63, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_64': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_64, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_65': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_65, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_66': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_66, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_67': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_67, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_68': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_68, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_69': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_69, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_70': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_70, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_71': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_71, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_72': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_72, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_73': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_73, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_74': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_74, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_75': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_75, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_76': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_76, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_77': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_77, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_78': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_78, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_79': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_79, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_80': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_80, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_81': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_81, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_82': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_82, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_83': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_83, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_84': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_84, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_85': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_85, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_86': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_86, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_87': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_87, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_88': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_88, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_89': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_89, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_90': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_90, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_91': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_91, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_92': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_92, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_93': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_93, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_94': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_94, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_95': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_95, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_96': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_96, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_97': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_97, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_98': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_98, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_99': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_99, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_100': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_100, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_101': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_101, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_102': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_102, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_103': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_103, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_104': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_104, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_105': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_105, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_106': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_106, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_107': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_107, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_108': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_108, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_109': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_109, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_110': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_110, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_111': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_111, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_112': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_112, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_113': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_113, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_114': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_114, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_115': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_115, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_116': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_116, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_117': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_117, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_118': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_118, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_119': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_119, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_120': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_120, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_121': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_121, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_122': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_122, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_123': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_123, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_124': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_124, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_125': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_125, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_126': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_126, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_127': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_127, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_128': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_128, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_129': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_129, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_130': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_130, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_131': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_131, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_132': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_132, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_133': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_133, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_134': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_134, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_135': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_135, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_136': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_136, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_137': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_137, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_138': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_138, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_139': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_139, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_140': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_140, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_141': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_141, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_142': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_142, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_143': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_143, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_144': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_144, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_145': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_145, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_146': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_146, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_147': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_147, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_148': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_148, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_149': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_149, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_150': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_150, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_151': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_151, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_152': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_152, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_153': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_153, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_154': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_154, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_155': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_155, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_156': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_156, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_157': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_157, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_158': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_158, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_159': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_159, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_160': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_160, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_161': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_161, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_162': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_162, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_163': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_163, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_164': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_164, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_165': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_165, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_166': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_166, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_167': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_167, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_168': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_168, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_169': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_169, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_170': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_170, 
        'xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_171': xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_171
    }
    
    def _fetch_via_api(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_orig"), object.__getattribute__(self, "xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _fetch_via_api.__signature__ = _mutmut_signature(xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_orig)
    xǁRetroAchievementsProviderǁ_fetch_via_api__mutmut_orig.__name__ = 'xǁRetroAchievementsProviderǁ_fetch_via_api'
