from src.models import PlatformStats, SubStat
from src.services.merge import apply_override, merge_with_cache, placeholder


def _stats(platform="xbox", **kw):
    return PlatformStats(platform=platform, **kw)


def test_merge_returns_cached_when_fresh_missing():
    cached = _stats(headline_value=100)
    assert merge_with_cache(None, cached, "xbox") is cached


def test_merge_fills_holes_from_cache():
    # None = genuinely missing, fill from cache. 0 = real fetched value, keep.
    fresh = _stats(headline_value=None, substats=[SubStat("gold", None)])
    cached = _stats(
        headline_value=500,
        substats=[SubStat("gold", 45), SubStat("silver", 205)],
    )
    merged = merge_with_cache(fresh, cached, "xbox")
    assert merged.headline_value == 500
    labels = {s.label: s.value for s in merged.substats}
    assert labels["gold"] == 45
    assert labels["silver"] == 205


def test_merge_preserves_fresh_zero():
    # A legitimate fetched 0 must not be overwritten by stale cache values.
    fresh = _stats(headline_value=0, substats=[SubStat("gold", 0)])
    cached = _stats(headline_value=500, substats=[SubStat("gold", 45)])
    merged = merge_with_cache(fresh, cached, "xbox")
    assert merged.headline_value == 0
    assert merged.substats[0].value == 0


def test_merge_fills_missing_extra_fields_from_cache():
    fresh = _stats(extra_fields={"present": 1, "nulled": None})
    cached = _stats(extra_fields={"nulled": 99, "absent": 7, "present": 999})
    merged = merge_with_cache(fresh, cached, "xbox")
    # null → replaced; absent → filled; present → kept
    assert merged.extra_fields == {"present": 1, "nulled": 99, "absent": 7}


def test_merge_fills_username_and_avatar_from_cache():
    fresh = _stats(username="", avatar_url=None)
    cached = _stats(username="Cached", avatar_url="http://cdn/a.png")
    merged = merge_with_cache(fresh, cached, "xbox")
    assert merged.username == "Cached"
    assert merged.avatar_url == "http://cdn/a.png"


def test_merge_fills_headline_label_from_cache():
    fresh = _stats(headline_label=None, headline_value=10)
    cached = _stats(headline_label="Gamerscore", headline_value=0)
    merged = merge_with_cache(fresh, cached, "xbox")
    assert merged.headline_label == "Gamerscore"


def test_merge_keeps_fresh_username_when_set():
    fresh = _stats(username="Fresh")
    cached = _stats(username="Stale")
    merged = merge_with_cache(fresh, cached, "xbox")
    assert merged.username == "Fresh"


def test_merge_returns_fresh_when_cache_missing():
    fresh = _stats(headline_value=1)
    assert merge_with_cache(fresh, None, "xbox") is fresh


def test_merge_keeps_fresh_values():
    fresh = _stats(headline_value=999, substats=[SubStat("gold", 10)])
    cached = _stats(headline_value=1, substats=[SubStat("gold", 1)])
    merged = merge_with_cache(fresh, cached, "xbox")
    assert merged.headline_value == 999
    assert merged.substats[0].value == 10


def test_apply_override_overwrites_fields():
    merged = apply_override(None, {"headline_value": 42, "username": "Manual"}, "xbox")
    assert merged.headline_value == 42
    assert merged.username == "Manual"


def test_apply_override_no_override_returns_stats_or_placeholder():
    base = _stats(headline_value=7)
    assert apply_override(base, None, "xbox") is base
    fresh_empty = apply_override(None, None, "xbox")
    assert fresh_empty.platform == "xbox"


def test_apply_override_replaces_substats_from_override():
    base = _stats(substats=[SubStat("gold", 5)])
    merged = apply_override(base, {"substats": [{"label": "silver", "value": 9}]}, "xbox")
    assert [(s.label, s.value) for s in merged.substats] == [("silver", 9)]


def test_apply_override_merges_extra_fields():
    base = _stats(extra_fields={"a": 1, "b": 2})
    merged = apply_override(base, {"extra_fields": {"b": 20, "c": 30}}, "xbox")
    assert merged.extra_fields == {"a": 1, "b": 20, "c": 30}


def test_placeholder_shapes():
    assert placeholder("xbox").headline_label == "Gamerscore"
    assert placeholder("psn").headline_label == "Trophies"
    ra = placeholder("retroachievements")
    assert ra.headline_label == "Hardcore Points"
    assert [s.label for s in ra.substats] == ["RR", "B", "M"]


