from unittest.mock import MagicMock, patch

import pytest
import requests
from bs4 import BeautifulSoup

from src.providers.base import ProviderError
from src.providers import retroachievements as ra_mod
from src.providers.retroachievements import RetroAchievementsProvider


PROFILE_URL = "https://retroachievements.org/user/newerest"


def _clear_ra_env(monkeypatch):
    for k in ("RA_API_USER", "RA_API_KEY", "RETROACHIEVEMENTS_API_USER", "RETROACHIEVEMENTS_API_KEY"):
        monkeypatch.delenv(k, raising=False)


def _html_fetch(provider, html, url=PROFILE_URL):
    provider._get_soup = lambda u: BeautifulSoup(html, "html.parser")  # type: ignore[assignment]
    return provider.fetch(url)


# ---------------------------------------------------------------- HTML path


def test_html_path_extracts_fields(monkeypatch):
    _clear_ra_env(monkeypatch)
    html = """
    <html><head><meta property='og:image' content='https://cdn/u.png'></head>
    <body>
      <h1>newerest</h1>
      <p>Softcore Points 242</p>
      <p>Hardcore Points 546</p>
      <p>True Ratio 2.26</p>
      <p>Masteries 0</p>
      <p>Completions 0</p>
      <p>Beaten 2</p>
    </body></html>
    """
    stats = _html_fetch(RetroAchievementsProvider(), html)
    assert stats.platform == "retroachievements"
    assert stats.username == "newerest"
    assert stats.avatar_url == "https://cdn/u.png"
    assert stats.headline_label == "Hardcore Points"
    assert stats.headline_value == 546
    assert stats.extra_fields["TotalPoints"] == 546
    assert stats.extra_fields["TotalSoftcorePoints"] == 242
    assert stats.extra_fields["TotalTruePoints"] is None  # HTML can't produce this
    assert stats.extra_fields["BeatenHardcoreAwardsCount"] == 2
    assert stats.extra_fields["MasteryAwardsCount"] == 0
    assert stats.extra_fields["CompletionAwardsCount"] == 0
    assert stats.extra_fields["true_ratio"] == 2.26
    assert [s.label for s in stats.substats] == ["RR", "B", "M"]


def test_html_path_raises_without_any_points(monkeypatch):
    _clear_ra_env(monkeypatch)
    html = "<html><body><h1>user</h1><p>no numbers</p></body></html>"
    with pytest.raises(ProviderError, match="no point totals"):
        _html_fetch(RetroAchievementsProvider(), html)


def test_html_path_falls_back_to_softcore_when_no_hardcore(monkeypatch):
    _clear_ra_env(monkeypatch)
    html = "<html><body><h1>u</h1><p>Softcore Points 99</p></body></html>"
    stats = _html_fetch(RetroAchievementsProvider(), html)
    assert stats.headline_value == 99


def test_html_path_username_from_url_when_no_h1(monkeypatch):
    _clear_ra_env(monkeypatch)
    html = "<html><body><p>Softcore Points 1</p></body></html>"
    stats = _html_fetch(RetroAchievementsProvider(), html, "https://retroachievements.org/user/urlman")
    assert stats.username == "urlman"


def test_html_path_username_empty_when_url_unparseable(monkeypatch):
    _clear_ra_env(monkeypatch)
    html = "<html><body><p>Softcore Points 1</p></body></html>"
    stats = _html_fetch(RetroAchievementsProvider(), html, "https://example.com/")
    assert stats.username == ""


def test_html_path_avatar_from_img_fallback(monkeypatch):
    _clear_ra_env(monkeypatch)
    html = "<html><body><h1>u</h1><img src='https://ra/UserPic/u.png'><p>Softcore Points 1</p></body></html>"
    stats = _html_fetch(RetroAchievementsProvider(), html)
    assert stats.avatar_url == "https://ra/UserPic/u.png"


def test_html_path_avatar_none_when_nothing_found(monkeypatch):
    _clear_ra_env(monkeypatch)
    html = "<html><body><h1>u</h1><p>Softcore Points 1</p></body></html>"
    stats = _html_fetch(RetroAchievementsProvider(), html)
    assert stats.avatar_url is None


# ---------------------------------------------------------------- API path


def _api_responses(summary, profile, awards):
    """Build a side_effect list of Mock responses for three sequential GETs."""
    def _make(payload):
        r = MagicMock()
        r.raise_for_status = MagicMock()
        r.json.return_value = payload
        return r
    return [_make(summary), _make(profile), _make(awards)]


