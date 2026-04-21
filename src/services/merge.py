"""Merge fresh scrape results with cached data and manual overrides.

Priority order when resolving platform stats:
  1. Fresh scrape (most authoritative)
  2. Manual override file (user edits)
  3. Cached data from the previous run
  4. Placeholder values (last resort — render never crashes)

When a fresh scrape succeeds but is missing some fields (e.g. avatar URL was
not found on the page), those holes are filled from the cache. The cache is
never preferred over fresh data for non-empty fields.
"""
from __future__ import annotations

import logging
from dataclasses import replace

from ..models import PlatformStats, SubStat

log = logging.getLogger(__name__)

# Placeholder display names per platform, used when no data is available at all
_PLACEHOLDER_USERNAME: dict[str, str] = {
    "xbox": "Gamer",
    "psn": "Player",
    "retroachievements": "RetroUser",
}


def merge_with_cache(
    fresh_stats: PlatformStats | None,
    cached_stats: PlatformStats | None,
    platform: str,
) -> PlatformStats | None:
    """Fill missing fields in `fresh_stats` from `cached_stats`.

    If there is no fresh data, the cached stats are returned as-is (they are
    better than nothing). If there is no cache either, returns None.

    Zero is treated as a legitimate value — a fresh zero is never overwritten
    by a non-zero cached value. Only genuinely absent fields (None or empty
    string) are filled from the cache.
    """
    if fresh_stats is None:
        if cached_stats is not None:
            log.info("%s: using cached data (scrape failed)", platform)
        return cached_stats

    if cached_stats is None:
        return fresh_stats

    merged_stats = replace(fresh_stats)
    _fill_missing_scalar_fields(merged_stats, cached_stats)
    merged_stats.substats = _merge_substats(merged_stats.substats, cached_stats.substats)

    for field_name, field_value in (cached_stats.extra_fields or {}).items():
        if field_name not in merged_stats.extra_fields or merged_stats.extra_fields[field_name] is None:
            merged_stats.extra_fields[field_name] = field_value

    return merged_stats


def _fill_missing_scalar_fields(
    merged_stats: PlatformStats,
    cached_stats: PlatformStats,
) -> None:
    """Overwrite absent scalar fields on `merged_stats` with values from `cached_stats`.

    Modifies `merged_stats` in place. Only fields that are None or empty string
    are replaced; non-empty fields from the fresh scrape are always preserved.
    """
    if not merged_stats.username:
        merged_stats.username = cached_stats.username
    if not merged_stats.avatar_url:
        merged_stats.avatar_url = cached_stats.avatar_url
    if merged_stats.headline_value is None or merged_stats.headline_value == "":
        merged_stats.headline_value = cached_stats.headline_value
    if not merged_stats.headline_label:
        merged_stats.headline_label = cached_stats.headline_label


def _merge_substats(
    fresh_substats: list[SubStat],
    cached_substats: list[SubStat],
) -> list[SubStat]:
    """Merge substat lists, using cache to fill holes in fresh data.

    For each substat in `fresh_substats`, if its value is None and the cache
    has a matching label, the cached value is used instead. Cached substats
    whose labels do not appear in the fresh list are appended at the end so
    no tracked stat is silently dropped between runs.
    """
    cached_substats_by_label = {substat.label: substat for substat in cached_substats}
    merged_substats: list[SubStat] = []

    for substat in fresh_substats:
        if substat.value is None and substat.label in cached_substats_by_label:
            merged_substats.append(cached_substats_by_label[substat.label])
        else:
            merged_substats.append(substat)

    # Append any cached substats missing from the fresh list
    included_labels = {substat.label for substat in merged_substats}
    for cached_substat in cached_substats:
        if cached_substat.label not in included_labels:
            merged_substats.append(cached_substat)

    return merged_substats


def apply_override(
    base_stats: PlatformStats | None,
    override_dict: dict | None,
    platform: str,
) -> PlatformStats:
    """Build or patch a PlatformStats from a manual override dict.

    The override dict may contain any fields from PlatformStats.to_dict().
    Substats and extra_fields are handled specially: substats replaces the
    list wholesale, while extra_fields merges key-by-key.
    """
    if not override_dict:
        return base_stats or PlatformStats(platform=platform)

    merged_dict = (base_stats or PlatformStats(platform=platform)).to_dict()
    for field_name, field_value in override_dict.items():
        if field_name == "substats" and isinstance(field_value, list):
            merged_dict["substats"] = field_value
        elif field_name == "extra_fields" and isinstance(field_value, dict):
            merged_dict.setdefault("extra_fields", {}).update(field_value)
        else:
            merged_dict[field_name] = field_value

    return PlatformStats.from_dict(merged_dict)


def placeholder(platform: str) -> PlatformStats:
    """Return last-resort placeholder stats for `platform` so rendering never crashes."""
    placeholder_stats: dict[str, PlatformStats] = {
        "xbox": PlatformStats(
            platform="xbox",
            username=_PLACEHOLDER_USERNAME["xbox"],
            headline_value=0,
            headline_label="Gamerscore",
            substats=[SubStat("TA", 0)],
        ),
        "psn": PlatformStats(
            platform="psn",
            username=_PLACEHOLDER_USERNAME["psn"],
            headline_value="0 Platinums",  # 0 takes plural form
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
            username=_PLACEHOLDER_USERNAME["retroachievements"],
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
    return placeholder_stats.get(platform, PlatformStats(platform=platform))
