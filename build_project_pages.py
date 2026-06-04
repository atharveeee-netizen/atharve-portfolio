# -*- coding: utf-8 -*-
"""Generate projects/<slug>.html detail pages from the how-it-works.html template.

Clones the full page shell (head, nav, footer, scripts, ScrollSmoother, audio),
rewrites relative asset/link paths to ../ for the subfolder, and swaps the single
content section for an on-brand project-detail layout carrying the VAEL case-study copy.

[bracket] tokens are real placeholders the user must replace with specifics; they are
wrapped in <span class="pd-todo"> so they are scannable on the page.
"""
import os, re

BASE_FILE = "how-it-works.html"
OUT_DIR = "projects"

OLD_TITLE = "<title>How It Works, atharveeee</title>"
OLD_DESC = ("From brief to board to firmware. Share your build, get a reply within 48 hours, "
            "then watch it get made and tested until it holds.")
OLD_OGTITLE = "How Working With atharveeee Works"

SECTION_START = '<div class="main-wrapper" id="smooth-content">'
SECTION_END = '<footer class="footer'

SCOPED_CSS = """
<style>
.project-detail .pd-inner{max-width:50rem;margin:0}
.project-detail .pd-back{display:inline-block;margin-bottom:3rem;font-size:.95em;letter-spacing:.04em;text-decoration:none;color:inherit;opacity:.55;transition:opacity .2s}
.project-detail .pd-back:hover{opacity:1}
.project-detail .pd-eyebrow{text-transform:uppercase;letter-spacing:.2em;font-size:.78em;opacity:.6;margin-bottom:1.25rem}
.project-detail .pd-title{margin:0 0 2.5rem}
.project-detail .pd-frame{margin:0 0 3rem;border:1px solid rgba(212,198,185,.16);overflow:hidden}
.project-detail .pd-img{display:block;width:100%;height:auto}
.project-detail .pd-hook{font-size:1.7em;line-height:1.32;font-style:italic;margin:0 0 2.5rem;max-width:24ch;opacity:.92}
.project-detail .pd-body p{margin:0 0 1.4rem;opacity:.85}
.project-detail .pd-body p:last-child{margin-bottom:0}
.project-detail .pd-meta{margin-top:3rem}
.project-detail .pd-meta-line{display:flex;gap:1.5rem;padding:1.1rem 0;border-top:1px solid rgba(212,198,185,.16)}
.project-detail .pd-meta-line:last-child{border-bottom:1px solid rgba(212,198,185,.16)}
.project-detail .pd-label{flex:0 0 9rem;text-transform:uppercase;letter-spacing:.14em;font-size:.72em;opacity:.5;padding-top:.3em}
.project-detail .pd-value{flex:1;opacity:.9}
.project-detail .pd-todo{font-style:italic;color:#7a8b69;border-bottom:1px dashed rgba(122,139,105,.7);padding:0 .12em}
.project-detail .pd-cta{display:flex;gap:1rem;flex-wrap:wrap;margin-top:3.5rem}
.project-detail .pd-btn{display:inline-block;padding:.85em 1.6em;border:1px solid rgba(212,198,185,.4);border-radius:2em;text-decoration:none;color:inherit;font-size:.9em;letter-spacing:.03em;transition:background .2s,color .2s,border-color .2s}
.project-detail .pd-btn:hover{border-color:rgba(212,198,185,.9)}
.project-detail .pd-btn-primary{background:#7a8b69;border-color:#7a8b69;color:#171c1c}
.project-detail .pd-btn-primary:hover{background:#8a9b79;border-color:#8a9b79}
@media screen and (max-width:479px){
.project-detail .pd-meta-line{flex-direction:column;gap:.4rem}
.project-detail .pd-label{flex:none}
.project-detail .pd-hook{font-size:1.4em}
}
</style>
"""

IMG = "uploads/draw-1b950292-d605-4273-a1df-5d8fb696315b.png"

