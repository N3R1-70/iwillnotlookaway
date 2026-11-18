/* search.js — ricerca libera negli articoli di iwillnotlookaway.org
   Indice: /data/search/{lang}.json (generato da build_search.py), caricato solo
   alla prima interazione con la casella. Nessuna dipendenza esterna. */
(function () {
  'use strict';
  var L = {
    it: { ph: 'Cerca negli articoli…', one: '1 articolo', many: '%n articoli', none: 'Nessun articolo contiene «%q».', more: 'Mostra altri', load: 'Carico l’indice…', err: 'Ricerca non disponibile al momento.', short: 'Scrivi almeno due lettere.' },
    en: { ph: 'Search the articles…', one: '1 article', many: '%n articles', none: 'No article contains “%q”.', more: 'Show more', load: 'Loading the index…', err: 'Search is unavailable right now.', short: 'Type at least two letters.' },
    fr: { ph: 'Rechercher dans les articles…', one: '1 article', many: '%n articles', none: 'Aucun article ne contient « %q ».', more: 'Afficher plus', load: 'Chargement de l’index…', err: 'Recherche indisponible pour le moment.', short: 'Saisissez au moins deux lettres.' },
    de: { ph: 'In den Artikeln suchen…', one: '1 Artikel', many: '%n Artikel', none: 'Kein Artikel enthält „%q“.', more: 'Mehr anzeigen', load: 'Index wird geladen…', err: 'Suche derzeit nicht verfügbar.', short: 'Mindestens zwei Buchstaben eingeben.' },
    es: { ph: 'Buscar en los artículos…', one: '1 artículo', many: '%n artículos', none: 'Ningún artículo contiene «%q».', more: 'Mostrar más', load: 'Cargando el índice…', err: 'Búsqueda no disponible en este momento.', short: 'Escribe al menos dos letras.' },
    pt: { ph: 'Pesquisar nos artigos…', one: '1 artigo', many: '%n artigos', none: 'Nenhum artigo contém «%q».', more: 'Mostrar mais', load: 'A carregar o índice…', err: 'Pesquisa indisponível de momento.', short: 'Escreva pelo menos duas letras.' },
    tr: { ph: 'Makalelerde ara…', one: '1 makale', many: '%n makale', none: '“%q” içeren makale yok.', more: 'Daha fazla göster', load: 'Dizin yükleniyor…', err: 'Arama şu anda kullanılamıyor.', short: 'En az iki harf yazın.' },
    zh: { ph: '在文章中搜索…', one: '1 篇文章', many: '%n 篇文章', none: '没有文章包含「%q」。', more: '显示更多', load: '正在加载索引…', err: '搜索暂时不可用。', short: '请至少输入两个字母。' },
    ar: { ph: 'ابحث في المقالات…', one: 'مقال واحد', many: 'عدد المقالات: %n', none: 'لا يوجد مقال يحتوي على «%q».', more: 'عرض المزيد', load: 'جارٍ تحميل الفهرس…', err: 'البحث غير متاح حاليًا.', short: 'اكتب حرفين على الأقل.' },
    he: { ph: 'חיפוש במאמרים…', one: 'מאמר אחד', many: '%n מאמרים', none: 'אין מאמר שמכיל „%q”.', more: 'הצג עוד', load: 'טוען את האינדקס…', err: 'החיפוש אינו זמין כרגע.', short: 'הקלידו לפחות שתי אותיות.' },
    ru: { ph: 'Поиск по статьям…', one: '1 статья', many: 'Статей: %n', none: 'Ни одна статья не содержит «%q».', more: 'Показать ещё', load: 'Загрузка индекса…', err: 'Поиск сейчас недоступен.', short: 'Введите не менее двух букв.' }
  };
  var lang = (document.documentElement.lang || 'it').slice(0, 2);
  var S = L[lang] || L.en;
  var PAGE = 5;

  function norm(s) {
    s = s.toLocaleLowerCase(lang === 'tr' ? 'tr' : undefined).normalize('NFD');
    return s
      .replace(/[̀-֑ͯ-ׇً-ٰٟـ]/g, '')
      .replace(/ı/g, 'i').replace(/ß/g, 'ss')
      .replace(/[‘’ʼ`´]/g, "'").replace(/[“”«»„]/g, '"')
      .replace(/[أإآٱ]/g, 'ا').replace(/ة/g, 'ه').replace(/ى/g, 'ي');
  }
  // normalizzazione carattere per carattere, con mappa verso il testo originale
  function normMap(s) {
    var out = '', map = [];
    for (var i = 0; i < s.length; i++) {
      var n = norm(s[i]);
      for (var k = 0; k < n.length; k++) { out += n[k]; map.push(i); }
    }
    map.push(s.length);
    return { s: out, map: map };
  }
  function esc(s) { return s.replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function tokens(q) {
    var t = norm(q).replace(/["]/g, ' ').split(/[\s,;:.!?()\[\]]+/).filter(function (x) { return x.length > 0; });
    // tolgo i duplicati
    return t.filter(function (x, i) { return t.indexOf(x) === i; });
  }
  function count(hay, t, cap) {
    var n = 0, p = hay.indexOf(t);
    while (p >= 0 && n < cap) { n++; p = hay.indexOf(t, p + t.length); }
    return n;
  }
  function mark(text, toks) {
    var m = normMap(text), ranges = [];
    toks.forEach(function (t) {
      var p = m.s.indexOf(t);
      while (p >= 0) { ranges.push([m.map[p], m.map[p + t.length - 1] + 1]); p = m.s.indexOf(t, p + t.length); }
    });
    if (!ranges.length) return esc(text);
    ranges.sort(function (a, b) { return a[0] - b[0]; });
    var out = '', last = 0;
    ranges.forEach(function (r) {
      if (r[0] < last) { if (r[1] > last) { out += '<mark>' + esc(text.slice(last, r[1])) + '</mark>'; last = r[1]; } return; }
      out += esc(text.slice(last, r[0])) + '<mark>' + esc(text.slice(r[0], r[1])) + '</mark>';
      last = r[1];
    });
    return out + esc(text.slice(last));
  }
  function snippet(it, toks) {
    // il frammento viene dal testo; se i termini compaiono solo nella descrizione, da lì
    var inX = toks.filter(function (t) { return it.nx.indexOf(t) >= 0; });
    var src = inX.length ? it.x : it.d, nsrc = inX.length ? it.nx : it.nd;
    var tk = inX.length ? inX[0] : toks.filter(function (t) { return nsrc.indexOf(t) >= 0; })[0];
    var pos = tk ? nsrc.indexOf(tk) : -1;
    if (pos < 0) return esc((it.d || it.x).slice(0, 220));
    var off = Math.max(0, pos - 600), frag = src.slice(off, pos + 600), m = normMap(frag), p2 = m.s.indexOf(tk);
    if (p2 < 0) { off = 0; frag = src; m = normMap(src); p2 = m.s.indexOf(tk); }
    var at = m.map[Math.max(0, p2)];
    var a = Math.max(0, at - 70), b = Math.min(frag.length, at + 130);
    while (a > 0 && !/\s/.test(frag[a - 1])) a--;
    while (b < frag.length && !/\s/.test(frag[b])) b++;
    return (off + a > 0 ? '… ' : '') + mark(frag.slice(a, b).trim(), toks) + (off + b < src.length ? ' …' : '');
  }

  var CSS = '.sr-wrap{margin:0 0 22px}' +
    '.sr-box{position:relative}' +
    '.sr-input{width:100%;box-sizing:border-box;background:var(--surface);border:1px solid var(--line);color:var(--bone);padding:16px 18px 16px 46px;font-size:16px;font-family:inherit;outline:none;transition:border-color .3s;-webkit-appearance:none;border-radius:0}' +
    '[dir=rtl] .sr-input{padding:16px 46px 16px 18px}' +
    '.sr-input:focus{border-color:var(--ember)}' +
    '.sr-input::placeholder{color:var(--ash)}' +
    '.sr-ico{position:absolute;top:50%;left:17px;width:16px;height:16px;transform:translateY(-50%);pointer-events:none;color:var(--dust)}' +
    '[dir=rtl] .sr-ico{left:auto;right:17px}' +
    '.sr-status{font-size:.62rem;letter-spacing:.2em;text-transform:uppercase;color:var(--dust);margin:16px 0 10px;min-height:1em}.sr-status.sr-msg{font-size:.9rem;letter-spacing:0;text-transform:none;font-style:italic}' +
    '.sr-list{display:flex;flex-direction:column;gap:12px}' +
    '.sr-item{display:block;text-decoration:none;border:1px solid var(--line);background:var(--surface);padding:18px 20px;transition:border-color .3s}' +
    '.sr-item:hover,.sr-item:focus{border-color:var(--ember);outline:none}' +
    '.sr-cat{display:block;font-size:.6rem;letter-spacing:.2em;text-transform:uppercase;color:var(--ember);margin-bottom:8px}' +
    '.sr-title{display:block;font-family:"EB Garamond",serif;font-size:1.2rem;font-weight:700;line-height:1.25;color:var(--bone);margin-bottom:8px}' +
    '.sr-snip{display:block;font-size:.88rem;line-height:1.55;color:var(--pale)}' +
    '.sr-item mark{background:rgba(139,32,32,.45);color:var(--bone);padding:0 1px}' +
    '.sr-more{margin-top:14px}';

  function init(root) {
    if (root.getAttribute('data-ready')) return;
    root.setAttribute('data-ready', '1');
    var st = document.createElement('style'); st.textContent = CSS; document.head.appendChild(st);
    root.innerHTML = '<div class="sr-box"><svg class="sr-ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5"/></svg>' +
      '<input type="search" class="sr-input" enterkeyhint="search" autocomplete="off" spellcheck="false"/></div>' +
      '<p class="sr-status" aria-live="polite"></p><div class="sr-list"></div>' +
      '<button type="button" class="btn-secondary sr-more" hidden style="display:none"></button>';
    var inp = root.querySelector('.sr-input'), stat = root.querySelector('.sr-status'),
      list = root.querySelector('.sr-list'), more = root.querySelector('.sr-more');
    inp.placeholder = S.ph; inp.setAttribute('aria-label', S.ph); more.textContent = S.more;
    var base = root.getAttribute('data-base') || '';
    var DATA = null, loading = null, hits = [], shown = 0, toks = [], timer = null;

    function load() {
      if (DATA) return Promise.resolve(DATA);
      if (loading) return loading;
      var p = fetch(root.getAttribute('data-index') || '/data/search/' + lang + '.json').then(function (r) { if (!r.ok) throw 0; return r.json(); });
      loading = p.then(function (j) {
        DATA = j.items.map(function (a, i) {
          return { u: a[0], t: a[1], c: a[2], dt: a[3], d: a[4], x: a[5], i: i, nt: norm(a[1]), nd: norm(a[4]), nx: norm(a[5]) };
        });
        return DATA;
      });
      return loading;
    }
    function render() {
      var html = '';
      hits.slice(shown, shown + PAGE).forEach(function (h) {
        var it = h.it;
        html += '<a class="sr-item" href="' + esc(base + it.u) + '"><span class="sr-cat">' + esc(it.c) + (it.dt ? ' · ' + esc(it.dt) : '') + '</span>' +
          '<span class="sr-title">' + mark(it.t, toks) + '</span><span class="sr-snip">' + snippet(it, toks) + '</span></a>';
      });
      list.insertAdjacentHTML('beforeend', html);
      shown = Math.min(hits.length, shown + PAGE);
      var rest = shown < hits.length;
      more.hidden = !rest; more.style.display = rest ? 'inline-block' : 'none';
    }
    function run() {
      var q = inp.value.trim();
      list.innerHTML = ''; shown = 0; hits = [];
      more.hidden = true; more.style.display = 'none';
      if (!q) { stat.textContent = ''; return; }
      var cjk = /[぀-ヿ㐀-鿿]/.test(q);
      if (!cjk && q.length < 2) { stat.textContent = S.short; return; }
      stat.textContent = S.load;
      load().then(function (D) {
        if (inp.value.trim() !== q) return;
        toks = tokens(q);
        var phrase = norm(q);
        D.forEach(function (it) {
          var sc = 0;
          for (var k = 0; k < toks.length; k++) {
            var t = toks[k], a = count(it.nt, t, 5), b = count(it.nd, t, 5), c = count(it.nx, t, 20);
            if (!a && !b && !c) return;
            sc += a * 12 + b * 5 + c;
          }
          if (toks.length > 1) { if (it.nt.indexOf(phrase) >= 0) sc += 40; else if (it.nx.indexOf(phrase) >= 0) sc += 15; }
          hits.push({ it: it, s: sc });
        });
        hits.sort(function (x, y) { return y.s - x.s || x.it.i - y.it.i; });
        stat.className = 'sr-status' + (hits.length ? '' : ' sr-msg');
        stat.textContent = hits.length ? (hits.length === 1 ? S.one : S.many.replace('%n', hits.length)) : S.none.replace('%q', q);
        render();
      }).catch(function () { stat.textContent = S.err; });
    }
    inp.addEventListener('focus', function () { load().catch(function () {}); });
    inp.addEventListener('input', function () { clearTimeout(timer); timer = setTimeout(run, 220); });
    inp.addEventListener('keydown', function (e) {
      if (e.key === 'Enter') { clearTimeout(timer); run(); inp.blur(); }
      if (e.key === 'Escape') { inp.value = ''; run(); }
    });
    more.addEventListener('click', render);
    var q0 = (location.search.match(/[?&]q=([^&]+)/) || [])[1];
    if (q0) { try { inp.value = decodeURIComponent(q0.replace(/\+/g, ' ')); run(); } catch (e) {} }
  }
  function boot() { var r = document.querySelectorAll('[data-iwnla-search]'); for (var i = 0; i < r.length; i++) init(r[i]); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot); else boot();
})();
