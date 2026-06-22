# -*- coding: utf-8 -*-
"""Copy rewrite round 2 (user-directed), June 13, 2026.

Targets:
- index.html: hero (Cold kills noise -> Coherence and cold), green CTA section
  (Overthinking/Overanalyzing + 3 cards), WhatsApp popup text, stories-cta
  ("orca") section (Every project has a story).
- how-it-works.html: the 4 HIW slides rewritten as THE INDIFFERENCE /
  THE LUCIDITY / THE STRUGGLE / THE ABSURD.

Idempotent: safe to re-run (raises if an OLD string is no longer found, e.g.
because it was already replaced).
"""
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent


def apply_replacements(path, replacements, text=None):
    if text is None:
        text = path.read_text(encoding="utf-8")
    for old, new in replacements:
        candidates = [old]
        if "'" in old:
            candidates.append(old.replace("'", "’"))

        applied = False
        for cand in candidates:
            count = text.count(cand)
            if count:
                text = text.replace(cand, new)
                print(f"{path.name}: replaced {count}x -> {new[:60]!r}")
                applied = True
                break

        if not applied:
            raise SystemExit(f"NOT FOUND in {path.name}: {old[:90]!r}")

    return text


INDEX_REPLACEMENTS = [
    # 1. Hero heading + subline (landing page)
    (
        '<h1 class="heading-m">Cold kills noise.<br/><span class="alt-heading">That\'s where I work.</span></h1>'
        '<div class="max-width-60ch"><div class="padding-top padding-24px"><p class="paragraph-l">'
        'Embedded systems and cryogenic electronics, edging toward quantum hardware. From a bench in Gujarat.</p></div></div>',

        '<h1 class="heading-m">COHERENCE<br/><span class="alt-heading">AND COLD</span></h1>'
        '<div class="max-width-60ch"><div class="padding-top padding-24px"><p class="paragraph-l">'
        'Embedded systems and cryogenic electronics, edging toward quantum hardware.</p></div></div>',
    ),

    # 2. Green CTA section heading
    (
        '<h2 class="heading-wrapper" style="text-align:center;display:flex;flex-direction:column;align-items:center;gap:.15em;">'
        '<div class="heading-l">Want to build something?</div><div class="heading-l alt-heading">The bench is open.</div></h2>',

        '<h2 class="heading-wrapper" style="text-align:center;display:flex;flex-direction:column;align-items:center;gap:.15em;">'
        '<div class="heading-l">OVERTHINKING,</div><div class="heading-l alt-heading">OVERANALYZING</div></h2>',
    ),

    # 3. Green CTA section body
    (
        '<p class="paragraph-m">I work close to the metal: every board, every frame, every line of flight code. '
        'Nothing out there asks me to. That\'s exactly why I do it.</p>',

        '<p class="paragraph-m">A drone in flight, a quantum readout chain, a custom silicon architecture. '
        'Across every scale of engineering, physical reality enforces the same law. '
        'No wasted space. No dead weight. No abstractions.</p>',
    ),

    # 4. Card 1 (appears twice: cta-cards-wrap + uc-circles)
    (
        '<h3 class="heading-s">Close to the metal</h3><div class="alt-heading"><div class="paragraph-xl alt-heading">'
        'Every board and every line of firmware, by hand.</div></div>',

        '<h3 class="heading-s">NOTHING LEFT TO TAKE AWAY.</h3><div class="alt-heading"><div class="paragraph-xl alt-heading">'
        'I reduce the architecture to its physical limit. No black boxes.</div></div>',
    ),

    # 5. Card 2 (appears twice)
    (
        '<h3 class="heading-s">Built to be broken</h3><div class="alt-heading"><div class="paragraph-xl alt-heading">'
        'Tested against the real world until it holds.</div></div>',

        '<h3 class="heading-s">WHAT I CANNOT CREATE...</h3><div class="alt-heading"><div class="paragraph-xl alt-heading">'
        '...I do not understand. I own the architecture from the logic up.</div></div>',
    ),

    # 6. Card 3 (appears twice)
    (
        '<h3 class="heading-s">Fast and personal</h3><div class="alt-heading"><div class="paragraph-xl alt-heading">'
        'A reply to your brief within 48 hours.</div></div>',

        '<h3 class="heading-s">WORDS ARE MEANINGLESS.</h3><div class="alt-heading"><div class="paragraph-xl alt-heading">'
        'Theory is quiet. A datasheet is a rumor until the hardware works.</div></div>',
    ),

    # 7. WhatsApp popup text
    (
        '<div class="popup-text"><div class="popup-text-inner"><div class="mono-type">'
        'Got a build in mind, or a hard question? Message me on WhatsApp.</div></div></div>',

        '<div class="popup-text"><div class="popup-text-inner"><div class="mono-type">'
        '<strong>HELLO? IS THERE ANYBODY IN THERE?</strong></div></div></div>',
    ),

    # 8. Stories-cta ("orca") heading
    (
        '<h2 class="heading-wrapper text-color-black"><div class="heading-l">Every project has a '
        '<span class="alt-heading">Story</span></div></h2>',

        '<h2 class="heading-wrapper text-color-black"><div class="heading-l">EVERY PROJECT HAS A '
        '<span class="alt-heading">STORY.</span></div></h2>',
    ),

    # 9. Stories-cta body
    (
        '<p class="paragraph-l stories-cta_title">Every build sits here with the reason it exists, the problem, '
        'the constraint, the fix. Walk through. Open one. Stay for the story.</p>',

        '<p class="paragraph-l stories-cta_title">"The world is the totality of facts, not of things."'
        '<br/><br/>It\'s a long way down.<br/><br/>'
        'I do not present projects. This is a library of things that survived.</p>',
    ),

    # 10. Stories-cta button + aria-label
    (
        '<a aria-label="Enter the gallery" class="btn-animate-chars w-inline-block [is-icon]" '
        'data-wf--button--variant="base" href="projects.html"><div class="btn-animate-chars__bg"></div>'
        '<span class="btn-animate-chars__text" data-button-animate-chars="">Enter the gallery</span>',

        '<a aria-label="ENTER THE GALLERY" class="btn-animate-chars w-inline-block [is-icon]" '
        'data-wf--button--variant="base" href="projects.html"><div class="btn-animate-chars__bg"></div>'
        '<span class="btn-animate-chars__text" data-button-animate-chars="">ENTER THE GALLERY</span>',
    ),
]


