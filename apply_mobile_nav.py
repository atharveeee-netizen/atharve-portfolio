# -*- coding: utf-8 -*-
"""Wire up the mobile full-screen hamburger menu (pieterkoopt-style) on every page.

The Webflow export already ships the full-screen menu markup (.navmenu-wrapper) and a
hamburger button (.nav-trigger), but:
  * the Webflow ix2 interaction that opens the menu never fires in this static clone, and
  * at <=767px Webflow hides BOTH the hamburger and the menu and instead shows the cramped
    inline .navbar_menu -> the "cut-off HOW IT WORKS" the user sees on a phone.

This injects a self-contained CSS + JS toggle (no dependency on Webflow ix2/GSAP):
  * <=991px: hide the cramped inline menu + in-bar CTA, show the hamburger.
  * .navmenu-wrapper becomes a fixed full-screen overlay, faded in via a .nav-open class.
  * vanilla JS toggles .nav-open on click, closes on link tap / Escape / resize-to-desktop,
    and locks background scroll while open.

Idempotent: re-running replaces the injected blocks (matched by marker id).
"""
import glob
import re

FILES = [f for f in glob.glob("*.html") + glob.glob("projects/*.html")
         if f not in ("index.html.backup",)]

STYLE_ID = "mobile-nav-overlay"
SCRIPT_ID = "mobile-nav-toggle"

STYLE_BLOCK = """<style id="mobile-nav-overlay">
  /* === Mobile full-screen nav (pieterkoopt-style) — injected by apply_mobile_nav.py === */
  @media screen and (max-width: 991px) {
    /* Hide the cramped inline center menu + the in-bar CTA: bar = logo + hamburger */
    .nav .navbar_col.is-center { display: none !important; }
    .nav .navbar_col.is-right .navbar-cta { display: none !important; }

    /* Show the hamburger */
    .nav .nav-trigger {
      display: flex !important;
      gap: 5px !important;
      cursor: pointer;
      -webkit-tap-highlight-color: transparent;
    }
    .nav .nav-trigger .nt_icon-line {
      width: 22px !important;
      height: 2px !important;
      background-color: var(--_colors---swatch--beige) !important;
      transition: transform .35s cubic-bezier(.16,1,.3,1), opacity .25s ease !important;
    }
    /* Morph hamburger -> X when open */
    .nav.nav-open .nt_icon-line.is-01 { transform: translateY(3.5px) rotate(45deg) !important; }
    .nav.nav-open .nt_icon-line.is-02 { transform: translateY(-3.5px) rotate(-45deg) !important; }

    /* Full-screen overlay menu, controlled by .nav-open (NOT Webflow ix2) */
    .nav .navmenu-wrapper {
      display: flex !important;
      opacity: 0;
      visibility: hidden;
      transform: translateY(-0.75em);
      pointer-events: none;
      transition: opacity .4s cubic-bezier(.16,1,.3,1),
                  transform .4s cubic-bezier(.16,1,.3,1),
                  visibility .4s;
    }
    .nav.nav-open .navmenu-wrapper {
      opacity: 1 !important;
      visibility: visible !important;
      transform: translateY(0) !important;
      pointer-events: auto !important;
    }

    /* Webflow ix2 leaves the inner panel at display:none + translateY(-100%)
       (its closed state). Force it open via OUR class, overriding ix2's inline. */
    .nav.nav-open .navmenu {
      display: flex !important;
      visibility: visible !important;
      opacity: 1 !important;
      transform: none !important;
    }

    /* Larger, prominent stacked menu links.
       NB: the desktop `navbar-flex-override` forces is-navlink height:100% !important,
       which blows each menu row up to ~420px here — pin it back to auto.
       text-transform keeps the span-less "About" consistent with its siblings. */
    .nav .navmenu_list .btn-animate-chars.is-navlink {
      height: auto !important;
      font-size: 1.5rem !important;
      padding-top: 1.05em !important;
      padding-bottom: 1.05em !important;
      letter-spacing: -0.02em !important;
      align-items: center !important;
      text-transform: uppercase !important;
    }
    .nav .navmenu_list .btn-animate-chars.is-navlink [data-button-animate-chars] {
      height: 1.4em !important;
    }

    /* Action buttons: full-width, stacked, properly filled (no GSAP fill here) */
    .nav .navmenu_button-group {
      grid-template-columns: 1fr !important;
      grid-row-gap: 0.75em !important;
      grid-column-gap: 0 !important;
    }
    .nav .navmenu_button-group > * { width: 100% !important; }
    .nav .navmenu_button-group .btn-animate-chars {
      display: flex !important;
      align-items: center !important;
      justify-content: center !important;
      width: 100% !important;
      min-height: 52px !important;
      border-radius: 6px !important;
      font-size: 1rem !important;
      letter-spacing: 0.01em !important;
    }
    /* Request Collab -> filled brand green */
    .nav .navmenu_button-item .btn-animate-chars {
      background-color: var(--_colors---swatch--green) !important;
      color: var(--_colors---swatch--black) !important;
      border: none !important;
    }
    /* WhatsApp -> outline */
    .nav .navmenu_button-group > .btn-animate-chars.outline {
      border: 1px solid var(--_colors---swatch--grey) !important;
      color: var(--_colors---swatch--beige) !important;
    }

    /* Drop leftover clone cruft ("Visit dutch site" locale buttons) from the menu */
    .nav .navmenu .w-locales-list { display: none !important; }
  }

  /* Lock background scroll while the menu is open */
  html.menu-open, body.menu-open { overflow: hidden !important; }
</style>"""

