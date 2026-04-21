"""Top-level renderer: composites all platform panels onto the banner canvas.

Pipeline:
  load_or_build_template()   →  RGBA canvas (gradient bg + panel shapes)
  render()                   →  iterates over platforms, calls _render_panel()
  _render_panel()            →  calls five row-drawing functions in order
  _draw_*_row()              →  each draws one horizontal strip of a panel

Every platform panel (xbox / psn / retroachievements) traces through the same
five row functions. The label and headline rows delegate to a shared
``_draw_text_cells_in_row`` helper, so a 1-cell xbox label and a 2-cell RA
label are the same function call — only the cell list differs.
"""
from __future__ import annotations

import logging
from pathlib import Path

from PIL import Image, ImageDraw

from ..cache import find_cached_avatar
from ..models import PlatformStats, SubStat
from ..services.normalize import format_headline_value, format_substat_value
from . import draw
from .layout import (
    BACKGROUND_GRADIENT_BOTTOM_RGB,
    BACKGROUND_GRADIENT_TOP_RGB,
    Box,
    CANVAS_HEIGHT_PX,
    CANVAS_WIDTH_PX,
    HEADLINE_BLOCK_CORNER_RADIUS_PX,
    PANEL_BORDER_WIDTH_PX,
    PANEL_CORNER_RADIUS_PX,
    PANEL_FILL_INNER_RGB,
    PANEL_FILL_RGB,
    PLATFORM_ORDER,
    TEXT_PRIMARY_RGB,
    TEXT_SECONDARY_RGB,
    THEMES,
    offset_box,
    panel_regions,
)

log = logging.getLogger(__name__)

TEMPLATE_PATH = Path(__file__).resolve().parents[2] / "assets" / "template" / "base_template.png"

# ---------------------------------------------------------------------------
# Typography — font sizes and bounding-box padding per row
# ---------------------------------------------------------------------------

# Header row
USERNAME_FONT_START_PX = 30
USERNAME_FONT_MAX_HEIGHT_PX = 32
SUBTITLE_FONT_PX = 22
SUBTITLE_VERTICAL_OFFSET_FROM_USERNAME_PX = 40
SUBTITLE_PREFIX_TO_NAME_GAP_PX = 8

# Label row
LABEL_FONT_START_PX = 26
LABEL_FONT_MAX_HEIGHT_PX = 26
LABEL_HORIZONTAL_PADDING_PX = 8
RA_LABEL_HORIZONTAL_PADDING_PX = 10

# Headline row
HEADLINE_FONT_START_PX = 62
HEADLINE_HORIZONTAL_INSET_PX = 16
HEADLINE_VERTICAL_INSET_PX = 10
HEADLINE_OPTICAL_CENTER_NUDGE_PX = 4
RA_HEADLINE_FONT_START_PX = 48

# Stats row
STAT_ICON_SIZE_PX = 35
STAT_ICON_TO_VALUE_GAP_PX = 15
STAT_VALUE_MAX_HEIGHT_PX = 40
STAT_VALUE_FONT_START_PX = 44
STAT_VALUE_FONT_MIN_PX = 22
STAT_VALUE_HORIZONTAL_PADDING_PX = 20
STAT_STACK_MIN_TOP_INSET_PX = 2
RA_PILL_BADGE_GAP_PX = 8
RA_PILL_BADGE_HEIGHT_SCALE = 1.08

# Footer row
FOOTER_HORIZONTAL_PADDING_PX = 16
FOOTER_ICON_VERTICAL_INSET_PX = 8
FOOTER_ICON_WIDTH_TO_HEIGHT_RATIO = 3.2
FOOTER_ICON_TO_LABEL_GAP_PX = 10
FOOTER_PROCEDURAL_ICON_TO_LABEL_GAP_PX = 8
FOOTER_LABEL_FONT_PX = 20

# ---------------------------------------------------------------------------
# RA-specific strings, colors, and field keys
# ---------------------------------------------------------------------------

RA_HARDCORE_POINTS_LABEL_TEXT = "Hardcore Points"
RA_RETROPOINTS_LABEL_TEXT = "RetroPoints"
RA_HARDCORE_POINTS_LABEL_COLOR = (222, 180, 56)  # gold
RA_RETROPOINTS_LABEL_COLOR = (208, 128, 44)       # amber