def test_api_path_happy(monkeypatch):
    monkeypatch.setenv("RA_API_USER", "apiuser")
    monkeypatch.setenv("RA_API_KEY", "apikey")
    summary = {"TotalPoints": 242, "TotalSoftcorePoints": 0, "TotalTruePoints": 546, "UserPic": "/UserPic/n.png", "User": "newerest"}
    profile = {"User": "newerest", "UserPic": "/UserPic/n.png"}
    awards = {"MasteryAwardsCount": 3, "CompletionAwardsCount": 1, "BeatenHardcoreAwardsCount": 7}

    with patch.object(ra_mod, "requests") as mock_req:
        mock_req.get.side_effect = _api_responses(summary, profile, awards)
        mock_req.RequestException = requests.RequestException
        stats = RetroAchievementsProvider().fetch(PROFILE_URL)

    assert stats.username == "newerest"
    assert stats.avatar_url == "https://retroachievements.org/UserPic/n.png"
    assert stats.headline_value == 242
    assert stats.headline_label == "Hardcore Points"
    assert stats.extra_fields["TotalPoints"] == 242
    assert stats.extra_fields["TotalSoftcorePoints"] == 0
    assert stats.extra_fields["TotalTruePoints"] == 546
    assert stats.extra_fields["BeatenHardcoreAwardsCount"] == 7
    assert stats.extra_fields["CompletionAwardsCount"] == 1
    assert stats.extra_fields["MasteryAwardsCount"] == 3
    assert stats.extra_fields["true_ratio"] == round(546 / 242, 2)
    # substat values follow the new layout
    by_label = {s.label: s.value for s in stats.substats}
    assert by_label == {"RR": round(546 / 242, 2), "B": 7, "M": 3}


def test_api_path_preserves_zero_awards(monkeypatch):
    """Regression: a legitimate 0 mastery count must NOT fall through `or` to
    some other count. The provider reads MasteryAwardsCount explicitly."""
    monkeypatch.setenv("RA_API_USER", "u")
    monkeypatch.setenv("RA_API_KEY", "k")
    summary = {"TotalPoints": 10, "TotalSoftcorePoints": 0, "TotalTruePoints": 20}
    profile = {"User": "u", "UserPic": "/UserPic/u.png"}
    awards = {"MasteryAwardsCount": 0, "CompletionAwardsCount": 0, "BeatenHardcoreAwardsCount": 0, "TotalAwardsCount": 999}

    with patch.object(ra_mod, "requests") as mock_req:
        mock_req.get.side_effect = _api_responses(summary, profile, awards)
        mock_req.RequestException = requests.RequestException
        stats = RetroAchievementsProvider().fetch(PROFILE_URL)

    assert stats.extra_fields["MasteryAwardsCount"] == 0
    assert stats.extra_fields["CompletionAwardsCount"] == 0
    assert stats.extra_fields["BeatenHardcoreAwardsCount"] == 0


def test_api_path_absolute_avatar_url(monkeypatch):
    monkeypatch.setenv("RA_API_USER", "u")
    monkeypatch.setenv("RA_API_KEY", "k")
    summary = {"TotalPoints": 1, "UserPic": "https://external/cdn/pic.png"}
    profile = {"User": "u", "UserPic": "https://external/cdn/pic.png"}
    awards = {"MasteryAwardsCount": 0, "CompletionAwardsCount": 0, "BeatenHardcoreAwardsCount": 0}

    with patch.object(ra_mod, "requests") as mock_req:
        mock_req.get.side_effect = _api_responses(summary, profile, awards)
        mock_req.RequestException = requests.RequestException
        stats = RetroAchievementsProvider().fetch(PROFILE_URL)

    assert stats.avatar_url == "https://external/cdn/pic.png"  # no prefix prepended


def test_api_path_headline_falls_back_to_softcore(monkeypatch):
    monkeypatch.setenv("RA_API_USER", "u")
    monkeypatch.setenv("RA_API_KEY", "k")
    summary = {"TotalPoints": None, "TotalSoftcorePoints": 50, "TotalTruePoints": None, "UserPic": ""}
    profile = {"User": "u"}
    awards = {"MasteryAwardsCount": 0, "CompletionAwardsCount": 0, "BeatenHardcoreAwardsCount": 0}

    with patch.object(ra_mod, "requests") as mock_req:
        mock_req.get.side_effect = _api_responses(summary, profile, awards)
        mock_req.RequestException = requests.RequestException
        stats = RetroAchievementsProvider().fetch(PROFILE_URL)

    assert stats.headline_value == 50


