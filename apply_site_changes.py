# -*- coding: utf-8 -*-
"""Cross-file site fixes applied consistently across every page (shared components).

1. Footer socials: rebuild the .button-icon_group as clean Instagram + GitHub + VSCO
   anchors (fixes stale TikTok label, malformed rel attrs). Label -> "Follow me".
2. WhatsApp: point every data-whatsapp-modal-link (popup + footer + modal) directly
   at wa.me so the popup works even without the modal JS.
3. Audio: stop on pagehide/close so the track never lingers after leaving.

Idempotent: safe to re-run.
"""
import glob, re, os

FILES = [f for f in glob.glob("*.html") + glob.glob("projects/*.html")
         if f not in ("index.html.backup",)]

WA = "https://wa.me/919983974154"

ICON_STYLE = ('<div class="icon-button_transform w-embed"><style>'
              '@media (min-width: 992px){.icon-button_element.is-outline:hover .icon-btn_bg'
              '{transform: translateX(0%) translateY(0%);}}</style></div>')

# Icon glyphs (inner SVG markup), viewbox 0 0 24 24
IG = ('<path d="M21.94 7.88C21.9206 7.0503 21.7652 6.2294 21.48 5.45C21.2283 4.78181 20.8322 4.17742 20.32 3.68C19.8226 3.16776 19.2182 2.77166 18.55 2.52C17.7706 2.23484 16.9497 2.07945 16.12 2.06C15.06 2 14.72 2 12 2C9.28 2 8.94 2 7.88 2.06C7.0503 2.07945 6.2294 2.23484 5.45 2.52C4.78181 2.77166 4.17742 3.16776 3.68 3.68C3.16743 4.17518 2.77418 4.78044 2.53 5.45C2.23616 6.22734 2.07721 7.04915 2.06 7.88C2 8.94 2 9.28 2 12C2 14.72 2 15.06 2.06 16.12C2.07721 16.9508 2.23616 17.7727 2.53 18.55C2.77418 19.2196 3.16743 19.8248 3.68 20.32C4.17742 20.8322 4.78181 21.2283 5.45 21.48C6.2294 21.7652 7.0503 21.9206 7.88 21.94C8.94 22 9.28 22 12 22C14.72 22 15.06 22 16.12 21.94C16.9497 21.9206 17.7706 21.7652 18.55 21.48C19.2134 21.219 19.816 20.8242 20.3201 20.3201C20.8242 19.816 21.219 19.2134 21.48 18.55C21.7652 17.7706 21.9206 16.9497 21.94 16.12C21.94 15.06 22 14.72 22 12C22 9.28 22 8.94 21.94 7.88ZM20.14 16C20.1327 16.6348 20.0178 17.2637 19.8 17.86C19.6327 18.2913 19.3773 18.683 19.0501 19.0101C18.723 19.3373 18.3313 19.5927 17.9 19.76C17.3037 19.9778 16.6748 20.0927 16.04 20.1C15.04 20.15 14.67 20.16 12.04 20.16C9.41 20.16 9.04 20.16 8.04 20.1C7.38073 20.1148 6.72401 20.0132 6.1 19.8C5.66869 19.6327 5.27698 19.3773 4.94985 19.0501C4.62272 18.723 4.36734 18.3313 4.2 17.9C3.97775 17.2911 3.86271 16.6482 3.86 16C3.86 15 3.8 14.63 3.8 12C3.8 9.37 3.8 9 3.86 8C3.86271 7.35178 3.97775 6.70893 4.2 6.1C4.36734 5.66869 4.62272 5.27698 4.94985 4.94985C5.27698 4.62272 5.66869 4.36734 6.1 4.2C6.70893 3.97775 7.35178 3.86271 8 3.86C9 3.86 9.37 3.8 12 3.8C14.63 3.8 15 3.8 16 3.86C16.6348 3.86728 17.2637 3.98225 17.86 4.2C18.2913 4.36734 18.683 4.62272 19.0101 4.94985C19.3373 5.27698 19.5927 5.66869 19.76 6.1C19.9959 6.7065 20.1245 7.34942 20.14 8C20.19 9 20.2 9.37 20.2 12C20.2 14.63 20.19 15 20.14 16Z" fill="currentColor"></path>'
      '<path d="M12.0001 6.86035C10.9835 6.86035 9.98975 7.16181 9.14448 7.7266C8.29921 8.29139 7.6404 9.09415 7.25137 10.0334C6.86233 10.9726 6.76055 12.0061 6.95887 13.0031C7.1572 14.0002 7.64674 14.916 8.36558 15.6349C9.08442 16.3537 10.0003 16.8433 10.9973 17.0416C11.9944 17.2399 13.0279 17.1381 13.9671 16.7491C14.9063 16.3601 15.7091 15.7013 16.2739 14.856C16.8387 14.0107 17.1401 13.0169 17.1401 12.0004C17.1401 10.6371 16.5986 9.32976 15.6346 8.36582C14.6707 7.40189 13.3633 6.86035 12.0001 6.86035ZM12.0001 15.3304C11.3415 15.3304 10.6977 15.1351 10.1501 14.7691C9.60244 14.4032 9.17563 13.8832 8.92359 13.2747C8.67155 12.6662 8.60561 11.9967 8.73409 11.3507C8.86258 10.7047 9.17974 10.1114 9.64544 9.64569C10.1112 9.17998 10.7045 8.86283 11.3505 8.73434C11.9964 8.60585 12.666 8.67179 13.2744 8.92383C13.8829 9.17587 14.403 9.60269 14.7689 10.1503C15.1348 10.6979 15.3301 11.3417 15.3301 12.0004C15.3301 12.4377 15.244 12.8707 15.0766 13.2747C14.9093 13.6787 14.664 14.0458 14.3548 14.355C14.0456 14.6642 13.6785 14.9095 13.2744 15.0769C12.8704 15.2442 12.4374 15.3304 12.0001 15.3304Z" fill="currentColor"></path>'
      '<path d="M17.3399 5.45996C17.1026 5.45996 16.8705 5.53034 16.6732 5.6622C16.4759 5.79406 16.3221 5.98147 16.2312 6.20074C16.1404 6.42001 16.1166 6.66129 16.163 6.89407C16.2093 7.12685 16.3235 7.34067 16.4914 7.50849C16.6592 7.67631 16.873 7.7906 17.1058 7.8369C17.3386 7.88321 17.5798 7.85944 17.7991 7.76862C18.0184 7.67779 18.2058 7.52398 18.3377 7.32665C18.4695 7.12931 18.5399 6.8973 18.5399 6.65996C18.5399 6.3417 18.4135 6.03648 18.1884 5.81143C17.9634 5.58639 17.6582 5.45996 17.3399 5.45996Z" fill="currentColor"></path>')

