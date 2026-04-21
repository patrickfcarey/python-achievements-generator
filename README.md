# python-achievements-generator

Generate a single Steam-ready banner image that combines Xbox (TrueAchievements),
PlayStation (PSNProfiles), and RetroAchievements public profile stats.

Two supported ways to use this tool:

1. **Scrape your public profiles** (`generate`): fetch fresh stats from each
   platform, cache the results, and render a 1500x450 PNG. If scraping fails,
   the last good cached numbers are used; if there's no cache, placeholders are
   used. This is the default workflow.
2. **Hand-edit your stats** (`render-manual`): fill in the numbers yourself in
   a YAML file and render from those. No scraping, no cache, no browser. This
   is a first-class, fully supported path — use it if you'd rather not run a
   scraper against third-party sites, want to customize values the scrapers
   don't expose, or just want a quick preview. See the `render-manual` section
   below.

## Setup

```bash
pip install -r requirements.txt
playwright install chromium   # one-time — downloads the browser binary
```

On Linux you may need a few system libraries the first time you launch the
browser. If Playwright complains, install the suggested packages via your
distro's package manager (e.g. `sudo dnf install nspr nss libXcomposite
libXdamage libXrandr libXtst libxkbcommon libXScrnSaver gtk3 pango atk
cairo-gobject cairo gdk-pixbuf2 freetype fontconfig alsa-lib at-spi2-atk
at-spi2-core mesa-libgbm` on Oracle Linux / RHEL, or `sudo apt-get install`
the Debian/Ubuntu equivalents).

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

All commands are run as a module from the repo root. The subcommand comes
after any global flags.

```
python -m src.main [global flags] <command>
```

---

### `generate` — scrape, cache, and render

Fetches fresh stats from all three platforms, updates the cache, and writes
`data/output/banner.png`. This is the normal day-to-day command.

```bash
python -m src.main generate
```

Use verbose logging to see exactly what each platform returned:

```bash
python -m src.main -v generate
```

Write the banner to a custom path:

```bash
python -m src.main generate --output ~/Desktop/banner.png
```

---

### `scrape` — scrape only, no render

Fetches fresh stats and updates the cache files but does not produce a PNG.
Useful if you want to update the numbers and render later, or just verify that
scraping is working.

```bash
python -m src.main scrape
```

---

### `render` — render from cache, no scraping

Reads the cached JSON files and renders the banner without opening a browser.
Fast — typically completes in under two seconds. Use this when you've already
scraped recently and just want to regenerate the image (e.g. after swapping in
a new background template).

```bash
python -m src.main render
```

Render to a different output file:

```bash
python -m src.main render --output out/preview.png
```

Render using a different cache directory (e.g. a snapshot you saved earlier):

```bash
python -m src.main render --cache-dir data/cache-backup
```

---

### `render-manual` — render from a hand-edited YAML file

**Use this if you'd rather not scrape.** It's a fully supported workflow for
anyone who wants to produce a banner without running a browser against
TrueAchievements, PSNProfiles, or RetroAchievements — just fill in your
numbers in a YAML file and render directly from it. No scraping, no cache,
no browser launch.

Renders the banner from `data/overrides/manual.yaml`. The file is read only
when you run this command — `generate`, `scrape`, and `render` never touch it.

To get started, copy the template and edit your values:

```bash
cp config/example_manual.yaml data/overrides/manual.yaml
# edit data/overrides/manual.yaml
python -m src.main render-manual
```

Use a different manual file:

```bash
python -m src.main render-manual --manual path/to/my-values.yaml
```

Write to a different output path:

```bash
python -m src.main render-manual --output out/manual-preview.png
```

---

### `build-template` — regenerate the background template

Rebuilds and saves the procedural gradient background to
`assets/template/base_template.png`. Only needed if you delete the template
file or want to reset it after experimenting with a custom background.

```bash
python -m src.main build-template
```

---

### Global flags

These flags apply to all commands and must appear **before** the subcommand:

| Flag | Default | Description |
|---|---|---|
| `--config PATH` | `config/profiles.yaml` | Profile URLs and display names |
| `--cache-dir PATH` | `data/cache` | Directory for cached JSON stats and avatars |
| `--output PATH` | `data/output/banner.png` | Output PNG path (`generate` and `render` only) |
| `-v` / `--verbose` | off | Enable DEBUG-level logging |

Example combining several flags:

```bash
python -m src.main -v generate \
  --config config/profiles-alt.yaml \
  --output data/output/banner-alt.png
