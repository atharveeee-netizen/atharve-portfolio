"""Projects gallery: drop per-frame captions + reframe as "Upcoming projects".

- Removes the 8 `.gs_content` caption headings (project name + role/year),
  keeping each frame's "View story" button.
- Retitles the gallery hero and rewrites the one supporting line that still
  referenced the now-hidden stories.
"""
import re

f = "projects.html"
s = open(f, encoding="utf-8").read()

# 1) Strip the per-frame captions (uniquely tagged with pointer-events-off).
s, n = re.subn(
    r'<h2 class="heading-wrapper pointer-events-off">.*?</h2>', "", s, flags=re.DOTALL
)

# 2) Retitle the hero, keeping the italic-second-line rhythm.
s = s.replace(
    '<h1 class="heading-s">Every project has<br/><span class="ital">a signal.</span></h1>',
    '<h1 class="heading-s">Upcoming<br/><span class="ital">projects.</span></h1>',
)

# 3) Replace the supporting line (no captions now; stories are "Coming soon").
s = s.replace(
    "Five builds, framed like work worth keeping. Drones, vision, boards, "
    "and one cold idea I can't put down. Click a frame for the full story.",
    "New builds, still on the bench. The frames go up first; the stories "
    "follow. Open one to see what's coming.",
)

open(f, "w", encoding="utf-8", newline="").write(s)
print("captions removed:", n)
