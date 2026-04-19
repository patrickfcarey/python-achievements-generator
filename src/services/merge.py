"""Merge fresh scrape results with cached data and manual overrides."""
from __future__ import annotations

import logging
from dataclasses import replace

from ..models import PlatformStats, SubStat

log = logging.getLogger(__name__)


def merge_with_cache(
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
    if merged.headline_value in (None, "", 0):
        merged.headline_value = cached.headline_value
    if not merged.headline_label:
        merged.headline_label = cached.headline_label

    merged.substats = _merge_substats(merged.substats, cached.substats)

    for k, v in (cached.extra_fields or {}).items():
        if merged.extra_fields.get(k) in (None, "", 0):
            merged.extra_fields[k] = v

    return merged


def _merge_substats(fresh: list[SubStat], cached: list[SubStat]) -> list[SubStat]:
    by_label = {s.label: s for s in cached}
    out: list[SubStat] = []
    for s in fresh:
        if s.value in (None, 0, "") and s.label in by_label:
            out.append(by_label[s.label])
        else:
            out.append(s)
    # append any cached stats that are missing from fresh
    seen = {s.label for s in out}
    for s in cached:
        if s.label not in seen:
            out.append(s)
    return out


def apply_override(stats: PlatformStats | None, override: dict | None, platform: str) -> PlatformStats:
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


def placeholder(platform: str) -> PlatformStats:
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
            headline_label="Points",
            substats=[
                SubStat("TR", 0.0),
                SubStat("M", 0),
            ],
            extra_fields={"masteries": 0, "completions": 0},
        ),
    }
    return defaults.get(platform, PlatformStats(platform=platform))