RA_TOTAL_POINTS_EXTRA_FIELD_KEY = "TotalPoints"
RA_TRUE_POINTS_EXTRA_FIELD_KEY = "TotalTruePoints"

DEFAULT_USERNAME_FALLBACK = "Player"
STAT_ICON_DEFAULT_COLOR = (205, 210, 220)

# Maps lowercase substat label keys to display text shown on RA pill badges
_RA_LABEL_DISPLAY_TEXT: dict[str, str] = {
    "rr": "RETRORATIO",
    "b":  "BEATEN",
    "m":  "MASTERED",
    "ta": "TRUEACHIEVEMENT SCORE",
}

# Maps lowercase substat label keys to pill fill colors for RA badges
_RA_BADGE_FILL_COLORS: dict[str, tuple[int, int, int]] = {
    "rr": (208, 128, 44),   # RetroRatio — amber
    "b":  (210, 85, 85),    # Beaten — warm red
    "m":  (156, 196, 80),   # Mastered — green
    "ta": (80, 170, 200),   # TrueAchievement Score — teal
}

# Maps lowercase stat label keys to procedural icon colors (xbox / fallback)
_PROCEDURAL_ICON_COLORS: dict[str, tuple[int, int, int]] = {
    "platinum":    (160, 210, 240),
    "gold":        (230, 190, 60),
    "silver":      (200, 205, 215),
    "bronze":      (200, 120, 70),
    "trophy":      (230, 190, 60),
    "completions": (230, 190, 60),
}

# Stat labels that render as a star icon rather than a trophy
_STAR_ICON_LABEL_KEYS = frozenset({"star", "stars", "masteries"})


# ---------------------------------------------------------------------------
# Template
# ---------------------------------------------------------------------------

def load_or_build_template() -> Image.Image:
    """Return the banner background template as an RGBA image.

    If a saved template exists at TEMPLATE_PATH and matches the canvas size,
    it is returned directly. If it exists but has the wrong size (user
    supplied custom artwork), it is cover-fit and warped to align grid lines.
    If no template exists, a procedural one is generated and saved for reuse.
    """
    if TEMPLATE_PATH.exists():
        try:
            template_image = Image.open(TEMPLATE_PATH).convert("RGBA")
            if template_image.size == (CANVAS_WIDTH_PX, CANVAS_HEIGHT_PX):
                return template_image
            log.info(
                "template: fitting user artwork %s to canvas %dx%d",
                template_image.size, CANVAS_WIDTH_PX, CANVAS_HEIGHT_PX,
            )
            return _fit_to_canvas(template_image, CANVAS_WIDTH_PX, CANVAS_HEIGHT_PX)
        except OSError as error:
            log.warning("template: failed to open %s: %s", TEMPLATE_PATH, error)

    procedural_template = build_base_template()
    TEMPLATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    procedural_template.save(TEMPLATE_PATH)
    log.info("template: wrote base template to %s", TEMPLATE_PATH)
    return procedural_template


