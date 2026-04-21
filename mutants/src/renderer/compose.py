"""Top-level renderer: backdrop -> per-platform panels -> PNG."""
from __future__ import annotations

import logging
from pathlib import Path

from PIL import Image, ImageDraw

from ..cache import find_cached_avatar
from ..models import PlatformStats, SubStat
from ..services.normalize import format_int, format_ratio
from . import draw as D
from .layout import (
    BG_BOTTOM,
    BG_TOP,
    CANVAS_H,
    CANVAS_W,
    PANEL_BORDER_W,
    PANEL_FILL,
    PANEL_FILL_INNER,
    PANEL_RADIUS,
    PLATFORM_ORDER,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    THEMES,
    panel_regions,
)

log = logging.getLogger(__name__)

TEMPLATE_PATH = Path(__file__).resolve().parents[2] / "assets" / "template" / "base_template.png"


def load_or_build_template() -> Image.Image:
    if TEMPLATE_PATH.exists():
        try:
            tpl = Image.open(TEMPLATE_PATH).convert("RGBA")
            if tpl.size == (CANVAS_W, CANVAS_H):
                return tpl
            log.info(
                "template: fitting user artwork %s to canvas %dx%d",
                tpl.size, CANVAS_W, CANVAS_H,
            )
            return _fit_to_canvas(tpl, CANVAS_W, CANVAS_H)
        except OSError as exc:
            log.warning("template: failed to open %s: %s", TEMPLATE_PATH, exc)

    tpl = build_base_template()
    TEMPLATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    tpl.save(TEMPLATE_PATH)
    log.info("template: wrote base template to %s", TEMPLATE_PATH)
    return tpl


def _fit_to_canvas(img: Image.Image, w: int, h: int) -> Image.Image:
    """Cover-fit + piecewise vertical warp + center crop so the template's
    grid lines land at the canvas positions needed to align with existing
    content (separators between gamertag/headline/stats/footer rows).

    Original template (1024 tall) has 3 horizontal grid lines at y ≈ 423, 660, 724.
    Line 1 is aligned as-is; lines 2 and 3 get pulled up by 150 / 30 canvas px
    respectively via piecewise vertical resampling of the inter-line bands."""
    src_w, src_h = img.size
    scale = max(w / src_w, h / src_h)
    new_w = int(round(src_w * scale))
    new_h = int(round(src_h * scale))
    img = img.resize((new_w, new_h), Image.LANCZOS)

    line1 = int(423 * scale)
    line2 = int(660 * scale)
    line3 = int(724 * scale)

    y_shift = 35  # template baseline offset (positive = crop from lower in source)
    crop_top = (new_h - h) // 2 + y_shift
    crop_top = max(0, min(crop_top, new_h - h))

    # target source y for each line so the resulting canvas position is correct
    target_line2 = crop_top + (line2 - crop_top) - 120  # up 150 canvas px
    target_line3 = crop_top + (line3 - crop_top) - 30   # up 30 canvas px

    warped = Image.new("RGBA", (new_w, new_h))
    # band 0: above line 1 — unchanged
    warped.paste(img.crop((0, 0, new_w, line1)), (0, 0))
    # band 1: line 1 → line 2 — compress to new height
    band_h = max(1, target_line2 - line1)
    b = img.crop((0, line1, new_w, line2)).resize((new_w, band_h), Image.LANCZOS)
    warped.paste(b, (0, line1))
    # band 2: line 2 → line 3 — resize to span to new line 3
    band_h = max(1, target_line3 - target_line2)
    b = img.crop((0, line2, new_w, line3)).resize((new_w, band_h), Image.LANCZOS)
    warped.paste(b, (0, target_line2))
    # band 3: below line 3 — shifted up, original pixel height
    b = img.crop((0, line3, new_w, new_h))
    warped.paste(b, (0, target_line3))

    x0 = (new_w - w) // 2
    return warped.crop((x0, crop_top, x0 + w, crop_top + h))


