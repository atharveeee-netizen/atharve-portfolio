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

    # Add guard after slides are queried
    # Pattern: const slides = document.querySelectorAll(".hiw-slide");
    # Add after it: if (!slides || slides.length === 0) return;

    pattern = r'(const slides = document\.querySelectorAll\("\.hiw-slide"\);)'
    replacement = r'\1\n  if (!slides || slides.length === 0) return;'

    # Check if the pattern exists and if the guard isn't already there
    if 'const slides = document.querySelectorAll(".hiw-slide");' in content:
        if 'if (!slides || slides.length === 0) return;' not in content:
            content = re.sub(pattern, replacement, content, count=1)
            print(f"[OK] Added guard to {filename}")
        else:
            print(f"[SKIP] Guard already exists in {filename}")
    else:
        print(f"[SKIP] No slide code in {filename}")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

print("\nSlide guards applied.")