def _fit_to_canvas(source_image: Image.Image, target_width: int, target_height: int) -> Image.Image:
    """Cover-fit + piecewise vertical warp + center crop.

    Aligns the template's three horizontal grid lines to the canvas positions
    that match the panel layout (separators between gamertag/headline/stats/footer).

    Original template (1024 px tall) has grid lines at y ≈ 423, 660, 724.
    Line 1 is preserved; lines 2 and 3 are pulled up by 150 px and 30 px
    respectively via piecewise band resampling.
    """
    # Y-positions of the three horizontal grid lines in the un-scaled source template.
    SOURCE_GRID_LINE_1_Y = 423
    SOURCE_GRID_LINE_2_Y = 660
    SOURCE_GRID_LINE_3_Y = 724
    # Shift the crop window downward so the template's visual midpoint aligns
    # with the banner's content rows rather than the exact geometric center.
    CROP_BASELINE_SHIFT_PX = 35
    # Pull each grid line upward via piecewise warp so panel separators in the
    # source artwork align with the banner's layout.
    BAND_1_COMPRESSION_PX = 120
    BAND_2_COMPRESSION_PX = 30

    source_width, source_height = source_image.size
    cover_scale = max(target_width / source_width, target_height / source_height)
    scaled_width = int(round(source_width * cover_scale))
    scaled_height = int(round(source_height * cover_scale))
    source_image = source_image.resize((scaled_width, scaled_height), Image.LANCZOS)

    grid_line_1_y = int(SOURCE_GRID_LINE_1_Y * cover_scale)
    grid_line_2_y = int(SOURCE_GRID_LINE_2_Y * cover_scale)
    grid_line_3_y = int(SOURCE_GRID_LINE_3_Y * cover_scale)

    crop_top = (scaled_height - target_height) // 2 + CROP_BASELINE_SHIFT_PX
    crop_top = max(0, min(crop_top, scaled_height - target_height))

    target_grid_line_2_y = crop_top + (grid_line_2_y - crop_top) - BAND_1_COMPRESSION_PX
    target_grid_line_3_y = crop_top + (grid_line_3_y - crop_top) - BAND_2_COMPRESSION_PX

    warped = Image.new("RGBA", (scaled_width, scaled_height))
    warped.paste(source_image.crop((0, 0, scaled_width, grid_line_1_y)), (0, 0))

    band_1_height = max(1, target_grid_line_2_y - grid_line_1_y)
    warped.paste(
        source_image.crop((0, grid_line_1_y, scaled_width, grid_line_2_y)).resize(
            (scaled_width, band_1_height), Image.LANCZOS,
        ),
        (0, grid_line_1_y),
    )

    band_2_height = max(1, target_grid_line_3_y - target_grid_line_2_y)
    warped.paste(
        source_image.crop((0, grid_line_2_y, scaled_width, grid_line_3_y)).resize(
            (scaled_width, band_2_height), Image.LANCZOS,
        ),
        (0, target_grid_line_2_y),
    )

    warped.paste(
        source_image.crop((0, grid_line_3_y, scaled_width, scaled_height)),
        (0, target_grid_line_3_y),
    )

    crop_left = (scaled_width - target_width) // 2
    return warped.crop((crop_left, crop_top, crop_left + target_width, crop_top + target_height))


def build_base_template() -> Image.Image:
    """Build the procedural backdrop: gradient sky + panel glows + panel bodies."""
    accent_glow_colors = [THEMES[platform].accent for platform in PLATFORM_ORDER]
    background = draw.build_background(
        (CANVAS_WIDTH_PX, CANVAS_HEIGHT_PX),
        BACKGROUND_GRADIENT_TOP_RGB,
        BACKGROUND_GRADIENT_BOTTOM_RGB,
        accent_colors=accent_glow_colors,
    )
    pen = ImageDraw.Draw(background)
    for panel_index, platform in enumerate(PLATFORM_ORDER):
        theme = THEMES[platform]
        regions = panel_regions(panel_index)
        draw.rounded_rect(pen, regions.panel, radius=PANEL_CORNER_RADIUS_PX, fill=PANEL_FILL_RGB)
        draw.rounded_rect(pen, regions.headline_block, radius=HEADLINE_BLOCK_CORNER_RADIUS_PX, fill=PANEL_FILL_INNER_RGB)
        pen.rectangle(regions.footer_divider, fill=theme.accent)
        draw.rounded_rect(
            pen, regions.panel,
            radius=PANEL_CORNER_RADIUS_PX, outline=theme.accent, width=PANEL_BORDER_WIDTH_PX,
        )
    return background


# ---------------------------------------------------------------------------
# Public render entry point
# ---------------------------------------------------------------------------

def render(
    stats_by_platform: dict[str, PlatformStats],
    cache_dir: Path,
    output_path: Path,
) -> Path:
    """Render all platform panels onto the banner and save to `output_path`.

    Missing platforms are skipped rather than crashing — the banner renders
    with however many panels have data. Returns the output path on success.
    """
    canvas = load_or_build_template().copy()
    pen = ImageDraw.Draw(canvas)
    for panel_index, platform in enumerate(PLATFORM_ORDER):
        stats = stats_by_platform.get(platform)
        if stats is None:
            continue
        _render_panel(canvas, pen, panel_index, platform, stats, cache_dir)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    canvas.convert("RGB").save(output_path, "PNG")
    log.info("render: wrote %s", output_path)
    return output_path


