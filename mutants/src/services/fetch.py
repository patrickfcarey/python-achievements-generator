"""Orchestrates per-platform scraping with cache + override fallback."""
from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path

from .. import cache as cache_mod
from ..config import AppConfig, ProfileConfig, load_overrides, save_overrides
from ..models import PlatformStats
from ..providers import browser as browser_mod
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


@dataclass
class FetchPaths:
    cache_dir: Path
    overrides_file: Path


def x_fetch_all__mutmut_orig(
    cfg: AppConfig,
    paths: FetchPaths,
    scrape: bool = True,
) -> dict[str, PlatformStats]:
    overrides = load_overrides(paths.overrides_file)
    results: dict[str, PlatformStats] = {}

    try:
        for platform, profile in cfg.profiles.items():
            stats = _resolve_platform(platform, profile, paths, overrides, scrape=scrape)
            if profile.display_name:
                stats.username = profile.display_name
            results[platform] = stats

            _refresh_avatar(stats, paths.cache_dir)
    finally:
        # Always shut down the shared browser so the Python process exits.
        browser_mod.close()

    _persist_overrides(results, paths.overrides_file)
    return results


def x_fetch_all__mutmut_1(
    cfg: AppConfig,
    paths: FetchPaths,
    scrape: bool = False,
) -> dict[str, PlatformStats]:
    overrides = load_overrides(paths.overrides_file)
    results: dict[str, PlatformStats] = {}

    try:
        for platform, profile in cfg.profiles.items():
            stats = _resolve_platform(platform, profile, paths, overrides, scrape=scrape)
            if profile.display_name:
                stats.username = profile.display_name
            results[platform] = stats

            _refresh_avatar(stats, paths.cache_dir)
    finally:
        # Always shut down the shared browser so the Python process exits.
        browser_mod.close()

    _persist_overrides(results, paths.overrides_file)
    return results


def x_fetch_all__mutmut_2(
    cfg: AppConfig,
    paths: FetchPaths,
    scrape: bool = True,
) -> dict[str, PlatformStats]:
    overrides = None
    results: dict[str, PlatformStats] = {}

    try:
        for platform, profile in cfg.profiles.items():
            stats = _resolve_platform(platform, profile, paths, overrides, scrape=scrape)
            if profile.display_name:
                stats.username = profile.display_name
            results[platform] = stats

            _refresh_avatar(stats, paths.cache_dir)
    finally:
        # Always shut down the shared browser so the Python process exits.
        browser_mod.close()

    _persist_overrides(results, paths.overrides_file)
    return results


def x_fetch_all__mutmut_3(
    cfg: AppConfig,
    paths: FetchPaths,
    scrape: bool = True,
) -> dict[str, PlatformStats]:
    overrides = load_overrides(None)
    results: dict[str, PlatformStats] = {}

    try:
        for platform, profile in cfg.profiles.items():
            stats = _resolve_platform(platform, profile, paths, overrides, scrape=scrape)
            if profile.display_name:
                stats.username = profile.display_name
            results[platform] = stats

            _refresh_avatar(stats, paths.cache_dir)
    finally:
        # Always shut down the shared browser so the Python process exits.
        browser_mod.close()

    _persist_overrides(results, paths.overrides_file)
    return results


def x_fetch_all__mutmut_4(
    cfg: AppConfig,
    paths: FetchPaths,
    scrape: bool = True,
) -> dict[str, PlatformStats]:
    overrides = load_overrides(paths.overrides_file)
    results: dict[str, PlatformStats] = None

    try:
        for platform, profile in cfg.profiles.items():
            stats = _resolve_platform(platform, profile, paths, overrides, scrape=scrape)
            if profile.display_name:
                stats.username = profile.display_name
            results[platform] = stats

            _refresh_avatar(stats, paths.cache_dir)
    finally:
        # Always shut down the shared browser so the Python process exits.
        browser_mod.close()

    _persist_overrides(results, paths.overrides_file)
    return results


def x_fetch_all__mutmut_5(
    cfg: AppConfig,
    paths: FetchPaths,
    scrape: bool = True,
) -> dict[str, PlatformStats]:
    overrides = load_overrides(paths.overrides_file)
    results: dict[str, PlatformStats] = {}

    try:
        for platform, profile in cfg.profiles.items():
            stats = None
            if profile.display_name:
                stats.username = profile.display_name
            results[platform] = stats

            _refresh_avatar(stats, paths.cache_dir)
    finally:
        # Always shut down the shared browser so the Python process exits.
        browser_mod.close()

    _persist_overrides(results, paths.overrides_file)
    return results


def x_fetch_all__mutmut_6(
    cfg: AppConfig,
    paths: FetchPaths,
    scrape: bool = True,
) -> dict[str, PlatformStats]:
    overrides = load_overrides(paths.overrides_file)
    results: dict[str, PlatformStats] = {}

    try:
        for platform, profile in cfg.profiles.items():
            stats = _resolve_platform(None, profile, paths, overrides, scrape=scrape)
            if profile.display_name:
                stats.username = profile.display_name
            results[platform] = stats

            _refresh_avatar(stats, paths.cache_dir)
    finally:
        # Always shut down the shared browser so the Python process exits.
        browser_mod.close()

    _persist_overrides(results, paths.overrides_file)
    return results


def x_fetch_all__mutmut_7(
    cfg: AppConfig,
    paths: FetchPaths,
    scrape: bool = True,
) -> dict[str, PlatformStats]:
    overrides = load_overrides(paths.overrides_file)
    results: dict[str, PlatformStats] = {}

    try:
        for platform, profile in cfg.profiles.items():
            stats = _resolve_platform(platform, None, paths, overrides, scrape=scrape)
            if profile.display_name:
                stats.username = profile.display_name
            results[platform] = stats

            _refresh_avatar(stats, paths.cache_dir)
    finally:
        # Always shut down the shared browser so the Python process exits.
        browser_mod.close()

    _persist_overrides(results, paths.overrides_file)
    return results


def x_fetch_all__mutmut_8(
    cfg: AppConfig,
    paths: FetchPaths,
    scrape: bool = True,
) -> dict[str, PlatformStats]:
    overrides = load_overrides(paths.overrides_file)
    results: dict[str, PlatformStats] = {}

    try:
        for platform, profile in cfg.profiles.items():
            stats = _resolve_platform(platform, profile, None, overrides, scrape=scrape)
            if profile.display_name:
                stats.username = profile.display_name
            results[platform] = stats

            _refresh_avatar(stats, paths.cache_dir)
    finally:
        # Always shut down the shared browser so the Python process exits.
        browser_mod.close()

    _persist_overrides(results, paths.overrides_file)
    return results


def x_fetch_all__mutmut_9(
    cfg: AppConfig,
    paths: FetchPaths,
    scrape: bool = True,
) -> dict[str, PlatformStats]:
    overrides = load_overrides(paths.overrides_file)
    results: dict[str, PlatformStats] = {}

    try:
        for platform, profile in cfg.profiles.items():
            stats = _resolve_platform(platform, profile, paths, None, scrape=scrape)
            if profile.display_name:
                stats.username = profile.display_name
            results[platform] = stats

            _refresh_avatar(stats, paths.cache_dir)
    finally:
        # Always shut down the shared browser so the Python process exits.
        browser_mod.close()

    _persist_overrides(results, paths.overrides_file)
    return results


def x_fetch_all__mutmut_10(
    cfg: AppConfig,
    paths: FetchPaths,
    scrape: bool = True,
) -> dict[str, PlatformStats]:
    overrides = load_overrides(paths.overrides_file)
    results: dict[str, PlatformStats] = {}

    try:
        for platform, profile in cfg.profiles.items():
            stats = _resolve_platform(platform, profile, paths, overrides, scrape=None)
            if profile.display_name:
                stats.username = profile.display_name
            results[platform] = stats

            _refresh_avatar(stats, paths.cache_dir)
    finally:
        # Always shut down the shared browser so the Python process exits.
        browser_mod.close()

    _persist_overrides(results, paths.overrides_file)
    return results


def x_fetch_all__mutmut_11(
    cfg: AppConfig,
    paths: FetchPaths,
    scrape: bool = True,
) -> dict[str, PlatformStats]:
    overrides = load_overrides(paths.overrides_file)
    results: dict[str, PlatformStats] = {}

    try:
        for platform, profile in cfg.profiles.items():
            stats = _resolve_platform(profile, paths, overrides, scrape=scrape)
            if profile.display_name:
                stats.username = profile.display_name
            results[platform] = stats

            _refresh_avatar(stats, paths.cache_dir)
    finally:
        # Always shut down the shared browser so the Python process exits.
        browser_mod.close()

    _persist_overrides(results, paths.overrides_file)
    return results


