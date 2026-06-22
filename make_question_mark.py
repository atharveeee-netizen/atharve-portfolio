"""Generate the yellow cartoon question-mark used as a placeholder in the
projects gallery frames (and the "Coming soon" detail pages).

Faithful to the reference the user supplied: a chunky rounded "?" in warm
yellow with a thick near-black outline. Rendered on a TRANSPARENT background
so it sits naturally on the cream museum mat (#fbf9f6) inside .painting-frame.

Output: assets/img/question-mark.png  (overwrites the unused dark version)
"""
import math
from PIL import Image, ImageDraw, ImageFont

SS = 4                      # supersample factor for smooth anti-aliasing
SIZE = 800                  # final px (square, matches the other frame art)
W = SIZE * SS

YELLOW = (0xF9, 0xB7, 0x1E, 255)
OUTLINE = (0x14, 0x12, 0x10, 255)   # near-black, warm
HIGHLIGHT = (255, 255, 255, 200)

FONT_CANDIDATES = [
    r"C:\Windows\Fonts\ariblk.ttf",   # Arial Black — chunky & rounded
    r"C:\Windows\Fonts\segoeuib.ttf", # Segoe UI Bold fallback
    r"C:\Windows\Fonts\arialbd.ttf",
]


def load_font(px):
    for p in FONT_CANDIDATES:
        try:
            return ImageFont.truetype(p, px)
        except OSError:
            continue
    raise SystemExit("No suitable bold font found")


def glyph_metrics(font, ch="?"):
    tmp = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
    b = tmp.textbbox((0, 0), ch, font=font)
    return b  # (x0, y0, x1, y1)


# --- size the glyph so its height fills ~60% of the canvas -------------------
target_h = int(W * 0.60)
fs = target_h                       # first guess
font = load_font(fs)
b = glyph_metrics(font)
gh = b[3] - b[1]
fs = max(8, int(fs * target_h / gh))
font = load_font(fs)
b = glyph_metrics(font)
gw, gh = b[2] - b[0], b[3] - b[1]

x = (W - gw) // 2 - b[0]
y = (W - gh) // 2 - b[1]

base = Image.new("RGBA", (W, W), (0, 0, 0, 0))

# --- thick rounded black outline via ring-stamping (dilation) ---------------
outline = Image.new("RGBA", (W, W), (0, 0, 0, 0))
od = ImageDraw.Draw(outline)
t = W * 0.024                        # outline thickness
for frac in (1.0, 0.72, 0.45):       # nested rings => solid dilation
    r = t * frac
    for i in range(48):
        a = 2 * math.pi * i / 48
        od.text((x + r * math.cos(a), y + r * math.sin(a)), "?", font=font, fill=OUTLINE)
base = Image.alpha_composite(base, outline)

# --- yellow glyph on top ----------------------------------------------------
fill = Image.new("RGBA", (W, W), (0, 0, 0, 0))
ImageDraw.Draw(fill).text((x, y), "?", font=font, fill=YELLOW)
base = Image.alpha_composite(base, fill)

# --- subtle white highlight on the upper-left of the hook -------------------
hl = Image.new("RGBA", (W, W), (0, 0, 0, 0))
hd = ImageDraw.Draw(hl)
hx, hy = x + int(gw * 0.30), y + int(gh * 0.17)
hx2, hy2 = x + int(gw * 0.255), y + int(gh * 0.29)
hw = int(W * 0.011)
hd.line([(hx, hy), (hx2, hy2)], fill=HIGHLIGHT, width=hw)
for (px, py) in ((hx, hy), (hx2, hy2)):
    hd.ellipse([px - hw / 2, py - hw / 2, px + hw / 2, py + hw / 2], fill=HIGHLIGHT)
base = Image.alpha_composite(base, hl)

# --- downscale & save -------------------------------------------------------
out = base.resize((SIZE, SIZE), Image.LANCZOS)
out.save(r"assets/img/question-mark.png")
print("wrote assets/img/question-mark.png", out.size)
