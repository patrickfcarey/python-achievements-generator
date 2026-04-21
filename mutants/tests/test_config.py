from pathlib import Path

import pytest

from src.config import (
    AppConfig,
    ProfileConfig,
    load_config,
    load_overrides,
    save_overrides,
)


def _write(path: Path, text: str) -> Path:
    path.write_text(text, encoding="utf-8")
    return path


def test_load_config_missing_file_raises(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_config(tmp_path / "absent.yaml")


def test_load_config_parses_known_platforms(tmp_path):
    cfg = _write(
        tmp_path / "c.yaml",
        """
xbox:
  profile_url: https://ta/gamer/x
  display_name: X
psn:
  profile_url: https://psn/u
  display_name: P
retroachievements:
  profile_url: https://ra/user/r
  display_name: R
""",
    )
    app = load_config(cfg)
    assert isinstance(app, AppConfig)
    assert set(app.profiles) == {"xbox", "psn", "retroachievements"}
    assert isinstance(app.profiles["xbox"], ProfileConfig)
    assert app.profiles["xbox"].platform == "xbox"
    assert app.profiles["xbox"].display_name == "X"


def test_load_config_ignores_unknown_platforms(tmp_path):
    cfg = _write(tmp_path / "c.yaml", "steam:\n  profile_url: http://x\n")
    app = load_config(cfg)
    assert app.profiles == {}


def test_load_config_handles_empty_file(tmp_path):
    cfg = _write(tmp_path / "c.yaml", "")
    app = load_config(cfg)
    assert app.profiles == {}


def test_load_config_missing_subfields_default_to_empty(tmp_path):
    cfg = _write(tmp_path / "c.yaml", "xbox:\n  profile_url: http://x\n")
    app = load_config(cfg)
    assert app.profiles["xbox"].display_name == ""


def test_app_config_get_returns_profile_or_none():
    app = AppConfig(profiles={"xbox": ProfileConfig("xbox", "url", "name")})
    assert app.get("xbox").display_name == "name"
    assert app.get("psn") is None


def test_load_overrides_missing_file_returns_empty(tmp_path):
    assert load_overrides(tmp_path / "none.yaml") == {}


def test_load_overrides_empty_file_returns_empty(tmp_path):
    p = _write(tmp_path / "o.yaml", "")
    assert load_overrides(p) == {}


def test_load_overrides_parses_yaml(tmp_path):
    p = _write(tmp_path / "o.yaml", "xbox:\n  headline_value: 42\n")
    assert load_overrides(p) == {"xbox": {"headline_value": 42}}


def test_save_overrides_creates_parent_dirs(tmp_path):
    target = tmp_path / "nested" / "deep" / "o.yaml"
    save_overrides(target, {"psn": {"headline_value": 3}})
    assert target.exists()
    assert load_overrides(target) == {"psn": {"headline_value": 3}}


def test_save_overrides_preserves_insertion_order(tmp_path):
    target = tmp_path / "o.yaml"
    payload = {"z": 1, "a": 2, "m": 3}
    save_overrides(target, payload)
    text = target.read_text()
    # yaml.safe_dump(sort_keys=False) should preserve order
    assert text.index("z:") < text.index("a:") < text.index("m:")


def test_load_config_profile_url_uses_exact_key_and_default_empty_string(tmp_path):
    # Guards several mutants on `entry.get("profile_url", "")`:
    # - wrong key ("PROFILE_URL") returns "" not "http://x"
    # - wrong default ("XXXX") returns that instead of "" when key missing
    # - None default returns None, not ""
    cfg = _write(tmp_path / "c.yaml", "xbox:\n  profile_url: http://x\n")
    app = load_config(cfg)
    assert app.profiles["xbox"].profile_url == "http://x"

    cfg2 = _write(tmp_path / "c2.yaml", "xbox:\n  display_name: Only\n")
    app2 = load_config(cfg2)
    # Exact empty-string default matters — `None` or `"XXXX"` mutants would diverge.
    assert app2.profiles["xbox"].profile_url == ""
    assert isinstance(app2.profiles["xbox"].profile_url, str)


def test_load_config_processes_all_listed_platforms(tmp_path):
    # Guards `continue` → `break`: after an entry is processed, the loop must
    # continue to the next platform, not exit.
    cfg = _write(
        tmp_path / "c.yaml",
        """
xbox:
  profile_url: http://x
psn:
  profile_url: http://p
retroachievements:
  profile_url: http://r
""",
    )
    app = load_config(cfg)
    assert set(app.profiles) == {"xbox", "psn", "retroachievements"}


def test_load_config_display_name_uses_exact_key_and_default_empty_string(tmp_path):
    # Same guard shape for the display_name field.
    cfg = _write(tmp_path / "c.yaml", "xbox:\n  profile_url: http://x\n")
    app = load_config(cfg)
    assert app.profiles["xbox"].display_name == ""
    cfg2 = _write(tmp_path / "c2.yaml", "xbox:\n  profile_url: http://x\n  display_name: My Name\n")
    app2 = load_config(cfg2)
    assert app2.profiles["xbox"].display_name == "My Name"


def test_save_overrides_uses_sort_keys_false(tmp_path):
    # Guards `sort_keys=False` → `sort_keys=None`. sort_keys=None defaults to True
    # in yaml — an alphabetically-sorted dump swaps z and a.
    target = tmp_path / "o.yaml"
    save_overrides(target, {"z": 1, "a": 2})
    text = target.read_text()
    assert text.index("z:") < text.index("a:")