def x_fetch_all__mutmut_12(
    cfg: AppConfig,
    paths: FetchPaths,
    scrape: bool = True,
) -> dict[str, PlatformStats]:
    overrides = load_overrides(paths.overrides_file)
    results: dict[str, PlatformStats] = {}

    try:
        for platform, profile in cfg.profiles.items():
            stats = _resolve_platform(platform, paths, overrides, scrape=scrape)
            if profile.display_name:
                stats.username = profile.display_name
            results[platform] = stats

            _refresh_avatar(stats, paths.cache_dir)
    finally:
        # Always shut down the shared browser so the Python process exits.
        browser_mod.close()

    _persist_overrides(results, paths.overrides_file)
    return results


def x_fetch_all__mutmut_13(
    cfg: AppConfig,
    paths: FetchPaths,
    scrape: bool = True,
) -> dict[str, PlatformStats]:
    overrides = load_overrides(paths.overrides_file)
    results: dict[str, PlatformStats] = {}

    try:
        for platform, profile in cfg.profiles.items():
            stats = _resolve_platform(platform, profile, overrides, scrape=scrape)
            if profile.display_name:
                stats.username = profile.display_name
            results[platform] = stats

            _refresh_avatar(stats, paths.cache_dir)
    finally:
        # Always shut down the shared browser so the Python process exits.
        browser_mod.close()

    _persist_overrides(results, paths.overrides_file)
    return results


def x_fetch_all__mutmut_14(
    cfg: AppConfig,
    paths: FetchPaths,
    scrape: bool = True,
) -> dict[str, PlatformStats]:
    overrides = load_overrides(paths.overrides_file)
    results: dict[str, PlatformStats] = {}

    try:
        for platform, profile in cfg.profiles.items():
            stats = _resolve_platform(platform, profile, paths, scrape=scrape)
            if profile.display_name:
                stats.username = profile.display_name
            results[platform] = stats

            _refresh_avatar(stats, paths.cache_dir)
    finally:
        # Always shut down the shared browser so the Python process exits.
        browser_mod.close()

    _persist_overrides(results, paths.overrides_file)
    return results


def x_fetch_all__mutmut_15(
    cfg: AppConfig,
    paths: FetchPaths,
    scrape: bool = True,
) -> dict[str, PlatformStats]:
    overrides = load_overrides(paths.overrides_file)
    results: dict[str, PlatformStats] = {}

    try:
        for platform, profile in cfg.profiles.items():
            stats = _resolve_platform(platform, profile, paths, overrides, )
            if profile.display_name:
                stats.username = profile.display_name
            results[platform] = stats

            _refresh_avatar(stats, paths.cache_dir)
    finally:
        # Always shut down the shared browser so the Python process exits.
        browser_mod.close()

    _persist_overrides(results, paths.overrides_file)
    return results


def x_fetch_all__mutmut_16(
    cfg: AppConfig,
    paths: FetchPaths,
    scrape: bool = True,
) -> dict[str, PlatformStats]:
    overrides = load_overrides(paths.overrides_file)
    results: dict[str, PlatformStats] = {}

    try:
        for platform, profile in cfg.profiles.items():
            stats = _resolve_platform(platform, profile, paths, overrides, scrape=scrape)
            if profile.display_name:
                stats.username = None
            results[platform] = stats

            _refresh_avatar(stats, paths.cache_dir)
    finally:
        # Always shut down the shared browser so the Python process exits.
        browser_mod.close()

    _persist_overrides(results, paths.overrides_file)
    return results


def x_fetch_all__mutmut_17(
    cfg: AppConfig,
    paths: FetchPaths,
    scrape: bool = True,
) -> dict[str, PlatformStats]:
    overrides = load_overrides(paths.overrides_file)
    results: dict[str, PlatformStats] = {}

    try:
        for platform, profile in cfg.profiles.items():
            stats = _resolve_platform(platform, profile, paths, overrides, scrape=scrape)
            if profile.display_name:
                stats.username = profile.display_name
            results[platform] = None

            _refresh_avatar(stats, paths.cache_dir)
    finally:
        # Always shut down the shared browser so the Python process exits.
        browser_mod.close()

    _persist_overrides(results, paths.overrides_file)
    return results


def x_fetch_all__mutmut_18(
    cfg: AppConfig,
    paths: FetchPaths,
    scrape: bool = True,
) -> dict[str, PlatformStats]:
    overrides = load_overrides(paths.overrides_file)
    results: dict[str, PlatformStats] = {}

    try:
        for platform, profile in cfg.profiles.items():
            stats = _resolve_platform(platform, profile, paths, overrides, scrape=scrape)
            if profile.display_name:
                stats.username = profile.display_name
            results[platform] = stats

            _refresh_avatar(None, paths.cache_dir)
    finally:
        # Always shut down the shared browser so the Python process exits.
        browser_mod.close()

    _persist_overrides(results, paths.overrides_file)
    return results


def x_fetch_all__mutmut_19(
    cfg: AppConfig,
    paths: FetchPaths,
    scrape: bool = True,
) -> dict[str, PlatformStats]:
    overrides = load_overrides(paths.overrides_file)
    results: dict[str, PlatformStats] = {}

    try:
        for platform, profile in cfg.profiles.items():
            stats = _resolve_platform(platform, profile, paths, overrides, scrape=scrape)
            if profile.display_name:
                stats.username = profile.display_name
            results[platform] = stats

            _refresh_avatar(stats, None)
    finally:
        # Always shut down the shared browser so the Python process exits.
        browser_mod.close()

    _persist_overrides(results, paths.overrides_file)
    return results


def x_fetch_all__mutmut_20(
    cfg: AppConfig,
    paths: FetchPaths,
    scrape: bool = True,
) -> dict[str, PlatformStats]:
    overrides = load_overrides(paths.overrides_file)
    results: dict[str, PlatformStats] = {}

    try:
        for platform, profile in cfg.profiles.items():
            stats = _resolve_platform(platform, profile, paths, overrides, scrape=scrape)
            if profile.display_name:
                stats.username = profile.display_name
            results[platform] = stats

            _refresh_avatar(paths.cache_dir)
    finally:
        # Always shut down the shared browser so the Python process exits.
        browser_mod.close()

    _persist_overrides(results, paths.overrides_file)
    return results


def x_fetch_all__mutmut_21(
    cfg: AppConfig,
    paths: FetchPaths,
    scrape: bool = True,
) -> dict[str, PlatformStats]:
    overrides = load_overrides(paths.overrides_file)
    results: dict[str, PlatformStats] = {}

    try:
        for platform, profile in cfg.profiles.items():
            stats = _resolve_platform(platform, profile, paths, overrides, scrape=scrape)
            if profile.display_name:
                stats.username = profile.display_name
            results[platform] = stats

            _refresh_avatar(stats, )
    finally:
        # Always shut down the shared browser so the Python process exits.
        browser_mod.close()

    _persist_overrides(results, paths.overrides_file)
    return results


def x_fetch_all__mutmut_22(
    cfg: AppConfig,
    paths: FetchPaths,
    scrape: bool = True,
) -> dict[str, PlatformStats]:
    overrides = load_overrides(paths.overrides_file)
    results: dict[str, PlatformStats] = {}

    try:
        for platform, profile in cfg.profiles.items():
            stats = _resolve_platform(platform, profile, paths, overrides, scrape=scrape)
            if profile.display_name:
                stats.username = profile.display_name
            results[platform] = stats

            _refresh_avatar(stats, paths.cache_dir)
    finally:
        # Always shut down the shared browser so the Python process exits.
        browser_mod.close()

    _persist_overrides(None, paths.overrides_file)
    return results


def x_fetch_all__mutmut_23(
    cfg: AppConfig,
    paths: FetchPaths,
    scrape: bool = True,
) -> dict[str, PlatformStats]:
    overrides = load_overrides(paths.overrides_file)
    results: dict[str, PlatformStats] = {}

    try:
        for platform, profile in cfg.profiles.items():
            stats = _resolve_platform(platform, profile, paths, overrides, scrape=scrape)
            if profile.display_name:
                stats.username = profile.display_name
            results[platform] = stats

            _refresh_avatar(stats, paths.cache_dir)
    finally:
        # Always shut down the shared browser so the Python process exits.
        browser_mod.close()

    _persist_overrides(results, None)
    return results


def x_fetch_all__mutmut_24(
    cfg: AppConfig,
    paths: FetchPaths,
    scrape: bool = True,
) -> dict[str, PlatformStats]:
    overrides = load_overrides(paths.overrides_file)
    results: dict[str, PlatformStats] = {}

    try:
        for platform, profile in cfg.profiles.items():
            stats = _resolve_platform(platform, profile, paths, overrides, scrape=scrape)
            if profile.display_name:
                stats.username = profile.display_name
            results[platform] = stats

            _refresh_avatar(stats, paths.cache_dir)
    finally:
        # Always shut down the shared browser so the Python process exits.
        browser_mod.close()

    _persist_overrides(paths.overrides_file)
    return results


