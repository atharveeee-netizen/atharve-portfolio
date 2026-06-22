"""Turn every project "view story" detail page into a "Coming soon" placeholder.

Per the brief: the words "Coming Soon" appear exactly ONCE (the page title);
every other field in the story area is filled with en-dashes (U+2013). Layout,
nav (back link + CTA), head/meta, footer and scripts are all left untouched.

Works by swapping the whole `.pd-inner` block (pd-inner -> closing </section>)
for a uniform placeholder. Idempotent: re-running matches the placeholder and
rewrites it identically. Original story copy is preserved in git history.
"""
import glob
import re

EN = "–"          # en dash
ARROW = "←"       # left arrow used by the existing back/CTA links


def dashes(n):
    return " ".join([EN] * n)


PD_INNER = (
    '<div class="pd-inner">'
    f'<a class="pd-back" href="../projects.html">{ARROW} All projects</a>'
    f'<div class="pd-eyebrow">{EN}</div>'
    '<h1 class="heading-s pd-title">Coming Soon</h1>'
    f'<p class="pd-hook"><span class="ital">{dashes(7)}</span></p>'
    '<div class="pd-body">'
    f'<p class="paragraph-l">{dashes(30)}</p>'
    f'<p class="paragraph-l">{dashes(22)}</p>'
    f'<p class="paragraph-l">{dashes(34)}</p>'
    '</div>'
    '<div class="pd-meta">'
    f'<div class="pd-meta-line"><div class="pd-label">{EN}</div><div class="pd-value">{dashes(6)}</div></div>'
    f'<div class="pd-meta-line"><div class="pd-label">{EN}</div><div class="pd-value">{dashes(4)}</div></div>'
    '</div>'
    f'<div class="pd-quote">{dashes(9)}<span class="cite">{EN}</span></div>'
    f'<div class="pd-cta"><a class="pd-btn" href="../projects.html">{ARROW} All projects</a></div>'
    '</div></div></div></section>'
)

pattern = re.compile(r'<div class="pd-inner">.*?</section>', re.DOTALL)

for path in sorted(glob.glob("projects/*.html")):
    with open(path, encoding="utf-8") as fh:
        src = fh.read()
    new, n = pattern.subn(PD_INNER, src, count=1)
    if n == 0:
        print("NO MATCH:", path)
        continue
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write(new)
    print("updated:", path)
