"""Per-platform JSON cache and avatar cache."""
from __future__ import annotations

import json
import logging
from pathlib import Path

import requests

from .models import PlatformStats

log = logging.getLogger(__name__)
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


def x_cache_path__mutmut_orig(cache_dir: Path, platform: str) -> Path:
    return Path(cache_dir) / f"{platform}.json"


def x_cache_path__mutmut_1(cache_dir: Path, platform: str) -> Path:
    return Path(cache_dir) * f"{platform}.json"


def x_cache_path__mutmut_2(cache_dir: Path, platform: str) -> Path:
    return Path(None) / f"{platform}.json"

x_cache_path__mutmut_mutants : ClassVar[MutantDict] = {
'x_cache_path__mutmut_1': x_cache_path__mutmut_1, 
    'x_cache_path__mutmut_2': x_cache_path__mutmut_2
}

def cache_path(*args, **kwargs):
    result = _mutmut_trampoline(x_cache_path__mutmut_orig, x_cache_path__mutmut_mutants, args, kwargs)
    return result 

cache_path.__signature__ = _mutmut_signature(x_cache_path__mutmut_orig)
x_cache_path__mutmut_orig.__name__ = 'x_cache_path'


def x_avatar_path__mutmut_orig(cache_dir: Path, platform: str, ext: str = "png") -> Path:
    return Path(cache_dir) / "avatars" / f"{platform}.{ext}"


def x_avatar_path__mutmut_1(cache_dir: Path, platform: str, ext: str = "XXpngXX") -> Path:
    return Path(cache_dir) / "avatars" / f"{platform}.{ext}"


def x_avatar_path__mutmut_2(cache_dir: Path, platform: str, ext: str = "PNG") -> Path:
    return Path(cache_dir) / "avatars" / f"{platform}.{ext}"


def x_avatar_path__mutmut_3(cache_dir: Path, platform: str, ext: str = "png") -> Path:
    return Path(cache_dir) / "avatars" * f"{platform}.{ext}"


def x_avatar_path__mutmut_4(cache_dir: Path, platform: str, ext: str = "png") -> Path:
    return Path(cache_dir) * "avatars" / f"{platform}.{ext}"


def x_avatar_path__mutmut_5(cache_dir: Path, platform: str, ext: str = "png") -> Path:
    return Path(None) / "avatars" / f"{platform}.{ext}"


def x_avatar_path__mutmut_6(cache_dir: Path, platform: str, ext: str = "png") -> Path:
    return Path(cache_dir) / "XXavatarsXX" / f"{platform}.{ext}"


def x_avatar_path__mutmut_7(cache_dir: Path, platform: str, ext: str = "png") -> Path:
    return Path(cache_dir) / "AVATARS" / f"{platform}.{ext}"

x_avatar_path__mutmut_mutants : ClassVar[MutantDict] = {
'x_avatar_path__mutmut_1': x_avatar_path__mutmut_1, 
    'x_avatar_path__mutmut_2': x_avatar_path__mutmut_2, 
    'x_avatar_path__mutmut_3': x_avatar_path__mutmut_3, 
    'x_avatar_path__mutmut_4': x_avatar_path__mutmut_4, 
    'x_avatar_path__mutmut_5': x_avatar_path__mutmut_5, 
    'x_avatar_path__mutmut_6': x_avatar_path__mutmut_6, 
    'x_avatar_path__mutmut_7': x_avatar_path__mutmut_7
}

def avatar_path(*args, **kwargs):
    result = _mutmut_trampoline(x_avatar_path__mutmut_orig, x_avatar_path__mutmut_mutants, args, kwargs)
    return result 

avatar_path.__signature__ = _mutmut_signature(x_avatar_path__mutmut_orig)
x_avatar_path__mutmut_orig.__name__ = 'x_avatar_path'


def x_load__mutmut_orig(cache_dir: Path, platform: str) -> PlatformStats | None:
    p = cache_path(cache_dir, platform)
    if not p.exists():
        return None
    try:
        return PlatformStats.from_dict(json.loads(p.read_text(encoding="utf-8")))
    except (ValueError, KeyError) as exc:
        log.warning("cache: failed to parse %s: %s", p, exc)
        return None


def x_load__mutmut_1(cache_dir: Path, platform: str) -> PlatformStats | None:
    p = None
    if not p.exists():
        return None
    try:
        return PlatformStats.from_dict(json.loads(p.read_text(encoding="utf-8")))
    except (ValueError, KeyError) as exc:
        log.warning("cache: failed to parse %s: %s", p, exc)
        return None


def x_load__mutmut_2(cache_dir: Path, platform: str) -> PlatformStats | None:
    p = cache_path(None, platform)
    if not p.exists():
        return None
    try:
        return PlatformStats.from_dict(json.loads(p.read_text(encoding="utf-8")))
    except (ValueError, KeyError) as exc:
        log.warning("cache: failed to parse %s: %s", p, exc)
        return None


def x_load__mutmut_3(cache_dir: Path, platform: str) -> PlatformStats | None:
    p = cache_path(cache_dir, None)
    if not p.exists():
        return None
    try:
        return PlatformStats.from_dict(json.loads(p.read_text(encoding="utf-8")))
    except (ValueError, KeyError) as exc:
        log.warning("cache: failed to parse %s: %s", p, exc)
        return None


def x_load__mutmut_4(cache_dir: Path, platform: str) -> PlatformStats | None:
    p = cache_path(platform)
    if not p.exists():
        return None
    try:
        return PlatformStats.from_dict(json.loads(p.read_text(encoding="utf-8")))
    except (ValueError, KeyError) as exc:
        log.warning("cache: failed to parse %s: %s", p, exc)
        return None


def x_load__mutmut_5(cache_dir: Path, platform: str) -> PlatformStats | None:
    p = cache_path(cache_dir, )
    if not p.exists():
        return None
    try:
        return PlatformStats.from_dict(json.loads(p.read_text(encoding="utf-8")))
    except (ValueError, KeyError) as exc:
        log.warning("cache: failed to parse %s: %s", p, exc)
        return None


def x_load__mutmut_6(cache_dir: Path, platform: str) -> PlatformStats | None:
    p = cache_path(cache_dir, platform)
    if p.exists():
        return None
    try:
        return PlatformStats.from_dict(json.loads(p.read_text(encoding="utf-8")))
    except (ValueError, KeyError) as exc:
        log.warning("cache: failed to parse %s: %s", p, exc)
        return None


def x_load__mutmut_7(cache_dir: Path, platform: str) -> PlatformStats | None:
    p = cache_path(cache_dir, platform)
    if not p.exists():
        return None
    try:
        return PlatformStats.from_dict(None)
    except (ValueError, KeyError) as exc:
        log.warning("cache: failed to parse %s: %s", p, exc)
        return None


def x_load__mutmut_8(cache_dir: Path, platform: str) -> PlatformStats | None:
    p = cache_path(cache_dir, platform)
    if not p.exists():
        return None
    try:
        return PlatformStats.from_dict(json.loads(None))
    except (ValueError, KeyError) as exc:
        log.warning("cache: failed to parse %s: %s", p, exc)
        return None