def x_fetch_all__mutmut_25(
    cfg: AppConfig,
    paths: FetchPaths,
    scrape: bool = True,
) -> dict[str, PlatformStats]:
    overrides = load_overrides(paths.overrides_file)
    results: dict[str, PlatformStats] = {}

    try:
        for platform, profile in cfg.profiles.items():
            stats = _resolve_platform(platform, profile, paths, overrides, scrape=scrape)
            if profile.display_name:
                stats.username = profile.display_name
            results[platform] = stats

            _refresh_avatar(stats, paths.cache_dir)
    finally:
        # Always shut down the shared browser so the Python process exits.
        browser_mod.close()

    _persist_overrides(results, )
    return results

x_fetch_all__mutmut_mutants : ClassVar[MutantDict] = {
'x_fetch_all__mutmut_1': x_fetch_all__mutmut_1, 
    'x_fetch_all__mutmut_2': x_fetch_all__mutmut_2, 
    'x_fetch_all__mutmut_3': x_fetch_all__mutmut_3, 
    'x_fetch_all__mutmut_4': x_fetch_all__mutmut_4, 
    'x_fetch_all__mutmut_5': x_fetch_all__mutmut_5, 
    'x_fetch_all__mutmut_6': x_fetch_all__mutmut_6, 
    'x_fetch_all__mutmut_7': x_fetch_all__mutmut_7, 
    'x_fetch_all__mutmut_8': x_fetch_all__mutmut_8, 
    'x_fetch_all__mutmut_9': x_fetch_all__mutmut_9, 
    'x_fetch_all__mutmut_10': x_fetch_all__mutmut_10, 
    'x_fetch_all__mutmut_11': x_fetch_all__mutmut_11, 
    'x_fetch_all__mutmut_12': x_fetch_all__mutmut_12, 
    'x_fetch_all__mutmut_13': x_fetch_all__mutmut_13, 
    'x_fetch_all__mutmut_14': x_fetch_all__mutmut_14, 
    'x_fetch_all__mutmut_15': x_fetch_all__mutmut_15, 
    'x_fetch_all__mutmut_16': x_fetch_all__mutmut_16, 
    'x_fetch_all__mutmut_17': x_fetch_all__mutmut_17, 
    'x_fetch_all__mutmut_18': x_fetch_all__mutmut_18, 
    'x_fetch_all__mutmut_19': x_fetch_all__mutmut_19, 
    'x_fetch_all__mutmut_20': x_fetch_all__mutmut_20, 
    'x_fetch_all__mutmut_21': x_fetch_all__mutmut_21, 
    'x_fetch_all__mutmut_22': x_fetch_all__mutmut_22, 
    'x_fetch_all__mutmut_23': x_fetch_all__mutmut_23, 
    'x_fetch_all__mutmut_24': x_fetch_all__mutmut_24, 
    'x_fetch_all__mutmut_25': x_fetch_all__mutmut_25
}

def fetch_all(*args, **kwargs):
    result = _mutmut_trampoline(x_fetch_all__mutmut_orig, x_fetch_all__mutmut_mutants, args, kwargs)
    return result 

fetch_all.__signature__ = _mutmut_signature(x_fetch_all__mutmut_orig)
x_fetch_all__mutmut_orig.__name__ = 'x_fetch_all'


