#!/usr/bin/env python3
"""Pre-deploy QA scanner - checks for Lighthouse & console issues."""
import os, re, glob

def check_missing_alts():
    """Find images without alt text."""
    files = glob.glob('*.html') + glob.glob('projects/*.html')
    issues = []
    for fn in files:
        with open(fn, 'r', encoding='utf-8') as f:
            content = f.read()
        # Simple check: count img tags and alt attributes
        img_count = content.count('<img ')
        alt_count = content.count('alt="')
        if img_count > alt_count:
            issues.append((fn, img_count - alt_count, "images missing alt text"))
    return issues

def check_missing_titles():
    """Find pages without proper title tags."""
    files = glob.glob('*.html') + glob.glob('projects/*.html')
    issues = []
    for fn in files:
        with open(fn, 'r', encoding='utf-8') as f:
            content = f.read()
        if '<title>' not in content or content.count('<title>') == 0:
            issues.append((fn, 1, "missing <title> tag"))
    return issues

def check_viewport_meta():
    """Verify viewport meta tags."""
    files = glob.glob('*.html') + glob.glob('projects/*.html')
    issues = []
    for fn in files:
        with open(fn, 'r', encoding='utf-8') as f:
            content = f.read()
        if 'viewport' not in content:
            issues.append((fn, 1, "missing viewport meta"))
    return issues

def check_color_contrast():
    """Flag potential contrast issues (low opacity text)."""
    files = glob.glob('*.html') + glob.glob('projects/*.html')
    issues = []
    for fn in files:
        with open(fn, 'r', encoding='utf-8') as f:
            content = f.read()
        # Look for opacity < 0.4 on text
        if re.search(r'opacity:\s*0\.[0-3]\d', content):
            count = len(re.findall(r'opacity:\s*0\.[0-3]\d', content))
            issues.append((fn, count, "low opacity text (may fail contrast)"))
    return issues

def check_console_errors():
    """Find code patterns that cause console errors."""
    files = glob.glob('*.html') + glob.glob('projects/*.html')
    issues = []
    for fn in files:
        with open(fn, 'r', encoding='utf-8') as f:
            content = f.read()
        # Simple pattern checks
        if 'JSON.parse' in content and 'try' not in content:
            issues.append((fn, 1, "unguarded JSON.parse (needs try/catch)"))
    return issues

def check_external_links():
    """Find external links that should have rel=noopener."""
    files = glob.glob('*.html') + glob.glob('projects/*.html')
    issues = []
    for fn in files:
        with open(fn, 'r', encoding='utf-8') as f:
            content = f.read()
        # Simple check for external links with target="_blank" but no rel
        if 'target="_blank"' in content and 'https://' in content:
            if 'rel="noopener' not in content or 'rel=\'noopener' not in content:
                # Count instances
                blank_count = content.count('target="_blank"')
                noopener_count = content.count('noopener')
                if blank_count > noopener_count:
                    issues.append((fn, blank_count - noopener_count, "external links may be missing rel=noopener"))
    return issues

def check_form_labels():
    """Find form fields without associated labels."""
    files = glob.glob('*.html') + glob.glob('projects/*.html')
    issues = []
    for fn in files:
        with open(fn, 'r', encoding='utf-8') as f:
            content = f.read()
        # Look for input/textarea without id or preceding label
        inputs = re.findall(r'<input[^>]*>', content)
        for inp in inputs:
            if 'type="hidden"' not in inp and 'type="submit"' not in inp:
                if 'id=' not in inp:
                    issues.append((fn, 1, "input field without id (label association)"))
                    break
    return issues

def run_audit():
    """Run all QA checks."""
    print("=" * 60)
    print("PRE-DEPLOY QA AUDIT")
    print("=" * 60)

    all_issues = []

    print("\n[1/6] Checking alt text on images...")
    issues = check_missing_alts()
    all_issues.extend(issues)
    if issues:
        for fn, count, desc in issues:
            print(f"  WARNING: {fn} - {count} {desc}")
    else:
        print("  [OK] All images have alt text")

    print("\n[2/6] Checking page titles...")
    issues = check_missing_titles()
    all_issues.extend(issues)
    if issues:
        for fn, count, desc in issues:
            print(f"  ERROR: {fn} - {desc}")
    else:
        print("  [OK] All pages have titles")

    print("\n[3/6] Checking viewport meta...")
    issues = check_viewport_meta()
    all_issues.extend(issues)
    if issues:
        for fn, count, desc in issues:
            print(f"  ERROR: {fn} - {desc}")
    else:
        print("  [OK] All pages have viewport meta")

    print("\n[4/6] Checking color contrast...")
    issues = check_color_contrast()
    all_issues.extend(issues)
    if issues:
        for fn, count, desc in issues:
            print(f"  WARNING: {fn} - {count} instances of {desc}")
    else:
        print("  [OK] No low-opacity text detected")

    print("\n[5/6] Checking for console errors...")
    issues = check_console_errors()
    all_issues.extend(issues)
    if issues:
        for fn, count, desc in issues:
            print(f"  WARNING: {fn} - {desc}")
    else:
        print("  [OK] No console error patterns detected")

    print("\n[6/6] Checking external links...")
    issues = check_external_links()
    all_issues.extend(issues)
    if issues:
        for fn, count, desc in issues:
            print(f"  WARNING: {fn} - {desc}")
    else:
        print("  [OK] All external links have rel=noopener")

    print("\n" + "=" * 60)
    error_count = sum(1 for _, _, d in all_issues if 'ERROR' in d.upper() or d.startswith('missing'))
    warning_count = len(all_issues) - error_count
    print(f"RESULTS: {error_count} errors, {warning_count} warnings")
    print("=" * 60)

    return error_count == 0

if __name__ == '__main__':
    success = run_audit()
    exit(0 if success else 1)