def x_load__mutmut_9(cache_dir: Path, platform: str) -> PlatformStats | None:
    p = cache_path(cache_dir, platform)
    if not p.exists():
        return None
    try:
        return PlatformStats.from_dict(json.loads(p.read_text(encoding=None)))
    except (ValueError, KeyError) as exc:
        log.warning("cache: failed to parse %s: %s", p, exc)
        return None


def x_load__mutmut_10(cache_dir: Path, platform: str) -> PlatformStats | None:
    p = cache_path(cache_dir, platform)
    if not p.exists():
        return None
    try:
        return PlatformStats.from_dict(json.loads(p.read_text(encoding="XXutf-8XX")))
    except (ValueError, KeyError) as exc:
        log.warning("cache: failed to parse %s: %s", p, exc)
        return None


def x_load__mutmut_11(cache_dir: Path, platform: str) -> PlatformStats | None:
    p = cache_path(cache_dir, platform)
    if not p.exists():
        return None
    try:
        return PlatformStats.from_dict(json.loads(p.read_text(encoding="UTF-8")))
    except (ValueError, KeyError) as exc:
        log.warning("cache: failed to parse %s: %s", p, exc)
        return None


def x_load__mutmut_12(cache_dir: Path, platform: str) -> PlatformStats | None:
    p = cache_path(cache_dir, platform)
    if not p.exists():
        return None
    try:
        return PlatformStats.from_dict(json.loads(p.read_text(encoding="utf-8")))
    except (ValueError, KeyError) as exc:
        log.warning(None, p, exc)
        return None


def x_load__mutmut_13(cache_dir: Path, platform: str) -> PlatformStats | None:
    p = cache_path(cache_dir, platform)
    if not p.exists():
        return None
    try:
        return PlatformStats.from_dict(json.loads(p.read_text(encoding="utf-8")))
    except (ValueError, KeyError) as exc:
        log.warning("cache: failed to parse %s: %s", None, exc)
        return None


def x_load__mutmut_14(cache_dir: Path, platform: str) -> PlatformStats | None:
    p = cache_path(cache_dir, platform)
    if not p.exists():
        return None
    try:
        return PlatformStats.from_dict(json.loads(p.read_text(encoding="utf-8")))
    except (ValueError, KeyError) as exc:
        log.warning("cache: failed to parse %s: %s", p, None)
        return None


def x_load__mutmut_15(cache_dir: Path, platform: str) -> PlatformStats | None:
    p = cache_path(cache_dir, platform)
    if not p.exists():
        return None
    try:
        return PlatformStats.from_dict(json.loads(p.read_text(encoding="utf-8")))
    except (ValueError, KeyError) as exc:
        log.warning(p, exc)
        return None


def x_load__mutmut_16(cache_dir: Path, platform: str) -> PlatformStats | None:
    p = cache_path(cache_dir, platform)
    if not p.exists():
        return None
    try:
        return PlatformStats.from_dict(json.loads(p.read_text(encoding="utf-8")))
    except (ValueError, KeyError) as exc:
        log.warning("cache: failed to parse %s: %s", exc)
        return None


def x_load__mutmut_17(cache_dir: Path, platform: str) -> PlatformStats | None:
    p = cache_path(cache_dir, platform)
    if not p.exists():
        return None
    try:
        return PlatformStats.from_dict(json.loads(p.read_text(encoding="utf-8")))
    except (ValueError, KeyError) as exc:
        log.warning("cache: failed to parse %s: %s", p, )
        return None


def x_load__mutmut_18(cache_dir: Path, platform: str) -> PlatformStats | None:
    p = cache_path(cache_dir, platform)
    if not p.exists():
        return None
    try:
        return PlatformStats.from_dict(json.loads(p.read_text(encoding="utf-8")))
    except (ValueError, KeyError) as exc:
        log.warning("XXcache: failed to parse %s: %sXX", p, exc)
        return None


def x_load__mutmut_19(cache_dir: Path, platform: str) -> PlatformStats | None:
    p = cache_path(cache_dir, platform)
    if not p.exists():
        return None
    try:
        return PlatformStats.from_dict(json.loads(p.read_text(encoding="utf-8")))
    except (ValueError, KeyError) as exc:
        log.warning("CACHE: FAILED TO PARSE %S: %S", p, exc)
        return None

x_load__mutmut_mutants : ClassVar[MutantDict] = {
'x_load__mutmut_1': x_load__mutmut_1, 
    'x_load__mutmut_2': x_load__mutmut_2, 
    'x_load__mutmut_3': x_load__mutmut_3, 
    'x_load__mutmut_4': x_load__mutmut_4, 
    'x_load__mutmut_5': x_load__mutmut_5, 
    'x_load__mutmut_6': x_load__mutmut_6, 
    'x_load__mutmut_7': x_load__mutmut_7, 
    'x_load__mutmut_8': x_load__mutmut_8, 
    'x_load__mutmut_9': x_load__mutmut_9, 
    'x_load__mutmut_10': x_load__mutmut_10, 
    'x_load__mutmut_11': x_load__mutmut_11, 
    'x_load__mutmut_12': x_load__mutmut_12, 
    'x_load__mutmut_13': x_load__mutmut_13, 
    'x_load__mutmut_14': x_load__mutmut_14, 
    'x_load__mutmut_15': x_load__mutmut_15, 
    'x_load__mutmut_16': x_load__mutmut_16, 
    'x_load__mutmut_17': x_load__mutmut_17, 
    'x_load__mutmut_18': x_load__mutmut_18, 
    'x_load__mutmut_19': x_load__mutmut_19
}

def load(*args, **kwargs):
    result = _mutmut_trampoline(x_load__mutmut_orig, x_load__mutmut_mutants, args, kwargs)
    return result 

load.__signature__ = _mutmut_signature(x_load__mutmut_orig)
x_load__mutmut_orig.__name__ = 'x_load'


def x_save__mutmut_orig(cache_dir: Path, stats: PlatformStats) -> None:
    p = cache_path(cache_dir, stats.platform)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(stats.to_dict(), indent=2), encoding="utf-8")


def x_save__mutmut_1(cache_dir: Path, stats: PlatformStats) -> None:
    p = None
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(stats.to_dict(), indent=2), encoding="utf-8")


def x_save__mutmut_2(cache_dir: Path, stats: PlatformStats) -> None:
    p = cache_path(None, stats.platform)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(stats.to_dict(), indent=2), encoding="utf-8")


def x_save__mutmut_3(cache_dir: Path, stats: PlatformStats) -> None:
    p = cache_path(cache_dir, None)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(stats.to_dict(), indent=2), encoding="utf-8")


def x_save__mutmut_4(cache_dir: Path, stats: PlatformStats) -> None:
    p = cache_path(stats.platform)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(stats.to_dict(), indent=2), encoding="utf-8")


def x_save__mutmut_5(cache_dir: Path, stats: PlatformStats) -> None:
    p = cache_path(cache_dir, )
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(stats.to_dict(), indent=2), encoding="utf-8")


def x_save__mutmut_6(cache_dir: Path, stats: PlatformStats) -> None:
    p = cache_path(cache_dir, stats.platform)
    p.parent.mkdir(parents=None, exist_ok=True)
    p.write_text(json.dumps(stats.to_dict(), indent=2), encoding="utf-8")


