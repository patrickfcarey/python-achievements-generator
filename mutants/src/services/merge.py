"""Merge fresh scrape results with cached data and manual overrides."""
from __future__ import annotations

import logging
from dataclasses import replace

from ..models import PlatformStats, SubStat

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


def x_merge_with_cache__mutmut_orig(
    fresh: PlatformStats | None,
    cached: PlatformStats | None,
    platform: str,
) -> PlatformStats | None:
    """Fill holes in `fresh` from `cached`. Return cached if no fresh data."""
    if fresh is None:
        if cached is not None:
            log.info("%s: using cached data (scrape failed)", platform)
        return cached

    if cached is None:
        return fresh

    merged = replace(fresh)
    if not merged.username:
        merged.username = cached.username
    if not merged.avatar_url:
        merged.avatar_url = cached.avatar_url
    # Only fill from cache when the fresh value is genuinely missing — treat
    # 0 as a legitimate value, not "empty", so an authoritative zero never
    # gets overwritten by stale cache.
    if merged.headline_value is None or merged.headline_value == "":
        merged.headline_value = cached.headline_value
    if not merged.headline_label:
        merged.headline_label = cached.headline_label

    merged.substats = _merge_substats(merged.substats, cached.substats)

    for k, v in (cached.extra_fields or {}).items():
        if k not in merged.extra_fields or merged.extra_fields[k] is None:
            merged.extra_fields[k] = v

    return merged


def x_merge_with_cache__mutmut_1(
    fresh: PlatformStats | None,
    cached: PlatformStats | None,
    platform: str,
) -> PlatformStats | None:
    """Fill holes in `fresh` from `cached`. Return cached if no fresh data."""
    if fresh is not None:
        if cached is not None:
            log.info("%s: using cached data (scrape failed)", platform)
        return cached

    if cached is None:
        return fresh

    merged = replace(fresh)
    if not merged.username:
        merged.username = cached.username
    if not merged.avatar_url:
        merged.avatar_url = cached.avatar_url
    # Only fill from cache when the fresh value is genuinely missing — treat
    # 0 as a legitimate value, not "empty", so an authoritative zero never
    # gets overwritten by stale cache.
    if merged.headline_value is None or merged.headline_value == "":
        merged.headline_value = cached.headline_value
    if not merged.headline_label:
        merged.headline_label = cached.headline_label

    merged.substats = _merge_substats(merged.substats, cached.substats)

    for k, v in (cached.extra_fields or {}).items():
        if k not in merged.extra_fields or merged.extra_fields[k] is None:
            merged.extra_fields[k] = v

    return merged


def x_merge_with_cache__mutmut_2(
    fresh: PlatformStats | None,
    cached: PlatformStats | None,
    platform: str,
) -> PlatformStats | None:
    """Fill holes in `fresh` from `cached`. Return cached if no fresh data."""
    if fresh is None:
        if cached is None:
            log.info("%s: using cached data (scrape failed)", platform)
        return cached

    if cached is None:
        return fresh

    merged = replace(fresh)
    if not merged.username:
        merged.username = cached.username
    if not merged.avatar_url:
        merged.avatar_url = cached.avatar_url
    # Only fill from cache when the fresh value is genuinely missing — treat
    # 0 as a legitimate value, not "empty", so an authoritative zero never
    # gets overwritten by stale cache.
    if merged.headline_value is None or merged.headline_value == "":
        merged.headline_value = cached.headline_value
    if not merged.headline_label:
        merged.headline_label = cached.headline_label

    merged.substats = _merge_substats(merged.substats, cached.substats)

    for k, v in (cached.extra_fields or {}).items():
        if k not in merged.extra_fields or merged.extra_fields[k] is None:
            merged.extra_fields[k] = v

    return merged


def x_merge_with_cache__mutmut_3(
    fresh: PlatformStats | None,
    cached: PlatformStats | None,
    platform: str,
) -> PlatformStats | None:
    """Fill holes in `fresh` from `cached`. Return cached if no fresh data."""
    if fresh is None:
        if cached is not None:
            log.info(None, platform)
        return cached

    if cached is None:
        return fresh

    merged = replace(fresh)
    if not merged.username:
        merged.username = cached.username
    if not merged.avatar_url:
        merged.avatar_url = cached.avatar_url
    # Only fill from cache when the fresh value is genuinely missing — treat
    # 0 as a legitimate value, not "empty", so an authoritative zero never
    # gets overwritten by stale cache.
    if merged.headline_value is None or merged.headline_value == "":
        merged.headline_value = cached.headline_value
    if not merged.headline_label:
        merged.headline_label = cached.headline_label

    merged.substats = _merge_substats(merged.substats, cached.substats)

    for k, v in (cached.extra_fields or {}).items():
        if k not in merged.extra_fields or merged.extra_fields[k] is None:
            merged.extra_fields[k] = v

    return merged


def x_merge_with_cache__mutmut_4(
    fresh: PlatformStats | None,
    cached: PlatformStats | None,
    platform: str,
) -> PlatformStats | None:
    """Fill holes in `fresh` from `cached`. Return cached if no fresh data."""
    if fresh is None:
        if cached is not None:
            log.info("%s: using cached data (scrape failed)", None)
        return cached

    if cached is None:
        return fresh

    merged = replace(fresh)
    if not merged.username:
        merged.username = cached.username
    if not merged.avatar_url:
        merged.avatar_url = cached.avatar_url
    # Only fill from cache when the fresh value is genuinely missing — treat
    # 0 as a legitimate value, not "empty", so an authoritative zero never
    # gets overwritten by stale cache.
    if merged.headline_value is None or merged.headline_value == "":
        merged.headline_value = cached.headline_value
    if not merged.headline_label:
        merged.headline_label = cached.headline_label

    merged.substats = _merge_substats(merged.substats, cached.substats)

    for k, v in (cached.extra_fields or {}).items():
        if k not in merged.extra_fields or merged.extra_fields[k] is None:
            merged.extra_fields[k] = v

    return merged


def x_merge_with_cache__mutmut_5(
    fresh: PlatformStats | None,
    cached: PlatformStats | None,
    platform: str,
) -> PlatformStats | None:
    """Fill holes in `fresh` from `cached`. Return cached if no fresh data."""
    if fresh is None:
        if cached is not None:
            log.info(platform)
        return cached

    if cached is None:
        return fresh

    merged = replace(fresh)
    if not merged.username:
        merged.username = cached.username
    if not merged.avatar_url:
        merged.avatar_url = cached.avatar_url
    # Only fill from cache when the fresh value is genuinely missing — treat
    # 0 as a legitimate value, not "empty", so an authoritative zero never
    # gets overwritten by stale cache.
    if merged.headline_value is None or merged.headline_value == "":
        merged.headline_value = cached.headline_value
    if not merged.headline_label:
        merged.headline_label = cached.headline_label

    merged.substats = _merge_substats(merged.substats, cached.substats)

    for k, v in (cached.extra_fields or {}).items():
        if k not in merged.extra_fields or merged.extra_fields[k] is None:
            merged.extra_fields[k] = v

    return merged


def x_merge_with_cache__mutmut_6(
    fresh: PlatformStats | None,
    cached: PlatformStats | None,
    platform: str,
) -> PlatformStats | None:
    """Fill holes in `fresh` from `cached`. Return cached if no fresh data."""
    if fresh is None:
        if cached is not None:
            log.info("%s: using cached data (scrape failed)", )
        return cached

    if cached is None:
        return fresh

    merged = replace(fresh)
    if not merged.username:
        merged.username = cached.username
    if not merged.avatar_url:
        merged.avatar_url = cached.avatar_url
    # Only fill from cache when the fresh value is genuinely missing — treat
    # 0 as a legitimate value, not "empty", so an authoritative zero never
    # gets overwritten by stale cache.
    if merged.headline_value is None or merged.headline_value == "":
        merged.headline_value = cached.headline_value
    if not merged.headline_label:
        merged.headline_label = cached.headline_label

    merged.substats = _merge_substats(merged.substats, cached.substats)

    for k, v in (cached.extra_fields or {}).items():
        if k not in merged.extra_fields or merged.extra_fields[k] is None:
            merged.extra_fields[k] = v

    return merged


def x_merge_with_cache__mutmut_7(
    fresh: PlatformStats | None,
    cached: PlatformStats | None,
    platform: str,
) -> PlatformStats | None:
    """Fill holes in `fresh` from `cached`. Return cached if no fresh data."""
    if fresh is None:
        if cached is not None:
            log.info("XX%s: using cached data (scrape failed)XX", platform)
        return cached

    if cached is None:
        return fresh

    merged = replace(fresh)
    if not merged.username:
        merged.username = cached.username
    if not merged.avatar_url:
        merged.avatar_url = cached.avatar_url
    # Only fill from cache when the fresh value is genuinely missing — treat
    # 0 as a legitimate value, not "empty", so an authoritative zero never
    # gets overwritten by stale cache.
    if merged.headline_value is None or merged.headline_value == "":
        merged.headline_value = cached.headline_value
    if not merged.headline_label:
        merged.headline_label = cached.headline_label

    merged.substats = _merge_substats(merged.substats, cached.substats)

    for k, v in (cached.extra_fields or {}).items():
        if k not in merged.extra_fields or merged.extra_fields[k] is None:
            merged.extra_fields[k] = v

    return merged


def x_merge_with_cache__mutmut_8(
    fresh: PlatformStats | None,
    cached: PlatformStats | None,
    platform: str,
) -> PlatformStats | None:
    """Fill holes in `fresh` from `cached`. Return cached if no fresh data."""
    if fresh is None:
        if cached is not None:
            log.info("%S: USING CACHED DATA (SCRAPE FAILED)", platform)
        return cached

    if cached is None:
        return fresh

    merged = replace(fresh)
    if not merged.username:
        merged.username = cached.username
    if not merged.avatar_url:
        merged.avatar_url = cached.avatar_url
    # Only fill from cache when the fresh value is genuinely missing — treat
    # 0 as a legitimate value, not "empty", so an authoritative zero never
    # gets overwritten by stale cache.
    if merged.headline_value is None or merged.headline_value == "":
        merged.headline_value = cached.headline_value
    if not merged.headline_label:
        merged.headline_label = cached.headline_label

    merged.substats = _merge_substats(merged.substats, cached.substats)

    for k, v in (cached.extra_fields or {}).items():
        if k not in merged.extra_fields or merged.extra_fields[k] is None:
            merged.extra_fields[k] = v

    return merged


def x_merge_with_cache__mutmut_9(
    fresh: PlatformStats | None,
    cached: PlatformStats | None,
    platform: str,
) -> PlatformStats | None:
    """Fill holes in `fresh` from `cached`. Return cached if no fresh data."""
    if fresh is None:
        if cached is not None:
            log.info("%s: using cached data (scrape failed)", platform)
        return cached

    if cached is not None:
        return fresh

    merged = replace(fresh)
    if not merged.username:
        merged.username = cached.username
    if not merged.avatar_url:
        merged.avatar_url = cached.avatar_url
    # Only fill from cache when the fresh value is genuinely missing — treat
    # 0 as a legitimate value, not "empty", so an authoritative zero never
    # gets overwritten by stale cache.
    if merged.headline_value is None or merged.headline_value == "":
        merged.headline_value = cached.headline_value
    if not merged.headline_label:
        merged.headline_label = cached.headline_label

    merged.substats = _merge_substats(merged.substats, cached.substats)

    for k, v in (cached.extra_fields or {}).items():
        if k not in merged.extra_fields or merged.extra_fields[k] is None:
            merged.extra_fields[k] = v

    return merged


def x_merge_with_cache__mutmut_10(
    fresh: PlatformStats | None,
    cached: PlatformStats | None,
    platform: str,
) -> PlatformStats | None:
    """Fill holes in `fresh` from `cached`. Return cached if no fresh data."""
    if fresh is None:
        if cached is not None:
            log.info("%s: using cached data (scrape failed)", platform)
        return cached

    if cached is None:
        return fresh

    merged = None
    if not merged.username:
        merged.username = cached.username
    if not merged.avatar_url:
        merged.avatar_url = cached.avatar_url
    # Only fill from cache when the fresh value is genuinely missing — treat
    # 0 as a legitimate value, not "empty", so an authoritative zero never
    # gets overwritten by stale cache.
    if merged.headline_value is None or merged.headline_value == "":
        merged.headline_value = cached.headline_value
    if not merged.headline_label:
        merged.headline_label = cached.headline_label

    merged.substats = _merge_substats(merged.substats, cached.substats)

    for k, v in (cached.extra_fields or {}).items():
        if k not in merged.extra_fields or merged.extra_fields[k] is None:
            merged.extra_fields[k] = v

    return merged


def x_merge_with_cache__mutmut_11(
    fresh: PlatformStats | None,
    cached: PlatformStats | None,
    platform: str,
) -> PlatformStats | None:
    """Fill holes in `fresh` from `cached`. Return cached if no fresh data."""
    if fresh is None:
        if cached is not None:
            log.info("%s: using cached data (scrape failed)", platform)
        return cached

    if cached is None:
        return fresh

    merged = replace(None)
    if not merged.username:
        merged.username = cached.username
    if not merged.avatar_url:
        merged.avatar_url = cached.avatar_url
    # Only fill from cache when the fresh value is genuinely missing — treat
    # 0 as a legitimate value, not "empty", so an authoritative zero never
    # gets overwritten by stale cache.
    if merged.headline_value is None or merged.headline_value == "":
        merged.headline_value = cached.headline_value
    if not merged.headline_label:
        merged.headline_label = cached.headline_label

    merged.substats = _merge_substats(merged.substats, cached.substats)

    for k, v in (cached.extra_fields or {}).items():
        if k not in merged.extra_fields or merged.extra_fields[k] is None:
            merged.extra_fields[k] = v

    return merged


def x_merge_with_cache__mutmut_12(
    fresh: PlatformStats | None,
    cached: PlatformStats | None,
    platform: str,
) -> PlatformStats | None:
    """Fill holes in `fresh` from `cached`. Return cached if no fresh data."""
    if fresh is None:
        if cached is not None:
            log.info("%s: using cached data (scrape failed)", platform)
        return cached

    if cached is None:
        return fresh

    merged = replace(fresh)
    if merged.username:
        merged.username = cached.username
    if not merged.avatar_url:
        merged.avatar_url = cached.avatar_url
    # Only fill from cache when the fresh value is genuinely missing — treat
    # 0 as a legitimate value, not "empty", so an authoritative zero never
    # gets overwritten by stale cache.
    if merged.headline_value is None or merged.headline_value == "":
        merged.headline_value = cached.headline_value
    if not merged.headline_label:
        merged.headline_label = cached.headline_label

    merged.substats = _merge_substats(merged.substats, cached.substats)

    for k, v in (cached.extra_fields or {}).items():
        if k not in merged.extra_fields or merged.extra_fields[k] is None:
            merged.extra_fields[k] = v

    return merged


def x_merge_with_cache__mutmut_13(
    fresh: PlatformStats | None,
    cached: PlatformStats | None,
    platform: str,
) -> PlatformStats | None:
    """Fill holes in `fresh` from `cached`. Return cached if no fresh data."""
    if fresh is None:
        if cached is not None:
            log.info("%s: using cached data (scrape failed)", platform)
        return cached

    if cached is None:
        return fresh

    merged = replace(fresh)
    if not merged.username:
        merged.username = None
    if not merged.avatar_url:
        merged.avatar_url = cached.avatar_url
    # Only fill from cache when the fresh value is genuinely missing — treat
    # 0 as a legitimate value, not "empty", so an authoritative zero never
    # gets overwritten by stale cache.
    if merged.headline_value is None or merged.headline_value == "":
        merged.headline_value = cached.headline_value
    if not merged.headline_label:
        merged.headline_label = cached.headline_label

    merged.substats = _merge_substats(merged.substats, cached.substats)

    for k, v in (cached.extra_fields or {}).items():
        if k not in merged.extra_fields or merged.extra_fields[k] is None:
            merged.extra_fields[k] = v

    return merged


def x_merge_with_cache__mutmut_14(
    fresh: PlatformStats | None,
    cached: PlatformStats | None,
    platform: str,
) -> PlatformStats | None:
    """Fill holes in `fresh` from `cached`. Return cached if no fresh data."""
    if fresh is None:
        if cached is not None:
            log.info("%s: using cached data (scrape failed)", platform)
        return cached

    if cached is None:
        return fresh

    merged = replace(fresh)
    if not merged.username:
        merged.username = cached.username
    if merged.avatar_url:
        merged.avatar_url = cached.avatar_url
    # Only fill from cache when the fresh value is genuinely missing — treat
    # 0 as a legitimate value, not "empty", so an authoritative zero never
    # gets overwritten by stale cache.
    if merged.headline_value is None or merged.headline_value == "":
        merged.headline_value = cached.headline_value
    if not merged.headline_label:
        merged.headline_label = cached.headline_label

    merged.substats = _merge_substats(merged.substats, cached.substats)

    for k, v in (cached.extra_fields or {}).items():
        if k not in merged.extra_fields or merged.extra_fields[k] is None:
            merged.extra_fields[k] = v

    return merged


def x_merge_with_cache__mutmut_15(
    fresh: PlatformStats | None,
    cached: PlatformStats | None,
    platform: str,
) -> PlatformStats | None:
    """Fill holes in `fresh` from `cached`. Return cached if no fresh data."""
    if fresh is None:
        if cached is not None:
            log.info("%s: using cached data (scrape failed)", platform)
        return cached

    if cached is None:
        return fresh

    merged = replace(fresh)
    if not merged.username:
        merged.username = cached.username
    if not merged.avatar_url:
        merged.avatar_url = None
    # Only fill from cache when the fresh value is genuinely missing — treat
    # 0 as a legitimate value, not "empty", so an authoritative zero never
    # gets overwritten by stale cache.
    if merged.headline_value is None or merged.headline_value == "":
        merged.headline_value = cached.headline_value
    if not merged.headline_label:
        merged.headline_label = cached.headline_label

    merged.substats = _merge_substats(merged.substats, cached.substats)

    for k, v in (cached.extra_fields or {}).items():
        if k not in merged.extra_fields or merged.extra_fields[k] is None:
            merged.extra_fields[k] = v

    return merged


def x_merge_with_cache__mutmut_16(
    fresh: PlatformStats | None,
    cached: PlatformStats | None,
    platform: str,
) -> PlatformStats | None:
    """Fill holes in `fresh` from `cached`. Return cached if no fresh data."""
    if fresh is None:
        if cached is not None:
            log.info("%s: using cached data (scrape failed)", platform)
        return cached

    if cached is None:
        return fresh

    merged = replace(fresh)
    if not merged.username:
        merged.username = cached.username
    if not merged.avatar_url:
        merged.avatar_url = cached.avatar_url
    # Only fill from cache when the fresh value is genuinely missing — treat
    # 0 as a legitimate value, not "empty", so an authoritative zero never
    # gets overwritten by stale cache.
    if merged.headline_value is None and merged.headline_value == "":
        merged.headline_value = cached.headline_value
    if not merged.headline_label:
        merged.headline_label = cached.headline_label

    merged.substats = _merge_substats(merged.substats, cached.substats)

    for k, v in (cached.extra_fields or {}).items():
        if k not in merged.extra_fields or merged.extra_fields[k] is None:
            merged.extra_fields[k] = v

    return merged


def x_merge_with_cache__mutmut_17(
    fresh: PlatformStats | None,
    cached: PlatformStats | None,
    platform: str,
) -> PlatformStats | None:
    """Fill holes in `fresh` from `cached`. Return cached if no fresh data."""
    if fresh is None:
        if cached is not None:
            log.info("%s: using cached data (scrape failed)", platform)
        return cached

    if cached is None:
        return fresh

    merged = replace(fresh)
    if not merged.username:
        merged.username = cached.username
    if not merged.avatar_url:
        merged.avatar_url = cached.avatar_url
    # Only fill from cache when the fresh value is genuinely missing — treat
    # 0 as a legitimate value, not "empty", so an authoritative zero never
    # gets overwritten by stale cache.
    if merged.headline_value is not None or merged.headline_value == "":
        merged.headline_value = cached.headline_value
    if not merged.headline_label:
        merged.headline_label = cached.headline_label

    merged.substats = _merge_substats(merged.substats, cached.substats)

    for k, v in (cached.extra_fields or {}).items():
        if k not in merged.extra_fields or merged.extra_fields[k] is None:
            merged.extra_fields[k] = v

    return merged


def x_merge_with_cache__mutmut_18(
    fresh: PlatformStats | None,
    cached: PlatformStats | None,
    platform: str,
) -> PlatformStats | None:
    """Fill holes in `fresh` from `cached`. Return cached if no fresh data."""
    if fresh is None:
        if cached is not None:
            log.info("%s: using cached data (scrape failed)", platform)
        return cached

    if cached is None:
        return fresh

    merged = replace(fresh)
    if not merged.username:
        merged.username = cached.username
    if not merged.avatar_url:
        merged.avatar_url = cached.avatar_url
    # Only fill from cache when the fresh value is genuinely missing — treat
    # 0 as a legitimate value, not "empty", so an authoritative zero never
    # gets overwritten by stale cache.
    if merged.headline_value is None or merged.headline_value != "":
        merged.headline_value = cached.headline_value
    if not merged.headline_label:
        merged.headline_label = cached.headline_label

    merged.substats = _merge_substats(merged.substats, cached.substats)

    for k, v in (cached.extra_fields or {}).items():
        if k not in merged.extra_fields or merged.extra_fields[k] is None:
            merged.extra_fields[k] = v

    return merged


def x_merge_with_cache__mutmut_19(
    fresh: PlatformStats | None,
    cached: PlatformStats | None,
    platform: str,
) -> PlatformStats | None:
    """Fill holes in `fresh` from `cached`. Return cached if no fresh data."""
    if fresh is None:
        if cached is not None:
            log.info("%s: using cached data (scrape failed)", platform)
        return cached

    if cached is None:
        return fresh

    merged = replace(fresh)
    if not merged.username:
        merged.username = cached.username
    if not merged.avatar_url:
        merged.avatar_url = cached.avatar_url
    # Only fill from cache when the fresh value is genuinely missing — treat
    # 0 as a legitimate value, not "empty", so an authoritative zero never
    # gets overwritten by stale cache.
    if merged.headline_value is None or merged.headline_value == "XXXX":
        merged.headline_value = cached.headline_value
    if not merged.headline_label:
        merged.headline_label = cached.headline_label

    merged.substats = _merge_substats(merged.substats, cached.substats)

    for k, v in (cached.extra_fields or {}).items():
        if k not in merged.extra_fields or merged.extra_fields[k] is None:
            merged.extra_fields[k] = v

    return merged


def x_merge_with_cache__mutmut_20(
    fresh: PlatformStats | None,
    cached: PlatformStats | None,
    platform: str,
) -> PlatformStats | None:
    """Fill holes in `fresh` from `cached`. Return cached if no fresh data."""
    if fresh is None:
        if cached is not None:
            log.info("%s: using cached data (scrape failed)", platform)
        return cached

    if cached is None:
        return fresh

    merged = replace(fresh)
    if not merged.username:
        merged.username = cached.username
    if not merged.avatar_url:
        merged.avatar_url = cached.avatar_url
    # Only fill from cache when the fresh value is genuinely missing — treat
    # 0 as a legitimate value, not "empty", so an authoritative zero never
    # gets overwritten by stale cache.
    if merged.headline_value is None or merged.headline_value == "":
        merged.headline_value = None
    if not merged.headline_label:
        merged.headline_label = cached.headline_label

    merged.substats = _merge_substats(merged.substats, cached.substats)

    for k, v in (cached.extra_fields or {}).items():
        if k not in merged.extra_fields or merged.extra_fields[k] is None:
            merged.extra_fields[k] = v

    return merged


def x_merge_with_cache__mutmut_21(
    fresh: PlatformStats | None,
    cached: PlatformStats | None,
    platform: str,
) -> PlatformStats | None:
    """Fill holes in `fresh` from `cached`. Return cached if no fresh data."""
    if fresh is None:
        if cached is not None:
            log.info("%s: using cached data (scrape failed)", platform)
        return cached

    if cached is None:
        return fresh

    merged = replace(fresh)
    if not merged.username:
        merged.username = cached.username
    if not merged.avatar_url:
        merged.avatar_url = cached.avatar_url
    # Only fill from cache when the fresh value is genuinely missing — treat
    # 0 as a legitimate value, not "empty", so an authoritative zero never
    # gets overwritten by stale cache.
    if merged.headline_value is None or merged.headline_value == "":
        merged.headline_value = cached.headline_value
    if merged.headline_label:
        merged.headline_label = cached.headline_label

    merged.substats = _merge_substats(merged.substats, cached.substats)

    for k, v in (cached.extra_fields or {}).items():
        if k not in merged.extra_fields or merged.extra_fields[k] is None:
            merged.extra_fields[k] = v

    return merged


def x_merge_with_cache__mutmut_22(
    fresh: PlatformStats | None,
    cached: PlatformStats | None,
    platform: str,
) -> PlatformStats | None:
    """Fill holes in `fresh` from `cached`. Return cached if no fresh data."""
    if fresh is None:
        if cached is not None:
            log.info("%s: using cached data (scrape failed)", platform)
        return cached

    if cached is None:
        return fresh

    merged = replace(fresh)
    if not merged.username:
        merged.username = cached.username
    if not merged.avatar_url:
        merged.avatar_url = cached.avatar_url
    # Only fill from cache when the fresh value is genuinely missing — treat
    # 0 as a legitimate value, not "empty", so an authoritative zero never
    # gets overwritten by stale cache.
    if merged.headline_value is None or merged.headline_value == "":
        merged.headline_value = cached.headline_value
    if not merged.headline_label:
        merged.headline_label = None

    merged.substats = _merge_substats(merged.substats, cached.substats)

    for k, v in (cached.extra_fields or {}).items():
        if k not in merged.extra_fields or merged.extra_fields[k] is None:
            merged.extra_fields[k] = v

    return merged


def x_merge_with_cache__mutmut_23(
    fresh: PlatformStats | None,
    cached: PlatformStats | None,
    platform: str,
) -> PlatformStats | None:
    """Fill holes in `fresh` from `cached`. Return cached if no fresh data."""
    if fresh is None:
        if cached is not None:
            log.info("%s: using cached data (scrape failed)", platform)
        return cached

    if cached is None:
        return fresh

    merged = replace(fresh)
    if not merged.username:
        merged.username = cached.username
    if not merged.avatar_url:
        merged.avatar_url = cached.avatar_url
    # Only fill from cache when the fresh value is genuinely missing — treat
    # 0 as a legitimate value, not "empty", so an authoritative zero never
    # gets overwritten by stale cache.
    if merged.headline_value is None or merged.headline_value == "":
        merged.headline_value = cached.headline_value
    if not merged.headline_label:
        merged.headline_label = cached.headline_label

    merged.substats = None

    for k, v in (cached.extra_fields or {}).items():
        if k not in merged.extra_fields or merged.extra_fields[k] is None:
            merged.extra_fields[k] = v

    return merged


def x_merge_with_cache__mutmut_24(
    fresh: PlatformStats | None,
    cached: PlatformStats | None,
    platform: str,
) -> PlatformStats | None:
    """Fill holes in `fresh` from `cached`. Return cached if no fresh data."""
    if fresh is None:
        if cached is not None:
            log.info("%s: using cached data (scrape failed)", platform)
        return cached

    if cached is None:
        return fresh

    merged = replace(fresh)
    if not merged.username:
        merged.username = cached.username
    if not merged.avatar_url:
        merged.avatar_url = cached.avatar_url
    # Only fill from cache when the fresh value is genuinely missing — treat
    # 0 as a legitimate value, not "empty", so an authoritative zero never
    # gets overwritten by stale cache.
    if merged.headline_value is None or merged.headline_value == "":
        merged.headline_value = cached.headline_value
    if not merged.headline_label:
        merged.headline_label = cached.headline_label

    merged.substats = _merge_substats(None, cached.substats)

    for k, v in (cached.extra_fields or {}).items():
        if k not in merged.extra_fields or merged.extra_fields[k] is None:
            merged.extra_fields[k] = v

    return merged


def x_merge_with_cache__mutmut_25(
    fresh: PlatformStats | None,
    cached: PlatformStats | None,
    platform: str,
) -> PlatformStats | None:
    """Fill holes in `fresh` from `cached`. Return cached if no fresh data."""
    if fresh is None:
        if cached is not None:
            log.info("%s: using cached data (scrape failed)", platform)
        return cached

    if cached is None:
        return fresh

    merged = replace(fresh)
    if not merged.username:
        merged.username = cached.username
    if not merged.avatar_url:
        merged.avatar_url = cached.avatar_url
    # Only fill from cache when the fresh value is genuinely missing — treat
    # 0 as a legitimate value, not "empty", so an authoritative zero never
    # gets overwritten by stale cache.
    if merged.headline_value is None or merged.headline_value == "":
        merged.headline_value = cached.headline_value
    if not merged.headline_label:
        merged.headline_label = cached.headline_label

    merged.substats = _merge_substats(merged.substats, None)

    for k, v in (cached.extra_fields or {}).items():
        if k not in merged.extra_fields or merged.extra_fields[k] is None:
            merged.extra_fields[k] = v

    return merged


