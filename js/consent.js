/* iwillnotlookaway.org — gestione del consenso cookie (GDPR, Linee guida Garante 10/6/2021)
 *
 * Al caricamento parte SOLO Umami (anonimo, senza cookie), che resta nell'<head> delle pagine.
 * Google Analytics 4 viene iniettato da loadTrackingScripts() SOLO se la scelta
 * salvata è 'accepted'. Prima del clic su «Accetto» non parte alcuna richiesta verso
 * googletagmanager.com o google-analytics.com.
 * v229 (13/11/2026): tolto Meta Pixel (nessuna campagna attiva); ID GA allineato alla proprietà attiva.
 * La pulizia di _fbp/_fbc resta, per chi aveva accettato prima della v229.
 *
 * Scelta salvata in localStorage, chiave "iwnla_consent", valore JSON:
 *   {"v":"accepted"|"rejected","ts":<ms epoch scelta>,"exp":<ms epoch scadenza>,"ver":2}
 * Durata: 180 giorni. Scaduta (o mancante, o nel vecchio formato "granted"/"denied") → banner di nuovo.
 *
 * Nessuna libreria esterna. Nessun cookie scritto da questo file.
 */
(function () {
  'use strict';

  var KEY = 'iwnla_consent';
  var VER = 2;
  var TTL = 180 * 24 * 60 * 60 * 1000; // 180 giorni
  var GA_IDS = ['G-9XSMGGT00Y'];

  // Pagina dell'informativa privacy e cookie (una per lingua). Da confermare quando la pagina è online.
  var PRIVACY_URL = {
    it: '/s/it/privacy.html', en: '/s/en/privacy.html', fr: '/s/fr/confidentialite.html',
    de: '/s/de/datenschutz.html', es: '/s/es/privacidad.html', pt: '/s/pt/privacidade.html',
    tr: '/s/tr/gizlilik.html', ar: '/s/ar/privacy.html', he: '/s/he/privacy.html'
  };

  var T = {
    it: {
      txt: 'Questo sito usa solo strumenti tecnici e Umami, che conta le visite in forma anonima e senza cookie. Solo se clicchi «Accetto» attiviamo anche Google Analytics 4, che usa cookie per misurare il traffico: i dati non vengono venduti e vanno solo a Google per questo scopo. Se clicchi «Rifiuto» o chiudi con la X, resta tutto com’è: nessun cookie di analisi o di profilazione. Puoi cambiare scelta quando vuoi da «Gestisci cookie», in fondo a ogni pagina.',
      link: 'Informativa privacy e cookie', ok: 'Accetto', no: 'Rifiuto',
      close: 'Chiudi e rifiuta i cookie facoltativi', label: 'Scelta sui cookie', manage: 'Gestisci cookie'
    },
    en: {
      txt: 'This site only uses technical tools and Umami, which counts visits anonymously and without cookies. Only if you click “Accept” do we also turn on Google Analytics 4, which uses cookies to measure traffic: data is not sold and goes only to Google for this purpose. If you click “Decline” or close with the X, nothing changes: no analytics or profiling cookies. You can change your choice at any time from “Manage cookies” at the bottom of every page.',
      link: 'Privacy and cookie policy', ok: 'Accept', no: 'Decline',
      close: 'Close and decline optional cookies', label: 'Cookie choice', manage: 'Manage cookies'
    },
    fr: {
      txt: 'Ce site n’utilise que des outils techniques et Umami, qui compte les visites de façon anonyme et sans cookies. C’est seulement si vous cliquez sur « J’accepte » que nous activons aussi Google Analytics 4, qui utilise des cookies pour mesurer le trafic : les données ne sont pas vendues et vont uniquement à Google à cette fin. Si vous cliquez sur « Je refuse » ou fermez avec le X, rien ne change : aucun cookie de mesure d’audience ni de profilage. Vous pouvez modifier votre choix à tout moment via « Gérer les cookies », en bas de chaque page.',
      link: 'Politique de confidentialité et cookies', ok: 'J’accepte', no: 'Je refuse',
      close: 'Fermer et refuser les cookies facultatifs', label: 'Choix des cookies', manage: 'Gérer les cookies'
    },
    de: {
      txt: 'Diese Website nutzt nur technische Hilfsmittel und Umami, das Besuche anonym und ohne Cookies zählt. Nur wenn Sie auf „Akzeptieren“ klicken, aktivieren wir zusätzlich Google Analytics 4, das Cookies verwendet, um den Datenverkehr zu messen: Daten werden nicht verkauft und gehen nur zu diesem Zweck an Google. Wenn Sie auf „Ablehnen“ klicken oder mit dem X schließen, bleibt alles, wie es ist: keine Analyse- oder Profiling-Cookies. Sie können Ihre Wahl jederzeit über „Cookies verwalten“ unten auf jeder Seite ändern.',
      link: 'Datenschutz- und Cookie-Hinweise', ok: 'Akzeptieren', no: 'Ablehnen',
      close: 'Schließen und optionale Cookies ablehnen', label: 'Cookie-Auswahl', manage: 'Cookies verwalten'
    },
    es: {
      txt: 'Este sitio solo usa herramientas técnicas y Umami, que cuenta las visitas de forma anónima y sin cookies. Solo si haces clic en «Acepto» activamos también Google Analytics 4, que usa cookies para medir el tráfico: los datos no se venden y van solo a Google para este fin. Si haces clic en «Rechazo» o cierras con la X, todo sigue igual: ninguna cookie de análisis ni de elaboración de perfiles. Puedes cambiar tu elección cuando quieras desde «Gestionar cookies», al final de cada página.',
      link: 'Política de privacidad y cookies', ok: 'Acepto', no: 'Rechazo',
      close: 'Cerrar y rechazar las cookies opcionales', label: 'Elección sobre cookies', manage: 'Gestionar cookies'
    },
    pt: {
      txt: 'Este site usa apenas ferramentas técnicas e o Umami, que conta as visitas de forma anónima e sem cookies. Só se clicar em «Aceito» ativamos também o Google Analytics 4, que usa cookies para medir o tráfego: os dados não são vendidos e vão apenas para a Google para este fim. Se clicar em «Recuso» ou fechar com o X, fica tudo como está: nenhum cookie de análise ou de definição de perfis. Pode alterar a sua escolha a qualquer momento em «Gerir cookies», no fundo de cada página.',
      link: 'Política de privacidade e cookies', ok: 'Aceito', no: 'Recuso',
      close: 'Fechar e recusar os cookies opcionais', label: 'Escolha sobre cookies', manage: 'Gerir cookies'
    },
    tr: {
      txt: 'Bu site yalnızca teknik araçları ve ziyaretleri anonim olarak, çerez kullanmadan sayan Umami’yi kullanır. Google Analytics 4’ü yalnızca “Kabul” düğmesine tıklarsanız etkinleştiririz; trafiği ölçmek için çerez kullanır. Veriler satılmaz, yalnızca bu amaçla Google’a gider. “Reddet” düğmesine tıklarsanız ya da X ile kapatırsanız hiçbir şey değişmez: analiz veya profil oluşturma çerezi kullanılmaz. Seçiminizi istediğiniz zaman her sayfanın altındaki “Çerezleri yönet” bağlantısından değiştirebilirsiniz.',
      link: 'Gizlilik ve çerez politikası', ok: 'Kabul', no: 'Reddet',
      close: 'Kapat ve isteğe bağlı çerezleri reddet', label: 'Çerez seçimi', manage: 'Çerezleri yönet'
    },
    ar: {
      txt: 'يستخدم هذا الموقع أدوات تقنية فقط، إضافة إلى Umami الذي يحصي الزيارات بشكل مجهول ومن دون ملفات تعريف الارتباط. ولا نفعّل Google Analytics 4، الذي يستخدم ملفات تعريف الارتباط لقياس حركة الزيارات، إلا إذا نقرت على «أوافق». لا تُباع البيانات، ولا تذهب إلا إلى Google لهذا الغرض. إذا نقرت على «أرفض» أو أغلقت الشريط بعلامة X، يبقى كل شيء كما هو: لا ملفات تعريف ارتباط للتحليل أو التنميط. يمكنك تغيير اختيارك في أي وقت من «إدارة ملفات تعريف الارتباط» أسفل كل صفحة.',
      link: 'سياسة الخصوصية وملفات تعريف الارتباط', ok: 'أوافق', no: 'أرفض',
      close: 'إغلاق ورفض ملفات تعريف الارتباط الاختيارية', label: 'اختيار ملفات تعريف الارتباط', manage: 'إدارة ملفات تعريف الارتباط'
    },
    he: {
      txt: 'האתר משתמש רק בכלים טכניים וב-Umami, שסופר ביקורים באופן אנונימי וללא עוגיות. רק אם תלחצו על „מסכים” נפעיל גם את Google Analytics 4, שמשתמש בעוגיות כדי למדוד את התנועה באתר: הנתונים אינם נמכרים ומועברים רק ל-Google למטרה זו. אם תלחצו על „דוחה” או תסגרו עם ה-X, שום דבר לא משתנה: אין עוגיות ניתוח או פרופיילינג. אפשר לשנות את הבחירה בכל עת דרך „ניהול עוגיות” בתחתית כל עמוד.',
      link: 'מדיניות פרטיות ועוגיות', ok: 'מסכים', no: 'דוחה',
      close: 'סגירה ודחיית עוגיות אופציונליות', label: 'בחירה לגבי עוגיות', manage: 'ניהול עוגיות'
    }
  };

  var lang = ((document.documentElement.getAttribute('lang') || 'it').slice(0, 2)).toLowerCase();
  if (!T[lang]) lang = 'en';
  var t = T[lang];
  var trackingLoaded = false;

  /* ---------- stato salvato ---------- */
  function readChoice() {
    var raw = null;
    try { raw = localStorage.getItem(KEY); } catch (e) { return null; }
    if (!raw) return null;
    var o = null;
    try { o = JSON.parse(raw); } catch (e) { o = null; }
    if (!o || o.ver !== VER || (o.v !== 'accepted' && o.v !== 'rejected') ||
        typeof o.exp !== 'number' || Date.now() > o.exp) {
      // formato vecchio ("granted"/"denied"), illeggibile o scaduto: si chiede di nuovo
      try { localStorage.removeItem(KEY); } catch (e) {}
      return null;
    }
    return o.v;
  }

  function saveChoice(v) {
    var now = Date.now();
    try { localStorage.setItem(KEY, JSON.stringify({ v: v, ts: now, exp: now + TTL, ver: VER })); } catch (e) {}
  }

  /* ---------- cookie di terze parti ---------- */
  var TP_COOKIE = /^(_ga|_ga_.+|_gid|_gat.*|_gcl_.+|_fbp|_fbc)$/;

  function deleteThirdPartyCookies() {
    var names = document.cookie.split(';').map(function (c) { return c.split('=')[0].trim(); })
      .filter(function (n) { return TP_COOKIE.test(n); });
    if (!names.length) return 0;
    var host = location.hostname, parts = host.split('.'), domains = [''];
    for (var i = 0; i < parts.length - 1; i++) {
      var d = parts.slice(i).join('.');
      domains.push('; domain=' + d, '; domain=.' + d);
    }
    names.forEach(function (n) {
      domains.forEach(function (d) {
        document.cookie = n + '=; expires=Thu, 01 Jan 1970 00:00:00 GMT; max-age=0; path=/' + d;
      });
    });
    return names.length;
  }

  /* ---------- Google Analytics 4: solo dopo «Accetto» ---------- */
  function loadTrackingScripts() {
    if (trackingLoaded || readChoice() !== 'accepted') return;
    trackingLoaded = true;

    // Google Analytics 4 (solo statistica: niente segnali pubblicitari)
    window.dataLayer = window.dataLayer || [];
    window.gtag = function () { window.dataLayer.push(arguments); };
    window.gtag('consent', 'default', {
      analytics_storage: 'granted', ad_storage: 'denied',
      ad_user_data: 'denied', ad_personalization: 'denied'
    });
    window.gtag('js', new Date());
    GA_IDS.forEach(function (id) {
      window.gtag('config', id, { allow_google_signals: false, allow_ad_personalization_signals: false });
    });
    var g = document.createElement('script');
    g.async = true;
    g.src = 'https://www.googletagmanager.com/gtag/js?id=' + encodeURIComponent(GA_IDS[0]);
    document.head.appendChild(g);

  }
  window.loadTrackingScripts = loadTrackingScripts;

  /* ---------- banner ---------- */
  var CSS =
    '#iwnla-ck{position:fixed;left:0;right:0;bottom:0;z-index:300;background:rgba(8,8,8,.98);' +
    'backdrop-filter:blur(8px);-webkit-backdrop-filter:blur(8px);border-top:1px solid var(--blood,#6b1414);' +
    'padding:22px 56px 20px 24px;display:none;justify-content:center;color:var(--dust,#8a8a8a)}' +
    '[dir="rtl"] #iwnla-ck{padding:22px 24px 20px 56px}' +
    '#iwnla-ck.on{display:flex}' +
    '#iwnla-ck .ck-in{max-width:760px;width:100%;display:flex;flex-direction:column;gap:14px;align-items:center}' +
    '#iwnla-ck .ck-txt{font-size:.85rem;line-height:1.6;margin:0;text-align:start}' +
    '#iwnla-ck .ck-txt a{color:var(--bone,#ece8e0);text-decoration:underline;text-underline-offset:3px}' +
    '#iwnla-ck .ck-txt a:hover{color:var(--glow,#a83030)}' +
    '#iwnla-ck .ck-btns{display:flex;gap:14px;flex-wrap:wrap;justify-content:center}' +
    '#iwnla-ck .ck-b{font-family:\'Source Serif 4\',serif;font-size:.72rem;font-weight:600;letter-spacing:.15em;' +
    'text-transform:uppercase;cursor:pointer;padding:10px 0;width:170px;color:var(--bone,#ece8e0);' +
    'background:none;border:1px solid var(--ember,#8b2020);transition:background .3s,border-color .3s}' +
    '#iwnla-ck .ck-b:hover,#iwnla-ck .ck-b:focus-visible{background:var(--blood,#6b1414);border-color:var(--glow,#a83030)}' +
    '#iwnla-ck .ck-x{position:absolute;top:10px;inset-inline-end:12px;width:36px;height:36px;line-height:1;' +
    'font-size:26px;font-family:Georgia,serif;color:var(--bone,#ece8e0);background:none;' +
    'border:1px solid var(--line,#2a2a2a);cursor:pointer;display:flex;align-items:center;justify-content:center;padding:0}' +
    '#iwnla-ck .ck-x:hover,#iwnla-ck .ck-x:focus-visible{border-color:var(--ember,#8b2020);color:#fff}' +
    '#iwnla-ck button:focus-visible,#iwnla-ck a:focus-visible{outline:2px solid var(--glow,#a83030);outline-offset:2px}' +
    '.iwnla-ck-manage{background:none;border:0;padding:0;font:inherit;color:inherit;text-decoration:underline;' +
    'text-underline-offset:3px;cursor:pointer}' +
    '@media(max-width:560px){#iwnla-ck .ck-b{width:auto;flex:1 1 0;min-width:120px}}' +
    '@media print{#iwnla-ck{display:none!important}}';

  var banner = null, openedFromManage = false;

  function build() {
    if (banner) return banner;
    var st = document.createElement('style');
    st.id = 'iwnla-ck-css';
    st.textContent = CSS;
    document.head.appendChild(st);

    banner = document.createElement('div');
    banner.id = 'iwnla-ck';
    banner.setAttribute('role', 'region');
    banner.setAttribute('aria-label', t.label);
    banner.innerHTML =
      '<button type="button" class="ck-x" aria-label="' + t.close + '" title="' + t.close + '">&times;</button>' +
      '<div class="ck-in">' +
        '<p class="ck-txt"></p>' +
        '<div class="ck-btns">' +
          '<button type="button" class="ck-b" data-ck="accepted"></button>' +
          '<button type="button" class="ck-b" data-ck="rejected"></button>' +
        '</div>' +
      '</div>';
    var p = banner.querySelector('.ck-txt');
    p.appendChild(document.createTextNode(t.txt + ' '));
    var a = document.createElement('a');
    a.href = PRIVACY_URL[lang] || PRIVACY_URL.en;
    a.textContent = t.link;
    p.appendChild(a);
    p.appendChild(document.createTextNode('.'));
    banner.querySelector('[data-ck="accepted"]').textContent = t.ok;
    banner.querySelector('[data-ck="rejected"]').textContent = t.no;

    banner.querySelector('.ck-x').addEventListener('click', function () { choose('rejected'); });
    banner.querySelectorAll('.ck-b').forEach(function (b) {
      b.addEventListener('click', function () { choose(b.getAttribute('data-ck')); });
    });
    document.body.appendChild(banner);
    return banner;
  }

  function show(fromManage) {
    build();
    openedFromManage = !!fromManage;
    banner.classList.add('on');
    if (fromManage) { var f = banner.querySelector('.ck-b'); if (f) f.focus(); }
  }

  function hide() { if (banner) banner.classList.remove('on'); }

  function choose(v) {
    var before = readChoice();
    saveChoice(v);
    hide();
    if (v === 'accepted') {
      loadTrackingScripts();
    } else {
      deleteThirdPartyCookies();
      // GA era già in memoria in questa pagina: si ricarica per toglierli davvero
      if (before === 'accepted' || trackingLoaded) location.reload();
    }
  }

  /* ---------- «Gestisci cookie» nel footer ---------- */
  function wireManage() {
    var els = document.querySelectorAll('[data-iwnla-cookie]');
    for (var i = 0; i < els.length; i++) {
      els[i].textContent = t.manage;
      els[i].addEventListener('click', function (e) { e.preventDefault(); show(true); });
    }
  }
  window.iwnlaManageCookies = function () { show(true); };

  /* ---------- avvio ---------- */
  function init() {
    var c = readChoice();
    if (c === 'accepted') {
      loadTrackingScripts();
    } else {
      // nessuna scelta valida o rifiuto: via eventuali cookie rimasti (anche da versioni precedenti del sito)
      deleteThirdPartyCookies();
      if (c === null) show(false);
    }
    if (!document.getElementById('iwnla-ck-css')) build();
    wireManage();
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
