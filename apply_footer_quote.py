# -*- coding: utf-8 -*-
"""Swap the shared footer disclaimer quote (Camus) site-wide, June 13, 2026.

Idempotent: safe to re-run.
"""
import glob

OLD = '"Real generosity toward the future lies in giving all to the present." Albert Camus, The Rebel, 1951.'
NEW = '"There is no sun without shadow, and it is essential to know the night." ~Camus'

FILES = [f for f in glob.glob("*.html") + glob.glob("projects/*.html")
         if f not in ("index.html.backup",)]

for f in FILES:
    text = open(f, encoding="utf-8").read()
    count = text.count(OLD)
    if count:
        text = text.replace(OLD, NEW)
        open(f, "w", encoding="utf-8").write(text)
        print(f"{f}: replaced {count}x")
