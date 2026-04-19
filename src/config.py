"""Config loader for profile URLs and display names."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml


@dataclass
class ProfileConfig:
    platform: str
    profile_url: str
    display_name: str


@dataclass
class AppConfig:
    profiles: dict[str, ProfileConfig]

    def get(self, platform: str) -> ProfileConfig | None:
        return self.profiles.get(platform)


def load_config(path: str | Path) -> AppConfig:
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Config not found: {path}")
    raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    profiles: dict[str, ProfileConfig] = {}
    for key in ("xbox", "psn", "retroachievements"):
        entry = raw.get(key)
        if not entry:
            continue
        profiles[key] = ProfileConfig(
            platform=key,
            profile_url=entry.get("profile_url", ""),
            display_name=entry.get("display_name", ""),
        )
    return AppConfig(profiles=profiles)


def load_overrides(path: str | Path) -> dict:
    path = Path(path)
    if not path.exists():
        return {}
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def save_overrides(path: str | Path, data: dict) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
