"""Orchestrates per-platform scraping with cache + override fallback."""
from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path

from .. import cache as cache_mod
from ..config import AppConfig, ProfileConfig, load_overrides, save_overrides
from ..models import PlatformStats
from ..providers.base import Provider, ProviderError
from ..providers.psn import PsnProvider
from ..providers.retroachievements import RetroAchievementsProvider
from ..providers.xbox import XboxProvider
from .merge import apply_override, merge_with_cache, placeholder

log = logging.getLogger(__name__)

PROVIDERS: dict[str, type[Provider]] = {
    "xbox": XboxProvider,
    "psn": PsnProvider,
    "retroachievements": RetroAchievementsProvider,
}


@dataclass
class FetchPaths:
    cache_dir: Path
    overrides_file: Path


def fetch_all(
    cfg: AppConfig,
    paths: FetchPaths,
    scrape: bool = True,
) -> dict[str, PlatformStats]:
    overrides = load_overrides(paths.overrides_file)
    results: dict[str, PlatformStats] = {}

    for platform, profile in cfg.profiles.items():
        stats = _resolve_platform(platform, profile, paths, overrides, scrape=scrape)
        if profile.display_name:
            stats.username = profile.display_name
        results[platform] = stats

        _refresh_avatar(stats, paths.cache_dir)

    _persist_overrides(results, paths.overrides_file)
    return results


def _resolve_platform(
    platform: str,
    profile: ProfileConfig,
    paths: FetchPaths,
    overrides: dict,
    scrape: bool,
) -> PlatformStats:
    cached = cache_mod.load(paths.cache_dir, platform)
    fresh: PlatformStats | None = None

    if scrape and profile.profile_url:
        provider_cls = PROVIDERS.get(platform)
        if provider_cls:
            try:
                fresh = provider_cls().fetch(profile.profile_url)
                log.info("%s: scrape OK", platform)
            except ProviderError as exc:
                log.warning("%s: scrape failed: %s", platform, exc)
            except Exception as exc:
                log.exception("%s: unexpected scrape error: %s", platform, exc)

    # Priority: fresh scrape > manual override > cache > placeholder.
    # When the scrape fails we prefer the user-editable override so hand-set
    # numbers actually take effect without requiring a cache wipe.
    override = overrides.get(platform) if isinstance(overrides, dict) else None
    if fresh is None and override:
        log.info("%s: using manual override (scrape failed or disabled)", platform)
        merged = apply_override(None, override, platform)
    else:
        merged = merge_with_cache(fresh, cached, platform)

    if merged is None:
        log.warning("%s: using placeholders (no data anywhere)", platform)
        merged = placeholder(platform)

    if fresh is not None and merged is not None:
        cache_mod.save(paths.cache_dir, merged)
        log.info("%s: cache updated", platform)

    return merged or placeholder(platform)


def _refresh_avatar(stats: PlatformStats, cache_dir: Path) -> None:
    # Prefer any existing local file so manually-placed avatars stick between
    # runs. Only fetch from URL when there's nothing on disk yet.
    cached = cache_mod.find_cached_avatar(cache_dir, stats.platform)
    if cached:
        log.info("%s: using local avatar %s", stats.platform, cached.name)
        return
    if stats.avatar_url:
        path = cache_mod.download_avatar(cache_dir, stats.platform, stats.avatar_url)
        if path:
            log.info("%s: avatar downloaded to %s", stats.platform, path.name)


def _persist_overrides(results: dict[str, PlatformStats], path: Path) -> None:
    """Seed the overrides file on first successful run so the user has a
    starting point to edit. After that, never overwrite user edits."""
    existing = load_overrides(path)
    if isinstance(existing, dict) and any(existing.get(p) for p in results):
        return
    payload = {platform: stats.to_dict() for platform, stats in results.items()}
    save_overrides(path, payload)
