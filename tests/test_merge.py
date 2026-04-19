from src.models import PlatformStats, SubStat
from src.services.merge import apply_override, merge_with_cache, placeholder


def _stats(platform="xbox", **kw):
    return PlatformStats(platform=platform, **kw)


def test_merge_returns_cached_when_fresh_missing():
    cached = _stats(headline_value=100)
    assert merge_with_cache(None, cached, "xbox") is cached


def test_merge_fills_holes_from_cache():
    fresh = _stats(headline_value=None, substats=[SubStat("gold", 0)])
    cached = _stats(
        headline_value=500,
        substats=[SubStat("gold", 45), SubStat("silver", 205)],
    )
    merged = merge_with_cache(fresh, cached, "xbox")
    assert merged.headline_value == 500
    labels = {s.label: s.value for s in merged.substats}
    assert labels["gold"] == 45
    assert labels["silver"] == 205


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


def test_placeholder_shapes():
    assert placeholder("xbox").headline_label == "Gamerscore"
    assert placeholder("psn").headline_label == "Trophies"
    ra = placeholder("retroachievements")
    assert ra.headline_label == "Points"
    assert [s.label for s in ra.substats] == ["TR", "M"]
