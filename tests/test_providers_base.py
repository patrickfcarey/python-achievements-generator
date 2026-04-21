from unittest.mock import patch

import pytest

from src.providers import base as base_mod
from src.providers.base import Provider, ProviderError


class _Dummy(Provider):
    platform = "dummy"

    def fetch(self, profile_url):
        return None


def test_get_soup_parses_returned_html():
    with patch.object(base_mod.browser, "fetch_html", return_value="<html><body><p>hi</p></body></html>"):
        soup = _Dummy()._get_soup("http://x")
    assert soup.find("p").get_text() == "hi"


def test_get_soup_raises_on_empty_response():
    with patch.object(base_mod.browser, "fetch_html", return_value=""):
        with pytest.raises(ProviderError, match="empty response"):
            _Dummy()._get_soup("http://x")


def test_get_soup_normalises_browser_exception():
    with patch.object(base_mod.browser, "fetch_html", side_effect=RuntimeError("boom")):
        with pytest.raises(ProviderError, match="browser fetch error"):
            _Dummy()._get_soup("http://x")


def test_get_soup_passes_url_and_timeout_to_browser():
    dummy = _Dummy()
    dummy.timeout = 7.0
    with patch.object(base_mod.browser, "fetch_html", return_value="<html></html>") as mock_fetch:
        dummy._get_soup("http://the-url")
    args, kwargs = mock_fetch.call_args
    assert args[0] == "http://the-url"
    # timeout_ms = int(7.0 * 1000) = 7000
    assert kwargs["timeout_ms"] == 7000


def test_get_soup_uses_html_parser():
    # "html.parser" is the stdlib parser — no lxml dep. Verify the returned
    # soup's builder is the stdlib HTMLParser, not a surprise alternative.
    with patch.object(base_mod.browser, "fetch_html", return_value="<html><body><br></body></html>"):
        soup = _Dummy()._get_soup("http://x")
    # The html.parser builder's name is "html.parser".
    assert soup.builder.NAME == "html.parser"
