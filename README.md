# python-achievements-generator

Generate a single Steam-ready banner image that combines Xbox (TrueAchievements),
PlayStation (PSNProfiles), and RetroAchievements public profile stats.

The pipeline scrapes each public profile, caches the results, and renders a
1500x450 PNG over a template background. If scraping fails, the last known good
data is used; if there's nothing to fall back to, the renderer falls through to
`data/overrides/manual.yaml` and finally to placeholders, always producing a
valid banner.

## Setup

```bash
pip install -r requirements.txt
```

Edit `config/profiles.yaml` with your profile URLs:

```yaml
xbox:
  profile_url: "https://www.trueachievements.com/gamer/YourGamertag"
  display_name: "YourName"
psn:
  profile_url: "https://psnprofiles.com/YourPsnId"
  display_name: "YourName"
retroachievements:
  profile_url: "https://retroachievements.org/user/YourRaUser"
  display_name: "YourName"
```

## Commands

Run as a module from the repo root:

```bash
python -m src.main generate        # scrape -> merge -> render
python -m src.main refresh-cache   # scrape + update cache only
python -m src.main render          # render from cached data only
python -m src.main build-template  # write a fresh base template PNG
```

Add `-v` before the subcommand (`python -m src.main -v generate`) for debug
logs. Use `--config`, `--cache-dir`, `--overrides`, `--output` to override
paths.

## Output

`data/output/banner.png`

## Layout

Three panels left-to-right: **Xbox**, **PlayStation**, **RetroAchievements**.

| Panel             | Headline            | Stats row                                |
| ----------------- | ------------------- | ---------------------------------------- |
| Xbox              | Gamerscore          | TrueAchievement Score pill badge         |
| PlayStation       | `N Platinums`       | Platinum / Gold / Silver / Bronze counts |
| RetroAchievements | Softcore / Hardcore | True Ratio + Mastery pill badges         |

## Customising the banner

Every dynamic image is loaded from the filesystem if present, otherwise the
renderer falls back to a procedural drawing. Drop files in these paths:

| File                                           | What it replaces                         |
| ---------------------------------------------- | ---------------------------------------- |
| `assets/template/base_template.png`            | Banner backdrop (any size — auto-fitted) |
| `assets/icons/xbox.png`                        | Xbox footer logo                         |
| `assets/icons/psn.png`                         | PlayStation footer logo                  |
| `assets/icons/retroachievements.png`           | RetroAchievements footer logo            |
| `assets/icons/psn/{platinum,gold,silver,bronze}.png` | PSN trophy icons in the stats row  |
| `data/cache/avatars/xbox.png`                  | Xbox avatar (also `.jpg/.jpeg/.webp/.gif`) |
| `data/cache/avatars/psn.png`                   | PSN avatar                               |
| `data/cache/avatars/retroachievements.png`     | RetroAchievements avatar                 |

Transparent PNGs are recommended for icons and trophies. Avatars you drop in
`data/cache/avatars/` are treated as authoritative — the scraper will not
overwrite them even if it returns a fresh URL.

## Fallback behavior

Priority when resolving each platform: **fresh scrape > manual override > cache > placeholder**.

| State                                     | Result                            |
| ----------------------------------------- | --------------------------------- |
| Scrape succeeds                           | Overwrite cache, render           |
| Scrape partial                            | Merge with cache, render          |
| Scrape fails, override exists             | Render from `manual.yaml`         |
| Scrape fails, no override, cache exists   | Render from cache                 |
| Scrape fails, no override, no cache       | Render platform placeholder       |

`data/overrides/manual.yaml` is seeded once from the first successful run so
you have a starting point to edit. Subsequent runs never overwrite it — edit
that file directly whenever you want to hand-set any values (username,
headline, substats, avatar URL). Your edits win over the cache whenever
scraping fails.

## Scraping caveats

TrueAchievements, PSNProfiles, and RetroAchievements all sit behind Cloudflare.
The project uses [`cloudscraper`](https://pypi.org/project/cloudscraper/) to
clear basic JS challenges, which is enough for PSNProfiles most of the time
but not for the managed challenges TA and RA currently serve. When a site
returns 403/404 the cache/override fallback chain kicks in — your banner still
renders with the last known good numbers.

For RetroAchievements you can skip the scrape entirely by using the official
JSON API. Create a key at <https://retroachievements.org/controlpanel.php>
and set two environment variables before running:

```bash
export RA_API_USER="your-ra-username"
export RA_API_KEY="your-api-key"
python -m src.main generate
```

When both are present the RA provider fetches via the API and bypasses the
Cloudflare web challenge entirely.

## Tests

```bash
python -m pytest tests/ -q
```

## Project layout

```
config/profiles.yaml        profile URLs + display names
data/cache/*.json           per-platform cached stats
data/cache/avatars/         avatar images (drop-in per platform)
data/output/banner.png      rendered banner
data/overrides/manual.yaml  user-editable fallback values
assets/template/            base_template.png (procedural or user-supplied)
assets/icons/               footer logos + per-stat trophy icons
assets/fonts/               bundled DejaVu Sans (Bitstream Vera license)
src/
  main.py                   CLI
  config.py                 yaml loader
  models.py                 PlatformStats / SubStat
  cache.py                  json + avatar cache
  providers/                xbox / psn / retroachievements scrapers
  services/                 fetch orchestration + merge + normalize
  renderer/                 layout + draw + compose
tests/
```
