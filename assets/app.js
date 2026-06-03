/* ============================================================
   ATHARVE DAHIMA — GLOBAL ANIMATION + INTERACTION ENGINE
   ============================================================ */
(function () {
  'use strict';

  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (reduced) document.documentElement.classList.add('no-motion');

  /* premium inertia smooth-scroll (Lenis, MIT) — skipped under reduced motion */
  if (!reduced && !window.__lenisInit) {
    window.__lenisInit = true;
    var ls = document.createElement('script');
    ls.src = 'https://cdn.jsdelivr.net/npm/lenis@1.1.14/dist/lenis.min.js';
    ls.onload = function () {
      try {
        var lenis = new Lenis({ duration: 1.15, smoothWheel: true, wheelMultiplier: 1, touchMultiplier: 1.4 });
        window.__lenis = lenis;
        function lraf(t) { lenis.raf(t); requestAnimationFrame(lraf); }
        requestAnimationFrame(lraf);
      } catch (e) {}
    };
    document.head.appendChild(ls);
  }

  var EASE_DELAY = 120;

  /* ============================================================
     ROBUST REVEAL CORE
     Each effect runs via IntersectionObserver, but ALSO fires
     immediately for anything already in view at load, and a
     failsafe guarantees nothing can ever stay invisible.
     ============================================================ */
  var pending = []; // { el, fn } for failsafe

  function inView(el, margin) {
    var r = el.getBoundingClientRect();
    margin = margin || 0;
    var vh = window.innerHeight || document.documentElement.clientHeight;
    return r.top < vh - margin && r.bottom > margin;
  }

  // run fn once; guard against double-run
  function once(el, fn) {
    if (el.__revealed) return;
    el.__revealed = true;
    fn(el);
  }

  // observe `sel` elements; when they enter, run `fn(el)`.
  // immediately runs for those already in view; registers failsafe.
  function reveal(sel, fn, opts) {
    var els = document.querySelectorAll(sel);
    if (!els.length) return;
    var threshold = (opts && opts.threshold) || 0.15;
    var margin = (opts && opts.margin) || 60;
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { once(e.target, fn); io.unobserve(e.target); }
      });
    }, { threshold: threshold, rootMargin: '0px 0px -8% 0px' });
    els.forEach(function (el) {
      pending.push({ el: el, fn: fn });
      if (inView(el, margin)) { once(el, fn); }   // above-the-fold: reveal now
      else io.observe(el);
    });
  }

  // failsafe: after 1.6s reveal anything still hidden, then pin
  // final states directly (covers environments where CSS
  // transitions never advance / IntersectionObserver never fires)
  setTimeout(function () {
    pending.forEach(function (p) { once(p.el, p.fn); });
    document.querySelectorAll('.line-inner.revealed').forEach(function (el) {
      el.style.transition = 'none'; el.style.opacity = '1'; el.style.transform = 'translateY(0)';
    });
    document.querySelectorAll('.reveal-child, .usp-item').forEach(function (el) {
      if (el.style.opacity === '1') { el.style.transition = 'none'; el.style.transform = 'translateY(0)'; }
    });
    document.querySelectorAll('.footer-lead.revealed, .footer-nav-large.revealed, .footer-right.revealed').forEach(function (el) {
      el.style.transition = 'none'; el.style.opacity = '1'; el.style.transform = 'translateY(0)';
    });
    document.querySelectorAll('.scatter-card.in').forEach(function (el) {
      el.style.transition = 'none'; el.style.opacity = '1';
    });
  }, 1600);

  /* ---------- effect fns ---------- */
  function revealHeading(el) {
    el.querySelectorAll('.line-inner').forEach(function (line, i) {
      setTimeout(function () { line.classList.add('revealed'); }, i * EASE_DELAY);
    });
  }
  function revealChildren(el) {
    el.querySelectorAll('.reveal-child').forEach(function (k, i) {
      setTimeout(function () { k.style.opacity = '1'; k.style.transform = 'translateY(0)'; }, i * 100);
    });
  }
  function revealUsp(el) {
    el.querySelectorAll('.usp-item').forEach(function (item, i) {
      setTimeout(function () { item.style.opacity = '1'; item.style.transform = 'translateY(0)'; }, i * 160);
    });
  }
  function revealCard(el) {
    var card = el.querySelector('.sticky-note-card');
    setTimeout(function () { if (card) card.classList.add('card-entered'); }, 400);
  }
  function revealStep(el) {
    var num = el.querySelector('.step-number');
    var content = el.querySelector('.step-content');
    var media = el.querySelector('.step-media');
    if (num) setTimeout(function () { num.classList.add('num-revealed'); }, 0);
    if (content) setTimeout(function () { content.classList.add('content-revealed'); }, 300);
    if (media) setTimeout(function () { media.classList.add('media-revealed'); }, 450);
  }
  function addIn(el) { el.classList.add('in'); }
  function revealCarousel(el) {
    el.querySelectorAll('.carousel-card').forEach(function (c, i) {
      setTimeout(function () { c.classList.add('revealed'); }, i * 100);
    });
  }
  function revealFooter(el) {
    el.classList.add('revealed');
  }
  function revealScatter(el) {
    el.querySelectorAll('.scatter-card').forEach(function (c, i) {
      setTimeout(function () {
        c.classList.add('in');
        setTimeout(function () { c.style.transition = 'none'; c.style.opacity = '1'; }, 1100);
      }, i * 240);
    });
  }

  /* sequential scroll-triggered scatter card reveal */
  (function () {
    var sec = document.querySelector('.starts-here');
    if (!sec) return;
    var cards = sec.querySelectorAll('.scatter-card');
    if (!cards.length) return;
    var mobile = window.matchMedia('(max-width: 768px)').matches;
    var th = mobile ? [0, 0.18, 0.36] : [0, 0.28, 0.56];
    function setCard(c, on) {
      if (on) {
        if (c.__on) return; c.__on = true;
        c.classList.add('in');
        clearTimeout(c.__pin);
        c.__pin = setTimeout(function () { c.style.transition = 'none'; c.style.opacity = '1'; }, 850);
      } else {
        if (!c.__on) return; c.__on = false;
        clearTimeout(c.__pin);
        c.classList.remove('in'); c.style.transition = ''; c.style.opacity = '';
      }
    }
    var tick = false;
    function upd() {
      var rect = sec.getBoundingClientRect();
      var vh = window.innerHeight || document.documentElement.clientHeight;
      var prog = (vh - rect.top) / (rect.height || 1);
      cards.forEach(function (c, i) { setCard(c, prog >= th[i]); });
      tick = false;
    }
    window.addEventListener('scroll', function () {
      if (!tick) { requestAnimationFrame(upd); tick = true; }
    }, { passive: true });
    window.addEventListener('resize', upd);
    upd();
  })();

  /* stacking cards: scrub scale-down + fade on the card behind as the
     next slides over (GSAP-style effect, original scroll code) */
  (function () {
    var cards = document.querySelectorAll('.hiw-card');
    if (cards.length < 2) return;
    var tick = false;
    function upd() {
      var vh = window.innerHeight || document.documentElement.clientHeight;
      for (var i = 0; i < cards.length - 1; i++) {
        var next = cards[i + 1];
        var nr = next.getBoundingClientRect();
        var p = (vh - nr.top) / vh;
        p = Math.max(0, Math.min(1, p));
        var scale = (1 - p * 0.12).toFixed(4);
        var op = (1 - p * 0.4).toFixed(3);
        cards[i].style.transformOrigin = 'center top';
        cards[i].style.transform = 'scale(' + scale + ')';
        cards[i].style.opacity = op;
      }
      tick = false;
    }
    window.addEventListener('scroll', function () { if (!tick) { requestAnimationFrame(upd); tick = true; } }, { passive: true });
    window.addEventListener('resize', upd);
    upd();
  })();
  function revealFrame(el) { el.classList.add('revealed'); }

  reveal('.framed', revealFrame, { threshold: 0.12 });

  reveal('.reveal-heading', revealHeading, { threshold: 0.2 });
  reveal('.reveal-section', revealChildren, { threshold: 0.12 });
  reveal('.usp .row', revealUsp, { threshold: 0.15 });
  reveal('.starts-here', revealCard, { threshold: 0.3 });
  reveal('.step', revealStep, { threshold: 0.2 });
  reveal('.pd-main, .pd-side, .contact-form', addIn, { threshold: 0.15 });
  reveal('.carousel-track', revealCarousel, { threshold: 0.05 });
  reveal('.labtour-imgs .img-placeholder', addIn, { threshold: 0.15 });
  reveal('.footer-lead, .footer-nav-large, .footer-right', revealFooter, { threshold: 0.1 });

  /* ---------- 9. cinematic shots (fade in AND out) ---------- */
  var shotObserver = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      var overlay = e.target.querySelector('.shot-overlay');
      if (!overlay) return;
      if (e.isIntersecting && e.intersectionRatio > 0.3) {
        overlay.style.opacity = '1';
        overlay.style.transform = 'translateY(0)';
      } else {
        overlay.style.opacity = '0';
        overlay.style.transform = 'translateY(20px)';
      }
    });
  }, { threshold: [0, 0.3, 0.7, 1], rootMargin: '-10% 0px -10% 0px' });
  document.querySelectorAll('.cinematic-shot').forEach(function (el) { shotObserver.observe(el); });

  /* ---------- 10. (footer reveal handled by reveal() core) ---------- */

  /* ---------- 11. nav scrolled state + parallax ---------- */
  var nav = document.querySelector('.global-nav');
  var heroEl = document.querySelector('.hero, .page-hero');
  var heroBg = document.querySelector('.hero-bg, .page-hero .ph-bg');
  var heroHeight = heroEl ? heroEl.offsetHeight : window.innerHeight;
  var ticking = false;

  function onScroll() {
    if (!ticking) {
      window.requestAnimationFrame(function () {
        var y = window.scrollY;
        if (nav) {
          if (y > heroHeight * 0.85) nav.classList.add('scrolled');
          else nav.classList.remove('scrolled');
        }
        if (heroBg && !reduced && y < heroHeight) {
          heroBg.style.transform = 'translateY(' + (y * 0.15) + 'px)';
        }
        ticking = false;
      });
      ticking = true;
    }
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', function () { heroHeight = heroEl ? heroEl.offsetHeight : window.innerHeight; });
  onScroll();

  /* ---------- 12. mobile drawer ---------- */
  var hamburger = document.querySelector('.hamburger');
  var drawer = document.querySelector('.nav-drawer');
  var overlay = document.querySelector('.drawer-overlay');
  var closeBtn = document.querySelector('.drawer-close');
  function openDrawer() { if (drawer) { drawer.classList.add('open'); if (overlay) overlay.classList.add('show'); document.body.style.overflow = 'hidden'; } }
  function closeDrawer() { if (drawer) { drawer.classList.remove('open'); if (overlay) overlay.classList.remove('show'); document.body.style.overflow = ''; } }
  if (hamburger) hamburger.addEventListener('click', openDrawer);
  if (closeBtn) closeBtn.addEventListener('click', closeDrawer);
  if (overlay) overlay.addEventListener('click', closeDrawer);
  document.querySelectorAll('.nav-drawer a').forEach(function (a) { a.addEventListener('click', closeDrawer); });

  /* ---------- 13. carousel drag ---------- */
  document.querySelectorAll('.carousel-track').forEach(function (track) {
    var isDown = false, startX, scrollLeft;
    track.addEventListener('mousedown', function (e) {
      isDown = true; track.classList.add('dragging');
      startX = e.pageX - track.offsetLeft; scrollLeft = track.scrollLeft;
    });
    track.addEventListener('mouseleave', function () { isDown = false; track.classList.remove('dragging'); });
    track.addEventListener('mouseup', function () { isDown = false; track.classList.remove('dragging'); });
    track.addEventListener('mousemove', function (e) {
      if (!isDown) return; e.preventDefault();
      var x = e.pageX - track.offsetLeft;
      track.scrollLeft = scrollLeft - (x - startX) * 1.8;
    });
    track.addEventListener('touchstart', function (e) { startX = e.touches[0].pageX - track.offsetLeft; scrollLeft = track.scrollLeft; }, { passive: true });
    track.addEventListener('touchmove', function (e) {
      var x = e.touches[0].pageX - track.offsetLeft;
      track.scrollLeft = scrollLeft - (x - startX) * 1.8;
    }, { passive: true });
  });

  /* ---------- 14. project detail gallery dots ---------- */
  var dots = document.querySelectorAll('.pd-dots .dot');
  var slots = document.querySelectorAll('.pd-main .gallery-slot');
  if (dots.length) {
    dots.forEach(function (dot, i) {
      dot.addEventListener('click', function () {
        dots.forEach(function (d) { d.classList.remove('active'); });
        dot.classList.add('active');
        if (slots.length) {
          slots.forEach(function (s, si) { s.style.display = si === i ? 'flex' : 'none'; });
        }
      });
    });
  }

  /* ---------- 15. wizard ---------- */
  var steps = document.querySelectorAll('.wizard-step');
  var tabs = document.querySelectorAll('.wizard-tab');
  if (steps.length) {
    var current = 0;
    window.goToStep = function (index) {
      if (index === current || index < 0 || index >= steps.length) return;
      var forward = index > current;
      var outgoing = steps[current];
      outgoing.style.opacity = '0';
      outgoing.style.transform = 'translateX(' + (forward ? -40 : 40) + 'px)';
      var prev = current;
      current = index;
      setTimeout(function () {
        steps[prev].classList.remove('active');
        var incoming = steps[current];
        incoming.classList.add('active');
        incoming.style.transition = 'none';
        incoming.style.opacity = '0';
        incoming.style.transform = 'translateX(' + (forward ? 40 : -40) + 'px)';
        incoming.offsetHeight; // reflow
        window.requestAnimationFrame(function () {
          incoming.style.transition = 'opacity 0.5s ease, transform 0.6s cubic-bezier(0.16,1,0.3,1)';
          incoming.style.opacity = '1';
          incoming.style.transform = 'translateX(0)';
        });
        tabs.forEach(function (t, i) { t.classList.toggle('active', i === current); });
      }, 300);
    };
    tabs.forEach(function (t, i) { t.addEventListener('click', function () { window.goToStep(i); }); });
    document.querySelectorAll('[data-next]').forEach(function (b) { b.addEventListener('click', function () { window.goToStep(current + 1); }); });
    document.querySelectorAll('[data-prev]').forEach(function (b) { b.addEventListener('click', function () { window.goToStep(current - 1); }); });
  }

  /* prevent fake form submits */
  document.querySelectorAll('form').forEach(function (f) {
    f.addEventListener('submit', function (e) {
      e.preventDefault();
      var btn = f.querySelector('[type="submit"], .btn-primary');
      if (btn) { var t = btn.querySelector('.btn-label') || btn; var old = t.textContent; t.textContent = 'Message sent ✓'; setTimeout(function () { t.textContent = old; f.reset(); }, 2600); }
    });
  });

  /* ============================================================
     AUDIO ENGINE  ·  Mozart K.218 — II. Andante cantabile
     ============================================================ */
  var audio = new Audio('mozart-k218-andante.mp3');
  audio.loop = false;
  audio.volume = 0;
  var TARGET_VOL = 0.18;
  var audioStarted = false;
  var soundBars = document.getElementById('sound-bars');

  audio.addEventListener('timeupdate', function () { if (audio.currentTime >= 90) audio.currentTime = 0; });
  audio.addEventListener('ended', function () { audio.currentTime = 0; audio.play().catch(function () {}); });

  function barsPlaying() { if (soundBars) { soundBars.classList.remove('muted'); soundBars.classList.add('playing'); } }
  function barsMuted() { if (soundBars) { soundBars.classList.remove('playing'); soundBars.classList.add('muted'); } }

  function rampIn() {
    var vol = 0; audio.volume = 0;
    var t = setInterval(function () { vol = Math.min(vol + 0.006, TARGET_VOL); audio.volume = vol; if (vol >= TARGET_VOL) clearInterval(t); }, 100);
  }
  function fadeOutPause() {
    var t = setInterval(function () { audio.volume = Math.max(audio.volume - 0.018, 0); if (audio.volume <= 0) { audio.pause(); clearInterval(t); } }, 100);
  }
  function playAudio(ramp) {
    audio.play().then(function () { audioStarted = true; if (ramp) rampIn(); else audio.volume = TARGET_VOL; barsPlaying(); }).catch(function () {});
  }

  /* ---------- nav sound-bars toggle ---------- */
  var navAudioBtn = document.getElementById('nav-audio-toggle');
  if (navAudioBtn) {
    navAudioBtn.addEventListener('click', function (e) {
      e.preventDefault(); e.stopPropagation();
      if (!audioStarted || audio.paused) {
        playAudio(!audioStarted);
        localStorage.setItem('atharve-audio-pref', 'on');
      } else {
        fadeOutPause(); barsMuted();
        localStorage.setItem('atharve-audio-pref', 'off');
      }
    });
  }

  /* ---------- first-visit audio splash ---------- */
  var splashCss = '#audio-splash{position:fixed;inset:0;z-index:9999;background:#14130f;display:flex;align-items:center;justify-content:center;opacity:1}'
    + '.splash-inner{display:flex;flex-direction:column;align-items:center;gap:40px;text-align:center;padding:24px}'
    + '.splash-bars{display:flex;align-items:flex-end;gap:4px;height:32px}'
    + '.splash-bars span{display:block;width:3px;background:#f2efe6;border-radius:2px;animation:bar-idle 1.2s ease-in-out infinite alternate}'
    + '.splash-bars span:nth-child(1){height:10px;animation-delay:0s}.splash-bars span:nth-child(2){height:24px;animation-delay:.15s}.splash-bars span:nth-child(3){height:32px;animation-delay:.05s}.splash-bars span:nth-child(4){height:20px;animation-delay:.2s}.splash-bars span:nth-child(5){height:14px;animation-delay:.1s}'
    + '@keyframes bar-idle{from{transform:scaleY(.4);opacity:.5}to{transform:scaleY(1);opacity:1}}'
    + '.splash-inner p{font-family:"DM Mono",ui-monospace,monospace;font-size:14px;line-height:1.7;color:#f2efe6;letter-spacing:.04em;opacity:.85}'
    + '.splash-btns{display:flex;gap:16px}'
    + '#btn-no-audio,#btn-with-audio{font-family:"DM Mono",ui-monospace,monospace;font-size:12px;letter-spacing:.12em;text-transform:uppercase;padding:18px 36px;cursor:pointer;transition:background .3s ease,color .3s ease;border:1px solid #3a3830}'
    + '#btn-no-audio{background:#2a2820;color:#f2efe6}#btn-no-audio:hover{background:#3a3830}'
    + '#btn-with-audio{background:#ece7da;color:#1a1916;border-color:#ece7da}#btn-with-audio:hover{background:#f5f0e8}';

  var pref = localStorage.getItem('atharve-audio-pref');
  if (pref === 'on') barsPlaying(); else barsMuted();

  var audioChosen = localStorage.getItem('atharve-audio-chosen');
  if (!audioChosen) {
    var st = document.createElement('style'); st.textContent = splashCss; document.head.appendChild(st);
    var splash = document.createElement('div');
    splash.id = 'audio-splash';
    splash.innerHTML = '<div class="splash-inner"><div class="splash-bars"><span></span><span></span><span></span><span></span><span></span></div>'
      + '<p>For the best experience, we<br>recommend turning on your sound.</p>'
      + '<div class="splash-btns"><button id="btn-no-audio">Without audio</button><button id="btn-with-audio">With audio</button></div></div>';
    document.body.appendChild(splash);
    document.body.style.overflow = 'hidden';
    var dismiss = function () { splash.style.transition = 'opacity 0.6s ease'; splash.style.opacity = '0'; document.body.style.overflow = ''; setTimeout(function () { if (splash.parentNode) splash.remove(); }, 620); };
    splash.querySelector('#btn-no-audio').addEventListener('click', function () { localStorage.setItem('atharve-audio-chosen', 'off'); localStorage.setItem('atharve-audio-pref', 'off'); barsMuted(); dismiss(); });
    splash.querySelector('#btn-with-audio').addEventListener('click', function () { localStorage.setItem('atharve-audio-chosen', 'on'); localStorage.setItem('atharve-audio-pref', 'on'); playAudio(true); dismiss(); });
  }

  /* ---------- tab visibility: pause/resume seamlessly ---------- */
  function freezeBars() { if (soundBars) soundBars.querySelectorAll('span').forEach(function (s) { s.style.animationPlayState = 'paused'; }); }
  function unfreezeBars() { if (soundBars) soundBars.querySelectorAll('span').forEach(function (s) { s.style.animationPlayState = 'running'; }); }
  document.addEventListener('visibilitychange', function () {
    if (document.hidden) {
      if (!audio.paused) { audio.pause(); freezeBars(); sessionStorage.setItem('atharve-paused-by-visibility', 'true'); }
      document._origTitle = document.title; document.title = '— come back · Atharve®';
    } else {
      document.title = document._origTitle || 'Atharve Dahima · Portfolio';
      if (sessionStorage.getItem('atharve-paused-by-visibility') === 'true' && localStorage.getItem('atharve-audio-pref') === 'on') {
        audio.play().catch(function () {}); unfreezeBars(); sessionStorage.removeItem('atharve-paused-by-visibility');
      }
    }
  });
  window.addEventListener('blur', function () {
    if (!audio.paused) { audio.pause(); freezeBars(); sessionStorage.setItem('atharve-paused-by-visibility', 'true'); }
  });
  window.addEventListener('focus', function () {
    if (sessionStorage.getItem('atharve-paused-by-visibility') === 'true' && localStorage.getItem('atharve-audio-pref') === 'on') {
      audio.play().catch(function () {}); unfreezeBars(); sessionStorage.removeItem('atharve-paused-by-visibility');
    }
  });

  /* ---------- WhatsApp bubble: appear after 4s ---------- */
  setTimeout(function () {
    var wb = document.getElementById('wa-bubble');
    if (wb && !sessionStorage.getItem('wa-bubble-closed')) wb.classList.add('visible');
  }, 4000);
  var waClose = document.getElementById('wa-close');
  if (waClose) waClose.addEventListener('click', function () {
    var wb = document.getElementById('wa-bubble'); if (wb) wb.classList.remove('visible');
    sessionStorage.setItem('wa-bubble-closed', 'true');
  });
})();