def x_merge_with_cache__mutmut_26(
    fresh: PlatformStats | None,
    cached: PlatformStats | None,
    platform: str,
) -> PlatformStats | None:
    """Fill holes in `fresh` from `cached`. Return cached if no fresh data."""
    if fresh is None:
        if cached is not None:
            log.info("%s: using cached data (scrape failed)", platform)
        return cached

    if cached is None:
        return fresh

    merged = replace(fresh)
    if not merged.username:
        merged.username = cached.username
    if not merged.avatar_url:
        merged.avatar_url = cached.avatar_url
    # Only fill from cache when the fresh value is genuinely missing — treat
    # 0 as a legitimate value, not "empty", so an authoritative zero never
    # gets overwritten by stale cache.
    if merged.headline_value is None or merged.headline_value == "":
        merged.headline_value = cached.headline_value
    if not merged.headline_label:
        merged.headline_label = cached.headline_label

    merged.substats = _merge_substats(cached.substats)

    for k, v in (cached.extra_fields or {}).items():
        if k not in merged.extra_fields or merged.extra_fields[k] is None:
            merged.extra_fields[k] = v

    return merged


def x_merge_with_cache__mutmut_27(
    fresh: PlatformStats | None,
    cached: PlatformStats | None,
    platform: str,
) -> PlatformStats | None:
    """Fill holes in `fresh` from `cached`. Return cached if no fresh data."""
    if fresh is None:
        if cached is not None:
            log.info("%s: using cached data (scrape failed)", platform)
        return cached

    if cached is None:
        return fresh

    merged = replace(fresh)
    if not merged.username:
        merged.username = cached.username
    if not merged.avatar_url:
        merged.avatar_url = cached.avatar_url
    # Only fill from cache when the fresh value is genuinely missing — treat
    # 0 as a legitimate value, not "empty", so an authoritative zero never
    # gets overwritten by stale cache.
    if merged.headline_value is None or merged.headline_value == "":
        merged.headline_value = cached.headline_value
    if not merged.headline_label:
        merged.headline_label = cached.headline_label

    merged.substats = _merge_substats(merged.substats, )

    for k, v in (cached.extra_fields or {}).items():
        if k not in merged.extra_fields or merged.extra_fields[k] is None:
            merged.extra_fields[k] = v

    return merged


def x_merge_with_cache__mutmut_28(
    fresh: PlatformStats | None,
    cached: PlatformStats | None,
    platform: str,
) -> PlatformStats | None:
    """Fill holes in `fresh` from `cached`. Return cached if no fresh data."""
    if fresh is None:
        if cached is not None:
            log.info("%s: using cached data (scrape failed)", platform)
        return cached

    if cached is None:
        return fresh

    merged = replace(fresh)
    if not merged.username:
        merged.username = cached.username
    if not merged.avatar_url:
        merged.avatar_url = cached.avatar_url
    # Only fill from cache when the fresh value is genuinely missing — treat
    # 0 as a legitimate value, not "empty", so an authoritative zero never
    # gets overwritten by stale cache.
    if merged.headline_value is None or merged.headline_value == "":
        merged.headline_value = cached.headline_value
    if not merged.headline_label:
        merged.headline_label = cached.headline_label

    merged.substats = _merge_substats(merged.substats, cached.substats)

    for k, v in (cached.extra_fields and {}).items():
        if k not in merged.extra_fields or merged.extra_fields[k] is None:
            merged.extra_fields[k] = v

    return merged


def x_merge_with_cache__mutmut_29(
    fresh: PlatformStats | None,
    cached: PlatformStats | None,
    platform: str,
) -> PlatformStats | None:
    """Fill holes in `fresh` from `cached`. Return cached if no fresh data."""
    if fresh is None:
        if cached is not None:
            log.info("%s: using cached data (scrape failed)", platform)
        return cached

    if cached is None:
        return fresh

    merged = replace(fresh)
    if not merged.username:
        merged.username = cached.username
    if not merged.avatar_url:
        merged.avatar_url = cached.avatar_url
    # Only fill from cache when the fresh value is genuinely missing — treat
    # 0 as a legitimate value, not "empty", so an authoritative zero never
    # gets overwritten by stale cache.
    if merged.headline_value is None or merged.headline_value == "":
        merged.headline_value = cached.headline_value
    if not merged.headline_label:
        merged.headline_label = cached.headline_label

    merged.substats = _merge_substats(merged.substats, cached.substats)

    for k, v in (cached.extra_fields or {}).items():
        if k not in merged.extra_fields and merged.extra_fields[k] is None:
            merged.extra_fields[k] = v

    return merged


def x_merge_with_cache__mutmut_30(
    fresh: PlatformStats | None,
    cached: PlatformStats | None,
    platform: str,
) -> PlatformStats | None:
    """Fill holes in `fresh` from `cached`. Return cached if no fresh data."""
    if fresh is None:
        if cached is not None:
            log.info("%s: using cached data (scrape failed)", platform)
        return cached

    if cached is None:
        return fresh

    merged = replace(fresh)
    if not merged.username:
        merged.username = cached.username
    if not merged.avatar_url:
        merged.avatar_url = cached.avatar_url
    # Only fill from cache when the fresh value is genuinely missing — treat
    # 0 as a legitimate value, not "empty", so an authoritative zero never
    # gets overwritten by stale cache.
    if merged.headline_value is None or merged.headline_value == "":
        merged.headline_value = cached.headline_value
    if not merged.headline_label:
        merged.headline_label = cached.headline_label

    merged.substats = _merge_substats(merged.substats, cached.substats)

    for k, v in (cached.extra_fields or {}).items():
        if k in merged.extra_fields or merged.extra_fields[k] is None:
            merged.extra_fields[k] = v

    return merged


def x_merge_with_cache__mutmut_31(
    fresh: PlatformStats | None,
    cached: PlatformStats | None,
    platform: str,
) -> PlatformStats | None:
    """Fill holes in `fresh` from `cached`. Return cached if no fresh data."""
    if fresh is None:
        if cached is not None:
            log.info("%s: using cached data (scrape failed)", platform)
        return cached

    if cached is None:
        return fresh

    merged = replace(fresh)
    if not merged.username:
        merged.username = cached.username
    if not merged.avatar_url:
        merged.avatar_url = cached.avatar_url
    # Only fill from cache when the fresh value is genuinely missing — treat
    # 0 as a legitimate value, not "empty", so an authoritative zero never
    # gets overwritten by stale cache.
    if merged.headline_value is None or merged.headline_value == "":
        merged.headline_value = cached.headline_value
    if not merged.headline_label:
        merged.headline_label = cached.headline_label

    merged.substats = _merge_substats(merged.substats, cached.substats)

    for k, v in (cached.extra_fields or {}).items():
        if k not in merged.extra_fields or merged.extra_fields[k] is not None:
            merged.extra_fields[k] = v

    return merged


def x_merge_with_cache__mutmut_32(
    fresh: PlatformStats | None,
    cached: PlatformStats | None,
    platform: str,
) -> PlatformStats | None:
    """Fill holes in `fresh` from `cached`. Return cached if no fresh data."""
    if fresh is None:
        if cached is not None:
            log.info("%s: using cached data (scrape failed)", platform)
        return cached

    if cached is None:
        return fresh

    merged = replace(fresh)
    if not merged.username:
        merged.username = cached.username
    if not merged.avatar_url:
        merged.avatar_url = cached.avatar_url
    # Only fill from cache when the fresh value is genuinely missing — treat
    # 0 as a legitimate value, not "empty", so an authoritative zero never
    # gets overwritten by stale cache.
    if merged.headline_value is None or merged.headline_value == "":
        merged.headline_value = cached.headline_value
    if not merged.headline_label:
        merged.headline_label = cached.headline_label

    merged.substats = _merge_substats(merged.substats, cached.substats)

    for k, v in (cached.extra_fields or {}).items():
        if k not in merged.extra_fields or merged.extra_fields[k] is None:
            merged.extra_fields[k] = None

    return merged

x_merge_with_cache__mutmut_mutants : ClassVar[MutantDict] = {
'x_merge_with_cache__mutmut_1': x_merge_with_cache__mutmut_1, 
    'x_merge_with_cache__mutmut_2': x_merge_with_cache__mutmut_2, 
    'x_merge_with_cache__mutmut_3': x_merge_with_cache__mutmut_3, 
    'x_merge_with_cache__mutmut_4': x_merge_with_cache__mutmut_4, 
    'x_merge_with_cache__mutmut_5': x_merge_with_cache__mutmut_5, 
    'x_merge_with_cache__mutmut_6': x_merge_with_cache__mutmut_6, 
    'x_merge_with_cache__mutmut_7': x_merge_with_cache__mutmut_7, 
    'x_merge_with_cache__mutmut_8': x_merge_with_cache__mutmut_8, 
    'x_merge_with_cache__mutmut_9': x_merge_with_cache__mutmut_9, 
    'x_merge_with_cache__mutmut_10': x_merge_with_cache__mutmut_10, 
    'x_merge_with_cache__mutmut_11': x_merge_with_cache__mutmut_11, 
    'x_merge_with_cache__mutmut_12': x_merge_with_cache__mutmut_12, 
    'x_merge_with_cache__mutmut_13': x_merge_with_cache__mutmut_13, 
    'x_merge_with_cache__mutmut_14': x_merge_with_cache__mutmut_14, 
    'x_merge_with_cache__mutmut_15': x_merge_with_cache__mutmut_15, 
    'x_merge_with_cache__mutmut_16': x_merge_with_cache__mutmut_16, 
    'x_merge_with_cache__mutmut_17': x_merge_with_cache__mutmut_17, 
    'x_merge_with_cache__mutmut_18': x_merge_with_cache__mutmut_18, 
    'x_merge_with_cache__mutmut_19': x_merge_with_cache__mutmut_19, 
    'x_merge_with_cache__mutmut_20': x_merge_with_cache__mutmut_20, 
    'x_merge_with_cache__mutmut_21': x_merge_with_cache__mutmut_21, 
    'x_merge_with_cache__mutmut_22': x_merge_with_cache__mutmut_22, 
    'x_merge_with_cache__mutmut_23': x_merge_with_cache__mutmut_23, 
    'x_merge_with_cache__mutmut_24': x_merge_with_cache__mutmut_24, 
    'x_merge_with_cache__mutmut_25': x_merge_with_cache__mutmut_25, 
    'x_merge_with_cache__mutmut_26': x_merge_with_cache__mutmut_26, 
    'x_merge_with_cache__mutmut_27': x_merge_with_cache__mutmut_27, 
    'x_merge_with_cache__mutmut_28': x_merge_with_cache__mutmut_28, 
    'x_merge_with_cache__mutmut_29': x_merge_with_cache__mutmut_29, 
    'x_merge_with_cache__mutmut_30': x_merge_with_cache__mutmut_30, 
    'x_merge_with_cache__mutmut_31': x_merge_with_cache__mutmut_31, 
    'x_merge_with_cache__mutmut_32': x_merge_with_cache__mutmut_32
}

def merge_with_cache(*args, **kwargs):
    result = _mutmut_trampoline(x_merge_with_cache__mutmut_orig, x_merge_with_cache__mutmut_mutants, args, kwargs)
    return result 

merge_with_cache.__signature__ = _mutmut_signature(x_merge_with_cache__mutmut_orig)
x_merge_with_cache__mutmut_orig.__name__ = 'x_merge_with_cache'


def x__merge_substats__mutmut_orig(fresh: list[SubStat], cached: list[SubStat]) -> list[SubStat]:
    by_label = {s.label: s for s in cached}
    out: list[SubStat] = []
    for s in fresh:
        if s.value is None and s.label in by_label:
            out.append(by_label[s.label])
        else:
            out.append(s)
    # append any cached stats that are missing from fresh
    seen = {s.label for s in out}
    for s in cached:
        if s.label not in seen:
            out.append(s)
    return out


def x__merge_substats__mutmut_1(fresh: list[SubStat], cached: list[SubStat]) -> list[SubStat]:
    by_label = None
    out: list[SubStat] = []
    for s in fresh:
        if s.value is None and s.label in by_label:
            out.append(by_label[s.label])
        else:
            out.append(s)
    # append any cached stats that are missing from fresh
    seen = {s.label for s in out}
    for s in cached:
        if s.label not in seen:
            out.append(s)
    return out


def x__merge_substats__mutmut_2(fresh: list[SubStat], cached: list[SubStat]) -> list[SubStat]:
    by_label = {s.label: s for s in cached}
    out: list[SubStat] = None
    for s in fresh:
        if s.value is None and s.label in by_label:
            out.append(by_label[s.label])
        else:
            out.append(s)
    # append any cached stats that are missing from fresh
    seen = {s.label for s in out}
    for s in cached:
        if s.label not in seen:
            out.append(s)
    return out


def x__merge_substats__mutmut_3(fresh: list[SubStat], cached: list[SubStat]) -> list[SubStat]:
    by_label = {s.label: s for s in cached}
    out: list[SubStat] = []
    for s in fresh:
        if s.value is None or s.label in by_label:
            out.append(by_label[s.label])
        else:
            out.append(s)
    # append any cached stats that are missing from fresh
    seen = {s.label for s in out}
    for s in cached:
        if s.label not in seen:
            out.append(s)
    return out


def x__merge_substats__mutmut_4(fresh: list[SubStat], cached: list[SubStat]) -> list[SubStat]:
    by_label = {s.label: s for s in cached}
    out: list[SubStat] = []
    for s in fresh:
        if s.value is not None and s.label in by_label:
            out.append(by_label[s.label])
        else:
            out.append(s)
    # append any cached stats that are missing from fresh
    seen = {s.label for s in out}
    for s in cached:
        if s.label not in seen:
            out.append(s)
    return out


def x__merge_substats__mutmut_5(fresh: list[SubStat], cached: list[SubStat]) -> list[SubStat]:
    by_label = {s.label: s for s in cached}
    out: list[SubStat] = []
    for s in fresh:
        if s.value is None and s.label not in by_label:
            out.append(by_label[s.label])
        else:
            out.append(s)
    # append any cached stats that are missing from fresh
    seen = {s.label for s in out}
    for s in cached:
        if s.label not in seen:
            out.append(s)
    return out


def x__merge_substats__mutmut_6(fresh: list[SubStat], cached: list[SubStat]) -> list[SubStat]:
    by_label = {s.label: s for s in cached}
    out: list[SubStat] = []
    for s in fresh:
        if s.value is None and s.label in by_label:
            out.append(None)
        else:
            out.append(s)
    # append any cached stats that are missing from fresh
    seen = {s.label for s in out}
    for s in cached:
        if s.label not in seen:
            out.append(s)
    return out


def x__merge_substats__mutmut_7(fresh: list[SubStat], cached: list[SubStat]) -> list[SubStat]:
    by_label = {s.label: s for s in cached}
    out: list[SubStat] = []
    for s in fresh:
        if s.value is None and s.label in by_label:
            out.append(by_label[s.label])
        else:
            out.append(None)
    # append any cached stats that are missing from fresh
    seen = {s.label for s in out}
    for s in cached:
        if s.label not in seen:
            out.append(s)
    return out


def x__merge_substats__mutmut_8(fresh: list[SubStat], cached: list[SubStat]) -> list[SubStat]:
    by_label = {s.label: s for s in cached}
    out: list[SubStat] = []
    for s in fresh:
        if s.value is None and s.label in by_label:
            out.append(by_label[s.label])
        else:
            out.append(s)
    # append any cached stats that are missing from fresh
    seen = None
    for s in cached:
        if s.label not in seen:
            out.append(s)
    return out


def x__merge_substats__mutmut_9(fresh: list[SubStat], cached: list[SubStat]) -> list[SubStat]:
    by_label = {s.label: s for s in cached}
    out: list[SubStat] = []
    for s in fresh:
        if s.value is None and s.label in by_label:
            out.append(by_label[s.label])
        else:
            out.append(s)
    # append any cached stats that are missing from fresh
    seen = {s.label for s in out}
    for s in cached:
        if s.label in seen:
            out.append(s)
    return out


def x__merge_substats__mutmut_10(fresh: list[SubStat], cached: list[SubStat]) -> list[SubStat]:
    by_label = {s.label: s for s in cached}
    out: list[SubStat] = []
    for s in fresh:
        if s.value is None and s.label in by_label:
            out.append(by_label[s.label])
        else:
            out.append(s)
    # append any cached stats that are missing from fresh
    seen = {s.label for s in out}
    for s in cached:
        if s.label not in seen:
            out.append(None)
    return out

x__merge_substats__mutmut_mutants : ClassVar[MutantDict] = {
'x__merge_substats__mutmut_1': x__merge_substats__mutmut_1, 
    'x__merge_substats__mutmut_2': x__merge_substats__mutmut_2, 
    'x__merge_substats__mutmut_3': x__merge_substats__mutmut_3, 
    'x__merge_substats__mutmut_4': x__merge_substats__mutmut_4, 
    'x__merge_substats__mutmut_5': x__merge_substats__mutmut_5, 
    'x__merge_substats__mutmut_6': x__merge_substats__mutmut_6, 
    'x__merge_substats__mutmut_7': x__merge_substats__mutmut_7, 
    'x__merge_substats__mutmut_8': x__merge_substats__mutmut_8, 
    'x__merge_substats__mutmut_9': x__merge_substats__mutmut_9, 
    'x__merge_substats__mutmut_10': x__merge_substats__mutmut_10
}

def _merge_substats(*args, **kwargs):
    result = _mutmut_trampoline(x__merge_substats__mutmut_orig, x__merge_substats__mutmut_mutants, args, kwargs)
    return result 

_merge_substats.__signature__ = _mutmut_signature(x__merge_substats__mutmut_orig)
x__merge_substats__mutmut_orig.__name__ = 'x__merge_substats'


def x_apply_override__mutmut_orig(stats: PlatformStats | None, override: dict | None, platform: str) -> PlatformStats:
    """Build or patch a PlatformStats from a manual override dict."""
    if not override:
        return stats or PlatformStats(platform=platform)
    base = stats or PlatformStats(platform=platform)
    data = base.to_dict()
    for k, v in override.items():
        if k == "substats" and isinstance(v, list):
            data["substats"] = v
        elif k == "extra_fields" and isinstance(v, dict):
            data.setdefault("extra_fields", {}).update(v)
        else:
            data[k] = v
    return PlatformStats.from_dict(data)


def x_apply_override__mutmut_1(stats: PlatformStats | None, override: dict | None, platform: str) -> PlatformStats:
    """Build or patch a PlatformStats from a manual override dict."""
    if override:
        return stats or PlatformStats(platform=platform)
    base = stats or PlatformStats(platform=platform)
    data = base.to_dict()
    for k, v in override.items():
        if k == "substats" and isinstance(v, list):
            data["substats"] = v
        elif k == "extra_fields" and isinstance(v, dict):
            data.setdefault("extra_fields", {}).update(v)
        else:
            data[k] = v
    return PlatformStats.from_dict(data)


def x_apply_override__mutmut_2(stats: PlatformStats | None, override: dict | None, platform: str) -> PlatformStats:
    """Build or patch a PlatformStats from a manual override dict."""
    if not override:
        return stats and PlatformStats(platform=platform)
    base = stats or PlatformStats(platform=platform)
    data = base.to_dict()
    for k, v in override.items():
        if k == "substats" and isinstance(v, list):
            data["substats"] = v
        elif k == "extra_fields" and isinstance(v, dict):
            data.setdefault("extra_fields", {}).update(v)
        else:
            data[k] = v
    return PlatformStats.from_dict(data)


def x_apply_override__mutmut_3(stats: PlatformStats | None, override: dict | None, platform: str) -> PlatformStats:
    """Build or patch a PlatformStats from a manual override dict."""
    if not override:
        return stats or PlatformStats(platform=None)
    base = stats or PlatformStats(platform=platform)
    data = base.to_dict()
    for k, v in override.items():
        if k == "substats" and isinstance(v, list):
            data["substats"] = v
        elif k == "extra_fields" and isinstance(v, dict):
            data.setdefault("extra_fields", {}).update(v)
        else:
            data[k] = v
    return PlatformStats.from_dict(data)


def x_apply_override__mutmut_4(stats: PlatformStats | None, override: dict | None, platform: str) -> PlatformStats:
    """Build or patch a PlatformStats from a manual override dict."""
    if not override:
        return stats or PlatformStats(platform=platform)
    base = None
    data = base.to_dict()
    for k, v in override.items():
        if k == "substats" and isinstance(v, list):
            data["substats"] = v
        elif k == "extra_fields" and isinstance(v, dict):
            data.setdefault("extra_fields", {}).update(v)
        else:
            data[k] = v
    return PlatformStats.from_dict(data)


def x_apply_override__mutmut_5(stats: PlatformStats | None, override: dict | None, platform: str) -> PlatformStats:
    """Build or patch a PlatformStats from a manual override dict."""
    if not override:
        return stats or PlatformStats(platform=platform)
    base = stats and PlatformStats(platform=platform)
    data = base.to_dict()
    for k, v in override.items():
        if k == "substats" and isinstance(v, list):
            data["substats"] = v
        elif k == "extra_fields" and isinstance(v, dict):
            data.setdefault("extra_fields", {}).update(v)
        else:
            data[k] = v
    return PlatformStats.from_dict(data)


def x_apply_override__mutmut_6(stats: PlatformStats | None, override: dict | None, platform: str) -> PlatformStats:
    """Build or patch a PlatformStats from a manual override dict."""
    if not override:
        return stats or PlatformStats(platform=platform)
    base = stats or PlatformStats(platform=None)
    data = base.to_dict()
    for k, v in override.items():
        if k == "substats" and isinstance(v, list):
            data["substats"] = v
        elif k == "extra_fields" and isinstance(v, dict):
            data.setdefault("extra_fields", {}).update(v)
        else:
            data[k] = v
    return PlatformStats.from_dict(data)


def x_apply_override__mutmut_7(stats: PlatformStats | None, override: dict | None, platform: str) -> PlatformStats:
    """Build or patch a PlatformStats from a manual override dict."""
    if not override:
        return stats or PlatformStats(platform=platform)
    base = stats or PlatformStats(platform=platform)
    data = None
    for k, v in override.items():
        if k == "substats" and isinstance(v, list):
            data["substats"] = v
        elif k == "extra_fields" and isinstance(v, dict):
            data.setdefault("extra_fields", {}).update(v)
        else:
            data[k] = v
    return PlatformStats.from_dict(data)


def x_apply_override__mutmut_8(stats: PlatformStats | None, override: dict | None, platform: str) -> PlatformStats:
    """Build or patch a PlatformStats from a manual override dict."""
    if not override:
        return stats or PlatformStats(platform=platform)
    base = stats or PlatformStats(platform=platform)
    data = base.to_dict()
    for k, v in override.items():
        if k == "substats" or isinstance(v, list):
            data["substats"] = v
        elif k == "extra_fields" and isinstance(v, dict):
            data.setdefault("extra_fields", {}).update(v)
        else:
            data[k] = v
    return PlatformStats.from_dict(data)


def x_apply_override__mutmut_9(stats: PlatformStats | None, override: dict | None, platform: str) -> PlatformStats:
    """Build or patch a PlatformStats from a manual override dict."""
    if not override:
        return stats or PlatformStats(platform=platform)
    base = stats or PlatformStats(platform=platform)
    data = base.to_dict()
    for k, v in override.items():
        if k != "substats" and isinstance(v, list):
            data["substats"] = v
        elif k == "extra_fields" and isinstance(v, dict):
            data.setdefault("extra_fields", {}).update(v)
        else:
            data[k] = v
    return PlatformStats.from_dict(data)


def x_apply_override__mutmut_10(stats: PlatformStats | None, override: dict | None, platform: str) -> PlatformStats:
    """Build or patch a PlatformStats from a manual override dict."""
    if not override:
        return stats or PlatformStats(platform=platform)
    base = stats or PlatformStats(platform=platform)
    data = base.to_dict()
    for k, v in override.items():
        if k == "XXsubstatsXX" and isinstance(v, list):
            data["substats"] = v
        elif k == "extra_fields" and isinstance(v, dict):
            data.setdefault("extra_fields", {}).update(v)
        else:
            data[k] = v
    return PlatformStats.from_dict(data)


def x_apply_override__mutmut_11(stats: PlatformStats | None, override: dict | None, platform: str) -> PlatformStats:
    """Build or patch a PlatformStats from a manual override dict."""
    if not override:
        return stats or PlatformStats(platform=platform)
    base = stats or PlatformStats(platform=platform)
    data = base.to_dict()
    for k, v in override.items():
        if k == "SUBSTATS" and isinstance(v, list):
            data["substats"] = v
        elif k == "extra_fields" and isinstance(v, dict):
            data.setdefault("extra_fields", {}).update(v)
        else:
            data[k] = v
    return PlatformStats.from_dict(data)


def x_apply_override__mutmut_12(stats: PlatformStats | None, override: dict | None, platform: str) -> PlatformStats:
    """Build or patch a PlatformStats from a manual override dict."""
    if not override:
        return stats or PlatformStats(platform=platform)
    base = stats or PlatformStats(platform=platform)
    data = base.to_dict()
    for k, v in override.items():
        if k == "substats" and isinstance(v, list):
            data["substats"] = None
        elif k == "extra_fields" and isinstance(v, dict):
            data.setdefault("extra_fields", {}).update(v)
        else:
            data[k] = v
    return PlatformStats.from_dict(data)


def x_apply_override__mutmut_13(stats: PlatformStats | None, override: dict | None, platform: str) -> PlatformStats:
    """Build or patch a PlatformStats from a manual override dict."""
    if not override:
        return stats or PlatformStats(platform=platform)
    base = stats or PlatformStats(platform=platform)
    data = base.to_dict()
    for k, v in override.items():
        if k == "substats" and isinstance(v, list):
            data["XXsubstatsXX"] = v
        elif k == "extra_fields" and isinstance(v, dict):
            data.setdefault("extra_fields", {}).update(v)
        else:
            data[k] = v
    return PlatformStats.from_dict(data)


def x_apply_override__mutmut_14(stats: PlatformStats | None, override: dict | None, platform: str) -> PlatformStats:
    """Build or patch a PlatformStats from a manual override dict."""
    if not override:
        return stats or PlatformStats(platform=platform)
    base = stats or PlatformStats(platform=platform)
    data = base.to_dict()
    for k, v in override.items():
        if k == "substats" and isinstance(v, list):
            data["SUBSTATS"] = v
        elif k == "extra_fields" and isinstance(v, dict):
            data.setdefault("extra_fields", {}).update(v)
        else:
            data[k] = v
    return PlatformStats.from_dict(data)


def x_apply_override__mutmut_15(stats: PlatformStats | None, override: dict | None, platform: str) -> PlatformStats:
    """Build or patch a PlatformStats from a manual override dict."""
    if not override:
        return stats or PlatformStats(platform=platform)
    base = stats or PlatformStats(platform=platform)
    data = base.to_dict()
    for k, v in override.items():
        if k == "substats" and isinstance(v, list):
            data["substats"] = v
        elif k == "extra_fields" or isinstance(v, dict):
            data.setdefault("extra_fields", {}).update(v)
        else:
            data[k] = v
    return PlatformStats.from_dict(data)


def x_apply_override__mutmut_16(stats: PlatformStats | None, override: dict | None, platform: str) -> PlatformStats:
    """Build or patch a PlatformStats from a manual override dict."""
    if not override:
        return stats or PlatformStats(platform=platform)
    base = stats or PlatformStats(platform=platform)
    data = base.to_dict()
    for k, v in override.items():
        if k == "substats" and isinstance(v, list):
            data["substats"] = v
        elif k != "extra_fields" and isinstance(v, dict):
            data.setdefault("extra_fields", {}).update(v)
        else:
            data[k] = v
    return PlatformStats.from_dict(data)


def x_apply_override__mutmut_17(stats: PlatformStats | None, override: dict | None, platform: str) -> PlatformStats:
    """Build or patch a PlatformStats from a manual override dict."""
    if not override:
        return stats or PlatformStats(platform=platform)
    base = stats or PlatformStats(platform=platform)
    data = base.to_dict()
    for k, v in override.items():
        if k == "substats" and isinstance(v, list):
            data["substats"] = v
        elif k == "XXextra_fieldsXX" and isinstance(v, dict):
            data.setdefault("extra_fields", {}).update(v)
        else:
            data[k] = v
    return PlatformStats.from_dict(data)


def x_apply_override__mutmut_18(stats: PlatformStats | None, override: dict | None, platform: str) -> PlatformStats:
    """Build or patch a PlatformStats from a manual override dict."""
    if not override:
        return stats or PlatformStats(platform=platform)
    base = stats or PlatformStats(platform=platform)
    data = base.to_dict()
    for k, v in override.items():
        if k == "substats" and isinstance(v, list):
            data["substats"] = v
        elif k == "EXTRA_FIELDS" and isinstance(v, dict):
            data.setdefault("extra_fields", {}).update(v)
        else:
            data[k] = v
    return PlatformStats.from_dict(data)


def x_apply_override__mutmut_19(stats: PlatformStats | None, override: dict | None, platform: str) -> PlatformStats:
    """Build or patch a PlatformStats from a manual override dict."""
    if not override:
        return stats or PlatformStats(platform=platform)
    base = stats or PlatformStats(platform=platform)
    data = base.to_dict()
    for k, v in override.items():
        if k == "substats" and isinstance(v, list):
            data["substats"] = v
        elif k == "extra_fields" and isinstance(v, dict):
            data.setdefault("extra_fields", {}).update(None)
        else:
            data[k] = v
    return PlatformStats.from_dict(data)


