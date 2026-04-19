"""Low-level drawing primitives: fonts, text, icons, stars, background."""
from __future__ import annotations

import math
import os
from functools import lru_cache
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ASSETS_FONTS = Path(__file__).resolve().parents[2] / "assets" / "fonts"
ASSETS_ICONS = Path(__file__).resolve().parents[2] / "assets" / "icons"

_FONT_CANDIDATES = [
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
def get_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    candidates = list(_FONT_CANDIDATES)
    if bold:
        bold_first = [p for p in candidates if "bold" in str(p).lower() or p.name.lower().endswith("bd.ttf")]
        rest = [p for p in candidates if p not in bold_first]
        candidates = bold_first + rest
    for path in candidates:
        try:
            if os.path.exists(path):
                return ImageFont.truetype(str(path), size)
        except OSError:
            continue
    return ImageFont.load_default()


def text_size(draw: ImageDraw.ImageDraw, text: str, font) -> tuple[int, int]:
    box = draw.textbbox((0, 0), text, font=font)
    return box[2] - box[0], box[3] - box[1]


def draw_text(draw, xy, text, font, fill, anchor="la", shadow=False):
    if shadow:
        draw.text((xy[0] + 2, xy[1] + 2), text, font=font, fill=(0, 0, 0, 170), anchor=anchor)
    draw.text(xy, text, font=font, fill=fill, anchor=anchor)


def fit_font(draw, text: str, max_w: int, max_h: int, start=64, minimum=14, bold=True):
    size = start
    while size > minimum:
        font = get_font(size, bold=bold)
        w, h = text_size(draw, text, font)
        if w <= max_w and h <= max_h:
            return font
        size -= 2
    return get_font(minimum, bold=bold)


def rounded_rect(draw, box, radius, fill=None, outline=None, width=1):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def build_background(size: tuple[int, int], top, bottom, accent_colors=None) -> Image.Image:
    """Vertical gradient + soft radial glows behind each panel."""
    w, h = size
    img = _vertical_gradient(size, top, bottom).convert("RGBA")

    if accent_colors:
        glow = Image.new("RGBA", size, (0, 0, 0, 0))
        gdraw = ImageDraw.Draw(glow)
        slot_w = w / len(accent_colors)
        for i, color in enumerate(accent_colors):
            cx = int(slot_w * (i + 0.5))
            cy = h // 2
            _radial_blob(gdraw, cx, cy, int(slot_w * 0.55), color)
        glow = glow.filter(ImageFilter.GaussianBlur(radius=60))
        img = Image.alpha_composite(img, glow)
    return img


def _vertical_gradient(size, top, bottom) -> Image.Image:
    w, h = size
    base = Image.new("RGB", (1, h))
    px = base.load()
    for y in range(h):
        t = y / max(h - 1, 1)
        px[0, y] = (
            int(top[0] + (bottom[0] - top[0]) * t),
            int(top[1] + (bottom[1] - top[1]) * t),
            int(top[2] + (bottom[2] - top[2]) * t),
        )
    return base.resize((w, h))


def _radial_blob(draw, cx, cy, r, color):
    (cr, cg, cb) = color
    draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(cr, cg, cb, 70))


def paste_circle_avatar(canvas, avatar, box, ring_color, ring_width=4):
    x0, y0, x1, y1 = box
    size = min(x1 - x0, y1 - y0)
    avatar = avatar.convert("RGBA").resize((size, size), Image.LANCZOS)
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, size, size), fill=255)
    canvas.paste(avatar, (x0, y0), mask)
    ImageDraw.Draw(canvas).ellipse(
        (x0, y0, x0 + size, y0 + size), outline=ring_color, width=ring_width
    )


def draw_placeholder_avatar(draw, box, ring_color, fill=(58, 70, 92)):
    draw.ellipse(box, fill=fill, outline=ring_color, width=4)
    cx = (box[0] + box[2]) // 2
    cy = (box[1] + box[3]) // 2
    # simple silhouette: head circle + shoulders arc
    r = (box[2] - box[0]) // 2
    head_r = int(r * 0.35)
    hy = cy - int(r * 0.1)
    draw.ellipse((cx - head_r, hy - head_r, cx + head_r, hy + head_r), fill=(190, 200, 220))
    shoulder_y = cy + int(r * 0.28)
    shoulder_h = int(r * 0.5)
    draw.chord(
        (cx - int(r * 0.75), shoulder_y, cx + int(r * 0.75), shoulder_y + shoulder_h * 2),
        start=180, end=360, fill=(190, 200, 220),
    )


