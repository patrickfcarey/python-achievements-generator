"""Banner geometry and per-platform theme definitions.

Bounding boxes are (x0, y0, x1, y1). Everything the renderer draws is derived
from the constants here so tweaking dimensions only touches one file.

The banner matches the provided example.png:
- three panels side by side
- each panel has a thin colored accent bar at the very top and a colored
  footer bar at the bottom containing the platform name + glyph
- the body flows avatar+name header -> label -> big headline -> stat icons
"""
from __future__ import annotations

from dataclasses import dataclass

# ---------------------------------------------------------------------------
# Canvas dimensions
# ---------------------------------------------------------------------------

CANVAS_WIDTH_PX = 1500
CANVAS_HEIGHT_PX = 450

# ---------------------------------------------------------------------------
# Panel grid geometry
# ---------------------------------------------------------------------------

PANEL_OUTER_MARGIN_PX = 14
PANEL_GAP_PX = 14
PANEL_WIDTH_PX = (CANVAS_WIDTH_PX - 2 * PANEL_OUTER_MARGIN_PX - 2 * PANEL_GAP_PX) // 3
PANEL_HEIGHT_PX = CANVAS_HEIGHT_PX - 2 * PANEL_OUTER_MARGIN_PX
PANEL_CORNER_RADIUS_PX = 14
PANEL_BORDER_WIDTH_PX = 3  # accent-color outline around each whole panel

# ---------------------------------------------------------------------------
# Footer strip
# ---------------------------------------------------------------------------

FOOTER_HEIGHT_PX = 48
FOOTER_DIVIDER_THICKNESS_PX = 1
FOOTER_DIVIDER_HORIZONTAL_INSET_PX = 10  # divider is inset from panel edges

# ---------------------------------------------------------------------------
# Panel interior layout
# ---------------------------------------------------------------------------

PANEL_INTERIOR_PAD_X_PX = 18           # left/right padding inside each panel body
PANEL_HEADER_TOP_OFFSET_PX = 14        # gap from top of panel body to header row
AVATAR_DIAMETER_PX = 85
AVATAR_TO_NAME_GAP_PX = 12             # horizontal gap between avatar right edge and name block

HEADLINE_BLOCK_TOP_MARGIN_PX = 10      # gap between header row bottom and headline block top
HEADLINE_BLOCK_HEIGHT_PX = 96
HEADLINE_BLOCK_HORIZONTAL_BLEED_PX = 2  # lifted block extends 2px beyond panel interior padding
HEADLINE_BLOCK_CORNER_RADIUS_PX = 12

LABEL_STRIP_TOP_PADDING_PX = 4         # top padding inside the headline block for the label text
LABEL_STRIP_HEIGHT_PX = 26             # vertical space allocated to the label

STATS_ROW_TOP_MARGIN_PX = 10           # gap between headline block bottom and stats row top
STATS_ROW_BOTTOM_INSET_PX = 10         # gap between stats row bottom and footer divider

# ---------------------------------------------------------------------------
# Colours
# ---------------------------------------------------------------------------

BACKGROUND_GRADIENT_TOP_RGB = (12, 26, 52)
BACKGROUND_GRADIENT_BOTTOM_RGB = (4, 10, 22)
PANEL_FILL_RGB = (18, 28, 46)
PANEL_FILL_INNER_RGB = (24, 34, 54)    # faint lift so the headline block pops
TEXT_PRIMARY_RGB = (244, 248, 255)
TEXT_SECONDARY_RGB = (178, 190, 210)
TEXT_MUTED_RGB = (130, 144, 166)

# ---------------------------------------------------------------------------
# Backward-compatible aliases (remove once all callers are updated)
# ---------------------------------------------------------------------------

