"""CLI entrypoint: generate | refresh-cache | render."""
from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

from . import cache as cache_mod
from .config import load_config
from .models import PlatformStats
from .renderer import compose
from .services.fetch import FetchPaths, fetch_all
from .services.merge import placeholder

log = logging.getLogger("banner")

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = REPO_ROOT / "config" / "profiles.yaml"
DEFAULT_CACHE = REPO_ROOT / "data" / "cache"
DEFAULT_OVERRIDES = REPO_ROOT / "data" / "overrides" / "manual.yaml"
DEFAULT_OUTPUT = REPO_ROOT / "data" / "output" / "banner.png"


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="banner", description="Cross-platform achievement banner generator")
    p.add_argument("--config", default=str(DEFAULT_CONFIG))
    p.add_argument("--cache-dir", default=str(DEFAULT_CACHE))
    p.add_argument("--overrides", default=str(DEFAULT_OVERRIDES))
    p.add_argument("--output", default=str(DEFAULT_OUTPUT))
    p.add_argument("-v", "--verbose", action="store_true")

    sub = p.add_subparsers(dest="command", required=True)
    sub.add_parser("generate", help="scrape -> merge -> render")
    sub.add_parser("refresh-cache", help="scrape + update cache only (no render)")
    sub.add_parser("render", help="render from cached data only")
    sub.add_parser("build-template", help="write the base template PNG to assets/template/")
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    )

    paths = FetchPaths(cache_dir=Path(args.cache_dir), overrides_file=Path(args.overrides))
    output = Path(args.output)

    if args.command == "build-template":
        compose.build_base_template().save(compose.TEMPLATE_PATH)
        log.info("template written to %s", compose.TEMPLATE_PATH)
        return 0

    cfg = load_config(args.config)
    if not cfg.profiles:
        log.error("no profiles configured in %s", args.config)
        return 1

    if args.command == "generate":
        stats = fetch_all(cfg, paths, scrape=True)
        compose.render(stats, paths.cache_dir, output)
    elif args.command == "refresh-cache":
        fetch_all(cfg, paths, scrape=True)
        log.info("cache refreshed")
    elif args.command == "render":
        stats = _load_from_cache_only(cfg.profiles.keys(), paths)
        compose.render(stats, paths.cache_dir, output)
    else:
        log.error("unknown command: %s", args.command)
        return 2

    return 0


def _load_from_cache_only(platforms, paths: FetchPaths) -> dict[str, PlatformStats]:
    out: dict[str, PlatformStats] = {}
    for p in platforms:
        cached = cache_mod.load(paths.cache_dir, p)
        out[p] = cached if cached is not None else placeholder(p)
    return out


if __name__ == "__main__":
    sys.exit(main())
