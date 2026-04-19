"""Smoke test — builds a banner with placeholder data and checks file output."""
from pathlib import Path

from src.renderer import compose
from src.services.merge import placeholder


def test_render_produces_png(tmp_path: Path):
    cache_dir = tmp_path / "cache"
    (cache_dir / "avatars").mkdir(parents=True)

    stats = {p: placeholder(p) for p in ("xbox", "psn", "retroachievements")}
    out = tmp_path / "banner.png"

    compose.render(stats, cache_dir, out)

    assert out.exists()
    assert out.stat().st_size > 5000  # guard against empty / trivial file