PROJECTS = [
    dict(
        slug="f450-multirotor-drone", title="F450 Multirotor Drone",
        cat="Lead Developer · 2025",
        desc="My first machine that chose to stay up. Built an F450 multirotor from the frame out, crashed it, and learned why a drone flies.",
        hook="My first machine that chose to stay up.",
        body=[
            "I didn't want a drone. I wanted to know why a drone flies. So I built one from the frame out: F450 airframe, brushless motors, ESCs, and a flight controller I configured by hand.",
            "The first three flights ended in the dirt. Props turning the wrong way, then a control loop so twitchy the thing shook itself out of the air. I fixed the motor mapping, calmed the gains, and it held a hover.",
            "Every drone I've built since flies on what this one taught me.",
        ],
        stack="F450 · [Pixhawk] · brushless motors + ESCs · [radio TX/RX]",
        change="Log telemetry from flight one. I learned half of this blind.",
    ),
    dict(
        slug="pcb-design", title="PCB Design",
        cat="Altium Designer · 2025",
        desc="A board is an argument about where electrons are allowed to go. Schematic, layout, and routing in Altium.",
        hook="A board is an argument about where electrons are allowed to go.",
        body=[
            "Breadboards lie. They work until they don't, and never tell you why. So I moved to real boards in Altium: schematic, layout, routing power and signal on their own terms.",
            "[Board's purpose, e.g. a power-distribution / sensor-breakout board for the drone]. Rev 1 had [a ground issue / footprint mismatch] that bit me on bring-up. Rev 2 came up clean.",
        ],
        stack="Altium Designer · [JLCPCB fab]",
        change="Test points everywhere. Debugging a board without them is punishment.",
    ),
    dict(
        slug="face-detection-drone", title="Face Detection Drone",
        cat="Technovation State Finalist · 2026",
        desc="A drone that looks back. Face-tracking flight on a hobby budget with OpenCV and ArduPilot. Technovation State Finalist 2026.",
        hook="A drone that looks back.",
        body=[
            "Commercial tracking drones cost lakhs and run closed firmware. I wanted to prove face-tracking flight was possible on a hobby budget with open tools.",
            "Vision ran on a [Raspberry Pi] doing [OpenCV] face detection and fed offset corrections to the flight controller over [MAVLink], so the drone yawed to keep a face centered. The first build chased every frame and oscillated hard.",
            "I added a deadzone and smoothing, dropped detection to [~10 fps] so flight control wasn't starved, and it settled. Held a moving face in frame at [~3 m]. State Finalist, Technovation 2026.",
        ],
        stack="[Raspberry Pi] · OpenCV · ArduPilot · MAVLink · [Pixhawk]",
        change="Swap the cascade for a lightweight CNN for harder angles.",
    ),
    dict(
        slug="rural-edtech-platform", title="Rural EdTech Platform",
        cat="Smart India Hackathon · 2025",
        desc="Not every hard problem is made of silicon. An offline-first learning platform built for Smart India Hackathon 2025.",
        hook="Not every hard problem is made of silicon.",
        body=[
            "Built under hackathon pressure for Smart India Hackathon 2025. The problem: [learning access in low-connectivity rural areas]. We built [an offline-first platform/app that ...].",
            "The constraint that shaped everything: [intermittent or no internet]. It had to work offline and sync when a connection appeared. [Result / placement].",
        ],
        stack="[fill in: web / Python / etc]",
        change="[...]",
    ),
    dict(
        slug="cryogenic-electronics", title="Cryogenic Electronics",
        cat="Research Interest · Ongoing",
        desc="How circuits behave once you take the heat away. Cryogenic electronics research, the ground floor of quantum hardware.",
        hook="How circuits behave once you take the heat away.",
        body=[
            "This one isn't finished, and that's the point.",
            "Cool a circuit toward absolute zero and the noise floor drops: thermal noise scales with temperature, so the colder it gets, the more of the real signal you can hear. That behavior is the ground floor of quantum hardware.",
            "I'm studying [how specific components / amplifiers / semiconductors behave at cryogenic temperatures] and working out what I can build toward. A frontier, not a gap.",
        ],
        openq="[...]",
    ),
    dict(
        slug="autonomous-tracking", title="Autonomous Tracking",
        cat="ArduPilot · OpenCV · 2025",
        desc="Teaching a machine to follow what it was never told to expect. Real-time tracking with ArduPilot and OpenCV.",
        hook="Teaching a machine to follow what it was never told to expect.",
        body=[
            "Tracking a fixed mark is easy. Following something that moves unpredictably is not. I paired ArduPilot with an OpenCV pipeline so the system could lock onto [a target] and adjust in real time. No waypoints, no script.",
            "The hard part: [latency between detection and control / holding the lock when speed changed]. [Result].",
        ],
        stack="ArduPilot · OpenCV · [Python]",
        change="[...]",
    ),
    dict(
        slug="embedded-flight-controller", title="Embedded Flight Controller",
        cat="Embedded Developer · 2025",
        desc="The part of the drone that decides it wants to live. IMU, control loop, and motors on bare metal.",
        hook="The part of the drone that decides it wants to live.",
        body=[
            "The flight controller is where physics meets firmware: read the IMU, run the loop, drive the motors, [hundreds of times a second].",
            "I worked close to the metal on [an STM32 / ESP32], handling [sensor reads and the stabilization loop]. [What broke: timing / sensor-fusion drift / a loop running too slow]. [The fix]. [Result: stable control].",
        ],
        stack="[STM32 / ESP32] · C/C++ · [IMU]",
        change="[...]",
    ),
    dict(
        slug="computer-vision-pipeline", title="Computer Vision Pipeline",
        cat="Python · 2026",
        desc="Most of seeing is deciding what to ignore. A real-time computer vision pipeline in Python.",
        hook="Most of seeing is deciding what to ignore.",
        body=[
            "A vision system spends most of its effort throwing data away: which pixels matter, which are noise.",
            "I built a pipeline in Python that [took raw frames, ran detection/tracking, and output ...] for [the use case]. The constraint: [real-time on limited hardware]. [The bottleneck and how I fixed it]. [Result].",
        ],
        stack="Python · OpenCV · [NumPy / model]",
        change="[...]",
    ),
]


