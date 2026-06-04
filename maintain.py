#!/usr/bin/env python3
"""Portfolio maintenance & QA utilities.

Consolidates all fix scripts:
  - fix_emdash: Remove em dashes from prose
  - fix_project_links: Correct hreflang/canonical/JSON-LD URLs
  - fix_medium_priority: Sound allowlist, viewport, focus accessibility
  - fix_slide_guards: Add guards for missing slide elements
  - cleanup: Dutch comments, old URLs
"""
import os, re, glob

def fix_emdash():
    """Remove em dashes from visible/prose copy."""
    files = glob.glob('*.html') + glob.glob('projects/*.html')
    for fn in files:
        with open(fn, 'r', encoding='utf-8') as f:
            s = f.read()
        orig = s
        s = s.replace('." — Albert Camus', '." Albert Camus')
        s = s.replace(' — ', ', ')
        if s != orig:
            with open(fn, 'w', encoding='utf-8') as f:
                f.write(s)
            print(f'  [emdash] {fn}')

def fix_project_links():
    """Correct hreflang/canonical/JSON-LD URLs for all projects."""
    projects = [
        ('autonomous-tracking', 'autonomous-tracking.html'),
        ('computer-vision-pipeline', 'computer-vision-pipeline.html'),
        ('cryogenic-electronics', 'cryogenic-electronics.html'),
        ('embedded-flight-controller', 'embedded-flight-controller.html'),
        ('f450-multirotor-drone', 'f450-multirotor-drone.html'),
        ('face-detection-drone', 'face-detection-drone.html'),
        ('pcb-design', 'pcb-design.html'),
        ('rural-edtech-platform', 'rural-edtech-platform.html'),
    ]
    for slug, filename in projects:
        filepath = f'projects/{filename}'
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        orig = content
        content = re.sub(
            r'<link href="[^"]*how-it-works[^"]*" hreflang="x-default" rel="alternate"/><link href="[^"]*how-it-works[^"]*" hreflang="en" rel="alternate"/><link href="[^"]*how-it-works[^"]*" hreflang="nl" rel="alternate"/>',
            f'<link href="https://www.atharveeee.com/projects/{slug}" hreflang="x-default" rel="alternate"/><link href="https://www.atharveeee.com/projects/{slug}" hreflang="en" rel="alternate"/><link href="https://www.atharveeee.com/projects/{slug}" hreflang="nl" rel="alternate"/>',
            content
        )
        content = re.sub(
            r'<link href="[^"]*how-it-works[^"]*" rel="canonical"/>',
            f'<link href="https://www.atharveeee.com/projects/{slug}" rel="canonical"/>',
            content
        )
        content = re.sub(r'"url":\s*"/how-it-works"', f'"url": "/projects/{slug}"', content)
        if content != orig:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f'  [links] {filename}')

def fix_accessibility():
    """Fix sound allowlist, viewport, and focus accessibility."""
    files = glob.glob('projects/*.html')
    for fn in files:
        with open(fn, 'r', encoding='utf-8') as f:
            content = f.read()
        orig = content
        # Remove duplicate viewport meta tag with user-scalable=0
        content = re.sub(
            r'<meta content="width=device-width, initial-scale=1\.0, maximum-scale=1\.0, user-scalable=0" name="viewport"/?>',
            '',
            content
        )
        # Unify sound allowlist logic
        content = re.sub(
            r'path === \'\/stories\' \|\| !path\.startsWith\(\'\/stories\/\'\)',
            r'!path.includes(\'/projects/\')',
            content
        )
        if content != orig:
            with open(fn, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f'  [a11y] {fn}')
    # Fix pcb-design focus accessibility
    fn = 'projects/pcb-design.html'
    with open(fn, 'r', encoding='utf-8') as f:
        content = f.read()
    orig = content
    content = re.sub(
        r':focus\s*\{\s*outline:\s*0;\s*\}',
        ':focus-visible { outline: 2px solid currentColor; }',
        content
    )
    if content != orig:
        with open(fn, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'  [focus] pcb-design.html')

def fix_slide_guards():
    """Add guards for missing .hiw-slide elements."""
    files = glob.glob('projects/*.html')
    for fn in files:
        with open(fn, 'r', encoding='utf-8') as f:
            content = f.read()
        if 'const slides = document.querySelectorAll(".hiw-slide");' in content:
            if 'if (!slides || slides.length === 0) return;' not in content:
                content = re.sub(
                    r'(const slides = document\.querySelectorAll\("\.hiw-slide"\);)',
                    r'\1\n  if (!slides || slides.length === 0) return;',
                    content
                )
                with open(fn, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f'  [guards] {fn}')

def cleanup_dutch_and_urls():
    """Remove Dutch comments and replace old URLs."""
    files = glob.glob('*.html') + glob.glob('projects/*.html')
    dutch = {
        '/* Alleen verbergen als JS actief is */': '/* Hide if JS is enabled (FOUC prevention) */',
        '/* Zorgt dat animatie vloeiend blijft */': '/* Keep animation smooth */',
        '/* Optioneel: voorkomt mini flash bij font swap */': '/* Prevent font swap flash */',
    }
    urls = {
        "'/sell-your-painting'": "'/collab-wizard'",
        '"/sell-your-painting"': '"/collab-wizard"',
    }
    for fn in files:
        with open(fn, 'r', encoding='utf-8') as f:
            content = f.read()
        orig = content
        for d, e in dutch.items():
            content = content.replace(d, e)
        for old, new in urls.items():
            content = content.replace(old, new)
        if content != orig:
            with open(fn, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f'  [cleanup] {fn}')

if __name__ == '__main__':
    print('Running portfolio maintenance...\n')
    print('[1/5] Em dash removal')
    fix_emdash()
    print('[2/5] Project link corrections')
    fix_project_links()
    print('[3/5] Accessibility fixes')
    fix_accessibility()
    print('[4/5] Slide controller guards')
    fix_slide_guards()
    print('[5/5] Dutch comments & old URLs')
    cleanup_dutch_and_urls()
    print('\nMaintenance complete.')