def test_api_path_raises_when_no_points(monkeypatch):
    monkeypatch.setenv("RA_API_USER", "u")
    monkeypatch.setenv("RA_API_KEY", "k")
    summary = {"TotalPoints": None, "TotalSoftcorePoints": None, "TotalTruePoints": None}
    profile = {"User": "u"}
    awards = {}

    # When the API raises ProviderError the outer fetch catches it and falls
    # through to HTML scrape — which we stub to also fail cleanly so the test
    # observes the API-path failure directly.
    provider = RetroAchievementsProvider()
    def _boom(url):
        raise ProviderError("html path disabled for this test")
    provider._get_soup = _boom  # type: ignore[assignment]

    with patch.object(ra_mod, "requests") as mock_req:
        mock_req.get.side_effect = _api_responses(summary, profile, awards)
        mock_req.RequestException = requests.RequestException
        with pytest.raises(ProviderError):
            provider.fetch(PROFILE_URL)


def test_api_failure_falls_through_to_html(monkeypatch):
    monkeypatch.setenv("RA_API_USER", "u")
    monkeypatch.setenv("RA_API_KEY", "k")
    html = "<html><body><h1>fallback</h1><p>Softcore Points 5</p></body></html>"

    def _raise(*args, **kwargs):
        raise requests.RequestException("boom")

    with patch.object(ra_mod, "requests") as mock_req:
        mock_req.get.side_effect = _raise
        mock_req.RequestException = requests.RequestException
        stats = _html_fetch(RetroAchievementsProvider(), html)

    assert stats.username == "fallback"
    assert stats.headline_value == 5


def test_api_skipped_when_env_missing(monkeypatch):
    _clear_ra_env(monkeypatch)
    html = "<html><body><h1>u</h1><p>Softcore Points 1</p></body></html>"

    # If requests.get were ever called the API path was wrongly taken.
    with patch.object(ra_mod, "requests") as mock_req:
        mock_req.get.side_effect = AssertionError("API path must not be taken without env vars")
        mock_req.RequestException = requests.RequestException
        stats = _html_fetch(RetroAchievementsProvider(), html)
    assert stats.username == "u"


def test_api_path_skipped_when_username_unparseable(monkeypatch):
    monkeypatch.setenv("RA_API_USER", "u")
    monkeypatch.setenv("RA_API_KEY", "k")
    html = "<html><body><h1>from-html</h1><p>Softcore Points 1</p></body></html>"

    # URL lacks /user/<name>, so API path is skipped and HTML runs instead.
    with patch.object(ra_mod, "requests") as mock_req:
        mock_req.get.side_effect = AssertionError("API path must not run without a username")
        mock_req.RequestException = requests.RequestException
        stats = _html_fetch(RetroAchievementsProvider(), html, "https://retroachievements.org/whatever")
    assert stats.username == "from-html"


def test_api_alt_env_var_names(monkeypatch):
    _clear_ra_env(monkeypatch)
    monkeypatch.setenv("RETROACHIEVEMENTS_API_USER", "altuser")
    monkeypatch.setenv("RETROACHIEVEMENTS_API_KEY", "altkey")
    summary = {"TotalPoints": 10, "TotalSoftcorePoints": 0, "TotalTruePoints": 20, "UserPic": "/x.png"}
    profile = {"User": "u"}
    awards = {"MasteryAwardsCount": 0, "CompletionAwardsCount": 0, "BeatenHardcoreAwardsCount": 0}

    with patch.object(ra_mod, "requests") as mock_req:
        mock_req.get.side_effect = _api_responses(summary, profile, awards)
        mock_req.RequestException = requests.RequestException
        stats = RetroAchievementsProvider().fetch(PROFILE_URL)
    # First positional arg of the first call includes z=altuser, y=altkey
    first_call = mock_req.get.call_args_list[0]
    assert first_call.kwargs["params"]["z"] == "altuser"
    assert first_call.kwargs["params"]["y"] == "altkey"
    assert stats.headline_value == 10


def test_username_from_url_helper():
    p = RetroAchievementsProvider()
    assert p._username_from_url("https://retroachievements.org/user/newerest/") == "newerest"
    assert p._username_from_url("https://retroachievements.org/user/a?b=c") == "a"
    assert p._username_from_url("https://no-match.example/") == ""
