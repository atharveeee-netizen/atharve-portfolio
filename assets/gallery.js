/* ============================================================
   MUSEUM GALLERY — sticky vertical scroll → horizontal glide
   with lerp smoothing + progress circle.
   ============================================================ */
(function () {
  var container = document.querySelector('.gallery-scroll-container');
  var track = document.querySelector('.gallery-track');
  var label = document.querySelector('.gallery-label');
  var hintText = document.querySelector('.gallery-hint span');
  var progFg = document.querySelector('.gallery-progress .fg');
  if (!container || !track) return;

  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var isMobile = window.matchMedia('(max-width: 768px)').matches;

  // progress circle setup
  var R = 20, CIRC = 2 * Math.PI * R;
  if (progFg) { progFg.style.strokeDasharray = CIRC; progFg.style.strokeDashoffset = CIRC; }

  function maxTranslate() {
    return Math.max(0, track.scrollWidth - window.innerWidth + window.innerWidth * 0.04);
  }

  // size the tall scroll container so there's room to scrub the whole track
  function sizeContainer() {
    if (isMobile) { container.style.height = 'auto'; return; }
    var dist = maxTranslate();
    container.style.height = (dist + window.innerHeight) + 'px';
  }

  var targetX = 0, currentX = 0, ticking = false;

  function computeTarget() {
    var rect = container.getBoundingClientRect();
    var total = container.offsetHeight - window.innerHeight;
    var progress = total > 0 ? Math.min(1, Math.max(0, -rect.top / total)) : 0;
    targetX = -(progress * maxTranslate());
    // label fades out over first 15%
    if (label) label.style.opacity = String(Math.max(0, 1 - progress * 6));
    if (hintText) hintText.style.opacity = String(Math.max(0, 1 - progress * 4));
    if (progFg) progFg.style.strokeDashoffset = String(CIRC * (1 - progress));
  }

  var smoothing = reduced ? 1 : 0.08;

  function raf() {
    currentX += (targetX - currentX) * smoothing;
    if (Math.abs(targetX - currentX) < 0.5) currentX = targetX;
    track.style.transform = 'translateX(' + currentX + 'px)';
    requestAnimationFrame(raf);
  }

  if (isMobile) {
    // no horizontal scrub on mobile — vertical stack fallback
    if (label) label.style.opacity = '1';
    return;
  }

  window.addEventListener('scroll', function () {
    if (!ticking) { requestAnimationFrame(function () { computeTarget(); ticking = false; }); ticking = true; }
  }, { passive: true });
  window.addEventListener('resize', function () { isMobile = window.matchMedia('(max-width: 768px)').matches; sizeContainer(); computeTarget(); });

  // wait for fonts so scrollWidth is accurate
  function init() { sizeContainer(); computeTarget(); raf(); }
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(init); else window.addEventListener('load', init);
  setTimeout(init, 400);
})();