def draw_trophy(draw, cx, cy, size, color):
    """Cup-style trophy that reads clearly even at small sizes."""
    r = size // 2
    # cup body (tapered)
    cup_top_l = cx - r
    cup_top_r = cx + r
    cup_bot_l = cx - int(r * 0.7)
    cup_bot_r = cx + int(r * 0.7)
    cup_top_y = cy - r + 2
    cup_bot_y = cy + int(r * 0.35)
    draw.polygon(
        [(cup_top_l, cup_top_y), (cup_top_r, cup_top_y),
         (cup_bot_r, cup_bot_y), (cup_bot_l, cup_bot_y)],
        fill=color,
    )
    # rim highlight
    draw.ellipse((cup_top_l, cup_top_y - 3, cup_top_r, cup_top_y + 3), fill=color)
    # handles
    hw = max(2, size // 10)
    h_top = cup_top_y + 2
    h_bot = cup_bot_y - 2
    draw.arc((cup_top_l - int(r * 0.5), h_top, cup_top_l + 2, h_bot),
             start=90, end=270, fill=color, width=hw)
    draw.arc((cup_top_r - 2, h_top, cup_top_r + int(r * 0.5), h_bot),
             start=-90, end=90, fill=color, width=hw)
    # stem
    stem_w = max(3, size // 7)
    draw.rectangle((cx - stem_w, cup_bot_y, cx + stem_w, cy + int(r * 0.75)), fill=color)
    # base
    base_w = int(r * 0.9)
    base_h = max(3, size // 10)
    draw.rectangle(
        (cx - base_w, cy + int(r * 0.75), cx + base_w, cy + int(r * 0.75) + base_h),
        fill=color,
    )


def draw_star(draw, cx, cy, size, filled=True, color=(232, 196, 56), outline_only=False):
    pts = []
    for i in range(10):
        angle = -math.pi / 2 + i * math.pi / 5
        r = size / 2 if i % 2 == 0 else size / 4.5
        pts.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))
    if filled and not outline_only:
        draw.polygon(pts, fill=color)
    else:
        draw.polygon(pts, outline=color, width=2)


def draw_stars_row(draw, x, y, total, filled, size=20, gap=4, color=(232, 196, 56)):
    filled = max(0, min(filled, total))
    for i in range(total):
        cx = x + i * (size + gap) + size // 2
        draw_star(draw, cx, y + size // 2, size, filled=i < filled, color=color)


def draw_footer_glyph(draw, box, glyph: str, fg, bg_circle_color):
    """Small round badge containing the platform's short glyph (e.g. "X", "PS", "RA")."""
    x0, y0, x1, y1 = box
    cx = (x0 + x1) // 2
    cy = (y0 + y1) // 2
    r = (y1 - y0) // 2 - 2
    draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=bg_circle_color)
    font = fit_font(draw, glyph, max_w=int(r * 1.4), max_h=int(r * 1.4), start=int(r * 1.4), bold=True)
    draw_text(draw, (cx, cy), glyph, font, fg, anchor="mm")


def draw_xbox_logo(draw, cx: int, cy: int, size: int, color=(255, 255, 255),
                   bg_color=(16, 124, 16)):
    """Xbox logo: green sphere with a stylized white 'X' formed by two thick diagonals."""
    r = size // 2
    draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=bg_color)
    stroke = max(3, size // 7)
    d = int(r * 0.58)
    # two thick diagonal strokes forming the X, clipped to the circle
    draw.line((cx - d, cy - d, cx + d, cy + d), fill=color, width=stroke)
    draw.line((cx - d, cy + d, cx + d, cy - d), fill=color, width=stroke)


def draw_playstation_symbols(draw, cx: int, cy: int, size: int, color=(230, 238, 255)):
    """Four PS controller symbols (△ ○ ✕ ▢) arranged in a 2x2 cluster."""
    import math as _m

    cell = size // 2
    half = cell // 2 - 2
    offsets = [(-cell // 2, -cell // 2), (cell // 2, -cell // 2),
               (-cell // 2,  cell // 2), (cell // 2,  cell // 2)]
    shapes = ("triangle", "circle", "cross", "square")
    stroke = max(2, size // 14)

    for (dx, dy), shape in zip(offsets, shapes):
        x = cx + dx
        y = cy + dy
        if shape == "triangle":
            pts = [
                (x, y - half),
                (x - half, y + half - 1),
                (x + half, y + half - 1),
            ]
            draw.polygon(pts, outline=color, width=stroke)
        elif shape == "circle":
            draw.ellipse(
                (x - half, y - half, x + half, y + half),
                outline=color, width=stroke,
            )
        elif shape == "cross":
            d = int(half * 0.9)
            draw.line((x - d, y - d, x + d, y + d), fill=color, width=stroke)
            draw.line((x - d, y + d, x + d, y - d), fill=color, width=stroke)
        elif shape == "square":
            draw.rectangle(
                (x - half, y - half, x + half, y + half),
                outline=color, width=stroke,
            )


def draw_ra_logo(draw, cx: int, cy: int, size: int,
                 color=(255, 255, 255), bg_color=(210, 174, 46)):
    """RA logo placeholder: colored circle with a white star centered inside."""
    r = size // 2
    draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=bg_color)
    draw_star(draw, cx, cy, int(size * 0.62), filled=True, color=color)


def draw_label_badge(
    draw,
    cx: int,
    cy: int,
    height: int,
    text: str,
    fill: tuple[int, int, int],
    fg: tuple[int, int, int] = (255, 255, 255),
):
    """Rounded pill badge containing a text label. Width auto-fits the text so
    short labels ('M') stay compact while longer ones ('TRUE RATIO') still fit."""
    probe_font = get_font(max(10, int(height * 0.6)), bold=True)
    tw, _ = text_size(draw, text, probe_font)
    # tighter horizontal padding — hugs the text more closely
    w = max(height + 4, tw + int(height * 0.55))
    x0 = cx - w // 2
    y0 = cy - height // 2
    rounded_rect(draw, (x0, y0, x0 + w, y0 + height), radius=height // 2, fill=fill)
    font = fit_font(
        draw, text,
        max_w=int(w * 0.92),
        max_h=int(height * 0.75),
        start=int(height * 0.72),
        bold=True,
    )
    draw_text(draw, (cx, cy), text, font, fg, anchor="mm")


def load_platform_icon(platform: str) -> Image.Image | None:
    """Return the user-supplied icon at assets/icons/<platform>.png, if present."""
    p = ASSETS_ICONS / f"{platform}.png"
    if not p.exists():
        return None
    try:
        return Image.open(p).convert("RGBA")
    except OSError:
        return None


def load_stat_icon(platform: str, label: str) -> Image.Image | None:
    """Return a user-supplied icon for a stat label (trophy tier, etc.).

    Lookup order:
      assets/icons/<platform>/<label>.png  (e.g. assets/icons/psn/platinum.png)
      assets/icons/<label>.png             (cross-platform fallback)
    """
    key = (label or "").lower()
    for p in (ASSETS_ICONS / platform / f"{key}.png", ASSETS_ICONS / f"{key}.png"):
        if p.exists():
            try:
                return Image.open(p).convert("RGBA")
            except OSError:
                continue
    return None


def paste_centered_icon(canvas: Image.Image, icon: Image.Image, cx: int, cy: int, size: int):
    """Fit icon into a size×size box centered at (cx, cy), preserving aspect."""
    iw, ih = icon.size
    scale = min(size / iw, size / ih)
    w = max(1, int(iw * scale))
    h = max(1, int(ih * scale))
    scaled = icon.resize((w, h), Image.LANCZOS)
    canvas.paste(scaled, (cx - w // 2, cy - h // 2), scaled)


def paste_platform_icon(
    canvas: Image.Image, icon: Image.Image, box: tuple[int, int, int, int]
) -> tuple[int, int, int, int]:
    """Fit `icon` inside `box` preserving aspect ratio, left-align vertically
    centered. Return the actual bounding box consumed."""
    x0, y0, x1, y1 = box
    max_w = x1 - x0
    max_h = y1 - y0
    iw, ih = icon.size
    scale = min(max_w / iw, max_h / ih)
    w = max(1, int(iw * scale))
    h = max(1, int(ih * scale))
    scaled = icon.resize((w, h), Image.LANCZOS)
    px = x0
    py = y0 + (max_h - h) // 2
    canvas.paste(scaled, (px, py), scaled)
    return (px, py, px + w, py + h)


def draw_platform_icon(draw, platform: str, box, accent_color):
    """Procedural fallback when no user-supplied icon is present."""
    x0, y0, x1, y1 = box
    cx = (x0 + x1) // 2
    cy = (y0 + y1) // 2
    size = min(x1 - x0, y1 - y0)
    if platform == "xbox":
        draw_xbox_logo(draw, cx, cy, size, color=(255, 255, 255), bg_color=accent_color)
    elif platform == "psn":
        draw_playstation_symbols(draw, cx, cy, size, color=(230, 238, 255))
    elif platform == "retroachievements":
        draw_ra_logo(draw, cx, cy, size, color=(255, 255, 255), bg_color=accent_color)
    else:
        draw_footer_glyph(draw, box, platform[:2].upper(),
                          fg=(255, 255, 255), bg_circle_color=accent_color)
