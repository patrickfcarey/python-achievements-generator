from __future__ import annotations

import pytest
from bs4 import BeautifulSoup

from src.providers.base import ProviderError
from src.providers.xbox import XboxProvider


def _scores_block(gs: str | None = "17,045", ta: str | None = "28,073") -> str:
    parts = []
    if ta is not None:
        parts.append(f'<span><i class="tgn-icon ta-emb md"></i>{ta}</span>')
    if gs is not None:
        parts.append(f'<span><i class="tgn-icon ta-gs invt md"></i>{gs}</span>')
    return f'<div class="scores">{"".join(parts)}</div>'


def _fetch(provider: XboxProvider, html: str, url: str = "https://trueachievements.com/gamer/TestUser"):
    provider._get_soup = lambda u: BeautifulSoup(html, "html.parser")  # type: ignore[assignment]
    return provider.fetch(url)


def test_fetch_extracts_gamerscore_and_ta_score():
    html = f"""
    <html><head><meta property='og:image' content='https://cdn/x.png'></head>
    <body>
      <h1>Newerest5543 Profile</h1>
      {_scores_block(gs='17,045', ta='28,073')}
    </body></html>
    """
    stats = _fetch(XboxProvider(), html)
    assert stats.platform == "xbox"
    assert stats.username == "Newerest5543"
    assert stats.avatar_url == "https://cdn/x.png"
    assert stats.headline_value == 17045
    assert stats.headline_label == "Gamerscore"
    assert stats.extra_fields == {"ta_score": 28073}
    assert len(stats.substats) == 1
    assert stats.substats[0].label == "TA"
    assert stats.substats[0].value == 28073


def test_fetch_username_from_url_when_no_h1():
    html = f"<html><body>{_scores_block()}</body></html>"
    stats = _fetch(XboxProvider(), html, "https://trueachievements.com/gamer/UrlOnly")
    assert stats.username == "UrlOnly"


def test_fetch_username_first_word_only():
    html = f"<html><body><h1>Gamer Tag With Spaces</h1>{_scores_block()}</body></html>"
    stats = _fetch(XboxProvider(), html)
    assert stats.username == "Gamer"


def test_fetch_username_empty_when_url_unparseable():
    html = f"<html><body>{_scores_block()}</body></html>"
    stats = _fetch(XboxProvider(), html, "https://example.com/nope")
    assert stats.username == ""


def test_fetch_avatar_from_img_fallback():
    html = f"""
    <html><body>
      <h1>X</h1>
      <img class='gamer-avatar' src='https://cdn/g.jpg'>
      {_scores_block()}
    </body></html>
    """
    stats = _fetch(XboxProvider(), html)
    assert stats.avatar_url == "https://cdn/g.jpg"


def test_fetch_avatar_none_when_nothing_found():
    html = f"<html><body><h1>X</h1>{_scores_block()}</body></html>"
    stats = _fetch(XboxProvider(), html)
    assert stats.avatar_url is None


def test_fetch_gamerscore_read_from_ta_gs_span_only():
    # A larger number elsewhere on the page must not be picked up — only the
    # span marked with the `ta-gs` icon counts as Gamerscore.
    html = f"""
    <html><body>
      <h1>X</h1>
      {_scores_block(gs='50', ta='28,073')}
      <p>99,999</p>
    </body></html>
    """
    stats = _fetch(XboxProvider(), html)
    assert stats.headline_value == 50


def test_fetch_ta_score_read_from_ta_emb_span_only():
    # Loose "TA" text on the page must not be used — only the ta-emb span counts.
    html = f"""
    <html><body>
      <h1>X</h1>
      {_scores_block(gs='17,045', ta='3,200')}
      <span>TA 999,999</span>
    </body></html>
    """
    stats = _fetch(XboxProvider(), html)
    assert stats.extra_fields["ta_score"] == 3200


def test_fetch_missing_ta_score_uses_zero_badge():
    html = f"<html><body><h1>X</h1>{_scores_block(gs='100', ta=None)}</body></html>"
    stats = _fetch(XboxProvider(), html)
    assert stats.extra_fields["ta_score"] is None
    assert stats.substats[0].value == 0


def test_fetch_raises_when_no_stats_found():
    html = "<html><body><h1>X</h1><p>nothing numeric</p></body></html>"
    with pytest.raises(ProviderError, match="no recognizable stats"):
        _fetch(XboxProvider(), html)