def x_save__mutmut_7(cache_dir: Path, stats: PlatformStats) -> None:
    p = cache_path(cache_dir, stats.platform)
    p.parent.mkdir(parents=True, exist_ok=None)
    p.write_text(json.dumps(stats.to_dict(), indent=2), encoding="utf-8")


def x_save__mutmut_8(cache_dir: Path, stats: PlatformStats) -> None:
    p = cache_path(cache_dir, stats.platform)
    p.parent.mkdir(exist_ok=True)
    p.write_text(json.dumps(stats.to_dict(), indent=2), encoding="utf-8")


def x_save__mutmut_9(cache_dir: Path, stats: PlatformStats) -> None:
    p = cache_path(cache_dir, stats.platform)
    p.parent.mkdir(parents=True, )
    p.write_text(json.dumps(stats.to_dict(), indent=2), encoding="utf-8")


def x_save__mutmut_10(cache_dir: Path, stats: PlatformStats) -> None:
    p = cache_path(cache_dir, stats.platform)
    p.parent.mkdir(parents=False, exist_ok=True)
    p.write_text(json.dumps(stats.to_dict(), indent=2), encoding="utf-8")


def x_save__mutmut_11(cache_dir: Path, stats: PlatformStats) -> None:
    p = cache_path(cache_dir, stats.platform)
    p.parent.mkdir(parents=True, exist_ok=False)
    p.write_text(json.dumps(stats.to_dict(), indent=2), encoding="utf-8")


def x_save__mutmut_12(cache_dir: Path, stats: PlatformStats) -> None:
    p = cache_path(cache_dir, stats.platform)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(None, encoding="utf-8")


def x_save__mutmut_13(cache_dir: Path, stats: PlatformStats) -> None:
    p = cache_path(cache_dir, stats.platform)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(stats.to_dict(), indent=2), encoding=None)


def x_save__mutmut_14(cache_dir: Path, stats: PlatformStats) -> None:
    p = cache_path(cache_dir, stats.platform)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(encoding="utf-8")


def x_save__mutmut_15(cache_dir: Path, stats: PlatformStats) -> None:
    p = cache_path(cache_dir, stats.platform)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(stats.to_dict(), indent=2), )


def x_save__mutmut_16(cache_dir: Path, stats: PlatformStats) -> None:
    p = cache_path(cache_dir, stats.platform)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(None, indent=2), encoding="utf-8")


def x_save__mutmut_17(cache_dir: Path, stats: PlatformStats) -> None:
    p = cache_path(cache_dir, stats.platform)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(stats.to_dict(), indent=None), encoding="utf-8")


def x_save__mutmut_18(cache_dir: Path, stats: PlatformStats) -> None:
    p = cache_path(cache_dir, stats.platform)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(indent=2), encoding="utf-8")


def x_save__mutmut_19(cache_dir: Path, stats: PlatformStats) -> None:
    p = cache_path(cache_dir, stats.platform)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(stats.to_dict(), ), encoding="utf-8")


def x_save__mutmut_20(cache_dir: Path, stats: PlatformStats) -> None:
    p = cache_path(cache_dir, stats.platform)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(stats.to_dict(), indent=3), encoding="utf-8")


def x_save__mutmut_21(cache_dir: Path, stats: PlatformStats) -> None:
    p = cache_path(cache_dir, stats.platform)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(stats.to_dict(), indent=2), encoding="XXutf-8XX")


def x_save__mutmut_22(cache_dir: Path, stats: PlatformStats) -> None:
    p = cache_path(cache_dir, stats.platform)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(stats.to_dict(), indent=2), encoding="UTF-8")

x_save__mutmut_mutants : ClassVar[MutantDict] = {
'x_save__mutmut_1': x_save__mutmut_1, 
    'x_save__mutmut_2': x_save__mutmut_2, 
    'x_save__mutmut_3': x_save__mutmut_3, 
    'x_save__mutmut_4': x_save__mutmut_4, 
    'x_save__mutmut_5': x_save__mutmut_5, 
    'x_save__mutmut_6': x_save__mutmut_6, 
    'x_save__mutmut_7': x_save__mutmut_7, 
    'x_save__mutmut_8': x_save__mutmut_8, 
    'x_save__mutmut_9': x_save__mutmut_9, 
    'x_save__mutmut_10': x_save__mutmut_10, 
    'x_save__mutmut_11': x_save__mutmut_11, 
    'x_save__mutmut_12': x_save__mutmut_12, 
    'x_save__mutmut_13': x_save__mutmut_13, 
    'x_save__mutmut_14': x_save__mutmut_14, 
    'x_save__mutmut_15': x_save__mutmut_15, 
    'x_save__mutmut_16': x_save__mutmut_16, 
    'x_save__mutmut_17': x_save__mutmut_17, 
    'x_save__mutmut_18': x_save__mutmut_18, 
    'x_save__mutmut_19': x_save__mutmut_19, 
    'x_save__mutmut_20': x_save__mutmut_20, 
    'x_save__mutmut_21': x_save__mutmut_21, 
    'x_save__mutmut_22': x_save__mutmut_22
}

def save(*args, **kwargs):
    result = _mutmut_trampoline(x_save__mutmut_orig, x_save__mutmut_mutants, args, kwargs)
    return result 

save.__signature__ = _mutmut_signature(x_save__mutmut_orig)
x_save__mutmut_orig.__name__ = 'x_save'


