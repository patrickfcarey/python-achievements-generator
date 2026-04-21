"""CLI entrypoint for the cross-platform achievement banner generator.

Commands:
  generate        Scrape all platforms, update the cache, and render the banner.
  scrape          Scrape all platforms and update the cache only (no render).
  render          Render the banner from cached data without scraping.
  render-manual   Render the banner from data/overrides/manual.yaml (no scraping, no cache update).
  build-template  Write the procedural base template PNG to assets/template/.

Global flags (must appear before the command):
  --config PATH       Path to profiles.yaml (default: config/profiles.yaml)
  --cache-dir PATH    Path to the cache directory (default: data/cache)
  --output PATH       Path for the output PNG (default: data/output/banner.png)
  -v / --verbose      Enable DEBUG-level logging
"""
from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

try:
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover - optional dependency
    load_dotenv = None

from . import cache as cache_module
from .config import load_config, load_overrides
from .models import PlatformStats
from .renderer import compose
from .renderer.layout import PLATFORM_ORDER
from .services.fetch import FetchPaths, fetch_all
from .services.merge import apply_override, placeholder

log = logging.getLogger("banner")

REPO_ROOT = Path(__file__).resolve().parents[1]

DEFAULT_CONFIG_PATH = REPO_ROOT / "config" / "profiles.yaml"
DEFAULT_CACHE_DIRECTORY = REPO_ROOT / "data" / "cache"
DEFAULT_MANUAL_PATH = REPO_ROOT / "data" / "overrides" / "manual.yaml"
DEFAULT_OUTPUT_PATH = REPO_ROOT / "data" / "output" / "banner.png"

EXIT_SUCCESS = 0
EXIT_NO_PROFILES = 1
EXIT_UNKNOWN_COMMAND = 2


def build_parser() -> argparse.ArgumentParser:
    """Build the argument parser for the banner CLI."""
    arg_parser = argparse.ArgumentParser(
        prog="banner",
        description="Cross-platform achievement banner generator",
    )
    arg_parser.add_argument("--config", default=str(DEFAULT_CONFIG_PATH))
    arg_parser.add_argument("--cache-dir", default=str(DEFAULT_CACHE_DIRECTORY))
    arg_parser.add_argument("--output", default=str(DEFAULT_OUTPUT_PATH))
    arg_parser.add_argument("-v", "--verbose", action="store_true")

    subcommands = arg_parser.add_subparsers(dest="command", required=True)
    subcommands.add_parser("generate", help="scrape -> cache -> render")
    subcommands.add_parser("scrape", help="scrape + update cache only (no render)")
    subcommands.add_parser("render", help="render from cached data only")
    render_manual_cmd = subcommands.add_parser(
        "render-manual", help="render from manual.yaml only (no scraping, no cache update)",
    )
    render_manual_cmd.add_argument(
        "--manual", default=str(DEFAULT_MANUAL_PATH),
        help="path to manual.yaml (default: data/overrides/manual.yaml)",
    )
    subcommands.add_parser("build-template", help="write the base template PNG to assets/template/")

    return arg_parser


def main(argv: list[str] | None = None) -> int:
    """Parse arguments, run the requested command, and return an exit code."""
    if load_dotenv is not None:
        load_dotenv(REPO_ROOT / ".env")

    parsed_args = build_parser().parse_args(argv)
    _configure_logging(verbose=parsed_args.verbose)

    fetch_paths = FetchPaths(
        cache_dir=Path(parsed_args.cache_dir),
    )
    output_path = Path(parsed_args.output)

    if parsed_args.command == "build-template":
        return _run_build_template()

    if parsed_args.command == "render-manual":
        manual_path = Path(getattr(parsed_args, "manual", str(DEFAULT_MANUAL_PATH)))
        return _run_render_manual(manual_path, fetch_paths.cache_dir, output_path)

    app_config = load_config(parsed_args.config)
    if not app_config.profiles:
        log.error("no profiles configured in %s", parsed_args.config)
        return EXIT_NO_PROFILES

    command_handlers = {
        "generate": lambda: _run_generate(app_config, fetch_paths, output_path),
        "scrape":   lambda: _run_scrape(app_config, fetch_paths),
        "render":   lambda: _run_render_from_cache(app_config, fetch_paths, output_path),
    }
    handler = command_handlers.get(parsed_args.command)
    if handler is None:
        log.error("unknown command: %s", parsed_args.command)
        return EXIT_UNKNOWN_COMMAND

    handler()
    return EXIT_SUCCESS


def _configure_logging(verbose: bool) -> None:
    """Set up root logging at INFO or DEBUG level."""
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    )


def _run_build_template() -> int:
    """Regenerate the procedural base template PNG and save it to disk."""
    compose.build_base_template().save(compose.TEMPLATE_PATH)
    log.info("template written to %s", compose.TEMPLATE_PATH)
    return EXIT_SUCCESS


def _run_generate(app_config, fetch_paths: FetchPaths, output_path: Path) -> None:
    """Scrape all platforms, update the cache, and render the banner."""
    platform_stats_map = fetch_all(app_config, fetch_paths, scrape=True)
    compose.render(platform_stats_map, fetch_paths.cache_dir, output_path)


def _run_scrape(app_config, fetch_paths: FetchPaths) -> None:
    """Scrape all platforms and update the cache without rendering."""
    fetch_all(app_config, fetch_paths, scrape=True)
    log.info("cache updated")


def _run_render_from_cache(app_config, fetch_paths: FetchPaths, output_path: Path) -> None:
    """Render the banner from cached data only, without scraping."""
    platform_stats_map = _load_all_from_cache(app_config.profiles.keys(), fetch_paths)
    compose.render(platform_stats_map, fetch_paths.cache_dir, output_path)


def _run_render_manual(manual_path: Path, cache_dir: Path, output_path: Path) -> int:
    """Render the banner from a manual.yaml file without scraping or updating the cache."""
    manual_data = load_overrides(manual_path)
    if not manual_data:
        log.error("manual.yaml not found or empty at %s — copy config/example_manual.yaml to %s", manual_path, manual_path)
        return EXIT_NO_PROFILES

    platform_stats_map: dict[str, PlatformStats] = {}
    for platform in PLATFORM_ORDER:
        platform_override = manual_data.get(platform)
        if platform_override:
            platform_stats_map[platform] = apply_override(None, platform_override, platform)
        else:
            platform_stats_map[platform] = placeholder(platform)

    compose.render(platform_stats_map, cache_dir, output_path)
    return EXIT_SUCCESS


def _load_all_from_cache(
    platform_keys,
    fetch_paths: FetchPaths,
) -> dict[str, PlatformStats]:
    """Load stats for each platform from cache, falling back to placeholder if absent."""
    platform_stats_map: dict[str, PlatformStats] = {}
    for platform in platform_keys:
        cached_stats = cache_module.load(fetch_paths.cache_dir, platform)
        platform_stats_map[platform] = cached_stats if cached_stats is not None else placeholder(platform)
    return platform_stats_map


if __name__ == "__main__":
    sys.exit(main())