GH = ('<path fill-rule="evenodd" clip-rule="evenodd" d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.02 10.02 0 0022 12.017C22 6.484 17.522 2 12 2z" fill="currentColor"></path>')

# VSCO segmented "ring" brand mark: two dashed circles (radial ticks) + center dot.
VSCO = ('<circle cx="12" cy="12" r="8" fill="none" stroke="currentColor" stroke-width="3" stroke-dasharray="2.5 1.1"></circle>'
        '<circle cx="12" cy="12" r="3.7" fill="none" stroke="currentColor" stroke-width="2.2" stroke-dasharray="1.7 0.9"></circle>'
        '<circle cx="12" cy="12" r="1.3" fill="currentColor"></circle>')


def social_anchor(label, url, icon):
    svg = ('<svg class="height-100" fill="none" height="100%%" viewbox="0 0 24 24" '
           'xmlns="http://www.w3.org/2000/svg">%s</svg>' % icon)
    icon_block = '<div class="icon-24px"><div class="icon">%s</div></div>' % svg
    return (
        '<a class="button-link w-inline-block" aria-label="%s" href="%s" target="_blank" rel="noopener">' % (label, url)
        + '<div aria-label="" class="icon-button" fs-mirrorclick-element="">'
        + ICON_STYLE
        + '<div class="icon-button_element is-outline is-outline">'
        + '<div class="icon-btn_bg is-vertical is-vertical"><div class="icon-btn_bg-fill is-outline"></div></div>'
        + '<div class="icon-btn_content"><div class="icon-btn_track is-vertical">'
        + '<div class="icon-btn_item">' + icon_block + '</div>'
        + '<div class="icon-btn_item is-vertical">' + icon_block + '</div>'
        + '</div></div></div></div></a>'
    )


