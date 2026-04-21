import pytest
from bs4 import BeautifulSoup

from src.providers.base import ProviderError
from src.providers.xbox import XboxProvider


def _fetch(provider: XboxProvider, html: str, url: str = "https://trueachievements.com/gamer/TestUser"):
    provider._get_soup = lambda u: BeautifulSoup(html, "html.parser")  # type: ignore[assignment]
    return provider.fetch(url)


def test_fetch_extracts_gamerscore_and_ta_score():
    html = """
    <html><head><meta property='og:image' content='https://cdn/x.png'></head>
    <body>
      <h1>Newerest5543 Profile</h1>
      <li>Gamerscore 85,420</li>
      <li>TrueAchievement Score 210,000</li>
    </body></html>
    """
    stats = _fetch(XboxProvider(), html)
    assert stats.platform == "xbox"
    assert stats.username == "Newerest5543"
    assert stats.avatar_url == "https://cdn/x.png"
    assert stats.headline_value == 85420
    assert stats.headline_label == "Gamerscore"
    assert stats.extra_fields == {"ta_score": 210000}
    assert stats.substats == [stats.substats[0]]
    assert stats.substats[0].label == "TA"
    assert stats.substats[0].value == 210000


def test_fetch_username_from_url_when_no_h1():
    html = "<html><body><li>Gamerscore 100</li></body></html>"
    stats = _fetch(XboxProvider(), html, "https://trueachievements.com/gamer/UrlOnly")
    assert stats.username == "UrlOnly"


def test_fetch_username_first_word_only():
    html = "<html><body><h1>Gamer Tag With Spaces</h1><li>Gamerscore 1</li></body></html>"
    stats = _fetch(XboxProvider(), html)
    assert stats.username == "Gamer"


def test_fetch_username_empty_when_url_unparseable():
    html = "<html><body><li>Gamerscore 1</li></body></html>"
    stats = _fetch(XboxProvider(), html, "https://example.com/nope")
    assert stats.username == ""


def test_fetch_avatar_from_img_fallback():
    html = """
    <html><body>
      <h1>X</h1>
      <img class='gamer-avatar' src='https://cdn/g.jpg'>
      <li>Gamerscore 10</li>
    </body></html>
    """
    stats = _fetch(XboxProvider(), html)
    assert stats.avatar_url == "https://cdn/g.jpg"


def test_fetch_avatar_none_when_nothing_found():
    html = "<html><body><h1>X</h1><li>Gamerscore 10</li></body></html>"
    stats = _fetch(XboxProvider(), html)
    assert stats.avatar_url is None


def test_fetch_gamerscore_from_labeled_row_preferred_over_page_text():
    # The label row has 50; the rest of the page has 999 — the label should win.
    html = """
    <html><body>
      <h1>X</h1>
      <li>Gamerscore 50</li>
      <p>999</p>
    </body></html>
    """
    stats = _fetch(XboxProvider(), html)
    assert stats.headline_value == 50


def test_fetch_ta_score_from_ta_shorthand():
    html = "<html><body><h1>X</h1><li>Gamerscore 100</li><span>TA 3,200</span></body></html>"
    stats = _fetch(XboxProvider(), html)
    assert stats.extra_fields["ta_score"] == 3200


def test_fetch_missing_ta_score_uses_zero_badge():
    html = "<html><body><h1>X</h1><li>Gamerscore 100</li></body></html>"
    stats = _fetch(XboxProvider(), html)
    assert stats.extra_fields["ta_score"] is None
    assert stats.substats[0].value == 0


def test_fetch_raises_when_no_stats_found():
    html = "<html><body><h1>X</h1><p>nothing numeric</p></body></html>"
    with pytest.raises(ProviderError, match="no recognizable stats"):
        _fetch(XboxProvider(), html)


def test_fetch_gamerscore_skips_labelled_row_without_usable_number():
    # Two rows match the "Gamerscore" label: the first has no parseable number,
    # so the scraper should continue to the next row and read 50 from there.
    html = """
    <html><body>
      <h1>X</h1>
      <li>Gamerscore nothing here</li>
      <li>Gamerscore 50</li>
    </body></html>
    """
    stats = _fetch(XboxProvider(), html)
    assert stats.headline_value == 50


def test_fetch_ta_score_skips_row_without_digit_run():
    # The first TA row is numberless, the second has 2,000. The scraper should
    # keep looking and pick up the real value.
    html = """
    <html><body>
      <h1>X</h1>
      <li>Gamerscore 10</li>
      <span>TrueAchievement Score pending</span>
      <span>TrueAchievement Score 2,000</span>
    </body></html>
    """
    stats = _fetch(XboxProvider(), html)
    assert stats.extra_fields["ta_score"] == 2000
