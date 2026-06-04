#!/usr/bin/env python3
"""Clean up Dutch comments and old art-dealer URLs across all HTML files."""
import os
import glob

files = glob.glob('*.html') + glob.glob('projects/*.html')

dutch_replacements = {
    '/* Alleen verbergen als JS actief is */': '/* Hide if JS is enabled (FOUC prevention) */',
    '/* Zorgt dat animatie vloeiend blijft */': '/* Keep animation smooth *//',
    '/* Optioneel: voorkomt mini flash bij font swap */': '/* Prevent font swap flash *//',
}

url_replacements = {
    "'/sell-your-painting'": "'/collab-wizard'",
    '"/sell-your-painting"': '"/collab-wizard"',
}

for fn in files:
    with open(fn, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # Replace Dutch comments
    for dutch, english in dutch_replacements.items():
        content = content.replace(dutch, english)

    # Replace old URLs
    for old_url, new_url in url_replacements.items():
        content = content.replace(old_url, new_url)

    if content != original:
        with open(fn, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'[OK] Cleaned {fn}')
    else:
        print(f'[SKIP] No changes needed in {fn}')

print('\nCleanup complete.')