def _render_panel(
    canvas: Image.Image,
    pen: ImageDraw.ImageDraw,
    panel_index: int,
    platform: str,
    stats: PlatformStats,
    cache_dir: Path,
) -> None:
    """Draw all five rows of one platform panel onto the canvas."""
    theme = THEMES[platform]
    regions = panel_regions(panel_index)
    _draw_header_row(canvas, pen, regions, theme, stats, cache_dir)
    _draw_label_row(pen, regions, theme, stats)
    _draw_headline_row(pen, regions, stats)
    _draw_stats_row(canvas, pen, regions.stats, stats.substats, platform)
    _draw_footer_row(canvas, pen, regions, theme)


# ---------------------------------------------------------------------------
# Shared helper: N centered-text cells in a row, one fitted font across all
# ---------------------------------------------------------------------------

def _draw_text_cells_in_row(
    pen: ImageDraw.ImageDraw,
    row_box: Box,
    cells: list[tuple[str, tuple[int, int, int]]],
    *,
    font_start_px: int,
    font_max_h_px: int,
    horizontal_padding_px: int,
    vertical_nudge_px: int = 0,
    shadow: bool = False,
) -> None:
    """Render N evenly-divided centered-text cells into `row_box`.

    A single font size is chosen that fits the widest cell's text, so every
    cell uses the same font. Drives both the label row (1 cell xbox/psn,
    2 cells RA) and the headline row (same).
    """
    if not cells:
        return
    x0, y0, x1, y1 = row_box
    cell_width = (x1 - x0) / len(cells)
    widest_text = max((text for text, _ in cells), key=len)
    font = draw.fit_font(
        pen, widest_text,
        max_w=int(cell_width) - horizontal_padding_px,
        max_h=font_max_h_px,
        start=font_start_px,
        bold=True,
    )
    center_y = (y0 + y1) // 2 + vertical_nudge_px
    for cell_index, (text, color) in enumerate(cells):
        center_x = int(x0 + cell_width * (cell_index + 0.5))
        draw.draw_text(pen, (center_x, center_y), text, font, color, anchor="mm", shadow=shadow)


# ---------------------------------------------------------------------------
# Row 1: header (avatar + username + network subtitle)
# ---------------------------------------------------------------------------

def _draw_header_row(
    canvas: Image.Image,
    pen: ImageDraw.ImageDraw,
    regions,
    theme,
    stats: PlatformStats,
    cache_dir: Path,
) -> None:
    """Circular avatar on the left, username and network subtitle on the right.

    ``theme.avatar_offset`` shifts the avatar around its own center so
    resizing doesn't drag it off-axis. ``theme.name_offset_x`` nudges the
    username text block rightward.
    """
    avatar_box = offset_box(regions.avatar, *theme.avatar_offset)
    avatar_image = _load_avatar_image(cache_dir, stats.platform)
    if avatar_image is not None:
        draw.paste_circle_avatar(canvas, avatar_image, avatar_box, theme.avatar_ring)
    else:
        draw.draw_placeholder_avatar(pen, avatar_box, theme.avatar_ring)

    name_left, name_top, name_right, _ = regions.name_block
    name_left += theme.name_offset_x
    username = stats.username or DEFAULT_USERNAME_FALLBACK
    username_font = draw.fit_font(
        pen, username,
        max_w=name_right - name_left,
        max_h=USERNAME_FONT_MAX_HEIGHT_PX,
        start=USERNAME_FONT_START_PX,
        bold=True,
    )
    draw.draw_text(pen, (name_left, name_top), username, username_font, TEXT_PRIMARY_RGB, anchor="la")

    subtitle_font = draw.get_font(SUBTITLE_FONT_PX, bold=True)
    subtitle_y = name_top + SUBTITLE_VERTICAL_OFFSET_FROM_USERNAME_PX
    cursor_x = name_left
    if theme.display_prefix:
        draw.draw_text(pen, (cursor_x, subtitle_y), theme.display_prefix, subtitle_font, theme.accent, anchor="la")
        prefix_width, _ = draw.text_size(pen, theme.display_prefix, subtitle_font)
        cursor_x += prefix_width + SUBTITLE_PREFIX_TO_NAME_GAP_PX
    draw.draw_text(pen, (cursor_x, subtitle_y), theme.display_name, subtitle_font, TEXT_SECONDARY_RGB, anchor="la")


