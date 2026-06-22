#!/usr/bin/env python3
"""Inject the cloned pieterkoopt button-hover engine into every content page.

Adds  <script defer src="(../)assets/btn-hover.js"></script>  right before the
closing </body> of each real page. Idempotent: re-running skips pages that
already reference the script. Backups, the dist/ build output, and the logo
fragment are left untouched.
"""
import pathlib
import re

ROOT = pathlib.Path(__file__).parent
TAG = 'assets/btn-hover.js'

# real, navigable pages only
ROOT_PAGES = [p for p in ROOT.glob('*.html')
              if '.backup' not in p.name and p.name != '_walogo.html']
PROJECT_PAGES = sorted((ROOT / 'projects').glob('*.html'))

CLOSE = re.compile(r'</body>', re.IGNORECASE)


def inject(path: pathlib.Path, prefix: str) -> str:
    html = path.read_text(encoding='utf-8')
    if TAG in html:
        return 'skip (already wired)'
    if not CLOSE.search(html):
        return 'SKIP (no </body>)'
    snippet = '<script defer src="%sassets/btn-hover.js"></script>\n' % prefix
    html = CLOSE.sub(snippet + '</body>', html, count=1)
    path.write_text(html, encoding='utf-8')
    return 'wired'


def main():
    for p in ROOT_PAGES:
        print(f'{p.name:32} {inject(p, "")}')
    for p in PROJECT_PAGES:
        print(f'projects/{p.name:22} {inject(p, "../")}')


if __name__ == '__main__':
    main()
