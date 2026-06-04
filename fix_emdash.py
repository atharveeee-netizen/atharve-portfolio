import os
import glob

# Remove em dashes (—) from visible/prose copy across all exported pages.
# Rules (order matters):
#   1. Fix the footer attribution: `." — Albert Camus` -> `." Albert Camus`
#      (a plain comma after a closing quote reads badly).
#   2. Any spaced em dash ` — ` becomes a comma+space `, ` (clause separator).
# Only spaced em dashes are touched, so CSS `content: "—"` glyphs are left alone.

# Scan top-level HTML files
files = [f for f in os.listdir('.') if f.endswith('.html')]

# Also include projects/*.html subdirectory
files.extend(glob.glob('projects/*.html'))

for fn in files:
    with open(fn, 'r', encoding='utf-8', newline='') as f:
        s = f.read()
    orig = s
    s = s.replace('." — Albert Camus', '." Albert Camus')
    s = s.replace(' — ', ', ')
    if s != orig:
        with open(fn, 'w', encoding='utf-8', newline='') as f:
            f.write(s)
        print(f'updated {fn}')

print('done')