def wrap_todo(text):
    return re.sub(r"\[([^\]]+)\]", r'<span class="pd-todo">[\1]</span>', text)


def rewrite_paths(html):
    skip = re.compile(r"^(https?:|//|mailto:|tel:|#|data:|\.\./|javascript:)")
    def repl(m):
        attr, val = m.group(1), m.group(2)
        if skip.match(val):
            return m.group(0)
        return '%s="../%s"' % (attr, val)
    return re.sub(r'\b(href|src)="([^"]+)"', repl, html)


def rewrite_quoted_assets(html):
    """Prefix ../ to JS-resolved relative asset paths (e.g. Howler audio src).

    Run AFTER rewrite_paths: attribute paths are already ../-prefixed, so the
    quote is no longer immediately followed by a bare asset dir. This pass only
    catches quoted paths still starting with a known asset dir, i.e. the inline
    <script> audio sources that browsers resolve against the page URL."""
    return re.sub(r"([\"'])((?:assets|uploads|css|js|fonts)/)", r"\1../\2", html)


def build_section(p):
    body_html = "".join("<p class=\"paragraph-l\">%s</p>" % wrap_todo(par) for par in p["body"])
    meta_lines = []
    if p.get("stack"):
        meta_lines.append(('Stack', p["stack"]))
    if p.get("change"):
        meta_lines.append(("What I'd change", p["change"]))
    if p.get("openq"):
        meta_lines.append(("Open question I'm chasing", p["openq"]))
    meta_html = ""
    if meta_lines:
        rows = "".join(
            '<div class="pd-meta-line"><div class="pd-label">%s</div><div class="pd-value">%s</div></div>'
            % (label, wrap_todo(val)) for label, val in meta_lines
        )
        meta_html = '<div class="pd-meta">%s</div>' % rows

    return (
        SCOPED_CSS
        + '<section class="section_intro project-detail" nav-scroll-trigger="">'
        + '<div class="section-padding-128px"><div class="padding-global">'
        + '<div class="pd-inner">'
        + '<a class="pd-back" href="../projects.html">← All projects</a>'
        + '<div class="pd-eyebrow">%s</div>' % p["cat"]
        + '<h1 class="heading-s pd-title">%s</h1>' % p["title"]
        + '<!-- Project image (add a real photo): <div class="pd-frame"><img class="pd-img" alt="%s" loading="eager" src="../uploads/REPLACE.png"/></div> -->' % p["title"]
        + '<p class="pd-hook"><span class="ital">%s</span></p>' % p["hook"]
        + '<div class="pd-body">%s</div>' % body_html
        + meta_html
        + '<div class="pd-cta">'
        + '<a class="pd-btn" href="../projects.html">← All projects</a>'
        + '<a class="pd-btn pd-btn-primary" href="../collab-wizard.html">Request Collab</a>'
        + '</div>'
        + '</div></div></div></section>'
    )


def build_jsonld(p):
    return (
        '<script type="application/ld+json">\n'
        '{\n'
        '  "@context": "https://schema.org",\n'
        '  "@type": "CreativeWork",\n'
        '  "name": "%s",\n' % p["title"]
        + '  "headline": "%s",\n' % p["hook"].replace('"', '\\"')
        + '  "description": "%s",\n' % p["desc"].replace('"', '\\"')
        + '  "url": "/projects/%s",\n' % p["slug"]
        + '  "inLanguage": "en",\n'
        '  "author": {\n'
        '    "@type": "Person",\n'
        '    "name": "Atharve Dahima",\n'
        '    "alternateName": "atharveeee",\n'
        '    "email": "atharveeee@gmail.com",\n'
        '    "url": "/"\n'
        '  }\n'
        '}\n'
        '</script>'
    )


def main():
    with open(BASE_FILE, encoding="utf-8") as f:
        base = f.read()
    base = rewrite_paths(base)
    base = rewrite_quoted_assets(base)

    i = base.index(SECTION_START) + len(SECTION_START)
    j = base.index(SECTION_END, i)

    jsonld_re = re.compile(r'<script type="application/ld\+json">.*?</script>', re.S)

    os.makedirs(OUT_DIR, exist_ok=True)
    for p in PROJECTS:
        page = base[:i] + build_section(p) + base[j:]
        page = page.replace(OLD_TITLE, "<title>%s, atharveeee</title>" % p["title"])
        page = jsonld_re.sub(lambda m, p=p: build_jsonld(p), page, count=1)
        page = page.replace(OLD_DESC, p["desc"])
        page = page.replace(OLD_OGTITLE, p["title"])
        out = os.path.join(OUT_DIR, p["slug"] + ".html")
        with open(out, "w", encoding="utf-8") as f:
            f.write(page)
        print("wrote", out, "(%d bytes)" % len(page))


if __name__ == "__main__":
    main()
