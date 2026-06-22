#!/usr/bin/env python3
"""
fix_navbar_clone.py
Clone the pieterkoopt.nl navbar spacing/look onto our nav, faithfully.

Reference values measured live at 1440px (root font-size = 16px):
  - bar:        transparent; .navbar-bg = #171C1C @60%; border 1px #706D66; radius .333rem
  - dividers:   1px solid #706D66 (warm grey, == --_colors---swatch--grey)
  - text:       #D4C6B9 (beige, == --_colors---swatch--beige)
  - menu link:  gap .333rem, padding 0 1rem, bg beige@5%, radius .167rem, hover lighten
  - green CTA:  #7A8B69 with #171C1C glyphs, radius .167rem

Change from reference: the right green compartment holds the LinkedIn + GitHub
icons (moved off the left) instead of "Request offer". Logo + sound stay on left.

Usage:
  python fix_navbar_clone.py index.html        # one file
  python fix_navbar_clone.py --all             # every page
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

NEW_STYLE = """<style id="navbar-clone-ref">
  /* === Navbar: faithful clone of pieterkoopt.nl (measured @1440, root 16px) ===
     Replaces the old navbar-flex-override + navbar-pieterkoopt-clone blocks. */

  /* Bar shell: translucent dark fill + warm-grey hairline border */
  .navbar {
    background-color: transparent !important;
    border: 1px solid #706d66 !important;
    border-radius: 0.333rem !important;
  }
  .navbar-bg {
    background-color: rgba(23, 28, 28, 0.6) !important; /* #171C1C @60% */
    border-radius: 0.267rem !important;
  }

  /* Columns: keep the menu centered, push the CTA to the far right */
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
    padding-right: 0.333rem !important;
  }

  /* Logo compartment */
  .navbar_col.is-left > a.navbar_logo {
    margin-right: 0 !important;
    padding: 0 1.333rem !important;
    display: flex !important; align-items: center !important;
  }
  /* Sound cell: square, divider on its left (warm grey) */
  .navbar_col.is-left > .navbar-item.is-sound {
    width: 2.875rem !important;          /* 46px */
    aspect-ratio: 1 / 1 !important;
    border-left: 1px solid #706d66 !important;
    border-right: 0 !important;
  }

  /* Center menu: tight pills */
  .navbar_menu {
    display: flex !important; align-items: stretch !important; justify-content: center !important;
    gap: 0.333rem !important;
    padding: 0.333rem 0 !important;
    width: 100% !important;
  }
  .btn-animate-chars.is-navlink {
    flex: 0 0 auto !important;
    height: 100% !important;
    padding: 0 1rem !important;
    font-size: 0.667rem !important;
    color: #d4c6b9 !important;
    background-color: rgba(212, 198, 185, 0.05) !important;
    border: 1px solid rgba(112, 109, 102, 0) !important;
    border-radius: 0.167rem !important;
    display: flex !important; align-items: center !important;
    overflow: hidden !important;
    transition: background-color .4s, border-color .4s !important;
  }
  .btn-animate-chars.is-navlink:hover {
    background-color: rgba(212, 198, 185, 0.10) !important;
    border-color: rgba(112, 109, 102, 0.4) !important;
  }
  [data-button-animate-chars] {
    overflow: hidden !important; height: 1.3em !important; display: inline-block !important;
  }

  /* Right compartment: green social cluster (clones the reference green button) */
  .navbar_col.is-right .navbar-cta {
    display: flex !important; align-items: stretch !important;
    padding: 0.333rem 0 !important;
  }
  .navbar-social {
    display: flex !important; align-items: stretch !important;
    background-color: #7a8b69 !important;      /* reference green */
    border-radius: 0.167rem !important;
    overflow: hidden !important;
  }
  .navbar-social a {
    display: flex !important; align-items: center !important; justify-content: center !important;
    width: 2.625rem !important;                /* ~42px */
    color: #171c1c !important;                 /* dark glyph on green */
    transition: background-color .35s ease !important;
  }
  .navbar-social a:hover { background-color: #6c7d5c !important; }
  .navbar-social a + a { border-left: 1px solid rgba(23, 28, 28, 0.18) !important; }
  .navbar-social svg { width: 1.125rem !important; height: 1.125rem !important; }
</style>"""

SOCIAL = (
    '<div class="navbar-cta"><div class="navbar-social">'
    f'<a href="{LI_HREF}" target="_blank" rel="noopener" aria-label="LinkedIn">'
    f'<svg viewBox="0 0 24 24" fill="currentColor" xmlns="http://www.w3.org/2000/svg"><path d="{LI_PATH}"></path></svg></a>'
    f'<a href="{GH_HREF}" target="_blank" rel="noopener" aria-label="GitHub">'
    f'<svg viewBox="0 0 24 24" fill="currentColor" xmlns="http://www.w3.org/2000/svg"><path d="{GH_PATH}"></path></svg></a>'
    '</div></div>'
)


def process(text: str) -> tuple[str, list[str]]:
    notes = []

    # 1) Replace the flex-override block with the new combined block.
    text, n = re.subn(r'<style id="navbar-flex-override">.*?</style>', NEW_STYLE, text, flags=re.S)
    notes.append(f"flex-override block replaced: {n}")

    # 2) Remove the old pieterkoopt-clone block.
    text, n = re.subn(r'<style id="navbar-pieterkoopt-clone">.*?</style>\s*', '', text, flags=re.S)
    notes.append(f"pieterkoopt-clone block removed: {n}")

    # 3) Remove the LinkedIn cell from the left column.
    text, n = re.subn(
        r'<div class="navbar-item hide-mobile"[^>]*>\s*<a href="https://www\.linkedin\.com/in/atharvedahima".*?</a>\s*</div>',
        '', text, flags=re.S)
    notes.append(f"linkedin cell removed: {n}")

    # 4) Remove the GitHub cell from the left column.
    text, n = re.subn(
        r'<div class="navbar-item hide-mobile"[^>]*>\s*<a href="https://github\.com/atharveeee-netizen".*?</a>\s*</div>',
        '', text, flags=re.S)
    notes.append(f"github cell removed: {n}")

    # 5) Insert the green social block as the first child of the right column.
    text, n = re.subn(r'(<div class="navbar_col is-right">)', r'\1' + SOCIAL, text, count=1)
    notes.append(f"social block inserted: {n}")

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
