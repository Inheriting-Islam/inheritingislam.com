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
     what is about to happen.

     Field-agnostic: it reads the form's own labels, so adding a field to the
     HTML adds it to the email with no JavaScript change. */
  document.querySelectorAll('form[data-to]').forEach(function (form) {
    var to = form.getAttribute('data-to');
    var note = form.querySelector('.formnote');

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var name = (form.querySelector('[name=name]') || {}).value || '';
      var email = (form.querySelector('[name=email]') || {}).value || '';
      name = name.trim(); email = email.trim();

      if (!name || email.indexOf('@') < 1) {
        if (note) {
          note.classList.remove('ok');
          note.textContent = 'Add your name and an email we can reply to, and we will open the message for you.';
        }
        var focus = name ? form.querySelector('[name=email]') : form.querySelector('[name=name]');
        if (focus) focus.focus();
        return;
      }

      var lines = ['Assalamu alaikum,', ''], message = '';
      form.querySelectorAll('input, select, textarea').forEach(function (el) {
        if (!el.name || el.type === 'submit') return;
        var label = form.querySelector('label[for="' + el.id + '"]');
        var key = label ? label.textContent.replace('*', '').trim() : el.name;
        if (el.type === 'checkbox') {
          if (el.checked) lines.push(key + ': yes');
        } else if (el.tagName === 'TEXTAREA') {
          if (el.value.trim()) message = key + ':\r\n' + el.value.trim();
        } else if (el.value.trim()) {
          lines.push(key + ': ' + el.value.trim());
        }
      });
      if (message) lines.push('', message);
      lines.push('');

      var subject = (form.getAttribute('data-subject') || 'Enquiry') + ' — ' + name;
      if (note) {
        note.classList.add('ok');
        note.textContent = 'Opening your email app with the message written out — press send. If nothing opens, write ' + to + ' directly.';
      }
      location.href = 'mailto:' + to +
        '?subject=' + encodeURIComponent(subject) +
        '&body=' + encodeURIComponent(lines.join('\r\n'));
    });
  });

  /* ---- year ---------------------------------------------------------- */
  var year = document.getElementById('year');
  if (year) year.textContent = new Date().getFullYear();
})();
