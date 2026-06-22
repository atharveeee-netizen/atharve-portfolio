"""Fix the favicon flicker during page navigation.

Problem: the favicon was set to assets/img/ashu-dither.png — a 1024x623, 365KB
non-square PNG (declared with the wrong type="image/x-icon"). Browsers re-fetch
and downscale it on every navigation, so the tab icon blinks out (black/blank)
and reloads. With no real /favicon.ico, the browser's automatic /favicon.ico
request 404s and falls back to a cached default (the pieterkoopt "pk" icon).

Fix: derive a small, square, fast icon set from the same dither image and add a
real root /favicon.ico, then point every page at the new set with root-relative
paths (identical for root pages and projects/ subpages).
"""
import glob
import os
from PIL import Image

ROOT = r"C:\Users\noobg\.gemini\antigravity\scratch\atharve-portfolio"

# --- 1) Generate a small square icon set from the dither image -------------
src = os.path.join(ROOT, "assets", "img", "ashu-dither.png")
im = Image.open(src).convert("RGBA")
w, h = im.size
side = min(w, h)
left, top = (w - side) // 2, (h - side) // 2
sq = im.crop((left, top, left + side, top + side))  # centre square crop

png32 = os.path.join(ROOT, "assets", "img", "favicon-32.png")
png180 = os.path.join(ROOT, "assets", "img", "favicon-180.png")
ico = os.path.join(ROOT, "favicon.ico")

sq.resize((32, 32), Image.LANCZOS).save(png32, "PNG", optimize=True)
sq.convert("RGB").resize((180, 180), Image.LANCZOS).save(png180, "PNG", optimize=True)
sq.save(ico, sizes=[(16, 16), (32, 32), (48, 48)])

for p in (png32, png180, ico):
    print(f"  wrote {os.path.relpath(p, ROOT)} ({os.path.getsize(p)} bytes)")

# --- 2) Swap the favicon <link> tags on every page -------------------------
NEW = (
    '<link rel="icon" href="/favicon.ico" sizes="any"/>'
    '<link rel="icon" type="image/png" sizes="32x32" href="/assets/img/favicon-32.png"/>'
    '<link rel="apple-touch-icon" href="/assets/img/favicon-180.png"/>'
)

# old shortcut-icon link -> replaced by the full new set; old apple link -> removed
old_shortcut = [
    '<link href="assets/img/ashu-dither.png" rel="shortcut icon" type="image/x-icon"/>',
    '<link href="../assets/img/ashu-dither.png" rel="shortcut icon" type="image/x-icon"/>',
]
old_apple = [
    '<link href="assets/img/ashu-dither.png" rel="apple-touch-icon"/>',
    '<link href="../assets/img/ashu-dither.png" rel="apple-touch-icon"/>',
]

files = glob.glob(os.path.join(ROOT, "*.html")) + glob.glob(
    os.path.join(ROOT, "projects", "*.html")
)
for fp in files:
    with open(fp, "r", encoding="utf-8") as f:
        content = f.read()
    original = content
    for o in old_shortcut:
        content = content.replace(o, NEW)
    for o in old_apple:
        content = content.replace(o, "")
    if content != original:
        with open(fp, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  updated {os.path.relpath(fp, ROOT)}")
