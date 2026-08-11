/* Inheriting Islam — the only script on the site.
   Theme, navigation, reveal-on-scroll, and a mailto composer. No trackers, no
   third-party calls, nothing that phones home. */
(function () {
  'use strict';
  var root = document.documentElement;

  /* ---- theme -------------------------------------------------------- */
  var toggle = document.getElementById('themeToggle');
  if (toggle) {
    toggle.addEventListener('click', function () {
      var next = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
      root.setAttribute('data-theme', next);
      toggle.setAttribute('aria-label', next === 'dark' ? 'Switch to light theme' : 'Switch to dark theme');
      try { localStorage.setItem('ii-theme', next); } catch (e) {}
    });
  }

  /* ---- header ------------------------------------------------------- */
  var header = document.getElementById('header');
  if (header) {
    var onScroll = function () { header.classList.toggle('is-stuck', window.scrollY > 8); };
    onScroll();
    addEventListener('scroll', onScroll, { passive: true });
  }

  /* ---- mobile nav --------------------------------------------------- */
  var navBtn = document.getElementById('navToggle');
  var navPanel = document.getElementById('mobileNav');
  function closeNav() {
    if (!navBtn) return;
    navBtn.setAttribute('aria-expanded', 'false');
    navPanel.classList.remove('open');
    document.body.classList.remove('nav-lock');
  }
  if (navBtn && navPanel) {
    navBtn.addEventListener('click', function () {
      var open = navBtn.getAttribute('aria-expanded') !== 'true';
      navBtn.setAttribute('aria-expanded', String(open));
      navPanel.classList.toggle('open', open);
      document.body.classList.toggle('nav-lock', open);
    });
    navPanel.querySelectorAll('a').forEach(function (a) { a.addEventListener('click', closeNav); });
    addEventListener('keydown', function (e) { if (e.key === 'Escape') closeNav(); });
  }

  /* ---- reveal ------------------------------------------------------- */
  var reveals = document.querySelectorAll('.reveal');
  if (matchMedia('(prefers-reduced-motion: reduce)').matches || !('IntersectionObserver' in window)) {
    reveals.forEach(function (el) { el.classList.add('in'); });
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) { entry.target.classList.add('in'); io.unobserve(entry.target); }
      });
    }, { rootMargin: '0px 0px -6% 0px', threshold: 0.06 });
    reveals.forEach(function (el) { io.observe(el); });
  }

  /* ---- copy-to-clipboard -------------------------------------------- */
  document.querySelectorAll('[data-copy]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var text = btn.getAttribute('data-copy');
      var done = function () {
        var was = btn.textContent;
        btn.textContent = 'Copied';
        setTimeout(function () { btn.textContent = was; }, 1600);
      };
      if (navigator.clipboard) { navigator.clipboard.writeText(text).then(done, function () {}); }
      else {
        var t = document.createElement('textarea');
        t.value = text; document.body.appendChild(t); t.select();
        try { document.execCommand('copy'); done(); } catch (e) {}
        document.body.removeChild(t);
      }
    });
  });

  /* ---- mailto composer ----------------------------------------------
     There is no form backend. Rather than pretend, we compose a complete,
     well-formatted email in the visitor's own mail app and tell them exactly
     what is about to happen. */
  var form = document.getElementById('contactForm');
  if (form) {
    var note = document.getElementById('formNote');
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var d = new FormData(form);
      var val = function (k) { return (d.get(k) || '').toString().trim(); };
      var name = val('name'), email = val('email');
      if (!name || email.indexOf('@') < 1) {
        if (note) { note.classList.remove('ok'); note.textContent = 'Add your name and an email we can reply to, and we will open the message for you.'; }
        (name ? form.querySelector('[name=email]') : form.querySelector('[name=name]')).focus();
        return;
      }
      var subject = (val('need') || 'Inquiry') + (val('org') ? ' — ' + val('org') : ' — ' + name);
      var lines = [
        'Assalamu alaikum Hamza,', '',
        'Name: ' + name,
        'Organization: ' + (val('org') || '—'),
        'Type: ' + (val('kind') || '—'),
        'Email: ' + email,
        'Phone: ' + (val('phone') || '—'),
        'Current website: ' + (val('site') || '—'),
        'What we need: ' + (val('need') || '—'),
        'Timing: ' + (val('timing') || '—'),
        'Budget: ' + (val('budget') || '—'),
        '', (val('message') || ''), ''
      ];
      var href = 'mailto:' + form.getAttribute('data-to') +
        '?subject=' + encodeURIComponent(subject) +
        '&body=' + encodeURIComponent(lines.join('\r\n'));
      if (note) {
        note.classList.add('ok');
        note.textContent = 'Opening your email app with the message written out — press send. If nothing opens, write ' + form.getAttribute('data-to') + ' directly.';
      }
      location.href = href;
    });
  }

  /* ---- year ---------------------------------------------------------- */
  var year = document.getElementById('year');
  if (year) year.textContent = new Date().getFullYear();
})();
