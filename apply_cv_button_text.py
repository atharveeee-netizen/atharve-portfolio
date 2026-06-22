# -*- coding: utf-8 -*-
"""Rename the navbar "cv" button to "download cv", site-wide, June 22, 2026.

Idempotent: safe to re-run.
"""
import glob

REPLACEMENTS = [
    ('/* CV button:', '/* Download CV button:'),
    ('aria-label="View CV"', 'aria-label="Download CV"'),
    ('data-button-animate-chars="">cv</span>', 'data-button-animate-chars="">download cv</span>'),
]

FILES = [f for f in glob.glob("*.html") + glob.glob("projects/*.html")
         if f not in ("index.html.backup",)]

for f in FILES:
    text = open(f, encoding="utf-8").read()
    total = 0
    for old, new in REPLACEMENTS:
        count = text.count(old)
        if count:
            text = text.replace(old, new)
            total += count
    if total:
        open(f, "w", encoding="utf-8").write(text)
        print(f"{f}: replaced {total}x")