```

---

## Data flow

### `generate` / `scrape` — live data pipeline

```
config/profiles.yaml
      │  (profile URLs)
      ▼
  Scrapers  ──── live fetch via Playwright browser
      │               (TrueAchievements / PSNProfiles / RetroAchievements)
      │  fresh stats
      ▼
   Merge  ◄──── data/cache/<platform>.json   (last successful scrape)
      │    ◄──── placeholder zeros           (last resort)
      │
      ▼
  Renderer  ──► data/output/banner.png   (generate only)
```

**Priority order** (highest wins):

1. **Fresh scrape** — live data fetched this run.
2. **Cache** — JSON written by the last successful scrape. Fills any fields
   the fresh scrape couldn't populate (e.g. avatar URL not found on the page
   today).
3. **Placeholder zeros** — last resort so the renderer never crashes.

**When each applies:**

| Situation | What you see |
|---|---|
| Scrape succeeds | Fresh numbers; cache updated |
| Scrape partially succeeds | Fresh fields + cached fields fill the gaps; cache updated |
| Scrape fails, cache exists | Last cached numbers |
| Scrape fails, no cache | Placeholder zeros |

**Avatars** follow the same priority but simpler: if a file already exists in
`data/cache/avatars/` it is always used and never re-downloaded, even when a
new URL is returned by the scraper. Drop a replacement file there to change
the avatar permanently.

### `render-manual` — hand-edited data pipeline

```
data/overrides/manual.yaml
      │  (your hand-edited values)
      ▼
  Renderer  ──► data/output/banner.png
```

Manual values are completely independent of the scrape/cache pipeline — they
are only used when you explicitly run `render-manual`. Copy
`config/example_manual.yaml` to `data/overrides/manual.yaml` to get started.

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

Priority when resolving each platform during `generate` / `scrape`:
**fresh scrape > cache > placeholder**.

| State                       | Result                      |
| --------------------------- | --------------------------- |
| Scrape succeeds             | Overwrite cache, render     |
| Scrape partial              | Merge with cache, render    |
| Scrape fails, cache exists  | Render from cache           |
| Scrape fails, no cache      | Render platform placeholder |

To render from hand-edited values, use `render-manual` (see above).

## Scraping caveats

TrueAchievements, PSNProfiles, and RetroAchievements all sit behind Cloudflare,
and header-spoofing / TLS-level workarounds no longer clear their challenges.
The project drives a real browser via [Playwright](https://playwright.dev/python/)
— one Chromium instance is launched at the start of each `generate` run and
reused across all three URLs (Cloudflare clearance cookies stick for the
duration of the run).

Defaults:

- **Browser**: Chromium. Override with `BANNER_BROWSER=firefox` or
  `BANNER_BROWSER=webkit`.
- **Headed window**: a visible window pops up briefly during the run. Cloudflare
  detects headless reliably, so headed is the default. Force headless with
  `BANNER_HEADLESS=1` — expect some sites to block it.

For RetroAchievements you can also skip the browser entirely by using the
official JSON API. Create a key at
<https://retroachievements.org/controlpanel.php> and set two environment
variables before running:

```bash
export RA_API_USER="your-ra-username"
export RA_API_KEY="your-api-key"
python -m src.main generate
```

When both are present the RA provider fetches via the API and doesn't hit the
browser path at all.

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
