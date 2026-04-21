"""Low-level drawing primitives: fonts, text, icons, stars, background.

All geometry is expressed in pixels. Functions here have no knowledge of
platform themes or panel layout — they operate only on coordinates, sizes,
and colors passed in by the caller. Higher-level composition lives in
compose.py.

Drawing routines for platform logos and trophy icons use inline proportional
ratios (e.g. ``cx - int(r * 0.35)``). These are kept inline rather than
promoted to module constants because they describe a single glyph's geometry
— extracting them would scatter what should be read as one specification.
"""
from __future__ import annotations

import math
import os
from functools import lru_cache
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ASSETS_FONTS = Path(__file__).resolve().parents[2] / "assets" / "fonts"
ASSETS_ICONS = Path(__file__).resolve().parents[2] / "assets" / "icons"

# ---------------------------------------------------------------------------
# Font loading
# ---------------------------------------------------------------------------

_FONT_SEARCH_PATHS = [
    ASSETS_FONTS / "DejaVuSans-Bold.ttf",
    ASSETS_FONTS / "DejaVuSans.ttf",
    Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"),
    Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
    Path("/System/Library/Fonts/Helvetica.ttc"),
    Path("/Library/Fonts/Arial Bold.ttf"),
    Path("/mnt/c/Windows/Fonts/arialbd.ttf"),
    Path("/mnt/c/Windows/Fonts/arial.ttf"),
    Path("C:/Windows/Fonts/arialbd.ttf"),
    Path("C:/Windows/Fonts/arial.ttf"),
]