def x_apply_override__mutmut_20(stats: PlatformStats | None, override: dict | None, platform: str) -> PlatformStats:
    """Build or patch a PlatformStats from a manual override dict."""
    if not override:
        return stats or PlatformStats(platform=platform)
    base = stats or PlatformStats(platform=platform)
    data = base.to_dict()
    for k, v in override.items():
        if k == "substats" and isinstance(v, list):
            data["substats"] = v
        elif k == "extra_fields" and isinstance(v, dict):
            data.setdefault(None, {}).update(v)
        else:
            data[k] = v
    return PlatformStats.from_dict(data)


def x_apply_override__mutmut_21(stats: PlatformStats | None, override: dict | None, platform: str) -> PlatformStats:
    """Build or patch a PlatformStats from a manual override dict."""
    if not override:
        return stats or PlatformStats(platform=platform)
    base = stats or PlatformStats(platform=platform)
    data = base.to_dict()
    for k, v in override.items():
        if k == "substats" and isinstance(v, list):
            data["substats"] = v
        elif k == "extra_fields" and isinstance(v, dict):
            data.setdefault("extra_fields", None).update(v)
        else:
            data[k] = v
    return PlatformStats.from_dict(data)


def x_apply_override__mutmut_22(stats: PlatformStats | None, override: dict | None, platform: str) -> PlatformStats:
    """Build or patch a PlatformStats from a manual override dict."""
    if not override:
        return stats or PlatformStats(platform=platform)
    base = stats or PlatformStats(platform=platform)
    data = base.to_dict()
    for k, v in override.items():
        if k == "substats" and isinstance(v, list):
            data["substats"] = v
        elif k == "extra_fields" and isinstance(v, dict):
            data.setdefault({}).update(v)
        else:
            data[k] = v
    return PlatformStats.from_dict(data)


def x_apply_override__mutmut_23(stats: PlatformStats | None, override: dict | None, platform: str) -> PlatformStats:
    """Build or patch a PlatformStats from a manual override dict."""
    if not override:
        return stats or PlatformStats(platform=platform)
    base = stats or PlatformStats(platform=platform)
    data = base.to_dict()
    for k, v in override.items():
        if k == "substats" and isinstance(v, list):
            data["substats"] = v
        elif k == "extra_fields" and isinstance(v, dict):
            data.setdefault("extra_fields", ).update(v)
        else:
            data[k] = v
    return PlatformStats.from_dict(data)


def x_apply_override__mutmut_24(stats: PlatformStats | None, override: dict | None, platform: str) -> PlatformStats:
    """Build or patch a PlatformStats from a manual override dict."""
    if not override:
        return stats or PlatformStats(platform=platform)
    base = stats or PlatformStats(platform=platform)
    data = base.to_dict()
    for k, v in override.items():
        if k == "substats" and isinstance(v, list):
            data["substats"] = v
        elif k == "extra_fields" and isinstance(v, dict):
            data.setdefault("XXextra_fieldsXX", {}).update(v)
        else:
            data[k] = v
    return PlatformStats.from_dict(data)


def x_apply_override__mutmut_25(stats: PlatformStats | None, override: dict | None, platform: str) -> PlatformStats:
    """Build or patch a PlatformStats from a manual override dict."""
    if not override:
        return stats or PlatformStats(platform=platform)
    base = stats or PlatformStats(platform=platform)
    data = base.to_dict()
    for k, v in override.items():
        if k == "substats" and isinstance(v, list):
            data["substats"] = v
        elif k == "extra_fields" and isinstance(v, dict):
            data.setdefault("EXTRA_FIELDS", {}).update(v)
        else:
            data[k] = v
    return PlatformStats.from_dict(data)


def x_apply_override__mutmut_26(stats: PlatformStats | None, override: dict | None, platform: str) -> PlatformStats:
    """Build or patch a PlatformStats from a manual override dict."""
    if not override:
        return stats or PlatformStats(platform=platform)
    base = stats or PlatformStats(platform=platform)
    data = base.to_dict()
    for k, v in override.items():
        if k == "substats" and isinstance(v, list):
            data["substats"] = v
        elif k == "extra_fields" and isinstance(v, dict):
            data.setdefault("extra_fields", {}).update(v)
        else:
            data[k] = None
    return PlatformStats.from_dict(data)


def x_apply_override__mutmut_27(stats: PlatformStats | None, override: dict | None, platform: str) -> PlatformStats:
    """Build or patch a PlatformStats from a manual override dict."""
    if not override:
        return stats or PlatformStats(platform=platform)
    base = stats or PlatformStats(platform=platform)
    data = base.to_dict()
    for k, v in override.items():
        if k == "substats" and isinstance(v, list):
            data["substats"] = v
        elif k == "extra_fields" and isinstance(v, dict):
            data.setdefault("extra_fields", {}).update(v)
        else:
            data[k] = v
    return PlatformStats.from_dict(None)

x_apply_override__mutmut_mutants : ClassVar[MutantDict] = {
'x_apply_override__mutmut_1': x_apply_override__mutmut_1, 
    'x_apply_override__mutmut_2': x_apply_override__mutmut_2, 
    'x_apply_override__mutmut_3': x_apply_override__mutmut_3, 
    'x_apply_override__mutmut_4': x_apply_override__mutmut_4, 
    'x_apply_override__mutmut_5': x_apply_override__mutmut_5, 
    'x_apply_override__mutmut_6': x_apply_override__mutmut_6, 
    'x_apply_override__mutmut_7': x_apply_override__mutmut_7, 
    'x_apply_override__mutmut_8': x_apply_override__mutmut_8, 
    'x_apply_override__mutmut_9': x_apply_override__mutmut_9, 
    'x_apply_override__mutmut_10': x_apply_override__mutmut_10, 
    'x_apply_override__mutmut_11': x_apply_override__mutmut_11, 
    'x_apply_override__mutmut_12': x_apply_override__mutmut_12, 
    'x_apply_override__mutmut_13': x_apply_override__mutmut_13, 
    'x_apply_override__mutmut_14': x_apply_override__mutmut_14, 
    'x_apply_override__mutmut_15': x_apply_override__mutmut_15, 
    'x_apply_override__mutmut_16': x_apply_override__mutmut_16, 
    'x_apply_override__mutmut_17': x_apply_override__mutmut_17, 
    'x_apply_override__mutmut_18': x_apply_override__mutmut_18, 
    'x_apply_override__mutmut_19': x_apply_override__mutmut_19, 
    'x_apply_override__mutmut_20': x_apply_override__mutmut_20, 
    'x_apply_override__mutmut_21': x_apply_override__mutmut_21, 
    'x_apply_override__mutmut_22': x_apply_override__mutmut_22, 
    'x_apply_override__mutmut_23': x_apply_override__mutmut_23, 
    'x_apply_override__mutmut_24': x_apply_override__mutmut_24, 
    'x_apply_override__mutmut_25': x_apply_override__mutmut_25, 
    'x_apply_override__mutmut_26': x_apply_override__mutmut_26, 
    'x_apply_override__mutmut_27': x_apply_override__mutmut_27
}

def apply_override(*args, **kwargs):
    result = _mutmut_trampoline(x_apply_override__mutmut_orig, x_apply_override__mutmut_mutants, args, kwargs)
    return result 

apply_override.__signature__ = _mutmut_signature(x_apply_override__mutmut_orig)
x_apply_override__mutmut_orig.__name__ = 'x_apply_override'


def x_placeholder__mutmut_orig(platform: str) -> PlatformStats:
    """Last-resort stats so rendering never crashes."""
    defaults = {
        "xbox": PlatformStats(
            platform="xbox",
            username="Gamer",
            headline_value=0,
            headline_label="Gamerscore",
            substats=[SubStat("TA", 0)],
        ),
        "psn": PlatformStats(
            platform="psn",
            username="Player",
            headline_value="0 Platinums",
            headline_label="Trophies",
            substats=[
                SubStat("platinum", 0),
                SubStat("gold", 0),
                SubStat("silver", 0),
                SubStat("bronze", 0),
            ],
        ),
        "retroachievements": PlatformStats(
            platform="retroachievements",
            username="RetroUser",
            headline_value=0,
            headline_label="Hardcore Points",
            substats=[
                SubStat("RR", 0.0),
                SubStat("B", 0),
                SubStat("M", 0),
            ],
            extra_fields={
                "BeatenHardcoreAwardsCount": 0,
                "CompletionAwardsCount": 0,
                "MasteryAwardsCount": 0,
            },
        ),
    }
    return defaults.get(platform, PlatformStats(platform=platform))


def x_placeholder__mutmut_1(platform: str) -> PlatformStats:
    """Last-resort stats so rendering never crashes."""
    defaults = None
    return defaults.get(platform, PlatformStats(platform=platform))


def x_placeholder__mutmut_2(platform: str) -> PlatformStats:
    """Last-resort stats so rendering never crashes."""
    defaults = {
        "XXxboxXX": PlatformStats(
            platform="xbox",
            username="Gamer",
            headline_value=0,
            headline_label="Gamerscore",
            substats=[SubStat("TA", 0)],
        ),
        "psn": PlatformStats(
            platform="psn",
            username="Player",
            headline_value="0 Platinums",
            headline_label="Trophies",
            substats=[
                SubStat("platinum", 0),
                SubStat("gold", 0),
                SubStat("silver", 0),
                SubStat("bronze", 0),
            ],
        ),
        "retroachievements": PlatformStats(
            platform="retroachievements",
            username="RetroUser",
            headline_value=0,
            headline_label="Hardcore Points",
            substats=[
                SubStat("RR", 0.0),
                SubStat("B", 0),
                SubStat("M", 0),
            ],
            extra_fields={
                "BeatenHardcoreAwardsCount": 0,
                "CompletionAwardsCount": 0,
                "MasteryAwardsCount": 0,
            },
        ),
    }
    return defaults.get(platform, PlatformStats(platform=platform))


def x_placeholder__mutmut_3(platform: str) -> PlatformStats:
    """Last-resort stats so rendering never crashes."""
    defaults = {
        "XBOX": PlatformStats(
            platform="xbox",
            username="Gamer",
            headline_value=0,
            headline_label="Gamerscore",
            substats=[SubStat("TA", 0)],
        ),
        "psn": PlatformStats(
            platform="psn",
            username="Player",
            headline_value="0 Platinums",
            headline_label="Trophies",
            substats=[
                SubStat("platinum", 0),
                SubStat("gold", 0),
                SubStat("silver", 0),
                SubStat("bronze", 0),
            ],
        ),
        "retroachievements": PlatformStats(
            platform="retroachievements",
            username="RetroUser",
            headline_value=0,
            headline_label="Hardcore Points",
            substats=[
                SubStat("RR", 0.0),
                SubStat("B", 0),
                SubStat("M", 0),
            ],
            extra_fields={
                "BeatenHardcoreAwardsCount": 0,
                "CompletionAwardsCount": 0,
                "MasteryAwardsCount": 0,
            },
        ),
    }
    return defaults.get(platform, PlatformStats(platform=platform))


def x_placeholder__mutmut_4(platform: str) -> PlatformStats:
    """Last-resort stats so rendering never crashes."""
    defaults = {
        "xbox": PlatformStats(
            platform=None,
            username="Gamer",
            headline_value=0,
            headline_label="Gamerscore",
            substats=[SubStat("TA", 0)],
        ),
        "psn": PlatformStats(
            platform="psn",
            username="Player",
            headline_value="0 Platinums",
            headline_label="Trophies",
            substats=[
                SubStat("platinum", 0),
                SubStat("gold", 0),
                SubStat("silver", 0),
                SubStat("bronze", 0),
            ],
        ),
        "retroachievements": PlatformStats(
            platform="retroachievements",
            username="RetroUser",
            headline_value=0,
            headline_label="Hardcore Points",
            substats=[
                SubStat("RR", 0.0),
                SubStat("B", 0),
                SubStat("M", 0),
            ],
            extra_fields={
                "BeatenHardcoreAwardsCount": 0,
                "CompletionAwardsCount": 0,
                "MasteryAwardsCount": 0,
            },
        ),
    }
    return defaults.get(platform, PlatformStats(platform=platform))


def x_placeholder__mutmut_5(platform: str) -> PlatformStats:
    """Last-resort stats so rendering never crashes."""
    defaults = {
        "xbox": PlatformStats(
            platform="xbox",
            username=None,
            headline_value=0,
            headline_label="Gamerscore",
            substats=[SubStat("TA", 0)],
        ),
        "psn": PlatformStats(
            platform="psn",
            username="Player",
            headline_value="0 Platinums",
            headline_label="Trophies",
            substats=[
                SubStat("platinum", 0),
                SubStat("gold", 0),
                SubStat("silver", 0),
                SubStat("bronze", 0),
            ],
        ),
        "retroachievements": PlatformStats(
            platform="retroachievements",
            username="RetroUser",
            headline_value=0,
            headline_label="Hardcore Points",
            substats=[
                SubStat("RR", 0.0),
                SubStat("B", 0),
                SubStat("M", 0),
            ],
            extra_fields={
                "BeatenHardcoreAwardsCount": 0,
                "CompletionAwardsCount": 0,
                "MasteryAwardsCount": 0,
            },
        ),
    }
    return defaults.get(platform, PlatformStats(platform=platform))


def x_placeholder__mutmut_6(platform: str) -> PlatformStats:
    """Last-resort stats so rendering never crashes."""
    defaults = {
        "xbox": PlatformStats(
            platform="xbox",
            username="Gamer",
            headline_value=None,
            headline_label="Gamerscore",
            substats=[SubStat("TA", 0)],
        ),
        "psn": PlatformStats(
            platform="psn",
            username="Player",
            headline_value="0 Platinums",
            headline_label="Trophies",
            substats=[
                SubStat("platinum", 0),
                SubStat("gold", 0),
                SubStat("silver", 0),
                SubStat("bronze", 0),
            ],
        ),
        "retroachievements": PlatformStats(
            platform="retroachievements",
            username="RetroUser",
            headline_value=0,
            headline_label="Hardcore Points",
            substats=[
                SubStat("RR", 0.0),
                SubStat("B", 0),
                SubStat("M", 0),
            ],
            extra_fields={
                "BeatenHardcoreAwardsCount": 0,
                "CompletionAwardsCount": 0,
                "MasteryAwardsCount": 0,
            },
        ),
    }
    return defaults.get(platform, PlatformStats(platform=platform))


def x_placeholder__mutmut_7(platform: str) -> PlatformStats:
    """Last-resort stats so rendering never crashes."""
    defaults = {
        "xbox": PlatformStats(
            platform="xbox",
            username="Gamer",
            headline_value=0,
            headline_label=None,
            substats=[SubStat("TA", 0)],
        ),
        "psn": PlatformStats(
            platform="psn",
            username="Player",
            headline_value="0 Platinums",
            headline_label="Trophies",
            substats=[
                SubStat("platinum", 0),
                SubStat("gold", 0),
                SubStat("silver", 0),
                SubStat("bronze", 0),
            ],
        ),
        "retroachievements": PlatformStats(
            platform="retroachievements",
            username="RetroUser",
            headline_value=0,
            headline_label="Hardcore Points",
            substats=[
                SubStat("RR", 0.0),
                SubStat("B", 0),
                SubStat("M", 0),
            ],
            extra_fields={
                "BeatenHardcoreAwardsCount": 0,
                "CompletionAwardsCount": 0,
                "MasteryAwardsCount": 0,
            },
        ),
    }
    return defaults.get(platform, PlatformStats(platform=platform))


def x_placeholder__mutmut_8(platform: str) -> PlatformStats:
    """Last-resort stats so rendering never crashes."""
    defaults = {
        "xbox": PlatformStats(
            platform="xbox",
            username="Gamer",
            headline_value=0,
            headline_label="Gamerscore",
            substats=None,
        ),
        "psn": PlatformStats(
            platform="psn",
            username="Player",
            headline_value="0 Platinums",
            headline_label="Trophies",
            substats=[
                SubStat("platinum", 0),
                SubStat("gold", 0),
                SubStat("silver", 0),
                SubStat("bronze", 0),
            ],
        ),
        "retroachievements": PlatformStats(
            platform="retroachievements",
            username="RetroUser",
            headline_value=0,
            headline_label="Hardcore Points",
            substats=[
                SubStat("RR", 0.0),
                SubStat("B", 0),
                SubStat("M", 0),
            ],
            extra_fields={
                "BeatenHardcoreAwardsCount": 0,
                "CompletionAwardsCount": 0,
                "MasteryAwardsCount": 0,
            },
        ),
    }
    return defaults.get(platform, PlatformStats(platform=platform))


def x_placeholder__mutmut_9(platform: str) -> PlatformStats:
    """Last-resort stats so rendering never crashes."""
    defaults = {
        "xbox": PlatformStats(
            username="Gamer",
            headline_value=0,
            headline_label="Gamerscore",
            substats=[SubStat("TA", 0)],
        ),
        "psn": PlatformStats(
            platform="psn",
            username="Player",
            headline_value="0 Platinums",
            headline_label="Trophies",
            substats=[
                SubStat("platinum", 0),
                SubStat("gold", 0),
                SubStat("silver", 0),
                SubStat("bronze", 0),
            ],
        ),
        "retroachievements": PlatformStats(
            platform="retroachievements",
            username="RetroUser",
            headline_value=0,
            headline_label="Hardcore Points",
            substats=[
                SubStat("RR", 0.0),
                SubStat("B", 0),
                SubStat("M", 0),
            ],
            extra_fields={
                "BeatenHardcoreAwardsCount": 0,
                "CompletionAwardsCount": 0,
                "MasteryAwardsCount": 0,
            },
        ),
    }
    return defaults.get(platform, PlatformStats(platform=platform))


def x_placeholder__mutmut_10(platform: str) -> PlatformStats:
    """Last-resort stats so rendering never crashes."""
    defaults = {
        "xbox": PlatformStats(
            platform="xbox",
            headline_value=0,
            headline_label="Gamerscore",
            substats=[SubStat("TA", 0)],
        ),
        "psn": PlatformStats(
            platform="psn",
            username="Player",
            headline_value="0 Platinums",
            headline_label="Trophies",
            substats=[
                SubStat("platinum", 0),
                SubStat("gold", 0),
                SubStat("silver", 0),
                SubStat("bronze", 0),
            ],
        ),
        "retroachievements": PlatformStats(
            platform="retroachievements",
            username="RetroUser",
            headline_value=0,
            headline_label="Hardcore Points",
            substats=[
                SubStat("RR", 0.0),
                SubStat("B", 0),
                SubStat("M", 0),
            ],
            extra_fields={
                "BeatenHardcoreAwardsCount": 0,
                "CompletionAwardsCount": 0,
                "MasteryAwardsCount": 0,
            },
        ),
    }
    return defaults.get(platform, PlatformStats(platform=platform))


def x_placeholder__mutmut_11(platform: str) -> PlatformStats:
    """Last-resort stats so rendering never crashes."""
    defaults = {
        "xbox": PlatformStats(
            platform="xbox",
            username="Gamer",
            headline_label="Gamerscore",
            substats=[SubStat("TA", 0)],
        ),
        "psn": PlatformStats(
            platform="psn",
            username="Player",
            headline_value="0 Platinums",
            headline_label="Trophies",
            substats=[
                SubStat("platinum", 0),
                SubStat("gold", 0),
                SubStat("silver", 0),
                SubStat("bronze", 0),
            ],
        ),
        "retroachievements": PlatformStats(
            platform="retroachievements",
            username="RetroUser",
            headline_value=0,
            headline_label="Hardcore Points",
            substats=[
                SubStat("RR", 0.0),
                SubStat("B", 0),
                SubStat("M", 0),
            ],
            extra_fields={
                "BeatenHardcoreAwardsCount": 0,
                "CompletionAwardsCount": 0,
                "MasteryAwardsCount": 0,
            },
        ),
    }
    return defaults.get(platform, PlatformStats(platform=platform))


def x_placeholder__mutmut_12(platform: str) -> PlatformStats:
    """Last-resort stats so rendering never crashes."""
    defaults = {
        "xbox": PlatformStats(
            platform="xbox",
            username="Gamer",
            headline_value=0,
            substats=[SubStat("TA", 0)],
        ),
        "psn": PlatformStats(
            platform="psn",
            username="Player",
            headline_value="0 Platinums",
            headline_label="Trophies",
            substats=[
                SubStat("platinum", 0),
                SubStat("gold", 0),
                SubStat("silver", 0),
                SubStat("bronze", 0),
            ],
        ),
        "retroachievements": PlatformStats(
            platform="retroachievements",
            username="RetroUser",
            headline_value=0,
            headline_label="Hardcore Points",
            substats=[
                SubStat("RR", 0.0),
                SubStat("B", 0),
                SubStat("M", 0),
            ],
            extra_fields={
                "BeatenHardcoreAwardsCount": 0,
                "CompletionAwardsCount": 0,
                "MasteryAwardsCount": 0,
            },
        ),
    }
    return defaults.get(platform, PlatformStats(platform=platform))


def x_placeholder__mutmut_13(platform: str) -> PlatformStats:
    """Last-resort stats so rendering never crashes."""
    defaults = {
        "xbox": PlatformStats(
            platform="xbox",
            username="Gamer",
            headline_value=0,
            headline_label="Gamerscore",
            ),
        "psn": PlatformStats(
            platform="psn",
            username="Player",
            headline_value="0 Platinums",
            headline_label="Trophies",
            substats=[
                SubStat("platinum", 0),
                SubStat("gold", 0),
                SubStat("silver", 0),
                SubStat("bronze", 0),
            ],
        ),
        "retroachievements": PlatformStats(
            platform="retroachievements",
            username="RetroUser",
            headline_value=0,
            headline_label="Hardcore Points",
            substats=[
                SubStat("RR", 0.0),
                SubStat("B", 0),
                SubStat("M", 0),
            ],
            extra_fields={
                "BeatenHardcoreAwardsCount": 0,
                "CompletionAwardsCount": 0,
                "MasteryAwardsCount": 0,
            },
        ),
    }
    return defaults.get(platform, PlatformStats(platform=platform))


def x_placeholder__mutmut_14(platform: str) -> PlatformStats:
    """Last-resort stats so rendering never crashes."""
    defaults = {
        "xbox": PlatformStats(
            platform="XXxboxXX",
            username="Gamer",
            headline_value=0,
            headline_label="Gamerscore",
            substats=[SubStat("TA", 0)],
        ),
        "psn": PlatformStats(
            platform="psn",
            username="Player",
            headline_value="0 Platinums",
            headline_label="Trophies",
            substats=[
                SubStat("platinum", 0),
                SubStat("gold", 0),
                SubStat("silver", 0),
                SubStat("bronze", 0),
            ],
        ),
        "retroachievements": PlatformStats(
            platform="retroachievements",
            username="RetroUser",
            headline_value=0,
            headline_label="Hardcore Points",
            substats=[
                SubStat("RR", 0.0),
                SubStat("B", 0),
                SubStat("M", 0),
            ],
            extra_fields={
                "BeatenHardcoreAwardsCount": 0,
                "CompletionAwardsCount": 0,
                "MasteryAwardsCount": 0,
            },
        ),
    }
    return defaults.get(platform, PlatformStats(platform=platform))


def x_placeholder__mutmut_15(platform: str) -> PlatformStats:
    """Last-resort stats so rendering never crashes."""
    defaults = {
        "xbox": PlatformStats(
            platform="XBOX",
            username="Gamer",
            headline_value=0,
            headline_label="Gamerscore",
            substats=[SubStat("TA", 0)],
        ),
        "psn": PlatformStats(
            platform="psn",
            username="Player",
            headline_value="0 Platinums",
            headline_label="Trophies",
            substats=[
                SubStat("platinum", 0),
                SubStat("gold", 0),
                SubStat("silver", 0),
                SubStat("bronze", 0),
            ],
        ),
        "retroachievements": PlatformStats(
            platform="retroachievements",
            username="RetroUser",
            headline_value=0,
            headline_label="Hardcore Points",
            substats=[
                SubStat("RR", 0.0),
                SubStat("B", 0),
                SubStat("M", 0),
            ],
            extra_fields={
                "BeatenHardcoreAwardsCount": 0,
                "CompletionAwardsCount": 0,
                "MasteryAwardsCount": 0,
            },
        ),
    }
    return defaults.get(platform, PlatformStats(platform=platform))


def x_placeholder__mutmut_16(platform: str) -> PlatformStats:
    """Last-resort stats so rendering never crashes."""
    defaults = {
        "xbox": PlatformStats(
            platform="xbox",
            username="XXGamerXX",
            headline_value=0,
            headline_label="Gamerscore",
            substats=[SubStat("TA", 0)],
        ),
        "psn": PlatformStats(
            platform="psn",
            username="Player",
            headline_value="0 Platinums",
            headline_label="Trophies",
            substats=[
                SubStat("platinum", 0),
                SubStat("gold", 0),
                SubStat("silver", 0),
                SubStat("bronze", 0),
            ],
        ),
        "retroachievements": PlatformStats(
            platform="retroachievements",
            username="RetroUser",
            headline_value=0,
            headline_label="Hardcore Points",
            substats=[
                SubStat("RR", 0.0),
                SubStat("B", 0),
                SubStat("M", 0),
            ],
            extra_fields={
                "BeatenHardcoreAwardsCount": 0,
                "CompletionAwardsCount": 0,
                "MasteryAwardsCount": 0,
            },
        ),
    }
    return defaults.get(platform, PlatformStats(platform=platform))


def x_placeholder__mutmut_17(platform: str) -> PlatformStats:
    """Last-resort stats so rendering never crashes."""
    defaults = {
        "xbox": PlatformStats(
            platform="xbox",
            username="gamer",
            headline_value=0,
            headline_label="Gamerscore",
            substats=[SubStat("TA", 0)],
        ),
        "psn": PlatformStats(
            platform="psn",
            username="Player",
            headline_value="0 Platinums",
            headline_label="Trophies",
            substats=[
                SubStat("platinum", 0),
                SubStat("gold", 0),
                SubStat("silver", 0),
                SubStat("bronze", 0),
            ],
        ),
        "retroachievements": PlatformStats(
            platform="retroachievements",
            username="RetroUser",
            headline_value=0,
            headline_label="Hardcore Points",
            substats=[
                SubStat("RR", 0.0),
                SubStat("B", 0),
                SubStat("M", 0),
            ],
            extra_fields={
                "BeatenHardcoreAwardsCount": 0,
                "CompletionAwardsCount": 0,
                "MasteryAwardsCount": 0,
            },
        ),
    }
    return defaults.get(platform, PlatformStats(platform=platform))


def x_placeholder__mutmut_18(platform: str) -> PlatformStats:
    """Last-resort stats so rendering never crashes."""
    defaults = {
        "xbox": PlatformStats(
            platform="xbox",
            username="GAMER",
            headline_value=0,
            headline_label="Gamerscore",
            substats=[SubStat("TA", 0)],
        ),
        "psn": PlatformStats(
            platform="psn",
            username="Player",
            headline_value="0 Platinums",
            headline_label="Trophies",
            substats=[
                SubStat("platinum", 0),
                SubStat("gold", 0),
                SubStat("silver", 0),
                SubStat("bronze", 0),
            ],
        ),
        "retroachievements": PlatformStats(
            platform="retroachievements",
            username="RetroUser",
            headline_value=0,
            headline_label="Hardcore Points",
            substats=[
                SubStat("RR", 0.0),
                SubStat("B", 0),
                SubStat("M", 0),
            ],
            extra_fields={
                "BeatenHardcoreAwardsCount": 0,
                "CompletionAwardsCount": 0,
                "MasteryAwardsCount": 0,
            },
        ),
    }
    return defaults.get(platform, PlatformStats(platform=platform))


def x_placeholder__mutmut_19(platform: str) -> PlatformStats:
    """Last-resort stats so rendering never crashes."""
    defaults = {
        "xbox": PlatformStats(
            platform="xbox",
            username="Gamer",
            headline_value=1,
            headline_label="Gamerscore",
            substats=[SubStat("TA", 0)],
        ),
        "psn": PlatformStats(
            platform="psn",
            username="Player",
            headline_value="0 Platinums",
            headline_label="Trophies",
            substats=[
                SubStat("platinum", 0),
                SubStat("gold", 0),
                SubStat("silver", 0),
                SubStat("bronze", 0),
            ],
        ),
        "retroachievements": PlatformStats(
            platform="retroachievements",
            username="RetroUser",
            headline_value=0,
            headline_label="Hardcore Points",
            substats=[
                SubStat("RR", 0.0),
                SubStat("B", 0),
                SubStat("M", 0),
            ],
            extra_fields={
                "BeatenHardcoreAwardsCount": 0,
                "CompletionAwardsCount": 0,
                "MasteryAwardsCount": 0,
            },
        ),
    }
    return defaults.get(platform, PlatformStats(platform=platform))


def x_placeholder__mutmut_20(platform: str) -> PlatformStats:
    """Last-resort stats so rendering never crashes."""
    defaults = {
        "xbox": PlatformStats(
            platform="xbox",
            username="Gamer",
            headline_value=0,
            headline_label="XXGamerscoreXX",
            substats=[SubStat("TA", 0)],
        ),
        "psn": PlatformStats(
            platform="psn",
            username="Player",
            headline_value="0 Platinums",
            headline_label="Trophies",
            substats=[
                SubStat("platinum", 0),
                SubStat("gold", 0),
                SubStat("silver", 0),
                SubStat("bronze", 0),
            ],
        ),
        "retroachievements": PlatformStats(
            platform="retroachievements",
            username="RetroUser",
            headline_value=0,
            headline_label="Hardcore Points",
            substats=[
                SubStat("RR", 0.0),
                SubStat("B", 0),
                SubStat("M", 0),
            ],
            extra_fields={
                "BeatenHardcoreAwardsCount": 0,
                "CompletionAwardsCount": 0,
                "MasteryAwardsCount": 0,
            },
        ),
    }
    return defaults.get(platform, PlatformStats(platform=platform))


