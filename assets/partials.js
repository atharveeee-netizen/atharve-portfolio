/* ============================================================
   SHARED PARTIALS — nav, drawer, footer, WhatsApp bubble
   Injected before app.js so observers can bind to them.
   ============================================================ */
(function () {
  var GH = 'https://github.com/atharveeee';
  var LI = 'https://linkedin.com/in/atharvedahima';
  var IG = 'https://www.instagram.com/atharveeee_4';
  var WA = 'https://wa.me/919983974154';
  var page = document.body.getAttribute('data-page') || '';

  var ghIcon = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 .5A11.5 11.5 0 0 0 .5 12a11.5 11.5 0 0 0 7.86 10.92c.58.1.79-.25.79-.56v-2c-3.2.7-3.88-1.37-3.88-1.37-.53-1.34-1.3-1.7-1.3-1.7-1.06-.72.08-.71.08-.71 1.17.08 1.79 1.2 1.79 1.2 1.04 1.79 2.73 1.27 3.4.97.1-.76.41-1.27.74-1.56-2.55-.29-5.23-1.28-5.23-5.7 0-1.26.45-2.29 1.19-3.1-.12-.29-.52-1.46.11-3.05 0 0 .97-.31 3.18 1.18a11 11 0 0 1 5.8 0c2.2-1.49 3.17-1.18 3.17-1.18.63 1.59.23 2.76.11 3.05.74.81 1.19 1.84 1.19 3.1 0 4.43-2.69 5.41-5.25 5.69.42.37.8 1.1.8 2.22v3.29c0 .31.21.67.8.56A11.5 11.5 0 0 0 23.5 12 11.5 11.5 0 0 0 12 .5Z"/></svg>';
  var liIcon = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M4.98 3.5A2.5 2.5 0 1 1 2.5 6 2.49 2.49 0 0 1 4.98 3.5ZM2.9 8.6h4.16V21H2.9ZM9.3 8.6h3.98v1.7h.06a4.36 4.36 0 0 1 3.93-2.16c4.2 0 4.98 2.77 4.98 6.37V21h-4.15v-5.5c0-1.31-.02-3-1.83-3-1.83 0-2.11 1.43-2.11 2.9V21H9.3Z"/></svg>';
  var waIcon = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.06L2 22l5.06-1.33A10 10 0 1 0 12 2Zm5.2 14.13c-.22.62-1.28 1.18-1.77 1.22-.47.04-.9.2-3.03-.63-2.55-1-4.17-3.6-4.3-3.77-.12-.17-1.03-1.37-1.03-2.61 0-1.24.65-1.85.88-2.1.23-.25.5-.31.67-.31l.48.01c.15 0 .36-.06.56.43.22.53.73 1.83.8 1.96.06.13.1.28.02.45-.08.17-.12.28-.24.43-.12.15-.25.33-.36.44-.12.12-.24.25-.1.49.13.24.6.98 1.28 1.59.88.78 1.61 1.02 1.85 1.14.24.12.38.1.52-.06.14-.17.6-.7.76-.94.16-.24.32-.2.54-.12.22.08 1.4.66 1.64.78.24.12.4.18.46.28.06.1.06.58-.16 1.2Z"/></svg>';

  var igIcon = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2.16c3.2 0 3.58.01 4.85.07 1.17.05 1.8.25 2.23.41.56.22.96.48 1.38.9.42.42.68.82.9 1.38.16.42.36 1.06.41 2.23.06 1.27.07 1.65.07 4.85s-.01 3.58-.07 4.85c-.05 1.17-.25 1.8-.41 2.23-.22.56-.48.96-.9 1.38-.42.42-.82.68-1.38.9-.42.16-1.06.36-2.23.41-1.27.06-1.65.07-4.85.07s-3.58-.01-4.85-.07c-1.17-.05-1.8-.25-2.23-.41a3.7 3.7 0 0 1-1.38-.9 3.7 3.7 0 0 1-.9-1.38c-.16-.42-.36-1.06-.41-2.23C2.17 15.58 2.16 15.2 2.16 12s.01-3.58.07-4.85c.05-1.17.25-1.8.41-2.23.22-.56.48-.96.9-1.38.42-.42.82-.68 1.38-.9.42-.16 1.06-.36 2.23-.41C8.42 2.17 8.8 2.16 12 2.16Zm0 1.62c-3.15 0-3.52.01-4.76.07-.9.04-1.39.19-1.71.32-.43.17-.74.37-1.06.69-.32.32-.52.63-.69 1.06-.13.32-.28.81-.32 1.71-.06 1.24-.07 1.61-.07 4.76s.01 3.52.07 4.76c.04.9.19 1.39.32 1.71.17.43.37.74.69 1.06.32.32.63.52 1.06.69.32.13.81.28 1.71.32 1.24.06 1.61.07 4.76.07s3.52-.01 4.76-.07c.9-.04 1.39-.19 1.71-.32.43-.17.74-.37 1.06-.69.32-.32.52-.63.69-1.06.13-.32.28-.81.32-1.71.06-1.24.07-1.61.07-4.76s-.01-3.52-.07-4.76c-.04-.9-.19-1.39-.32-1.71a2.85 2.85 0 0 0-.69-1.06 2.85 2.85 0 0 0-1.06-.69c-.32-.13-.81-.28-1.71-.32-1.24-.06-1.61-.07-4.76-.07Zm0 2.76a5.46 5.46 0 1 1 0 10.92 5.46 5.46 0 0 1 0-10.92Zm0 1.62a3.84 3.84 0 1 0 0 7.68 3.84 3.84 0 0 0 0-7.68Zm5.65-2.91a1.28 1.28 0 1 1 0 2.55 1.28 1.28 0 0 1 0-2.55Z"/></svg>';

  var navLinks = [
    ['How it works', 'index.html#how-it-works', 'how'],
    ['About', 'about.html', 'about'],
    ['Projects', 'projects.html', 'projects'],
    ['Lab Tour', 'labtour.html', 'labtour'],
    ['Contact', 'contact.html', 'contact']
  ];
  function centerLinks(cls) {
    return navLinks.map(function (l) {
      var active = l[2] === page ? ' active' : '';
      return '<a class="' + cls + active + '" href="' + l[1] + '">' + l[0] + '</a>';
    }).join('');
  }

  var nav =
    '<nav class="global-nav nav-load">' +
      '<div class="nav-cluster">' +
        '<a class="wordmark cell" href="index.html">atharve</a>' +
        '<button class="cell icon-cell audio-btn-nav" id="nav-audio-toggle" aria-label="Toggle background music" title="Toggle background music">' +
          '<span class="sound-bars muted" id="sound-bars"><span></span><span></span><span></span><span></span></span>' +
        '</button>' +
        '<a class="cell icon-cell" href="' + WA + '" target="_blank" rel="noopener" aria-label="WhatsApp">' + waIcon + '</a>' +
      '</div>' +
      '<div class="nav-center">' + centerLinks('nav-link') + '</div>' +
      '<div class="nav-right">' +
        '<a class="btn-nav" href="start.html"><span class="lbl">Request collab</span><span class="arrow-box">&rarr;</span></a>' +
        '<button class="hamburger" aria-label="Menu"><span></span><span></span><span></span></button>' +
      '</div>' +
    '</nav>' +
    '<aside class="nav-drawer">' +
      '<button class="drawer-close" aria-label="Close">&times;</button>' +
      centerLinks('') +
      '<a href="start.html">Request collab</a>' +
    '</aside>' +
    '<div class="drawer-overlay"></div>';

  // ---- footer large nav links (with active dot) ----
  var curPage = (window.location.pathname.split('/').pop() || 'index.html');
  if (curPage === '') curPage = 'index.html';
  var bigLinks = [
    ['Home', 'index.html'],
    ['Start a project', 'start.html'],
    ['How it works', 'index.html#how-it-works'],
    ['About', 'about.html'],
    ['Projects', 'projects.html'],
    ['Lab Tour', 'labtour.html'],
    ['Contact', 'contact.html']
  ];
  var bigNav = bigLinks.map(function (l) {
    var active = l[1] === curPage ? ' active' : '';
    var dot = active ? '<span class="active-dot">&#9679;</span>' : '';
    return '<a class="footer-nav-link' + active + '" href="' + l[1] + '">' + dot + l[0] + '</a>';
  }).join('');

  var footer =
    '<footer class="global-footer reveal-heading">' +
      '<div class="wrap footer-grid">' +
        '<div class="footer-lead">' +
          '<h2 class="display" style="text-transform:none">' +
            '<span class="line-mask"><span class="line-inner">Building hardware?</span></span>' +
            '<span class="line-mask"><span class="line-inner ital">Atharve engineers it.</span></span>' +
          '</h2>' +
          '<a class="btn-primary footer-cta" href="start.html">Request collab <span class="arrow">&rarr;</span></a>' +
          '<div class="footer-wordmark">atharve</div>' +
          '<p class="footer-sub">No agency fees, direct collaboration, and a response within 48 hours.</p>' +
        '</div>' +
        '<nav class="footer-nav-large">' + bigNav + '</nav>' +
        '<div class="footer-right">' +
          '<div class="footer-section">' +
            '<h4>Contact details</h4>' +
            '<a href="mailto:atharveeee@gmail.com">atharveeee@gmail.com</a>' +
            '<a href="tel:+919983974154">+91-9983974154</a>' +
          '</div>' +
          '<div class="footer-section">' +
            '<h4>WhatsApp</h4>' +
            '<div class="social-row"><a class="social-box" href="' + WA + '" target="_blank" rel="noopener" aria-label="WhatsApp">' + waIcon + '</a></div>' +
          '</div>' +
          '<div class="footer-section">' +
            '<h4>Address</h4>' +
            '<span>Rashtriya Raksha University,</span>' +
            '<span>Lavad, Gujarat</span>' +
          '</div>' +
          '<div class="footer-section">' +
            '<h4>Follow us</h4>' +
            '<div class="social-row">' +
              '<a class="social-box" href="' + GH + '" target="_blank" rel="noopener" aria-label="GitHub">' + ghIcon + '</a>' +
              '<a class="social-box" href="' + LI + '" target="_blank" rel="noopener" aria-label="LinkedIn">' + liIcon + '</a>' +
              '<a class="social-box" href="' + IG + '" target="_blank" rel="noopener" aria-label="Instagram">' + igIcon + '</a>' +
            '</div>' +
          '</div>' +
        '</div>' +
        '<div class="footer-bottom">' +
          '<p>Atharve Dahima is a student engineer registered at Rashtriya Raksha University (RRU).</p>' +
          '<div class="footer-legal">' +
            '<a href="#">Privacy settings</a>' +
            '<a href="#">Privacy Policy</a>' +
            '<a href="#">Terms &amp; Conditions</a>' +
          '</div>' +
        '</div>' +
      '</div>' +
    '</footer>';

  // ---- WhatsApp chat bubble (bottom-right) ----
  var bubble =
    '<div class="wa-bubble" id="wa-bubble">' +
      '<button class="wa-close" id="wa-close" aria-label="Close">&#8854;</button>' +
      '<div class="wa-bubble-inner">' +
        '<div class="wa-avatar"><div class="wa-avatar-img">[ PHOTO:<br>Atharve ]</div></div>' +
        '<div class="wa-message"><p>Have a project idea or a question? Send me a WhatsApp message &mdash; I reply within 48 hours.</p></div>' +
        '<a href="' + WA + '" class="wa-action" target="_blank" rel="noopener" aria-label="Open WhatsApp">' + waIcon + '</a>' +
      '</div>' +
    '</div>';

  document.body.insertAdjacentHTML('afterbegin', nav);
  if (!document.body.hasAttribute('data-no-footer')) {
    var fp = document.getElementById('site-footer');
    if (fp) fp.outerHTML = footer;
    else document.body.insertAdjacentHTML('beforeend', footer);
  }
  document.body.insertAdjacentHTML('beforeend', bubble);

  window.__icons = { gh: ghIcon, li: liIcon, wa: waIcon };
})();
