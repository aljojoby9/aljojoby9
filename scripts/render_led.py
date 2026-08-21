"""Rasterize the LED-matrix header/divider so GitHub always displays them."""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

OUT = Path(__file__).resolve().parents[1] / "assets"

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

ON = (61, 255, 138, 255)
ON_CORE = (216, 255, 232, 255)
MAGENTA = (232, 121, 249, 255)
MAGENTA_CORE = (255, 220, 255, 255)
OFF = (11, 26, 18, 255)
PANEL = (7, 9, 13, 255)
FRAME = (28, 58, 42, 255)


def text_size(text: str, pitch: int) -> tuple[int, int]:
    cols = len(text) * 5 + max(0, len(text) - 1)
    return cols * pitch, 7 * pitch


def blit_led(img: Image.Image, text: str, origin: tuple[int, int], pitch: int, on=ON, core=ON_CORE) -> None:
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    x0, y0 = origin
    r = pitch * 0.34
    x = x0
    for i, ch in enumerate(text):
        glyph = F.get(ch, F[" "])
        for row, bits in enumerate(glyph):
            for col, bit in enumerate(bits):
                cx = x + (col + 0.5) * pitch
                cy = y0 + (row + 0.5) * pitch
                if bit == "1":
                    draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=on)
                    draw.ellipse(
                        (cx - r * 0.55, cy - r * 0.55, cx + r * 0.55, cy + r * 0.55),
                        fill=core,
                    )
                else:
                    draw.ellipse((cx - r * 0.72, cy - r * 0.72, cx + r * 0.72, cy + r * 0.72), fill=OFF)
        x += 6 * pitch
    glow = overlay.filter(ImageFilter.GaussianBlur(pitch * 0.18))
    img.alpha_composite(glow)
    img.alpha_composite(overlay)


def render_header() -> None:
    W, H = 2360, 620
    img = Image.new("RGBA", (W, H), PANEL)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((0, 0, W - 1, H - 1), radius=28, outline=FRAME, width=4)
    d.rounded_rectangle((20, 20, W - 21, H - 21), radius=16, outline=(22, 50, 38, 255), width=2)

    for x, y in ((48, 48), (W - 48, 48), (48, H - 48), (W - 48, H - 48)):
        d.ellipse((x - 8, y - 8, x + 8, y + 8), fill=(42, 47, 51, 255), outline=(90, 100, 108, 255), width=2)

    title = "ALJO JOBY"
    sub = "PRESENT DAY  PRESENT TIME"
    stat = "NODE ALJOJOBY9  LAYER WIRED  FY 2026"
    tp, sp, stp = 30, 14, 10
    tw, th = text_size(title, tp)
    sw, sh = text_size(sub, sp)
    stw, sth = text_size(stat, stp)

    blit_led(img, "ONLINE", (96, 40), 8)
    blit_led(
        img,
        "WORLD LINE 1.048596",
        (W - 40 - text_size("WORLD LINE 1.048596", 8)[0], 40),
        8,
        on=MAGENTA,
        core=MAGENTA_CORE,
    )
    title_y = 110
    sub_y = title_y + th + 24
    stat_y = sub_y + sh + 24
    blit_led(img, title, ((W - tw) // 2, title_y), tp)
    blit_led(img, sub, ((W - sw) // 2, sub_y), sp, on=MAGENTA, core=MAGENTA_CORE)
    blit_led(img, stat, ((W - stw) // 2, stat_y), stp)

    scan = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(scan)
    for y in range(24, H - 24, 4):
        sd.line((24, y, W - 24, y), fill=(61, 255, 138, 18), width=1)
    img.alpha_composite(scan)

    out = img.convert("RGB")
    OUT.mkdir(parents=True, exist_ok=True)
    out.save(OUT / "led-header.png", optimize=True)
    print("wrote", OUT / "led-header.png", out.size)


def render_divider() -> None:
    W, H = 2360, 56
    img = Image.new("RGBA", (W, H), PANEL)
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    pitch = 20
    cols = (W - 80) // pitch
    r_on, r_off = 6.2, 4.2
    for i in range(cols):
        cx = 40 + i * pitch + pitch / 2
        cy = H / 2
        if i % 4 != 3:
            d.ellipse((cx - r_on, cy - r_on, cx + r_on, cy + r_on), fill=ON)
        else:
            d.ellipse((cx - r_off, cy - r_off, cx + r_off, cy + r_off), fill=OFF)
    glow = overlay.filter(ImageFilter.GaussianBlur(2.4))
    img.alpha_composite(glow)
    img.alpha_composite(overlay)
    out = img.convert("RGB")
    out.save(OUT / "led-divider.png", optimize=True)
    print("wrote", OUT / "led-divider.png", out.size)


if __name__ == "__main__":
    render_header()
    render_divider()