def x_placeholder__mutmut_21(platform: str) -> PlatformStats:
    """Last-resort stats so rendering never crashes."""
    defaults = {
        "xbox": PlatformStats(
            platform="xbox",
            username="Gamer",
            headline_value=0,
            headline_label="gamerscore",
            substats=[SubStat("TA", 0)],
        ),
        "psn": PlatformStats(
            platform="psn",
            username="Player",
            headline_value="0 Platinums",
            headline_label="Trophies",
            substats=[
                SubStat("platinum", 0),
                SubStat("gold", 0),
                SubStat("silver", 0),
                SubStat("bronze", 0),
            ],
        ),
        "retroachievements": PlatformStats(
            platform="retroachievements",
            username="RetroUser",
            headline_value=0,
            headline_label="Hardcore Points",
            substats=[
                SubStat("RR", 0.0),
                SubStat("B", 0),
                SubStat("M", 0),
            ],
            extra_fields={
                "BeatenHardcoreAwardsCount": 0,
                "CompletionAwardsCount": 0,
                "MasteryAwardsCount": 0,
            },
        ),
    }
    return defaults.get(platform, PlatformStats(platform=platform))


def x_placeholder__mutmut_22(platform: str) -> PlatformStats:
    """Last-resort stats so rendering never crashes."""
    defaults = {
        "xbox": PlatformStats(
            platform="xbox",
            username="Gamer",
            headline_value=0,
            headline_label="GAMERSCORE",
            substats=[SubStat("TA", 0)],
        ),
        "psn": PlatformStats(
            platform="psn",
            username="Player",
            headline_value="0 Platinums",
            headline_label="Trophies",
            substats=[
                SubStat("platinum", 0),
                SubStat("gold", 0),
                SubStat("silver", 0),
                SubStat("bronze", 0),
            ],
        ),
        "retroachievements": PlatformStats(
            platform="retroachievements",
            username="RetroUser",
            headline_value=0,
            headline_label="Hardcore Points",
            substats=[
                SubStat("RR", 0.0),
                SubStat("B", 0),
                SubStat("M", 0),
            ],
            extra_fields={
                "BeatenHardcoreAwardsCount": 0,
                "CompletionAwardsCount": 0,
                "MasteryAwardsCount": 0,
            },
        ),
    }
    return defaults.get(platform, PlatformStats(platform=platform))


def x_placeholder__mutmut_23(platform: str) -> PlatformStats:
    """Last-resort stats so rendering never crashes."""
    defaults = {
        "xbox": PlatformStats(
            platform="xbox",
            username="Gamer",
            headline_value=0,
            headline_label="Gamerscore",
            substats=[SubStat(None, 0)],
        ),
        "psn": PlatformStats(
            platform="psn",
            username="Player",
            headline_value="0 Platinums",
            headline_label="Trophies",
            substats=[
                SubStat("platinum", 0),
                SubStat("gold", 0),
                SubStat("silver", 0),
                SubStat("bronze", 0),
            ],
        ),
        "retroachievements": PlatformStats(
            platform="retroachievements",
            username="RetroUser",
            headline_value=0,
            headline_label="Hardcore Points",
            substats=[
                SubStat("RR", 0.0),
                SubStat("B", 0),
                SubStat("M", 0),
            ],
            extra_fields={
                "BeatenHardcoreAwardsCount": 0,
                "CompletionAwardsCount": 0,
                "MasteryAwardsCount": 0,
            },
        ),
    }
    return defaults.get(platform, PlatformStats(platform=platform))


def x_placeholder__mutmut_24(platform: str) -> PlatformStats:
    """Last-resort stats so rendering never crashes."""
    defaults = {
        "xbox": PlatformStats(
            platform="xbox",
            username="Gamer",
            headline_value=0,
            headline_label="Gamerscore",
            substats=[SubStat("TA", None)],
        ),
        "psn": PlatformStats(
            platform="psn",
            username="Player",
            headline_value="0 Platinums",
            headline_label="Trophies",
            substats=[
                SubStat("platinum", 0),
                SubStat("gold", 0),
                SubStat("silver", 0),
                SubStat("bronze", 0),
            ],
        ),
        "retroachievements": PlatformStats(
            platform="retroachievements",
            username="RetroUser",
            headline_value=0,
            headline_label="Hardcore Points",
            substats=[
                SubStat("RR", 0.0),
                SubStat("B", 0),
                SubStat("M", 0),
            ],
            extra_fields={
                "BeatenHardcoreAwardsCount": 0,
                "CompletionAwardsCount": 0,
                "MasteryAwardsCount": 0,
            },
        ),
    }
    return defaults.get(platform, PlatformStats(platform=platform))


def x_placeholder__mutmut_25(platform: str) -> PlatformStats:
    """Last-resort stats so rendering never crashes."""
    defaults = {
        "xbox": PlatformStats(
            platform="xbox",
            username="Gamer",
            headline_value=0,
            headline_label="Gamerscore",
            substats=[SubStat(0)],
        ),
        "psn": PlatformStats(
            platform="psn",
            username="Player",
            headline_value="0 Platinums",
            headline_label="Trophies",
            substats=[
                SubStat("platinum", 0),
                SubStat("gold", 0),
                SubStat("silver", 0),
                SubStat("bronze", 0),
            ],
        ),
        "retroachievements": PlatformStats(
            platform="retroachievements",
            username="RetroUser",
            headline_value=0,
            headline_label="Hardcore Points",
            substats=[
                SubStat("RR", 0.0),
                SubStat("B", 0),
                SubStat("M", 0),
            ],
            extra_fields={
                "BeatenHardcoreAwardsCount": 0,
                "CompletionAwardsCount": 0,
                "MasteryAwardsCount": 0,
            },
        ),
    }
    return defaults.get(platform, PlatformStats(platform=platform))


def x_placeholder__mutmut_26(platform: str) -> PlatformStats:
    """Last-resort stats so rendering never crashes."""
    defaults = {
        "xbox": PlatformStats(
            platform="xbox",
            username="Gamer",
            headline_value=0,
            headline_label="Gamerscore",
            substats=[SubStat("TA", )],
        ),
        "psn": PlatformStats(
            platform="psn",
            username="Player",
            headline_value="0 Platinums",
            headline_label="Trophies",
            substats=[
                SubStat("platinum", 0),
                SubStat("gold", 0),
                SubStat("silver", 0),
                SubStat("bronze", 0),
            ],
        ),
        "retroachievements": PlatformStats(
            platform="retroachievements",
            username="RetroUser",
            headline_value=0,
            headline_label="Hardcore Points",
            substats=[
                SubStat("RR", 0.0),
                SubStat("B", 0),
                SubStat("M", 0),
            ],
            extra_fields={
                "BeatenHardcoreAwardsCount": 0,
                "CompletionAwardsCount": 0,
                "MasteryAwardsCount": 0,
            },
        ),
    }
    return defaults.get(platform, PlatformStats(platform=platform))


def x_placeholder__mutmut_27(platform: str) -> PlatformStats:
    """Last-resort stats so rendering never crashes."""
    defaults = {
        "xbox": PlatformStats(
            platform="xbox",
            username="Gamer",
            headline_value=0,
            headline_label="Gamerscore",
            substats=[SubStat("XXTAXX", 0)],
        ),
        "psn": PlatformStats(
            platform="psn",
            username="Player",
            headline_value="0 Platinums",
            headline_label="Trophies",
            substats=[
                SubStat("platinum", 0),
                SubStat("gold", 0),
                SubStat("silver", 0),
                SubStat("bronze", 0),
            ],
        ),
        "retroachievements": PlatformStats(
            platform="retroachievements",
            username="RetroUser",
            headline_value=0,
            headline_label="Hardcore Points",
            substats=[
                SubStat("RR", 0.0),
                SubStat("B", 0),
                SubStat("M", 0),
            ],
            extra_fields={
                "BeatenHardcoreAwardsCount": 0,
                "CompletionAwardsCount": 0,
                "MasteryAwardsCount": 0,
            },
        ),
    }
    return defaults.get(platform, PlatformStats(platform=platform))


def x_placeholder__mutmut_28(platform: str) -> PlatformStats:
    """Last-resort stats so rendering never crashes."""
    defaults = {
        "xbox": PlatformStats(
            platform="xbox",
            username="Gamer",
            headline_value=0,
            headline_label="Gamerscore",
            substats=[SubStat("ta", 0)],
        ),
        "psn": PlatformStats(
            platform="psn",
            username="Player",
            headline_value="0 Platinums",
            headline_label="Trophies",
            substats=[
                SubStat("platinum", 0),
                SubStat("gold", 0),
                SubStat("silver", 0),
                SubStat("bronze", 0),
            ],
        ),
        "retroachievements": PlatformStats(
            platform="retroachievements",
            username="RetroUser",
            headline_value=0,
            headline_label="Hardcore Points",
            substats=[
                SubStat("RR", 0.0),
                SubStat("B", 0),
                SubStat("M", 0),
            ],
            extra_fields={
                "BeatenHardcoreAwardsCount": 0,
                "CompletionAwardsCount": 0,
                "MasteryAwardsCount": 0,
            },
        ),
    }
    return defaults.get(platform, PlatformStats(platform=platform))


def x_placeholder__mutmut_29(platform: str) -> PlatformStats:
    """Last-resort stats so rendering never crashes."""
    defaults = {
        "xbox": PlatformStats(
            platform="xbox",
            username="Gamer",
            headline_value=0,
            headline_label="Gamerscore",
            substats=[SubStat("TA", 1)],
        ),
        "psn": PlatformStats(
            platform="psn",
            username="Player",
            headline_value="0 Platinums",
            headline_label="Trophies",
            substats=[
                SubStat("platinum", 0),
                SubStat("gold", 0),
                SubStat("silver", 0),
                SubStat("bronze", 0),
            ],
        ),
        "retroachievements": PlatformStats(
            platform="retroachievements",
            username="RetroUser",
            headline_value=0,
            headline_label="Hardcore Points",
            substats=[
                SubStat("RR", 0.0),
                SubStat("B", 0),
                SubStat("M", 0),
            ],
            extra_fields={
                "BeatenHardcoreAwardsCount": 0,
                "CompletionAwardsCount": 0,
                "MasteryAwardsCount": 0,
            },
        ),
    }
    return defaults.get(platform, PlatformStats(platform=platform))


def x_placeholder__mutmut_30(platform: str) -> PlatformStats:
    """Last-resort stats so rendering never crashes."""
    defaults = {
        "xbox": PlatformStats(
            platform="xbox",
            username="Gamer",
            headline_value=0,
            headline_label="Gamerscore",
            substats=[SubStat("TA", 0)],
        ),
        "XXpsnXX": PlatformStats(
            platform="psn",
            username="Player",
            headline_value="0 Platinums",
            headline_label="Trophies",
            substats=[
                SubStat("platinum", 0),
                SubStat("gold", 0),
                SubStat("silver", 0),
                SubStat("bronze", 0),
            ],
        ),
        "retroachievements": PlatformStats(
            platform="retroachievements",
            username="RetroUser",
            headline_value=0,
            headline_label="Hardcore Points",
            substats=[
                SubStat("RR", 0.0),
                SubStat("B", 0),
                SubStat("M", 0),
            ],
            extra_fields={
                "BeatenHardcoreAwardsCount": 0,
                "CompletionAwardsCount": 0,
                "MasteryAwardsCount": 0,
            },
        ),
    }
    return defaults.get(platform, PlatformStats(platform=platform))


def x_placeholder__mutmut_31(platform: str) -> PlatformStats:
    """Last-resort stats so rendering never crashes."""
    defaults = {
        "xbox": PlatformStats(
            platform="xbox",
            username="Gamer",
            headline_value=0,
            headline_label="Gamerscore",
            substats=[SubStat("TA", 0)],
        ),
        "PSN": PlatformStats(
            platform="psn",
            username="Player",
            headline_value="0 Platinums",
            headline_label="Trophies",
            substats=[
                SubStat("platinum", 0),
                SubStat("gold", 0),
                SubStat("silver", 0),
                SubStat("bronze", 0),
            ],
        ),
        "retroachievements": PlatformStats(
            platform="retroachievements",
            username="RetroUser",
            headline_value=0,
            headline_label="Hardcore Points",
            substats=[
                SubStat("RR", 0.0),
                SubStat("B", 0),
                SubStat("M", 0),
            ],
            extra_fields={
                "BeatenHardcoreAwardsCount": 0,
                "CompletionAwardsCount": 0,
                "MasteryAwardsCount": 0,
            },
        ),
    }
    return defaults.get(platform, PlatformStats(platform=platform))


def x_placeholder__mutmut_32(platform: str) -> PlatformStats:
    """Last-resort stats so rendering never crashes."""
    defaults = {
        "xbox": PlatformStats(
            platform="xbox",
            username="Gamer",
            headline_value=0,
            headline_label="Gamerscore",
            substats=[SubStat("TA", 0)],
        ),
        "psn": PlatformStats(
            platform=None,
            username="Player",
            headline_value="0 Platinums",
            headline_label="Trophies",
            substats=[
                SubStat("platinum", 0),
                SubStat("gold", 0),
                SubStat("silver", 0),
                SubStat("bronze", 0),
            ],
        ),
        "retroachievements": PlatformStats(
            platform="retroachievements",
            username="RetroUser",
            headline_value=0,
            headline_label="Hardcore Points",
            substats=[
                SubStat("RR", 0.0),
                SubStat("B", 0),
                SubStat("M", 0),
            ],
            extra_fields={
                "BeatenHardcoreAwardsCount": 0,
                "CompletionAwardsCount": 0,
                "MasteryAwardsCount": 0,
            },
        ),
    }
    return defaults.get(platform, PlatformStats(platform=platform))


def x_placeholder__mutmut_33(platform: str) -> PlatformStats:
    """Last-resort stats so rendering never crashes."""
    defaults = {
        "xbox": PlatformStats(
            platform="xbox",
            username="Gamer",
            headline_value=0,
            headline_label="Gamerscore",
            substats=[SubStat("TA", 0)],
        ),
        "psn": PlatformStats(
            platform="psn",
            username=None,
            headline_value="0 Platinums",
            headline_label="Trophies",
            substats=[
                SubStat("platinum", 0),
                SubStat("gold", 0),
                SubStat("silver", 0),
                SubStat("bronze", 0),
            ],
        ),
        "retroachievements": PlatformStats(
            platform="retroachievements",
            username="RetroUser",
            headline_value=0,
            headline_label="Hardcore Points",
            substats=[
                SubStat("RR", 0.0),
                SubStat("B", 0),
                SubStat("M", 0),
            ],
            extra_fields={
                "BeatenHardcoreAwardsCount": 0,
                "CompletionAwardsCount": 0,
                "MasteryAwardsCount": 0,
            },
        ),
    }
    return defaults.get(platform, PlatformStats(platform=platform))


def x_placeholder__mutmut_34(platform: str) -> PlatformStats:
    """Last-resort stats so rendering never crashes."""
    defaults = {
        "xbox": PlatformStats(
            platform="xbox",
            username="Gamer",
            headline_value=0,
            headline_label="Gamerscore",
            substats=[SubStat("TA", 0)],
        ),
        "psn": PlatformStats(
            platform="psn",
            username="Player",
            headline_value=None,
            headline_label="Trophies",
            substats=[
                SubStat("platinum", 0),
                SubStat("gold", 0),
                SubStat("silver", 0),
                SubStat("bronze", 0),
            ],
        ),
        "retroachievements": PlatformStats(
            platform="retroachievements",
            username="RetroUser",
            headline_value=0,
            headline_label="Hardcore Points",
            substats=[
                SubStat("RR", 0.0),
                SubStat("B", 0),
                SubStat("M", 0),
            ],
            extra_fields={
                "BeatenHardcoreAwardsCount": 0,
                "CompletionAwardsCount": 0,
                "MasteryAwardsCount": 0,
            },
        ),
    }
    return defaults.get(platform, PlatformStats(platform=platform))


def x_placeholder__mutmut_35(platform: str) -> PlatformStats:
    """Last-resort stats so rendering never crashes."""
    defaults = {
        "xbox": PlatformStats(
            platform="xbox",
            username="Gamer",
            headline_value=0,
            headline_label="Gamerscore",
            substats=[SubStat("TA", 0)],
        ),
        "psn": PlatformStats(
            platform="psn",
            username="Player",
            headline_value="0 Platinums",
            headline_label=None,
            substats=[
                SubStat("platinum", 0),
                SubStat("gold", 0),
                SubStat("silver", 0),
                SubStat("bronze", 0),
            ],
        ),
        "retroachievements": PlatformStats(
            platform="retroachievements",
            username="RetroUser",
            headline_value=0,
            headline_label="Hardcore Points",
            substats=[
                SubStat("RR", 0.0),
                SubStat("B", 0),
                SubStat("M", 0),
            ],
            extra_fields={
                "BeatenHardcoreAwardsCount": 0,
                "CompletionAwardsCount": 0,
                "MasteryAwardsCount": 0,
            },
        ),
    }
    return defaults.get(platform, PlatformStats(platform=platform))


def x_placeholder__mutmut_36(platform: str) -> PlatformStats:
    """Last-resort stats so rendering never crashes."""
    defaults = {
        "xbox": PlatformStats(
            platform="xbox",
            username="Gamer",
            headline_value=0,
            headline_label="Gamerscore",
            substats=[SubStat("TA", 0)],
        ),
        "psn": PlatformStats(
            platform="psn",
            username="Player",
            headline_value="0 Platinums",
            headline_label="Trophies",
            substats=None,
        ),
        "retroachievements": PlatformStats(
            platform="retroachievements",
            username="RetroUser",
            headline_value=0,
            headline_label="Hardcore Points",
            substats=[
                SubStat("RR", 0.0),
                SubStat("B", 0),
                SubStat("M", 0),
            ],
            extra_fields={
                "BeatenHardcoreAwardsCount": 0,
                "CompletionAwardsCount": 0,
                "MasteryAwardsCount": 0,
            },
        ),
    }
    return defaults.get(platform, PlatformStats(platform=platform))


def x_placeholder__mutmut_37(platform: str) -> PlatformStats:
    """Last-resort stats so rendering never crashes."""
    defaults = {
        "xbox": PlatformStats(
            platform="xbox",
            username="Gamer",
            headline_value=0,
            headline_label="Gamerscore",
            substats=[SubStat("TA", 0)],
        ),
        "psn": PlatformStats(
            username="Player",
            headline_value="0 Platinums",
            headline_label="Trophies",
            substats=[
                SubStat("platinum", 0),
                SubStat("gold", 0),
                SubStat("silver", 0),
                SubStat("bronze", 0),
            ],
        ),
        "retroachievements": PlatformStats(
            platform="retroachievements",
            username="RetroUser",
            headline_value=0,
            headline_label="Hardcore Points",
            substats=[
                SubStat("RR", 0.0),
                SubStat("B", 0),
                SubStat("M", 0),
            ],
            extra_fields={
                "BeatenHardcoreAwardsCount": 0,
                "CompletionAwardsCount": 0,
                "MasteryAwardsCount": 0,
            },
        ),
    }
    return defaults.get(platform, PlatformStats(platform=platform))


def x_placeholder__mutmut_38(platform: str) -> PlatformStats:
    """Last-resort stats so rendering never crashes."""
    defaults = {
        "xbox": PlatformStats(
            platform="xbox",
            username="Gamer",
            headline_value=0,
            headline_label="Gamerscore",
            substats=[SubStat("TA", 0)],
        ),
        "psn": PlatformStats(
            platform="psn",
            headline_value="0 Platinums",
            headline_label="Trophies",
            substats=[
                SubStat("platinum", 0),
                SubStat("gold", 0),
                SubStat("silver", 0),
                SubStat("bronze", 0),
            ],
        ),
        "retroachievements": PlatformStats(
            platform="retroachievements",
            username="RetroUser",
            headline_value=0,
            headline_label="Hardcore Points",
            substats=[
                SubStat("RR", 0.0),
                SubStat("B", 0),
                SubStat("M", 0),
            ],
            extra_fields={
                "BeatenHardcoreAwardsCount": 0,
                "CompletionAwardsCount": 0,
                "MasteryAwardsCount": 0,
            },
        ),
    }
    return defaults.get(platform, PlatformStats(platform=platform))


def x_placeholder__mutmut_39(platform: str) -> PlatformStats:
    """Last-resort stats so rendering never crashes."""
    defaults = {
        "xbox": PlatformStats(
            platform="xbox",
            username="Gamer",
            headline_value=0,
            headline_label="Gamerscore",
            substats=[SubStat("TA", 0)],
        ),
        "psn": PlatformStats(
            platform="psn",
            username="Player",
            headline_label="Trophies",
            substats=[
                SubStat("platinum", 0),
                SubStat("gold", 0),
                SubStat("silver", 0),
                SubStat("bronze", 0),
            ],
        ),
        "retroachievements": PlatformStats(
            platform="retroachievements",
            username="RetroUser",
            headline_value=0,
            headline_label="Hardcore Points",
            substats=[
                SubStat("RR", 0.0),
                SubStat("B", 0),
                SubStat("M", 0),
            ],
            extra_fields={
                "BeatenHardcoreAwardsCount": 0,
                "CompletionAwardsCount": 0,
                "MasteryAwardsCount": 0,
            },
        ),
    }
    return defaults.get(platform, PlatformStats(platform=platform))


def x_placeholder__mutmut_40(platform: str) -> PlatformStats:
    """Last-resort stats so rendering never crashes."""
    defaults = {
        "xbox": PlatformStats(
            platform="xbox",
            username="Gamer",
            headline_value=0,
            headline_label="Gamerscore",
            substats=[SubStat("TA", 0)],
        ),
        "psn": PlatformStats(
            platform="psn",
            username="Player",
            headline_value="0 Platinums",
            substats=[
                SubStat("platinum", 0),
                SubStat("gold", 0),
                SubStat("silver", 0),
                SubStat("bronze", 0),
            ],
        ),
        "retroachievements": PlatformStats(
            platform="retroachievements",
            username="RetroUser",
            headline_value=0,
            headline_label="Hardcore Points",
            substats=[
                SubStat("RR", 0.0),
                SubStat("B", 0),
                SubStat("M", 0),
            ],
            extra_fields={
                "BeatenHardcoreAwardsCount": 0,
                "CompletionAwardsCount": 0,
                "MasteryAwardsCount": 0,
            },
        ),
    }
    return defaults.get(platform, PlatformStats(platform=platform))


def x_placeholder__mutmut_41(platform: str) -> PlatformStats:
    """Last-resort stats so rendering never crashes."""
    defaults = {
        "xbox": PlatformStats(
            platform="xbox",
            username="Gamer",
            headline_value=0,
            headline_label="Gamerscore",
            substats=[SubStat("TA", 0)],
        ),
        "psn": PlatformStats(
            platform="psn",
            username="Player",
            headline_value="0 Platinums",
            headline_label="Trophies",
            ),
        "retroachievements": PlatformStats(
            platform="retroachievements",
            username="RetroUser",
            headline_value=0,
            headline_label="Hardcore Points",
            substats=[
                SubStat("RR", 0.0),
                SubStat("B", 0),
                SubStat("M", 0),
            ],
            extra_fields={
                "BeatenHardcoreAwardsCount": 0,
                "CompletionAwardsCount": 0,
                "MasteryAwardsCount": 0,
            },
        ),
    }
    return defaults.get(platform, PlatformStats(platform=platform))


def x_placeholder__mutmut_42(platform: str) -> PlatformStats:
    """Last-resort stats so rendering never crashes."""
    defaults = {
        "xbox": PlatformStats(
            platform="xbox",
            username="Gamer",
            headline_value=0,
            headline_label="Gamerscore",
            substats=[SubStat("TA", 0)],
        ),
        "psn": PlatformStats(
            platform="XXpsnXX",
            username="Player",
            headline_value="0 Platinums",
            headline_label="Trophies",
            substats=[
                SubStat("platinum", 0),
                SubStat("gold", 0),
                SubStat("silver", 0),
                SubStat("bronze", 0),
            ],
        ),
        "retroachievements": PlatformStats(
            platform="retroachievements",
            username="RetroUser",
            headline_value=0,
            headline_label="Hardcore Points",
            substats=[
                SubStat("RR", 0.0),
                SubStat("B", 0),
                SubStat("M", 0),
            ],
            extra_fields={
                "BeatenHardcoreAwardsCount": 0,
                "CompletionAwardsCount": 0,
                "MasteryAwardsCount": 0,
            },
        ),
    }
    return defaults.get(platform, PlatformStats(platform=platform))


def x_placeholder__mutmut_43(platform: str) -> PlatformStats:
    """Last-resort stats so rendering never crashes."""
    defaults = {
        "xbox": PlatformStats(
            platform="xbox",
            username="Gamer",
            headline_value=0,
            headline_label="Gamerscore",
            substats=[SubStat("TA", 0)],
        ),
        "psn": PlatformStats(
            platform="PSN",
            username="Player",
            headline_value="0 Platinums",
            headline_label="Trophies",
            substats=[
                SubStat("platinum", 0),
                SubStat("gold", 0),
                SubStat("silver", 0),
                SubStat("bronze", 0),
            ],
        ),
        "retroachievements": PlatformStats(
            platform="retroachievements",
            username="RetroUser",
            headline_value=0,
            headline_label="Hardcore Points",
            substats=[
                SubStat("RR", 0.0),
                SubStat("B", 0),
                SubStat("M", 0),
            ],
            extra_fields={
                "BeatenHardcoreAwardsCount": 0,
                "CompletionAwardsCount": 0,
                "MasteryAwardsCount": 0,
            },
        ),
    }
    return defaults.get(platform, PlatformStats(platform=platform))


def x_placeholder__mutmut_44(platform: str) -> PlatformStats:
    """Last-resort stats so rendering never crashes."""
    defaults = {
        "xbox": PlatformStats(
            platform="xbox",
            username="Gamer",
            headline_value=0,
            headline_label="Gamerscore",
            substats=[SubStat("TA", 0)],
        ),
        "psn": PlatformStats(
            platform="psn",
            username="XXPlayerXX",
            headline_value="0 Platinums",
            headline_label="Trophies",
            substats=[
                SubStat("platinum", 0),
                SubStat("gold", 0),
                SubStat("silver", 0),
                SubStat("bronze", 0),
            ],
        ),
        "retroachievements": PlatformStats(
            platform="retroachievements",
            username="RetroUser",
            headline_value=0,
            headline_label="Hardcore Points",
            substats=[
                SubStat("RR", 0.0),
                SubStat("B", 0),
                SubStat("M", 0),
            ],
            extra_fields={
                "BeatenHardcoreAwardsCount": 0,
                "CompletionAwardsCount": 0,
                "MasteryAwardsCount": 0,
            },
        ),
    }
    return defaults.get(platform, PlatformStats(platform=platform))


def x_placeholder__mutmut_45(platform: str) -> PlatformStats:
    """Last-resort stats so rendering never crashes."""
    defaults = {
        "xbox": PlatformStats(
            platform="xbox",
            username="Gamer",
            headline_value=0,
            headline_label="Gamerscore",
            substats=[SubStat("TA", 0)],
        ),
        "psn": PlatformStats(
            platform="psn",
            username="player",
            headline_value="0 Platinums",
            headline_label="Trophies",
            substats=[
                SubStat("platinum", 0),
                SubStat("gold", 0),
                SubStat("silver", 0),
                SubStat("bronze", 0),
            ],
        ),
        "retroachievements": PlatformStats(
            platform="retroachievements",
            username="RetroUser",
            headline_value=0,
            headline_label="Hardcore Points",
            substats=[
                SubStat("RR", 0.0),
                SubStat("B", 0),
                SubStat("M", 0),
            ],
            extra_fields={
                "BeatenHardcoreAwardsCount": 0,
                "CompletionAwardsCount": 0,
                "MasteryAwardsCount": 0,
            },
        ),
    }
    return defaults.get(platform, PlatformStats(platform=platform))


def x_placeholder__mutmut_46(platform: str) -> PlatformStats:
    """Last-resort stats so rendering never crashes."""
    defaults = {
        "xbox": PlatformStats(
            platform="xbox",
            username="Gamer",
            headline_value=0,
            headline_label="Gamerscore",
            substats=[SubStat("TA", 0)],
        ),
        "psn": PlatformStats(
            platform="psn",
            username="PLAYER",
            headline_value="0 Platinums",
            headline_label="Trophies",
            substats=[
                SubStat("platinum", 0),
                SubStat("gold", 0),
                SubStat("silver", 0),
                SubStat("bronze", 0),
            ],
        ),
        "retroachievements": PlatformStats(
            platform="retroachievements",
            username="RetroUser",
            headline_value=0,
            headline_label="Hardcore Points",
            substats=[
                SubStat("RR", 0.0),
                SubStat("B", 0),
                SubStat("M", 0),
            ],
            extra_fields={
                "BeatenHardcoreAwardsCount": 0,
                "CompletionAwardsCount": 0,
                "MasteryAwardsCount": 0,
            },
        ),
    }
    return defaults.get(platform, PlatformStats(platform=platform))


