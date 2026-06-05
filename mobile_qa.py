#!/usr/bin/env python3
"""Mobile responsiveness checker - verifies mobile-friendly markup."""
import os, re, glob

def check_viewport():
    """Verify viewport meta tags are correct."""
    files = glob.glob('*.html') + glob.glob('projects/*.html')
    issues = []
    for fn in files:
        with open(fn, 'r', encoding='utf-8') as f:
            content = f.read()
        # Check for correct viewport
        if 'viewport' not in content:
            issues.append((fn, 'missing viewport meta'))
        # Check for user-scalable=0 (bad for accessibility)
        if 'user-scalable=0' in content:
            issues.append((fn, 'user-scalable=0 breaks zoom'))
        # Check for maximum-scale=1 (also restrictive)
        if 'maximum-scale=1.0' in content:
            issues.append((fn, 'maximum-scale=1.0 is too restrictive'))
    return issues

def check_touch_targets():
    """Find buttons/links that may be too small."""
    files = glob.glob('*.html') + glob.glob('projects/*.html')
    issues = []
    for fn in files:
        with open(fn, 'r', encoding='utf-8') as f:
            content = f.read()
        # Look for inline styles with small height/width on clickable elements
        # Buttons should be at least 44x44px
        if re.search(r'(padding|height|width):\s*([0-9]{1,2})px', content):
            matches = re.findall(r'(padding|height|width):\s*([0-9]{1,2})px', content)
            small_values = [m for m in matches if int(m[1]) < 44]
            if small_values:
                issues.append((fn, f"{len(small_values)} potential small touch targets"))
    return issues

def check_fixed_positioning():
    """Check for problematic fixed positioning."""
    files = glob.glob('*.html') + glob.glob('projects/*.html')
    issues = []
    for fn in files:
        with open(fn, 'r', encoding='utf-8') as f:
            content = f.read()
        # Fixed positioning can cause issues on mobile
        fixed_count = content.count('position:fixed')
        if fixed_count > 2:  # Allow nav, but not excessive
            issues.append((fn, f"{fixed_count} instances of position:fixed"))
    return issues

def check_font_sizes():
    """Verify base font size is readable on mobile."""
    files = glob.glob('*.html') + glob.glob('projects/*.html')
    issues = []
    for fn in files:
        with open(fn, 'r', encoding='utf-8') as f:
            content = f.read()
        # Look for font-size < 12px (too small for mobile)
        tiny_fonts = re.findall(r'font-size:\s*([0-9]{1,2})px', content)
        for size in tiny_fonts:
            if int(size) < 12:
                issues.append((fn, f"font-size:{size}px is too small for mobile"))
                break
    return issues

def check_images():
    """Check for responsive image practices."""
    files = glob.glob('*.html') + glob.glob('projects/*.html')
    issues = []
    for fn in files:
        with open(fn, 'r', encoding='utf-8') as f:
            content = f.read()
        # Check for width=100% or max-width on images
        img_count = content.count('<img ')
        responsive_imgs = len(re.findall(r'width="100%"|max-width', content))
        if img_count > 0 and responsive_imgs < img_count * 0.5:
            issues.append((fn, f"only {responsive_imgs}/{img_count} images are responsive"))
    return issues

if __name__ == '__main__':
    print("=" * 60)
    print("MOBILE RESPONSIVENESS QA")
    print("=" * 60)

    all_issues = []

    print("\n[1/5] Viewport meta tags...")
    issues = check_viewport()
    all_issues.extend(issues)
    if issues:
        for fn, desc in issues:
            print(f"  WARNING: {fn} - {desc}")
    else:
        print("  [OK] All viewports are correct")

    print("\n[2/5] Touch target sizes...")
    issues = check_touch_targets()
    all_issues.extend(issues)
    if issues:
        for fn, desc in issues:
            print(f"  INFO: {fn} - {desc}")
    else:
        print("  [OK] Touch targets appear adequate")

    print("\n[3/5] Fixed positioning...")
    issues = check_fixed_positioning()
    all_issues.extend(issues)
    if issues:
        for fn, desc in issues:
            print(f"  WARNING: {fn} - {desc}")
    else:
        print("  [OK] Fixed positioning is reasonable")

    print("\n[4/5] Font sizes...")
    issues = check_font_sizes()
    all_issues.extend(issues)
    if issues:
        for fn, desc in issues:
            print(f"  WARNING: {fn} - {desc}")
    else:
        print("  [OK] Font sizes are readable")

    print("\n[5/5] Image responsiveness...")
    issues = check_images()
    all_issues.extend(issues)
    if issues:
        for fn, desc in issues:
            print(f"  INFO: {fn} - {desc}")
    else:
        print("  [OK] Images are responsive")

    print("\n" + "=" * 60)
    warning_count = len(all_issues)
    if warning_count == 0:
        print("RESULT: Mobile-friendly site - ready for device testing")
    else:
        print(f"RESULT: {warning_count} potential mobile issues found")
    print("=" * 60)
