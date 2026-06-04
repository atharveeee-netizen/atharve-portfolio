#!/usr/bin/env python3
import os
import re

projects = [
    'autonomous-tracking.html',
    'computer-vision-pipeline.html',
    'cryogenic-electronics.html',
    'embedded-flight-controller.html',
    'f450-multirotor-drone.html',
    'face-detection-drone.html',
    'pcb-design.html',
    'rural-edtech-platform.html',
]

for filename in projects:
    filepath = f'projects/{filename}'

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Remove duplicate viewport meta tag with user-scalable=0
    # Pattern: <meta content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=0" name="viewport"/>
    content = re.sub(
        r'<meta content="width=device-width, initial-scale=1\.0, maximum-scale=1\.0, user-scalable=0" name="viewport"/?>',
        '',
        content
    )

    # 2. Unify sound allowlist logic
    # Replace the old pattern that checks for /stories
    content = re.sub(
        r'path === \'\/stories\' \|\| !path\.startsWith\(\'\/stories\/\'\)',
        r'!path.includes(\'/projects/\')',
        content
    )

    # 3. Fix pcb-design.html focus accessibility
    if filename == 'pcb-design.html':
        # Replace global :focus { outline: 0; } with :focus-visible
        content = re.sub(
            r':focus\s*\{\s*outline:\s*0;\s*\}',
            ':focus-visible { outline: 2px solid currentColor; }',
            content
        )

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"[OK] Fixed {filename}")

print("\nAll medium-priority fixes applied.")