def x_placeholder__mutmut_47(platform: str) -> PlatformStats:
    """Last-resort stats so rendering never crashes."""
    defaults = {
        "xbox": PlatformStats(
            platform="xbox",
            username="Gamer",
            headline_value=0,
            headline_label="Gamerscore",
            substats=[SubStat("TA", 0)],
        ),
        "psn": PlatformStats(
            platform="psn",
            username="Player",
            headline_value="XX0 PlatinumsXX",
            headline_label="Trophies",
            substats=[
                SubStat("platinum", 0),
                SubStat("gold", 0),
                SubStat("silver", 0),
                SubStat("bronze", 0),
            ],
        ),
        "retroachievements": PlatformStats(
            platform="retroachievements",
            username="RetroUser",
            headline_value=0,
            headline_label="Hardcore Points",
            substats=[
                SubStat("RR", 0.0),
                SubStat("B", 0),
                SubStat("M", 0),
            ],
            extra_fields={
                "BeatenHardcoreAwardsCount": 0,
                "CompletionAwardsCount": 0,
                "MasteryAwardsCount": 0,
            },
        ),
    }
    return defaults.get(platform, PlatformStats(platform=platform))


def x_placeholder__mutmut_48(platform: str) -> PlatformStats:
    """Last-resort stats so rendering never crashes."""
    defaults = {
        "xbox": PlatformStats(
            platform="xbox",
            username="Gamer",
            headline_value=0,
            headline_label="Gamerscore",
            substats=[SubStat("TA", 0)],
        ),
        "psn": PlatformStats(
            platform="psn",
            username="Player",
            headline_value="0 platinums",
            headline_label="Trophies",
            substats=[
                SubStat("platinum", 0),
                SubStat("gold", 0),
                SubStat("silver", 0),
                SubStat("bronze", 0),
            ],
        ),
        "retroachievements": PlatformStats(
            platform="retroachievements",
            username="RetroUser",
            headline_value=0,
            headline_label="Hardcore Points",
            substats=[
                SubStat("RR", 0.0),
                SubStat("B", 0),
                SubStat("M", 0),
            ],
            extra_fields={
                "BeatenHardcoreAwardsCount": 0,
                "CompletionAwardsCount": 0,
                "MasteryAwardsCount": 0,
            },
        ),
    }
    return defaults.get(platform, PlatformStats(platform=platform))


def x_placeholder__mutmut_49(platform: str) -> PlatformStats:
    """Last-resort stats so rendering never crashes."""
    defaults = {
        "xbox": PlatformStats(
            platform="xbox",
            username="Gamer",
            headline_value=0,
            headline_label="Gamerscore",
            substats=[SubStat("TA", 0)],
        ),
        "psn": PlatformStats(
            platform="psn",
            username="Player",
            headline_value="0 PLATINUMS",
            headline_label="Trophies",
            substats=[
                SubStat("platinum", 0),
                SubStat("gold", 0),
                SubStat("silver", 0),
                SubStat("bronze", 0),
            ],
        ),
        "retroachievements": PlatformStats(
            platform="retroachievements",
            username="RetroUser",
            headline_value=0,
            headline_label="Hardcore Points",
            substats=[
                SubStat("RR", 0.0),
                SubStat("B", 0),
                SubStat("M", 0),
            ],
            extra_fields={
                "BeatenHardcoreAwardsCount": 0,
                "CompletionAwardsCount": 0,
                "MasteryAwardsCount": 0,
            },
        ),
    }
    return defaults.get(platform, PlatformStats(platform=platform))


def x_placeholder__mutmut_50(platform: str) -> PlatformStats:
    """Last-resort stats so rendering never crashes."""
    defaults = {
        "xbox": PlatformStats(
            platform="xbox",
            username="Gamer",
            headline_value=0,
            headline_label="Gamerscore",
            substats=[SubStat("TA", 0)],
        ),
        "psn": PlatformStats(
            platform="psn",
            username="Player",
            headline_value="0 Platinums",
            headline_label="XXTrophiesXX",
            substats=[
                SubStat("platinum", 0),
                SubStat("gold", 0),
                SubStat("silver", 0),
                SubStat("bronze", 0),
            ],
        ),
        "retroachievements": PlatformStats(
            platform="retroachievements",
            username="RetroUser",
            headline_value=0,
            headline_label="Hardcore Points",
            substats=[
                SubStat("RR", 0.0),
                SubStat("B", 0),
                SubStat("M", 0),
            ],
            extra_fields={
                "BeatenHardcoreAwardsCount": 0,
                "CompletionAwardsCount": 0,
                "MasteryAwardsCount": 0,
            },
        ),
    }
    return defaults.get(platform, PlatformStats(platform=platform))


def x_placeholder__mutmut_51(platform: str) -> PlatformStats:
    """Last-resort stats so rendering never crashes."""
    defaults = {
        "xbox": PlatformStats(
            platform="xbox",
            username="Gamer",
            headline_value=0,
            headline_label="Gamerscore",
            substats=[SubStat("TA", 0)],
        ),
        "psn": PlatformStats(
            platform="psn",
            username="Player",
            headline_value="0 Platinums",
            headline_label="trophies",
            substats=[
                SubStat("platinum", 0),
                SubStat("gold", 0),
                SubStat("silver", 0),
                SubStat("bronze", 0),
            ],
        ),
        "retroachievements": PlatformStats(
            platform="retroachievements",
            username="RetroUser",
            headline_value=0,
            headline_label="Hardcore Points",
            substats=[
                SubStat("RR", 0.0),
                SubStat("B", 0),
                SubStat("M", 0),
            ],
            extra_fields={
                "BeatenHardcoreAwardsCount": 0,
                "CompletionAwardsCount": 0,
                "MasteryAwardsCount": 0,
            },
        ),
    }
    return defaults.get(platform, PlatformStats(platform=platform))


def x_placeholder__mutmut_52(platform: str) -> PlatformStats:
    """Last-resort stats so rendering never crashes."""
    defaults = {
        "xbox": PlatformStats(
            platform="xbox",
            username="Gamer",
            headline_value=0,
            headline_label="Gamerscore",
            substats=[SubStat("TA", 0)],
        ),
        "psn": PlatformStats(
            platform="psn",
            username="Player",
            headline_value="0 Platinums",
            headline_label="TROPHIES",
            substats=[
                SubStat("platinum", 0),
                SubStat("gold", 0),
                SubStat("silver", 0),
                SubStat("bronze", 0),
            ],
        ),
        "retroachievements": PlatformStats(
            platform="retroachievements",
            username="RetroUser",
            headline_value=0,
            headline_label="Hardcore Points",
            substats=[
                SubStat("RR", 0.0),
                SubStat("B", 0),
                SubStat("M", 0),
            ],
            extra_fields={
                "BeatenHardcoreAwardsCount": 0,
                "CompletionAwardsCount": 0,
                "MasteryAwardsCount": 0,
            },
        ),
    }
    return defaults.get(platform, PlatformStats(platform=platform))


def x_placeholder__mutmut_53(platform: str) -> PlatformStats:
    """Last-resort stats so rendering never crashes."""
    defaults = {
        "xbox": PlatformStats(
            platform="xbox",
            username="Gamer",
            headline_value=0,
            headline_label="Gamerscore",
            substats=[SubStat("TA", 0)],
        ),
        "psn": PlatformStats(
            platform="psn",
            username="Player",
            headline_value="0 Platinums",
            headline_label="Trophies",
            substats=[
                SubStat(None, 0),
                SubStat("gold", 0),
                SubStat("silver", 0),
                SubStat("bronze", 0),
            ],
        ),
        "retroachievements": PlatformStats(
            platform="retroachievements",
            username="RetroUser",
            headline_value=0,
            headline_label="Hardcore Points",
            substats=[
                SubStat("RR", 0.0),
                SubStat("B", 0),
                SubStat("M", 0),
            ],
            extra_fields={
                "BeatenHardcoreAwardsCount": 0,
                "CompletionAwardsCount": 0,
                "MasteryAwardsCount": 0,
            },
        ),
    }
    return defaults.get(platform, PlatformStats(platform=platform))


def x_placeholder__mutmut_54(platform: str) -> PlatformStats:
    """Last-resort stats so rendering never crashes."""
    defaults = {
        "xbox": PlatformStats(
            platform="xbox",
            username="Gamer",
            headline_value=0,
            headline_label="Gamerscore",
            substats=[SubStat("TA", 0)],
        ),
        "psn": PlatformStats(
            platform="psn",
            username="Player",
            headline_value="0 Platinums",
            headline_label="Trophies",
            substats=[
                SubStat("platinum", None),
                SubStat("gold", 0),
                SubStat("silver", 0),
                SubStat("bronze", 0),
            ],
        ),
        "retroachievements": PlatformStats(
            platform="retroachievements",
            username="RetroUser",
            headline_value=0,
            headline_label="Hardcore Points",
            substats=[
                SubStat("RR", 0.0),
                SubStat("B", 0),
                SubStat("M", 0),
            ],
            extra_fields={
                "BeatenHardcoreAwardsCount": 0,
                "CompletionAwardsCount": 0,
                "MasteryAwardsCount": 0,
            },
        ),
    }
    return defaults.get(platform, PlatformStats(platform=platform))


def x_placeholder__mutmut_55(platform: str) -> PlatformStats:
    """Last-resort stats so rendering never crashes."""
    defaults = {
        "xbox": PlatformStats(
            platform="xbox",
            username="Gamer",
            headline_value=0,
            headline_label="Gamerscore",
            substats=[SubStat("TA", 0)],
        ),
        "psn": PlatformStats(
            platform="psn",
            username="Player",
            headline_value="0 Platinums",
            headline_label="Trophies",
            substats=[
                SubStat(0),
                SubStat("gold", 0),
                SubStat("silver", 0),
                SubStat("bronze", 0),
            ],
        ),
        "retroachievements": PlatformStats(
            platform="retroachievements",
            username="RetroUser",
            headline_value=0,
            headline_label="Hardcore Points",
            substats=[
                SubStat("RR", 0.0),
                SubStat("B", 0),
                SubStat("M", 0),
            ],
            extra_fields={
                "BeatenHardcoreAwardsCount": 0,
                "CompletionAwardsCount": 0,
                "MasteryAwardsCount": 0,
            },
        ),
    }
    return defaults.get(platform, PlatformStats(platform=platform))


def x_placeholder__mutmut_56(platform: str) -> PlatformStats:
    """Last-resort stats so rendering never crashes."""
    defaults = {
        "xbox": PlatformStats(
            platform="xbox",
            username="Gamer",
            headline_value=0,
            headline_label="Gamerscore",
            substats=[SubStat("TA", 0)],
        ),
        "psn": PlatformStats(
            platform="psn",
            username="Player",
            headline_value="0 Platinums",
            headline_label="Trophies",
            substats=[
                SubStat("platinum", ),
                SubStat("gold", 0),
                SubStat("silver", 0),
                SubStat("bronze", 0),
            ],
        ),
        "retroachievements": PlatformStats(
            platform="retroachievements",
            username="RetroUser",
            headline_value=0,
            headline_label="Hardcore Points",
            substats=[
                SubStat("RR", 0.0),
                SubStat("B", 0),
                SubStat("M", 0),
            ],
            extra_fields={
                "BeatenHardcoreAwardsCount": 0,
                "CompletionAwardsCount": 0,
                "MasteryAwardsCount": 0,
            },
        ),
    }
    return defaults.get(platform, PlatformStats(platform=platform))


def x_placeholder__mutmut_57(platform: str) -> PlatformStats:
    """Last-resort stats so rendering never crashes."""
    defaults = {
        "xbox": PlatformStats(
            platform="xbox",
            username="Gamer",
            headline_value=0,
            headline_label="Gamerscore",
            substats=[SubStat("TA", 0)],
        ),
        "psn": PlatformStats(
            platform="psn",
            username="Player",
            headline_value="0 Platinums",
            headline_label="Trophies",
            substats=[
                SubStat("XXplatinumXX", 0),
                SubStat("gold", 0),
                SubStat("silver", 0),
                SubStat("bronze", 0),
            ],
        ),
        "retroachievements": PlatformStats(
            platform="retroachievements",
            username="RetroUser",
            headline_value=0,
            headline_label="Hardcore Points",
            substats=[
                SubStat("RR", 0.0),
                SubStat("B", 0),
                SubStat("M", 0),
            ],
            extra_fields={
                "BeatenHardcoreAwardsCount": 0,
                "CompletionAwardsCount": 0,
                "MasteryAwardsCount": 0,
            },
        ),
    }
    return defaults.get(platform, PlatformStats(platform=platform))


def x_placeholder__mutmut_58(platform: str) -> PlatformStats:
    """Last-resort stats so rendering never crashes."""
    defaults = {
        "xbox": PlatformStats(
            platform="xbox",
            username="Gamer",
            headline_value=0,
            headline_label="Gamerscore",
            substats=[SubStat("TA", 0)],
        ),
        "psn": PlatformStats(
            platform="psn",
            username="Player",
            headline_value="0 Platinums",
            headline_label="Trophies",
            substats=[
                SubStat("PLATINUM", 0),
                SubStat("gold", 0),
                SubStat("silver", 0),
                SubStat("bronze", 0),
            ],
        ),
        "retroachievements": PlatformStats(
            platform="retroachievements",
            username="RetroUser",
            headline_value=0,
            headline_label="Hardcore Points",
            substats=[
                SubStat("RR", 0.0),
                SubStat("B", 0),
                SubStat("M", 0),
            ],
            extra_fields={
                "BeatenHardcoreAwardsCount": 0,
                "CompletionAwardsCount": 0,
                "MasteryAwardsCount": 0,
            },
        ),
    }
    return defaults.get(platform, PlatformStats(platform=platform))


def x_placeholder__mutmut_59(platform: str) -> PlatformStats:
    """Last-resort stats so rendering never crashes."""
    defaults = {
        "xbox": PlatformStats(
            platform="xbox",
            username="Gamer",
            headline_value=0,
            headline_label="Gamerscore",
            substats=[SubStat("TA", 0)],
        ),
        "psn": PlatformStats(
            platform="psn",
            username="Player",
            headline_value="0 Platinums",
            headline_label="Trophies",
            substats=[
                SubStat("platinum", 1),
                SubStat("gold", 0),
                SubStat("silver", 0),
                SubStat("bronze", 0),
            ],
        ),
        "retroachievements": PlatformStats(
            platform="retroachievements",
            username="RetroUser",
            headline_value=0,
            headline_label="Hardcore Points",
            substats=[
                SubStat("RR", 0.0),
                SubStat("B", 0),
                SubStat("M", 0),
            ],
            extra_fields={
                "BeatenHardcoreAwardsCount": 0,
                "CompletionAwardsCount": 0,
                "MasteryAwardsCount": 0,
            },
        ),
    }
    return defaults.get(platform, PlatformStats(platform=platform))


def x_placeholder__mutmut_60(platform: str) -> PlatformStats:
    """Last-resort stats so rendering never crashes."""
    defaults = {
        "xbox": PlatformStats(
            platform="xbox",
            username="Gamer",
            headline_value=0,
            headline_label="Gamerscore",
            substats=[SubStat("TA", 0)],
        ),
        "psn": PlatformStats(
            platform="psn",
            username="Player",
            headline_value="0 Platinums",
            headline_label="Trophies",
            substats=[
                SubStat("platinum", 0),
                SubStat(None, 0),
                SubStat("silver", 0),
                SubStat("bronze", 0),
            ],
        ),
        "retroachievements": PlatformStats(
            platform="retroachievements",
            username="RetroUser",
            headline_value=0,
            headline_label="Hardcore Points",
            substats=[
                SubStat("RR", 0.0),
                SubStat("B", 0),
                SubStat("M", 0),
            ],
            extra_fields={
                "BeatenHardcoreAwardsCount": 0,
                "CompletionAwardsCount": 0,
                "MasteryAwardsCount": 0,
            },
        ),
    }
    return defaults.get(platform, PlatformStats(platform=platform))


def x_placeholder__mutmut_61(platform: str) -> PlatformStats:
    """Last-resort stats so rendering never crashes."""
    defaults = {
        "xbox": PlatformStats(
            platform="xbox",
            username="Gamer",
            headline_value=0,
            headline_label="Gamerscore",
            substats=[SubStat("TA", 0)],
        ),
        "psn": PlatformStats(
            platform="psn",
            username="Player",
            headline_value="0 Platinums",
            headline_label="Trophies",
            substats=[
                SubStat("platinum", 0),
                SubStat("gold", None),
                SubStat("silver", 0),
                SubStat("bronze", 0),
            ],
        ),
        "retroachievements": PlatformStats(
            platform="retroachievements",
            username="RetroUser",
            headline_value=0,
            headline_label="Hardcore Points",
            substats=[
                SubStat("RR", 0.0),
                SubStat("B", 0),
                SubStat("M", 0),
            ],
            extra_fields={
                "BeatenHardcoreAwardsCount": 0,
                "CompletionAwardsCount": 0,
                "MasteryAwardsCount": 0,
            },
        ),
    }
    return defaults.get(platform, PlatformStats(platform=platform))


def x_placeholder__mutmut_62(platform: str) -> PlatformStats:
    """Last-resort stats so rendering never crashes."""
    defaults = {
        "xbox": PlatformStats(
            platform="xbox",
            username="Gamer",
            headline_value=0,
            headline_label="Gamerscore",
            substats=[SubStat("TA", 0)],
        ),
        "psn": PlatformStats(
            platform="psn",
            username="Player",
            headline_value="0 Platinums",
            headline_label="Trophies",
            substats=[
                SubStat("platinum", 0),
                SubStat(0),
                SubStat("silver", 0),
                SubStat("bronze", 0),
            ],
        ),
        "retroachievements": PlatformStats(
            platform="retroachievements",
            username="RetroUser",
            headline_value=0,
            headline_label="Hardcore Points",
            substats=[
                SubStat("RR", 0.0),
                SubStat("B", 0),
                SubStat("M", 0),
            ],
            extra_fields={
                "BeatenHardcoreAwardsCount": 0,
                "CompletionAwardsCount": 0,
                "MasteryAwardsCount": 0,
            },
        ),
    }
    return defaults.get(platform, PlatformStats(platform=platform))


def x_placeholder__mutmut_63(platform: str) -> PlatformStats:
    """Last-resort stats so rendering never crashes."""
    defaults = {
        "xbox": PlatformStats(
            platform="xbox",
            username="Gamer",
            headline_value=0,
            headline_label="Gamerscore",
            substats=[SubStat("TA", 0)],
        ),
        "psn": PlatformStats(
            platform="psn",
            username="Player",
            headline_value="0 Platinums",
            headline_label="Trophies",
            substats=[
                SubStat("platinum", 0),
                SubStat("gold", ),
                SubStat("silver", 0),
                SubStat("bronze", 0),
            ],
        ),
        "retroachievements": PlatformStats(
            platform="retroachievements",
            username="RetroUser",
            headline_value=0,
            headline_label="Hardcore Points",
            substats=[
                SubStat("RR", 0.0),
                SubStat("B", 0),
                SubStat("M", 0),
            ],
            extra_fields={
                "BeatenHardcoreAwardsCount": 0,
                "CompletionAwardsCount": 0,
                "MasteryAwardsCount": 0,
            },
        ),
    }
    return defaults.get(platform, PlatformStats(platform=platform))


def x_placeholder__mutmut_64(platform: str) -> PlatformStats:
    """Last-resort stats so rendering never crashes."""
    defaults = {
        "xbox": PlatformStats(
            platform="xbox",
            username="Gamer",
            headline_value=0,
            headline_label="Gamerscore",
            substats=[SubStat("TA", 0)],
        ),
        "psn": PlatformStats(
            platform="psn",
            username="Player",
            headline_value="0 Platinums",
            headline_label="Trophies",
            substats=[
                SubStat("platinum", 0),
                SubStat("XXgoldXX", 0),
                SubStat("silver", 0),
                SubStat("bronze", 0),
            ],
        ),
        "retroachievements": PlatformStats(
            platform="retroachievements",
            username="RetroUser",
            headline_value=0,
            headline_label="Hardcore Points",
            substats=[
                SubStat("RR", 0.0),
                SubStat("B", 0),
                SubStat("M", 0),
            ],
            extra_fields={
                "BeatenHardcoreAwardsCount": 0,
                "CompletionAwardsCount": 0,
                "MasteryAwardsCount": 0,
            },
        ),
    }
    return defaults.get(platform, PlatformStats(platform=platform))


def x_placeholder__mutmut_65(platform: str) -> PlatformStats:
    """Last-resort stats so rendering never crashes."""
    defaults = {
        "xbox": PlatformStats(
            platform="xbox",
            username="Gamer",
            headline_value=0,
            headline_label="Gamerscore",
            substats=[SubStat("TA", 0)],
        ),
        "psn": PlatformStats(
            platform="psn",
            username="Player",
            headline_value="0 Platinums",
            headline_label="Trophies",
            substats=[
                SubStat("platinum", 0),
                SubStat("GOLD", 0),
                SubStat("silver", 0),
                SubStat("bronze", 0),
            ],
        ),
        "retroachievements": PlatformStats(
            platform="retroachievements",
            username="RetroUser",
            headline_value=0,
            headline_label="Hardcore Points",
            substats=[
                SubStat("RR", 0.0),
                SubStat("B", 0),
                SubStat("M", 0),
            ],
            extra_fields={
                "BeatenHardcoreAwardsCount": 0,
                "CompletionAwardsCount": 0,
                "MasteryAwardsCount": 0,
            },
        ),
    }
    return defaults.get(platform, PlatformStats(platform=platform))


def x_placeholder__mutmut_66(platform: str) -> PlatformStats:
    """Last-resort stats so rendering never crashes."""
    defaults = {
        "xbox": PlatformStats(
            platform="xbox",
            username="Gamer",
            headline_value=0,
            headline_label="Gamerscore",
            substats=[SubStat("TA", 0)],
        ),
        "psn": PlatformStats(
            platform="psn",
            username="Player",
            headline_value="0 Platinums",
            headline_label="Trophies",
            substats=[
                SubStat("platinum", 0),
                SubStat("gold", 1),
                SubStat("silver", 0),
                SubStat("bronze", 0),
            ],
        ),
        "retroachievements": PlatformStats(
            platform="retroachievements",
            username="RetroUser",
            headline_value=0,
            headline_label="Hardcore Points",
            substats=[
                SubStat("RR", 0.0),
                SubStat("B", 0),
                SubStat("M", 0),
            ],
            extra_fields={
                "BeatenHardcoreAwardsCount": 0,
                "CompletionAwardsCount": 0,
                "MasteryAwardsCount": 0,
            },
        ),
    }
    return defaults.get(platform, PlatformStats(platform=platform))


def x_placeholder__mutmut_67(platform: str) -> PlatformStats:
    """Last-resort stats so rendering never crashes."""
    defaults = {
        "xbox": PlatformStats(
            platform="xbox",
            username="Gamer",
            headline_value=0,
            headline_label="Gamerscore",
            substats=[SubStat("TA", 0)],
        ),
        "psn": PlatformStats(
            platform="psn",
            username="Player",
            headline_value="0 Platinums",
            headline_label="Trophies",
            substats=[
                SubStat("platinum", 0),
                SubStat("gold", 0),
                SubStat(None, 0),
                SubStat("bronze", 0),
            ],
        ),
        "retroachievements": PlatformStats(
            platform="retroachievements",
            username="RetroUser",
            headline_value=0,
            headline_label="Hardcore Points",
            substats=[
                SubStat("RR", 0.0),
                SubStat("B", 0),
                SubStat("M", 0),
            ],
            extra_fields={
                "BeatenHardcoreAwardsCount": 0,
                "CompletionAwardsCount": 0,
                "MasteryAwardsCount": 0,
            },
        ),
    }
    return defaults.get(platform, PlatformStats(platform=platform))


def x_placeholder__mutmut_68(platform: str) -> PlatformStats:
    """Last-resort stats so rendering never crashes."""
    defaults = {
        "xbox": PlatformStats(
            platform="xbox",
            username="Gamer",
            headline_value=0,
            headline_label="Gamerscore",
            substats=[SubStat("TA", 0)],
        ),
        "psn": PlatformStats(
            platform="psn",
            username="Player",
            headline_value="0 Platinums",
            headline_label="Trophies",
            substats=[
                SubStat("platinum", 0),
                SubStat("gold", 0),
                SubStat("silver", None),
                SubStat("bronze", 0),
            ],
        ),
        "retroachievements": PlatformStats(
            platform="retroachievements",
            username="RetroUser",
            headline_value=0,
            headline_label="Hardcore Points",
            substats=[
                SubStat("RR", 0.0),
                SubStat("B", 0),
                SubStat("M", 0),
            ],
            extra_fields={
                "BeatenHardcoreAwardsCount": 0,
                "CompletionAwardsCount": 0,
                "MasteryAwardsCount": 0,
            },
        ),
    }
    return defaults.get(platform, PlatformStats(platform=platform))


def x_placeholder__mutmut_69(platform: str) -> PlatformStats:
    """Last-resort stats so rendering never crashes."""
    defaults = {
        "xbox": PlatformStats(
            platform="xbox",
            username="Gamer",
            headline_value=0,
            headline_label="Gamerscore",
            substats=[SubStat("TA", 0)],
        ),
        "psn": PlatformStats(
            platform="psn",
            username="Player",
            headline_value="0 Platinums",
            headline_label="Trophies",
            substats=[
                SubStat("platinum", 0),
                SubStat("gold", 0),
                SubStat(0),
                SubStat("bronze", 0),
            ],
        ),
        "retroachievements": PlatformStats(
            platform="retroachievements",
            username="RetroUser",
            headline_value=0,
            headline_label="Hardcore Points",
            substats=[
                SubStat("RR", 0.0),
                SubStat("B", 0),
                SubStat("M", 0),
            ],
            extra_fields={
                "BeatenHardcoreAwardsCount": 0,
                "CompletionAwardsCount": 0,
                "MasteryAwardsCount": 0,
            },
        ),
    }
    return defaults.get(platform, PlatformStats(platform=platform))


def x_placeholder__mutmut_70(platform: str) -> PlatformStats:
    """Last-resort stats so rendering never crashes."""
    defaults = {
        "xbox": PlatformStats(
            platform="xbox",
            username="Gamer",
            headline_value=0,
            headline_label="Gamerscore",
            substats=[SubStat("TA", 0)],
        ),
        "psn": PlatformStats(
            platform="psn",
            username="Player",
            headline_value="0 Platinums",
            headline_label="Trophies",
            substats=[
                SubStat("platinum", 0),
                SubStat("gold", 0),
                SubStat("silver", ),
                SubStat("bronze", 0),
            ],
        ),
        "retroachievements": PlatformStats(
            platform="retroachievements",
            username="RetroUser",
            headline_value=0,
            headline_label="Hardcore Points",
            substats=[
                SubStat("RR", 0.0),
                SubStat("B", 0),
                SubStat("M", 0),
            ],
            extra_fields={
                "BeatenHardcoreAwardsCount": 0,
                "CompletionAwardsCount": 0,
                "MasteryAwardsCount": 0,
            },
        ),
    }
    return defaults.get(platform, PlatformStats(platform=platform))


def x_placeholder__mutmut_71(platform: str) -> PlatformStats:
    """Last-resort stats so rendering never crashes."""
    defaults = {
        "xbox": PlatformStats(
            platform="xbox",
            username="Gamer",
            headline_value=0,
            headline_label="Gamerscore",
            substats=[SubStat("TA", 0)],
        ),
        "psn": PlatformStats(
            platform="psn",
            username="Player",
            headline_value="0 Platinums",
            headline_label="Trophies",
            substats=[
                SubStat("platinum", 0),
                SubStat("gold", 0),
                SubStat("XXsilverXX", 0),
                SubStat("bronze", 0),
            ],
        ),
        "retroachievements": PlatformStats(
            platform="retroachievements",
            username="RetroUser",
            headline_value=0,
            headline_label="Hardcore Points",
            substats=[
                SubStat("RR", 0.0),
                SubStat("B", 0),
                SubStat("M", 0),
            ],
            extra_fields={
                "BeatenHardcoreAwardsCount": 0,
                "CompletionAwardsCount": 0,
                "MasteryAwardsCount": 0,
            },
        ),
    }
    return defaults.get(platform, PlatformStats(platform=platform))


def x_placeholder__mutmut_72(platform: str) -> PlatformStats:
    """Last-resort stats so rendering never crashes."""
    defaults = {
        "xbox": PlatformStats(
            platform="xbox",
            username="Gamer",
            headline_value=0,
            headline_label="Gamerscore",
            substats=[SubStat("TA", 0)],
        ),
        "psn": PlatformStats(
            platform="psn",
            username="Player",
            headline_value="0 Platinums",
            headline_label="Trophies",
            substats=[
                SubStat("platinum", 0),
                SubStat("gold", 0),
                SubStat("SILVER", 0),
                SubStat("bronze", 0),
            ],
        ),
        "retroachievements": PlatformStats(
            platform="retroachievements",
            username="RetroUser",
            headline_value=0,
            headline_label="Hardcore Points",
            substats=[
                SubStat("RR", 0.0),
                SubStat("B", 0),
                SubStat("M", 0),
            ],
            extra_fields={
                "BeatenHardcoreAwardsCount": 0,
                "CompletionAwardsCount": 0,
                "MasteryAwardsCount": 0,
            },
        ),
    }
    return defaults.get(platform, PlatformStats(platform=platform))


