from src.models import PlatformStats, SubStat


def test_substat_defaults():
    s = SubStat("gold", 12)
    assert s.label == "gold"
    assert s.value == 12
    assert s.icon is None


def test_platformstats_defaults():
    ps = PlatformStats(platform="xbox")
    assert ps.username == ""
    assert ps.avatar_url is None
    assert ps.headline_value is None
    assert ps.headline_label is None
    assert ps.substats == []
    assert ps.extra_fields == {}


def test_to_dict_roundtrip():
    ps = PlatformStats(
        platform="psn",
        username="Player",
        avatar_url="https://cdn/a.png",
        headline_value="3 Platinums",
        headline_label="Trophies",
        substats=[SubStat("platinum", 3), SubStat("gold", 45, "gold.png")],
        extra_fields={"rank": 12, "nested": {"k": 1}},
    )
    back = PlatformStats.from_dict(ps.to_dict())
    assert back == ps


def test_from_dict_accepts_substat_objects():
    sub = SubStat("silver", 10)
    ps = PlatformStats.from_dict({"platform": "psn", "substats": [sub]})
    assert ps.substats == [sub]


def test_from_dict_fills_defaults_for_missing_fields():
    ps = PlatformStats.from_dict({"platform": "xbox"})
    assert ps.platform == "xbox"
    assert ps.username == ""
    assert ps.substats == []
    assert ps.extra_fields == {}


def test_from_dict_copies_extra_fields():
    src_dict = {"platform": "xbox", "extra_fields": {"ta": 1}}
    ps = PlatformStats.from_dict(src_dict)
    ps.extra_fields["ta"] = 999
    assert src_dict["extra_fields"]["ta"] == 1  # original untouched


def test_from_dict_handles_null_extra_fields():
    ps = PlatformStats.from_dict({"platform": "xbox", "extra_fields": None})
    assert ps.extra_fields == {}


def test_from_dict_handles_null_substats():
    ps = PlatformStats.from_dict({"platform": "xbox", "substats": None})
    assert ps.substats == []


def test_has_core_data_false_when_empty():
    assert PlatformStats(platform="xbox").has_core_data() is False


def test_has_core_data_true_for_headline_value():
    assert PlatformStats(platform="xbox", headline_value=0).has_core_data() is True
    assert PlatformStats(platform="xbox", headline_value="0").has_core_data() is True


def test_has_core_data_true_for_substats():
    ps = PlatformStats(platform="xbox", substats=[SubStat("a", 0)])
    assert ps.has_core_data() is True


def test_has_core_data_true_for_extra_fields():
    ps = PlatformStats(platform="xbox", extra_fields={"a": 1})
    assert ps.has_core_data() is True
