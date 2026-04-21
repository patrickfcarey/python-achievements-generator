"""Per-platform JSON cache and avatar image cache.

Two kinds of data are stored:
- Platform stats (JSON): one file per platform at <cache_dir>/<platform>.json
- Avatar images: one file per platform at <cache_dir>/avatars/<platform>.<ext>

Avatars are downloaded once and then reused. If the extension changes between
runs (e.g. the server starts returning WebP instead of PNG), older files for
the same platform are cleaned up so only one avatar file exists per platform.
"""
from __future__ import annotations

import json
import logging
from pathlib import Path

import requests

from .models import PlatformStats

log = logging.getLogger(__name__)

AVATAR_DOWNLOAD_TIMEOUT_SECONDS = 10.0
AVATAR_DOWNLOAD_USER_AGENT = "achievement-banner/1.0"
AVATAR_SUPPORTED_EXTENSIONS = ("png", "jpg", "jpeg", "webp", "gif")

_CONTENT_TYPE_TO_FILE_EXTENSION: dict[str, str] = {
    "image/png":  "png",
    "image/jpeg": "jpg",
    "image/jpg":  "jpg",
    "image/webp": "webp",
    "image/gif":  "gif",
}


def cache_path(cache_dir: Path, platform: str) -> Path:
    """Return the JSON cache file path for the given platform."""
    return Path(cache_dir) / f"{platform}.json"


def avatar_path(cache_dir: Path, platform: str, file_extension: str = "png") -> Path:
    """Return the expected avatar file path for the given platform and extension."""
    return Path(cache_dir) / "avatars" / f"{platform}.{file_extension}"


def load(cache_dir: Path, platform: str) -> PlatformStats | None:
    """Load and deserialize cached platform stats from disk.

    Returns None if the file does not exist or cannot be parsed.
    """
    cache_file_path = cache_path(cache_dir, platform)
    if not cache_file_path.exists():
        return None
    try:
        return PlatformStats.from_dict(json.loads(cache_file_path.read_text(encoding="utf-8")))
    except (ValueError, KeyError) as error:
        log.warning("cache: failed to parse %s: %s", cache_file_path, error)
        return None


def save(cache_dir: Path, stats: PlatformStats) -> None:
    """Serialize and write platform stats to the JSON cache on disk."""
    cache_file_path = cache_path(cache_dir, stats.platform)
    cache_file_path.parent.mkdir(parents=True, exist_ok=True)
    cache_file_path.write_text(json.dumps(stats.to_dict(), indent=2), encoding="utf-8")


def download_avatar(
    cache_dir: Path,
    platform: str,
    image_url: str,
    timeout: float = AVATAR_DOWNLOAD_TIMEOUT_SECONDS,
) -> Path | None:
    """Download the avatar image from `image_url` and store it in the avatar cache.

    Returns the path of the saved file, or None if the download failed.
    Cleans up any existing avatar files for the same platform that use a
    different extension (e.g. stale .png when new format is .webp).
    """
    if not image_url:
        return None
    try:
        response = requests.get(
            image_url,
            timeout=timeout,
            headers={"User-Agent": AVATAR_DOWNLOAD_USER_AGENT},
        )
        response.raise_for_status()
    except requests.RequestException as error:
        log.warning("avatar: download failed for %s: %s", platform, error)
        return None

    content_type_header = response.headers.get("content-type", "")
    file_extension = _extension_from_content_type(content_type_header) or "png"
    avatar_file_path = avatar_path(cache_dir, platform, file_extension)
    avatar_file_path.parent.mkdir(parents=True, exist_ok=True)
    avatar_file_path.write_bytes(response.content)

    # Remove any sibling avatar files for the same platform with a different extension
    for sibling_file in avatar_file_path.parent.glob(f"{platform}.*"):
        if sibling_file != avatar_file_path:
            sibling_file.unlink(missing_ok=True)

    return avatar_file_path


def find_cached_avatar(cache_dir: Path, platform: str) -> Path | None:
    """Return the path to the cached avatar for `platform`, or None if absent.

    Tries each supported extension in order and returns the first that exists.
    """
    for file_extension in AVATAR_SUPPORTED_EXTENSIONS:
        candidate_path = avatar_path(cache_dir, platform, file_extension)
        if candidate_path.exists():
            return candidate_path
    return None


def _extension_from_content_type(content_type_header: str) -> str | None:
    """Parse a Content-Type header value and return the corresponding file extension."""
    normalized_mime_type = content_type_header.split(";")[0].strip().lower()
    return _CONTENT_TYPE_TO_FILE_EXTENSION.get(normalized_mime_type)


# Tests import this under the old short name; keep as alias.
_ext_from_content_type = _extension_from_content_type
