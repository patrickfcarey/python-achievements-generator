"""Config loader for profile URLs and display names."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml
from inspect import signature as _mutmut_signature
from typing import Annotated
from typing import Callable
from typing import ClassVar


MutantDict = Annotated[dict[str, Callable], "Mutant"]


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg = None):
    """Forward call to original or mutated function, depending on the environment"""
    import os
    mutant_under_test = os.environ['MUTANT_UNDER_TEST']
    if mutant_under_test == 'fail':
        from mutmut.__main__ import MutmutProgrammaticFailException
        raise MutmutProgrammaticFailException('Failed programmatically')      
    elif mutant_under_test == 'stats':
        from mutmut.__main__ import record_trampoline_hit
        record_trampoline_hit(orig.__module__ + '.' + orig.__name__)
        result = orig(*call_args, **call_kwargs)
        return result
    prefix = orig.__module__ + '.' + orig.__name__ + '__mutmut_'
    if not mutant_under_test.startswith(prefix):
        result = orig(*call_args, **call_kwargs)
        return result
    mutant_name = mutant_under_test.rpartition('.')[-1]
    if self_arg:
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs)
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs)
    return result


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


def x_load_config__mutmut_orig(path: str | Path) -> AppConfig:
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


def x_load_config__mutmut_1(path: str | Path) -> AppConfig:
    path = None
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


def x_load_config__mutmut_2(path: str | Path) -> AppConfig:
    path = Path(None)
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


def x_load_config__mutmut_3(path: str | Path) -> AppConfig:
    path = Path(path)
    if path.exists():
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


def x_load_config__mutmut_4(path: str | Path) -> AppConfig:
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(None)
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


def x_load_config__mutmut_5(path: str | Path) -> AppConfig:
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Config not found: {path}")
    raw = None
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


def x_load_config__mutmut_6(path: str | Path) -> AppConfig:
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Config not found: {path}")
    raw = yaml.safe_load(path.read_text(encoding="utf-8")) and {}
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


def x_load_config__mutmut_7(path: str | Path) -> AppConfig:
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Config not found: {path}")
    raw = yaml.safe_load(None) or {}
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


def x_load_config__mutmut_8(path: str | Path) -> AppConfig:
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Config not found: {path}")
    raw = yaml.safe_load(path.read_text(encoding=None)) or {}
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


def x_load_config__mutmut_9(path: str | Path) -> AppConfig:
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Config not found: {path}")
    raw = yaml.safe_load(path.read_text(encoding="XXutf-8XX")) or {}
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


def x_load_config__mutmut_10(path: str | Path) -> AppConfig:
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Config not found: {path}")
    raw = yaml.safe_load(path.read_text(encoding="UTF-8")) or {}
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


def x_load_config__mutmut_11(path: str | Path) -> AppConfig:
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Config not found: {path}")
    raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    profiles: dict[str, ProfileConfig] = None
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


def x_load_config__mutmut_12(path: str | Path) -> AppConfig:
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Config not found: {path}")
    raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    profiles: dict[str, ProfileConfig] = {}
    for key in ("XXxboxXX", "psn", "retroachievements"):
        entry = raw.get(key)
        if not entry:
            continue
        profiles[key] = ProfileConfig(
            platform=key,
            profile_url=entry.get("profile_url", ""),
            display_name=entry.get("display_name", ""),
        )
    return AppConfig(profiles=profiles)


def x_load_config__mutmut_13(path: str | Path) -> AppConfig:
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Config not found: {path}")
    raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    profiles: dict[str, ProfileConfig] = {}
    for key in ("XBOX", "psn", "retroachievements"):
        entry = raw.get(key)
        if not entry:
            continue
        profiles[key] = ProfileConfig(
            platform=key,
            profile_url=entry.get("profile_url", ""),
            display_name=entry.get("display_name", ""),
        )
    return AppConfig(profiles=profiles)


def x_load_config__mutmut_14(path: str | Path) -> AppConfig:
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Config not found: {path}")
    raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    profiles: dict[str, ProfileConfig] = {}
    for key in ("xbox", "XXpsnXX", "retroachievements"):
        entry = raw.get(key)
        if not entry:
            continue
        profiles[key] = ProfileConfig(
            platform=key,
            profile_url=entry.get("profile_url", ""),
            display_name=entry.get("display_name", ""),
        )
    return AppConfig(profiles=profiles)


def x_load_config__mutmut_15(path: str | Path) -> AppConfig:
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Config not found: {path}")
    raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    profiles: dict[str, ProfileConfig] = {}
    for key in ("xbox", "PSN", "retroachievements"):
        entry = raw.get(key)
        if not entry:
            continue
        profiles[key] = ProfileConfig(
            platform=key,
            profile_url=entry.get("profile_url", ""),
            display_name=entry.get("display_name", ""),
        )
    return AppConfig(profiles=profiles)


def x_load_config__mutmut_16(path: str | Path) -> AppConfig:
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Config not found: {path}")
    raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    profiles: dict[str, ProfileConfig] = {}
    for key in ("xbox", "psn", "XXretroachievementsXX"):
        entry = raw.get(key)
        if not entry:
            continue
        profiles[key] = ProfileConfig(
            platform=key,
            profile_url=entry.get("profile_url", ""),
            display_name=entry.get("display_name", ""),
        )
    return AppConfig(profiles=profiles)


def x_load_config__mutmut_17(path: str | Path) -> AppConfig:
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Config not found: {path}")
    raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    profiles: dict[str, ProfileConfig] = {}
    for key in ("xbox", "psn", "RETROACHIEVEMENTS"):
        entry = raw.get(key)
        if not entry:
            continue
        profiles[key] = ProfileConfig(
            platform=key,
            profile_url=entry.get("profile_url", ""),
            display_name=entry.get("display_name", ""),
        )
    return AppConfig(profiles=profiles)


def x_load_config__mutmut_18(path: str | Path) -> AppConfig:
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Config not found: {path}")
    raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    profiles: dict[str, ProfileConfig] = {}
    for key in ("xbox", "psn", "retroachievements"):
        entry = None
        if not entry:
            continue
        profiles[key] = ProfileConfig(
            platform=key,
            profile_url=entry.get("profile_url", ""),
            display_name=entry.get("display_name", ""),
        )
    return AppConfig(profiles=profiles)


def x_load_config__mutmut_19(path: str | Path) -> AppConfig:
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Config not found: {path}")
    raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    profiles: dict[str, ProfileConfig] = {}
    for key in ("xbox", "psn", "retroachievements"):
        entry = raw.get(None)
        if not entry:
            continue
        profiles[key] = ProfileConfig(
            platform=key,
            profile_url=entry.get("profile_url", ""),
            display_name=entry.get("display_name", ""),
        )
    return AppConfig(profiles=profiles)


def x_load_config__mutmut_20(path: str | Path) -> AppConfig:
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Config not found: {path}")
    raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    profiles: dict[str, ProfileConfig] = {}
    for key in ("xbox", "psn", "retroachievements"):
        entry = raw.get(key)
        if entry:
            continue
        profiles[key] = ProfileConfig(
            platform=key,
            profile_url=entry.get("profile_url", ""),
            display_name=entry.get("display_name", ""),
        )
    return AppConfig(profiles=profiles)


def x_load_config__mutmut_21(path: str | Path) -> AppConfig:
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Config not found: {path}")
    raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    profiles: dict[str, ProfileConfig] = {}
    for key in ("xbox", "psn", "retroachievements"):
        entry = raw.get(key)
        if not entry:
            break
        profiles[key] = ProfileConfig(
            platform=key,
            profile_url=entry.get("profile_url", ""),
            display_name=entry.get("display_name", ""),
        )
    return AppConfig(profiles=profiles)


def x_load_config__mutmut_22(path: str | Path) -> AppConfig:
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Config not found: {path}")
    raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    profiles: dict[str, ProfileConfig] = {}
    for key in ("xbox", "psn", "retroachievements"):
        entry = raw.get(key)
        if not entry:
            continue
        profiles[key] = None
    return AppConfig(profiles=profiles)


def x_load_config__mutmut_23(path: str | Path) -> AppConfig:
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
            platform=None,
            profile_url=entry.get("profile_url", ""),
            display_name=entry.get("display_name", ""),
        )
    return AppConfig(profiles=profiles)


def x_load_config__mutmut_24(path: str | Path) -> AppConfig:
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
            profile_url=None,
            display_name=entry.get("display_name", ""),
        )
    return AppConfig(profiles=profiles)


def x_load_config__mutmut_25(path: str | Path) -> AppConfig:
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
            display_name=None,
        )
    return AppConfig(profiles=profiles)


def x_load_config__mutmut_26(path: str | Path) -> AppConfig:
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
            profile_url=entry.get("profile_url", ""),
            display_name=entry.get("display_name", ""),
        )
    return AppConfig(profiles=profiles)


def x_load_config__mutmut_27(path: str | Path) -> AppConfig:
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
            display_name=entry.get("display_name", ""),
        )
    return AppConfig(profiles=profiles)


def x_load_config__mutmut_28(path: str | Path) -> AppConfig:
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
            )
    return AppConfig(profiles=profiles)


def x_load_config__mutmut_29(path: str | Path) -> AppConfig:
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
            profile_url=entry.get(None, ""),
            display_name=entry.get("display_name", ""),
        )
    return AppConfig(profiles=profiles)


def x_load_config__mutmut_30(path: str | Path) -> AppConfig:
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
            profile_url=entry.get("profile_url", None),
            display_name=entry.get("display_name", ""),
        )
    return AppConfig(profiles=profiles)


def x_load_config__mutmut_31(path: str | Path) -> AppConfig:
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
            profile_url=entry.get(""),
            display_name=entry.get("display_name", ""),
        )
    return AppConfig(profiles=profiles)


def x_load_config__mutmut_32(path: str | Path) -> AppConfig:
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
            profile_url=entry.get("profile_url", ),
            display_name=entry.get("display_name", ""),
        )
    return AppConfig(profiles=profiles)


def x_load_config__mutmut_33(path: str | Path) -> AppConfig:
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
            profile_url=entry.get("XXprofile_urlXX", ""),
            display_name=entry.get("display_name", ""),
        )
    return AppConfig(profiles=profiles)


def x_load_config__mutmut_34(path: str | Path) -> AppConfig:
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
            profile_url=entry.get("PROFILE_URL", ""),
            display_name=entry.get("display_name", ""),
        )
    return AppConfig(profiles=profiles)


def x_load_config__mutmut_35(path: str | Path) -> AppConfig:
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
            profile_url=entry.get("profile_url", "XXXX"),
            display_name=entry.get("display_name", ""),
        )
    return AppConfig(profiles=profiles)


def x_load_config__mutmut_36(path: str | Path) -> AppConfig:
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
            display_name=entry.get(None, ""),
        )
    return AppConfig(profiles=profiles)


def x_load_config__mutmut_37(path: str | Path) -> AppConfig:
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
            display_name=entry.get("display_name", None),
        )
    return AppConfig(profiles=profiles)


def x_load_config__mutmut_38(path: str | Path) -> AppConfig:
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
            display_name=entry.get(""),
        )
    return AppConfig(profiles=profiles)


def x_load_config__mutmut_39(path: str | Path) -> AppConfig:
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
            display_name=entry.get("display_name", ),
        )
    return AppConfig(profiles=profiles)


def x_load_config__mutmut_40(path: str | Path) -> AppConfig:
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
            display_name=entry.get("XXdisplay_nameXX", ""),
        )
    return AppConfig(profiles=profiles)


def x_load_config__mutmut_41(path: str | Path) -> AppConfig:
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
            display_name=entry.get("DISPLAY_NAME", ""),
        )
    return AppConfig(profiles=profiles)


def x_load_config__mutmut_42(path: str | Path) -> AppConfig:
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
            display_name=entry.get("display_name", "XXXX"),
        )
    return AppConfig(profiles=profiles)


def x_load_config__mutmut_43(path: str | Path) -> AppConfig:
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
    return AppConfig(profiles=None)

x_load_config__mutmut_mutants : ClassVar[MutantDict] = {
'x_load_config__mutmut_1': x_load_config__mutmut_1, 
    'x_load_config__mutmut_2': x_load_config__mutmut_2, 
    'x_load_config__mutmut_3': x_load_config__mutmut_3, 
    'x_load_config__mutmut_4': x_load_config__mutmut_4, 
    'x_load_config__mutmut_5': x_load_config__mutmut_5, 
    'x_load_config__mutmut_6': x_load_config__mutmut_6, 
    'x_load_config__mutmut_7': x_load_config__mutmut_7, 
    'x_load_config__mutmut_8': x_load_config__mutmut_8, 
    'x_load_config__mutmut_9': x_load_config__mutmut_9, 
    'x_load_config__mutmut_10': x_load_config__mutmut_10, 
    'x_load_config__mutmut_11': x_load_config__mutmut_11, 
    'x_load_config__mutmut_12': x_load_config__mutmut_12, 
    'x_load_config__mutmut_13': x_load_config__mutmut_13, 
    'x_load_config__mutmut_14': x_load_config__mutmut_14, 
    'x_load_config__mutmut_15': x_load_config__mutmut_15, 
    'x_load_config__mutmut_16': x_load_config__mutmut_16, 
    'x_load_config__mutmut_17': x_load_config__mutmut_17, 
    'x_load_config__mutmut_18': x_load_config__mutmut_18, 
    'x_load_config__mutmut_19': x_load_config__mutmut_19, 
    'x_load_config__mutmut_20': x_load_config__mutmut_20, 
    'x_load_config__mutmut_21': x_load_config__mutmut_21, 
    'x_load_config__mutmut_22': x_load_config__mutmut_22, 
    'x_load_config__mutmut_23': x_load_config__mutmut_23, 
    'x_load_config__mutmut_24': x_load_config__mutmut_24, 
    'x_load_config__mutmut_25': x_load_config__mutmut_25, 
    'x_load_config__mutmut_26': x_load_config__mutmut_26, 
    'x_load_config__mutmut_27': x_load_config__mutmut_27, 
    'x_load_config__mutmut_28': x_load_config__mutmut_28, 
    'x_load_config__mutmut_29': x_load_config__mutmut_29, 
    'x_load_config__mutmut_30': x_load_config__mutmut_30, 
    'x_load_config__mutmut_31': x_load_config__mutmut_31, 
    'x_load_config__mutmut_32': x_load_config__mutmut_32, 
    'x_load_config__mutmut_33': x_load_config__mutmut_33, 
    'x_load_config__mutmut_34': x_load_config__mutmut_34, 
    'x_load_config__mutmut_35': x_load_config__mutmut_35, 
    'x_load_config__mutmut_36': x_load_config__mutmut_36, 
    'x_load_config__mutmut_37': x_load_config__mutmut_37, 
    'x_load_config__mutmut_38': x_load_config__mutmut_38, 
    'x_load_config__mutmut_39': x_load_config__mutmut_39, 
    'x_load_config__mutmut_40': x_load_config__mutmut_40, 
    'x_load_config__mutmut_41': x_load_config__mutmut_41, 
    'x_load_config__mutmut_42': x_load_config__mutmut_42, 
    'x_load_config__mutmut_43': x_load_config__mutmut_43
}

def load_config(*args, **kwargs):
    result = _mutmut_trampoline(x_load_config__mutmut_orig, x_load_config__mutmut_mutants, args, kwargs)
    return result 

load_config.__signature__ = _mutmut_signature(x_load_config__mutmut_orig)
x_load_config__mutmut_orig.__name__ = 'x_load_config'


def x_load_overrides__mutmut_orig(path: str | Path) -> dict:
    path = Path(path)
    if not path.exists():
        return {}
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def x_load_overrides__mutmut_1(path: str | Path) -> dict:
    path = None
    if not path.exists():
        return {}
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def x_load_overrides__mutmut_2(path: str | Path) -> dict:
    path = Path(None)
    if not path.exists():
        return {}
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def x_load_overrides__mutmut_3(path: str | Path) -> dict:
    path = Path(path)
    if path.exists():
        return {}
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def x_load_overrides__mutmut_4(path: str | Path) -> dict:
    path = Path(path)
    if not path.exists():
        return {}
    return yaml.safe_load(path.read_text(encoding="utf-8")) and {}


def x_load_overrides__mutmut_5(path: str | Path) -> dict:
    path = Path(path)
    if not path.exists():
        return {}
    return yaml.safe_load(None) or {}


def x_load_overrides__mutmut_6(path: str | Path) -> dict:
    path = Path(path)
    if not path.exists():
        return {}
    return yaml.safe_load(path.read_text(encoding=None)) or {}


def x_load_overrides__mutmut_7(path: str | Path) -> dict:
    path = Path(path)
    if not path.exists():
        return {}
    return yaml.safe_load(path.read_text(encoding="XXutf-8XX")) or {}


def x_load_overrides__mutmut_8(path: str | Path) -> dict:
    path = Path(path)
    if not path.exists():
        return {}
    return yaml.safe_load(path.read_text(encoding="UTF-8")) or {}

x_load_overrides__mutmut_mutants : ClassVar[MutantDict] = {
'x_load_overrides__mutmut_1': x_load_overrides__mutmut_1, 
    'x_load_overrides__mutmut_2': x_load_overrides__mutmut_2, 
    'x_load_overrides__mutmut_3': x_load_overrides__mutmut_3, 
    'x_load_overrides__mutmut_4': x_load_overrides__mutmut_4, 
    'x_load_overrides__mutmut_5': x_load_overrides__mutmut_5, 
    'x_load_overrides__mutmut_6': x_load_overrides__mutmut_6, 
    'x_load_overrides__mutmut_7': x_load_overrides__mutmut_7, 
    'x_load_overrides__mutmut_8': x_load_overrides__mutmut_8
}

def load_overrides(*args, **kwargs):
    result = _mutmut_trampoline(x_load_overrides__mutmut_orig, x_load_overrides__mutmut_mutants, args, kwargs)
    return result 

load_overrides.__signature__ = _mutmut_signature(x_load_overrides__mutmut_orig)
x_load_overrides__mutmut_orig.__name__ = 'x_load_overrides'


def x_save_overrides__mutmut_orig(path: str | Path, data: dict) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")


def x_save_overrides__mutmut_1(path: str | Path, data: dict) -> None:
    path = None
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")


def x_save_overrides__mutmut_2(path: str | Path, data: dict) -> None:
    path = Path(None)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")


def x_save_overrides__mutmut_3(path: str | Path, data: dict) -> None:
    path = Path(path)
    path.parent.mkdir(parents=None, exist_ok=True)
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")


def x_save_overrides__mutmut_4(path: str | Path, data: dict) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=None)
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")


def x_save_overrides__mutmut_5(path: str | Path, data: dict) -> None:
    path = Path(path)
    path.parent.mkdir(exist_ok=True)
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")


def x_save_overrides__mutmut_6(path: str | Path, data: dict) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, )
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")


def x_save_overrides__mutmut_7(path: str | Path, data: dict) -> None:
    path = Path(path)
    path.parent.mkdir(parents=False, exist_ok=True)
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")


def x_save_overrides__mutmut_8(path: str | Path, data: dict) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=False)
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")


def x_save_overrides__mutmut_9(path: str | Path, data: dict) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(None, encoding="utf-8")


def x_save_overrides__mutmut_10(path: str | Path, data: dict) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding=None)


def x_save_overrides__mutmut_11(path: str | Path, data: dict) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(encoding="utf-8")


def x_save_overrides__mutmut_12(path: str | Path, data: dict) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(data, sort_keys=False), )


def x_save_overrides__mutmut_13(path: str | Path, data: dict) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(None, sort_keys=False), encoding="utf-8")


def x_save_overrides__mutmut_14(path: str | Path, data: dict) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(data, sort_keys=None), encoding="utf-8")


def x_save_overrides__mutmut_15(path: str | Path, data: dict) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(sort_keys=False), encoding="utf-8")


def x_save_overrides__mutmut_16(path: str | Path, data: dict) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(data, ), encoding="utf-8")


def x_save_overrides__mutmut_17(path: str | Path, data: dict) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(data, sort_keys=True), encoding="utf-8")


def x_save_overrides__mutmut_18(path: str | Path, data: dict) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="XXutf-8XX")


def x_save_overrides__mutmut_19(path: str | Path, data: dict) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="UTF-8")

x_save_overrides__mutmut_mutants : ClassVar[MutantDict] = {
'x_save_overrides__mutmut_1': x_save_overrides__mutmut_1, 
    'x_save_overrides__mutmut_2': x_save_overrides__mutmut_2, 
    'x_save_overrides__mutmut_3': x_save_overrides__mutmut_3, 
    'x_save_overrides__mutmut_4': x_save_overrides__mutmut_4, 
    'x_save_overrides__mutmut_5': x_save_overrides__mutmut_5, 
    'x_save_overrides__mutmut_6': x_save_overrides__mutmut_6, 
    'x_save_overrides__mutmut_7': x_save_overrides__mutmut_7, 
    'x_save_overrides__mutmut_8': x_save_overrides__mutmut_8, 
    'x_save_overrides__mutmut_9': x_save_overrides__mutmut_9, 
    'x_save_overrides__mutmut_10': x_save_overrides__mutmut_10, 
    'x_save_overrides__mutmut_11': x_save_overrides__mutmut_11, 
    'x_save_overrides__mutmut_12': x_save_overrides__mutmut_12, 
    'x_save_overrides__mutmut_13': x_save_overrides__mutmut_13, 
    'x_save_overrides__mutmut_14': x_save_overrides__mutmut_14, 
    'x_save_overrides__mutmut_15': x_save_overrides__mutmut_15, 
    'x_save_overrides__mutmut_16': x_save_overrides__mutmut_16, 
    'x_save_overrides__mutmut_17': x_save_overrides__mutmut_17, 
    'x_save_overrides__mutmut_18': x_save_overrides__mutmut_18, 
    'x_save_overrides__mutmut_19': x_save_overrides__mutmut_19
}

def save_overrides(*args, **kwargs):
    result = _mutmut_trampoline(x_save_overrides__mutmut_orig, x_save_overrides__mutmut_mutants, args, kwargs)
    return result 

save_overrides.__signature__ = _mutmut_signature(x_save_overrides__mutmut_orig)
x_save_overrides__mutmut_orig.__name__ = 'x_save_overrides'
