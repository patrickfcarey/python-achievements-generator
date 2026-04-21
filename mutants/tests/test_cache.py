import json
from unittest.mock import MagicMock, patch

import pytest
import requests

from src import cache as cache_mod
from src.models import PlatformStats, SubStat


def test_cache_path_composition(tmp_path):
    assert cache_mod.cache_path(tmp_path, "xbox") == tmp_path / "xbox.json"


def test_avatar_path_default_png(tmp_path):
    assert cache_mod.avatar_path(tmp_path, "psn") == tmp_path / "avatars" / "psn.png"


def test_avatar_path_custom_ext(tmp_path):
    assert cache_mod.avatar_path(tmp_path, "psn", "webp") == tmp_path / "avatars" / "psn.webp"


def test_load_missing_returns_none(tmp_path):
    assert cache_mod.load(tmp_path, "xbox") is None


def test_save_and_load_roundtrip(tmp_path):
    ps = PlatformStats(
        platform="psn",
        username="Player",
        headline_value="1 Platinum",
        substats=[SubStat("platinum", 1)],
    )
    cache_mod.save(tmp_path, ps)
    loaded = cache_mod.load(tmp_path, "psn")
    assert loaded == ps


def test_save_creates_parent_dir(tmp_path):
    deep = tmp_path / "nested"
    ps = PlatformStats(platform="xbox")
    cache_mod.save(deep, ps)
    assert (deep / "xbox.json").exists()


def test_load_corrupt_json_returns_none(tmp_path):
    (tmp_path / "xbox.json").write_text("not json at all {", encoding="utf-8")
    assert cache_mod.load(tmp_path, "xbox") is None


def test_load_missing_platform_key_returns_none(tmp_path):
    (tmp_path / "xbox.json").write_text(json.dumps({"username": "x"}), encoding="utf-8")
    assert cache_mod.load(tmp_path, "xbox") is None


def test_find_cached_avatar_returns_existing_png(tmp_path):
    avatars = tmp_path / "avatars"
    avatars.mkdir()
    target = avatars / "xbox.png"
    target.write_bytes(b"fakepng")
    assert cache_mod.find_cached_avatar(tmp_path, "xbox") == target


def test_find_cached_avatar_prefers_first_listed_extension(tmp_path):
    avatars = tmp_path / "avatars"
    avatars.mkdir()
    (avatars / "xbox.jpg").write_bytes(b"j")
    (avatars / "xbox.png").write_bytes(b"p")
    # ("png", "jpg", "jpeg", "webp", "gif") — png comes first
    assert cache_mod.find_cached_avatar(tmp_path, "xbox").name == "xbox.png"


def test_find_cached_avatar_missing_returns_none(tmp_path):
    assert cache_mod.find_cached_avatar(tmp_path, "xbox") is None


def test_download_avatar_empty_url_returns_none(tmp_path):
    assert cache_mod.download_avatar(tmp_path, "xbox", "") is None


def test_download_avatar_handles_request_error(tmp_path):
    with patch.object(cache_mod.requests, "get", side_effect=requests.RequestException("boom")):
        assert cache_mod.download_avatar(tmp_path, "xbox", "http://x/a.png") is None


def test_download_avatar_writes_file_and_cleans_up_older(tmp_path):
    # Seed an older .jpg that should be removed after a .png is written.
    avatars = tmp_path / "avatars"
    avatars.mkdir()
    old = avatars / "xbox.jpg"
    old.write_bytes(b"old")

    resp = MagicMock(content=b"new-png-bytes", headers={"content-type": "image/png"})
    resp.raise_for_status = MagicMock()
    with patch.object(cache_mod.requests, "get", return_value=resp):
        out = cache_mod.download_avatar(tmp_path, "xbox", "http://x/a.png")
    assert out == avatars / "xbox.png"
    assert out.read_bytes() == b"new-png-bytes"
    assert not old.exists()


def test_download_avatar_falls_back_to_png_for_unknown_content_type(tmp_path):
    resp = MagicMock(content=b"x", headers={"content-type": "text/weird"})
    resp.raise_for_status = MagicMock()
    with patch.object(cache_mod.requests, "get", return_value=resp):
        out = cache_mod.download_avatar(tmp_path, "xbox", "http://x/a")
    assert out.suffix == ".png"