def x_placeholder__mutmut_73(platform: str) -> PlatformStats:
    """Last-resort stats so rendering never crashes."""
    defaults = {
        "xbox": PlatformStats(
            platform="xbox",
            username="Gamer",
            headline_value=0,
            headline_label="Gamerscore",
            substats=[SubStat("TA", 0)],
        ),
        "psn": PlatformStats(
            platform="psn",
            username="Player",
            headline_value="0 Platinums",
            headline_label="Trophies",
            substats=[
                SubStat("platinum", 0),
                SubStat("gold", 0),
                SubStat("silver", 1),
                SubStat("bronze", 0),
            ],
        ),
        "retroachievements": PlatformStats(
            platform="retroachievements",
            username="RetroUser",
            headline_value=0,
            headline_label="Hardcore Points",
            substats=[
                SubStat("RR", 0.0),
                SubStat("B", 0),
                SubStat("M", 0),
            ],
            extra_fields={
                "BeatenHardcoreAwardsCount": 0,
                "CompletionAwardsCount": 0,
                "MasteryAwardsCount": 0,
            },
        ),
    }
    return defaults.get(platform, PlatformStats(platform=platform))


def x_placeholder__mutmut_74(platform: str) -> PlatformStats:
    """Last-resort stats so rendering never crashes."""
    defaults = {
        "xbox": PlatformStats(
            platform="xbox",
            username="Gamer",
            headline_value=0,
            headline_label="Gamerscore",
            substats=[SubStat("TA", 0)],
        ),
        "psn": PlatformStats(
            platform="psn",
            username="Player",
            headline_value="0 Platinums",
            headline_label="Trophies",
            substats=[
                SubStat("platinum", 0),
                SubStat("gold", 0),
                SubStat("silver", 0),
                SubStat(None, 0),
            ],
        ),
        "retroachievements": PlatformStats(
            platform="retroachievements",
            username="RetroUser",
            headline_value=0,
            headline_label="Hardcore Points",
            substats=[
                SubStat("RR", 0.0),
                SubStat("B", 0),
                SubStat("M", 0),
            ],
            extra_fields={
                "BeatenHardcoreAwardsCount": 0,
                "CompletionAwardsCount": 0,
                "MasteryAwardsCount": 0,
            },
        ),
    }
    return defaults.get(platform, PlatformStats(platform=platform))


def x_placeholder__mutmut_75(platform: str) -> PlatformStats:
    """Last-resort stats so rendering never crashes."""
    defaults = {
        "xbox": PlatformStats(
            platform="xbox",
            username="Gamer",
            headline_value=0,
            headline_label="Gamerscore",
            substats=[SubStat("TA", 0)],
        ),
        "psn": PlatformStats(
            platform="psn",
            username="Player",
            headline_value="0 Platinums",
            headline_label="Trophies",
            substats=[
                SubStat("platinum", 0),
                SubStat("gold", 0),
                SubStat("silver", 0),
                SubStat("bronze", None),
            ],
        ),
        "retroachievements": PlatformStats(
            platform="retroachievements",
            username="RetroUser",
            headline_value=0,
            headline_label="Hardcore Points",
            substats=[
                SubStat("RR", 0.0),
                SubStat("B", 0),
                SubStat("M", 0),
            ],
            extra_fields={
                "BeatenHardcoreAwardsCount": 0,
                "CompletionAwardsCount": 0,
                "MasteryAwardsCount": 0,
            },
        ),
    }
    return defaults.get(platform, PlatformStats(platform=platform))


def x_placeholder__mutmut_76(platform: str) -> PlatformStats:
    """Last-resort stats so rendering never crashes."""
    defaults = {
        "xbox": PlatformStats(
            platform="xbox",
            username="Gamer",
            headline_value=0,
            headline_label="Gamerscore",
            substats=[SubStat("TA", 0)],
        ),
        "psn": PlatformStats(
            platform="psn",
            username="Player",
            headline_value="0 Platinums",
            headline_label="Trophies",
            substats=[
                SubStat("platinum", 0),
                SubStat("gold", 0),
                SubStat("silver", 0),
                SubStat(0),
            ],
        ),
        "retroachievements": PlatformStats(
            platform="retroachievements",
            username="RetroUser",
            headline_value=0,
            headline_label="Hardcore Points",
            substats=[
                SubStat("RR", 0.0),
                SubStat("B", 0),
                SubStat("M", 0),
            ],
            extra_fields={
                "BeatenHardcoreAwardsCount": 0,
                "CompletionAwardsCount": 0,
                "MasteryAwardsCount": 0,
            },
        ),
    }
    return defaults.get(platform, PlatformStats(platform=platform))


def x_placeholder__mutmut_77(platform: str) -> PlatformStats:
    """Last-resort stats so rendering never crashes."""
    defaults = {
        "xbox": PlatformStats(
            platform="xbox",
            username="Gamer",
            headline_value=0,
            headline_label="Gamerscore",
            substats=[SubStat("TA", 0)],
        ),
        "psn": PlatformStats(
            platform="psn",
            username="Player",
            headline_value="0 Platinums",
            headline_label="Trophies",
            substats=[
                SubStat("platinum", 0),
                SubStat("gold", 0),
                SubStat("silver", 0),
                SubStat("bronze", ),
            ],
        ),
        "retroachievements": PlatformStats(
            platform="retroachievements",
            username="RetroUser",
            headline_value=0,
            headline_label="Hardcore Points",
            substats=[
                SubStat("RR", 0.0),
                SubStat("B", 0),
                SubStat("M", 0),
            ],
            extra_fields={
                "BeatenHardcoreAwardsCount": 0,
                "CompletionAwardsCount": 0,
                "MasteryAwardsCount": 0,
            },
        ),
    }
    return defaults.get(platform, PlatformStats(platform=platform))


def x_placeholder__mutmut_78(platform: str) -> PlatformStats:
    """Last-resort stats so rendering never crashes."""
    defaults = {
        "xbox": PlatformStats(
            platform="xbox",
            username="Gamer",
            headline_value=0,
            headline_label="Gamerscore",
            substats=[SubStat("TA", 0)],
        ),
        "psn": PlatformStats(
            platform="psn",
            username="Player",
            headline_value="0 Platinums",
            headline_label="Trophies",
            substats=[
                SubStat("platinum", 0),
                SubStat("gold", 0),
                SubStat("silver", 0),
                SubStat("XXbronzeXX", 0),
            ],
        ),
        "retroachievements": PlatformStats(
            platform="retroachievements",
            username="RetroUser",
            headline_value=0,
            headline_label="Hardcore Points",
            substats=[
                SubStat("RR", 0.0),
                SubStat("B", 0),
                SubStat("M", 0),
            ],
            extra_fields={
                "BeatenHardcoreAwardsCount": 0,
                "CompletionAwardsCount": 0,
                "MasteryAwardsCount": 0,
            },
        ),
    }
    return defaults.get(platform, PlatformStats(platform=platform))


def x_placeholder__mutmut_79(platform: str) -> PlatformStats:
    """Last-resort stats so rendering never crashes."""
    defaults = {
        "xbox": PlatformStats(
            platform="xbox",
            username="Gamer",
            headline_value=0,
            headline_label="Gamerscore",
            substats=[SubStat("TA", 0)],
        ),
        "psn": PlatformStats(
            platform="psn",
            username="Player",
            headline_value="0 Platinums",
            headline_label="Trophies",
            substats=[
                SubStat("platinum", 0),
                SubStat("gold", 0),
                SubStat("silver", 0),
                SubStat("BRONZE", 0),
            ],
        ),
        "retroachievements": PlatformStats(
            platform="retroachievements",
            username="RetroUser",
            headline_value=0,
            headline_label="Hardcore Points",
            substats=[
                SubStat("RR", 0.0),
                SubStat("B", 0),
                SubStat("M", 0),
            ],
            extra_fields={
                "BeatenHardcoreAwardsCount": 0,
                "CompletionAwardsCount": 0,
                "MasteryAwardsCount": 0,
            },
        ),
    }
    return defaults.get(platform, PlatformStats(platform=platform))


def x_placeholder__mutmut_80(platform: str) -> PlatformStats:
    """Last-resort stats so rendering never crashes."""
    defaults = {
        "xbox": PlatformStats(
            platform="xbox",
            username="Gamer",
            headline_value=0,
            headline_label="Gamerscore",
            substats=[SubStat("TA", 0)],
        ),
        "psn": PlatformStats(
            platform="psn",
            username="Player",
            headline_value="0 Platinums",
            headline_label="Trophies",
            substats=[
                SubStat("platinum", 0),
                SubStat("gold", 0),
                SubStat("silver", 0),
                SubStat("bronze", 1),
            ],
        ),
        "retroachievements": PlatformStats(
            platform="retroachievements",
            username="RetroUser",
            headline_value=0,
            headline_label="Hardcore Points",
            substats=[
                SubStat("RR", 0.0),
                SubStat("B", 0),
                SubStat("M", 0),
            ],
            extra_fields={
                "BeatenHardcoreAwardsCount": 0,
                "CompletionAwardsCount": 0,
                "MasteryAwardsCount": 0,
            },
        ),
    }
    return defaults.get(platform, PlatformStats(platform=platform))


def x_placeholder__mutmut_81(platform: str) -> PlatformStats:
    """Last-resort stats so rendering never crashes."""
    defaults = {
        "xbox": PlatformStats(
            platform="xbox",
            username="Gamer",
            headline_value=0,
            headline_label="Gamerscore",
            substats=[SubStat("TA", 0)],
        ),
        "psn": PlatformStats(
            platform="psn",
            username="Player",
            headline_value="0 Platinums",
            headline_label="Trophies",
            substats=[
                SubStat("platinum", 0),
                SubStat("gold", 0),
                SubStat("silver", 0),
                SubStat("bronze", 0),
            ],
        ),
        "XXretroachievementsXX": PlatformStats(
            platform="retroachievements",
            username="RetroUser",
            headline_value=0,
            headline_label="Hardcore Points",
            substats=[
                SubStat("RR", 0.0),
                SubStat("B", 0),
                SubStat("M", 0),
            ],
            extra_fields={
                "BeatenHardcoreAwardsCount": 0,
                "CompletionAwardsCount": 0,
                "MasteryAwardsCount": 0,
            },
        ),
    }
    return defaults.get(platform, PlatformStats(platform=platform))


def x_placeholder__mutmut_82(platform: str) -> PlatformStats:
    """Last-resort stats so rendering never crashes."""
    defaults = {
        "xbox": PlatformStats(
            platform="xbox",
            username="Gamer",
            headline_value=0,
            headline_label="Gamerscore",
            substats=[SubStat("TA", 0)],
        ),
        "psn": PlatformStats(
            platform="psn",
            username="Player",
            headline_value="0 Platinums",
            headline_label="Trophies",
            substats=[
                SubStat("platinum", 0),
                SubStat("gold", 0),
                SubStat("silver", 0),
                SubStat("bronze", 0),
            ],
        ),
        "RETROACHIEVEMENTS": PlatformStats(
            platform="retroachievements",
            username="RetroUser",
            headline_value=0,
            headline_label="Hardcore Points",
            substats=[
                SubStat("RR", 0.0),
                SubStat("B", 0),
                SubStat("M", 0),
            ],
            extra_fields={
                "BeatenHardcoreAwardsCount": 0,
                "CompletionAwardsCount": 0,
                "MasteryAwardsCount": 0,
            },
        ),
    }
    return defaults.get(platform, PlatformStats(platform=platform))


def x_placeholder__mutmut_83(platform: str) -> PlatformStats:
    """Last-resort stats so rendering never crashes."""
    defaults = {
        "xbox": PlatformStats(
            platform="xbox",
            username="Gamer",
            headline_value=0,
            headline_label="Gamerscore",
            substats=[SubStat("TA", 0)],
        ),
        "psn": PlatformStats(
            platform="psn",
            username="Player",
            headline_value="0 Platinums",
            headline_label="Trophies",
            substats=[
                SubStat("platinum", 0),
                SubStat("gold", 0),
                SubStat("silver", 0),
                SubStat("bronze", 0),
            ],
        ),
        "retroachievements": PlatformStats(
            platform=None,
            username="RetroUser",
            headline_value=0,
            headline_label="Hardcore Points",
            substats=[
                SubStat("RR", 0.0),
                SubStat("B", 0),
                SubStat("M", 0),
            ],
            extra_fields={
                "BeatenHardcoreAwardsCount": 0,
                "CompletionAwardsCount": 0,
                "MasteryAwardsCount": 0,
            },
        ),
    }
    return defaults.get(platform, PlatformStats(platform=platform))


def x_placeholder__mutmut_84(platform: str) -> PlatformStats:
    """Last-resort stats so rendering never crashes."""
    defaults = {
        "xbox": PlatformStats(
            platform="xbox",
            username="Gamer",
            headline_value=0,
            headline_label="Gamerscore",
            substats=[SubStat("TA", 0)],
        ),
        "psn": PlatformStats(
            platform="psn",
            username="Player",
            headline_value="0 Platinums",
            headline_label="Trophies",
            substats=[
                SubStat("platinum", 0),
                SubStat("gold", 0),
                SubStat("silver", 0),
                SubStat("bronze", 0),
            ],
        ),
        "retroachievements": PlatformStats(
            platform="retroachievements",
            username=None,
            headline_value=0,
            headline_label="Hardcore Points",
            substats=[
                SubStat("RR", 0.0),
                SubStat("B", 0),
                SubStat("M", 0),
            ],
            extra_fields={
                "BeatenHardcoreAwardsCount": 0,
                "CompletionAwardsCount": 0,
                "MasteryAwardsCount": 0,
            },
        ),
    }
    return defaults.get(platform, PlatformStats(platform=platform))


def x_placeholder__mutmut_85(platform: str) -> PlatformStats:
    """Last-resort stats so rendering never crashes."""
    defaults = {
        "xbox": PlatformStats(
            platform="xbox",
            username="Gamer",
            headline_value=0,
            headline_label="Gamerscore",
            substats=[SubStat("TA", 0)],
        ),
        "psn": PlatformStats(
            platform="psn",
            username="Player",
            headline_value="0 Platinums",
            headline_label="Trophies",
            substats=[
                SubStat("platinum", 0),
                SubStat("gold", 0),
                SubStat("silver", 0),
                SubStat("bronze", 0),
            ],
        ),
        "retroachievements": PlatformStats(
            platform="retroachievements",
            username="RetroUser",
            headline_value=None,
            headline_label="Hardcore Points",
            substats=[
                SubStat("RR", 0.0),
                SubStat("B", 0),
                SubStat("M", 0),
            ],
            extra_fields={
                "BeatenHardcoreAwardsCount": 0,
                "CompletionAwardsCount": 0,
                "MasteryAwardsCount": 0,
            },
        ),
    }
    return defaults.get(platform, PlatformStats(platform=platform))


def x_placeholder__mutmut_86(platform: str) -> PlatformStats:
    """Last-resort stats so rendering never crashes."""
    defaults = {
        "xbox": PlatformStats(
            platform="xbox",
            username="Gamer",
            headline_value=0,
            headline_label="Gamerscore",
            substats=[SubStat("TA", 0)],
        ),
        "psn": PlatformStats(
            platform="psn",
            username="Player",
            headline_value="0 Platinums",
            headline_label="Trophies",
            substats=[
                SubStat("platinum", 0),
                SubStat("gold", 0),
                SubStat("silver", 0),
                SubStat("bronze", 0),
            ],
        ),
        "retroachievements": PlatformStats(
            platform="retroachievements",
            username="RetroUser",
            headline_value=0,
            headline_label=None,
            substats=[
                SubStat("RR", 0.0),
                SubStat("B", 0),
                SubStat("M", 0),
            ],
            extra_fields={
                "BeatenHardcoreAwardsCount": 0,
                "CompletionAwardsCount": 0,
                "MasteryAwardsCount": 0,
            },
        ),
    }
    return defaults.get(platform, PlatformStats(platform=platform))


def x_placeholder__mutmut_87(platform: str) -> PlatformStats:
    """Last-resort stats so rendering never crashes."""
    defaults = {
        "xbox": PlatformStats(
            platform="xbox",
            username="Gamer",
            headline_value=0,
            headline_label="Gamerscore",
            substats=[SubStat("TA", 0)],
        ),
        "psn": PlatformStats(
            platform="psn",
            username="Player",
            headline_value="0 Platinums",
            headline_label="Trophies",
            substats=[
                SubStat("platinum", 0),
                SubStat("gold", 0),
                SubStat("silver", 0),
                SubStat("bronze", 0),
            ],
        ),
        "retroachievements": PlatformStats(
            platform="retroachievements",
            username="RetroUser",
            headline_value=0,
            headline_label="Hardcore Points",
            substats=None,
            extra_fields={
                "BeatenHardcoreAwardsCount": 0,
                "CompletionAwardsCount": 0,
                "MasteryAwardsCount": 0,
            },
        ),
    }
    return defaults.get(platform, PlatformStats(platform=platform))


def x_placeholder__mutmut_88(platform: str) -> PlatformStats:
    """Last-resort stats so rendering never crashes."""
    defaults = {
        "xbox": PlatformStats(
            platform="xbox",
            username="Gamer",
            headline_value=0,
            headline_label="Gamerscore",
            substats=[SubStat("TA", 0)],
        ),
        "psn": PlatformStats(
            platform="psn",
            username="Player",
            headline_value="0 Platinums",
            headline_label="Trophies",
            substats=[
                SubStat("platinum", 0),
                SubStat("gold", 0),
                SubStat("silver", 0),
                SubStat("bronze", 0),
            ],
        ),
        "retroachievements": PlatformStats(
            platform="retroachievements",
            username="RetroUser",
            headline_value=0,
            headline_label="Hardcore Points",
            substats=[
                SubStat("RR", 0.0),
                SubStat("B", 0),
                SubStat("M", 0),
            ],
            extra_fields=None,
        ),
    }
    return defaults.get(platform, PlatformStats(platform=platform))


def x_placeholder__mutmut_89(platform: str) -> PlatformStats:
    """Last-resort stats so rendering never crashes."""
    defaults = {
        "xbox": PlatformStats(
            platform="xbox",
            username="Gamer",
            headline_value=0,
            headline_label="Gamerscore",
            substats=[SubStat("TA", 0)],
        ),
        "psn": PlatformStats(
            platform="psn",
            username="Player",
            headline_value="0 Platinums",
            headline_label="Trophies",
            substats=[
                SubStat("platinum", 0),
                SubStat("gold", 0),
                SubStat("silver", 0),
                SubStat("bronze", 0),
            ],
        ),
        "retroachievements": PlatformStats(
            username="RetroUser",
            headline_value=0,
            headline_label="Hardcore Points",
            substats=[
                SubStat("RR", 0.0),
                SubStat("B", 0),
                SubStat("M", 0),
            ],
            extra_fields={
                "BeatenHardcoreAwardsCount": 0,
                "CompletionAwardsCount": 0,
                "MasteryAwardsCount": 0,
            },
        ),
    }
    return defaults.get(platform, PlatformStats(platform=platform))


def x_placeholder__mutmut_90(platform: str) -> PlatformStats:
    """Last-resort stats so rendering never crashes."""
    defaults = {
        "xbox": PlatformStats(
            platform="xbox",
            username="Gamer",
            headline_value=0,
            headline_label="Gamerscore",
            substats=[SubStat("TA", 0)],
        ),
        "psn": PlatformStats(
            platform="psn",
            username="Player",
            headline_value="0 Platinums",
            headline_label="Trophies",
            substats=[
                SubStat("platinum", 0),
                SubStat("gold", 0),
                SubStat("silver", 0),
                SubStat("bronze", 0),
            ],
        ),
        "retroachievements": PlatformStats(
            platform="retroachievements",
            headline_value=0,
            headline_label="Hardcore Points",
            substats=[
                SubStat("RR", 0.0),
                SubStat("B", 0),
                SubStat("M", 0),
            ],
            extra_fields={
                "BeatenHardcoreAwardsCount": 0,
                "CompletionAwardsCount": 0,
                "MasteryAwardsCount": 0,
            },
        ),
    }
    return defaults.get(platform, PlatformStats(platform=platform))


def x_placeholder__mutmut_91(platform: str) -> PlatformStats:
    """Last-resort stats so rendering never crashes."""
    defaults = {
        "xbox": PlatformStats(
            platform="xbox",
            username="Gamer",
            headline_value=0,
            headline_label="Gamerscore",
            substats=[SubStat("TA", 0)],
        ),
        "psn": PlatformStats(
            platform="psn",
            username="Player",
            headline_value="0 Platinums",
            headline_label="Trophies",
            substats=[
                SubStat("platinum", 0),
                SubStat("gold", 0),
                SubStat("silver", 0),
                SubStat("bronze", 0),
            ],
        ),
        "retroachievements": PlatformStats(
            platform="retroachievements",
            username="RetroUser",
            headline_label="Hardcore Points",
            substats=[
                SubStat("RR", 0.0),
                SubStat("B", 0),
                SubStat("M", 0),
            ],
            extra_fields={
                "BeatenHardcoreAwardsCount": 0,
                "CompletionAwardsCount": 0,
                "MasteryAwardsCount": 0,
            },
        ),
    }
    return defaults.get(platform, PlatformStats(platform=platform))


def x_placeholder__mutmut_92(platform: str) -> PlatformStats:
    """Last-resort stats so rendering never crashes."""
    defaults = {
        "xbox": PlatformStats(
            platform="xbox",
            username="Gamer",
            headline_value=0,
            headline_label="Gamerscore",
            substats=[SubStat("TA", 0)],
        ),
        "psn": PlatformStats(
            platform="psn",
            username="Player",
            headline_value="0 Platinums",
            headline_label="Trophies",
            substats=[
                SubStat("platinum", 0),
                SubStat("gold", 0),
                SubStat("silver", 0),
                SubStat("bronze", 0),
            ],
        ),
        "retroachievements": PlatformStats(
            platform="retroachievements",
            username="RetroUser",
            headline_value=0,
            substats=[
                SubStat("RR", 0.0),
                SubStat("B", 0),
                SubStat("M", 0),
            ],
            extra_fields={
                "BeatenHardcoreAwardsCount": 0,
                "CompletionAwardsCount": 0,
                "MasteryAwardsCount": 0,
            },
        ),
    }
    return defaults.get(platform, PlatformStats(platform=platform))


def x_placeholder__mutmut_93(platform: str) -> PlatformStats:
    """Last-resort stats so rendering never crashes."""
    defaults = {
        "xbox": PlatformStats(
            platform="xbox",
            username="Gamer",
            headline_value=0,
            headline_label="Gamerscore",
            substats=[SubStat("TA", 0)],
        ),
        "psn": PlatformStats(
            platform="psn",
            username="Player",
            headline_value="0 Platinums",
            headline_label="Trophies",
            substats=[
                SubStat("platinum", 0),
                SubStat("gold", 0),
                SubStat("silver", 0),
                SubStat("bronze", 0),
            ],
        ),
        "retroachievements": PlatformStats(
            platform="retroachievements",
            username="RetroUser",
            headline_value=0,
            headline_label="Hardcore Points",
            extra_fields={
                "BeatenHardcoreAwardsCount": 0,
                "CompletionAwardsCount": 0,
                "MasteryAwardsCount": 0,
            },
        ),
    }
    return defaults.get(platform, PlatformStats(platform=platform))


def x_placeholder__mutmut_94(platform: str) -> PlatformStats:
    """Last-resort stats so rendering never crashes."""
    defaults = {
        "xbox": PlatformStats(
            platform="xbox",
            username="Gamer",
            headline_value=0,
            headline_label="Gamerscore",
            substats=[SubStat("TA", 0)],
        ),
        "psn": PlatformStats(
            platform="psn",
            username="Player",
            headline_value="0 Platinums",
            headline_label="Trophies",
            substats=[
                SubStat("platinum", 0),
                SubStat("gold", 0),
                SubStat("silver", 0),
                SubStat("bronze", 0),
            ],
        ),
        "retroachievements": PlatformStats(
            platform="retroachievements",
            username="RetroUser",
            headline_value=0,
            headline_label="Hardcore Points",
            substats=[
                SubStat("RR", 0.0),
                SubStat("B", 0),
                SubStat("M", 0),
            ],
            ),
    }
    return defaults.get(platform, PlatformStats(platform=platform))


def x_placeholder__mutmut_95(platform: str) -> PlatformStats:
    """Last-resort stats so rendering never crashes."""
    defaults = {
        "xbox": PlatformStats(
            platform="xbox",
            username="Gamer",
            headline_value=0,
            headline_label="Gamerscore",
            substats=[SubStat("TA", 0)],
        ),
        "psn": PlatformStats(
            platform="psn",
            username="Player",
            headline_value="0 Platinums",
            headline_label="Trophies",
            substats=[
                SubStat("platinum", 0),
                SubStat("gold", 0),
                SubStat("silver", 0),
                SubStat("bronze", 0),
            ],
        ),
        "retroachievements": PlatformStats(
            platform="XXretroachievementsXX",
            username="RetroUser",
            headline_value=0,
            headline_label="Hardcore Points",
            substats=[
                SubStat("RR", 0.0),
                SubStat("B", 0),
                SubStat("M", 0),
            ],
            extra_fields={
                "BeatenHardcoreAwardsCount": 0,
                "CompletionAwardsCount": 0,
                "MasteryAwardsCount": 0,
            },
        ),
    }
    return defaults.get(platform, PlatformStats(platform=platform))


def x_placeholder__mutmut_96(platform: str) -> PlatformStats:
    """Last-resort stats so rendering never crashes."""
    defaults = {
        "xbox": PlatformStats(
            platform="xbox",
            username="Gamer",
            headline_value=0,
            headline_label="Gamerscore",
            substats=[SubStat("TA", 0)],
        ),
        "psn": PlatformStats(
            platform="psn",
            username="Player",
            headline_value="0 Platinums",
            headline_label="Trophies",
            substats=[
                SubStat("platinum", 0),
                SubStat("gold", 0),
                SubStat("silver", 0),
                SubStat("bronze", 0),
            ],
        ),
        "retroachievements": PlatformStats(
            platform="RETROACHIEVEMENTS",
            username="RetroUser",
            headline_value=0,
            headline_label="Hardcore Points",
            substats=[
                SubStat("RR", 0.0),
                SubStat("B", 0),
                SubStat("M", 0),
            ],
            extra_fields={
                "BeatenHardcoreAwardsCount": 0,
                "CompletionAwardsCount": 0,
                "MasteryAwardsCount": 0,
            },
        ),
    }
    return defaults.get(platform, PlatformStats(platform=platform))


def x_placeholder__mutmut_97(platform: str) -> PlatformStats:
    """Last-resort stats so rendering never crashes."""
    defaults = {
        "xbox": PlatformStats(
            platform="xbox",
            username="Gamer",
            headline_value=0,
            headline_label="Gamerscore",
            substats=[SubStat("TA", 0)],
        ),
        "psn": PlatformStats(
            platform="psn",
            username="Player",
            headline_value="0 Platinums",
            headline_label="Trophies",
            substats=[
                SubStat("platinum", 0),
                SubStat("gold", 0),
                SubStat("silver", 0),
                SubStat("bronze", 0),
            ],
        ),
        "retroachievements": PlatformStats(
            platform="retroachievements",
            username="XXRetroUserXX",
            headline_value=0,
            headline_label="Hardcore Points",
            substats=[
                SubStat("RR", 0.0),
                SubStat("B", 0),
                SubStat("M", 0),
            ],
            extra_fields={
                "BeatenHardcoreAwardsCount": 0,
                "CompletionAwardsCount": 0,
                "MasteryAwardsCount": 0,
            },
        ),
    }
    return defaults.get(platform, PlatformStats(platform=platform))


def x_placeholder__mutmut_98(platform: str) -> PlatformStats:
    """Last-resort stats so rendering never crashes."""
    defaults = {
        "xbox": PlatformStats(
            platform="xbox",
            username="Gamer",
            headline_value=0,
            headline_label="Gamerscore",
            substats=[SubStat("TA", 0)],
        ),
        "psn": PlatformStats(
            platform="psn",
            username="Player",
            headline_value="0 Platinums",
            headline_label="Trophies",
            substats=[
                SubStat("platinum", 0),
                SubStat("gold", 0),
                SubStat("silver", 0),
                SubStat("bronze", 0),
            ],
        ),
        "retroachievements": PlatformStats(
            platform="retroachievements",
            username="retrouser",
            headline_value=0,
            headline_label="Hardcore Points",
            substats=[
                SubStat("RR", 0.0),
                SubStat("B", 0),
                SubStat("M", 0),
            ],
            extra_fields={
                "BeatenHardcoreAwardsCount": 0,
                "CompletionAwardsCount": 0,
                "MasteryAwardsCount": 0,
            },
        ),
    }
    return defaults.get(platform, PlatformStats(platform=platform))


def x_placeholder__mutmut_99(platform: str) -> PlatformStats:
    """Last-resort stats so rendering never crashes."""
    defaults = {
        "xbox": PlatformStats(
            platform="xbox",
            username="Gamer",
            headline_value=0,
            headline_label="Gamerscore",
            substats=[SubStat("TA", 0)],
        ),
        "psn": PlatformStats(
            platform="psn",
            username="Player",
            headline_value="0 Platinums",
            headline_label="Trophies",
            substats=[
                SubStat("platinum", 0),
                SubStat("gold", 0),
                SubStat("silver", 0),
                SubStat("bronze", 0),
            ],
        ),
        "retroachievements": PlatformStats(
            platform="retroachievements",
            username="RETROUSER",
            headline_value=0,
            headline_label="Hardcore Points",
            substats=[
                SubStat("RR", 0.0),
                SubStat("B", 0),
                SubStat("M", 0),
            ],
            extra_fields={
                "BeatenHardcoreAwardsCount": 0,
                "CompletionAwardsCount": 0,
                "MasteryAwardsCount": 0,
            },
        ),
    }
    return defaults.get(platform, PlatformStats(platform=platform))