SCRIPT_BLOCK = """<script id="mobile-nav-toggle">
(function(){
  function init(){
    var nav = document.querySelector('nav.nav');
    if(!nav || nav.__mobileNavInit) return;
    var trigger = nav.querySelector('.nav-trigger');
    var wrapper = nav.querySelector('.navmenu-wrapper');
    if(!trigger || !wrapper) return;
    nav.__mobileNavInit = true;

    trigger.setAttribute('role', 'button');
    trigger.setAttribute('aria-label', 'Menu');
    trigger.setAttribute('aria-controls', 'navmenu');
    trigger.setAttribute('aria-expanded', 'false');
    wrapper.id = wrapper.id || 'navmenu';

    var root = document.documentElement, body = document.body;
    function open(){
      nav.classList.add('nav-open');
      root.classList.add('menu-open');
      body.classList.add('menu-open');
      trigger.setAttribute('aria-expanded', 'true');
    }
    function close(){
      nav.classList.remove('nav-open');
      root.classList.remove('menu-open');
      body.classList.remove('menu-open');
      trigger.setAttribute('aria-expanded', 'false');
    }
    function toggle(e){
      if(e){ e.preventDefault(); e.stopPropagation(); }
      if(nav.classList.contains('nav-open')) close(); else open();
    }

    trigger.addEventListener('click', toggle);
    // Tapping a menu link navigates AND closes the overlay
    wrapper.addEventListener('click', function(e){
      if(e.target.closest('a')) close();
    });
    // Escape closes
    document.addEventListener('keydown', function(e){
      if((e.key === 'Escape' || e.key === 'Esc') && nav.classList.contains('nav-open')) close();
    });
    // Returning to desktop width tidies up state
    window.addEventListener('resize', function(){
      if(window.innerWidth > 991 && nav.classList.contains('nav-open')) close();
    });
  }
  if(document.readyState === 'loading'){
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
</script>"""


def upsert(html, block, marker_id, tag, before):
    """Insert `block` before the `before` tag, or replace an existing <tag id=marker_id> block."""
    existing = re.compile(
        r'[ \t]*<%s id="%s">.*?</%s>\n?' % (tag, re.escape(marker_id), tag),
        re.S,
    )
    if existing.search(html):
        return existing.sub(lambda m: block + "\n", html, count=1), "replaced"
    idx = html.rfind(before)
    if idx == -1:
        return html, "no-anchor(%s)" % before
    return html[:idx] + block + "\n" + html[idx:], "inserted"


def main():
    for f in FILES:
        s = open(f, encoding="utf-8").read()
        orig = s
        notes = []

        # The "About" NAV link is the only menu item shipped as bare text (no inner
        # .navbar-link_text span), so it renders in a different font/case than its
        # siblings. Wrap it to match — but ONLY the nav links (is-navlink), never the
        # footer link, which must not inherit the global data-button-animate-chars clip.
        # First reset any prior wrap (idempotent + undoes an earlier over-broad pass).
        wrapped = ('href="about.html"><span class="navbar-link_text" '
                   'data-button-animate-chars="">About</span></a>')
        s = s.replace(wrapped, 'href="about.html">About</a>')
        s, about_n = re.subn(
            r'(<a[^>]*\bis-navlink\b[^>]*href="about\.html">)About(</a>)',
            r'\1<span class="navbar-link_text" data-button-animate-chars="">About</span>\2',
            s,
        )
        if about_n:
            notes.append("about-span x%d" % about_n)

        s, n1 = upsert(s, STYLE_BLOCK, STYLE_ID, "style", "</head>")
        notes.append("style:" + n1)
        s, n2 = upsert(s, SCRIPT_BLOCK, SCRIPT_ID, "script", "</body>")
        notes.append("script:" + n2)

        if s != orig:
            open(f, "w", encoding="utf-8").write(s)
            print("%-42s %s" % (f, ", ".join(notes)))
        else:
            print("%-42s (no change)" % f)


if __name__ == "__main__":
    main()