@pytest.mark.parametrize(
    "header,expected",
    [
        ("image/png", "png"),
        ("image/jpeg", "jpg"),
        ("image/jpg", "jpg"),
        ("image/webp", "webp"),
        ("image/gif", "gif"),
        ("image/png; charset=utf-8", "png"),
        ("IMAGE/PNG", "png"),
        ("text/html", None),
        ("", None),
    ],
)
def test_ext_from_content_type(header, expected):
    assert cache_mod._ext_from_content_type(header) == expected


@pytest.mark.parametrize("ext", ["png", "jpg", "jpeg", "webp", "gif"])
def test_find_cached_avatar_discovers_each_extension(tmp_path, ext):
    # The scraper can't cache an avatar we won't later look up. Each listed
    # extension must be discoverable on its own.
    avatars = tmp_path / "avatars"
    avatars.mkdir()
    target = avatars / f"xbox.{ext}"
    target.write_bytes(b"x")
    assert cache_mod.find_cached_avatar(tmp_path, "xbox") == target


@pytest.mark.parametrize(
    "content_type,expected_ext",
    [
        ("image/png", "png"),
        ("image/jpeg", "jpg"),
        ("image/webp", "webp"),
        ("image/gif", "gif"),
    ],
)
def test_download_avatar_uses_content_type_extension(tmp_path, content_type, expected_ext):
    resp = MagicMock(content=b"x", headers={"content-type": content_type})
    resp.raise_for_status = MagicMock()
    with patch.object(cache_mod.requests, "get", return_value=resp):
        out = cache_mod.download_avatar(tmp_path, "xbox", "http://x/a")
    assert out.suffix == f".{expected_ext}"


def test_download_avatar_passes_url_and_headers_to_requests(tmp_path):
    resp = MagicMock(content=b"x", headers={"content-type": "image/png"})
    resp.raise_for_status = MagicMock()
    with patch.object(cache_mod.requests, "get", return_value=resp) as mock_get:
        cache_mod.download_avatar(tmp_path, "xbox", "http://x/a.png", timeout=5.0)
    # positional: url is first arg
    args, kwargs = mock_get.call_args
    assert args[0] == "http://x/a.png"
    assert kwargs["timeout"] == 5.0
    assert kwargs["headers"] == {"User-Agent": "achievement-banner/1.0"}


def test_download_avatar_default_timeout_is_ten_seconds(tmp_path):
    resp = MagicMock(content=b"x", headers={"content-type": "image/png"})
    resp.raise_for_status = MagicMock()
    with patch.object(cache_mod.requests, "get", return_value=resp) as mock_get:
        cache_mod.download_avatar(tmp_path, "xbox", "http://x/a.png")
    assert mock_get.call_args.kwargs["timeout"] == 10.0


def test_save_writes_indented_json(tmp_path):
    # indent=2 keeps the file human-readable. A mutation to indent=None or indent=3 changes the output.
    ps = PlatformStats(platform="xbox", username="X")
    cache_mod.save(tmp_path, ps)
    text = (tmp_path / "xbox.json").read_text(encoding="utf-8")
    # Two-space indent means the first nested key line starts with exactly 2 spaces.
    nested_lines = [ln for ln in text.splitlines() if ln.startswith(" ") and not ln.startswith("   ")]
    assert any(ln.startswith("  ") and not ln.startswith("   ") for ln in nested_lines)


def test_download_avatar_unlinks_strictly_different_files(tmp_path):
    # Ensure unlink targets the older files — not the new one — by seeding two
    # old files and confirming they're both removed while the new one remains.
    avatars = tmp_path / "avatars"
    avatars.mkdir()
    (avatars / "xbox.jpg").write_bytes(b"old-jpg")
    (avatars / "xbox.webp").write_bytes(b"old-webp")

    resp = MagicMock(content=b"new", headers={"content-type": "image/png"})
    resp.raise_for_status = MagicMock()
    with patch.object(cache_mod.requests, "get", return_value=resp):
        out = cache_mod.download_avatar(tmp_path, "xbox", "http://x/a.png")
    assert out.read_bytes() == b"new"
    assert not (avatars / "xbox.jpg").exists()
    assert not (avatars / "xbox.webp").exists()