def x_placeholder__mutmut_100(platform: str) -> PlatformStats:
    """Last-resort stats so rendering never crashes."""
    defaults = {
        "xbox": PlatformStats(
            platform="xbox",
            username="Gamer",
            headline_value=0,
            headline_label="Gamerscore",
            substats=[SubStat("TA", 0)],
        ),
        "psn": PlatformStats(
            platform="psn",
            username="Player",
            headline_value="0 Platinums",
            headline_label="Trophies",
            substats=[
                SubStat("platinum", 0),
                SubStat("gold", 0),
                SubStat("silver", 0),
                SubStat("bronze", 0),
            ],
        ),
        "retroachievements": PlatformStats(
            platform="retroachievements",
            username="RetroUser",
            headline_value=1,
            headline_label="Hardcore Points",
            substats=[
                SubStat("RR", 0.0),
                SubStat("B", 0),
                SubStat("M", 0),
            ],
            extra_fields={
                "BeatenHardcoreAwardsCount": 0,
                "CompletionAwardsCount": 0,
                "MasteryAwardsCount": 0,
            },
        ),
    }
    return defaults.get(platform, PlatformStats(platform=platform))


def x_placeholder__mutmut_101(platform: str) -> PlatformStats:
    """Last-resort stats so rendering never crashes."""
    defaults = {
        "xbox": PlatformStats(
            platform="xbox",
            username="Gamer",
            headline_value=0,
            headline_label="Gamerscore",
            substats=[SubStat("TA", 0)],
        ),
        "psn": PlatformStats(
            platform="psn",
            username="Player",
            headline_value="0 Platinums",
            headline_label="Trophies",
            substats=[
                SubStat("platinum", 0),
                SubStat("gold", 0),
                SubStat("silver", 0),
                SubStat("bronze", 0),
            ],
        ),
        "retroachievements": PlatformStats(
            platform="retroachievements",
            username="RetroUser",
            headline_value=0,
            headline_label="XXHardcore PointsXX",
            substats=[
                SubStat("RR", 0.0),
                SubStat("B", 0),
                SubStat("M", 0),
            ],
            extra_fields={
                "BeatenHardcoreAwardsCount": 0,
                "CompletionAwardsCount": 0,
                "MasteryAwardsCount": 0,
            },
        ),
    }
    return defaults.get(platform, PlatformStats(platform=platform))


def x_placeholder__mutmut_102(platform: str) -> PlatformStats:
    """Last-resort stats so rendering never crashes."""
    defaults = {
        "xbox": PlatformStats(
            platform="xbox",
            username="Gamer",
            headline_value=0,
            headline_label="Gamerscore",
            substats=[SubStat("TA", 0)],
        ),
        "psn": PlatformStats(
            platform="psn",
            username="Player",
            headline_value="0 Platinums",
            headline_label="Trophies",
            substats=[
                SubStat("platinum", 0),
                SubStat("gold", 0),
                SubStat("silver", 0),
                SubStat("bronze", 0),
            ],
        ),
        "retroachievements": PlatformStats(
            platform="retroachievements",
            username="RetroUser",
            headline_value=0,
            headline_label="hardcore points",
            substats=[
                SubStat("RR", 0.0),
                SubStat("B", 0),
                SubStat("M", 0),
            ],
            extra_fields={
                "BeatenHardcoreAwardsCount": 0,
                "CompletionAwardsCount": 0,
                "MasteryAwardsCount": 0,
            },
        ),
    }
    return defaults.get(platform, PlatformStats(platform=platform))


def x_placeholder__mutmut_103(platform: str) -> PlatformStats:
    """Last-resort stats so rendering never crashes."""
    defaults = {
        "xbox": PlatformStats(
            platform="xbox",
            username="Gamer",
            headline_value=0,
            headline_label="Gamerscore",
            substats=[SubStat("TA", 0)],
        ),
        "psn": PlatformStats(
            platform="psn",
            username="Player",
            headline_value="0 Platinums",
            headline_label="Trophies",
            substats=[
                SubStat("platinum", 0),
                SubStat("gold", 0),
                SubStat("silver", 0),
                SubStat("bronze", 0),
            ],
        ),
        "retroachievements": PlatformStats(
            platform="retroachievements",
            username="RetroUser",
            headline_value=0,
            headline_label="HARDCORE POINTS",
            substats=[
                SubStat("RR", 0.0),
                SubStat("B", 0),
                SubStat("M", 0),
            ],
            extra_fields={
                "BeatenHardcoreAwardsCount": 0,
                "CompletionAwardsCount": 0,
                "MasteryAwardsCount": 0,
            },
        ),
    }
    return defaults.get(platform, PlatformStats(platform=platform))


def x_placeholder__mutmut_104(platform: str) -> PlatformStats:
    """Last-resort stats so rendering never crashes."""
    defaults = {
        "xbox": PlatformStats(
            platform="xbox",
            username="Gamer",
            headline_value=0,
            headline_label="Gamerscore",
            substats=[SubStat("TA", 0)],
        ),
        "psn": PlatformStats(
            platform="psn",
            username="Player",
            headline_value="0 Platinums",
            headline_label="Trophies",
            substats=[
                SubStat("platinum", 0),
                SubStat("gold", 0),
                SubStat("silver", 0),
                SubStat("bronze", 0),
            ],
        ),
        "retroachievements": PlatformStats(
            platform="retroachievements",
            username="RetroUser",
            headline_value=0,
            headline_label="Hardcore Points",
            substats=[
                SubStat(None, 0.0),
                SubStat("B", 0),
                SubStat("M", 0),
            ],
            extra_fields={
                "BeatenHardcoreAwardsCount": 0,
                "CompletionAwardsCount": 0,
                "MasteryAwardsCount": 0,
            },
        ),
    }
    return defaults.get(platform, PlatformStats(platform=platform))


def x_placeholder__mutmut_105(platform: str) -> PlatformStats:
    """Last-resort stats so rendering never crashes."""
    defaults = {
        "xbox": PlatformStats(
            platform="xbox",
            username="Gamer",
            headline_value=0,
            headline_label="Gamerscore",
            substats=[SubStat("TA", 0)],
        ),
        "psn": PlatformStats(
            platform="psn",
            username="Player",
            headline_value="0 Platinums",
            headline_label="Trophies",
            substats=[
                SubStat("platinum", 0),
                SubStat("gold", 0),
                SubStat("silver", 0),
                SubStat("bronze", 0),
            ],
        ),
        "retroachievements": PlatformStats(
            platform="retroachievements",
            username="RetroUser",
            headline_value=0,
            headline_label="Hardcore Points",
            substats=[
                SubStat("RR", None),
                SubStat("B", 0),
                SubStat("M", 0),
            ],
            extra_fields={
                "BeatenHardcoreAwardsCount": 0,
                "CompletionAwardsCount": 0,
                "MasteryAwardsCount": 0,
            },
        ),
    }
    return defaults.get(platform, PlatformStats(platform=platform))


def x_placeholder__mutmut_106(platform: str) -> PlatformStats:
    """Last-resort stats so rendering never crashes."""
    defaults = {
        "xbox": PlatformStats(
            platform="xbox",
            username="Gamer",
            headline_value=0,
            headline_label="Gamerscore",
            substats=[SubStat("TA", 0)],
        ),
        "psn": PlatformStats(
            platform="psn",
            username="Player",
            headline_value="0 Platinums",
            headline_label="Trophies",
            substats=[
                SubStat("platinum", 0),
                SubStat("gold", 0),
                SubStat("silver", 0),
                SubStat("bronze", 0),
            ],
        ),
        "retroachievements": PlatformStats(
            platform="retroachievements",
            username="RetroUser",
            headline_value=0,
            headline_label="Hardcore Points",
            substats=[
                SubStat(0.0),
                SubStat("B", 0),
                SubStat("M", 0),
            ],
            extra_fields={
                "BeatenHardcoreAwardsCount": 0,
                "CompletionAwardsCount": 0,
                "MasteryAwardsCount": 0,
            },
        ),
    }
    return defaults.get(platform, PlatformStats(platform=platform))


def x_placeholder__mutmut_107(platform: str) -> PlatformStats:
    """Last-resort stats so rendering never crashes."""
    defaults = {
        "xbox": PlatformStats(
            platform="xbox",
            username="Gamer",
            headline_value=0,
            headline_label="Gamerscore",
            substats=[SubStat("TA", 0)],
        ),
        "psn": PlatformStats(
            platform="psn",
            username="Player",
            headline_value="0 Platinums",
            headline_label="Trophies",
            substats=[
                SubStat("platinum", 0),
                SubStat("gold", 0),
                SubStat("silver", 0),
                SubStat("bronze", 0),
            ],
        ),
        "retroachievements": PlatformStats(
            platform="retroachievements",
            username="RetroUser",
            headline_value=0,
            headline_label="Hardcore Points",
            substats=[
                SubStat("RR", ),
                SubStat("B", 0),
                SubStat("M", 0),
            ],
            extra_fields={
                "BeatenHardcoreAwardsCount": 0,
                "CompletionAwardsCount": 0,
                "MasteryAwardsCount": 0,
            },
        ),
    }
    return defaults.get(platform, PlatformStats(platform=platform))


def x_placeholder__mutmut_108(platform: str) -> PlatformStats:
    """Last-resort stats so rendering never crashes."""
    defaults = {
        "xbox": PlatformStats(
            platform="xbox",
            username="Gamer",
            headline_value=0,
            headline_label="Gamerscore",
            substats=[SubStat("TA", 0)],
        ),
        "psn": PlatformStats(
            platform="psn",
            username="Player",
            headline_value="0 Platinums",
            headline_label="Trophies",
            substats=[
                SubStat("platinum", 0),
                SubStat("gold", 0),
                SubStat("silver", 0),
                SubStat("bronze", 0),
            ],
        ),
        "retroachievements": PlatformStats(
            platform="retroachievements",
            username="RetroUser",
            headline_value=0,
            headline_label="Hardcore Points",
            substats=[
                SubStat("XXRRXX", 0.0),
                SubStat("B", 0),
                SubStat("M", 0),
            ],
            extra_fields={
                "BeatenHardcoreAwardsCount": 0,
                "CompletionAwardsCount": 0,
                "MasteryAwardsCount": 0,
            },
        ),
    }
    return defaults.get(platform, PlatformStats(platform=platform))


def x_placeholder__mutmut_109(platform: str) -> PlatformStats:
    """Last-resort stats so rendering never crashes."""
    defaults = {
        "xbox": PlatformStats(
            platform="xbox",
            username="Gamer",
            headline_value=0,
            headline_label="Gamerscore",
            substats=[SubStat("TA", 0)],
        ),
        "psn": PlatformStats(
            platform="psn",
            username="Player",
            headline_value="0 Platinums",
            headline_label="Trophies",
            substats=[
                SubStat("platinum", 0),
                SubStat("gold", 0),
                SubStat("silver", 0),
                SubStat("bronze", 0),
            ],
        ),
        "retroachievements": PlatformStats(
            platform="retroachievements",
            username="RetroUser",
            headline_value=0,
            headline_label="Hardcore Points",
            substats=[
                SubStat("rr", 0.0),
                SubStat("B", 0),
                SubStat("M", 0),
            ],
            extra_fields={
                "BeatenHardcoreAwardsCount": 0,
                "CompletionAwardsCount": 0,
                "MasteryAwardsCount": 0,
            },
        ),
    }
    return defaults.get(platform, PlatformStats(platform=platform))


def x_placeholder__mutmut_110(platform: str) -> PlatformStats:
    """Last-resort stats so rendering never crashes."""
    defaults = {
        "xbox": PlatformStats(
            platform="xbox",
            username="Gamer",
            headline_value=0,
            headline_label="Gamerscore",
            substats=[SubStat("TA", 0)],
        ),
        "psn": PlatformStats(
            platform="psn",
            username="Player",
            headline_value="0 Platinums",
            headline_label="Trophies",
            substats=[
                SubStat("platinum", 0),
                SubStat("gold", 0),
                SubStat("silver", 0),
                SubStat("bronze", 0),
            ],
        ),
        "retroachievements": PlatformStats(
            platform="retroachievements",
            username="RetroUser",
            headline_value=0,
            headline_label="Hardcore Points",
            substats=[
                SubStat("RR", 1.0),
                SubStat("B", 0),
                SubStat("M", 0),
            ],
            extra_fields={
                "BeatenHardcoreAwardsCount": 0,
                "CompletionAwardsCount": 0,
                "MasteryAwardsCount": 0,
            },
        ),
    }
    return defaults.get(platform, PlatformStats(platform=platform))


def x_placeholder__mutmut_111(platform: str) -> PlatformStats:
    """Last-resort stats so rendering never crashes."""
    defaults = {
        "xbox": PlatformStats(
            platform="xbox",
            username="Gamer",
            headline_value=0,
            headline_label="Gamerscore",
            substats=[SubStat("TA", 0)],
        ),
        "psn": PlatformStats(
            platform="psn",
            username="Player",
            headline_value="0 Platinums",
            headline_label="Trophies",
            substats=[
                SubStat("platinum", 0),
                SubStat("gold", 0),
                SubStat("silver", 0),
                SubStat("bronze", 0),
            ],
        ),
        "retroachievements": PlatformStats(
            platform="retroachievements",
            username="RetroUser",
            headline_value=0,
            headline_label="Hardcore Points",
            substats=[
                SubStat("RR", 0.0),
                SubStat(None, 0),
                SubStat("M", 0),
            ],
            extra_fields={
                "BeatenHardcoreAwardsCount": 0,
                "CompletionAwardsCount": 0,
                "MasteryAwardsCount": 0,
            },
        ),
    }
    return defaults.get(platform, PlatformStats(platform=platform))


def x_placeholder__mutmut_112(platform: str) -> PlatformStats:
    """Last-resort stats so rendering never crashes."""
    defaults = {
        "xbox": PlatformStats(
            platform="xbox",
            username="Gamer",
            headline_value=0,
            headline_label="Gamerscore",
            substats=[SubStat("TA", 0)],
        ),
        "psn": PlatformStats(
            platform="psn",
            username="Player",
            headline_value="0 Platinums",
            headline_label="Trophies",
            substats=[
                SubStat("platinum", 0),
                SubStat("gold", 0),
                SubStat("silver", 0),
                SubStat("bronze", 0),
            ],
        ),
        "retroachievements": PlatformStats(
            platform="retroachievements",
            username="RetroUser",
            headline_value=0,
            headline_label="Hardcore Points",
            substats=[
                SubStat("RR", 0.0),
                SubStat("B", None),
                SubStat("M", 0),
            ],
            extra_fields={
                "BeatenHardcoreAwardsCount": 0,
                "CompletionAwardsCount": 0,
                "MasteryAwardsCount": 0,
            },
        ),
    }
    return defaults.get(platform, PlatformStats(platform=platform))


def x_placeholder__mutmut_113(platform: str) -> PlatformStats:
    """Last-resort stats so rendering never crashes."""
    defaults = {
        "xbox": PlatformStats(
            platform="xbox",
            username="Gamer",
            headline_value=0,
            headline_label="Gamerscore",
            substats=[SubStat("TA", 0)],
        ),
        "psn": PlatformStats(
            platform="psn",
            username="Player",
            headline_value="0 Platinums",
            headline_label="Trophies",
            substats=[
                SubStat("platinum", 0),
                SubStat("gold", 0),
                SubStat("silver", 0),
                SubStat("bronze", 0),
            ],
        ),
        "retroachievements": PlatformStats(
            platform="retroachievements",
            username="RetroUser",
            headline_value=0,
            headline_label="Hardcore Points",
            substats=[
                SubStat("RR", 0.0),
                SubStat(0),
                SubStat("M", 0),
            ],
            extra_fields={
                "BeatenHardcoreAwardsCount": 0,
                "CompletionAwardsCount": 0,
                "MasteryAwardsCount": 0,
            },
        ),
    }
    return defaults.get(platform, PlatformStats(platform=platform))


def x_placeholder__mutmut_114(platform: str) -> PlatformStats:
    """Last-resort stats so rendering never crashes."""
    defaults = {
        "xbox": PlatformStats(
            platform="xbox",
            username="Gamer",
            headline_value=0,
            headline_label="Gamerscore",
            substats=[SubStat("TA", 0)],
        ),
        "psn": PlatformStats(
            platform="psn",
            username="Player",
            headline_value="0 Platinums",
            headline_label="Trophies",
            substats=[
                SubStat("platinum", 0),
                SubStat("gold", 0),
                SubStat("silver", 0),
                SubStat("bronze", 0),
            ],
        ),
        "retroachievements": PlatformStats(
            platform="retroachievements",
            username="RetroUser",
            headline_value=0,
            headline_label="Hardcore Points",
            substats=[
                SubStat("RR", 0.0),
                SubStat("B", ),
                SubStat("M", 0),
            ],
            extra_fields={
                "BeatenHardcoreAwardsCount": 0,
                "CompletionAwardsCount": 0,
                "MasteryAwardsCount": 0,
            },
        ),
    }
    return defaults.get(platform, PlatformStats(platform=platform))


def x_placeholder__mutmut_115(platform: str) -> PlatformStats:
    """Last-resort stats so rendering never crashes."""
    defaults = {
        "xbox": PlatformStats(
            platform="xbox",
            username="Gamer",
            headline_value=0,
            headline_label="Gamerscore",
            substats=[SubStat("TA", 0)],
        ),
        "psn": PlatformStats(
            platform="psn",
            username="Player",
            headline_value="0 Platinums",
            headline_label="Trophies",
            substats=[
                SubStat("platinum", 0),
                SubStat("gold", 0),
                SubStat("silver", 0),
                SubStat("bronze", 0),
            ],
        ),
        "retroachievements": PlatformStats(
            platform="retroachievements",
            username="RetroUser",
            headline_value=0,
            headline_label="Hardcore Points",
            substats=[
                SubStat("RR", 0.0),
                SubStat("XXBXX", 0),
                SubStat("M", 0),
            ],
            extra_fields={
                "BeatenHardcoreAwardsCount": 0,
                "CompletionAwardsCount": 0,
                "MasteryAwardsCount": 0,
            },
        ),
    }
    return defaults.get(platform, PlatformStats(platform=platform))


def x_placeholder__mutmut_116(platform: str) -> PlatformStats:
    """Last-resort stats so rendering never crashes."""
    defaults = {
        "xbox": PlatformStats(
            platform="xbox",
            username="Gamer",
            headline_value=0,
            headline_label="Gamerscore",
            substats=[SubStat("TA", 0)],
        ),
        "psn": PlatformStats(
            platform="psn",
            username="Player",
            headline_value="0 Platinums",
            headline_label="Trophies",
            substats=[
                SubStat("platinum", 0),
                SubStat("gold", 0),
                SubStat("silver", 0),
                SubStat("bronze", 0),
            ],
        ),
        "retroachievements": PlatformStats(
            platform="retroachievements",
            username="RetroUser",
            headline_value=0,
            headline_label="Hardcore Points",
            substats=[
                SubStat("RR", 0.0),
                SubStat("b", 0),
                SubStat("M", 0),
            ],
            extra_fields={
                "BeatenHardcoreAwardsCount": 0,
                "CompletionAwardsCount": 0,
                "MasteryAwardsCount": 0,
            },
        ),
    }
    return defaults.get(platform, PlatformStats(platform=platform))


def x_placeholder__mutmut_117(platform: str) -> PlatformStats:
    """Last-resort stats so rendering never crashes."""
    defaults = {
        "xbox": PlatformStats(
            platform="xbox",
            username="Gamer",
            headline_value=0,
            headline_label="Gamerscore",
            substats=[SubStat("TA", 0)],
        ),
        "psn": PlatformStats(
            platform="psn",
            username="Player",
            headline_value="0 Platinums",
            headline_label="Trophies",
            substats=[
                SubStat("platinum", 0),
                SubStat("gold", 0),
                SubStat("silver", 0),
                SubStat("bronze", 0),
            ],
        ),
        "retroachievements": PlatformStats(
            platform="retroachievements",
            username="RetroUser",
            headline_value=0,
            headline_label="Hardcore Points",
            substats=[
                SubStat("RR", 0.0),
                SubStat("B", 1),
                SubStat("M", 0),
            ],
            extra_fields={
                "BeatenHardcoreAwardsCount": 0,
                "CompletionAwardsCount": 0,
                "MasteryAwardsCount": 0,
            },
        ),
    }
    return defaults.get(platform, PlatformStats(platform=platform))


def x_placeholder__mutmut_118(platform: str) -> PlatformStats:
    """Last-resort stats so rendering never crashes."""
    defaults = {
        "xbox": PlatformStats(
            platform="xbox",
            username="Gamer",
            headline_value=0,
            headline_label="Gamerscore",
            substats=[SubStat("TA", 0)],
        ),
        "psn": PlatformStats(
            platform="psn",
            username="Player",
            headline_value="0 Platinums",
            headline_label="Trophies",
            substats=[
                SubStat("platinum", 0),
                SubStat("gold", 0),
                SubStat("silver", 0),
                SubStat("bronze", 0),
            ],
        ),
        "retroachievements": PlatformStats(
            platform="retroachievements",
            username="RetroUser",
            headline_value=0,
            headline_label="Hardcore Points",
            substats=[
                SubStat("RR", 0.0),
                SubStat("B", 0),
                SubStat(None, 0),
            ],
            extra_fields={
                "BeatenHardcoreAwardsCount": 0,
                "CompletionAwardsCount": 0,
                "MasteryAwardsCount": 0,
            },
        ),
    }
    return defaults.get(platform, PlatformStats(platform=platform))


def x_placeholder__mutmut_119(platform: str) -> PlatformStats:
    """Last-resort stats so rendering never crashes."""
    defaults = {
        "xbox": PlatformStats(
            platform="xbox",
            username="Gamer",
            headline_value=0,
            headline_label="Gamerscore",
            substats=[SubStat("TA", 0)],
        ),
        "psn": PlatformStats(
            platform="psn",
            username="Player",
            headline_value="0 Platinums",
            headline_label="Trophies",
            substats=[
                SubStat("platinum", 0),
                SubStat("gold", 0),
                SubStat("silver", 0),
                SubStat("bronze", 0),
            ],
        ),
        "retroachievements": PlatformStats(
            platform="retroachievements",
            username="RetroUser",
            headline_value=0,
            headline_label="Hardcore Points",
            substats=[
                SubStat("RR", 0.0),
                SubStat("B", 0),
                SubStat("M", None),
            ],
            extra_fields={
                "BeatenHardcoreAwardsCount": 0,
                "CompletionAwardsCount": 0,
                "MasteryAwardsCount": 0,
            },
        ),
    }
    return defaults.get(platform, PlatformStats(platform=platform))


def x_placeholder__mutmut_120(platform: str) -> PlatformStats:
    """Last-resort stats so rendering never crashes."""
    defaults = {
        "xbox": PlatformStats(
            platform="xbox",
            username="Gamer",
            headline_value=0,
            headline_label="Gamerscore",
            substats=[SubStat("TA", 0)],
        ),
        "psn": PlatformStats(
            platform="psn",
            username="Player",
            headline_value="0 Platinums",
            headline_label="Trophies",
            substats=[
                SubStat("platinum", 0),
                SubStat("gold", 0),
                SubStat("silver", 0),
                SubStat("bronze", 0),
            ],
        ),
        "retroachievements": PlatformStats(
            platform="retroachievements",
            username="RetroUser",
            headline_value=0,
            headline_label="Hardcore Points",
            substats=[
                SubStat("RR", 0.0),
                SubStat("B", 0),
                SubStat(0),
            ],
            extra_fields={
                "BeatenHardcoreAwardsCount": 0,
                "CompletionAwardsCount": 0,
                "MasteryAwardsCount": 0,
            },
        ),
    }
    return defaults.get(platform, PlatformStats(platform=platform))


def x_placeholder__mutmut_121(platform: str) -> PlatformStats:
    """Last-resort stats so rendering never crashes."""
    defaults = {
        "xbox": PlatformStats(
            platform="xbox",
            username="Gamer",
            headline_value=0,
            headline_label="Gamerscore",
            substats=[SubStat("TA", 0)],
        ),
        "psn": PlatformStats(
            platform="psn",
            username="Player",
            headline_value="0 Platinums",
            headline_label="Trophies",
            substats=[
                SubStat("platinum", 0),
                SubStat("gold", 0),
                SubStat("silver", 0),
                SubStat("bronze", 0),
            ],
        ),
        "retroachievements": PlatformStats(
            platform="retroachievements",
            username="RetroUser",
            headline_value=0,
            headline_label="Hardcore Points",
            substats=[
                SubStat("RR", 0.0),
                SubStat("B", 0),
                SubStat("M", ),
            ],
            extra_fields={
                "BeatenHardcoreAwardsCount": 0,
                "CompletionAwardsCount": 0,
                "MasteryAwardsCount": 0,
            },
        ),
    }
    return defaults.get(platform, PlatformStats(platform=platform))


def x_placeholder__mutmut_122(platform: str) -> PlatformStats:
    """Last-resort stats so rendering never crashes."""
    defaults = {
        "xbox": PlatformStats(
            platform="xbox",
            username="Gamer",
            headline_value=0,
            headline_label="Gamerscore",
            substats=[SubStat("TA", 0)],
        ),
        "psn": PlatformStats(
            platform="psn",
            username="Player",
            headline_value="0 Platinums",
            headline_label="Trophies",
            substats=[
                SubStat("platinum", 0),
                SubStat("gold", 0),
                SubStat("silver", 0),
                SubStat("bronze", 0),
            ],
        ),
        "retroachievements": PlatformStats(
            platform="retroachievements",
            username="RetroUser",
            headline_value=0,
            headline_label="Hardcore Points",
            substats=[
                SubStat("RR", 0.0),
                SubStat("B", 0),
                SubStat("XXMXX", 0),
            ],
            extra_fields={
                "BeatenHardcoreAwardsCount": 0,
                "CompletionAwardsCount": 0,
                "MasteryAwardsCount": 0,
            },
        ),
    }
    return defaults.get(platform, PlatformStats(platform=platform))


def x_placeholder__mutmut_123(platform: str) -> PlatformStats:
    """Last-resort stats so rendering never crashes."""
    defaults = {
        "xbox": PlatformStats(
            platform="xbox",
            username="Gamer",
            headline_value=0,
            headline_label="Gamerscore",
            substats=[SubStat("TA", 0)],
        ),
        "psn": PlatformStats(
            platform="psn",
            username="Player",
            headline_value="0 Platinums",
            headline_label="Trophies",
            substats=[
                SubStat("platinum", 0),
                SubStat("gold", 0),
                SubStat("silver", 0),
                SubStat("bronze", 0),
            ],
        ),
        "retroachievements": PlatformStats(
            platform="retroachievements",
            username="RetroUser",
            headline_value=0,
            headline_label="Hardcore Points",
            substats=[
                SubStat("RR", 0.0),
                SubStat("B", 0),
                SubStat("m", 0),
            ],
            extra_fields={
                "BeatenHardcoreAwardsCount": 0,
                "CompletionAwardsCount": 0,
                "MasteryAwardsCount": 0,
            },
        ),
    }
    return defaults.get(platform, PlatformStats(platform=platform))


def x_placeholder__mutmut_124(platform: str) -> PlatformStats:
    """Last-resort stats so rendering never crashes."""
    defaults = {
        "xbox": PlatformStats(
            platform="xbox",
            username="Gamer",
            headline_value=0,
            headline_label="Gamerscore",
            substats=[SubStat("TA", 0)],
        ),
        "psn": PlatformStats(
            platform="psn",
            username="Player",
            headline_value="0 Platinums",
            headline_label="Trophies",
            substats=[
                SubStat("platinum", 0),
                SubStat("gold", 0),
                SubStat("silver", 0),
                SubStat("bronze", 0),
            ],
        ),
        "retroachievements": PlatformStats(
            platform="retroachievements",
            username="RetroUser",
            headline_value=0,
            headline_label="Hardcore Points",
            substats=[
                SubStat("RR", 0.0),
                SubStat("B", 0),
                SubStat("M", 1),
            ],
            extra_fields={
                "BeatenHardcoreAwardsCount": 0,
                "CompletionAwardsCount": 0,
                "MasteryAwardsCount": 0,
            },
        ),
    }
    return defaults.get(platform, PlatformStats(platform=platform))


def x_placeholder__mutmut_125(platform: str) -> PlatformStats:
    """Last-resort stats so rendering never crashes."""
    defaults = {
        "xbox": PlatformStats(
            platform="xbox",
            username="Gamer",
            headline_value=0,
            headline_label="Gamerscore",
            substats=[SubStat("TA", 0)],
        ),
        "psn": PlatformStats(
            platform="psn",
            username="Player",
            headline_value="0 Platinums",
            headline_label="Trophies",
            substats=[
                SubStat("platinum", 0),
                SubStat("gold", 0),
                SubStat("silver", 0),
                SubStat("bronze", 0),
            ],
        ),
        "retroachievements": PlatformStats(
            platform="retroachievements",
            username="RetroUser",
            headline_value=0,
            headline_label="Hardcore Points",
            substats=[
                SubStat("RR", 0.0),
                SubStat("B", 0),
                SubStat("M", 0),
            ],
            extra_fields={
                "XXBeatenHardcoreAwardsCountXX": 0,
                "CompletionAwardsCount": 0,
                "MasteryAwardsCount": 0,
            },
        ),
    }
    return defaults.get(platform, PlatformStats(platform=platform))


