"""Swap background music from Beethoven (~7.4MB, loop window 80-220s) to
La Parisien by Jakub Pietras (76.8s). Because the new track is far shorter
than the old loop window, we also switch to native looping and reset the
seek clamp to the track's real length."""
import os, sys

ROOT = ["index.html", "labtour.html", "about.html", "contact.html",
        "how-it-works.html", "privacy-policy.html", "terms-conditions.html",
        "projects.html"]
PROJECTS = ["projects/" + n for n in [
    "autonomous-tracking.html", "computer-vision-pipeline.html",
    "cryogenic-electronics.html", "embedded-flight-controller.html",
    "f450-multirotor-drone.html", "face-detection-drone.html",
    "pcb-design.html", "rural-edtech-platform.html"]]
PAGES = ROOT + PROJECTS

REPLACEMENTS = [
    # (old, new, expected_count_per_file)
    ("audio/beethoven.mp3", "audio/la-parisien-jakub-pietras.mp3", 1),
    ("loop: false,", "loop: true,", 1),
    ("localStorage.getItem('soundPosition')) || 80;",
     "localStorage.getItem('soundPosition')) || 0;", 1),
    ("if(soundPosition < 80 || soundPosition > 220) soundPosition = 80;",
     "if(soundPosition < 0 || soundPosition > 76) soundPosition = 0;", 1),
]

errors = []
for p in PAGES:
    if not os.path.exists(p):
        errors.append(f"MISSING FILE: {p}")
        continue
    txt = open(p, encoding="utf-8").read()
    for old, new, want in REPLACEMENTS:
        got = txt.count(old)
        if got != want:
            errors.append(f"{p}: expected {want}x '{old[:30]}...', found {got}")

if errors:
    print("ABORT - pre-checks failed:")
    print("\n".join(errors))
    sys.exit(1)

for p in PAGES:
    txt = open(p, encoding="utf-8").read()
    for old, new, _ in REPLACEMENTS:
        txt = txt.replace(old, new)
    open(p, "w", encoding="utf-8").write(txt)
    print(f"updated {p}")

print(f"\nDone: {len(PAGES)} pages swapped to la-parisien-jakub-pietras.mp3")
