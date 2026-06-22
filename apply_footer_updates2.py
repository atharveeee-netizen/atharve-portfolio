# -*- coding: utf-8 -*-
"""Footer tweaks round 2, June 13, 2026.

1. Remove the "Nature flew first. / I'm still translating." heading block
   from footer-col.is-left (two markup variants: top-level pages vs project
   subpages, which have an extra empty display-inlineflex div).
2. Rewrite the Camus footer quote: no quote marks, all lowercase, "night"
   continues directly into "~camus" (no period, no space).

Idempotent: safe to re-run.
"""
import glob

FILES = [f for f in glob.glob("*.html") + glob.glob("projects/*.html")
         if f not in ("index.html.backup",)]

APOS = chr(39)
CURLY = chr(8217)

NATURE_TOP = (
    '<div><h2 class="heading-wrapper"><div class="heading-s">Nature flew first.</div>'
    '<div class="heading-s alt-heading">I' + APOS + 'm still translating.</div></h2></div>'
)
NATURE_PROJECT = (
    '<div><h2 class="heading-wrapper"><div class="heading-s">Nature flew first.</div>'
    '<div class="heading-s alt-heading">I' + APOS + 'm still translating.</div></h2>'
    '<div class="display-inlineflex"></div></div>'
)

CAMUS_OLD = '"There is no sun without shadow, and it is essential to know the night." ~Camus'
CAMUS_NEW = 'there is no sun without shadow, and it is essential to know the night~camus'

for f in FILES:
    text = open(f, encoding="utf-8").read()
    orig = text
    notes = []

    for old in (NATURE_TOP, NATURE_PROJECT, NATURE_TOP.replace(APOS, CURLY), NATURE_PROJECT.replace(APOS, CURLY)):
        c = text.count(old)
        if c:
            text = text.replace(old, "")
            notes.append(f"nature-removed x{c}")
            break

    c = text.count(CAMUS_OLD)
    if c:
        text = text.replace(CAMUS_OLD, CAMUS_NEW)
        notes.append(f"camus x{c}")

    if text != orig:
        open(f, "w", encoding="utf-8").write(text)
        print(f"{f}: {', '.join(notes)}")
    else:
        print(f"{f}: (no change)")