CANVAS_W = CANVAS_WIDTH_PX
CANVAS_H = CANVAS_HEIGHT_PX
OUTER_MARGIN = PANEL_OUTER_MARGIN_PX
PANEL_GAP = PANEL_GAP_PX
PANEL_W = PANEL_WIDTH_PX
PANEL_H = PANEL_HEIGHT_PX
PANEL_RADIUS = PANEL_CORNER_RADIUS_PX
PANEL_BORDER_W = PANEL_BORDER_WIDTH_PX
FOOTER_H = FOOTER_HEIGHT_PX
FOOTER_DIVIDER_W = FOOTER_DIVIDER_THICKNESS_PX
BG_TOP = BACKGROUND_GRADIENT_TOP_RGB
BG_BOTTOM = BACKGROUND_GRADIENT_BOTTOM_RGB
PANEL_FILL = PANEL_FILL_RGB
PANEL_FILL_INNER = PANEL_FILL_INNER_RGB
TEXT_PRIMARY = TEXT_PRIMARY_RGB
TEXT_SECONDARY = TEXT_SECONDARY_RGB
TEXT_MUTED = TEXT_MUTED_RGB


# ---------------------------------------------------------------------------
# Per-platform themes
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Theme:
    key: str
    display_name: str          # subtitle under username (plain text run)
    display_prefix: str = ""   # optional colored prefix drawn before display_name
    accent: tuple[int, int, int] = (255, 255, 255)
    accent_deep: tuple[int, int, int] = (0, 0, 0)
    avatar_ring: tuple[int, int, int] = (255, 255, 255)
    footer_label: str = ""
    footer_glyph: str = ""
    label_color: tuple[int, int, int] = (255, 255, 255)
    # Per-platform pixel nudges applied by the header row renderer.
    # avatar_offset shifts the avatar around its own center so resizing
    # doesn't drag the image off-axis. (delta_x, delta_y) in pixels.
    avatar_offset: tuple[int, int] = (-14, -15)
    # name_offset_x shifts the username + subtitle text block rightward.
    name_offset_x: int = 0


THEMES: dict[str, Theme] = {
    "xbox": Theme(
        key="xbox",
        display_name="XBOX LIVE",
        accent=(28, 150, 36),
        accent_deep=(16, 86, 22),
        avatar_ring=(40, 190, 60),
        footer_label="XBOX",
        footer_glyph="X",
        label_color=(190, 230, 195),
    ),
    "psn": Theme(
        key="psn",
        display_name="PlayStation Network",
        accent=(40, 120, 220),
        accent_deep=(16, 58, 132),
        avatar_ring=(72, 148, 232),
        footer_label="PlayStation",
        footer_glyph="PS",
        label_color=(185, 210, 245),
        avatar_offset=(0, -15),
        name_offset_x=15,
    ),
    "retroachievements": Theme(
        key="retroachievements",
        display_name="RetroAchievements",
        display_prefix="RA",
        accent=(210, 174, 46),
        accent_deep=(120, 94, 20),
        avatar_ring=(232, 196, 56),
        footer_label="RetroAchievements",
        footer_glyph="RA",
        label_color=(240, 216, 130),
    ),
}


# ---------------------------------------------------------------------------
# Geometry helpers
# ---------------------------------------------------------------------------

def panel_box(panel_index: int) -> tuple[int, int, int, int]:
    """Return the bounding box (left, top, right, bottom) for the nth panel (0-based)."""
    panel_left = PANEL_OUTER_MARGIN_PX + panel_index * (PANEL_WIDTH_PX + PANEL_GAP_PX)
    panel_top = PANEL_OUTER_MARGIN_PX
    return (panel_left, panel_top, panel_left + PANEL_WIDTH_PX, panel_top + PANEL_HEIGHT_PX)


@dataclass(frozen=True)
class PanelRegions:
    """All sub-regions of one panel, precomputed for the renderer.

    Every value is a (left, top, right, bottom) bounding box. The renderer
    reads these rather than recomputing geometry inline, so all layout
    decisions stay in this module.
    """
    panel: tuple[int, int, int, int]
    body: tuple[int, int, int, int]
    header: tuple[int, int, int, int]          # avatar + name block combined
    avatar: tuple[int, int, int, int]
    name_block: tuple[int, int, int, int]
    label: tuple[int, int, int, int]
    headline_block: tuple[int, int, int, int]  # lifted background behind label + headline
    headline: tuple[int, int, int, int]
    stats: tuple[int, int, int, int]
    footer_divider: tuple[int, int, int, int]  # thin accent line above footer
    footer: tuple[int, int, int, int]