# ---------------------------------------------------------------------------
# Row 2: label strip (1 cell for xbox/psn, 2 cells for RA)
# ---------------------------------------------------------------------------

def _draw_label_row(
    pen: ImageDraw.ImageDraw,
    regions,
    theme,
    stats: PlatformStats,
) -> None:
    """One centered label (xbox/psn) or two side-by-side labels (RA)."""
    if stats.platform == "retroachievements":
        cells = [
            (RA_HARDCORE_POINTS_LABEL_TEXT, RA_HARDCORE_POINTS_LABEL_COLOR),
            (RA_RETROPOINTS_LABEL_TEXT, RA_RETROPOINTS_LABEL_COLOR),
        ]
        font_start_px = LABEL_FONT_START_PX - 2
        horizontal_padding_px = RA_LABEL_HORIZONTAL_PADDING_PX
    else:
        cells = [(stats.headline_label or "", theme.label_color)]
        font_start_px = LABEL_FONT_START_PX
        horizontal_padding_px = LABEL_HORIZONTAL_PADDING_PX
    _draw_text_cells_in_row(
        pen, regions.label, cells,
        font_start_px=font_start_px,
        font_max_h_px=LABEL_FONT_MAX_HEIGHT_PX,
        horizontal_padding_px=horizontal_padding_px,
    )


# ---------------------------------------------------------------------------
# Row 3: headline value (1 cell for xbox/psn, 2 cells for RA)
# ---------------------------------------------------------------------------

def _draw_headline_row(
    pen: ImageDraw.ImageDraw,
    regions,
    stats: PlatformStats,
) -> None:
    """One big headline value (xbox/psn) or two side-by-side values (RA).

    Headline text is drawn with a drop shadow and nudged slightly below the
    geometric center, because large numerals with ascenders read as too high
    otherwise.
    """
    if stats.platform == "retroachievements":
        extra = stats.extra_fields or {}
        cells = [
            (format_headline_value(extra.get(RA_TOTAL_POINTS_EXTRA_FIELD_KEY)), TEXT_PRIMARY_RGB),
            (format_headline_value(extra.get(RA_TRUE_POINTS_EXTRA_FIELD_KEY)), TEXT_PRIMARY_RGB),
        ]
        font_start_px = RA_HEADLINE_FONT_START_PX
    else:
        cells = [(format_headline_value(stats.headline_value), TEXT_PRIMARY_RGB)]
        font_start_px = HEADLINE_FONT_START_PX
    _draw_text_cells_in_row(
        pen, regions.headline, cells,
        font_start_px=font_start_px,
        font_max_h_px=(regions.headline[3] - regions.headline[1]) - HEADLINE_VERTICAL_INSET_PX,
        horizontal_padding_px=HEADLINE_HORIZONTAL_INSET_PX,
        vertical_nudge_px=HEADLINE_OPTICAL_CENTER_NUDGE_PX,
        shadow=True,
    )


# ---------------------------------------------------------------------------
# Row 4: stats (icons + values)
# ---------------------------------------------------------------------------

def _draw_stats_row(
    canvas: Image.Image,
    pen: ImageDraw.ImageDraw,
    stats_box: Box,
    substats: list[SubStat],
    platform: str,
) -> None:
    """N stat cells, each an icon stacked above a numeric value.

    For RetroAchievements (all pill badges), slot centers are recomputed from
    actual pill widths so the visible gap between adjacent pills is equal
    regardless of pill width. All other platforms use evenly-spaced centers.
    """
    if not substats:
        return
    stats_left, stats_top, stats_right, stats_bottom = stats_box
    slot_width = (stats_right - stats_left) / len(substats)
    slot_centers = (
        _compute_ra_pill_centers(pen, stats_left, stats_right, substats)
        if platform == "retroachievements" else None
    ) or [int(stats_left + slot_width * (i + 0.5)) for i in range(len(substats))]

    for i, substat in enumerate(substats):
        cell_box = (
            int(stats_left + slot_width * i), stats_top,
            int(stats_left + slot_width * (i + 1)), stats_bottom,
        )
        _draw_stat_cell(canvas, pen, cell_box, slot_centers[i], slot_width, substat, platform)


