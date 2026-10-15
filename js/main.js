(function () {
  var burger = document.getElementById('burger');
  var nav = document.getElementById('nav');
  var links = nav.querySelectorAll('a:not(.btn)');

  function closeMenu() {
    nav.classList.remove('is-open');
    burger.setAttribute('aria-expanded', 'false');
  }
  burger.addEventListener('click', function () {
    var open = nav.classList.toggle('is-open');
    burger.setAttribute('aria-expanded', String(open));
  });
  nav.addEventListener('click', function (e) {
    if (e.target.closest('a')) closeMenu();
  });

  // link ativo conforme a seção visível
  var map = {};
  links.forEach(function (a) { map[a.getAttribute('href').slice(1)] = a; });
  if ('IntersectionObserver' in window) {
    var spy = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting && map[en.target.id]) {
          links.forEach(function (l) { l.classList.remove('is-active'); });
          map[en.target.id].classList.add('is-active');
        }
      });
    }, { rootMargin: '-45% 0px -50% 0px' });
    Object.keys(map).forEach(function (id) {
      var el = document.getElementById(id);
      if (el) spy.observe(el);
    });

    // animação de entrada
    var targets = document.querySelectorAll('.card, .combo, .quote, .badge, .footer__cols > *');
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add('is-in'); io.unobserve(en.target); }
      });
    }, { threshold: 0.12 });
    targets.forEach(function (el, i) {
      el.classList.add('reveal');
      el.style.transitionDelay = (i % 4) * 80 + 'ms';
      io.observe(el);
    });
  }

  // abas do cardápio completo (sem JS, todas as categorias ficam visíveis)
  var tabs = document.querySelectorAll('.tab[data-tab]');
  var panels = document.querySelectorAll('.mpanel');
  function openTab(key) {
    tabs.forEach(function (t) { t.setAttribute('aria-selected', String(t.dataset.tab === key)); });
    panels.forEach(function (p) { p.hidden = p.dataset.panel !== key; });
  }
  if (tabs.length) {
    openTab(tabs[0].dataset.tab);
    tabs.forEach(function (t) {
      t.addEventListener('click', function () { openTab(t.dataset.tab); });
    });
    document.querySelectorAll('[data-open-tab]').forEach(function (a) {
      a.addEventListener('click', function () { openTab(a.dataset.openTab); });
    });
    // links antigos (ex.: /batata.html -> /?aba=batatas#cardapio-completo) abrem a aba certa
    var aba = new URLSearchParams(location.search).get('aba');
    if (aba && document.getElementById('t-' + aba)) openTab(aba);
  }

  document.getElementById('ano').textContent = new Date().getFullYear();
})();