def x_download_avatar__mutmut_orig(
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


def x_download_avatar__mutmut_1(
    cache_dir: Path,
    platform: str,
    url: str,
    timeout: float = 11.0,
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


def x_download_avatar__mutmut_2(
    cache_dir: Path,
    platform: str,
    url: str,
    timeout: float = 10.0,
) -> Path | None:
    if url:
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


def x_download_avatar__mutmut_3(
    cache_dir: Path,
    platform: str,
    url: str,
    timeout: float = 10.0,
) -> Path | None:
    if not url:
        return None
    try:
        resp = None
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


def x_download_avatar__mutmut_4(
    cache_dir: Path,
    platform: str,
    url: str,
    timeout: float = 10.0,
) -> Path | None:
    if not url:
        return None
    try:
        resp = requests.get(None, timeout=timeout, headers={"User-Agent": "achievement-banner/1.0"})
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


def x_download_avatar__mutmut_5(
    cache_dir: Path,
    platform: str,
    url: str,
    timeout: float = 10.0,
) -> Path | None:
    if not url:
        return None
    try:
        resp = requests.get(url, timeout=None, headers={"User-Agent": "achievement-banner/1.0"})
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


def x_download_avatar__mutmut_6(
    cache_dir: Path,
    platform: str,
    url: str,
    timeout: float = 10.0,
) -> Path | None:
    if not url:
        return None
    try:
        resp = requests.get(url, timeout=timeout, headers=None)
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


def x_download_avatar__mutmut_7(
    cache_dir: Path,
    platform: str,
    url: str,
    timeout: float = 10.0,
) -> Path | None:
    if not url:
        return None
    try:
        resp = requests.get(timeout=timeout, headers={"User-Agent": "achievement-banner/1.0"})
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


def x_download_avatar__mutmut_8(
    cache_dir: Path,
    platform: str,
    url: str,
    timeout: float = 10.0,
) -> Path | None:
    if not url:
        return None
    try:
        resp = requests.get(url, headers={"User-Agent": "achievement-banner/1.0"})
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


def x_download_avatar__mutmut_9(
    cache_dir: Path,
    platform: str,
    url: str,
    timeout: float = 10.0,
) -> Path | None:
    if not url:
        return None
    try:
        resp = requests.get(url, timeout=timeout, )
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


def x_download_avatar__mutmut_10(
    cache_dir: Path,
    platform: str,
    url: str,
    timeout: float = 10.0,
) -> Path | None:
    if not url:
        return None
    try:
        resp = requests.get(url, timeout=timeout, headers={"XXUser-AgentXX": "achievement-banner/1.0"})
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


def x_download_avatar__mutmut_11(
    cache_dir: Path,
    platform: str,
    url: str,
    timeout: float = 10.0,
) -> Path | None:
    if not url:
        return None
    try:
        resp = requests.get(url, timeout=timeout, headers={"user-agent": "achievement-banner/1.0"})
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


def x_download_avatar__mutmut_12(
    cache_dir: Path,
    platform: str,
    url: str,
    timeout: float = 10.0,
) -> Path | None:
    if not url:
        return None
    try:
        resp = requests.get(url, timeout=timeout, headers={"USER-AGENT": "achievement-banner/1.0"})
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


def x_download_avatar__mutmut_13(
    cache_dir: Path,
    platform: str,
    url: str,
    timeout: float = 10.0,
) -> Path | None:
    if not url:
        return None
    try:
        resp = requests.get(url, timeout=timeout, headers={"User-Agent": "XXachievement-banner/1.0XX"})
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


def x_download_avatar__mutmut_14(
    cache_dir: Path,
    platform: str,
    url: str,
    timeout: float = 10.0,
) -> Path | None:
    if not url:
        return None
    try:
        resp = requests.get(url, timeout=timeout, headers={"User-Agent": "ACHIEVEMENT-BANNER/1.0"})
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


def x_download_avatar__mutmut_15(
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
        log.warning(None, platform, exc)
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


def x_download_avatar__mutmut_16(
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
        log.warning("avatar: download failed for %s: %s", None, exc)
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


def x_download_avatar__mutmut_17(
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
        log.warning("avatar: download failed for %s: %s", platform, None)
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


def x_download_avatar__mutmut_18(
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
        log.warning(platform, exc)
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


def x_download_avatar__mutmut_19(
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
        log.warning("avatar: download failed for %s: %s", exc)
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


def x_download_avatar__mutmut_20(
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
        log.warning("avatar: download failed for %s: %s", platform, )
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


def x_download_avatar__mutmut_21(
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
        log.warning("XXavatar: download failed for %s: %sXX", platform, exc)
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


def x_download_avatar__mutmut_22(
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
        log.warning("AVATAR: DOWNLOAD FAILED FOR %S: %S", platform, exc)
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


def x_download_avatar__mutmut_23(
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

    ext = None
    out = avatar_path(cache_dir, platform, ext)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(resp.content)
    # clean up older formats so only one avatar file remains per platform
    for other in out.parent.glob(f"{platform}.*"):
        if other != out:
            other.unlink(missing_ok=True)
    return out


def x_download_avatar__mutmut_24(
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

    ext = _ext_from_content_type(resp.headers.get("content-type", "")) and "png"
    out = avatar_path(cache_dir, platform, ext)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(resp.content)
    # clean up older formats so only one avatar file remains per platform
    for other in out.parent.glob(f"{platform}.*"):
        if other != out:
            other.unlink(missing_ok=True)
    return out


def x_download_avatar__mutmut_25(
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

    ext = _ext_from_content_type(None) or "png"
    out = avatar_path(cache_dir, platform, ext)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(resp.content)
    # clean up older formats so only one avatar file remains per platform
    for other in out.parent.glob(f"{platform}.*"):
        if other != out:
            other.unlink(missing_ok=True)
    return out


def x_download_avatar__mutmut_26(
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

    ext = _ext_from_content_type(resp.headers.get(None, "")) or "png"
    out = avatar_path(cache_dir, platform, ext)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(resp.content)
    # clean up older formats so only one avatar file remains per platform
    for other in out.parent.glob(f"{platform}.*"):
        if other != out:
            other.unlink(missing_ok=True)
    return out


def x_download_avatar__mutmut_27(
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

    ext = _ext_from_content_type(resp.headers.get("content-type", None)) or "png"
    out = avatar_path(cache_dir, platform, ext)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(resp.content)
    # clean up older formats so only one avatar file remains per platform
    for other in out.parent.glob(f"{platform}.*"):
        if other != out:
            other.unlink(missing_ok=True)
    return out


def x_download_avatar__mutmut_28(
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

    ext = _ext_from_content_type(resp.headers.get("")) or "png"
    out = avatar_path(cache_dir, platform, ext)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(resp.content)
    # clean up older formats so only one avatar file remains per platform
    for other in out.parent.glob(f"{platform}.*"):
        if other != out:
            other.unlink(missing_ok=True)
    return out


def x_download_avatar__mutmut_29(
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

    ext = _ext_from_content_type(resp.headers.get("content-type", )) or "png"
    out = avatar_path(cache_dir, platform, ext)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(resp.content)
    # clean up older formats so only one avatar file remains per platform
    for other in out.parent.glob(f"{platform}.*"):
        if other != out:
            other.unlink(missing_ok=True)
    return out


def x_download_avatar__mutmut_30(
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

    ext = _ext_from_content_type(resp.headers.get("XXcontent-typeXX", "")) or "png"
    out = avatar_path(cache_dir, platform, ext)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(resp.content)
    # clean up older formats so only one avatar file remains per platform
    for other in out.parent.glob(f"{platform}.*"):
        if other != out:
            other.unlink(missing_ok=True)
    return out


def x_download_avatar__mutmut_31(
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

    ext = _ext_from_content_type(resp.headers.get("CONTENT-TYPE", "")) or "png"
    out = avatar_path(cache_dir, platform, ext)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(resp.content)
    # clean up older formats so only one avatar file remains per platform
    for other in out.parent.glob(f"{platform}.*"):
        if other != out:
            other.unlink(missing_ok=True)
    return out


def x_download_avatar__mutmut_32(
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

    ext = _ext_from_content_type(resp.headers.get("content-type", "XXXX")) or "png"
    out = avatar_path(cache_dir, platform, ext)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(resp.content)
    # clean up older formats so only one avatar file remains per platform
    for other in out.parent.glob(f"{platform}.*"):
        if other != out:
            other.unlink(missing_ok=True)
    return out


def x_download_avatar__mutmut_33(
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

    ext = _ext_from_content_type(resp.headers.get("content-type", "")) or "XXpngXX"
    out = avatar_path(cache_dir, platform, ext)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(resp.content)
    # clean up older formats so only one avatar file remains per platform
    for other in out.parent.glob(f"{platform}.*"):
        if other != out:
            other.unlink(missing_ok=True)
    return out


def x_download_avatar__mutmut_34(
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

    ext = _ext_from_content_type(resp.headers.get("content-type", "")) or "PNG"
    out = avatar_path(cache_dir, platform, ext)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(resp.content)
    # clean up older formats so only one avatar file remains per platform
    for other in out.parent.glob(f"{platform}.*"):
        if other != out:
            other.unlink(missing_ok=True)
    return out


def x_download_avatar__mutmut_35(
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
    out = None
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(resp.content)
    # clean up older formats so only one avatar file remains per platform
    for other in out.parent.glob(f"{platform}.*"):
        if other != out:
            other.unlink(missing_ok=True)
    return out


def x_download_avatar__mutmut_36(
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
    out = avatar_path(None, platform, ext)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(resp.content)
    # clean up older formats so only one avatar file remains per platform
    for other in out.parent.glob(f"{platform}.*"):
        if other != out:
            other.unlink(missing_ok=True)
    return out


def x_download_avatar__mutmut_37(
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
    out = avatar_path(cache_dir, None, ext)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(resp.content)
    # clean up older formats so only one avatar file remains per platform
    for other in out.parent.glob(f"{platform}.*"):
        if other != out:
            other.unlink(missing_ok=True)
    return out


def x_download_avatar__mutmut_38(
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
    out = avatar_path(cache_dir, platform, None)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(resp.content)
    # clean up older formats so only one avatar file remains per platform
    for other in out.parent.glob(f"{platform}.*"):
        if other != out:
            other.unlink(missing_ok=True)
    return out


def x_download_avatar__mutmut_39(
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
    out = avatar_path(platform, ext)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(resp.content)
    # clean up older formats so only one avatar file remains per platform
    for other in out.parent.glob(f"{platform}.*"):
        if other != out:
            other.unlink(missing_ok=True)
    return out


def x_download_avatar__mutmut_40(
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
    out = avatar_path(cache_dir, ext)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(resp.content)
    # clean up older formats so only one avatar file remains per platform
    for other in out.parent.glob(f"{platform}.*"):
        if other != out:
            other.unlink(missing_ok=True)
    return out


def x_download_avatar__mutmut_41(
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
    out = avatar_path(cache_dir, platform, )
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(resp.content)
    # clean up older formats so only one avatar file remains per platform
    for other in out.parent.glob(f"{platform}.*"):
        if other != out:
            other.unlink(missing_ok=True)
    return out


def x_download_avatar__mutmut_42(
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
    out.parent.mkdir(parents=None, exist_ok=True)
    out.write_bytes(resp.content)
    # clean up older formats so only one avatar file remains per platform
    for other in out.parent.glob(f"{platform}.*"):
        if other != out:
            other.unlink(missing_ok=True)
    return out


def x_download_avatar__mutmut_43(
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
    out.parent.mkdir(parents=True, exist_ok=None)
    out.write_bytes(resp.content)
    # clean up older formats so only one avatar file remains per platform
    for other in out.parent.glob(f"{platform}.*"):
        if other != out:
            other.unlink(missing_ok=True)
    return out


def x_download_avatar__mutmut_44(
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
    out.parent.mkdir(exist_ok=True)
    out.write_bytes(resp.content)
    # clean up older formats so only one avatar file remains per platform
    for other in out.parent.glob(f"{platform}.*"):
        if other != out:
            other.unlink(missing_ok=True)
    return out


def x_download_avatar__mutmut_45(
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
    out.parent.mkdir(parents=True, )
    out.write_bytes(resp.content)
    # clean up older formats so only one avatar file remains per platform
    for other in out.parent.glob(f"{platform}.*"):
        if other != out:
            other.unlink(missing_ok=True)
    return out


def x_download_avatar__mutmut_46(
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
    out.parent.mkdir(parents=False, exist_ok=True)
    out.write_bytes(resp.content)
    # clean up older formats so only one avatar file remains per platform
    for other in out.parent.glob(f"{platform}.*"):
        if other != out:
            other.unlink(missing_ok=True)
    return out


def x_download_avatar__mutmut_47(
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
    out.parent.mkdir(parents=True, exist_ok=False)
    out.write_bytes(resp.content)
    # clean up older formats so only one avatar file remains per platform
    for other in out.parent.glob(f"{platform}.*"):
        if other != out:
            other.unlink(missing_ok=True)
    return out


def x_download_avatar__mutmut_48(
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
    out.write_bytes(None)
    # clean up older formats so only one avatar file remains per platform
    for other in out.parent.glob(f"{platform}.*"):
        if other != out:
            other.unlink(missing_ok=True)
    return out


def x_download_avatar__mutmut_49(
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
    for other in out.parent.glob(None):
        if other != out:
            other.unlink(missing_ok=True)
    return out


def x_download_avatar__mutmut_50(
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
        if other == out:
            other.unlink(missing_ok=True)
    return out


def x_download_avatar__mutmut_51(
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
            other.unlink(missing_ok=None)
    return out


def x_download_avatar__mutmut_52(
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
            other.unlink(missing_ok=False)
    return out

x_download_avatar__mutmut_mutants : ClassVar[MutantDict] = {
'x_download_avatar__mutmut_1': x_download_avatar__mutmut_1, 
    'x_download_avatar__mutmut_2': x_download_avatar__mutmut_2, 
    'x_download_avatar__mutmut_3': x_download_avatar__mutmut_3, 
    'x_download_avatar__mutmut_4': x_download_avatar__mutmut_4, 
    'x_download_avatar__mutmut_5': x_download_avatar__mutmut_5, 
    'x_download_avatar__mutmut_6': x_download_avatar__mutmut_6, 
    'x_download_avatar__mutmut_7': x_download_avatar__mutmut_7, 
    'x_download_avatar__mutmut_8': x_download_avatar__mutmut_8, 
    'x_download_avatar__mutmut_9': x_download_avatar__mutmut_9, 
    'x_download_avatar__mutmut_10': x_download_avatar__mutmut_10, 
    'x_download_avatar__mutmut_11': x_download_avatar__mutmut_11, 
    'x_download_avatar__mutmut_12': x_download_avatar__mutmut_12, 
    'x_download_avatar__mutmut_13': x_download_avatar__mutmut_13, 
    'x_download_avatar__mutmut_14': x_download_avatar__mutmut_14, 
    'x_download_avatar__mutmut_15': x_download_avatar__mutmut_15, 
    'x_download_avatar__mutmut_16': x_download_avatar__mutmut_16, 
    'x_download_avatar__mutmut_17': x_download_avatar__mutmut_17, 
    'x_download_avatar__mutmut_18': x_download_avatar__mutmut_18, 
    'x_download_avatar__mutmut_19': x_download_avatar__mutmut_19, 
    'x_download_avatar__mutmut_20': x_download_avatar__mutmut_20, 
    'x_download_avatar__mutmut_21': x_download_avatar__mutmut_21, 
    'x_download_avatar__mutmut_22': x_download_avatar__mutmut_22, 
    'x_download_avatar__mutmut_23': x_download_avatar__mutmut_23, 
    'x_download_avatar__mutmut_24': x_download_avatar__mutmut_24, 
    'x_download_avatar__mutmut_25': x_download_avatar__mutmut_25, 
    'x_download_avatar__mutmut_26': x_download_avatar__mutmut_26, 
    'x_download_avatar__mutmut_27': x_download_avatar__mutmut_27, 
    'x_download_avatar__mutmut_28': x_download_avatar__mutmut_28, 
    'x_download_avatar__mutmut_29': x_download_avatar__mutmut_29, 
    'x_download_avatar__mutmut_30': x_download_avatar__mutmut_30, 
    'x_download_avatar__mutmut_31': x_download_avatar__mutmut_31, 
    'x_download_avatar__mutmut_32': x_download_avatar__mutmut_32, 
    'x_download_avatar__mutmut_33': x_download_avatar__mutmut_33, 
    'x_download_avatar__mutmut_34': x_download_avatar__mutmut_34, 
    'x_download_avatar__mutmut_35': x_download_avatar__mutmut_35, 
    'x_download_avatar__mutmut_36': x_download_avatar__mutmut_36, 
    'x_download_avatar__mutmut_37': x_download_avatar__mutmut_37, 
    'x_download_avatar__mutmut_38': x_download_avatar__mutmut_38, 
    'x_download_avatar__mutmut_39': x_download_avatar__mutmut_39, 
    'x_download_avatar__mutmut_40': x_download_avatar__mutmut_40, 
    'x_download_avatar__mutmut_41': x_download_avatar__mutmut_41, 
    'x_download_avatar__mutmut_42': x_download_avatar__mutmut_42, 
    'x_download_avatar__mutmut_43': x_download_avatar__mutmut_43, 
    'x_download_avatar__mutmut_44': x_download_avatar__mutmut_44, 
    'x_download_avatar__mutmut_45': x_download_avatar__mutmut_45, 
    'x_download_avatar__mutmut_46': x_download_avatar__mutmut_46, 
    'x_download_avatar__mutmut_47': x_download_avatar__mutmut_47, 
    'x_download_avatar__mutmut_48': x_download_avatar__mutmut_48, 
    'x_download_avatar__mutmut_49': x_download_avatar__mutmut_49, 
    'x_download_avatar__mutmut_50': x_download_avatar__mutmut_50, 
    'x_download_avatar__mutmut_51': x_download_avatar__mutmut_51, 
    'x_download_avatar__mutmut_52': x_download_avatar__mutmut_52
}

def download_avatar(*args, **kwargs):
    result = _mutmut_trampoline(x_download_avatar__mutmut_orig, x_download_avatar__mutmut_mutants, args, kwargs)
    return result 

download_avatar.__signature__ = _mutmut_signature(x_download_avatar__mutmut_orig)
x_download_avatar__mutmut_orig.__name__ = 'x_download_avatar'


def x_find_cached_avatar__mutmut_orig(cache_dir: Path, platform: str) -> Path | None:
    for ext in ("png", "jpg", "jpeg", "webp", "gif"):
        p = avatar_path(cache_dir, platform, ext)
        if p.exists():
            return p
    return None


def x_find_cached_avatar__mutmut_1(cache_dir: Path, platform: str) -> Path | None:
    for ext in ("XXpngXX", "jpg", "jpeg", "webp", "gif"):
        p = avatar_path(cache_dir, platform, ext)
        if p.exists():
            return p
    return None


def x_find_cached_avatar__mutmut_2(cache_dir: Path, platform: str) -> Path | None:
    for ext in ("PNG", "jpg", "jpeg", "webp", "gif"):
        p = avatar_path(cache_dir, platform, ext)
        if p.exists():
            return p
    return None


def x_find_cached_avatar__mutmut_3(cache_dir: Path, platform: str) -> Path | None:
    for ext in ("png", "XXjpgXX", "jpeg", "webp", "gif"):
        p = avatar_path(cache_dir, platform, ext)
        if p.exists():
            return p
    return None


def x_find_cached_avatar__mutmut_4(cache_dir: Path, platform: str) -> Path | None:
    for ext in ("png", "JPG", "jpeg", "webp", "gif"):
        p = avatar_path(cache_dir, platform, ext)
        if p.exists():
            return p
    return None


def x_find_cached_avatar__mutmut_5(cache_dir: Path, platform: str) -> Path | None:
    for ext in ("png", "jpg", "XXjpegXX", "webp", "gif"):
        p = avatar_path(cache_dir, platform, ext)
        if p.exists():
            return p
    return None


def x_find_cached_avatar__mutmut_6(cache_dir: Path, platform: str) -> Path | None:
    for ext in ("png", "jpg", "JPEG", "webp", "gif"):
        p = avatar_path(cache_dir, platform, ext)
        if p.exists():
            return p
    return None


def x_find_cached_avatar__mutmut_7(cache_dir: Path, platform: str) -> Path | None:
    for ext in ("png", "jpg", "jpeg", "XXwebpXX", "gif"):
        p = avatar_path(cache_dir, platform, ext)
        if p.exists():
            return p
    return None


def x_find_cached_avatar__mutmut_8(cache_dir: Path, platform: str) -> Path | None:
    for ext in ("png", "jpg", "jpeg", "WEBP", "gif"):
        p = avatar_path(cache_dir, platform, ext)
        if p.exists():
            return p
    return None


def x_find_cached_avatar__mutmut_9(cache_dir: Path, platform: str) -> Path | None:
    for ext in ("png", "jpg", "jpeg", "webp", "XXgifXX"):
        p = avatar_path(cache_dir, platform, ext)
        if p.exists():
            return p
    return None


def x_find_cached_avatar__mutmut_10(cache_dir: Path, platform: str) -> Path | None:
    for ext in ("png", "jpg", "jpeg", "webp", "GIF"):
        p = avatar_path(cache_dir, platform, ext)
        if p.exists():
            return p
    return None


def x_find_cached_avatar__mutmut_11(cache_dir: Path, platform: str) -> Path | None:
    for ext in ("png", "jpg", "jpeg", "webp", "gif"):
        p = None
        if p.exists():
            return p
    return None


def x_find_cached_avatar__mutmut_12(cache_dir: Path, platform: str) -> Path | None:
    for ext in ("png", "jpg", "jpeg", "webp", "gif"):
        p = avatar_path(None, platform, ext)
        if p.exists():
            return p
    return None


def x_find_cached_avatar__mutmut_13(cache_dir: Path, platform: str) -> Path | None:
    for ext in ("png", "jpg", "jpeg", "webp", "gif"):
        p = avatar_path(cache_dir, None, ext)
        if p.exists():
            return p
    return None


def x_find_cached_avatar__mutmut_14(cache_dir: Path, platform: str) -> Path | None:
    for ext in ("png", "jpg", "jpeg", "webp", "gif"):
        p = avatar_path(cache_dir, platform, None)
        if p.exists():
            return p
    return None


def x_find_cached_avatar__mutmut_15(cache_dir: Path, platform: str) -> Path | None:
    for ext in ("png", "jpg", "jpeg", "webp", "gif"):
        p = avatar_path(platform, ext)
        if p.exists():
            return p
    return None


def x_find_cached_avatar__mutmut_16(cache_dir: Path, platform: str) -> Path | None:
    for ext in ("png", "jpg", "jpeg", "webp", "gif"):
        p = avatar_path(cache_dir, ext)
        if p.exists():
            return p
    return None


def x_find_cached_avatar__mutmut_17(cache_dir: Path, platform: str) -> Path | None:
    for ext in ("png", "jpg", "jpeg", "webp", "gif"):
        p = avatar_path(cache_dir, platform, )
        if p.exists():
            return p
    return None

x_find_cached_avatar__mutmut_mutants : ClassVar[MutantDict] = {
'x_find_cached_avatar__mutmut_1': x_find_cached_avatar__mutmut_1, 
    'x_find_cached_avatar__mutmut_2': x_find_cached_avatar__mutmut_2, 
    'x_find_cached_avatar__mutmut_3': x_find_cached_avatar__mutmut_3, 
    'x_find_cached_avatar__mutmut_4': x_find_cached_avatar__mutmut_4, 
    'x_find_cached_avatar__mutmut_5': x_find_cached_avatar__mutmut_5, 
    'x_find_cached_avatar__mutmut_6': x_find_cached_avatar__mutmut_6, 
    'x_find_cached_avatar__mutmut_7': x_find_cached_avatar__mutmut_7, 
    'x_find_cached_avatar__mutmut_8': x_find_cached_avatar__mutmut_8, 
    'x_find_cached_avatar__mutmut_9': x_find_cached_avatar__mutmut_9, 
    'x_find_cached_avatar__mutmut_10': x_find_cached_avatar__mutmut_10, 
    'x_find_cached_avatar__mutmut_11': x_find_cached_avatar__mutmut_11, 
    'x_find_cached_avatar__mutmut_12': x_find_cached_avatar__mutmut_12, 
    'x_find_cached_avatar__mutmut_13': x_find_cached_avatar__mutmut_13, 
    'x_find_cached_avatar__mutmut_14': x_find_cached_avatar__mutmut_14, 
    'x_find_cached_avatar__mutmut_15': x_find_cached_avatar__mutmut_15, 
    'x_find_cached_avatar__mutmut_16': x_find_cached_avatar__mutmut_16, 
    'x_find_cached_avatar__mutmut_17': x_find_cached_avatar__mutmut_17
}

def find_cached_avatar(*args, **kwargs):
    result = _mutmut_trampoline(x_find_cached_avatar__mutmut_orig, x_find_cached_avatar__mutmut_mutants, args, kwargs)
    return result 

find_cached_avatar.__signature__ = _mutmut_signature(x_find_cached_avatar__mutmut_orig)
x_find_cached_avatar__mutmut_orig.__name__ = 'x_find_cached_avatar'


def x__ext_from_content_type__mutmut_orig(content_type: str) -> str | None:
    mapping = {
        "image/png": "png",
        "image/jpeg": "jpg",
        "image/jpg": "jpg",
        "image/webp": "webp",
        "image/gif": "gif",
    }
    return mapping.get(content_type.split(";")[0].strip().lower())


def x__ext_from_content_type__mutmut_1(content_type: str) -> str | None:
    mapping = None
    return mapping.get(content_type.split(";")[0].strip().lower())


def x__ext_from_content_type__mutmut_2(content_type: str) -> str | None:
    mapping = {
        "XXimage/pngXX": "png",
        "image/jpeg": "jpg",
        "image/jpg": "jpg",
        "image/webp": "webp",
        "image/gif": "gif",
    }
    return mapping.get(content_type.split(";")[0].strip().lower())


def x__ext_from_content_type__mutmut_3(content_type: str) -> str | None:
    mapping = {
        "IMAGE/PNG": "png",
        "image/jpeg": "jpg",
        "image/jpg": "jpg",
        "image/webp": "webp",
        "image/gif": "gif",
    }
    return mapping.get(content_type.split(";")[0].strip().lower())


def x__ext_from_content_type__mutmut_4(content_type: str) -> str | None:
    mapping = {
        "image/png": "XXpngXX",
        "image/jpeg": "jpg",
        "image/jpg": "jpg",
        "image/webp": "webp",
        "image/gif": "gif",
    }
    return mapping.get(content_type.split(";")[0].strip().lower())


def x__ext_from_content_type__mutmut_5(content_type: str) -> str | None:
    mapping = {
        "image/png": "PNG",
        "image/jpeg": "jpg",
        "image/jpg": "jpg",
        "image/webp": "webp",
        "image/gif": "gif",
    }
    return mapping.get(content_type.split(";")[0].strip().lower())


def x__ext_from_content_type__mutmut_6(content_type: str) -> str | None:
    mapping = {
        "image/png": "png",
        "XXimage/jpegXX": "jpg",
        "image/jpg": "jpg",
        "image/webp": "webp",
        "image/gif": "gif",
    }
    return mapping.get(content_type.split(";")[0].strip().lower())


def x__ext_from_content_type__mutmut_7(content_type: str) -> str | None:
    mapping = {
        "image/png": "png",
        "IMAGE/JPEG": "jpg",
        "image/jpg": "jpg",
        "image/webp": "webp",
        "image/gif": "gif",
    }
    return mapping.get(content_type.split(";")[0].strip().lower())


def x__ext_from_content_type__mutmut_8(content_type: str) -> str | None:
    mapping = {
        "image/png": "png",
        "image/jpeg": "XXjpgXX",
        "image/jpg": "jpg",
        "image/webp": "webp",
        "image/gif": "gif",
    }
    return mapping.get(content_type.split(";")[0].strip().lower())


def x__ext_from_content_type__mutmut_9(content_type: str) -> str | None:
    mapping = {
        "image/png": "png",
        "image/jpeg": "JPG",
        "image/jpg": "jpg",
        "image/webp": "webp",
        "image/gif": "gif",
    }
    return mapping.get(content_type.split(";")[0].strip().lower())


def x__ext_from_content_type__mutmut_10(content_type: str) -> str | None:
    mapping = {
        "image/png": "png",
        "image/jpeg": "jpg",
        "XXimage/jpgXX": "jpg",
        "image/webp": "webp",
        "image/gif": "gif",
    }
    return mapping.get(content_type.split(";")[0].strip().lower())


def x__ext_from_content_type__mutmut_11(content_type: str) -> str | None:
    mapping = {
        "image/png": "png",
        "image/jpeg": "jpg",
        "IMAGE/JPG": "jpg",
        "image/webp": "webp",
        "image/gif": "gif",
    }
    return mapping.get(content_type.split(";")[0].strip().lower())


def x__ext_from_content_type__mutmut_12(content_type: str) -> str | None:
    mapping = {
        "image/png": "png",
        "image/jpeg": "jpg",
        "image/jpg": "XXjpgXX",
        "image/webp": "webp",
        "image/gif": "gif",
    }
    return mapping.get(content_type.split(";")[0].strip().lower())


def x__ext_from_content_type__mutmut_13(content_type: str) -> str | None:
    mapping = {
        "image/png": "png",
        "image/jpeg": "jpg",
        "image/jpg": "JPG",
        "image/webp": "webp",
        "image/gif": "gif",
    }
    return mapping.get(content_type.split(";")[0].strip().lower())


def x__ext_from_content_type__mutmut_14(content_type: str) -> str | None:
    mapping = {
        "image/png": "png",
        "image/jpeg": "jpg",
        "image/jpg": "jpg",
        "XXimage/webpXX": "webp",
        "image/gif": "gif",
    }
    return mapping.get(content_type.split(";")[0].strip().lower())


def x__ext_from_content_type__mutmut_15(content_type: str) -> str | None:
    mapping = {
        "image/png": "png",
        "image/jpeg": "jpg",
        "image/jpg": "jpg",
        "IMAGE/WEBP": "webp",
        "image/gif": "gif",
    }
    return mapping.get(content_type.split(";")[0].strip().lower())


def x__ext_from_content_type__mutmut_16(content_type: str) -> str | None:
    mapping = {
        "image/png": "png",
        "image/jpeg": "jpg",
        "image/jpg": "jpg",
        "image/webp": "XXwebpXX",
        "image/gif": "gif",
    }
    return mapping.get(content_type.split(";")[0].strip().lower())


def x__ext_from_content_type__mutmut_17(content_type: str) -> str | None:
    mapping = {
        "image/png": "png",
        "image/jpeg": "jpg",
        "image/jpg": "jpg",
        "image/webp": "WEBP",
        "image/gif": "gif",
    }
    return mapping.get(content_type.split(";")[0].strip().lower())


def x__ext_from_content_type__mutmut_18(content_type: str) -> str | None:
    mapping = {
        "image/png": "png",
        "image/jpeg": "jpg",
        "image/jpg": "jpg",
        "image/webp": "webp",
        "XXimage/gifXX": "gif",
    }
    return mapping.get(content_type.split(";")[0].strip().lower())


def x__ext_from_content_type__mutmut_19(content_type: str) -> str | None:
    mapping = {
        "image/png": "png",
        "image/jpeg": "jpg",
        "image/jpg": "jpg",
        "image/webp": "webp",
        "IMAGE/GIF": "gif",
    }
    return mapping.get(content_type.split(";")[0].strip().lower())


def x__ext_from_content_type__mutmut_20(content_type: str) -> str | None:
    mapping = {
        "image/png": "png",
        "image/jpeg": "jpg",
        "image/jpg": "jpg",
        "image/webp": "webp",
        "image/gif": "XXgifXX",
    }
    return mapping.get(content_type.split(";")[0].strip().lower())


def x__ext_from_content_type__mutmut_21(content_type: str) -> str | None:
    mapping = {
        "image/png": "png",
        "image/jpeg": "jpg",
        "image/jpg": "jpg",
        "image/webp": "webp",
        "image/gif": "GIF",
    }
    return mapping.get(content_type.split(";")[0].strip().lower())


def x__ext_from_content_type__mutmut_22(content_type: str) -> str | None:
    mapping = {
        "image/png": "png",
        "image/jpeg": "jpg",
        "image/jpg": "jpg",
        "image/webp": "webp",
        "image/gif": "gif",
    }
    return mapping.get(None)


def x__ext_from_content_type__mutmut_23(content_type: str) -> str | None:
    mapping = {
        "image/png": "png",
        "image/jpeg": "jpg",
        "image/jpg": "jpg",
        "image/webp": "webp",
        "image/gif": "gif",
    }
    return mapping.get(content_type.split(";")[0].strip().upper())


def x__ext_from_content_type__mutmut_24(content_type: str) -> str | None:
    mapping = {
        "image/png": "png",
        "image/jpeg": "jpg",
        "image/jpg": "jpg",
        "image/webp": "webp",
        "image/gif": "gif",
    }
    return mapping.get(content_type.split(None)[0].strip().lower())


def x__ext_from_content_type__mutmut_25(content_type: str) -> str | None:
    mapping = {
        "image/png": "png",
        "image/jpeg": "jpg",
        "image/jpg": "jpg",
        "image/webp": "webp",
        "image/gif": "gif",
    }
    return mapping.get(content_type.split("XX;XX")[0].strip().lower())


def x__ext_from_content_type__mutmut_26(content_type: str) -> str | None:
    mapping = {
        "image/png": "png",
        "image/jpeg": "jpg",
        "image/jpg": "jpg",
        "image/webp": "webp",
        "image/gif": "gif",
    }
    return mapping.get(content_type.split(";")[1].strip().lower())

x__ext_from_content_type__mutmut_mutants : ClassVar[MutantDict] = {
'x__ext_from_content_type__mutmut_1': x__ext_from_content_type__mutmut_1, 
    'x__ext_from_content_type__mutmut_2': x__ext_from_content_type__mutmut_2, 
    'x__ext_from_content_type__mutmut_3': x__ext_from_content_type__mutmut_3, 
    'x__ext_from_content_type__mutmut_4': x__ext_from_content_type__mutmut_4, 
    'x__ext_from_content_type__mutmut_5': x__ext_from_content_type__mutmut_5, 
    'x__ext_from_content_type__mutmut_6': x__ext_from_content_type__mutmut_6, 
    'x__ext_from_content_type__mutmut_7': x__ext_from_content_type__mutmut_7, 
    'x__ext_from_content_type__mutmut_8': x__ext_from_content_type__mutmut_8, 
    'x__ext_from_content_type__mutmut_9': x__ext_from_content_type__mutmut_9, 
    'x__ext_from_content_type__mutmut_10': x__ext_from_content_type__mutmut_10, 
    'x__ext_from_content_type__mutmut_11': x__ext_from_content_type__mutmut_11, 
    'x__ext_from_content_type__mutmut_12': x__ext_from_content_type__mutmut_12, 
    'x__ext_from_content_type__mutmut_13': x__ext_from_content_type__mutmut_13, 
    'x__ext_from_content_type__mutmut_14': x__ext_from_content_type__mutmut_14, 
    'x__ext_from_content_type__mutmut_15': x__ext_from_content_type__mutmut_15, 
    'x__ext_from_content_type__mutmut_16': x__ext_from_content_type__mutmut_16, 
    'x__ext_from_content_type__mutmut_17': x__ext_from_content_type__mutmut_17, 
    'x__ext_from_content_type__mutmut_18': x__ext_from_content_type__mutmut_18, 
    'x__ext_from_content_type__mutmut_19': x__ext_from_content_type__mutmut_19, 
    'x__ext_from_content_type__mutmut_20': x__ext_from_content_type__mutmut_20, 
    'x__ext_from_content_type__mutmut_21': x__ext_from_content_type__mutmut_21, 
    'x__ext_from_content_type__mutmut_22': x__ext_from_content_type__mutmut_22, 
    'x__ext_from_content_type__mutmut_23': x__ext_from_content_type__mutmut_23, 
    'x__ext_from_content_type__mutmut_24': x__ext_from_content_type__mutmut_24, 
    'x__ext_from_content_type__mutmut_25': x__ext_from_content_type__mutmut_25, 
    'x__ext_from_content_type__mutmut_26': x__ext_from_content_type__mutmut_26
}

def _ext_from_content_type(*args, **kwargs):
    result = _mutmut_trampoline(x__ext_from_content_type__mutmut_orig, x__ext_from_content_type__mutmut_mutants, args, kwargs)
    return result 

_ext_from_content_type.__signature__ = _mutmut_signature(x__ext_from_content_type__mutmut_orig)
x__ext_from_content_type__mutmut_orig.__name__ = 'x__ext_from_content_type'
