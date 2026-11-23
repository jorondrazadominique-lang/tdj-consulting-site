(function () {
  'use strict';

  document.querySelectorAll('.year').forEach(function (el) { el.textContent = new Date().getFullYear(); });

  /* ---- onglets des pages activité : centrer l'onglet courant */
  var strip = document.querySelector('.tab-strip');
  var cur = strip && strip.querySelector('[aria-current="page"]');
  if (cur) strip.scrollLeft = cur.offsetLeft - (strip.clientWidth - cur.offsetWidth) / 2;

  /* ---- menu mobile */
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.getElementById('main-nav');
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open);
      toggle.textContent = open ? 'Fermer' : 'Menu';
      document.body.classList.toggle('nav-open', open);
    });
    nav.addEventListener('click', function (e) {
      if (e.target.closest('a') && nav.classList.contains('open')) toggle.click();
    });
  }

  /* ---- menu Activités */
  var menuBtn = document.querySelector('.menu-btn');
  var mega = document.getElementById('menu-activites');
  if (menuBtn && mega) {
    var setMenu = function (open) {
      mega.hidden = !open;
      menuBtn.setAttribute('aria-expanded', open);
    };
    menuBtn.addEventListener('click', function () { setMenu(mega.hidden); });
    document.addEventListener('click', function (e) {
      if (!mega.hidden && !e.target.closest('.has-menu') && window.innerWidth > 900) setMenu(false);
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && !mega.hidden) { setMenu(false); menuBtn.focus(); }
    });
    var li = menuBtn.parentElement, t;
    li.addEventListener('mouseenter', function () { if (window.matchMedia('(hover:hover) and (min-width:901px)').matches) { clearTimeout(t); setMenu(true); } });
    li.addEventListener('mouseleave', function () { if (window.matchMedia('(hover:hover) and (min-width:901px)').matches) { t = setTimeout(function () { setMenu(false); }, 180); } });
  }

  /* ---- jeu de barres : onglets des activités */
  var tablist = document.querySelector('.bus-list');
  if (tablist) {
    var tabs = Array.prototype.slice.call(tablist.querySelectorAll('[role="tab"]'));
    var select = function (tab, focus) {
      tabs.forEach(function (t) {
        var on = t === tab;
        t.setAttribute('aria-selected', on);
        t.tabIndex = on ? 0 : -1;
        document.getElementById(t.getAttribute('aria-controls')).hidden = !on;
      });
      if (focus) tab.focus();
    };
    tabs.forEach(function (tab, i) {
      tab.addEventListener('click', function () { select(tab, false); });
      tab.addEventListener('keydown', function (e) {
        var k = e.key, j = null;
        if (k === 'ArrowDown' || k === 'ArrowRight') j = (i + 1) % tabs.length;
        if (k === 'ArrowUp' || k === 'ArrowLeft') j = (i - 1 + tabs.length) % tabs.length;
        if (k === 'Home') j = 0;
        if (k === 'End') j = tabs.length - 1;
        if (j !== null) { e.preventDefault(); select(tabs[j], true); }
      });
    });
  }

  /* ---- formulaire : e-mail pré-rempli */
  var form = document.getElementById('contact-form');
  if (form) {
    var sujet = new URLSearchParams(location.search).get('sujet');
    if (sujet && form.subject.querySelector('option[value="' + sujet + '"]')) form.subject.value = sujet;

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var note = document.getElementById('form-note');
      var missing = [];
      ['name', 'email', 'message'].forEach(function (n) {
        var f = form[n], bad = !f.value.trim() || (n === 'email' && !/^\S+@\S+\.\S+$/.test(f.value.trim()));
        f.setAttribute('aria-invalid', bad);
        if (bad) missing.push(f);
      });
      if (missing.length) {
        note.textContent = 'Renseignez votre nom, une adresse e-mail valide et une description du projet.';
        missing[0].focus();
        return;
      }
      var v = function (n) { return form[n].value.trim(); };
      var label = form.subject.options[form.subject.selectedIndex].text;
      var lines = [
        'Nom : ' + v('name'),
        'E-mail : ' + v('email'),
        v('phone') ? 'Téléphone : ' + v('phone') : null,
        'Activité : ' + label,
        v('lieu') ? 'Lieu du projet : ' + v('lieu') : null,
        v('delai') ? 'Échéance souhaitée : ' + v('delai') : null,
        '',
        v('message')
      ].filter(function (x) { return x !== null; });
      window.location.href = 'mailto:jorondrazadominique@gmail.com?subject=' +
        encodeURIComponent('Demande TDJ Consulting · ' + label + ' · ' + v('name')) +
        '&body=' + encodeURIComponent(lines.join('\n'));
      note.textContent = 'Votre messagerie s\'ouvre avec la demande prête à envoyer. Rien ne s\'ouvre ? Écrivez à jorondrazadominique@gmail.com ou sur WhatsApp.';
    });
  }
})();
