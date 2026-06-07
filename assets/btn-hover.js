/* ============================================================
   PIETERKOOPT BUTTON HOVER - cloned for atharveeee, v2 (clean)
   ------------------------------------------------------------
   Faithfully reproduces pieterkoopt.nl's CTA hover:

     1. per-character text ROLL  (each letter lifts out, a clone
        rolls up into its place, staggered left -> right)
     2. dual-arrow forward LOOP  (the front arrow slides out right,
        the second arrow enters from the left)
     3. subtle background FILL   (a soft wipe rises from the bottom)

   Timing is REFERENCE-FAITHFUL and matches the template's native
   inline hover exactly: ease cubic-bezier(.16,1,.3,1), .6s duration,
   .01s per-char stagger. (An earlier draft used .625,.05,0,1 / .5s /
   .02s, which did not match pieterkoopt.)

   WHY v2 EXISTS (the regression this fixes):
   The page ALSO ships an inline hover system (initButtonCharacterStagger
   + a `[data-button-animate-chars] span { text-shadow: 0 1.3em }` CSS
   roll). v1 of this file layered a SECOND roll on top of that one, so
   both fired on the same spans -> ghost text-shadows and double
   translate -> visibly broken hover.

   The clean fix: when we enhance a button we REMOVE its
   `data-button-animate-chars` attribute. That disconnects every inline
   `[data-button-animate-chars] ...` rule from our new .fx-char spans in
   one move (no specificity war), so this module becomes the single,
   authoritative hover. The arrow/bg inline rules are out-specified by
   our `.cta-fx`-scoped selectors.

   Self-contained: injects its own CSS, auto-binds to every CTA
   button site-wide, skips plain nav links, and no-ops under
   prefers-reduced-motion. Safe to load once per page.
   ============================================================ */
(function () {
  'use strict';

  if (window.__btnHoverInit) return;
  window.__btnHoverInit = true;

  /* honour the same reduced-motion contract the rest of the site uses */
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  // Reference-faithful timing (matches the template's native inline hover
  // and pieterkoopt.nl): ease cubic-bezier(.16,1,.3,1), .6s, .01s stagger.
  var EASE = 'cubic-bezier(.16,1,.3,1)';

  /* ---------- 1. inject the stylesheet (once) ---------- */
  var css =
    /* text roll: each char is a 1em clip window holding two stacked copies
       (visible on top, clone below). On hover both lift one line: the top
       copy exits up, the clone rolls into its place. We null out text-shadow
       defensively in case any residual inline rule still reaches a span. */
    '.cta-fx .btn-animate-chars__text{overflow:hidden;}' +
    '.cta-fx .fx-char{display:inline-block;overflow:hidden;height:1em;line-height:1em;vertical-align:top;text-shadow:none;}' +
    '.cta-fx .fx-char .fx-char__a,.cta-fx .fx-char .fx-char__b{display:block;height:1em;line-height:1em;text-shadow:none;' +
      'white-space:pre;transition:transform .6s ' + EASE + ';will-change:transform;}' +
    '.cta-fx:hover .fx-char .fx-char__a,.cta-fx:focus-visible .fx-char .fx-char__a,' +
    '.cta-fx:hover .fx-char .fx-char__b,.cta-fx:focus-visible .fx-char .fx-char__b{transform:translateY(-100%);}' +

    /* arrow track: forward loop inside the clipped icon box */
    '.cta-fx .button-icon{overflow:hidden;justify-content:flex-start;}' +
    '.cta-fx .button-icon_track{transform:translateX(-50%);' +
      'transition:transform .6s ' + EASE + ';will-change:transform;}' +
    '.cta-fx:hover .button-icon_track,.cta-fx:focus-visible .button-icon_track{transform:translateX(0%);}' +

    /* background: a soft fill wipes up from the bottom */
    '.cta-fx .btn-animate-chars__bg{overflow:hidden;}' +
    '.cta-fx .btn-animate-chars__bg::after{content:"";position:absolute;inset:0;border-radius:inherit;' +
      'background:rgba(255,255,255,.10);transform:scaleY(0);transform-origin:50% 100%;' +
      'transition:transform .6s ' + EASE + ';pointer-events:none;}' +
    '.cta-fx:hover .btn-animate-chars__bg::after,.cta-fx:focus-visible .btn-animate-chars__bg::after{transform:scaleY(1);}';

  var style = document.createElement('style');
  style.id = 'btn-hover-fx';
  style.textContent = css;
  document.head.appendChild(style);

  /* ---------- 2. split a label into animatable characters ---------- */
  function splitLabel(textEl) {
    if (textEl.__split) return;
    textEl.__split = true;

    /* textContent flattens whatever the inline splitter may have already
       produced back into the plain label, so this is order-independent. */
    var raw = textEl.textContent;
    var chars = Array.prototype.slice.call(raw); // unicode-aware enough for Latin labels
    var frag = document.createDocumentFragment();

    chars.forEach(function (ch, i) {
      var glyph = ch === ' ' ? ' ' : ch;
      var delay = (i * 0.01).toFixed(3) + 's'; // .01s per-char stagger (reference)

      var wrap = document.createElement('span');
      wrap.className = 'fx-char';

      var a = document.createElement('span');
      a.className = 'fx-char__a';
      a.textContent = glyph;
      a.style.transitionDelay = delay;

      var b = document.createElement('span');
      b.className = 'fx-char__b';
      b.textContent = glyph;
      b.style.transitionDelay = delay;
      b.setAttribute('aria-hidden', 'true'); // the clone is decorative

      wrap.appendChild(a);
      wrap.appendChild(b);
      frag.appendChild(wrap);
    });

    textEl.textContent = '';
    textEl.appendChild(frag);

    /* THE KEY FIX: drop the attribute so the inline
       `[data-button-animate-chars] span` rules can no longer touch our
       spans. This makes us the single hover system, conflict-free. */
    textEl.removeAttribute('data-button-animate-chars');
  }

  /* ---------- 3. enhance every CTA, skip plain nav links ---------- */
  // nav text links, language switcher, story tiles, upload zones keep their own hover
  var SKIP = '.is-navlink, .is-stories, .is-localization, .is-upload, .is-toggle';

  function enhance() {
    var buttons = document.querySelectorAll('.btn-animate-chars');
    Array.prototype.forEach.call(buttons, function (btn) {
      if (btn.__ctaFx || btn.matches(SKIP)) return;

      // Only enhance buttons that actually carry the animatable label
      // structure. Plain text CTAs (e.g. the nav "Request Collab", which
      // is a bare <a> with no __text) have nothing to roll, so we leave
      // them untouched rather than tag them with a no-op .cta-fx.
      var text = btn.querySelector('.btn-animate-chars__text');
      if (!text) return;

      btn.__ctaFx = true;
      btn.classList.add('cta-fx');
      splitLabel(text);
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', enhance);
  } else {
    enhance();
  }

  /* re-scan once more after late template hydration (footer, ix2 clones) */
  window.addEventListener('load', enhance);
})();