HIW_REPLACEMENTS = [
    # 0. THE INDIFFERENCE (intro slide)
    (
        '<h2 class="heading-wrapper"><div class="heading-l"><span class="alt-heading">From a sketch </span>'
        'to a board that holds</div></h2><div class="max-width-55ch"><div class="padding-top padding-32px">'
        '<p class="paragraph-l text-weight-medium">No black box, no hand-waving. Three steps from your brief '
        'to working hardware, and you see the reasoning behind every one.</p></div></div>',

        '<h2 class="heading-wrapper"><div class="heading-l"><span class="alt-heading">THE </span>'
        'INDIFFERENCE</div></h2><div class="max-width-55ch"><div class="padding-top padding-32px">'
        '<p class="paragraph-l text-weight-medium">Physics does not care about the design. Whether it is a cryo '
        'vacuum, microscopic silicon constraints, or raw gravity, the environment is absolute. '
        'I map these rules first.</p></div></div>',
    ),

    # 01. THE LUCIDITY
    (
        '<div class="hiw-number"><div>01</div></div><div class="hiw-info"><h2 class="heading-wrapper">'
        '<div class="heading-m">Share the</div><div class="heading-m alt-heading">brief</div></h2>'
        '<div class="max-width-55ch"><div class="padding-top padding-32px"><p class="paragraph-l text-weight-medium">'
        'Share your specs, a schematic, or just a sentence on a napkin, tell me what it needs to do.'
        '</p></div></div></div>',

        '<div class="hiw-number"><div>01</div></div><div class="hiw-info"><h2 class="heading-wrapper">'
        '<div class="heading-m">THE</div><div class="heading-m alt-heading">LUCIDITY</div></h2>'
        '<div class="max-width-55ch"><div class="padding-top padding-32px"><p class="paragraph-l text-weight-medium">'
        'Translating abstract logic into exact physical geometry. I map the architecture manually, whether '
        'routing quantum control lines or laying out VLSI traces. Every connection is intentional.'
        '</p></div></div></div>',
    ),

    # 02. THE STRUGGLE
    (
        '<div class="hiw-number"><div>02</div></div><div class="hiw-info"><h2 class="heading-wrapper">'
        '<div class="heading-m">Review <br/><span class="alt-heading">in 48 hours</span></div></h2>'
        '<div class="max-width-55ch"><div class="padding-top padding-32px"><p class="paragraph-l text-weight-medium">'
        'I review what you send within 48 hours and tell you straight whether it\'s a build worth doing.'
        '</p></div></div></div>',

        '<div class="hiw-number"><div>02</div></div><div class="hiw-info"><h2 class="heading-wrapper">'
        '<div class="heading-m">THE</div><div class="heading-m alt-heading">STRUGGLE</div></h2>'
        '<div class="max-width-55ch"><div class="padding-top padding-32px"><p class="paragraph-l text-weight-medium">'
        'Pulling the simulation off the screen. Etching the die, extruding the chassis, or wiring the fridge. '
        'This is where pure math is forced into heavy, physical materials.'
        '</p></div></div></div>',
    ),

    # 03. THE ABSURD -- paragraph only (heading handled via regex, see below, due to a
    # zero-width-joiner character between <br/> and <span> in the source markup).
    (
        '<p class="paragraph-l text-weight-medium">If it\'s worth doing, we scope it together: timeline, parts, '
        'cost. Then I build it, boards and firmware, and break it against the real world until it holds.</p>',

        '<p class="paragraph-l text-weight-medium">The bench verdict. Perfect simulation meets unforgiving '
        'reality, whether it is thermal noise, signal collapse, or structural impact. If the hardware fractures, '
        'I log the exact flaw and rebuild.</p>',
    ),
]


index_text = apply_replacements(ROOT / "index.html", INDEX_REPLACEMENTS)
(ROOT / "index.html").write_text(index_text, encoding="utf-8")

hiw_text = (ROOT / "how-it-works.html").read_text(encoding="utf-8")

# 03 heading: "Build <br/>[ZWJ]<span class="alt-heading">& test</span>" -> "THE" / "ABSURD"
# `.?` swallows the optional zero-width-joiner without needing to type it literally.
pattern = re.compile(
    r'<h2 class="heading-wrapper"><div class="heading-m">Build <br/>.?'
    r'<span class="alt-heading">& test</span></div></h2>'
)
hiw_text, n = pattern.subn(
    '<h2 class="heading-wrapper"><div class="heading-m">THE</div>'
    '<div class="heading-m alt-heading">ABSURD</div></h2>',
    hiw_text,
)
if n != 1:
    raise SystemExit(f"slide-03 heading regex matched {n} times (expected 1)")
print(f"how-it-works.html: replaced {n}x -> slide-03 heading (THE ABSURD)")

hiw_text = apply_replacements(ROOT / "how-it-works.html", HIW_REPLACEMENTS, text=hiw_text)
(ROOT / "how-it-works.html").write_text(hiw_text, encoding="utf-8")

print("Done.")
