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

CANVAS_W = 1500
CANVAS_H = 450

OUTER_MARGIN = 14
PANEL_GAP = 14
PANEL_W = (CANVAS_W - 2 * OUTER_MARGIN - 2 * PANEL_GAP) // 3
PANEL_H = CANVAS_H - 2 * OUTER_MARGIN
PANEL_RADIUS = 14
PANEL_BORDER_W = 3  # accent-color outline around each whole panel

FOOTER_H = 48
FOOTER_DIVIDER_W = 1

# colours
BG_TOP = (12, 26, 52)
BG_BOTTOM = (4, 10, 22)
PANEL_FILL = (18, 28, 46)
PANEL_FILL_INNER = (24, 34, 54)  # faint lift so the headline block pops
TEXT_PRIMARY = (244, 248, 255)
TEXT_SECONDARY = (178, 190, 210)
TEXT_MUTED = (130, 144, 166)


@dataclass(frozen=True)
class Theme:
    key: str
    display_name: str        # subtitle under username (plain text run)
    display_prefix: str = ""  # optional colored prefix drawn before display_name
    accent: tuple[int, int, int] = (255, 255, 255)
    accent_deep: tuple[int, int, int] = (0, 0, 0)
    avatar_ring: tuple[int, int, int] = (255, 255, 255)
    footer_label: str = ""
    footer_glyph: str = ""
    label_color: tuple[int, int, int] = (255, 255, 255)


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


def panel_box(index: int) -> tuple[int, int, int, int]:
    """Return the bounding box for the nth panel (0-based, left to right)."""
    x0 = OUTER_MARGIN + index * (PANEL_W + PANEL_GAP)
    y0 = OUTER_MARGIN
    return (x0, y0, x0 + PANEL_W, y0 + PANEL_H)


@dataclass(frozen=True)
class PanelRegions:
    panel: tuple[int, int, int, int]
    body: tuple[int, int, int, int]
    header: tuple[int, int, int, int]     # avatar + name block
    avatar: tuple[int, int, int, int]
    name_block: tuple[int, int, int, int]
    label: tuple[int, int, int, int]
    headline_block: tuple[int, int, int, int]  # label+headline lifted panel
    headline: tuple[int, int, int, int]
    stats: tuple[int, int, int, int]
    footer_divider: tuple[int, int, int, int]  # thin accent line above footer
    footer: tuple[int, int, int, int]


def panel_regions(index: int) -> PanelRegions:
    x0, y0, x1, y1 = panel_box(index)
    footer = (x0, y1 - FOOTER_H, x1, y1)
    footer_divider = (x0 + 10, footer[1] - 1, x1 - 10, footer[1])
    body = (x0, y0, x1, footer[1])

    pad_x = 18
    inner_l = body[0] + pad_x
    inner_r = body[2] - pad_x

    # header: avatar + name block
    header_top = body[1] + 14
    avatar_size = 85  # +10% over prior 77
    header = (inner_l, header_top, inner_r, header_top + avatar_size)
    avatar = (inner_l, header_top, inner_l + avatar_size, header_top + avatar_size)
    name_block = (avatar[2] + 12, header_top - 2, inner_r, header[3] + 2)

    # headline block (label + big value lifted background)
    block_top = header[3] + 10
    block_h = 96
    headline_block = (inner_l - 2, block_top, inner_r + 2, block_top + block_h)
    label = (headline_block[0], block_top + 4, headline_block[2], block_top + 30)
    headline = (headline_block[0], label[3], headline_block[2], block_top + block_h - 4)

    # stats row fills the remaining space down to the footer divider
    stats_top = headline_block[3] + 10
    stats = (inner_l, stats_top, inner_r, body[3] - 10)

    return PanelRegions(
        panel=(x0, y0, x1, y1),
        body=body,
        header=header,
        avatar=avatar,
        name_block=name_block,
        label=label,
        headline_block=headline_block,
        headline=headline,
        stats=stats,
        footer_divider=footer_divider,
        footer=footer,
    )


PLATFORM_ORDER = ("xbox", "psn", "retroachievements")