CANON_SOCIALS = (
    social_anchor("Instagram", "https://www.instagram.com/atharveeee_4?igsh=MXRjNXVvdG00ZTdsZw==", IG)
    + social_anchor("GitHub", "https://github.com/atharveeee-netizen", GH)
    + social_anchor("VSCO", "https://vsco.co/atharveeee", VSCO)
)

ANCHOR_RE = re.compile(r'\s*<a class="button-link.*?</a>', re.S)


def rebuild_socials(html):
    """Replace the inner anchors of every .button-icon_group with the canonical set."""
    out = []
    idx = 0
    changed = 0
    for m in re.finditer(r'class="button-icon_group">', html):
        start = m.end()
        out.append(html[idx:start])
        # consume consecutive <a class="button-link">...</a>
        pos = start
        while True:
            am = ANCHOR_RE.match(html, pos)
            if not am:
                break
            pos = am.end()
        out.append(CANON_SOCIALS)
        idx = pos
        changed += 1
    out.append(html[idx:])
    return "".join(out), changed


def add_pagehide_stop(html):
    if "'pagehide'" in html or '"pagehide"' in html:
        return html, False
    pat = re.compile(r"(window\.addEventListener\('beforeunload',\s*function\(\)\s*\{\s*localStorage\.setItem\('soundPosition',\s*bgSound\.seek\(\)\s*\|\|\s*0\);\s*\}\);)")
    inject = (r"\1"
              "\n  window.addEventListener('pagehide', function(){"
              "try{localStorage.setItem('soundPosition', bgSound.seek()||0);}catch(e){}"
              "try{if(window.Howler){Howler.stop();}else if(window.bgSound){bgSound.stop();}}catch(e){}});")
    new = pat.sub(inject, html, count=1)
    return new, (new != html)


def main():
    for f in FILES:
        s = open(f, encoding="utf-8").read()
        orig = s
        notes = []

        # 1. Footer label
        if "Follow us" in s:
            s = s.replace("Follow us", "Follow me")
            notes.append("follow-me")

        # 2. Socials rebuild
        s, n = rebuild_socials(s)
        if n:
            notes.append("socials x%d" % n)

        # 3. WhatsApp direct links
        c_before = s.count('data-whatsapp-modal-link="" href="#"')
        if c_before:
            s = s.replace('data-whatsapp-modal-link="" href="#"',
                          'data-whatsapp-modal-link="" href="%s" target="_blank" rel="noopener"' % WA)
            notes.append("wa x%d" % c_before)

        # 4. Audio stop on close
        s, ph = add_pagehide_stop(s)
        if ph:
            notes.append("pagehide-stop")

        # 5. Absurdo image in the popup's empty frame
        VF = "https://cdn.prod.website-files.com/67890d3b1a9365a1173c954e/68414b36c5bc5cd43e314e77_Videoframe.webp"
        if VF in s:
            prefix = "../" if os.path.dirname(f).endswith("projects") else ""
            s = s.replace(VF, prefix + "assets/img/popup-image.png")
            notes.append("absurdo")

        if s != orig:
            open(f, "w", encoding="utf-8").write(s)
            print("%-42s %s" % (f, ", ".join(notes)))
        else:
            print("%-42s (no change)" % f)


if __name__ == "__main__":
    main()
