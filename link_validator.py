#!/usr/bin/env python3
"""Link validator - checks for broken internal links."""
import os, re, glob

def get_all_pages():
    """Get list of all HTML pages."""
    files = glob.glob('*.html') + glob.glob('projects/*.html')
    return {f.replace('\\', '/'): True for f in files}

def extract_links(content):
    """Extract all href links from HTML."""
    # Find all href="..." patterns
    pattern = r'href=["\']([^"\']+)["\']'
    matches = re.findall(pattern, content)
    return matches

def validate_links():
    """Check for broken internal links."""
    pages = get_all_pages()
    issues = []

    for fn in pages.keys():
        with open(fn, 'r', encoding='utf-8') as f:
            content = f.read()

        links = extract_links(content)
        for link in links:
            # Skip external links, anchors, and special protocols
            if link.startswith(('http://', 'https://', 'mailto:', 'tel:', 'whatsapp:', '#', 'data:', '/')):
                continue

            # Relative link - check if file exists
            if link.startswith('./') or link.startswith('../'):
                # Resolve relative path
                base_dir = os.path.dirname(fn)
                resolved = os.path.normpath(os.path.join(base_dir, link))
                resolved = resolved.replace('\\', '/')

                if not os.path.exists(resolved):
                    issues.append((fn, link, resolved))
            else:
                # Simple filename link
                if link not in pages and not os.path.exists(link):
                    # Check with .html added
                    if link + '.html' not in pages:
                        issues.append((fn, link, 'file not found'))

    return issues

if __name__ == '__main__':
    print("=" * 60)
    print("LINK VALIDATION REPORT")
    print("=" * 60)

    issues = validate_links()

    if issues:
        print(f"\nFound {len(issues)} potential broken links:\n")
        for fn, link, details in issues:
            print(f"  {fn}")
            print(f"    -> {link} ({details})\n")
        print("=" * 60)
        print(f"RESULT: {len(issues)} broken links found")
        exit(1)
    else:
        print("\n[OK] All internal links are valid")
        print("=" * 60)
        exit(0)
