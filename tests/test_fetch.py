from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from src.config import AppConfig, ProfileConfig
from src.models import PlatformStats, SubStat
from src.providers.base import Provider, ProviderError
from src.services import fetch as fetch_mod
from src.services.fetch import FetchPaths, fetch_all


def _make_provider(stats: PlatformStats | None = None, error: Exception | None = None):
    """Build a Provider subclass whose fetch() returns `stats` or raises `error`."""
    class _Fake(Provider):
        platform = stats.platform if stats else "unknown"

        def fetch(self, url):
            if error:
                raise error
            return stats
    return _Fake


def _paths(tmp_path) -> FetchPaths:
    return FetchPaths(
        cache_dir=tmp_path / "cache",
    )


def _cfg(**profiles) -> AppConfig:
    return AppConfig(
        profiles={
            p: ProfileConfig(platform=p, profile_url=url, display_name="")
            for p, url in profiles.items()
        }
    )


@pytest.fixture(autouse=True)
def _stub_browser_close():
    """Every test — avoid touching the real Playwright browser singleton."""
    with patch.object(fetch_mod.browser_mod, "close") as mock_close:
        yield mock_close


@pytest.fixture
def _no_avatar_downloads():
    """Avoid network during avatar handling."""
    with patch.object(fetch_mod.cache_mod, "download_avatar", return_value=None) as m:
        yield m


# ---------------------------------------------------------------- happy path


def test_fetch_all_scrapes_each_platform(tmp_path, _no_avatar_downloads):
    xbox_stats = PlatformStats(platform="xbox", username="X", headline_value=100, headline_label="Gamerscore")
    psn_stats = PlatformStats(platform="psn", username="P", headline_value="1 Platinum", headline_label="Trophies")

    providers = {
        "xbox": _make_provider(xbox_stats),
        "psn": _make_provider(psn_stats),
    }
    paths = _paths(tmp_path)
    with patch.dict(fetch_mod.PROVIDERS, providers, clear=True):
        out = fetch_all(_cfg(xbox="http://x", psn="http://p"), paths, scrape=True)

    assert set(out) == {"xbox", "psn"}
    assert out["xbox"].headline_value == 100
    assert out["psn"].headline_value == "1 Platinum"
    # Cache files written on successful scrape
    assert (paths.cache_dir / "xbox.json").exists()
    assert (paths.cache_dir / "psn.json").exists()


def test_fetch_all_applies_display_name_override(tmp_path, _no_avatar_downloads):
    stats = PlatformStats(platform="xbox", username="RawGamer", headline_value=1)
    providers = {"xbox": _make_provider(stats)}
    paths = _paths(tmp_path)
    cfg = AppConfig(profiles={"xbox": ProfileConfig("xbox", "http://x", "Display Override")})
    with patch.dict(fetch_mod.PROVIDERS, providers, clear=True):
        out = fetch_all(cfg, paths, scrape=True)
    assert out["xbox"].username == "Display Override"


def test_fetch_all_closes_browser_even_on_provider_crash(tmp_path, _no_avatar_downloads, _stub_browser_close):
    providers = {"xbox": _make_provider(error=RuntimeError("kaboom"))}
    paths = _paths(tmp_path)
    with patch.dict(fetch_mod.PROVIDERS, providers, clear=True):
        # Unexpected exceptions are caught by the provider loop (logged as
        # "unexpected"), so fetch_all returns normally.
        out = fetch_all(_cfg(xbox="http://x"), paths, scrape=True)
    assert "xbox" in out
    _stub_browser_close.assert_called_once()


# ---------------------------------------------------------------- fallbacks


def test_scrape_failure_falls_back_to_cache(tmp_path, _no_avatar_downloads):
    paths = _paths(tmp_path)
    paths.cache_dir.mkdir(parents=True, exist_ok=True)
    cached = PlatformStats(platform="xbox", headline_value=500, headline_label="Gamerscore")
    fetch_mod.cache_mod.save(paths.cache_dir, cached)

    providers = {"xbox": _make_provider(error=ProviderError("fail"))}
    with patch.dict(fetch_mod.PROVIDERS, providers, clear=True):
        out = fetch_all(_cfg(xbox="http://x"), paths, scrape=True)
    assert out["xbox"].headline_value == 500


def test_scrape_failure_no_cache_uses_placeholder(tmp_path, _no_avatar_downloads):
    providers = {"xbox": _make_provider(error=ProviderError("fail"))}
    paths = _paths(tmp_path)
    with patch.dict(fetch_mod.PROVIDERS, providers, clear=True):
        out = fetch_all(_cfg(xbox="http://x"), paths, scrape=True)
    # Placeholder values from merge.placeholder("xbox")
    assert out["xbox"].headline_label == "Gamerscore"
    assert out["xbox"].username == "Gamer"


def test_fresh_scrape_wins_over_cache(tmp_path, _no_avatar_downloads):
    paths = _paths(tmp_path)
    paths.cache_dir.mkdir(parents=True, exist_ok=True)
    fetch_mod.cache_mod.save(paths.cache_dir, PlatformStats(platform="xbox", headline_value=500))
    providers = {"xbox": _make_provider(PlatformStats(platform="xbox", headline_value=999))}
    with patch.dict(fetch_mod.PROVIDERS, providers, clear=True):
        out = fetch_all(_cfg(xbox="http://x"), paths, scrape=True)
    assert out["xbox"].headline_value == 999