def build_base_template() -> Image.Image:
    """Procedural backdrop: gradient sky + panel-colour glows + panel bodies."""
    glows = [THEMES[p].accent for p in PLATFORM_ORDER]
    bg = D.build_background((CANVAS_W, CANVAS_H), BG_TOP, BG_BOTTOM, accent_colors=glows)
    draw = ImageDraw.Draw(bg)

    for idx, platform in enumerate(PLATFORM_ORDER):
        theme = THEMES[platform]
        regions = panel_regions(idx)

        # solid dark panel body (includes the footer area — the footer is dark
        # in the example, not a colored strip)
        D.rounded_rect(draw, regions.panel, radius=PANEL_RADIUS, fill=PANEL_FILL)

        # faint lifted block behind the label + headline area
        D.rounded_rect(draw, regions.headline_block, radius=12, fill=PANEL_FILL_INNER)

        # thin accent-color divider line above the footer
        draw.rectangle(regions.footer_divider, fill=theme.accent)

        # full accent-color border around the whole panel
        D.rounded_rect(
            draw,
            regions.panel,
            radius=PANEL_RADIUS,
            outline=theme.accent,
            width=PANEL_BORDER_W,
        )

    return bg


def render(
    stats_by_platform: dict[str, PlatformStats],
    cache_dir: Path,
    output_path: Path,
) -> Path:
    canvas = load_or_build_template().copy()
    draw = ImageDraw.Draw(canvas)

    for idx, platform in enumerate(PLATFORM_ORDER):
        stats = stats_by_platform.get(platform)
        if stats is None:
            continue
        _render_panel(canvas, draw, idx, platform, stats, cache_dir)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    canvas.convert("RGB").save(output_path, "PNG")
    log.info("render: wrote %s", output_path)
    return output_path


def _render_panel(canvas, draw, index, platform, stats, cache_dir):
    theme = THEMES[platform]
    regions = panel_regions(index)

    _draw_header(canvas, draw, regions, theme, stats, cache_dir)
    _draw_label_and_headline(draw, regions, theme, stats)
    _draw_stats_row(canvas, draw, regions.stats, stats.substats, platform)
    _draw_footer(canvas, draw, regions, theme)


def _draw_header(canvas, draw, regions, theme, stats, cache_dir):
    # Shift the avatar around its own center so growing the size doesn't drag
    # the image off-center. dx/dy are the requested nudges from default.
    dx = 0 if stats.platform == "psn" else -14
    dy = -15
    ax0, ay0, ax1, ay1 = regions.avatar
    cx = (ax0 + ax1) // 2 + dx
    cy = (ay0 + ay1) // 2 + dy
    half = (ax1 - ax0) // 2
    avatar_box = (cx - half, cy - half, cx - half + (ax1 - ax0), cy - half + (ay1 - ay0))
    avatar_img = _load_avatar(cache_dir, stats.platform)
    if avatar_img is not None:
        D.paste_circle_avatar(canvas, avatar_img, avatar_box, theme.avatar_ring)
    else:
        D.draw_placeholder_avatar(draw, avatar_box, theme.avatar_ring)

    nx0, ny0, nx1, ny1 = regions.name_block
    if stats.platform == "psn":
        nx0 += 15  # per-user request: nudge PSN name+network text right
    username = stats.username or "Player"
    name_font = D.fit_font(draw, username, max_w=nx1 - nx0, max_h=32, start=30, bold=True)
    D.draw_text(draw, (nx0, ny0), username, name_font, TEXT_PRIMARY, anchor="la")

    sub_font = D.get_font(22, bold=True)
    sub_y = ny0 + 40
    cursor_x = nx0
    if theme.display_prefix:
        D.draw_text(draw, (cursor_x, sub_y), theme.display_prefix, sub_font, theme.accent, anchor="la")
        pw, _ = D.text_size(draw, theme.display_prefix, sub_font)
        cursor_x += pw + 8
    D.draw_text(
        draw, (cursor_x, sub_y), theme.display_name, sub_font, TEXT_SECONDARY, anchor="la"
    )


