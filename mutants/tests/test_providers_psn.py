import pytest
from bs4 import BeautifulSoup

from src.providers.base import ProviderError
from src.providers.psn import PsnProvider


def _soup(html: str) -> BeautifulSoup:
    return BeautifulSoup(html, "html.parser")


def _fetch(provider: PsnProvider, html: str, url: str = "https://psnprofiles.com/TestUser"):
    provider._get_soup = lambda u: _soup(html)  # type: ignore[assignment]
    return provider.fetch(url)


def test_fetch_extracts_all_tiers_from_li_markup():
    html = """
    <html><head><meta property='og:image' content='https://cdn/a.png'></head>
    <body>
      <span class='username'>Newerest1</span>
      <li class='platinum'>5</li>
      <li class='gold'>120</li>
      <li class='silver'>300</li>
      <li class='bronze'>800</li>
    </body></html>
    """
    stats = _fetch(PsnProvider(), html)
    assert stats.platform == "psn"
    assert stats.username == "Newerest1"
    assert stats.avatar_url == "https://cdn/a.png"
    assert stats.headline_label == "Trophies"
    assert stats.headline_value == "5 Platinums"
    counts = {s.label: s.value for s in stats.substats}
    assert counts == {"platinum": 5, "gold": 120, "silver": 300, "bronze": 800}


def test_fetch_username_falls_back_to_url():
    html = "<html><body><li class='platinum'>1</li></body></html>"
    stats = _fetch(PsnProvider(), html, "https://psnprofiles.com/FallbackUser/")
    assert stats.username == "FallbackUser"


def test_fetch_username_empty_when_url_unparseable():
    html = "<html><body><li class='platinum'>1</li></body></html>"
    stats = _fetch(PsnProvider(), html, "https://example.com/nope")
    assert stats.username == ""


def test_fetch_username_from_h1_when_no_username_span():
    html = "<html><body><h1>HeaderUser</h1><li class='platinum'>1</li></body></html>"
    stats = _fetch(PsnProvider(), html)
    assert stats.username == "HeaderUser"


def test_fetch_avatar_from_img_fallback():
    html = """
    <html><body>
      <img class='avatar' src='https://cdn/i.jpg'>
      <li class='platinum'>1</li>
    </body></html>
    """
    stats = _fetch(PsnProvider(), html)
    assert stats.avatar_url == "https://cdn/i.jpg"


def test_fetch_avatar_none_when_nothing_found():
    html = "<html><body><li class='platinum'>1</li></body></html>"
    stats = _fetch(PsnProvider(), html)
    assert stats.avatar_url is None


def test_fetch_uses_regex_fallback_for_trophy_counts():
    # No class markers — regex reads "platinum 5 gold 10 silver 20 bronze 30"
    html = "<html><body>Trophies: platinum 5 gold 10 silver 20 bronze 30</body></html>"
    stats = _fetch(PsnProvider(), html)
    counts = {s.label: s.value for s in stats.substats}
    assert counts == {"platinum": 5, "gold": 10, "silver": 20, "bronze": 30}


def test_fetch_raises_when_no_counts_found():
    html = "<html><body><h1>Nothing here</h1></body></html>"
    with pytest.raises(ProviderError, match="no trophy counts"):
        _fetch(PsnProvider(), html)


def test_fetch_headline_formatting_uses_comma_separator():
    html = "<html><body><li class='platinum'>1234</li></body></html>"
    stats = _fetch(PsnProvider(), html)
    assert stats.headline_value == "1,234 Platinums"


def test_fetch_missing_tiers_default_to_zero():
    html = "<html><body><li class='platinum'>3</li></body></html>"
    stats = _fetch(PsnProvider(), html)
    by_label = {s.label: s.value for s in stats.substats}
    # Only platinum was found — others should still appear at 0
    assert by_label == {"platinum": 3, "gold": 0, "silver": 0, "bronze": 0}


def test_fetch_li_without_number_falls_through_to_regex():
    # The .gold element has non-numeric text, so parse_int returns None and
    # the regex fallback should match "gold 12" from the page text.
    html = """
    <html><body>
      <li class='platinum'>1</li>
      <li class='gold'>no digits here</li>
      <p>gold 12 trophies</p>
    </body></html>
    """
    stats = _fetch(PsnProvider(), html)
    by_label = {s.label: s.value for s in stats.substats}
    assert by_label["gold"] == 12