def x_placeholder__mutmut_126(platform: str) -> PlatformStats:
    """Last-resort stats so rendering never crashes."""
    defaults = {
        "xbox": PlatformStats(
            platform="xbox",
            username="Gamer",
            headline_value=0,
            headline_label="Gamerscore",
            substats=[SubStat("TA", 0)],
        ),
        "psn": PlatformStats(
            platform="psn",
            username="Player",
            headline_value="0 Platinums",
            headline_label="Trophies",
            substats=[
                SubStat("platinum", 0),
                SubStat("gold", 0),
                SubStat("silver", 0),
                SubStat("bronze", 0),
            ],
        ),
        "retroachievements": PlatformStats(
            platform="retroachievements",
            username="RetroUser",
            headline_value=0,
            headline_label="Hardcore Points",
            substats=[
                SubStat("RR", 0.0),
                SubStat("B", 0),
                SubStat("M", 0),
            ],
            extra_fields={
                "beatenhardcoreawardscount": 0,
                "CompletionAwardsCount": 0,
                "MasteryAwardsCount": 0,
            },
        ),
    }
    return defaults.get(platform, PlatformStats(platform=platform))


def x_placeholder__mutmut_127(platform: str) -> PlatformStats:
    """Last-resort stats so rendering never crashes."""
    defaults = {
        "xbox": PlatformStats(
            platform="xbox",
            username="Gamer",
            headline_value=0,
            headline_label="Gamerscore",
            substats=[SubStat("TA", 0)],
        ),
        "psn": PlatformStats(
            platform="psn",
            username="Player",
            headline_value="0 Platinums",
            headline_label="Trophies",
            substats=[
                SubStat("platinum", 0),
                SubStat("gold", 0),
                SubStat("silver", 0),
                SubStat("bronze", 0),
            ],
        ),
        "retroachievements": PlatformStats(
            platform="retroachievements",
            username="RetroUser",
            headline_value=0,
            headline_label="Hardcore Points",
            substats=[
                SubStat("RR", 0.0),
                SubStat("B", 0),
                SubStat("M", 0),
            ],
            extra_fields={
                "BEATENHARDCOREAWARDSCOUNT": 0,
                "CompletionAwardsCount": 0,
                "MasteryAwardsCount": 0,
            },
        ),
    }
    return defaults.get(platform, PlatformStats(platform=platform))


def x_placeholder__mutmut_128(platform: str) -> PlatformStats:
    """Last-resort stats so rendering never crashes."""
    defaults = {
        "xbox": PlatformStats(
            platform="xbox",
            username="Gamer",
            headline_value=0,
            headline_label="Gamerscore",
            substats=[SubStat("TA", 0)],
        ),
        "psn": PlatformStats(
            platform="psn",
            username="Player",
            headline_value="0 Platinums",
            headline_label="Trophies",
            substats=[
                SubStat("platinum", 0),
                SubStat("gold", 0),
                SubStat("silver", 0),
                SubStat("bronze", 0),
            ],
        ),
        "retroachievements": PlatformStats(
            platform="retroachievements",
            username="RetroUser",
            headline_value=0,
            headline_label="Hardcore Points",
            substats=[
                SubStat("RR", 0.0),
                SubStat("B", 0),
                SubStat("M", 0),
            ],
            extra_fields={
                "BeatenHardcoreAwardsCount": 1,
                "CompletionAwardsCount": 0,
                "MasteryAwardsCount": 0,
            },
        ),
    }
    return defaults.get(platform, PlatformStats(platform=platform))


def x_placeholder__mutmut_129(platform: str) -> PlatformStats:
    """Last-resort stats so rendering never crashes."""
    defaults = {
        "xbox": PlatformStats(
            platform="xbox",
            username="Gamer",
            headline_value=0,
            headline_label="Gamerscore",
            substats=[SubStat("TA", 0)],
        ),
        "psn": PlatformStats(
            platform="psn",
            username="Player",
            headline_value="0 Platinums",
            headline_label="Trophies",
            substats=[
                SubStat("platinum", 0),
                SubStat("gold", 0),
                SubStat("silver", 0),
                SubStat("bronze", 0),
            ],
        ),
        "retroachievements": PlatformStats(
            platform="retroachievements",
            username="RetroUser",
            headline_value=0,
            headline_label="Hardcore Points",
            substats=[
                SubStat("RR", 0.0),
                SubStat("B", 0),
                SubStat("M", 0),
            ],
            extra_fields={
                "BeatenHardcoreAwardsCount": 0,
                "XXCompletionAwardsCountXX": 0,
                "MasteryAwardsCount": 0,
            },
        ),
    }
    return defaults.get(platform, PlatformStats(platform=platform))


def x_placeholder__mutmut_130(platform: str) -> PlatformStats:
    """Last-resort stats so rendering never crashes."""
    defaults = {
        "xbox": PlatformStats(
            platform="xbox",
            username="Gamer",
            headline_value=0,
            headline_label="Gamerscore",
            substats=[SubStat("TA", 0)],
        ),
        "psn": PlatformStats(
            platform="psn",
            username="Player",
            headline_value="0 Platinums",
            headline_label="Trophies",
            substats=[
                SubStat("platinum", 0),
                SubStat("gold", 0),
                SubStat("silver", 0),
                SubStat("bronze", 0),
            ],
        ),
        "retroachievements": PlatformStats(
            platform="retroachievements",
            username="RetroUser",
            headline_value=0,
            headline_label="Hardcore Points",
            substats=[
                SubStat("RR", 0.0),
                SubStat("B", 0),
                SubStat("M", 0),
            ],
            extra_fields={
                "BeatenHardcoreAwardsCount": 0,
                "completionawardscount": 0,
                "MasteryAwardsCount": 0,
            },
        ),
    }
    return defaults.get(platform, PlatformStats(platform=platform))


def x_placeholder__mutmut_131(platform: str) -> PlatformStats:
    """Last-resort stats so rendering never crashes."""
    defaults = {
        "xbox": PlatformStats(
            platform="xbox",
            username="Gamer",
            headline_value=0,
            headline_label="Gamerscore",
            substats=[SubStat("TA", 0)],
        ),
        "psn": PlatformStats(
            platform="psn",
            username="Player",
            headline_value="0 Platinums",
            headline_label="Trophies",
            substats=[
                SubStat("platinum", 0),
                SubStat("gold", 0),
                SubStat("silver", 0),
                SubStat("bronze", 0),
            ],
        ),
        "retroachievements": PlatformStats(
            platform="retroachievements",
            username="RetroUser",
            headline_value=0,
            headline_label="Hardcore Points",
            substats=[
                SubStat("RR", 0.0),
                SubStat("B", 0),
                SubStat("M", 0),
            ],
            extra_fields={
                "BeatenHardcoreAwardsCount": 0,
                "COMPLETIONAWARDSCOUNT": 0,
                "MasteryAwardsCount": 0,
            },
        ),
    }
    return defaults.get(platform, PlatformStats(platform=platform))


def x_placeholder__mutmut_132(platform: str) -> PlatformStats:
    """Last-resort stats so rendering never crashes."""
    defaults = {
        "xbox": PlatformStats(
            platform="xbox",
            username="Gamer",
            headline_value=0,
            headline_label="Gamerscore",
            substats=[SubStat("TA", 0)],
        ),
        "psn": PlatformStats(
            platform="psn",
            username="Player",
            headline_value="0 Platinums",
            headline_label="Trophies",
            substats=[
                SubStat("platinum", 0),
                SubStat("gold", 0),
                SubStat("silver", 0),
                SubStat("bronze", 0),
            ],
        ),
        "retroachievements": PlatformStats(
            platform="retroachievements",
            username="RetroUser",
            headline_value=0,
            headline_label="Hardcore Points",
            substats=[
                SubStat("RR", 0.0),
                SubStat("B", 0),
                SubStat("M", 0),
            ],
            extra_fields={
                "BeatenHardcoreAwardsCount": 0,
                "CompletionAwardsCount": 1,
                "MasteryAwardsCount": 0,
            },
        ),
    }
    return defaults.get(platform, PlatformStats(platform=platform))


def x_placeholder__mutmut_133(platform: str) -> PlatformStats:
    """Last-resort stats so rendering never crashes."""
    defaults = {
        "xbox": PlatformStats(
            platform="xbox",
            username="Gamer",
            headline_value=0,
            headline_label="Gamerscore",
            substats=[SubStat("TA", 0)],
        ),
        "psn": PlatformStats(
            platform="psn",
            username="Player",
            headline_value="0 Platinums",
            headline_label="Trophies",
            substats=[
                SubStat("platinum", 0),
                SubStat("gold", 0),
                SubStat("silver", 0),
                SubStat("bronze", 0),
            ],
        ),
        "retroachievements": PlatformStats(
            platform="retroachievements",
            username="RetroUser",
            headline_value=0,
            headline_label="Hardcore Points",
            substats=[
                SubStat("RR", 0.0),
                SubStat("B", 0),
                SubStat("M", 0),
            ],
            extra_fields={
                "BeatenHardcoreAwardsCount": 0,
                "CompletionAwardsCount": 0,
                "XXMasteryAwardsCountXX": 0,
            },
        ),
    }
    return defaults.get(platform, PlatformStats(platform=platform))


def x_placeholder__mutmut_134(platform: str) -> PlatformStats:
    """Last-resort stats so rendering never crashes."""
    defaults = {
        "xbox": PlatformStats(
            platform="xbox",
            username="Gamer",
            headline_value=0,
            headline_label="Gamerscore",
            substats=[SubStat("TA", 0)],
        ),
        "psn": PlatformStats(
            platform="psn",
            username="Player",
            headline_value="0 Platinums",
            headline_label="Trophies",
            substats=[
                SubStat("platinum", 0),
                SubStat("gold", 0),
                SubStat("silver", 0),
                SubStat("bronze", 0),
            ],
        ),
        "retroachievements": PlatformStats(
            platform="retroachievements",
            username="RetroUser",
            headline_value=0,
            headline_label="Hardcore Points",
            substats=[
                SubStat("RR", 0.0),
                SubStat("B", 0),
                SubStat("M", 0),
            ],
            extra_fields={
                "BeatenHardcoreAwardsCount": 0,
                "CompletionAwardsCount": 0,
                "masteryawardscount": 0,
            },
        ),
    }
    return defaults.get(platform, PlatformStats(platform=platform))


def x_placeholder__mutmut_135(platform: str) -> PlatformStats:
    """Last-resort stats so rendering never crashes."""
    defaults = {
        "xbox": PlatformStats(
            platform="xbox",
            username="Gamer",
            headline_value=0,
            headline_label="Gamerscore",
            substats=[SubStat("TA", 0)],
        ),
        "psn": PlatformStats(
            platform="psn",
            username="Player",
            headline_value="0 Platinums",
            headline_label="Trophies",
            substats=[
                SubStat("platinum", 0),
                SubStat("gold", 0),
                SubStat("silver", 0),
                SubStat("bronze", 0),
            ],
        ),
        "retroachievements": PlatformStats(
            platform="retroachievements",
            username="RetroUser",
            headline_value=0,
            headline_label="Hardcore Points",
            substats=[
                SubStat("RR", 0.0),
                SubStat("B", 0),
                SubStat("M", 0),
            ],
            extra_fields={
                "BeatenHardcoreAwardsCount": 0,
                "CompletionAwardsCount": 0,
                "MASTERYAWARDSCOUNT": 0,
            },
        ),
    }
    return defaults.get(platform, PlatformStats(platform=platform))


def x_placeholder__mutmut_136(platform: str) -> PlatformStats:
    """Last-resort stats so rendering never crashes."""
    defaults = {
        "xbox": PlatformStats(
            platform="xbox",
            username="Gamer",
            headline_value=0,
            headline_label="Gamerscore",
            substats=[SubStat("TA", 0)],
        ),
        "psn": PlatformStats(
            platform="psn",
            username="Player",
            headline_value="0 Platinums",
            headline_label="Trophies",
            substats=[
                SubStat("platinum", 0),
                SubStat("gold", 0),
                SubStat("silver", 0),
                SubStat("bronze", 0),
            ],
        ),
        "retroachievements": PlatformStats(
            platform="retroachievements",
            username="RetroUser",
            headline_value=0,
            headline_label="Hardcore Points",
            substats=[
                SubStat("RR", 0.0),
                SubStat("B", 0),
                SubStat("M", 0),
            ],
            extra_fields={
                "BeatenHardcoreAwardsCount": 0,
                "CompletionAwardsCount": 0,
                "MasteryAwardsCount": 1,
            },
        ),
    }
    return defaults.get(platform, PlatformStats(platform=platform))


def x_placeholder__mutmut_137(platform: str) -> PlatformStats:
    """Last-resort stats so rendering never crashes."""
    defaults = {
        "xbox": PlatformStats(
            platform="xbox",
            username="Gamer",
            headline_value=0,
            headline_label="Gamerscore",
            substats=[SubStat("TA", 0)],
        ),
        "psn": PlatformStats(
            platform="psn",
            username="Player",
            headline_value="0 Platinums",
            headline_label="Trophies",
            substats=[
                SubStat("platinum", 0),
                SubStat("gold", 0),
                SubStat("silver", 0),
                SubStat("bronze", 0),
            ],
        ),
        "retroachievements": PlatformStats(
            platform="retroachievements",
            username="RetroUser",
            headline_value=0,
            headline_label="Hardcore Points",
            substats=[
                SubStat("RR", 0.0),
                SubStat("B", 0),
                SubStat("M", 0),
            ],
            extra_fields={
                "BeatenHardcoreAwardsCount": 0,
                "CompletionAwardsCount": 0,
                "MasteryAwardsCount": 0,
            },
        ),
    }
    return defaults.get(None, PlatformStats(platform=platform))


def x_placeholder__mutmut_138(platform: str) -> PlatformStats:
    """Last-resort stats so rendering never crashes."""
    defaults = {
        "xbox": PlatformStats(
            platform="xbox",
            username="Gamer",
            headline_value=0,
            headline_label="Gamerscore",
            substats=[SubStat("TA", 0)],
        ),
        "psn": PlatformStats(
            platform="psn",
            username="Player",
            headline_value="0 Platinums",
            headline_label="Trophies",
            substats=[
                SubStat("platinum", 0),
                SubStat("gold", 0),
                SubStat("silver", 0),
                SubStat("bronze", 0),
            ],
        ),
        "retroachievements": PlatformStats(
            platform="retroachievements",
            username="RetroUser",
            headline_value=0,
            headline_label="Hardcore Points",
            substats=[
                SubStat("RR", 0.0),
                SubStat("B", 0),
                SubStat("M", 0),
            ],
            extra_fields={
                "BeatenHardcoreAwardsCount": 0,
                "CompletionAwardsCount": 0,
                "MasteryAwardsCount": 0,
            },
        ),
    }
    return defaults.get(platform, None)


def x_placeholder__mutmut_139(platform: str) -> PlatformStats:
    """Last-resort stats so rendering never crashes."""
    defaults = {
        "xbox": PlatformStats(
            platform="xbox",
            username="Gamer",
            headline_value=0,
            headline_label="Gamerscore",
            substats=[SubStat("TA", 0)],
        ),
        "psn": PlatformStats(
            platform="psn",
            username="Player",
            headline_value="0 Platinums",
            headline_label="Trophies",
            substats=[
                SubStat("platinum", 0),
                SubStat("gold", 0),
                SubStat("silver", 0),
                SubStat("bronze", 0),
            ],
        ),
        "retroachievements": PlatformStats(
            platform="retroachievements",
            username="RetroUser",
            headline_value=0,
            headline_label="Hardcore Points",
            substats=[
                SubStat("RR", 0.0),
                SubStat("B", 0),
                SubStat("M", 0),
            ],
            extra_fields={
                "BeatenHardcoreAwardsCount": 0,
                "CompletionAwardsCount": 0,
                "MasteryAwardsCount": 0,
            },
        ),
    }
    return defaults.get(PlatformStats(platform=platform))


def x_placeholder__mutmut_140(platform: str) -> PlatformStats:
    """Last-resort stats so rendering never crashes."""
    defaults = {
        "xbox": PlatformStats(
            platform="xbox",
            username="Gamer",
            headline_value=0,
            headline_label="Gamerscore",
            substats=[SubStat("TA", 0)],
        ),
        "psn": PlatformStats(
            platform="psn",
            username="Player",
            headline_value="0 Platinums",
            headline_label="Trophies",
            substats=[
                SubStat("platinum", 0),
                SubStat("gold", 0),
                SubStat("silver", 0),
                SubStat("bronze", 0),
            ],
        ),
        "retroachievements": PlatformStats(
            platform="retroachievements",
            username="RetroUser",
            headline_value=0,
            headline_label="Hardcore Points",
            substats=[
                SubStat("RR", 0.0),
                SubStat("B", 0),
                SubStat("M", 0),
            ],
            extra_fields={
                "BeatenHardcoreAwardsCount": 0,
                "CompletionAwardsCount": 0,
                "MasteryAwardsCount": 0,
            },
        ),
    }
    return defaults.get(platform, )


def x_placeholder__mutmut_141(platform: str) -> PlatformStats:
    """Last-resort stats so rendering never crashes."""
    defaults = {
        "xbox": PlatformStats(
            platform="xbox",
            username="Gamer",
            headline_value=0,
            headline_label="Gamerscore",
            substats=[SubStat("TA", 0)],
        ),
        "psn": PlatformStats(
            platform="psn",
            username="Player",
            headline_value="0 Platinums",
            headline_label="Trophies",
            substats=[
                SubStat("platinum", 0),
                SubStat("gold", 0),
                SubStat("silver", 0),
                SubStat("bronze", 0),
            ],
        ),
        "retroachievements": PlatformStats(
            platform="retroachievements",
            username="RetroUser",
            headline_value=0,
            headline_label="Hardcore Points",
            substats=[
                SubStat("RR", 0.0),
                SubStat("B", 0),
                SubStat("M", 0),
            ],
            extra_fields={
                "BeatenHardcoreAwardsCount": 0,
                "CompletionAwardsCount": 0,
                "MasteryAwardsCount": 0,
            },
        ),
    }
    return defaults.get(platform, PlatformStats(platform=None))

x_placeholder__mutmut_mutants : ClassVar[MutantDict] = {
'x_placeholder__mutmut_1': x_placeholder__mutmut_1, 
    'x_placeholder__mutmut_2': x_placeholder__mutmut_2, 
    'x_placeholder__mutmut_3': x_placeholder__mutmut_3, 
    'x_placeholder__mutmut_4': x_placeholder__mutmut_4, 
    'x_placeholder__mutmut_5': x_placeholder__mutmut_5, 
    'x_placeholder__mutmut_6': x_placeholder__mutmut_6, 
    'x_placeholder__mutmut_7': x_placeholder__mutmut_7, 
    'x_placeholder__mutmut_8': x_placeholder__mutmut_8, 
    'x_placeholder__mutmut_9': x_placeholder__mutmut_9, 
    'x_placeholder__mutmut_10': x_placeholder__mutmut_10, 
    'x_placeholder__mutmut_11': x_placeholder__mutmut_11, 
    'x_placeholder__mutmut_12': x_placeholder__mutmut_12, 
    'x_placeholder__mutmut_13': x_placeholder__mutmut_13, 
    'x_placeholder__mutmut_14': x_placeholder__mutmut_14, 
    'x_placeholder__mutmut_15': x_placeholder__mutmut_15, 
    'x_placeholder__mutmut_16': x_placeholder__mutmut_16, 
    'x_placeholder__mutmut_17': x_placeholder__mutmut_17, 
    'x_placeholder__mutmut_18': x_placeholder__mutmut_18, 
    'x_placeholder__mutmut_19': x_placeholder__mutmut_19, 
    'x_placeholder__mutmut_20': x_placeholder__mutmut_20, 
    'x_placeholder__mutmut_21': x_placeholder__mutmut_21, 
    'x_placeholder__mutmut_22': x_placeholder__mutmut_22, 
    'x_placeholder__mutmut_23': x_placeholder__mutmut_23, 
    'x_placeholder__mutmut_24': x_placeholder__mutmut_24, 
    'x_placeholder__mutmut_25': x_placeholder__mutmut_25, 
    'x_placeholder__mutmut_26': x_placeholder__mutmut_26, 
    'x_placeholder__mutmut_27': x_placeholder__mutmut_27, 
    'x_placeholder__mutmut_28': x_placeholder__mutmut_28, 
    'x_placeholder__mutmut_29': x_placeholder__mutmut_29, 
    'x_placeholder__mutmut_30': x_placeholder__mutmut_30, 
    'x_placeholder__mutmut_31': x_placeholder__mutmut_31, 
    'x_placeholder__mutmut_32': x_placeholder__mutmut_32, 
    'x_placeholder__mutmut_33': x_placeholder__mutmut_33, 
    'x_placeholder__mutmut_34': x_placeholder__mutmut_34, 
    'x_placeholder__mutmut_35': x_placeholder__mutmut_35, 
    'x_placeholder__mutmut_36': x_placeholder__mutmut_36, 
    'x_placeholder__mutmut_37': x_placeholder__mutmut_37, 
    'x_placeholder__mutmut_38': x_placeholder__mutmut_38, 
    'x_placeholder__mutmut_39': x_placeholder__mutmut_39, 
    'x_placeholder__mutmut_40': x_placeholder__mutmut_40, 
    'x_placeholder__mutmut_41': x_placeholder__mutmut_41, 
    'x_placeholder__mutmut_42': x_placeholder__mutmut_42, 
    'x_placeholder__mutmut_43': x_placeholder__mutmut_43, 
    'x_placeholder__mutmut_44': x_placeholder__mutmut_44, 
    'x_placeholder__mutmut_45': x_placeholder__mutmut_45, 
    'x_placeholder__mutmut_46': x_placeholder__mutmut_46, 
    'x_placeholder__mutmut_47': x_placeholder__mutmut_47, 
    'x_placeholder__mutmut_48': x_placeholder__mutmut_48, 
    'x_placeholder__mutmut_49': x_placeholder__mutmut_49, 
    'x_placeholder__mutmut_50': x_placeholder__mutmut_50, 
    'x_placeholder__mutmut_51': x_placeholder__mutmut_51, 
    'x_placeholder__mutmut_52': x_placeholder__mutmut_52, 
    'x_placeholder__mutmut_53': x_placeholder__mutmut_53, 
    'x_placeholder__mutmut_54': x_placeholder__mutmut_54, 
    'x_placeholder__mutmut_55': x_placeholder__mutmut_55, 
    'x_placeholder__mutmut_56': x_placeholder__mutmut_56, 
    'x_placeholder__mutmut_57': x_placeholder__mutmut_57, 
    'x_placeholder__mutmut_58': x_placeholder__mutmut_58, 
    'x_placeholder__mutmut_59': x_placeholder__mutmut_59, 
    'x_placeholder__mutmut_60': x_placeholder__mutmut_60, 
    'x_placeholder__mutmut_61': x_placeholder__mutmut_61, 
    'x_placeholder__mutmut_62': x_placeholder__mutmut_62, 
    'x_placeholder__mutmut_63': x_placeholder__mutmut_63, 
    'x_placeholder__mutmut_64': x_placeholder__mutmut_64, 
    'x_placeholder__mutmut_65': x_placeholder__mutmut_65, 
    'x_placeholder__mutmut_66': x_placeholder__mutmut_66, 
    'x_placeholder__mutmut_67': x_placeholder__mutmut_67, 
    'x_placeholder__mutmut_68': x_placeholder__mutmut_68, 
    'x_placeholder__mutmut_69': x_placeholder__mutmut_69, 
    'x_placeholder__mutmut_70': x_placeholder__mutmut_70, 
    'x_placeholder__mutmut_71': x_placeholder__mutmut_71, 
    'x_placeholder__mutmut_72': x_placeholder__mutmut_72, 
    'x_placeholder__mutmut_73': x_placeholder__mutmut_73, 
    'x_placeholder__mutmut_74': x_placeholder__mutmut_74, 
    'x_placeholder__mutmut_75': x_placeholder__mutmut_75, 
    'x_placeholder__mutmut_76': x_placeholder__mutmut_76, 
    'x_placeholder__mutmut_77': x_placeholder__mutmut_77, 
    'x_placeholder__mutmut_78': x_placeholder__mutmut_78, 
    'x_placeholder__mutmut_79': x_placeholder__mutmut_79, 
    'x_placeholder__mutmut_80': x_placeholder__mutmut_80, 
    'x_placeholder__mutmut_81': x_placeholder__mutmut_81, 
    'x_placeholder__mutmut_82': x_placeholder__mutmut_82, 
    'x_placeholder__mutmut_83': x_placeholder__mutmut_83, 
    'x_placeholder__mutmut_84': x_placeholder__mutmut_84, 
    'x_placeholder__mutmut_85': x_placeholder__mutmut_85, 
    'x_placeholder__mutmut_86': x_placeholder__mutmut_86, 
    'x_placeholder__mutmut_87': x_placeholder__mutmut_87, 
    'x_placeholder__mutmut_88': x_placeholder__mutmut_88, 
    'x_placeholder__mutmut_89': x_placeholder__mutmut_89, 
    'x_placeholder__mutmut_90': x_placeholder__mutmut_90, 
    'x_placeholder__mutmut_91': x_placeholder__mutmut_91, 
    'x_placeholder__mutmut_92': x_placeholder__mutmut_92, 
    'x_placeholder__mutmut_93': x_placeholder__mutmut_93, 
    'x_placeholder__mutmut_94': x_placeholder__mutmut_94, 
    'x_placeholder__mutmut_95': x_placeholder__mutmut_95, 
    'x_placeholder__mutmut_96': x_placeholder__mutmut_96, 
    'x_placeholder__mutmut_97': x_placeholder__mutmut_97, 
    'x_placeholder__mutmut_98': x_placeholder__mutmut_98, 
    'x_placeholder__mutmut_99': x_placeholder__mutmut_99, 
    'x_placeholder__mutmut_100': x_placeholder__mutmut_100, 
    'x_placeholder__mutmut_101': x_placeholder__mutmut_101, 
    'x_placeholder__mutmut_102': x_placeholder__mutmut_102, 
    'x_placeholder__mutmut_103': x_placeholder__mutmut_103, 
    'x_placeholder__mutmut_104': x_placeholder__mutmut_104, 
    'x_placeholder__mutmut_105': x_placeholder__mutmut_105, 
    'x_placeholder__mutmut_106': x_placeholder__mutmut_106, 
    'x_placeholder__mutmut_107': x_placeholder__mutmut_107, 
    'x_placeholder__mutmut_108': x_placeholder__mutmut_108, 
    'x_placeholder__mutmut_109': x_placeholder__mutmut_109, 
    'x_placeholder__mutmut_110': x_placeholder__mutmut_110, 
    'x_placeholder__mutmut_111': x_placeholder__mutmut_111, 
    'x_placeholder__mutmut_112': x_placeholder__mutmut_112, 
    'x_placeholder__mutmut_113': x_placeholder__mutmut_113, 
    'x_placeholder__mutmut_114': x_placeholder__mutmut_114, 
    'x_placeholder__mutmut_115': x_placeholder__mutmut_115, 
    'x_placeholder__mutmut_116': x_placeholder__mutmut_116, 
    'x_placeholder__mutmut_117': x_placeholder__mutmut_117, 
    'x_placeholder__mutmut_118': x_placeholder__mutmut_118, 
    'x_placeholder__mutmut_119': x_placeholder__mutmut_119, 
    'x_placeholder__mutmut_120': x_placeholder__mutmut_120, 
    'x_placeholder__mutmut_121': x_placeholder__mutmut_121, 
    'x_placeholder__mutmut_122': x_placeholder__mutmut_122, 
    'x_placeholder__mutmut_123': x_placeholder__mutmut_123, 
    'x_placeholder__mutmut_124': x_placeholder__mutmut_124, 
    'x_placeholder__mutmut_125': x_placeholder__mutmut_125, 
    'x_placeholder__mutmut_126': x_placeholder__mutmut_126, 
    'x_placeholder__mutmut_127': x_placeholder__mutmut_127, 
    'x_placeholder__mutmut_128': x_placeholder__mutmut_128, 
    'x_placeholder__mutmut_129': x_placeholder__mutmut_129, 
    'x_placeholder__mutmut_130': x_placeholder__mutmut_130, 
    'x_placeholder__mutmut_131': x_placeholder__mutmut_131, 
    'x_placeholder__mutmut_132': x_placeholder__mutmut_132, 
    'x_placeholder__mutmut_133': x_placeholder__mutmut_133, 
    'x_placeholder__mutmut_134': x_placeholder__mutmut_134, 
    'x_placeholder__mutmut_135': x_placeholder__mutmut_135, 
    'x_placeholder__mutmut_136': x_placeholder__mutmut_136, 
    'x_placeholder__mutmut_137': x_placeholder__mutmut_137, 
    'x_placeholder__mutmut_138': x_placeholder__mutmut_138, 
    'x_placeholder__mutmut_139': x_placeholder__mutmut_139, 
    'x_placeholder__mutmut_140': x_placeholder__mutmut_140, 
    'x_placeholder__mutmut_141': x_placeholder__mutmut_141
}

def placeholder(*args, **kwargs):
    result = _mutmut_trampoline(x_placeholder__mutmut_orig, x_placeholder__mutmut_mutants, args, kwargs)
    return result 

placeholder.__signature__ = _mutmut_signature(x_placeholder__mutmut_orig)
x_placeholder__mutmut_orig.__name__ = 'x_placeholder'