def _draw_label_and_headline(draw, regions, theme, stats):
    if stats.platform == "retroachievements":
        _draw_ra_dual_headline(draw, regions, stats)
        return
    label = stats.headline_label or ""
    label_font = D.fit_font(
        draw, label, max_w=regions.label[2] - regions.label[0] - 8, max_h=22, start=22, bold=True
    )
    lx = (regions.label[0] + regions.label[2]) // 2
    ly = (regions.label[1] + regions.label[3]) // 2
    D.draw_text(draw, (lx, ly), label, label_font, theme.label_color, anchor="mm")

    headline = _format_headline(stats)
    hx = (regions.headline[0] + regions.headline[2]) // 2
    hy = (regions.headline[1] + regions.headline[3]) // 2 + 4
    head_font = D.fit_font(
        draw,
        headline,
        max_w=regions.headline[2] - regions.headline[0] - 16,
        max_h=regions.headline[3] - regions.headline[1] - 10,
        start=62,
        bold=True,
    )
    D.draw_text(draw, (hx, hy), headline, head_font, TEXT_PRIMARY, anchor="mm", shadow=True)


def _draw_ra_dual_headline(draw, regions, stats):
    """RA headline: Hardcore Points (TotalPoints) | RetroPoints (TotalTruePoints)."""
    extras = stats.extra_fields or {}
    hp = extras.get("TotalPoints")
    rp = extras.get("TotalTruePoints")
    hp_color = (222, 180, 56)   # gold
    rp_color = (208, 128, 44)   # amber

    lx0, ly0, lx1, ly1 = regions.label
    label_cy = (ly0 + ly1) // 2
    col_w_lbl = (lx1 - lx0) // 2
    left_lx = lx0 + col_w_lbl // 2
    right_lx = lx0 + col_w_lbl + col_w_lbl // 2
    label_font = D.fit_font(
        draw, "Hardcore Points", max_w=col_w_lbl - 10, max_h=22, start=20, bold=True
    )
    D.draw_text(draw, (left_lx, label_cy), "Hardcore Points", label_font, hp_color, anchor="mm")
    D.draw_text(draw, (right_lx, label_cy), "RetroPoints", label_font, rp_color, anchor="mm")

    hx0, hy0, hx1, hy1 = regions.headline
    col_w_val = (hx1 - hx0) // 2
    left_hx = hx0 + col_w_val // 2
    right_hx = hx0 + col_w_val + col_w_val // 2
    val_cy = (hy0 + hy1) // 2 + 4

    hp_text = format_int(hp) if isinstance(hp, (int, float)) else "--"
    rp_text = format_int(rp) if isinstance(rp, (int, float)) else "--"
    probe = hp_text if len(hp_text) >= len(rp_text) else rp_text
    val_font = D.fit_font(
        draw,
        probe,
        max_w=col_w_val - 16,
        max_h=hy1 - hy0 - 10,
        start=48,
        bold=True,
    )
    D.draw_text(draw, (left_hx, val_cy), hp_text, val_font, TEXT_PRIMARY, anchor="mm", shadow=True)
    D.draw_text(draw, (right_hx, val_cy), rp_text, val_font, TEXT_PRIMARY, anchor="mm", shadow=True)


