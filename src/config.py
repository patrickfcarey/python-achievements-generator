"""Config loader for profile URLs and display names.

Reads profiles.yaml and, separately, the manual overrides YAML used to
hand-edit displayed values when scraping fails or needs correction.

Known platform keys come from PLATFORM_ORDER in the layout module so there
is one source of truth for which platforms the app supports.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml

from .renderer.layout import PLATFORM_ORDER


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
    """Parse the profiles YAML file and return an AppConfig.

    Only platform keys listed in PLATFORM_ORDER are loaded; unknown keys
    (e.g. "steam") are silently ignored. Raises FileNotFoundError if the
    config file does not exist.
    """
    config_path = Path(path)
    if not config_path.exists():
        raise FileNotFoundError(f"Config not found: {config_path}")

    raw_config_dict = yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}
    loaded_profiles: dict[str, ProfileConfig] = {}

    for platform_key in PLATFORM_ORDER:
        platform_entry = raw_config_dict.get(platform_key)
        if not platform_entry:
            continue
        loaded_profiles[platform_key] = ProfileConfig(
            platform=platform_key,
            profile_url=platform_entry.get("profile_url", ""),
            display_name=platform_entry.get("display_name", ""),
        )

    return AppConfig(profiles=loaded_profiles)


def load_overrides(path: str | Path) -> dict:
    """Load the manual overrides YAML file. Returns an empty dict if absent."""
    overrides_path = Path(path)
    if not overrides_path.exists():
        return {}
    return yaml.safe_load(overrides_path.read_text(encoding="utf-8")) or {}


def save_overrides(path: str | Path, data: dict) -> None:
    """Serialize `data` to the overrides YAML file, preserving insertion order."""
    overrides_path = Path(path)
    overrides_path.parent.mkdir(parents=True, exist_ok=True)
    overrides_path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