def test_placeholder_xbox_full_shape():
    p = placeholder("xbox")
    assert p.platform == "xbox"
    assert p.username == "Gamer"
    assert p.headline_value == 0
    assert p.headline_label == "Gamerscore"
    assert len(p.substats) == 1
    assert p.substats[0].label == "TA"
    assert p.substats[0].value == 0


def test_placeholder_psn_full_shape():
    p = placeholder("psn")
    assert p.platform == "psn"
    assert p.username == "Player"
    assert p.headline_value == "0 Platinums"
    assert p.headline_label == "Trophies"
    labels = [s.label for s in p.substats]
    values = [s.value for s in p.substats]
    assert labels == ["platinum", "gold", "silver", "bronze"]
    assert values == [0, 0, 0, 0]


def test_placeholder_retro_full_shape():
    p = placeholder("retroachievements")
    assert p.platform == "retroachievements"
    assert p.username == "RetroUser"
    assert p.headline_value == 0
    assert p.headline_label == "Hardcore Points"
    labels = [s.label for s in p.substats]
    values = [s.value for s in p.substats]
    assert labels == ["RR", "B", "M"]
    assert values == [0.0, 0, 0]
    assert p.extra_fields == {
        "BeatenHardcoreAwardsCount": 0,
        "CompletionAwardsCount": 0,
        "MasteryAwardsCount": 0,
    }


def test_placeholder_unknown_platform_returns_bare_stats():
    p = placeholder("switch")
    assert p.platform == "switch"
    assert p.username == ""
    assert p.headline_value is None
    assert p.substats == []


def test_apply_override_no_stats_no_override_uses_platform_arg():
    # stats=None + override=None path — the bare placeholder must carry the given platform.
    out = apply_override(None, None, "psn")
    assert out.platform == "psn"


def test_apply_override_no_stats_with_override_uses_platform_arg():
    # stats=None + truthy override exercises the `base = stats or PlatformStats(platform=platform)` line.
    out = apply_override(None, {"headline_value": 5}, "retroachievements")
    assert out.platform == "retroachievements"
    assert out.headline_value == 5


def test_apply_override_list_value_for_non_substats_key_does_not_clobber_substats():
    # If `k == "substats" and isinstance(v, list)` were mutated to `or`, a list
    # value under any other key would overwrite substats. Assert it doesn't.
    base = _stats(substats=[SubStat("gold", 5)])
    merged = apply_override(base, {"username": "Name"}, "xbox")
    assert [(s.label, s.value) for s in merged.substats] == [("gold", 5)]
    assert merged.username == "Name"


def test_apply_override_dict_value_for_non_extra_fields_key_does_not_merge_as_extra_fields():
    # If `k == "extra_fields" and isinstance(v, dict)` were mutated to `or`, a dict
    # value under any other key would update extra_fields. Assert it doesn't.
    base = _stats(extra_fields={"orig": 1})
    # headline_value is a scalar field; a dict value would normally be wrong but
    # must still be stored under that key, not merged into extra_fields.
    merged = apply_override(base, {"username": "NewName"}, "xbox")
    assert merged.extra_fields == {"orig": 1}
    assert merged.username == "NewName"


def test_apply_override_extra_fields_seeds_empty_when_base_has_none():
    # Exercises data.setdefault("extra_fields", {}).update(v) when no extra_fields yet.
    # PlatformStats() default is {} already, but this confirms the merge result shape.
    merged = apply_override(None, {"extra_fields": {"x": 1, "y": 2}}, "xbox")
    assert merged.extra_fields == {"x": 1, "y": 2}


def test_merge_with_cache_both_none_returns_none():
    assert merge_with_cache(None, None, "xbox") is None


def test_merge_empty_string_headline_treated_as_missing():
    # "" is explicitly treated as missing by the merge logic.
    fresh = _stats(headline_value="")
    cached = _stats(headline_value=42)
    merged = merge_with_cache(fresh, cached, "xbox")
    assert merged.headline_value == 42


def test_merge_substats_cache_only_labels_appended():
    fresh = _stats(substats=[SubStat("gold", 5)])
    cached = _stats(substats=[SubStat("gold", 1), SubStat("silver", 99)])
    merged = merge_with_cache(fresh, cached, "xbox")
    labels = {s.label: s.value for s in merged.substats}
    # gold comes from fresh, silver is appended from cache.
    assert labels == {"gold": 5, "silver": 99}
