"""Per-platform JSON cache and avatar cache."""
from __future__ import annotations

import json
import logging
from pathlib import Path

import requests

from .models import PlatformStats

log = logging.getLogger(__name__)


def cache_path(cache_dir: Path, platform: str) -> Path:
    return Path(cache_dir) / f"{platform}.json"


def avatar_path(cache_dir: Path, platform: str, ext: str = "png") -> Path:
    return Path(cache_dir) / "avatars" / f"{platform}.{ext}"


def load(cache_dir: Path, platform: str) -> PlatformStats | None:
    p = cache_path(cache_dir, platform)
    if not p.exists():
        return None
    try:
        return PlatformStats.from_dict(json.loads(p.read_text(encoding="utf-8")))
    except (ValueError, KeyError) as exc:
        log.warning("cache: failed to parse %s: %s", p, exc)
        return None


def save(cache_dir: Path, stats: PlatformStats) -> None:
    p = cache_path(cache_dir, stats.platform)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(stats.to_dict(), indent=2), encoding="utf-8")


def download_avatar(
    cache_dir: Path,
    platform: str,
    url: str,
    timeout: float = 10.0,
) -> Path | None:
    if not url:
        return None
    try:
        resp = requests.get(url, timeout=timeout, headers={"User-Agent": "achievement-banner/1.0"})
        resp.raise_for_status()
    except requests.RequestException as exc:
        log.warning("avatar: download failed for %s: %s", platform, exc)
        return None

    ext = _ext_from_content_type(resp.headers.get("content-type", "")) or "png"
    out = avatar_path(cache_dir, platform, ext)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(resp.content)
    # clean up older formats so only one avatar file remains per platform
    for other in out.parent.glob(f"{platform}.*"):
        if other != out:
            other.unlink(missing_ok=True)
    return out


def find_cached_avatar(cache_dir: Path, platform: str) -> Path | None:
    for ext in ("png", "jpg", "jpeg", "webp", "gif"):
        p = avatar_path(cache_dir, platform, ext)
        if p.exists():
            return p
    return None


def _ext_from_content_type(content_type: str) -> str | None:
    mapping = {
        "image/png": "png",
        "image/jpeg": "jpg",
        "image/jpg": "jpg",
        "image/webp": "webp",
        "image/gif": "gif",
    }
    return mapping.get(content_type.split(";")[0].strip().lower())