def test_scrape_disabled_uses_cache(tmp_path, _no_avatar_downloads):
    paths = _paths(tmp_path)
    paths.cache_dir.mkdir(parents=True, exist_ok=True)
    cached = PlatformStats(platform="xbox", headline_value=500)
    fetch_mod.cache_mod.save(paths.cache_dir, cached)
    providers = {"xbox": _make_provider(error=AssertionError("provider must NOT be called"))}
    with patch.dict(fetch_mod.PROVIDERS, providers, clear=True):
        out = fetch_all(_cfg(xbox="http://x"), paths, scrape=False)
    assert out["xbox"].headline_value == 500


def test_empty_profile_url_skips_provider(tmp_path, _no_avatar_downloads):
    providers = {"xbox": _make_provider(error=AssertionError("provider must NOT be called"))}
    paths = _paths(tmp_path)
    cfg = AppConfig(profiles={"xbox": ProfileConfig("xbox", "", "")})
    with patch.dict(fetch_mod.PROVIDERS, providers, clear=True):
        out = fetch_all(cfg, paths, scrape=True)
    # No cache, no URL — placeholder
    assert out["xbox"].username == "Gamer"


def test_unknown_platform_falls_through_to_cache_or_placeholder(tmp_path, _no_avatar_downloads):
    # No provider registered — resolve must go straight to cache/placeholder
    paths = _paths(tmp_path)
    cfg = AppConfig(profiles={"steam": ProfileConfig("steam", "http://s", "")})
    with patch.dict(fetch_mod.PROVIDERS, {}, clear=True):
        out = fetch_all(cfg, paths, scrape=True)
    assert out["steam"].platform == "steam"


# ---------------------------------------------------------------- avatars


def test_existing_local_avatar_short_circuits_download(tmp_path):
    paths = _paths(tmp_path)
    paths.cache_dir.mkdir(parents=True, exist_ok=True)
    (paths.cache_dir / "avatars").mkdir()
    (paths.cache_dir / "avatars" / "xbox.png").write_bytes(b"local")

    providers = {"xbox": _make_provider(PlatformStats(platform="xbox", headline_value=1, avatar_url="http://cdn/a.png"))}
    with patch.dict(fetch_mod.PROVIDERS, providers, clear=True), \
         patch.object(fetch_mod.cache_mod, "download_avatar", side_effect=AssertionError("must not download")):
        fetch_all(_cfg(xbox="http://x"), paths, scrape=True)


def test_avatar_downloads_when_local_missing(tmp_path):
    paths = _paths(tmp_path)
    providers = {"xbox": _make_provider(PlatformStats(platform="xbox", headline_value=1, avatar_url="http://cdn/a.png"))}
    dl = MagicMock(return_value=paths.cache_dir / "avatars" / "xbox.png")
    with patch.dict(fetch_mod.PROVIDERS, providers, clear=True), \
         patch.object(fetch_mod.cache_mod, "download_avatar", dl):
        fetch_all(_cfg(xbox="http://x"), paths, scrape=True)
    dl.assert_called_once()


def test_avatar_download_skipped_without_url(tmp_path):
    paths = _paths(tmp_path)
    providers = {"xbox": _make_provider(PlatformStats(platform="xbox", headline_value=1, avatar_url=None))}
    with patch.dict(fetch_mod.PROVIDERS, providers, clear=True), \
         patch.object(fetch_mod.cache_mod, "download_avatar", side_effect=AssertionError("no url = no download")):
        fetch_all(_cfg(xbox="http://x"), paths, scrape=True)


def test_provider_receives_exact_profile_url(tmp_path, _no_avatar_downloads):
    captured = {}

    class _Capturing(Provider):
        platform = "xbox"
        def fetch(self, url):
            captured["url"] = url
            return PlatformStats(platform="xbox", headline_value=1)

    paths = _paths(tmp_path)
    with patch.dict(fetch_mod.PROVIDERS, {"xbox": _Capturing}, clear=True):
        fetch_all(_cfg(xbox="http://xbox.example/profile"), paths, scrape=True)
    assert captured["url"] == "http://xbox.example/profile"


def test_scrape_false_with_profile_url_still_skips_provider(tmp_path, _no_avatar_downloads):
    # Guards against `scrape and profile_url` → `scrape or profile_url`: with
    # scrape=False, the provider must NOT run even though profile_url is truthy.
    providers = {"xbox": _make_provider(error=AssertionError("provider must NOT be called"))}
    paths = _paths(tmp_path)
    with patch.dict(fetch_mod.PROVIDERS, providers, clear=True):
        fetch_all(_cfg(xbox="http://x"), paths, scrape=False)


def test_cache_not_written_when_fresh_is_none_and_placeholder_used(tmp_path, _no_avatar_downloads):
    # Another guard for the `and`/`or` mutation on line 92. No fresh, no cache,
    # no override — placeholder is returned, but must not be persisted to disk.
    paths = _paths(tmp_path)
    providers = {"xbox": _make_provider(error=ProviderError("fail"))}
    with patch.dict(fetch_mod.PROVIDERS, providers, clear=True), \
         patch.object(fetch_mod.cache_mod, "save") as mock_save:
        fetch_all(_cfg(xbox="http://x"), paths, scrape=True)
    mock_save.assert_not_called()
