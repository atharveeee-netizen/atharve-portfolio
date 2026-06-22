#!/usr/bin/env python3
"""
restore_left_social.py
Revert the social cluster back to the LEFT as plain bordered icon cells
(LinkedIn + GitHub, like before), remove the green right-side block, and make
the bar a true pixel-clone of pieterkoopt.nl by deferring sizing to the shared
template (12px links, 52px icon cells) instead of too-small hardcoded values.

Usage:
  python restore_left_social.py index.html   # one file
  python restore_left_social.py --all        # every page
"""
import re
import sys
import pathlib

PAGES = [
    "index.html", "about.html", "contact.html", "projects.html",
    "how-it-works.html", "labtour.html",
    "privacy-policy.html", "terms-conditions.html",
    "projects/autonomous-tracking.html",
    "projects/computer-vision-pipeline.html",
    "projects/cryogenic-electronics.html",
    "projects/embedded-flight-controller.html",
    "projects/f450-multirotor-drone.html",
    "projects/face-detection-drone.html",
    "projects/pcb-design.html",
    "projects/rural-edtech-platform.html",
]

LI_HREF = "https://www.linkedin.com/in/atharvedahima"
GH_HREF = "https://github.com/atharveeee-netizen"
LI_PATH = ("M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 "
           "5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79"
           "-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm"
           "13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7"
           "-2.777 7 2.476v6.759z")
GH_PATH = ("M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261"
           ".793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1."
           "333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 "
           "1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334"
           "-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 "
           "1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006."
           "404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 "
           "1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3."
           "293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12"
           "-12-12z")

# Plain bordered icon cells on the LEFT (warm-grey hairline, full-height square,
# 24px currentColor glyph) — same look as before, with fixed rel/target.
def cell(href, path, label):
    return (
        '<div class="navbar-item hide-mobile" style="display: flex; align-items: center; '
        'justify-content: center; height: 100%; aspect-ratio: 1; '
        'border-left: 1px solid var(--_colors---swatch--grey);">'
        f'<a href="{href}" style="color: inherit; display: flex; align-items: center; '
        f'justify-content: center;" rel="noopener" target="_blank" aria-label="{label}">'
        '<svg class="icon-24px" fill="currentColor" style="width: 24px; height: 24px;" '
        f'viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="{path}"></path></svg>'
        '</a></div>'
    )

LEFT_CELLS = cell(LI_HREF, LI_PATH, "LinkedIn") + cell(GH_HREF, GH_PATH, "GitHub")

NEW_STYLE = """<style id="navbar-clone-ref">
  /* Pixel-clone of pieterkoopt.nl nav.
     The shared template stylesheet already produces the reference look
     pixel-for-pixel (12px links, 52px square icon cells, beige@5% pills).
     So we override ONLY: bar tone, column balance, and the logo's inline
     right-margin. Sizing is left to the template so it stays responsive
     and never looks "slim". */

  /* Bar shell — match the reference exactly */
  .navbar {
    background-color: transparent !important;
    border: 1px solid #706d66 !important;
    border-radius: 0.333rem !important;
  }
  .navbar-bg {
    background-color: rgba(23, 28, 28, 0.6) !important; /* #171C1C @60% */
    border-radius: 0.267rem !important;
  }

  /* Columns: center the menu, balance the (empty) right */
  .navbar_col.is-left {
    flex: 1 1 0% !important; width: auto !important;
    display: flex !important; align-items: stretch !important;
  }
  .navbar_col.is-center {
    flex: 0 0 auto !important; width: auto !important;
    display: flex !important; align-items: stretch !important; justify-content: center !important;
  }
  .navbar_col.is-right {
    flex: 1 1 0% !important; width: auto !important;
    display: flex !important; align-items: stretch !important; justify-content: flex-end !important;
  }

  /* Logo: drop the inline 1.5rem right margin so its divider sits flush */
  .navbar_col.is-left > a.navbar_logo { margin-right: 0 !important; }
  /* Warm-grey hairline divider between every left cell (logo|sound|in|github) */
  .navbar_col.is-left > .navbar-item {
    border-left: 1px solid #706d66 !important;
    border-right: 0 !important;
  }

  /* Center menu — EXACT reference button sizing, fluid.
     Reference scales 12px@1440 -> 13.33px@1920; padding/radius/gap are em
     ratios of the font, so the whole pill scales with it. The menu carries
     the fluid font-size; the link inherits it (1em). High-specificity
     (.is-center ...) so it wins over the template's base padding. */
  .navbar_col.is-center .navbar_menu {
    display: flex !important; align-items: stretch !important; justify-content: center !important;
    /* Bigger than the reference's 13.33px cap and floored high so the buttons
       never look small, even in a narrow window. */
    font-size: clamp(13.5px, calc(9px + 0.32vw), 16px) !important;
    gap: 0.5em !important;
    padding: 0.5em 0 !important;
  }
  .navbar_col.is-center .btn-animate-chars.is-navlink {
    flex: 0 0 auto !important;
    height: 100% !important;
    font-size: 1em !important;
    padding: 0 1.5em !important;               /* 18px@1440, 20px@1920 */
    border-radius: 0.25em !important;          /* 3px@1440, 3.33px@1920 */
    color: #d4c6b9 !important;
    text-decoration: none !important;
    background-color: rgba(212, 198, 185, 0.05) !important;
    border: 1px solid rgba(112, 109, 102, 0) !important;
    display: flex !important; align-items: center !important;
    overflow: hidden !important;
    transition: background-color .4s, border-color .4s !important;
  }
  .navbar_col.is-center .btn-animate-chars.is-navlink:hover {
    background-color: rgba(212, 198, 185, 0.10) !important;
    border-color: rgba(112, 109, 102, 0.4) !important;
  }

  /* Keep the per-char hover roll intact */
  [data-button-animate-chars] {
    overflow: hidden !important; height: 1.3em !important; display: inline-block !important;
  }
</style>"""


def process(text: str):
    notes = []

    # 1) Remove the green social block from the right column.
    text, n = re.subn(
        r'<div class="navbar-cta"><div class="navbar-social">.*?</div></div>',
        '', text, flags=re.S)
    notes.append(f"green block removed: {n}")

    # 2) Restore LinkedIn + GitHub cells at the end of the left column
    #    (guard against double-insert).
    if 'linkedin.com/in/atharvedahima' not in text.split('navbar_col is-center')[0]:
        text, n = re.subn(
            r'(</div><div class="navbar_col is-center">)',
            LEFT_CELLS + r'\1', text, count=1)
        notes.append(f"left cells restored: {n}")
    else:
        notes.append("left cells already present: skip")

    # 3) Replace the nav style block with the minimal pixel-perfect version.
    text, n = re.subn(r'<style id="navbar-clone-ref">.*?</style>', NEW_STYLE, text, flags=re.S)
    notes.append(f"style block updated: {n}")

    return text, notes


def main():
    args = sys.argv[1:]
    targets = PAGES if (not args or args == ["--all"]) else args
    root = pathlib.Path(__file__).parent
    for rel in targets:
        p = root / rel
        if not p.exists():
            print(f"SKIP (missing): {rel}")
            continue
        original = p.read_text(encoding="utf-8")
        updated, notes = process(original)
        if updated == original:
            print(f"NO CHANGE: {rel}  ({'; '.join(notes)})")
            continue
        p.write_text(updated, encoding="utf-8")
        print(f"UPDATED: {rel}  ({'; '.join(notes)})")


if __name__ == "__main__":
    main()
