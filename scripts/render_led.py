"""Rasterize the LED-matrix header/divider so GitHub always displays them."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

OUT = Path(__file__).resolve().parents[1] / "assets"
Color = tuple[int, int, int, int]

F = {
    "A": ["01110", "10001", "10001", "11111", "10001", "10001", "10001"],
    "B": ["11110", "10001", "10001", "11110", "10001", "10001", "11110"],
    "C": ["01110", "10001", "10000", "10000", "10000", "10001", "01110"],
    "D": ["11110", "10001", "10001", "10001", "10001", "10001", "11110"],
    "E": ["11111", "10000", "10000", "11110", "10000", "10000", "11111"],
    "F": ["11111", "10000", "10000", "11110", "10000", "10000", "10000"],
    "G": ["01110", "10001", "10000", "10111", "10001", "10001", "01111"],
    "H": ["10001", "10001", "10001", "11111", "10001", "10001", "10001"],
    "I": ["11111", "00100", "00100", "00100", "00100", "00100", "11111"],
    "J": ["00111", "00010", "00010", "00010", "00010", "10010", "01100"],
    "K": ["10001", "10010", "10100", "11000", "10100", "10010", "10001"],
    "L": ["10000", "10000", "10000", "10000", "10000", "10000", "11111"],
    "M": ["10001", "11011", "10101", "10101", "10001", "10001", "10001"],
    "N": ["10001", "11001", "10101", "10011", "10001", "10001", "10001"],
    "O": ["01110", "10001", "10001", "10001", "10001", "10001", "01110"],
    "P": ["11110", "10001", "10001", "11110", "10000", "10000", "10000"],
    "Q": ["01110", "10001", "10001", "10001", "10101", "10010", "01101"],
    "R": ["11110", "10001", "10001", "11110", "10100", "10010", "10001"],
    "S": ["01111", "10000", "10000", "01110", "00001", "00001", "11110"],
    "T": ["11111", "00100", "00100", "00100", "00100", "00100", "00100"],
    "U": ["10001", "10001", "10001", "10001", "10001", "10001", "01110"],
    "V": ["10001", "10001", "10001", "10001", "10001", "01010", "00100"],
    "W": ["10001", "10001", "10001", "10101", "10101", "10101", "01010"],
    "X": ["10001", "10001", "01010", "00100", "01010", "10001", "10001"],
    "Y": ["10001", "10001", "01010", "00100", "00100", "00100", "00100"],
    "Z": ["11111", "00001", "00010", "00100", "01000", "10000", "11111"],
    "0": ["01110", "10001", "10011", "10101", "11001", "10001", "01110"],
    "1": ["00100", "01100", "00100", "00100", "00100", "00100", "01110"],
    "2": ["01110", "10001", "00001", "00110", "01000", "10000", "11111"],
    "3": ["11110", "00001", "00001", "01110", "00001", "00001", "11110"],
    "4": ["00010", "00110", "01010", "10010", "11111", "00010", "00010"],
    "5": ["11111", "10000", "11110", "00001", "00001", "10001", "01110"],
    "6": ["01110", "10000", "10000", "11110", "10001", "10001", "01110"],
    "7": ["11111", "00001", "00010", "00100", "01000", "01000", "01000"],
    "8": ["01110", "10001", "10001", "01110", "10001", "10001", "01110"],
    "9": ["01110", "10001", "10001", "01111", "00001", "00001", "01110"],
    " ": ["00000", "00000", "00000", "00000", "00000", "00000", "00000"],
    ".": ["00000", "00000", "00000", "00000", "00000", "00100", "00100"],
    ":": ["00000", "00100", "00100", "00000", "00100", "00100", "00000"],
    "-": ["00000", "00000", "00000", "11111", "00000", "00000", "00000"],
    "/": ["00001", "00010", "00010", "00100", "01000", "01000", "10000"],
}

ON: Color = (61, 255, 138, 255)
ON_CORE: Color = (216, 255, 232, 255)
MAGENTA: Color = (232, 121, 249, 255)
MAGENTA_CORE: Color = (255, 220, 255, 255)
OFF: Color = (11, 26, 18, 255)
PANEL: Color = (7, 9, 13, 255)
FRAME: Color = (28, 58, 42, 255)
GAP_OFF_INDEX = 3
HEADER_MARGIN = 40


def _validate_font() -> None:
    for char, rows in F.items():
        if len(rows) != 7:
            raise ValueError(f"glyph {char!r} must have 7 rows")
        for row in rows:
            if len(row) != 5 or set(row) - {"0", "1"}:
                raise ValueError(f"glyph {char!r} has a bad row {row!r}")


_validate_font()


def text_size(text: str, pitch: int) -> tuple[int, int]:
    """Return pixel width/height of a 5x7 LED string at the given pitch."""
    cols = len(text) * 5 + max(0, len(text) - 1)
    return cols * pitch, 7 * pitch


def blit_led(
    img: Image.Image,
    text: str,
    origin: tuple[int, int],
    pitch: int,
    on: Color = ON,
    core: Color = ON_CORE,
) -> None:
    """Draw a 5x7 LED string onto `img` at `origin`."""
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    x0, y0 = origin
    radius = pitch * 0.34
    x = x0
    for char in text:
        glyph = F[char]
        for row, bits in enumerate(glyph):
            for col, bit in enumerate(bits):
                cx = x + (col + 0.5) * pitch
                cy = y0 + (row + 0.5) * pitch
                if bit == "1":
                    draw.ellipse(
                        (cx - radius, cy - radius, cx + radius, cy + radius),
                        fill=on,
                    )
                    inner = radius * 0.55
                    draw.ellipse(
                        (cx - inner, cy - inner, cx + inner, cy + inner),
                        fill=core,
                    )
                else:
                    off_r = radius * 0.72
                    draw.ellipse(
                        (cx - off_r, cy - off_r, cx + off_r, cy + off_r),
                        fill=OFF,
                    )
        x += 6 * pitch
    glow = overlay.filter(ImageFilter.GaussianBlur(pitch * 0.18))
    img.alpha_composite(glow)
    img.alpha_composite(overlay)


def _assert_fits(
    label: str,
    x: int,
    y: int,
    size: tuple[int, int],
    canvas: tuple[int, int],
) -> None:
    width, height = size
    canvas_w, canvas_h = canvas
    if x < HEADER_MARGIN or y < HEADER_MARGIN:
        raise ValueError(f"{label} collides with margin ({x},{y})")
    if x + width > canvas_w - HEADER_MARGIN:
        raise ValueError(f"{label} overflows horizontally ({x + width})")
    if y + height > canvas_h - HEADER_MARGIN:
        raise ValueError(f"{label} overflows vertically ({y + height})")


def render_header() -> None:
    """Write the profile LED-matrix banner."""
    width, height = 2360, 620
    img = Image.new("RGBA", (width, height), PANEL)
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle(
        (0, 0, width - 1, height - 1),
        radius=28,
        outline=FRAME,
        width=4,
    )
    draw.rounded_rectangle(
        (20, 20, width - 21, height - 21),
        radius=16,
        outline=(22, 50, 38, 255),
        width=2,
    )

    screws = (
        (48, 48),
        (width - 48, 48),
        (48, height - 48),
        (width - 48, height - 48),
    )
    for sx, sy in screws:
        draw.ellipse(
            (sx - 8, sy - 8, sx + 8, sy + 8),
            fill=(42, 47, 51, 255),
            outline=(90, 100, 108, 255),
            width=2,
        )

    title = "ALJO JOBY"
    sub = "PRESENT DAY  PRESENT TIME"
    stat = "NODE ALJOJOBY9  LAYER WIRED  FY 2026"
    title_pitch, sub_pitch, stat_pitch = 30, 14, 10
    title_size = text_size(title, title_pitch)
    sub_size = text_size(sub, sub_pitch)
    stat_size = text_size(stat, stat_pitch)
    canvas = (width, height)

    online_origin = (96, 40)
    world_label = "WORLD LINE 1.048596"
    world_size = text_size(world_label, 8)
    world_origin = (width - 40 - world_size[0], 40)
    title_origin = ((width - title_size[0]) // 2, 110)
    sub_origin = ((width - sub_size[0]) // 2, title_origin[1] + title_size[1] + 24)
    stat_origin = ((width - stat_size[0]) // 2, sub_origin[1] + sub_size[1] + 24)

    _assert_fits("ONLINE", *online_origin, text_size("ONLINE", 8), canvas)
    _assert_fits("worldline", *world_origin, world_size, canvas)
    _assert_fits("title", *title_origin, title_size, canvas)
    _assert_fits("subtitle", *sub_origin, sub_size, canvas)
    _assert_fits("status", *stat_origin, stat_size, canvas)

    blit_led(img, "ONLINE", online_origin, 8)
    blit_led(img, world_label, world_origin, 8, on=MAGENTA, core=MAGENTA_CORE)
    blit_led(img, title, title_origin, title_pitch)
    blit_led(img, sub, sub_origin, sub_pitch, on=MAGENTA, core=MAGENTA_CORE)
    blit_led(img, stat, stat_origin, stat_pitch)

    scan = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    scan_draw = ImageDraw.Draw(scan)
    for y in range(24, height - 24, 4):
        scan_draw.line((24, y, width - 24, y), fill=(61, 255, 138, 18), width=1)
    img.alpha_composite(scan)

    out = img.convert("RGB")
    OUT.mkdir(parents=True, exist_ok=True)
    out.save(OUT / "led-header.png", optimize=True)
    print("wrote", OUT / "led-header.png", out.size)


def render_divider() -> None:
    """Write the repeating LED-dot divider."""
    width, height = 2360, 56
    img = Image.new("RGBA", (width, height), PANEL)
    overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    pitch = 20
    cols = (width - 80) // pitch
    r_on, r_off = 6.2, 4.2
    for i in range(cols):
        cx = 40 + i * pitch + pitch / 2
        cy = height / 2
        if i % 4 != GAP_OFF_INDEX:
            draw.ellipse((cx - r_on, cy - r_on, cx + r_on, cy + r_on), fill=ON)
        else:
            draw.ellipse(
                (cx - r_off, cy - r_off, cx + r_off, cy + r_off),
                fill=OFF,
            )
    glow = overlay.filter(ImageFilter.GaussianBlur(2.4))
    img.alpha_composite(glow)
    img.alpha_composite(overlay)
    out = img.convert("RGB")
    out.save(OUT / "led-divider.png", optimize=True)
    print("wrote", OUT / "led-divider.png", out.size)


if __name__ == "__main__":
    render_header()
    render_divider()
