#!/usr/bin/env python3
"""Fix mobile responsiveness issues - viewport meta tags."""
import os, re, glob

def fix_viewport_meta():
    """Remove user-scalable=0 and overly restrictive maximum-scale."""
    files = glob.glob('*.html') + glob.glob('projects/*.html')
    for fn in files:
        with open(fn, 'r', encoding='utf-8') as f:
            content = f.read()
        orig = content

        # Replace restrictive viewport with accessible one
        # Old: width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=0
        # New: width=device-width, initial-scale=1
        content = re.sub(
            r'<meta\s+content="width=device-width,\s*initial-scale=1\.0,\s*maximum-scale=1\.0,\s*user-scalable=0"\s+name="viewport"\s*/?>\s*',
            '<meta content="width=device-width, initial-scale=1" name="viewport"/>',
            content
        )

        # Also fix variations
        content = re.sub(
            r'<meta\s+name="viewport"\s+content="width=device-width,\s*initial-scale=1\.0,\s*maximum-scale=1\.0,\s*user-scalable=0"\s*/?>\s*',
            '<meta content="width=device-width, initial-scale=1" name="viewport"/>',
            content
        )

        if content != orig:
            with open(fn, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"[VIEWPORT] Fixed {fn}")
        else:
            print(f"[SKIP] No restrictive viewport in {fn}")

if __name__ == '__main__':
    print("Fixing mobile accessibility issues...\n")
    print("[1/1] Updating viewport meta tags...")
    fix_viewport_meta()
    print("\nDone.")