def _draw_stats_row(canvas, draw, box, substats: list[SubStat], platform: str):
    """Each substat is rendered as a vertical stack: icon/badge on top, number
    directly beneath, centered in its slot."""
    if not substats:
        return
    x0, y0, x1, y1 = box
    slots = len(substats)
    slot_w = (x1 - x0) / slots
    available_h = y1 - y0

    icon_size = 35  # +10% over prior 32
    vgap = 15  # +25% over prior 12
    max_value_h = 40

    stack_h = icon_size + vgap + max_value_h
    top_y = y0 + max(2, (available_h - stack_h) // 2)

    for i, s in enumerate(substats):
        slot_cx = int(x0 + slot_w * (i + 0.5))
        icon_cy = top_y + icon_size // 2
        _draw_stat_icon(canvas, draw, s.label, slot_cx, icon_cy, icon_size, platform)

        value_text = _format_stat_value(s)
        value_font = D.fit_font(
            draw, value_text,
            max_w=int(slot_w - 20),
            max_h=max_value_h,
            start=44,
            minimum=22,
            bold=True,
        )
        D.draw_text(
            draw,
            (slot_cx, top_y + icon_size + vgap),
            value_text,
            value_font,
            TEXT_PRIMARY,
            anchor="mt",
        )


def _draw_stat_icon(canvas, draw, label: str, cx: int, cy: int, size: int, platform: str):
    key = (label or "").lower()
    # RA uses labeled pill badges for softcore / hardcore / true ratio / mastery
    badge = _ra_badge_colors().get(key)
    if badge is not None:
        display = _RA_LABEL_DISPLAY.get(key, label.upper())
        D.draw_label_badge(draw, cx, cy, int(size * 1.08), display, fill=badge)
        return
    # User-supplied PNG takes priority (e.g. assets/icons/psn/platinum.png)
    real = D.load_stat_icon(platform, key)
    if real is not None:
        D.paste_centered_icon(canvas, real, cx, cy, size)
        return
    if key in ("star", "stars", "masteries"):
        D.draw_star(draw, cx, cy, size, filled=True)
        return
    color = _icon_colors(platform).get(key, (205, 210, 220))
    D.draw_trophy(draw, cx, cy, size, color)


def _format_stat_value(s: SubStat) -> str:
    if isinstance(s.value, bool):
        return str(s.value)
    if isinstance(s.value, float):
        return format_ratio(s.value)
    if isinstance(s.value, int):
        return format_int(s.value)
    return str(s.value)


def _draw_footer(canvas, draw, regions, theme):
    """Dark footer with a platform icon on the left and the platform name
    centered. Uses assets/icons/<platform>.png if present, otherwise a
    procedural glyph. The thin accent divider above is painted in
    build_base_template."""
    x0, y0, x1, y1 = regions.footer
    pad = 16
    cy = (y0 + y1) // 2
    icon_h = (y1 - y0) - 8  # ~15% larger footer logos
    icon_box = (x0 + pad, cy - icon_h // 2,
                x0 + pad + int(icon_h * 3.2), cy + icon_h // 2)

    real = D.load_platform_icon(theme.key)
    if real is not None:
        icon_bbox = D.paste_platform_icon(canvas, real, icon_box)
        label_area_l = icon_bbox[2] + 10
    else:
        # procedural fallback: use a square glyph
        glyph_box = (x0 + pad, cy - icon_h // 2,
                     x0 + pad + icon_h, cy + icon_h // 2)
        D.draw_platform_icon(draw, theme.key, glyph_box, theme.accent)
        label_area_l = glyph_box[2] + 8

    label_area_r = x1 - pad
    font = D.get_font(20, bold=True)
    cx = (label_area_l + label_area_r) // 2
    D.draw_text(draw, (cx, cy), theme.footer_label, font, TEXT_PRIMARY, anchor="mm")


def _load_avatar(cache_dir: Path, platform: str) -> Image.Image | None:
    p = find_cached_avatar(cache_dir, platform)
    if not p:
        return None
    try:
        return Image.open(p)
    except OSError as exc:
        log.warning("avatar: cannot open %s: %s", p, exc)
        return None


def _format_headline(stats: PlatformStats) -> str:
    value = stats.headline_value
    if value is None:
        return "--"
    if isinstance(value, (int, float)):
        return format_int(value)
    return str(value)


def _icon_colors(platform: str) -> dict[str, tuple[int, int, int]]:
    return {
        "platinum": (160, 210, 240),
        "gold": (230, 190, 60),
        "silver": (200, 205, 215),
        "bronze": (200, 120, 70),
        "trophy": (230, 190, 60),
        "completions": (230, 190, 60),
    }


_RA_LABEL_DISPLAY = {
    "rr": "RETRORATIO",
    "b":  "BEATEN",
    "m":  "MASTERED",
    "ta": "TRUEACHIEVEMENT SCORE",
}


def _ra_badge_colors() -> dict[str, tuple[int, int, int]]:
    """Per-stat badge colours for the RetroAchievements pill labels."""
    return {
        "rr": (208, 128, 44),    # RetroRatio — amber
        "b":  (210, 85, 85),     # Beaten — warm red
        "m":  (156, 196, 80),    # Mastered — green/gold
        "ta": (80, 170, 200),    # TrueAchievement Score — teal
    }
