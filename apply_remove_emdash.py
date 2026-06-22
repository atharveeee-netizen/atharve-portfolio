# -*- coding: utf-8 -*-
"""Replace em-dash (—, U+2014) with a plain hyphen site-wide, June 22, 2026.

Covers visible copy (titles, body text, alt text, meta descriptions) and dev
comments alike. Does NOT touch en-dash (–, U+2013) anywhere, which is a
distinct character used deliberately as "Coming Soon" placeholder filler on
several project pages -- left untouched on purpose.

Idempotent: safe to re-run.
"""
import glob

FILES = [f for f in glob.glob("*.html") + glob.glob("projects/*.html")
         if f not in ("index.html.backup",)]

for f in FILES:
    text = open(f, encoding="utf-8").read()
    count = text.count("—")
    if count:
        text = text.replace("—", "-")
        open(f, "w", encoding="utf-8").write(text)
        print(f"{f}: replaced {count}x")
