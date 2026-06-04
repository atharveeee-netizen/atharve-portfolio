#!/usr/bin/env python3
import os
import re

# Map filenames to their URL slugs
projects = {
    'autonomous-tracking.html': 'autonomous-tracking',
    'computer-vision-pipeline.html': 'computer-vision-pipeline',
    'cryogenic-electronics.html': 'cryogenic-electronics',
    'embedded-flight-controller.html': 'embedded-flight-controller',
    'f450-multirotor-drone.html': 'f450-multirotor-drone',
    'face-detection-drone.html': 'face-detection-drone',
    'pcb-design.html': 'pcb-design',
    'rural-edtech-platform.html': 'rural-edtech-platform',
}

for filename, slug in projects.items():
    filepath = f'projects/{filename}'

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Fix hreflang tags pointing to /how-it-works to correct slug
    # Original pattern: hreflang tags with /how-it-works
    # We need to replace these with the correct project slug

    # Replace hreflang x-default, en, nl tags
    original_hreflang = r'<link href="[^"]*how-it-works[^"]*" hreflang="x-default" rel="alternate"/><link href="[^"]*how-it-works[^"]*" hreflang="en" rel="alternate"/><link href="[^"]*how-it-works[^"]*" hreflang="nl" rel="alternate"/>'
    new_hreflang = f'<link href="https://www.atharveeee.com/projects/{slug}" hreflang="x-default" rel="alternate"/><link href="https://www.atharveeee.com/projects/{slug}" hreflang="en" rel="alternate"/><link href="https://www.atharveeee.com/projects/{slug}" hreflang="nl" rel="alternate"/>'

    # Try to match and replace
    if 'hreflang="x-default"' in content and 'how-it-works' in content:
        content = re.sub(
            r'<link href="[^"]*how-it-works[^"]*" hreflang="x-default" rel="alternate"/><link href="[^"]*how-it-works[^"]*" hreflang="en" rel="alternate"/><link href="[^"]*how-it-works[^"]*" hreflang="nl" rel="alternate"/>',
            new_hreflang,
            content
        )

    # Replace canonical link
    original_canonical = r'<link href="[^"]*how-it-works[^"]*" rel="canonical"/>'
    new_canonical = f'<link href="https://www.atharveeee.com/projects/{slug}" rel="canonical"/>'
    content = re.sub(original_canonical, new_canonical, content)

    # Replace JSON-LD @url for /how-it-works pattern
    # Match:  "url": "/how-it-works" (with possible variations in spacing)
    original_url_pattern = r'"url":\s*"/how-it-works"'
    new_url = f'"url": "/projects/{slug}"'
    content = re.sub(original_url_pattern, new_url, content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"[OK] Fixed {filename}")

print("\nAll project links fixed.")