def panel_regions(panel_index: int) -> PanelRegions:
    """Compute all sub-region bounding boxes for the panel at the given index."""
    panel_left, panel_top, panel_right, panel_bottom = panel_box(panel_index)

    footer_top = panel_bottom - FOOTER_HEIGHT_PX
    footer_box = (panel_left, footer_top, panel_right, panel_bottom)
    footer_divider_box = (
        panel_left + FOOTER_DIVIDER_HORIZONTAL_INSET_PX,
        footer_top - FOOTER_DIVIDER_THICKNESS_PX,
        panel_right - FOOTER_DIVIDER_HORIZONTAL_INSET_PX,
        footer_top,
    )
    body_box = (panel_left, panel_top, panel_right, footer_top)

    interior_left = body_box[0] + PANEL_INTERIOR_PAD_X_PX
    interior_right = body_box[2] - PANEL_INTERIOR_PAD_X_PX

    # Header row: avatar circle on the left, name + subtitle on the right
    header_top = body_box[1] + PANEL_HEADER_TOP_OFFSET_PX
    avatar_bottom = header_top + AVATAR_DIAMETER_PX
    header_box = (interior_left, header_top, interior_right, avatar_bottom)
    avatar_box = (interior_left, header_top, interior_left + AVATAR_DIAMETER_PX, avatar_bottom)
    name_block_box = (
        avatar_box[2] + AVATAR_TO_NAME_GAP_PX,
        header_top - 2,
        interior_right,
        avatar_bottom + 2,
    )

    # Headline block: lifted background containing the label strip + headline value
    headline_block_top = header_box[3] + HEADLINE_BLOCK_TOP_MARGIN_PX
    headline_block_box = (
        interior_left - HEADLINE_BLOCK_HORIZONTAL_BLEED_PX,
        headline_block_top,
        interior_right + HEADLINE_BLOCK_HORIZONTAL_BLEED_PX,
        headline_block_top + HEADLINE_BLOCK_HEIGHT_PX,
    )
    label_box = (
        headline_block_box[0],
        headline_block_top + LABEL_STRIP_TOP_PADDING_PX,
        headline_block_box[2],
        headline_block_top + LABEL_STRIP_TOP_PADDING_PX + LABEL_STRIP_HEIGHT_PX,
    )
    headline_box = (
        headline_block_box[0],
        label_box[3],
        headline_block_box[2],
        headline_block_top + HEADLINE_BLOCK_HEIGHT_PX - LABEL_STRIP_TOP_PADDING_PX,
    )

    # Stats row: fills remaining vertical space between headline block and footer divider
    stats_top = headline_block_box[3] + STATS_ROW_TOP_MARGIN_PX
    stats_box = (
        interior_left,
        stats_top,
        interior_right,
        body_box[3] - STATS_ROW_BOTTOM_INSET_PX,
    )

    return PanelRegions(
        panel=panel_box(panel_index),
        body=body_box,
        header=header_box,
        avatar=avatar_box,
        name_block=name_block_box,
        label=label_box,
        headline_block=headline_block_box,
        headline=headline_box,
        stats=stats_box,
        footer_divider=footer_divider_box,
        footer=footer_box,
    )


PLATFORM_ORDER = ("xbox", "psn", "retroachievements")

# ---------------------------------------------------------------------------
# Bounding-box utilities
# ---------------------------------------------------------------------------

Box = tuple[int, int, int, int]


def offset_box(box: Box, dx: int, dy: int) -> Box:
    """Return `box` shifted by (dx, dy) without changing its size."""
    x0, y0, x1, y1 = box
    return (x0 + dx, y0 + dy, x1 + dx, y1 + dy)


def split_box_horizontally(box: Box) -> tuple[Box, Box]:
    """Split `box` at its horizontal midpoint into (left_half, right_half)."""
    x0, y0, x1, y1 = box
    mid = (x0 + x1) // 2
    return (x0, y0, mid, y1), (mid, y0, x1, y1)
