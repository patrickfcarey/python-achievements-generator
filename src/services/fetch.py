"""Orchestrates per-platform scraping with cache fallback.

Resolution priority for each platform (highest to lowest):
  1. Fresh scrape — most up-to-date; used when scrape=True and a URL is set.
  2. Cached data — last successful scrape result stored as JSON.
  3. Placeholder — synthetic zeros so rendering never crashes.

Use ``render-manual`` (main.py) to render from a hand-edited manual.yaml
instead of the scrape/cache pipeline.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path

from .. import cache as cache_module

# Tests patch these attributes by their old names; keep as aliases.
cache_mod = cache_module
from ..config import AppConfig, ProfileConfig
from ..models import PlatformStats
from ..providers import browser as browser_module

# Tests patch this module attribute by the old name; keep as alias.
browser_mod = browser_module
from ..providers.base import Provider, ProviderError
from ..providers.psn import PsnProvider
from ..providers.retroachievements import RetroAchievementsProvider
from ..providers.xbox import XboxProvider
from .merge import merge_with_cache, placeholder

log = logging.getLogger(__name__)

PROVIDERS: dict[str, type[Provider]] = {
    "xbox": XboxProvider,
    "psn": PsnProvider,
    "retroachievements": RetroAchievementsProvider,
}


@dataclass
class FetchPaths:
    """File-system paths used by the fetch pipeline."""
    cache_dir: Path


def fetch_all(
    app_config: AppConfig,
    fetch_paths: FetchPaths,
    scrape: bool = True,
) -> dict[str, PlatformStats]:
    """Scrape, merge, and return stats for every configured platform.

    Always closes the shared browser session in a finally block so the Python
    process can exit cleanly even when scraping fails mid-run.
    """
    platform_results: dict[str, PlatformStats] = {}

    try:
        for platform, profile_config in app_config.profiles.items():
            platform_stats = _resolve_platform_stats(
                platform, profile_config, fetch_paths, scrape=scrape,
            )
            if profile_config.display_name:
                platform_stats.username = profile_config.display_name
            platform_results[platform] = platform_stats

            _refresh_avatar_if_needed(platform_stats, fetch_paths.cache_dir)
    finally:
        browser_module.close()

    return platform_results


def _resolve_platform_stats(
    platform: str,
    profile_config: ProfileConfig,
    fetch_paths: FetchPaths,
    scrape: bool,
) -> PlatformStats:
    """Resolve the best available stats for one platform using the priority chain.

    Attempts a live scrape when enabled, then applies the priority chain
    (fresh → cache → placeholder) to produce the final result.
    When a fresh result is available, it is written back to the cache.
    """
    cached_stats = cache_module.load(fetch_paths.cache_dir, platform)
    fresh_stats = _try_scrape(platform, profile_config, scrape)

    resolved_stats = merge_with_cache(fresh_stats, cached_stats, platform)

    if resolved_stats is None:
        log.warning("%s: using placeholders (no data anywhere)", platform)
        resolved_stats = placeholder(platform)

    if fresh_stats is not None and resolved_stats is not None:
        cache_module.save(fetch_paths.cache_dir, resolved_stats)
        log.info("%s: cache updated", platform)

    return resolved_stats or placeholder(platform)


def _try_scrape(
    platform: str,
    profile_config: ProfileConfig,
    scrape: bool,
) -> PlatformStats | None:
    """Attempt a live scrape and return the result, or None on any failure.

    Returns None immediately if scraping is disabled or no profile URL is set.
    Catches both expected ProviderError and unexpected exceptions so a single
    platform failure never aborts the rest of the run.
    """
    if not scrape or not profile_config.profile_url:
        return None

    provider_class = PROVIDERS.get(platform)
    if provider_class is None:
        return None

    try:
        fresh_stats = provider_class().fetch(profile_config.profile_url)
        log.info("%s: scrape OK", platform)
        return fresh_stats
    except ProviderError as provider_error:
        log.warning("%s: scrape failed: %s", platform, provider_error)
    except Exception as unexpected_error:
        log.exception("%s: unexpected scrape error: %s", platform, unexpected_error)
    return None


def _refresh_avatar_if_needed(platform_stats: PlatformStats, cache_dir: Path) -> None:
    """Download the avatar if no local copy exists yet.

    Prefers any existing local file so manually-placed avatars persist between
    runs. Only fetches from the URL when there is nothing on disk.
    """
    existing_avatar = cache_module.find_cached_avatar(cache_dir, platform_stats.platform)
    if existing_avatar:
        log.info("%s: using local avatar %s", platform_stats.platform, existing_avatar.name)
        return
    if platform_stats.avatar_url:
        downloaded_path = cache_module.download_avatar(
            cache_dir, platform_stats.platform, platform_stats.avatar_url,
        )
        if downloaded_path:
            log.info("%s: avatar downloaded to %s", platform_stats.platform, downloaded_path.name)