def x__resolve_platform__mutmut_orig(
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


def x__resolve_platform__mutmut_1(
    platform: str,
    profile: ProfileConfig,
    paths: FetchPaths,
    overrides: dict,
    scrape: bool,
) -> PlatformStats:
    cached = None
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


def x__resolve_platform__mutmut_2(
    platform: str,
    profile: ProfileConfig,
    paths: FetchPaths,
    overrides: dict,
    scrape: bool,
) -> PlatformStats:
    cached = cache_mod.load(None, platform)
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


def x__resolve_platform__mutmut_3(
    platform: str,
    profile: ProfileConfig,
    paths: FetchPaths,
    overrides: dict,
    scrape: bool,
) -> PlatformStats:
    cached = cache_mod.load(paths.cache_dir, None)
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


def x__resolve_platform__mutmut_4(
    platform: str,
    profile: ProfileConfig,
    paths: FetchPaths,
    overrides: dict,
    scrape: bool,
) -> PlatformStats:
    cached = cache_mod.load(platform)
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


def x__resolve_platform__mutmut_5(
    platform: str,
    profile: ProfileConfig,
    paths: FetchPaths,
    overrides: dict,
    scrape: bool,
) -> PlatformStats:
    cached = cache_mod.load(paths.cache_dir, )
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


def x__resolve_platform__mutmut_6(
    platform: str,
    profile: ProfileConfig,
    paths: FetchPaths,
    overrides: dict,
    scrape: bool,
) -> PlatformStats:
    cached = cache_mod.load(paths.cache_dir, platform)
    fresh: PlatformStats | None = ""

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


def x__resolve_platform__mutmut_7(
    platform: str,
    profile: ProfileConfig,
    paths: FetchPaths,
    overrides: dict,
    scrape: bool,
) -> PlatformStats:
    cached = cache_mod.load(paths.cache_dir, platform)
    fresh: PlatformStats | None = None

    if scrape or profile.profile_url:
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


def x__resolve_platform__mutmut_8(
    platform: str,
    profile: ProfileConfig,
    paths: FetchPaths,
    overrides: dict,
    scrape: bool,
) -> PlatformStats:
    cached = cache_mod.load(paths.cache_dir, platform)
    fresh: PlatformStats | None = None

    if scrape and profile.profile_url:
        provider_cls = None
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


def x__resolve_platform__mutmut_9(
    platform: str,
    profile: ProfileConfig,
    paths: FetchPaths,
    overrides: dict,
    scrape: bool,
) -> PlatformStats:
    cached = cache_mod.load(paths.cache_dir, platform)
    fresh: PlatformStats | None = None

    if scrape and profile.profile_url:
        provider_cls = PROVIDERS.get(None)
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


def x__resolve_platform__mutmut_10(
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
                fresh = None
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


def x__resolve_platform__mutmut_11(
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
                fresh = provider_cls().fetch(None)
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


def x__resolve_platform__mutmut_12(
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
                log.info(None, platform)
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


def x__resolve_platform__mutmut_13(
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
                log.info("%s: scrape OK", None)
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


def x__resolve_platform__mutmut_14(
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
                log.info(platform)
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


def x__resolve_platform__mutmut_15(
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
                log.info("%s: scrape OK", )
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


def x__resolve_platform__mutmut_16(
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
                log.info("XX%s: scrape OKXX", platform)
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


def x__resolve_platform__mutmut_17(
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
                log.info("%s: scrape ok", platform)
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


def x__resolve_platform__mutmut_18(
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
                log.info("%S: SCRAPE OK", platform)
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


def x__resolve_platform__mutmut_19(
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
                log.warning(None, platform, exc)
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


def x__resolve_platform__mutmut_20(
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
                log.warning("%s: scrape failed: %s", None, exc)
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


def x__resolve_platform__mutmut_21(
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
                log.warning("%s: scrape failed: %s", platform, None)
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


def x__resolve_platform__mutmut_22(
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
                log.warning(platform, exc)
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


def x__resolve_platform__mutmut_23(
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
                log.warning("%s: scrape failed: %s", exc)
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


def x__resolve_platform__mutmut_24(
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
                log.warning("%s: scrape failed: %s", platform, )
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


def x__resolve_platform__mutmut_25(
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
                log.warning("XX%s: scrape failed: %sXX", platform, exc)
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


def x__resolve_platform__mutmut_26(
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
                log.warning("%S: SCRAPE FAILED: %S", platform, exc)
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


def x__resolve_platform__mutmut_27(
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
                log.exception(None, platform, exc)

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


def x__resolve_platform__mutmut_28(
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
                log.exception("%s: unexpected scrape error: %s", None, exc)

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


def x__resolve_platform__mutmut_29(
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
                log.exception("%s: unexpected scrape error: %s", platform, None)

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


def x__resolve_platform__mutmut_30(
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
                log.exception(platform, exc)

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


def x__resolve_platform__mutmut_31(
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
                log.exception("%s: unexpected scrape error: %s", exc)

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


def x__resolve_platform__mutmut_32(
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
                log.exception("%s: unexpected scrape error: %s", platform, )

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


def x__resolve_platform__mutmut_33(
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
                log.exception("XX%s: unexpected scrape error: %sXX", platform, exc)

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


def x__resolve_platform__mutmut_34(
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
                log.exception("%S: UNEXPECTED SCRAPE ERROR: %S", platform, exc)

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


def x__resolve_platform__mutmut_35(
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
    override = None
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


def x__resolve_platform__mutmut_36(
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
    override = overrides.get(None) if isinstance(overrides, dict) else None
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


def x__resolve_platform__mutmut_37(
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
    if fresh is None or override:
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


def x__resolve_platform__mutmut_38(
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
    if fresh is not None and override:
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


def x__resolve_platform__mutmut_39(
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
        log.info(None, platform)
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


def x__resolve_platform__mutmut_40(
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
        log.info("%s: using manual override (scrape failed or disabled)", None)
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


def x__resolve_platform__mutmut_41(
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
        log.info(platform)
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


def x__resolve_platform__mutmut_42(
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
        log.info("%s: using manual override (scrape failed or disabled)", )
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


def x__resolve_platform__mutmut_43(
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
        log.info("XX%s: using manual override (scrape failed or disabled)XX", platform)
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


def x__resolve_platform__mutmut_44(
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
        log.info("%S: USING MANUAL OVERRIDE (SCRAPE FAILED OR DISABLED)", platform)
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


def x__resolve_platform__mutmut_45(
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
        merged = None
    else:
        merged = merge_with_cache(fresh, cached, platform)

    if merged is None:
        log.warning("%s: using placeholders (no data anywhere)", platform)
        merged = placeholder(platform)

    if fresh is not None and merged is not None:
        cache_mod.save(paths.cache_dir, merged)
        log.info("%s: cache updated", platform)

    return merged or placeholder(platform)


def x__resolve_platform__mutmut_46(
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
        merged = apply_override(None, None, platform)
    else:
        merged = merge_with_cache(fresh, cached, platform)

    if merged is None:
        log.warning("%s: using placeholders (no data anywhere)", platform)
        merged = placeholder(platform)

    if fresh is not None and merged is not None:
        cache_mod.save(paths.cache_dir, merged)
        log.info("%s: cache updated", platform)

    return merged or placeholder(platform)


def x__resolve_platform__mutmut_47(
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
        merged = apply_override(None, override, None)
    else:
        merged = merge_with_cache(fresh, cached, platform)

    if merged is None:
        log.warning("%s: using placeholders (no data anywhere)", platform)
        merged = placeholder(platform)

    if fresh is not None and merged is not None:
        cache_mod.save(paths.cache_dir, merged)
        log.info("%s: cache updated", platform)

    return merged or placeholder(platform)


def x__resolve_platform__mutmut_48(
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
        merged = apply_override(override, platform)
    else:
        merged = merge_with_cache(fresh, cached, platform)

    if merged is None:
        log.warning("%s: using placeholders (no data anywhere)", platform)
        merged = placeholder(platform)

    if fresh is not None and merged is not None:
        cache_mod.save(paths.cache_dir, merged)
        log.info("%s: cache updated", platform)

    return merged or placeholder(platform)


def x__resolve_platform__mutmut_49(
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
        merged = apply_override(None, platform)
    else:
        merged = merge_with_cache(fresh, cached, platform)

    if merged is None:
        log.warning("%s: using placeholders (no data anywhere)", platform)
        merged = placeholder(platform)

    if fresh is not None and merged is not None:
        cache_mod.save(paths.cache_dir, merged)
        log.info("%s: cache updated", platform)

    return merged or placeholder(platform)


def x__resolve_platform__mutmut_50(
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
        merged = apply_override(None, override, )
    else:
        merged = merge_with_cache(fresh, cached, platform)

    if merged is None:
        log.warning("%s: using placeholders (no data anywhere)", platform)
        merged = placeholder(platform)

    if fresh is not None and merged is not None:
        cache_mod.save(paths.cache_dir, merged)
        log.info("%s: cache updated", platform)

    return merged or placeholder(platform)


def x__resolve_platform__mutmut_51(
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
        merged = None

    if merged is None:
        log.warning("%s: using placeholders (no data anywhere)", platform)
        merged = placeholder(platform)

    if fresh is not None and merged is not None:
        cache_mod.save(paths.cache_dir, merged)
        log.info("%s: cache updated", platform)

    return merged or placeholder(platform)


def x__resolve_platform__mutmut_52(
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
        merged = merge_with_cache(None, cached, platform)

    if merged is None:
        log.warning("%s: using placeholders (no data anywhere)", platform)
        merged = placeholder(platform)

    if fresh is not None and merged is not None:
        cache_mod.save(paths.cache_dir, merged)
        log.info("%s: cache updated", platform)

    return merged or placeholder(platform)


def x__resolve_platform__mutmut_53(
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
        merged = merge_with_cache(fresh, None, platform)

    if merged is None:
        log.warning("%s: using placeholders (no data anywhere)", platform)
        merged = placeholder(platform)

    if fresh is not None and merged is not None:
        cache_mod.save(paths.cache_dir, merged)
        log.info("%s: cache updated", platform)

    return merged or placeholder(platform)


def x__resolve_platform__mutmut_54(
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
        merged = merge_with_cache(fresh, cached, None)

    if merged is None:
        log.warning("%s: using placeholders (no data anywhere)", platform)
        merged = placeholder(platform)

    if fresh is not None and merged is not None:
        cache_mod.save(paths.cache_dir, merged)
        log.info("%s: cache updated", platform)

    return merged or placeholder(platform)


def x__resolve_platform__mutmut_55(
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
        merged = merge_with_cache(cached, platform)

    if merged is None:
        log.warning("%s: using placeholders (no data anywhere)", platform)
        merged = placeholder(platform)

    if fresh is not None and merged is not None:
        cache_mod.save(paths.cache_dir, merged)
        log.info("%s: cache updated", platform)

    return merged or placeholder(platform)


def x__resolve_platform__mutmut_56(
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
        merged = merge_with_cache(fresh, platform)

    if merged is None:
        log.warning("%s: using placeholders (no data anywhere)", platform)
        merged = placeholder(platform)

    if fresh is not None and merged is not None:
        cache_mod.save(paths.cache_dir, merged)
        log.info("%s: cache updated", platform)

    return merged or placeholder(platform)


def x__resolve_platform__mutmut_57(
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
        merged = merge_with_cache(fresh, cached, )

    if merged is None:
        log.warning("%s: using placeholders (no data anywhere)", platform)
        merged = placeholder(platform)

    if fresh is not None and merged is not None:
        cache_mod.save(paths.cache_dir, merged)
        log.info("%s: cache updated", platform)

    return merged or placeholder(platform)


def x__resolve_platform__mutmut_58(
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

    if merged is not None:
        log.warning("%s: using placeholders (no data anywhere)", platform)
        merged = placeholder(platform)

    if fresh is not None and merged is not None:
        cache_mod.save(paths.cache_dir, merged)
        log.info("%s: cache updated", platform)

    return merged or placeholder(platform)


def x__resolve_platform__mutmut_59(
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
        log.warning(None, platform)
        merged = placeholder(platform)

    if fresh is not None and merged is not None:
        cache_mod.save(paths.cache_dir, merged)
        log.info("%s: cache updated", platform)

    return merged or placeholder(platform)


def x__resolve_platform__mutmut_60(
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
        log.warning("%s: using placeholders (no data anywhere)", None)
        merged = placeholder(platform)

    if fresh is not None and merged is not None:
        cache_mod.save(paths.cache_dir, merged)
        log.info("%s: cache updated", platform)

    return merged or placeholder(platform)


def x__resolve_platform__mutmut_61(
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
        log.warning(platform)
        merged = placeholder(platform)

    if fresh is not None and merged is not None:
        cache_mod.save(paths.cache_dir, merged)
        log.info("%s: cache updated", platform)

    return merged or placeholder(platform)


def x__resolve_platform__mutmut_62(
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
        log.warning("%s: using placeholders (no data anywhere)", )
        merged = placeholder(platform)

    if fresh is not None and merged is not None:
        cache_mod.save(paths.cache_dir, merged)
        log.info("%s: cache updated", platform)

    return merged or placeholder(platform)


def x__resolve_platform__mutmut_63(
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
        log.warning("XX%s: using placeholders (no data anywhere)XX", platform)
        merged = placeholder(platform)

    if fresh is not None and merged is not None:
        cache_mod.save(paths.cache_dir, merged)
        log.info("%s: cache updated", platform)

    return merged or placeholder(platform)


def x__resolve_platform__mutmut_64(
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
        log.warning("%S: USING PLACEHOLDERS (NO DATA ANYWHERE)", platform)
        merged = placeholder(platform)

    if fresh is not None and merged is not None:
        cache_mod.save(paths.cache_dir, merged)
        log.info("%s: cache updated", platform)

    return merged or placeholder(platform)


def x__resolve_platform__mutmut_65(
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
        merged = None

    if fresh is not None and merged is not None:
        cache_mod.save(paths.cache_dir, merged)
        log.info("%s: cache updated", platform)

    return merged or placeholder(platform)


def x__resolve_platform__mutmut_66(
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
        merged = placeholder(None)

    if fresh is not None and merged is not None:
        cache_mod.save(paths.cache_dir, merged)
        log.info("%s: cache updated", platform)

    return merged or placeholder(platform)


def x__resolve_platform__mutmut_67(
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

    if fresh is not None or merged is not None:
        cache_mod.save(paths.cache_dir, merged)
        log.info("%s: cache updated", platform)

    return merged or placeholder(platform)


def x__resolve_platform__mutmut_68(
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

    if fresh is None and merged is not None:
        cache_mod.save(paths.cache_dir, merged)
        log.info("%s: cache updated", platform)

    return merged or placeholder(platform)


def x__resolve_platform__mutmut_69(
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

    if fresh is not None and merged is None:
        cache_mod.save(paths.cache_dir, merged)
        log.info("%s: cache updated", platform)

    return merged or placeholder(platform)


def x__resolve_platform__mutmut_70(
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
        cache_mod.save(None, merged)
        log.info("%s: cache updated", platform)

    return merged or placeholder(platform)


def x__resolve_platform__mutmut_71(
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
        cache_mod.save(paths.cache_dir, None)
        log.info("%s: cache updated", platform)

    return merged or placeholder(platform)


def x__resolve_platform__mutmut_72(
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
        cache_mod.save(merged)
        log.info("%s: cache updated", platform)

    return merged or placeholder(platform)


def x__resolve_platform__mutmut_73(
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
        cache_mod.save(paths.cache_dir, )
        log.info("%s: cache updated", platform)

    return merged or placeholder(platform)


def x__resolve_platform__mutmut_74(
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
        log.info(None, platform)

    return merged or placeholder(platform)


def x__resolve_platform__mutmut_75(
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
        log.info("%s: cache updated", None)

    return merged or placeholder(platform)


def x__resolve_platform__mutmut_76(
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
        log.info(platform)

    return merged or placeholder(platform)


def x__resolve_platform__mutmut_77(
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
        log.info("%s: cache updated", )

    return merged or placeholder(platform)


def x__resolve_platform__mutmut_78(
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
        log.info("XX%s: cache updatedXX", platform)

    return merged or placeholder(platform)


def x__resolve_platform__mutmut_79(
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
        log.info("%S: CACHE UPDATED", platform)

    return merged or placeholder(platform)


def x__resolve_platform__mutmut_80(
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

    return merged and placeholder(platform)


def x__resolve_platform__mutmut_81(
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

    return merged or placeholder(None)

x__resolve_platform__mutmut_mutants : ClassVar[MutantDict] = {
'x__resolve_platform__mutmut_1': x__resolve_platform__mutmut_1, 
    'x__resolve_platform__mutmut_2': x__resolve_platform__mutmut_2, 
    'x__resolve_platform__mutmut_3': x__resolve_platform__mutmut_3, 
    'x__resolve_platform__mutmut_4': x__resolve_platform__mutmut_4, 
    'x__resolve_platform__mutmut_5': x__resolve_platform__mutmut_5, 
    'x__resolve_platform__mutmut_6': x__resolve_platform__mutmut_6, 
    'x__resolve_platform__mutmut_7': x__resolve_platform__mutmut_7, 
    'x__resolve_platform__mutmut_8': x__resolve_platform__mutmut_8, 
    'x__resolve_platform__mutmut_9': x__resolve_platform__mutmut_9, 
    'x__resolve_platform__mutmut_10': x__resolve_platform__mutmut_10, 
    'x__resolve_platform__mutmut_11': x__resolve_platform__mutmut_11, 
    'x__resolve_platform__mutmut_12': x__resolve_platform__mutmut_12, 
    'x__resolve_platform__mutmut_13': x__resolve_platform__mutmut_13, 
    'x__resolve_platform__mutmut_14': x__resolve_platform__mutmut_14, 
    'x__resolve_platform__mutmut_15': x__resolve_platform__mutmut_15, 
    'x__resolve_platform__mutmut_16': x__resolve_platform__mutmut_16, 
    'x__resolve_platform__mutmut_17': x__resolve_platform__mutmut_17, 
    'x__resolve_platform__mutmut_18': x__resolve_platform__mutmut_18, 
    'x__resolve_platform__mutmut_19': x__resolve_platform__mutmut_19, 
    'x__resolve_platform__mutmut_20': x__resolve_platform__mutmut_20, 
    'x__resolve_platform__mutmut_21': x__resolve_platform__mutmut_21, 
    'x__resolve_platform__mutmut_22': x__resolve_platform__mutmut_22, 
    'x__resolve_platform__mutmut_23': x__resolve_platform__mutmut_23, 
    'x__resolve_platform__mutmut_24': x__resolve_platform__mutmut_24, 
    'x__resolve_platform__mutmut_25': x__resolve_platform__mutmut_25, 
    'x__resolve_platform__mutmut_26': x__resolve_platform__mutmut_26, 
    'x__resolve_platform__mutmut_27': x__resolve_platform__mutmut_27, 
    'x__resolve_platform__mutmut_28': x__resolve_platform__mutmut_28, 
    'x__resolve_platform__mutmut_29': x__resolve_platform__mutmut_29, 
    'x__resolve_platform__mutmut_30': x__resolve_platform__mutmut_30, 
    'x__resolve_platform__mutmut_31': x__resolve_platform__mutmut_31, 
    'x__resolve_platform__mutmut_32': x__resolve_platform__mutmut_32, 
    'x__resolve_platform__mutmut_33': x__resolve_platform__mutmut_33, 
    'x__resolve_platform__mutmut_34': x__resolve_platform__mutmut_34, 
    'x__resolve_platform__mutmut_35': x__resolve_platform__mutmut_35, 
    'x__resolve_platform__mutmut_36': x__resolve_platform__mutmut_36, 
    'x__resolve_platform__mutmut_37': x__resolve_platform__mutmut_37, 
    'x__resolve_platform__mutmut_38': x__resolve_platform__mutmut_38, 
    'x__resolve_platform__mutmut_39': x__resolve_platform__mutmut_39, 
    'x__resolve_platform__mutmut_40': x__resolve_platform__mutmut_40, 
    'x__resolve_platform__mutmut_41': x__resolve_platform__mutmut_41, 
    'x__resolve_platform__mutmut_42': x__resolve_platform__mutmut_42, 
    'x__resolve_platform__mutmut_43': x__resolve_platform__mutmut_43, 
    'x__resolve_platform__mutmut_44': x__resolve_platform__mutmut_44, 
    'x__resolve_platform__mutmut_45': x__resolve_platform__mutmut_45, 
    'x__resolve_platform__mutmut_46': x__resolve_platform__mutmut_46, 
    'x__resolve_platform__mutmut_47': x__resolve_platform__mutmut_47, 
    'x__resolve_platform__mutmut_48': x__resolve_platform__mutmut_48, 
    'x__resolve_platform__mutmut_49': x__resolve_platform__mutmut_49, 
    'x__resolve_platform__mutmut_50': x__resolve_platform__mutmut_50, 
    'x__resolve_platform__mutmut_51': x__resolve_platform__mutmut_51, 
    'x__resolve_platform__mutmut_52': x__resolve_platform__mutmut_52, 
    'x__resolve_platform__mutmut_53': x__resolve_platform__mutmut_53, 
    'x__resolve_platform__mutmut_54': x__resolve_platform__mutmut_54, 
    'x__resolve_platform__mutmut_55': x__resolve_platform__mutmut_55, 
    'x__resolve_platform__mutmut_56': x__resolve_platform__mutmut_56, 
    'x__resolve_platform__mutmut_57': x__resolve_platform__mutmut_57, 
    'x__resolve_platform__mutmut_58': x__resolve_platform__mutmut_58, 
    'x__resolve_platform__mutmut_59': x__resolve_platform__mutmut_59, 
    'x__resolve_platform__mutmut_60': x__resolve_platform__mutmut_60, 
    'x__resolve_platform__mutmut_61': x__resolve_platform__mutmut_61, 
    'x__resolve_platform__mutmut_62': x__resolve_platform__mutmut_62, 
    'x__resolve_platform__mutmut_63': x__resolve_platform__mutmut_63, 
    'x__resolve_platform__mutmut_64': x__resolve_platform__mutmut_64, 
    'x__resolve_platform__mutmut_65': x__resolve_platform__mutmut_65, 
    'x__resolve_platform__mutmut_66': x__resolve_platform__mutmut_66, 
    'x__resolve_platform__mutmut_67': x__resolve_platform__mutmut_67, 
    'x__resolve_platform__mutmut_68': x__resolve_platform__mutmut_68, 
    'x__resolve_platform__mutmut_69': x__resolve_platform__mutmut_69, 
    'x__resolve_platform__mutmut_70': x__resolve_platform__mutmut_70, 
    'x__resolve_platform__mutmut_71': x__resolve_platform__mutmut_71, 
    'x__resolve_platform__mutmut_72': x__resolve_platform__mutmut_72, 
    'x__resolve_platform__mutmut_73': x__resolve_platform__mutmut_73, 
    'x__resolve_platform__mutmut_74': x__resolve_platform__mutmut_74, 
    'x__resolve_platform__mutmut_75': x__resolve_platform__mutmut_75, 
    'x__resolve_platform__mutmut_76': x__resolve_platform__mutmut_76, 
    'x__resolve_platform__mutmut_77': x__resolve_platform__mutmut_77, 
    'x__resolve_platform__mutmut_78': x__resolve_platform__mutmut_78, 
    'x__resolve_platform__mutmut_79': x__resolve_platform__mutmut_79, 
    'x__resolve_platform__mutmut_80': x__resolve_platform__mutmut_80, 
    'x__resolve_platform__mutmut_81': x__resolve_platform__mutmut_81
}

def _resolve_platform(*args, **kwargs):
    result = _mutmut_trampoline(x__resolve_platform__mutmut_orig, x__resolve_platform__mutmut_mutants, args, kwargs)
    return result 

_resolve_platform.__signature__ = _mutmut_signature(x__resolve_platform__mutmut_orig)
x__resolve_platform__mutmut_orig.__name__ = 'x__resolve_platform'


def x__refresh_avatar__mutmut_orig(stats: PlatformStats, cache_dir: Path) -> None:
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


def x__refresh_avatar__mutmut_1(stats: PlatformStats, cache_dir: Path) -> None:
    # Prefer any existing local file so manually-placed avatars stick between
    # runs. Only fetch from URL when there's nothing on disk yet.
    cached = None
    if cached:
        log.info("%s: using local avatar %s", stats.platform, cached.name)
        return
    if stats.avatar_url:
        path = cache_mod.download_avatar(cache_dir, stats.platform, stats.avatar_url)
        if path:
            log.info("%s: avatar downloaded to %s", stats.platform, path.name)


def x__refresh_avatar__mutmut_2(stats: PlatformStats, cache_dir: Path) -> None:
    # Prefer any existing local file so manually-placed avatars stick between
    # runs. Only fetch from URL when there's nothing on disk yet.
    cached = cache_mod.find_cached_avatar(None, stats.platform)
    if cached:
        log.info("%s: using local avatar %s", stats.platform, cached.name)
        return
    if stats.avatar_url:
        path = cache_mod.download_avatar(cache_dir, stats.platform, stats.avatar_url)
        if path:
            log.info("%s: avatar downloaded to %s", stats.platform, path.name)


def x__refresh_avatar__mutmut_3(stats: PlatformStats, cache_dir: Path) -> None:
    # Prefer any existing local file so manually-placed avatars stick between
    # runs. Only fetch from URL when there's nothing on disk yet.
    cached = cache_mod.find_cached_avatar(cache_dir, None)
    if cached:
        log.info("%s: using local avatar %s", stats.platform, cached.name)
        return
    if stats.avatar_url:
        path = cache_mod.download_avatar(cache_dir, stats.platform, stats.avatar_url)
        if path:
            log.info("%s: avatar downloaded to %s", stats.platform, path.name)


def x__refresh_avatar__mutmut_4(stats: PlatformStats, cache_dir: Path) -> None:
    # Prefer any existing local file so manually-placed avatars stick between
    # runs. Only fetch from URL when there's nothing on disk yet.
    cached = cache_mod.find_cached_avatar(stats.platform)
    if cached:
        log.info("%s: using local avatar %s", stats.platform, cached.name)
        return
    if stats.avatar_url:
        path = cache_mod.download_avatar(cache_dir, stats.platform, stats.avatar_url)
        if path:
            log.info("%s: avatar downloaded to %s", stats.platform, path.name)


def x__refresh_avatar__mutmut_5(stats: PlatformStats, cache_dir: Path) -> None:
    # Prefer any existing local file so manually-placed avatars stick between
    # runs. Only fetch from URL when there's nothing on disk yet.
    cached = cache_mod.find_cached_avatar(cache_dir, )
    if cached:
        log.info("%s: using local avatar %s", stats.platform, cached.name)
        return
    if stats.avatar_url:
        path = cache_mod.download_avatar(cache_dir, stats.platform, stats.avatar_url)
        if path:
            log.info("%s: avatar downloaded to %s", stats.platform, path.name)


def x__refresh_avatar__mutmut_6(stats: PlatformStats, cache_dir: Path) -> None:
    # Prefer any existing local file so manually-placed avatars stick between
    # runs. Only fetch from URL when there's nothing on disk yet.
    cached = cache_mod.find_cached_avatar(cache_dir, stats.platform)
    if cached:
        log.info(None, stats.platform, cached.name)
        return
    if stats.avatar_url:
        path = cache_mod.download_avatar(cache_dir, stats.platform, stats.avatar_url)
        if path:
            log.info("%s: avatar downloaded to %s", stats.platform, path.name)


def x__refresh_avatar__mutmut_7(stats: PlatformStats, cache_dir: Path) -> None:
    # Prefer any existing local file so manually-placed avatars stick between
    # runs. Only fetch from URL when there's nothing on disk yet.
    cached = cache_mod.find_cached_avatar(cache_dir, stats.platform)
    if cached:
        log.info("%s: using local avatar %s", None, cached.name)
        return
    if stats.avatar_url:
        path = cache_mod.download_avatar(cache_dir, stats.platform, stats.avatar_url)
        if path:
            log.info("%s: avatar downloaded to %s", stats.platform, path.name)


def x__refresh_avatar__mutmut_8(stats: PlatformStats, cache_dir: Path) -> None:
    # Prefer any existing local file so manually-placed avatars stick between
    # runs. Only fetch from URL when there's nothing on disk yet.
    cached = cache_mod.find_cached_avatar(cache_dir, stats.platform)
    if cached:
        log.info("%s: using local avatar %s", stats.platform, None)
        return
    if stats.avatar_url:
        path = cache_mod.download_avatar(cache_dir, stats.platform, stats.avatar_url)
        if path:
            log.info("%s: avatar downloaded to %s", stats.platform, path.name)


def x__refresh_avatar__mutmut_9(stats: PlatformStats, cache_dir: Path) -> None:
    # Prefer any existing local file so manually-placed avatars stick between
    # runs. Only fetch from URL when there's nothing on disk yet.
    cached = cache_mod.find_cached_avatar(cache_dir, stats.platform)
    if cached:
        log.info(stats.platform, cached.name)
        return
    if stats.avatar_url:
        path = cache_mod.download_avatar(cache_dir, stats.platform, stats.avatar_url)
        if path:
            log.info("%s: avatar downloaded to %s", stats.platform, path.name)


def x__refresh_avatar__mutmut_10(stats: PlatformStats, cache_dir: Path) -> None:
    # Prefer any existing local file so manually-placed avatars stick between
    # runs. Only fetch from URL when there's nothing on disk yet.
    cached = cache_mod.find_cached_avatar(cache_dir, stats.platform)
    if cached:
        log.info("%s: using local avatar %s", cached.name)
        return
    if stats.avatar_url:
        path = cache_mod.download_avatar(cache_dir, stats.platform, stats.avatar_url)
        if path:
            log.info("%s: avatar downloaded to %s", stats.platform, path.name)


def x__refresh_avatar__mutmut_11(stats: PlatformStats, cache_dir: Path) -> None:
    # Prefer any existing local file so manually-placed avatars stick between
    # runs. Only fetch from URL when there's nothing on disk yet.
    cached = cache_mod.find_cached_avatar(cache_dir, stats.platform)
    if cached:
        log.info("%s: using local avatar %s", stats.platform, )
        return
    if stats.avatar_url:
        path = cache_mod.download_avatar(cache_dir, stats.platform, stats.avatar_url)
        if path:
            log.info("%s: avatar downloaded to %s", stats.platform, path.name)


def x__refresh_avatar__mutmut_12(stats: PlatformStats, cache_dir: Path) -> None:
    # Prefer any existing local file so manually-placed avatars stick between
    # runs. Only fetch from URL when there's nothing on disk yet.
    cached = cache_mod.find_cached_avatar(cache_dir, stats.platform)
    if cached:
        log.info("XX%s: using local avatar %sXX", stats.platform, cached.name)
        return
    if stats.avatar_url:
        path = cache_mod.download_avatar(cache_dir, stats.platform, stats.avatar_url)
        if path:
            log.info("%s: avatar downloaded to %s", stats.platform, path.name)


def x__refresh_avatar__mutmut_13(stats: PlatformStats, cache_dir: Path) -> None:
    # Prefer any existing local file so manually-placed avatars stick between
    # runs. Only fetch from URL when there's nothing on disk yet.
    cached = cache_mod.find_cached_avatar(cache_dir, stats.platform)
    if cached:
        log.info("%S: USING LOCAL AVATAR %S", stats.platform, cached.name)
        return
    if stats.avatar_url:
        path = cache_mod.download_avatar(cache_dir, stats.platform, stats.avatar_url)
        if path:
            log.info("%s: avatar downloaded to %s", stats.platform, path.name)


def x__refresh_avatar__mutmut_14(stats: PlatformStats, cache_dir: Path) -> None:
    # Prefer any existing local file so manually-placed avatars stick between
    # runs. Only fetch from URL when there's nothing on disk yet.
    cached = cache_mod.find_cached_avatar(cache_dir, stats.platform)
    if cached:
        log.info("%s: using local avatar %s", stats.platform, cached.name)
        return
    if stats.avatar_url:
        path = None
        if path:
            log.info("%s: avatar downloaded to %s", stats.platform, path.name)


def x__refresh_avatar__mutmut_15(stats: PlatformStats, cache_dir: Path) -> None:
    # Prefer any existing local file so manually-placed avatars stick between
    # runs. Only fetch from URL when there's nothing on disk yet.
    cached = cache_mod.find_cached_avatar(cache_dir, stats.platform)
    if cached:
        log.info("%s: using local avatar %s", stats.platform, cached.name)
        return
    if stats.avatar_url:
        path = cache_mod.download_avatar(None, stats.platform, stats.avatar_url)
        if path:
            log.info("%s: avatar downloaded to %s", stats.platform, path.name)


def x__refresh_avatar__mutmut_16(stats: PlatformStats, cache_dir: Path) -> None:
    # Prefer any existing local file so manually-placed avatars stick between
    # runs. Only fetch from URL when there's nothing on disk yet.
    cached = cache_mod.find_cached_avatar(cache_dir, stats.platform)
    if cached:
        log.info("%s: using local avatar %s", stats.platform, cached.name)
        return
    if stats.avatar_url:
        path = cache_mod.download_avatar(cache_dir, None, stats.avatar_url)
        if path:
            log.info("%s: avatar downloaded to %s", stats.platform, path.name)


def x__refresh_avatar__mutmut_17(stats: PlatformStats, cache_dir: Path) -> None:
    # Prefer any existing local file so manually-placed avatars stick between
    # runs. Only fetch from URL when there's nothing on disk yet.
    cached = cache_mod.find_cached_avatar(cache_dir, stats.platform)
    if cached:
        log.info("%s: using local avatar %s", stats.platform, cached.name)
        return
    if stats.avatar_url:
        path = cache_mod.download_avatar(cache_dir, stats.platform, None)
        if path:
            log.info("%s: avatar downloaded to %s", stats.platform, path.name)


def x__refresh_avatar__mutmut_18(stats: PlatformStats, cache_dir: Path) -> None:
    # Prefer any existing local file so manually-placed avatars stick between
    # runs. Only fetch from URL when there's nothing on disk yet.
    cached = cache_mod.find_cached_avatar(cache_dir, stats.platform)
    if cached:
        log.info("%s: using local avatar %s", stats.platform, cached.name)
        return
    if stats.avatar_url:
        path = cache_mod.download_avatar(stats.platform, stats.avatar_url)
        if path:
            log.info("%s: avatar downloaded to %s", stats.platform, path.name)


def x__refresh_avatar__mutmut_19(stats: PlatformStats, cache_dir: Path) -> None:
    # Prefer any existing local file so manually-placed avatars stick between
    # runs. Only fetch from URL when there's nothing on disk yet.
    cached = cache_mod.find_cached_avatar(cache_dir, stats.platform)
    if cached:
        log.info("%s: using local avatar %s", stats.platform, cached.name)
        return
    if stats.avatar_url:
        path = cache_mod.download_avatar(cache_dir, stats.avatar_url)
        if path:
            log.info("%s: avatar downloaded to %s", stats.platform, path.name)


def x__refresh_avatar__mutmut_20(stats: PlatformStats, cache_dir: Path) -> None:
    # Prefer any existing local file so manually-placed avatars stick between
    # runs. Only fetch from URL when there's nothing on disk yet.
    cached = cache_mod.find_cached_avatar(cache_dir, stats.platform)
    if cached:
        log.info("%s: using local avatar %s", stats.platform, cached.name)
        return
    if stats.avatar_url:
        path = cache_mod.download_avatar(cache_dir, stats.platform, )
        if path:
            log.info("%s: avatar downloaded to %s", stats.platform, path.name)


def x__refresh_avatar__mutmut_21(stats: PlatformStats, cache_dir: Path) -> None:
    # Prefer any existing local file so manually-placed avatars stick between
    # runs. Only fetch from URL when there's nothing on disk yet.
    cached = cache_mod.find_cached_avatar(cache_dir, stats.platform)
    if cached:
        log.info("%s: using local avatar %s", stats.platform, cached.name)
        return
    if stats.avatar_url:
        path = cache_mod.download_avatar(cache_dir, stats.platform, stats.avatar_url)
        if path:
            log.info(None, stats.platform, path.name)


def x__refresh_avatar__mutmut_22(stats: PlatformStats, cache_dir: Path) -> None:
    # Prefer any existing local file so manually-placed avatars stick between
    # runs. Only fetch from URL when there's nothing on disk yet.
    cached = cache_mod.find_cached_avatar(cache_dir, stats.platform)
    if cached:
        log.info("%s: using local avatar %s", stats.platform, cached.name)
        return
    if stats.avatar_url:
        path = cache_mod.download_avatar(cache_dir, stats.platform, stats.avatar_url)
        if path:
            log.info("%s: avatar downloaded to %s", None, path.name)


def x__refresh_avatar__mutmut_23(stats: PlatformStats, cache_dir: Path) -> None:
    # Prefer any existing local file so manually-placed avatars stick between
    # runs. Only fetch from URL when there's nothing on disk yet.
    cached = cache_mod.find_cached_avatar(cache_dir, stats.platform)
    if cached:
        log.info("%s: using local avatar %s", stats.platform, cached.name)
        return
    if stats.avatar_url:
        path = cache_mod.download_avatar(cache_dir, stats.platform, stats.avatar_url)
        if path:
            log.info("%s: avatar downloaded to %s", stats.platform, None)


def x__refresh_avatar__mutmut_24(stats: PlatformStats, cache_dir: Path) -> None:
    # Prefer any existing local file so manually-placed avatars stick between
    # runs. Only fetch from URL when there's nothing on disk yet.
    cached = cache_mod.find_cached_avatar(cache_dir, stats.platform)
    if cached:
        log.info("%s: using local avatar %s", stats.platform, cached.name)
        return
    if stats.avatar_url:
        path = cache_mod.download_avatar(cache_dir, stats.platform, stats.avatar_url)
        if path:
            log.info(stats.platform, path.name)


def x__refresh_avatar__mutmut_25(stats: PlatformStats, cache_dir: Path) -> None:
    # Prefer any existing local file so manually-placed avatars stick between
    # runs. Only fetch from URL when there's nothing on disk yet.
    cached = cache_mod.find_cached_avatar(cache_dir, stats.platform)
    if cached:
        log.info("%s: using local avatar %s", stats.platform, cached.name)
        return
    if stats.avatar_url:
        path = cache_mod.download_avatar(cache_dir, stats.platform, stats.avatar_url)
        if path:
            log.info("%s: avatar downloaded to %s", path.name)


def x__refresh_avatar__mutmut_26(stats: PlatformStats, cache_dir: Path) -> None:
    # Prefer any existing local file so manually-placed avatars stick between
    # runs. Only fetch from URL when there's nothing on disk yet.
    cached = cache_mod.find_cached_avatar(cache_dir, stats.platform)
    if cached:
        log.info("%s: using local avatar %s", stats.platform, cached.name)
        return
    if stats.avatar_url:
        path = cache_mod.download_avatar(cache_dir, stats.platform, stats.avatar_url)
        if path:
            log.info("%s: avatar downloaded to %s", stats.platform, )


def x__refresh_avatar__mutmut_27(stats: PlatformStats, cache_dir: Path) -> None:
    # Prefer any existing local file so manually-placed avatars stick between
    # runs. Only fetch from URL when there's nothing on disk yet.
    cached = cache_mod.find_cached_avatar(cache_dir, stats.platform)
    if cached:
        log.info("%s: using local avatar %s", stats.platform, cached.name)
        return
    if stats.avatar_url:
        path = cache_mod.download_avatar(cache_dir, stats.platform, stats.avatar_url)
        if path:
            log.info("XX%s: avatar downloaded to %sXX", stats.platform, path.name)


def x__refresh_avatar__mutmut_28(stats: PlatformStats, cache_dir: Path) -> None:
    # Prefer any existing local file so manually-placed avatars stick between
    # runs. Only fetch from URL when there's nothing on disk yet.
    cached = cache_mod.find_cached_avatar(cache_dir, stats.platform)
    if cached:
        log.info("%s: using local avatar %s", stats.platform, cached.name)
        return
    if stats.avatar_url:
        path = cache_mod.download_avatar(cache_dir, stats.platform, stats.avatar_url)
        if path:
            log.info("%S: AVATAR DOWNLOADED TO %S", stats.platform, path.name)

x__refresh_avatar__mutmut_mutants : ClassVar[MutantDict] = {
'x__refresh_avatar__mutmut_1': x__refresh_avatar__mutmut_1, 
    'x__refresh_avatar__mutmut_2': x__refresh_avatar__mutmut_2, 
    'x__refresh_avatar__mutmut_3': x__refresh_avatar__mutmut_3, 
    'x__refresh_avatar__mutmut_4': x__refresh_avatar__mutmut_4, 
    'x__refresh_avatar__mutmut_5': x__refresh_avatar__mutmut_5, 
    'x__refresh_avatar__mutmut_6': x__refresh_avatar__mutmut_6, 
    'x__refresh_avatar__mutmut_7': x__refresh_avatar__mutmut_7, 
    'x__refresh_avatar__mutmut_8': x__refresh_avatar__mutmut_8, 
    'x__refresh_avatar__mutmut_9': x__refresh_avatar__mutmut_9, 
    'x__refresh_avatar__mutmut_10': x__refresh_avatar__mutmut_10, 
    'x__refresh_avatar__mutmut_11': x__refresh_avatar__mutmut_11, 
    'x__refresh_avatar__mutmut_12': x__refresh_avatar__mutmut_12, 
    'x__refresh_avatar__mutmut_13': x__refresh_avatar__mutmut_13, 
    'x__refresh_avatar__mutmut_14': x__refresh_avatar__mutmut_14, 
    'x__refresh_avatar__mutmut_15': x__refresh_avatar__mutmut_15, 
    'x__refresh_avatar__mutmut_16': x__refresh_avatar__mutmut_16, 
    'x__refresh_avatar__mutmut_17': x__refresh_avatar__mutmut_17, 
    'x__refresh_avatar__mutmut_18': x__refresh_avatar__mutmut_18, 
    'x__refresh_avatar__mutmut_19': x__refresh_avatar__mutmut_19, 
    'x__refresh_avatar__mutmut_20': x__refresh_avatar__mutmut_20, 
    'x__refresh_avatar__mutmut_21': x__refresh_avatar__mutmut_21, 
    'x__refresh_avatar__mutmut_22': x__refresh_avatar__mutmut_22, 
    'x__refresh_avatar__mutmut_23': x__refresh_avatar__mutmut_23, 
    'x__refresh_avatar__mutmut_24': x__refresh_avatar__mutmut_24, 
    'x__refresh_avatar__mutmut_25': x__refresh_avatar__mutmut_25, 
    'x__refresh_avatar__mutmut_26': x__refresh_avatar__mutmut_26, 
    'x__refresh_avatar__mutmut_27': x__refresh_avatar__mutmut_27, 
    'x__refresh_avatar__mutmut_28': x__refresh_avatar__mutmut_28
}

def _refresh_avatar(*args, **kwargs):
    result = _mutmut_trampoline(x__refresh_avatar__mutmut_orig, x__refresh_avatar__mutmut_mutants, args, kwargs)
    return result 

_refresh_avatar.__signature__ = _mutmut_signature(x__refresh_avatar__mutmut_orig)
x__refresh_avatar__mutmut_orig.__name__ = 'x__refresh_avatar'


def x__persist_overrides__mutmut_orig(results: dict[str, PlatformStats], path: Path) -> None:
    """Seed the overrides file on first successful run so the user has a
    starting point to edit. After that, never overwrite user edits."""
    existing = load_overrides(path)
    if isinstance(existing, dict) and any(existing.get(p) for p in results):
        return
    payload = {platform: stats.to_dict() for platform, stats in results.items()}
    save_overrides(path, payload)


def x__persist_overrides__mutmut_1(results: dict[str, PlatformStats], path: Path) -> None:
    """Seed the overrides file on first successful run so the user has a
    starting point to edit. After that, never overwrite user edits."""
    existing = None
    if isinstance(existing, dict) and any(existing.get(p) for p in results):
        return
    payload = {platform: stats.to_dict() for platform, stats in results.items()}
    save_overrides(path, payload)


def x__persist_overrides__mutmut_2(results: dict[str, PlatformStats], path: Path) -> None:
    """Seed the overrides file on first successful run so the user has a
    starting point to edit. After that, never overwrite user edits."""
    existing = load_overrides(None)
    if isinstance(existing, dict) and any(existing.get(p) for p in results):
        return
    payload = {platform: stats.to_dict() for platform, stats in results.items()}
    save_overrides(path, payload)


def x__persist_overrides__mutmut_3(results: dict[str, PlatformStats], path: Path) -> None:
    """Seed the overrides file on first successful run so the user has a
    starting point to edit. After that, never overwrite user edits."""
    existing = load_overrides(path)
    if isinstance(existing, dict) or any(existing.get(p) for p in results):
        return
    payload = {platform: stats.to_dict() for platform, stats in results.items()}
    save_overrides(path, payload)


def x__persist_overrides__mutmut_4(results: dict[str, PlatformStats], path: Path) -> None:
    """Seed the overrides file on first successful run so the user has a
    starting point to edit. After that, never overwrite user edits."""
    existing = load_overrides(path)
    if isinstance(existing, dict) and any(None):
        return
    payload = {platform: stats.to_dict() for platform, stats in results.items()}
    save_overrides(path, payload)


def x__persist_overrides__mutmut_5(results: dict[str, PlatformStats], path: Path) -> None:
    """Seed the overrides file on first successful run so the user has a
    starting point to edit. After that, never overwrite user edits."""
    existing = load_overrides(path)
    if isinstance(existing, dict) and any(existing.get(None) for p in results):
        return
    payload = {platform: stats.to_dict() for platform, stats in results.items()}
    save_overrides(path, payload)


def x__persist_overrides__mutmut_6(results: dict[str, PlatformStats], path: Path) -> None:
    """Seed the overrides file on first successful run so the user has a
    starting point to edit. After that, never overwrite user edits."""
    existing = load_overrides(path)
    if isinstance(existing, dict) and any(existing.get(p) for p in results):
        return
    payload = None
    save_overrides(path, payload)


def x__persist_overrides__mutmut_7(results: dict[str, PlatformStats], path: Path) -> None:
    """Seed the overrides file on first successful run so the user has a
    starting point to edit. After that, never overwrite user edits."""
    existing = load_overrides(path)
    if isinstance(existing, dict) and any(existing.get(p) for p in results):
        return
    payload = {platform: stats.to_dict() for platform, stats in results.items()}
    save_overrides(None, payload)


def x__persist_overrides__mutmut_8(results: dict[str, PlatformStats], path: Path) -> None:
    """Seed the overrides file on first successful run so the user has a
    starting point to edit. After that, never overwrite user edits."""
    existing = load_overrides(path)
    if isinstance(existing, dict) and any(existing.get(p) for p in results):
        return
    payload = {platform: stats.to_dict() for platform, stats in results.items()}
    save_overrides(path, None)


def x__persist_overrides__mutmut_9(results: dict[str, PlatformStats], path: Path) -> None:
    """Seed the overrides file on first successful run so the user has a
    starting point to edit. After that, never overwrite user edits."""
    existing = load_overrides(path)
    if isinstance(existing, dict) and any(existing.get(p) for p in results):
        return
    payload = {platform: stats.to_dict() for platform, stats in results.items()}
    save_overrides(payload)


def x__persist_overrides__mutmut_10(results: dict[str, PlatformStats], path: Path) -> None:
    """Seed the overrides file on first successful run so the user has a
    starting point to edit. After that, never overwrite user edits."""
    existing = load_overrides(path)
    if isinstance(existing, dict) and any(existing.get(p) for p in results):
        return
    payload = {platform: stats.to_dict() for platform, stats in results.items()}
    save_overrides(path, )

x__persist_overrides__mutmut_mutants : ClassVar[MutantDict] = {
'x__persist_overrides__mutmut_1': x__persist_overrides__mutmut_1, 
    'x__persist_overrides__mutmut_2': x__persist_overrides__mutmut_2, 
    'x__persist_overrides__mutmut_3': x__persist_overrides__mutmut_3, 
    'x__persist_overrides__mutmut_4': x__persist_overrides__mutmut_4, 
    'x__persist_overrides__mutmut_5': x__persist_overrides__mutmut_5, 
    'x__persist_overrides__mutmut_6': x__persist_overrides__mutmut_6, 
    'x__persist_overrides__mutmut_7': x__persist_overrides__mutmut_7, 
    'x__persist_overrides__mutmut_8': x__persist_overrides__mutmut_8, 
    'x__persist_overrides__mutmut_9': x__persist_overrides__mutmut_9, 
    'x__persist_overrides__mutmut_10': x__persist_overrides__mutmut_10
}

def _persist_overrides(*args, **kwargs):
    result = _mutmut_trampoline(x__persist_overrides__mutmut_orig, x__persist_overrides__mutmut_mutants, args, kwargs)
    return result 

_persist_overrides.__signature__ = _mutmut_signature(x__persist_overrides__mutmut_orig)
x__persist_overrides__mutmut_orig.__name__ = 'x__persist_overrides'