def _draw_stat_cell(
    canvas: Image.Image,
    pen: ImageDraw.ImageDraw,
    cell_box: Box,
    slot_center_x: int,
    slot_width: float,
    substat: SubStat,
    platform: str,
) -> None:
    """Icon on top, numeric value directly beneath. Stack vertically centered in the cell."""
    _, cell_top, _, cell_bottom = cell_box
    stack_height = STAT_ICON_SIZE_PX + STAT_ICON_TO_VALUE_GAP_PX + STAT_VALUE_MAX_HEIGHT_PX
    stack_top_y = cell_top + max(STAT_STACK_MIN_TOP_INSET_PX, (cell_bottom - cell_top - stack_height) // 2)

    icon_center_y = stack_top_y + STAT_ICON_SIZE_PX // 2
    _draw_stat_icon(canvas, pen, substat.label, slot_center_x, icon_center_y, STAT_ICON_SIZE_PX, platform)

    value_text = format_substat_value(substat.value)
    value_font = draw.fit_font(
        pen, value_text,
        max_w=int(slot_width - STAT_VALUE_HORIZONTAL_PADDING_PX),
        max_h=STAT_VALUE_MAX_HEIGHT_PX,
        start=STAT_VALUE_FONT_START_PX,
        minimum=STAT_VALUE_FONT_MIN_PX,
        bold=True,
    )
    value_top_y = stack_top_y + STAT_ICON_SIZE_PX + STAT_ICON_TO_VALUE_GAP_PX
    draw.draw_text(pen, (slot_center_x, value_top_y), value_text, value_font, TEXT_PRIMARY_RGB, anchor="mt")


def _draw_stat_icon(
    canvas: Image.Image,
    pen: ImageDraw.ImageDraw,
    substat_label: str,
    center_x: int,
    center_y: int,
    icon_size_px: int,
    platform: str,
) -> None:
    """Draw one stat icon. Three rendering modes, tried in priority order:

    1) RA pill badge — label key matches a known RetroAchievements badge.
    2) Bundled PNG asset — e.g. assets/icons/psn/platinum.png.
    3) Procedural fallback — star (mastery labels) or trophy.
    """
    label_key = (substat_label or "").lower()

    badge_color = _RA_BADGE_FILL_COLORS.get(label_key)
    if badge_color is not None:
        badge_text = _RA_LABEL_DISPLAY_TEXT.get(label_key, substat_label.upper())
        badge_height = int(icon_size_px * RA_PILL_BADGE_HEIGHT_SCALE)
        draw.draw_label_badge(pen, center_x, center_y, badge_height, badge_text, fill_color=badge_color)
        return

    asset_icon = draw.load_stat_icon(platform, label_key)
    if asset_icon is not None:
        draw.paste_centered_icon(canvas, asset_icon, center_x, center_y, icon_size_px)
        return

    if label_key in _STAR_ICON_LABEL_KEYS:
        draw.draw_star(pen, center_x, center_y, icon_size_px, filled=True)
        return
    fallback_color = _PROCEDURAL_ICON_COLORS.get(label_key, STAT_ICON_DEFAULT_COLOR)
    draw.draw_trophy(pen, center_x, center_y, icon_size_px, fallback_color)


# ---------------------------------------------------------------------------
# Row 4 helpers — RA pill layout with equal visible gaps
# ---------------------------------------------------------------------------

def _compute_ra_pill_centers(
    pen: ImageDraw.ImageDraw,
    stats_left: int,
    stats_right: int,
    substats: list[SubStat],
) -> list[int] | None:
    """x-centers that give RA_PILL_BADGE_GAP_PX between adjacent pills.

    Returns None if any substat is not a known RA pill, so the caller falls
    back to evenly-spaced slot centers. Pills are horizontally centered as
    a group within the stats box.
    """
    badge_height = int(STAT_ICON_SIZE_PX * RA_PILL_BADGE_HEIGHT_SCALE)
    pill_widths: list[int] = []
    for substat in substats:
        label_key = (substat.label or "").lower()
        if label_key not in _RA_BADGE_FILL_COLORS:
            return None
        display_text = _RA_LABEL_DISPLAY_TEXT.get(label_key, substat.label.upper())
        pill_widths.append(_measure_pill_badge_width(pen, display_text, badge_height))

    total_group_width = sum(pill_widths) + RA_PILL_BADGE_GAP_PX * (len(pill_widths) - 1)
    cursor_x = (stats_left + stats_right) // 2 - total_group_width // 2
    centers: list[int] = []
    for width in pill_widths:
        centers.append(cursor_x + width // 2)
        cursor_x += width + RA_PILL_BADGE_GAP_PX
    return centers


def _measure_pill_badge_width(pen: ImageDraw.ImageDraw, display_text: str, height_px: int) -> int:
    """Pill-badge width without drawing it — mirrors draw.draw_label_badge."""
    probe_font_size = max(10, int(height_px * draw.PILL_BADGE_PROBE_FONT_SIZE_RATIO))
    probe_font = draw.get_font(probe_font_size, bold=True)
    measured_text_width, _ = draw.text_size(pen, display_text, probe_font)
    return max(
        height_px + draw.PILL_BADGE_MIN_WIDTH_OVER_HEIGHT_PX,
        measured_text_width + int(height_px * draw.PILL_BADGE_HORIZONTAL_PAD_RATIO),
    )


# ---------------------------------------------------------------------------
# Row 5: footer (platform icon + platform name)
# ---------------------------------------------------------------------------

def _draw_footer_row(
    canvas: Image.Image,
    pen: ImageDraw.ImageDraw,
    regions,
    theme,
) -> None:
    """Platform icon on the left, platform name centered to its right.

    Uses the user-supplied PNG at assets/icons/<platform>.png when present,
    otherwise falls back to a procedural glyph. The icon's rendered width
    determines where the label text area begins.
    """
    footer_left, footer_top, footer_right, footer_bottom = regions.footer
    footer_center_y = (footer_top + footer_bottom) // 2
    icon_height = (footer_bottom - footer_top) - FOOTER_ICON_VERTICAL_INSET_PX
    icon_left = footer_left + FOOTER_HORIZONTAL_PADDING_PX
    icon_top = footer_center_y - icon_height // 2
    icon_bottom = footer_center_y + icon_height // 2

    platform_png_icon = draw.load_platform_icon(theme.key)
    if platform_png_icon is not None:
        icon_box = (icon_left, icon_top,
                    icon_left + int(icon_height * FOOTER_ICON_WIDTH_TO_HEIGHT_RATIO), icon_bottom)
        rendered_bbox = draw.paste_platform_icon(canvas, platform_png_icon, icon_box)
        label_area_left_x = rendered_bbox[2] + FOOTER_ICON_TO_LABEL_GAP_PX
    else:
        glyph_box = (icon_left, icon_top, icon_left + icon_height, icon_bottom)
        draw.draw_platform_icon(pen, theme.key, glyph_box, theme.accent)
        label_area_left_x = glyph_box[2] + FOOTER_PROCEDURAL_ICON_TO_LABEL_GAP_PX

    label_area_right_x = footer_right - FOOTER_HORIZONTAL_PADDING_PX
    label_font = draw.get_font(FOOTER_LABEL_FONT_PX, bold=True)
    label_center_x = (label_area_left_x + label_area_right_x) // 2
    draw.draw_text(pen, (label_center_x, footer_center_y), theme.footer_label, label_font, TEXT_PRIMARY_RGB, anchor="mm")


# ---------------------------------------------------------------------------
# Data helpers
# ---------------------------------------------------------------------------

def _load_avatar_image(cache_dir: Path, platform: str) -> Image.Image | None:
    """Return the cached avatar image for `platform`, or None on failure."""
    avatar_path = find_cached_avatar(cache_dir, platform)
    if not avatar_path:
        return None
    try:
        return Image.open(avatar_path)
    except OSError as error:
        log.warning("avatar: cannot open %s: %s", avatar_path, error)
        return None
