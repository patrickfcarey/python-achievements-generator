"""Shared Playwright browser session used by HTML-scraping providers.

The live scraping targets (TrueAchievements, PSNProfiles, RetroAchievements)
all sit behind Cloudflare, which rejects requests/cloudscraper on TLS
fingerprint alone. Driving a real browser is the only reliable fix.

One browser + context is launched on first use and reused for the rest of the
process so Cloudflare clearance cookies stick between pages. Call `close()` at
shutdown (fetch_all does this in its finally block).

Browser choice via `BANNER_BROWSER` env var: chromium (default), firefox,
webkit. Headed by default — Cloudflare reliably detects headless Chromium.
Override with `BANNER_HEADLESS=1` if running somewhere without a display.
"""
from __future__ import annotations

import logging
import os
import time

log = logging.getLogger(__name__)

_PW = None
_BROWSER = None
_CONTEXT = None

_USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
)

# Challenge-page title markers Cloudflare uses while the interstitial is up.
_CF_TITLE_MARKERS = ("just a moment", "attention required", "checking your browser")


def _browser_kind():
    return (os.environ.get("BANNER_BROWSER") or "chromium").lower()


def _headless() -> bool:
    return os.environ.get("BANNER_HEADLESS", "").lower() in ("1", "true", "yes")


def _ensure_context():
    global _PW, _BROWSER, _CONTEXT
    if _CONTEXT is not None:
        return _CONTEXT

    from playwright.sync_api import sync_playwright

    _PW = sync_playwright().start()
    kind = _browser_kind()
    launcher = getattr(_PW, kind, _PW.chromium)
    _BROWSER = launcher.launch(headless=_headless())
    _CONTEXT = _BROWSER.new_context(
        user_agent=_USER_AGENT,
        viewport={"width": 1366, "height": 820},
        locale="en-US",
    )
    log.info("browser: launched %s (headless=%s)", kind, _headless())
    return _CONTEXT


def fetch_html(url: str, timeout_ms: int = 30000) -> str:
    """Navigate to `url` and return fully rendered HTML.

    Waits out Cloudflare's interstitial by polling the page title until the
    challenge markers disappear (up to ~15s).
    """
    ctx = _ensure_context()
    page = ctx.new_page()
    try:
        page.goto(url, wait_until="domcontentloaded", timeout=timeout_ms)
        deadline = time.time() + 20
        while time.time() < deadline:
            title = (page.title() or "").lower()
            if not any(m in title for m in _CF_TITLE_MARKERS):
                break
            time.sleep(1)
        try:
            page.wait_for_load_state("networkidle", timeout=timeout_ms)
        except Exception:
            pass  # networkidle may never fire on chatty pages; HTML is already there
        return page.content()
    finally:
        page.close()


def close() -> None:
    global _PW, _BROWSER, _CONTEXT
    if _CONTEXT is not None:
        try:
            _CONTEXT.close()
        except Exception:
            pass
        _CONTEXT = None
    if _BROWSER is not None:
        try:
            _BROWSER.close()
        except Exception:
            pass
        _BROWSER = None
    if _PW is not None:
        try:
            _PW.stop()
        except Exception:
            pass
        _PW = None