@lru_cache(maxsize=64)
def get_font(size_px: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    """Return the best available font at `size_px`.

    Searches bundled assets first, then common system locations.
    Bold fonts are preferred when ``bold=True``. Falls back to Pillow's
    built-in bitmap font if no TTF is found.
    """
    candidates = list(_FONT_SEARCH_PATHS)
    if bold:
        bold_candidates = [
            path for path in candidates
            if "bold" in str(path).lower() or path.name.lower().endswith("bd.ttf")
        ]
        non_bold_candidates = [path for path in candidates if path not in bold_candidates]
        candidates = bold_candidates + non_bold_candidates

    for font_path in candidates:
        try:
            if os.path.exists(font_path):
                return ImageFont.truetype(str(font_path), size_px)
        except OSError:
            continue
    return ImageFont.load_default()


# ---------------------------------------------------------------------------
# Text helpers
# ---------------------------------------------------------------------------

TEXT_SHADOW_OFFSET_PX = 2
TEXT_SHADOW_RGBA = (0, 0, 0, 170)


def text_size(pen: ImageDraw.ImageDraw, text: str, font) -> tuple[int, int]:
    """Return the (width, height) in pixels of `text` rendered with `font`."""
    bounding_box = pen.textbbox((0, 0), text, font=font)
    text_width = bounding_box[2] - bounding_box[0]
    text_height = bounding_box[3] - bounding_box[1]
    return text_width, text_height


def draw_text(
    pen: ImageDraw.ImageDraw,
    position: tuple[int, int],
    text: str,
    font,
    fill_color,
    anchor: str = "la",
    shadow: bool = False,
) -> None:
    """Draw `text` at `position`. Optionally render a dark drop-shadow first."""
    if shadow:
        shadow_position = (position[0] + TEXT_SHADOW_OFFSET_PX, position[1] + TEXT_SHADOW_OFFSET_PX)
        pen.text(shadow_position, text, font=font, fill=TEXT_SHADOW_RGBA, anchor=anchor)
    pen.text(position, text, font=font, fill=fill_color, anchor=anchor)


def fit_font(
    pen: ImageDraw.ImageDraw,
    text: str,
    max_w: int,
    max_h: int,
    start: int = 64,
    minimum: int = 14,
    bold: bool = True,
) -> ImageFont.FreeTypeFont:
    """Return the largest font that fits `text` within `max_w` × `max_h` pixels.

    Starts at `start` pt and steps down by 2 until the text fits or `minimum`
    is reached, at which point `minimum` is returned unconditionally.
    """
    current_size = start
    while current_size > minimum:
        candidate_font = get_font(current_size, bold=bold)
        rendered_width, rendered_height = text_size(pen, text, candidate_font)
        if rendered_width <= max_w and rendered_height <= max_h:
            return candidate_font
        current_size -= 2
    return get_font(minimum, bold=bold)


# ---------------------------------------------------------------------------
# Shape primitives
# ---------------------------------------------------------------------------

def rounded_rect(
    pen: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    radius: int,
    fill=None,
    outline=None,
    width: int = 1,
) -> None:
    """Draw a rounded rectangle. Thin wrapper around Pillow's rounded_rectangle."""
    pen.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


# ---------------------------------------------------------------------------
# Background
# ---------------------------------------------------------------------------

GLOW_BLUR_RADIUS_PX = 60
GLOW_ALPHA = 70
GLOW_RADIUS_TO_SLOT_RATIO = 0.55   # radial glow radius as a fraction of slot width


def build_background(
    canvas_size: tuple[int, int],
    gradient_top_rgb: tuple[int, int, int],
    gradient_bottom_rgb: tuple[int, int, int],
    accent_colors: list[tuple[int, int, int]] | None = None,
) -> Image.Image:
    """Build the banner backdrop: vertical gradient with soft radial glows per panel."""
    canvas_width, canvas_height = canvas_size
    background = _vertical_gradient(canvas_size, gradient_top_rgb, gradient_bottom_rgb).convert("RGBA")

    if accent_colors:
        glow_layer = Image.new("RGBA", canvas_size, (0, 0, 0, 0))
        glow_pen = ImageDraw.Draw(glow_layer)
        slot_width = canvas_width / len(accent_colors)
        for slot_index, accent_color in enumerate(accent_colors):
            glow_center_x = int(slot_width * (slot_index + 0.5))
            glow_center_y = canvas_height // 2
            glow_radius = int(slot_width * GLOW_RADIUS_TO_SLOT_RATIO)
            _radial_glow_blob(glow_pen, glow_center_x, glow_center_y, glow_radius, accent_color)
        glow_layer = glow_layer.filter(ImageFilter.GaussianBlur(radius=GLOW_BLUR_RADIUS_PX))
        background = Image.alpha_composite(background, glow_layer)

    return background


def _vertical_gradient(
    canvas_size: tuple[int, int],
    top_rgb: tuple[int, int, int],
    bottom_rgb: tuple[int, int, int],
) -> Image.Image:
    """Render a 1×H gradient strip and tile it to the full canvas width."""
    canvas_width, canvas_height = canvas_size
    gradient_strip = Image.new("RGB", (1, canvas_height))
    pixel_buffer = gradient_strip.load()
    for y in range(canvas_height):
        blend_factor = y / max(canvas_height - 1, 1)
        pixel_buffer[0, y] = (
            int(top_rgb[0] + (bottom_rgb[0] - top_rgb[0]) * blend_factor),
            int(top_rgb[1] + (bottom_rgb[1] - top_rgb[1]) * blend_factor),
            int(top_rgb[2] + (bottom_rgb[2] - top_rgb[2]) * blend_factor),
        )
    return gradient_strip.resize((canvas_width, canvas_height))


def _radial_glow_blob(
    pen: ImageDraw.ImageDraw,
    center_x: int,
    center_y: int,
    radius_px: int,
    color_rgb: tuple[int, int, int],
) -> None:
    """Draw a filled ellipse that, after Gaussian blur, becomes a soft radial glow."""
    red, green, blue = color_rgb
    pen.ellipse(
        (center_x - radius_px, center_y - radius_px,
         center_x + radius_px, center_y + radius_px),
        fill=(red, green, blue, GLOW_ALPHA),
    )


# ---------------------------------------------------------------------------
# Avatar
# ---------------------------------------------------------------------------

AVATAR_RING_DEFAULT_WIDTH_PX = 4
PLACEHOLDER_AVATAR_BACKGROUND_RGB = (58, 70, 92)
PLACEHOLDER_AVATAR_FIGURE_RGB = (190, 200, 220)


def paste_circle_avatar(
    canvas: Image.Image,
    avatar_image: Image.Image,
    destination_box: tuple[int, int, int, int],
    ring_color: tuple[int, int, int],
    ring_width_px: int = AVATAR_RING_DEFAULT_WIDTH_PX,
) -> None:
    """Paste `avatar_image` as a circle with a colored ring into `canvas`.

    The avatar is resized to fill the destination box, clipped to a circle
    mask, and then an outline ring is drawn on top.
    """
    box_left, box_top, box_right, box_bottom = destination_box
    avatar_size_px = min(box_right - box_left, box_bottom - box_top)
    resized_avatar = avatar_image.convert("RGBA").resize(
        (avatar_size_px, avatar_size_px), Image.LANCZOS
    )
    circle_mask = Image.new("L", (avatar_size_px, avatar_size_px), 0)
    ImageDraw.Draw(circle_mask).ellipse((0, 0, avatar_size_px, avatar_size_px), fill=255)
    canvas.paste(resized_avatar, (box_left, box_top), circle_mask)
    ImageDraw.Draw(canvas).ellipse(
        (box_left, box_top, box_left + avatar_size_px, box_top + avatar_size_px),
        outline=ring_color,
        width=ring_width_px,
    )


def draw_placeholder_avatar(
    pen: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    ring_color: tuple[int, int, int],
    background_fill: tuple[int, int, int] = PLACEHOLDER_AVATAR_BACKGROUND_RGB,
) -> None:
    """Draw a generic silhouette avatar when no real image is available.

    Renders a filled circle background, a circular head, and a shoulder arc
    to suggest a human figure without requiring an actual photo.
    """
    pen.ellipse(box, fill=background_fill, outline=ring_color, width=AVATAR_RING_DEFAULT_WIDTH_PX)
    box_left, box_top, box_right, box_bottom = box
    center_x = (box_left + box_right) // 2
    center_y = (box_top + box_bottom) // 2
    avatar_radius = (box_right - box_left) // 2

    # Head: a smaller circle positioned slightly above center
    head_radius = int(avatar_radius * 0.35)
    head_center_y = center_y - int(avatar_radius * 0.1)
    pen.ellipse(
        (center_x - head_radius, head_center_y - head_radius,
         center_x + head_radius, head_center_y + head_radius),
        fill=PLACEHOLDER_AVATAR_FIGURE_RGB,
    )

    # Shoulders: a chord arc below the head
    shoulder_top_y = center_y + int(avatar_radius * 0.28)
    shoulder_arc_height = int(avatar_radius * 0.5)
    pen.chord(
        (center_x - int(avatar_radius * 0.75), shoulder_top_y,
         center_x + int(avatar_radius * 0.75), shoulder_top_y + shoulder_arc_height * 2),
        start=180,
        end=360,
        fill=PLACEHOLDER_AVATAR_FIGURE_RGB,
    )


# ---------------------------------------------------------------------------
# Icons — procedural (trophy, star)
# ---------------------------------------------------------------------------

def draw_trophy(
    pen: ImageDraw.ImageDraw,
    center_x: int,
    center_y: int,
    size_px: int,
    color: tuple[int, int, int],
) -> None:
    """Draw a cup-style trophy that reads clearly even at small sizes."""
    half_size = size_px // 2

    # Cup body: a tapered trapezoid
    cup_top_y = center_y - half_size + 2
    cup_bottom_y = center_y + int(half_size * 0.35)
    pen.polygon(
        [
            (center_x - half_size, cup_top_y),
            (center_x + half_size, cup_top_y),
            (center_x + int(half_size * 0.7), cup_bottom_y),
            (center_x - int(half_size * 0.7), cup_bottom_y),
        ],
        fill=color,
    )

    # Rim: a small ellipse cap at the top of the cup
    pen.ellipse((center_x - half_size, cup_top_y - 3, center_x + half_size, cup_top_y + 3), fill=color)

    # Handles: arcs on each side
    handle_stroke_width = max(2, size_px // 10)
    handle_top_y = cup_top_y + 2
    handle_bottom_y = cup_bottom_y - 2
    pen.arc(
        (center_x - half_size - int(half_size * 0.5), handle_top_y,
         center_x - half_size + 2, handle_bottom_y),
        start=90, end=270, fill=color, width=handle_stroke_width,
    )
    pen.arc(
        (center_x + half_size - 2, handle_top_y,
         center_x + half_size + int(half_size * 0.5), handle_bottom_y),
        start=-90, end=90, fill=color, width=handle_stroke_width,
    )

    # Stem: a vertical rectangle connecting cup to base
    stem_half_width = max(3, size_px // 7)
    stem_bottom_y = center_y + int(half_size * 0.75)
    pen.rectangle(
        (center_x - stem_half_width, cup_bottom_y,
         center_x + stem_half_width, stem_bottom_y),
        fill=color,
    )

    # Base: a wide flat rectangle
    base_half_width = int(half_size * 0.9)
    base_height = max(3, size_px // 10)
    pen.rectangle(
        (center_x - base_half_width, stem_bottom_y,
         center_x + base_half_width, stem_bottom_y + base_height),
        fill=color,
    )


def draw_star(
    pen: ImageDraw.ImageDraw,
    center_x: int,
    center_y: int,
    size_px: int,
    filled: bool = True,
    color: tuple[int, int, int] = (232, 196, 56),
    outline_only: bool = False,
) -> None:
    """Draw a 5-pointed star centered at (center_x, center_y)."""
    star_points = []
    for vertex_index in range(10):
        angle_radians = -math.pi / 2 + vertex_index * math.pi / 5
        # Outer points (even indices) use full radius; inner points use a smaller inset radius
        vertex_radius = size_px / 2 if vertex_index % 2 == 0 else size_px / 4.5
        star_points.append((
            center_x + vertex_radius * math.cos(angle_radians),
            center_y + vertex_radius * math.sin(angle_radians),
        ))
    if filled and not outline_only:
        pen.polygon(star_points, fill=color)
    else:
        pen.polygon(star_points, outline=color, width=2)


def draw_stars_row(
    pen: ImageDraw.ImageDraw,
    left_x: int,
    top_y: int,
    total_stars: int,
    filled_count: int,
    star_size_px: int = 20,
    star_gap_px: int = 4,
    color: tuple[int, int, int] = (232, 196, 56),
) -> None:
    """Draw a horizontal row of `total_stars` stars, `filled_count` of which are filled."""
    filled_count = max(0, min(filled_count, total_stars))
    for star_index in range(total_stars):
        star_center_x = left_x + star_index * (star_size_px + star_gap_px) + star_size_px // 2
        draw_star(
            pen, star_center_x, top_y + star_size_px // 2, star_size_px,
            filled=star_index < filled_count, color=color,
        )


# ---------------------------------------------------------------------------
# Icons — platform logos (procedural fallbacks)
# ---------------------------------------------------------------------------

def draw_footer_glyph(
    pen: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    glyph_text: str,
    foreground_color,
    background_circle_color,
) -> None:
    """Draw a small round badge containing the platform's short glyph (e.g. "X", "PS", "RA")."""
    box_left, box_top, box_right, box_bottom = box
    center_x = (box_left + box_right) // 2
    center_y = (box_top + box_bottom) // 2
    circle_radius = (box_bottom - box_top) // 2 - 2
    pen.ellipse(
        (center_x - circle_radius, center_y - circle_radius,
         center_x + circle_radius, center_y + circle_radius),
        fill=background_circle_color,
    )
    glyph_max_dimension = int(circle_radius * 1.4)
    glyph_font = fit_font(
        pen, glyph_text,
        max_w=glyph_max_dimension,
        max_h=glyph_max_dimension,
        start=glyph_max_dimension,
        bold=True,
    )
    draw_text(pen, (center_x, center_y), glyph_text, glyph_font, foreground_color, anchor="mm")


def draw_xbox_logo(
    pen: ImageDraw.ImageDraw,
    center_x: int,
    center_y: int,
    size_px: int,
    color: tuple[int, int, int] = (255, 255, 255),
    background_color: tuple[int, int, int] = (16, 124, 16),
) -> None:
    """Xbox logo: green sphere with a stylized white 'X' formed by two thick diagonals."""
    half_size = size_px // 2
    pen.ellipse(
        (center_x - half_size, center_y - half_size,
         center_x + half_size, center_y + half_size),
        fill=background_color,
    )
    stroke_width = max(3, size_px // 7)
    diagonal_reach = int(half_size * 0.58)
    pen.line(
        (center_x - diagonal_reach, center_y - diagonal_reach,
         center_x + diagonal_reach, center_y + diagonal_reach),
        fill=color, width=stroke_width,
    )
    pen.line(
        (center_x - diagonal_reach, center_y + diagonal_reach,
         center_x + diagonal_reach, center_y - diagonal_reach),
        fill=color, width=stroke_width,
    )


def draw_playstation_symbols(
    pen: ImageDraw.ImageDraw,
    center_x: int,
    center_y: int,
    size_px: int,
    color: tuple[int, int, int] = (230, 238, 255),
) -> None:
    """Four PS controller symbols (△ ○ ✕ ▢) arranged in a 2×2 cluster."""
    import math as _math  # noqa: F401 — already imported at module level; re-import kept for clarity

    cell_size = size_px // 2
    symbol_half = cell_size // 2 - 2
    stroke_width = max(2, size_px // 14)

    # (delta_x, delta_y) offsets and shape names for the four quadrants
    quadrant_offsets = [
        (-cell_size // 2, -cell_size // 2),
        ( cell_size // 2, -cell_size // 2),
        (-cell_size // 2,  cell_size // 2),
        ( cell_size // 2,  cell_size // 2),
    ]
    quadrant_shapes = ("triangle", "circle", "cross", "square")

    for (offset_x, offset_y), shape_name in zip(quadrant_offsets, quadrant_shapes):
        symbol_center_x = center_x + offset_x
        symbol_center_y = center_y + offset_y

        if shape_name == "triangle":
            pen.polygon(
                [
                    (symbol_center_x, symbol_center_y - symbol_half),
                    (symbol_center_x - symbol_half, symbol_center_y + symbol_half - 1),
                    (symbol_center_x + symbol_half, symbol_center_y + symbol_half - 1),
                ],
                outline=color, width=stroke_width,
            )
        elif shape_name == "circle":
            pen.ellipse(
                (symbol_center_x - symbol_half, symbol_center_y - symbol_half,
                 symbol_center_x + symbol_half, symbol_center_y + symbol_half),
                outline=color, width=stroke_width,
            )
        elif shape_name == "cross":
            cross_reach = int(symbol_half * 0.9)
            pen.line(
                (symbol_center_x - cross_reach, symbol_center_y - cross_reach,
                 symbol_center_x + cross_reach, symbol_center_y + cross_reach),
                fill=color, width=stroke_width,
            )
            pen.line(
                (symbol_center_x - cross_reach, symbol_center_y + cross_reach,
                 symbol_center_x + cross_reach, symbol_center_y - cross_reach),
                fill=color, width=stroke_width,
            )
        elif shape_name == "square":
            pen.rectangle(
                (symbol_center_x - symbol_half, symbol_center_y - symbol_half,
                 symbol_center_x + symbol_half, symbol_center_y + symbol_half),
                outline=color, width=stroke_width,
            )


def draw_ra_logo(
    pen: ImageDraw.ImageDraw,
    center_x: int,
    center_y: int,
    size_px: int,
    color: tuple[int, int, int] = (255, 255, 255),
    background_color: tuple[int, int, int] = (210, 174, 46),
) -> None:
    """RetroAchievements logo: colored circle with a centered star."""
    half_size = size_px // 2
    pen.ellipse(
        (center_x - half_size, center_y - half_size,
         center_x + half_size, center_y + half_size),
        fill=background_color,
    )
    draw_star(pen, center_x, center_y, int(size_px * 0.62), filled=True, color=color)


# ---------------------------------------------------------------------------
# Pill badge
# ---------------------------------------------------------------------------

PILL_BADGE_TEXT_FIT_WIDTH_RATIO = 0.92     # max text width as fraction of pill width
PILL_BADGE_TEXT_HEIGHT_RATIO = 0.75        # max text height as fraction of pill height
PILL_BADGE_TEXT_START_SIZE_RATIO = 0.72    # initial fit-font size as fraction of pill height
PILL_BADGE_PROBE_FONT_SIZE_RATIO = 0.6     # probe font for width measurement
PILL_BADGE_HORIZONTAL_PAD_RATIO = 0.55     # extra horizontal padding = height * ratio
PILL_BADGE_MIN_WIDTH_OVER_HEIGHT_PX = 4    # minimum width = height + this value


def draw_label_badge(
    pen: ImageDraw.ImageDraw,
    center_x: int,
    center_y: int,
    height_px: int,
    label_text: str,
    fill_color: tuple[int, int, int],
    text_color: tuple[int, int, int] = (255, 255, 255),
) -> None:
    """Draw a rounded pill badge containing a text label.

    Width auto-fits the text so short labels ('M') stay compact while longer
    ones ('RETRORATIO') still fit. The minimum width is ``height + 4`` px.
    """
    probe_font_size = max(10, int(height_px * PILL_BADGE_PROBE_FONT_SIZE_RATIO))
    probe_font = get_font(probe_font_size, bold=True)
    measured_text_width, _ = text_size(pen, label_text, probe_font)
    pill_width = max(
        height_px + PILL_BADGE_MIN_WIDTH_OVER_HEIGHT_PX,
        measured_text_width + int(height_px * PILL_BADGE_HORIZONTAL_PAD_RATIO),
    )
    pill_left = center_x - pill_width // 2
    pill_top = center_y - height_px // 2
    rounded_rect(
        pen,
        (pill_left, pill_top, pill_left + pill_width, pill_top + height_px),
        radius=height_px // 2,
        fill=fill_color,
    )
    label_font = fit_font(
        pen, label_text,
        max_w=int(pill_width * PILL_BADGE_TEXT_FIT_WIDTH_RATIO),
        max_h=int(height_px * PILL_BADGE_TEXT_HEIGHT_RATIO),
        start=int(height_px * PILL_BADGE_TEXT_START_SIZE_RATIO),
        bold=True,
    )
    draw_text(pen, (center_x, center_y), label_text, label_font, text_color, anchor="mm")


# ---------------------------------------------------------------------------
# Icon asset loading
# ---------------------------------------------------------------------------

def load_platform_icon(platform: str) -> Image.Image | None:
    """Return the user-supplied platform icon at assets/icons/<platform>.png, if present."""
    icon_path = ASSETS_ICONS / f"{platform}.png"
    if not icon_path.exists():
        return None
    try:
        return Image.open(icon_path).convert("RGBA")
    except OSError:
        return None


def load_stat_icon(platform: str, label_key: str) -> Image.Image | None:
    """Return a user-supplied icon for a stat label (trophy tier, etc.).

    Lookup order:
      assets/icons/<platform>/<label>.png  (e.g. assets/icons/psn/platinum.png)
      assets/icons/<label>.png             (cross-platform fallback)
    """
    normalized_key = (label_key or "").lower()
    search_paths = [
        ASSETS_ICONS / platform / f"{normalized_key}.png",
        ASSETS_ICONS / f"{normalized_key}.png",
    ]
    for icon_path in search_paths:
        if icon_path.exists():
            try:
                return Image.open(icon_path).convert("RGBA")
            except OSError:
                continue
    return None


# ---------------------------------------------------------------------------
# Icon pasting
# ---------------------------------------------------------------------------

def _scale_image_to_fit(
    image: Image.Image,
    max_width_px: int,
    max_height_px: int,
) -> Image.Image:
    """Scale `image` to fit within the given dimensions, preserving aspect ratio."""
    source_width, source_height = image.size
    scale_factor = min(max_width_px / source_width, max_height_px / source_height)
    scaled_width = max(1, int(source_width * scale_factor))
    scaled_height = max(1, int(source_height * scale_factor))
    return image.resize((scaled_width, scaled_height), Image.LANCZOS)


def paste_centered_icon(
    canvas: Image.Image,
    icon_image: Image.Image,
    center_x: int,
    center_y: int,
    target_size_px: int,
) -> None:
    """Fit `icon_image` into a square box and paste it centered at (center_x, center_y)."""
    scaled_icon = _scale_image_to_fit(icon_image, target_size_px, target_size_px)
    scaled_width, scaled_height = scaled_icon.size
    paste_left = center_x - scaled_width // 2
    paste_top = center_y - scaled_height // 2
    canvas.paste(scaled_icon, (paste_left, paste_top), scaled_icon)


def paste_platform_icon(
    canvas: Image.Image,
    icon_image: Image.Image,
    destination_box: tuple[int, int, int, int],
) -> tuple[int, int, int, int]:
    """Fit `icon_image` inside `destination_box` preserving aspect ratio, left-aligned
    and vertically centered. Returns the actual bounding box consumed."""
    box_left, box_top, box_right, box_bottom = destination_box
    available_width = box_right - box_left
    available_height = box_bottom - box_top
    scaled_icon = _scale_image_to_fit(icon_image, available_width, available_height)
    scaled_width, scaled_height = scaled_icon.size
    paste_left = box_left
    paste_top = box_top + (available_height - scaled_height) // 2
    canvas.paste(scaled_icon, (paste_left, paste_top), scaled_icon)
    return (paste_left, paste_top, paste_left + scaled_width, paste_top + scaled_height)


def draw_platform_icon(
    pen: ImageDraw.ImageDraw,
    platform: str,
    box: tuple[int, int, int, int],
    accent_color: tuple[int, int, int],
) -> None:
    """Draw a procedural platform icon when no user-supplied image is present."""
    box_left, box_top, box_right, box_bottom = box
    center_x = (box_left + box_right) // 2
    center_y = (box_top + box_bottom) // 2
    icon_size = min(box_right - box_left, box_bottom - box_top)

    if platform == "xbox":
        draw_xbox_logo(pen, center_x, center_y, icon_size, color=(255, 255, 255), background_color=accent_color)
    elif platform == "psn":
        draw_playstation_symbols(pen, center_x, center_y, icon_size, color=(230, 238, 255))
    elif platform == "retroachievements":
        draw_ra_logo(pen, center_x, center_y, icon_size, color=(255, 255, 255), background_color=accent_color)
    else:
        draw_footer_glyph(
            pen, box, platform[:2].upper(),
            foreground_color=(255, 255, 255),
            background_circle_color=accent_color,
        )
