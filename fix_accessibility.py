#!/usr/bin/env python3
"""Fix accessibility issues: alt text and external link security."""
import os, re, glob

def fix_alt_text():
    """Add alt text to images missing it."""
    files = glob.glob('*.html') + glob.glob('projects/*.html')
    for fn in files:
        with open(fn, 'r', encoding='utf-8') as f:
            content = f.read()
        orig = content
        # Add alt="" to decorative background images (ashu-dither, project-placeholder)
        content = re.sub(
            r'<img\s+src="[^"]*ashu-dither\.png"([^>]*)/>',
            r'<img src="assets/img/ashu-dither.png"\1 alt=""/>',
            content
        )
        content = re.sub(
            r'<img\s+src="[^"]*project-placeholder\.png"([^>]*)/>',
            r'<img src="assets/img/project-placeholder.png"\1 alt=""/>',
            content
        )
        if content != orig:
            with open(fn, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"[ALT] Fixed {fn}")

def fix_external_links():
    """Add rel=noopener to external target="_blank" links."""
    files = glob.glob('*.html') + glob.glob('projects/*.html')
    for fn in files:
        with open(fn, 'r', encoding='utf-8') as f:
            content = f.read()
        orig = content
        # Find <a> tags with target="_blank" and https://, add rel=noopener if missing
        content = re.sub(
            r'<a\s+([^>]*href="https?://[^"]*"[^>]*)target="_blank"([^>]*)>',
            lambda m: '<a ' + m.group(1) + ('rel="noopener ' if 'rel=' not in m.group(1) + m.group(2) else '') +
                      ('noopener ' if 'noopener' not in (m.group(1) + m.group(2)) else '') +
                      'target="_blank"' + m.group(2) + '>',
            content
        )
        # Simpler approach: add rel attribute if target="_blank" exists but rel doesn't
        if 'target="_blank"' in content and 'https://' in content:
            # For WhatsApp and Instagram links specifically
            content = content.replace(
                'href="https://wa.me/',
                'rel="noopener" href="https://wa.me/'
            )
            content = content.replace(
                'href="https://www.instagram.com/',
                'rel="noopener" href="https://www.instagram.com/'
            )
        if content != orig:
            with open(fn, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"[LINKS] Fixed {fn}")

if __name__ == '__main__':
    print("Fixing accessibility issues...\n")
    print("[1/2] Adding alt text...")
    fix_alt_text()
    print("\n[2/2] Adding rel=noopener...")
    fix_external_links()
    print("\nDone.")
