# -*- coding: utf-8 -*-
import re, os, html, json
import og_gen
REPO='/home/claude/repo'; BASE='https://iwillnotlookaway.org'
LANGS=['it','en','fr','de','es','pt','tr','zh','ar','he','ru']
RTL={'ar','he'}
SRC='/home/claude/repo_bak'
def fpath(l): return os.path.join(SRC,'index.html') if l=='it' else os.path.join(SRC,l,'index.html')
def plain(s): return re.sub(r'\s+',' ',html.unescape(re.sub('<[^>]+>','',s))).strip()
LOCALE={'it':'it_IT','en':'en_US','fr':'fr_FR','de':'de_DE','es':'es_ES','pt':'pt_PT','tr':'tr_TR','zh':'zh_CN','ar':'ar_AR','he':'he_IL'}
CAT_N={'it':'NOTIZIA','en':'NEWS','fr':'ACTUALITÉ','de':'NACHRICHT','es':'NOTICIA','pt':'NOTÍCIA','tr':'HABER','zh':'动态','ar':'خبر','he':'חדשות'}
CAT_M={'it':'MANIFESTO','en':'MANIFESTO','fr':'MANIFESTE','de':'MANIFEST','es':'MANIFIESTO','pt':'MANIFESTO','tr':'MANIFESTO','zh':'宣言','ar':'بيان','he':'מניפסט'}
OGCAT_M=CAT_M
BACK={'it':'Tutte le notizie e i manifesti','en':'All news and manifestos','fr':'Toutes les actualités et manifestes','de':'Alle Nachrichten und Manifeste','es':'Todas las noticias y manifiestos','pt':'Todas as notícias e manifestos','tr':'Tüm haberler ve manifestolar','zh':'全部动态与宣言','ar':'كل الأخبار والبيانات','he':'כל החדשות והמניפסטים'}
NLSUB={'it':'Una sintesi essenziale, solo quando un fatto lo merita.','en':'A concise digest, only when a fact deserves it.','fr':'Une synthèse essentielle, seulement quand un fait le mérite.','de':'Eine knappe Zusammenfassung, nur wenn ein Fakt es verdient.','es':'Una síntesis esencial, solo cuando un hecho lo merece.','pt':'Uma síntese essencial, só quando um facto o merece.','tr':'Yalnızca bir olgu hak ettiğinde, özlü bir özet.','zh':'只有当事实值得时，才发送一份精要摘要。','ar':'خلاصة موجزة، فقط حين يستحق الأمر ذلك.','he':'תקציר תמציתי, רק כשעובדה ראויה לכך.'}
NLBTN={'it':'Iscriviti alla newsletter','en':'Subscribe to the newsletter','fr':"S'inscrire à la newsletter",'de':'Newsletter abonnieren','es':'Suscríbete al boletín','pt':'Subscrever a newsletter','tr':'Bültene abone ol','zh':'订阅资讯邮件','ar':'اشترك في النشرة','he':'הרשמה לניוזלטר'}
def home(l): return '/' if l=='it' else '/%s/'%l
NAV=json.load(open('/home/claude/navlabels.json',encoding='utf-8'))
LANGLABEL={'it':'IT','en':'EN','fr':'FR','de':'DE','zh':'中文','ar':'AR','es':'ES','pt':'PT','tr':'TR','he':'עב'}
LANGORDER=['it','en','fr','de','zh','ar','es','pt','tr','he','ru']
NLSEC=json.load(open('/home/claude/nlsections.json',encoding='utf-8'))
NLJS=open('/home/claude/nlsub.js',encoding='utf-8').read()

# ---- news ISO dates from IT ----
MESI={'gennaio':'01','febbraio':'02','marzo':'03','aprile':'04','maggio':'05','giugno':'06','luglio':'07','agosto':'08','settembre':'09','ottobre':'10','novembre':'11','dicembre':'12'}
hit=open(fpath('it'),encoding='utf-8').read()
NEWS=re.findall(r'data-news="(nd-[^"]+)"',hit)
SHARES=re.findall(r'data-share-key="(m[^"]*)"',hit)
def news_iso(datestr):
    m=re.search(r'(\d{1,2})\s+(%s)\s+(\d{4})'%'|'.join(MESI),datestr.lower())
    if m: return '%s-%s-%02d'%(m.group(3),MESI[m.group(2)],int(m.group(1)))
    m=re.search(r'(%s)\s+(\d{4})'%'|'.join(MESI),datestr.lower())
    if m: return '%s-%s-01'%(m.group(2),MESI[m.group(1)])
    return None
NISO={}
for k in NEWS:
    i=hit.find('id="%s"'%k); cs=hit.rfind('news-date">',0,i)
    dt=re.search(r'news-date">([^<]+)<',hit[cs:cs+220]).group(1)
    NISO[k]=news_iso(dt)

def end_of_div(h,start):
    depth=0
    for m in re.finditer(r'<div\b|</div>',h[start:]):
        depth+=(-1 if m.group(0)=='</div>' else 1)
        if depth==0: return start+m.end()
    return -1

def extract_news(h,key):
    i=h.find('id="%s"'%key); cs=h.rfind('<div class="news-card">',0,i)
    card=h[cs:h.find('</div>\n</div>',i)+12]
    date=re.search(r'news-date">([^<]+)<',card).group(1)
    title=re.search(r'news-title">([^<]+)<',card).group(1)
    quote=re.search(r'news-quote">(.*?)</div>',card,re.S).group(1).strip()
    labels=re.findall(r'news-label">([^<]+)</p>',card)
    bodies=[re.sub(r'\s*<button.*?</button>','',b,flags=re.S).strip() for b in re.findall(r'news-body">(.*?)</p>',card,re.S)]
    sm=re.search(r'news-source">(.*?)</p>',card,re.S)
    src=sm.group(1).strip() if sm else ''
    return dict(date=date,title=title,quote=quote,labels=labels,bodies=bodies,src=src)

def extract_manifesto(h,sk):
    cid='manifesto-text' if sk=='m1' else 'manifesto-text-'+sk[2:]
    ci=h.find('id="%s">'%cid)
    bi=h.find('<div class="manifesto-block active"',ci)
    be=end_of_div(h,bi)
    inner=h[h.find('>',bi)+1:be-6]  # between block open and its </div>
    si=h.find('data-share-key="%s"'%sk)
    cardstart=h.rfind('<div class="manifesto-card">',0,si)
    title=re.search(r'manifesto-card-title"[^>]*>([^<]+)<',h[cardstart:si]).group(1)
    subm=re.search(r'manifesto-card-sub"[^>]*>([^<]+)<',h[cardstart:si])
    sub=subm.group(1) if subm else ''
    return dict(title=title,sub=sub,body=inner.strip())

FONTLINK='<link href="https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,500;0,700;0,800;1,400;1,700&amp;family=Source+Serif+4:ital,wght@0,300;0,400;0,600;1,300;1,400&amp;display=swap" rel="stylesheet"/>'
CSS='''<style>
:root{--void:#080808;--deep:#0e0e0e;--surface:#141414;--line:#2a2a2a;--ash:#5a5a5a;--dust:#8a8a8a;--pale:#b8b4ac;--ghost:#d8d4cc;--bone:#ece8e0;--blood:#6b1414;--ember:#8b2020;--glow:#a83030}
*{box-sizing:border-box}
body{margin:0;background:var(--void);color:var(--pale);font-family:'Source Serif 4',Georgia,serif;line-height:1.75;font-size:18px}
a{color:var(--glow)}
#main-nav{position:sticky;top:0;z-index:100;background:rgba(8,8,8,.97);backdrop-filter:blur(8px);border-bottom:1px solid var(--line)}
#nav-logo-wrap{display:flex;justify-content:center;padding:10px 0 6px;border-bottom:1px solid var(--line)}
#nav-logo{width:280px;max-width:80%;height:auto;display:block}
#nav-links{display:flex;justify-content:center;flex-wrap:wrap;border-bottom:1px solid var(--line)}
.nav-link{font-family:'Source Serif 4',serif;font-size:.7rem;font-weight:600;letter-spacing:.18em;text-transform:uppercase;color:var(--ash);padding:10px 18px;text-decoration:none;transition:color .3s}
.nav-link:hover,.nav-link.active{color:var(--glow)}
#lang-bar{display:flex;justify-content:center;flex-wrap:wrap}
.lang-btn{font-size:.68rem;font-weight:600;letter-spacing:.1em;text-transform:uppercase;color:var(--ash);padding:8px 12px;text-decoration:none;display:inline-block}
.lang-btn:hover{color:var(--ghost)}
.lang-btn.active{color:var(--glow)}
.section-inner{max-width:800px;margin:0 auto;padding:50px 48px 90px}
.section-header{font-size:.62rem;letter-spacing:.4em;text-transform:uppercase;color:var(--glow);margin-bottom:32px;display:flex;align-items:center;gap:20px}
.section-header::after{content:'';flex:1;height:1px;background:linear-gradient(to right,var(--blood),transparent)}
.btn-primary{display:inline-block;text-decoration:none;font-size:.82rem;font-weight:600;letter-spacing:.18em;text-transform:uppercase;color:var(--bone);background:var(--blood);border:1px solid var(--ember);padding:16px 40px;cursor:pointer;font-family:inherit}
.btn-primary:hover{background:var(--ember)}
@media(max-width:640px){.nav-link{padding:8px 12px;font-size:.62rem}.lang-btn{padding:7px 8px;font-size:.62rem}.section-inner{padding:36px 24px 70px}}
.wrap{max-width:720px;margin:0 auto;padding:54px 24px 30px}
.cat{color:var(--glow);font-size:12px;letter-spacing:.3em;text-transform:uppercase;margin:0 0 18px}
h1{font-family:'EB Garamond',serif;font-weight:700;font-size:38px;line-height:1.18;color:var(--bone);margin:0 0 16px}
.date{color:var(--dust);font-size:15px;margin:0 0 30px}
.quote{border-left:2px solid var(--ember);padding:6px 0 6px 22px;margin:0 0 36px;font-style:italic;font-size:22px;color:var(--ghost);line-height:1.5}
.lab,h2{color:var(--glow);font-size:12px;letter-spacing:.22em;text-transform:uppercase;margin:38px 0 10px;font-weight:600;font-family:'Source Serif 4',Georgia,serif}
h3.mt{font-family:'EB Garamond',serif;font-weight:700;font-size:30px;color:var(--bone);margin:0 0 14px;line-height:1.2}
h4{color:var(--glow);font-size:12px;letter-spacing:.22em;text-transform:uppercase;margin:34px 0 10px;font-weight:600}
p{margin:0 0 18px}
.src{border-top:1px solid var(--line);margin-top:40px;padding-top:18px;color:var(--ash);font-size:14px}
.src a{color:var(--dust)}
.cta{border:1px solid var(--line);background:var(--deep);padding:26px;margin:46px 0 0;text-align:center}
.cta a.btn{display:inline-block;border:1px solid var(--glow);color:var(--bone);text-decoration:none;padding:11px 22px;letter-spacing:.04em;margin-top:6px}
.back{margin:34px 0 0}
.back a{color:var(--dust);text-decoration:none;letter-spacing:.04em}
footer{border-top:1px solid var(--line);margin-top:50px;padding:26px 24px 40px;text-align:center;color:var(--ash);font-size:13px}
footer a{color:var(--dust);text-decoration:none;letter-spacing:.05em}
[dir=rtl] .quote{border-left:0;border-right:2px solid var(--ember);padding:6px 22px 6px 0}
@media(max-width:600px){h1{font-size:30px}h3.mt{font-size:25px}.quote{font-size:19px}body{font-size:17px}}
</style>'''

# ============ TAG SYSTEM ============
VOC={
'Myanmar':['myanmar','birmania','rakhine','min aung hlaing','naypyidaw'],'Rohingya':['rohingya','rohinya','rohinyá'],
'RD Congo':['rd congo','rdc','kivu','goma','m23'],'Ruanda':['ruanda','kigali','kagame'],
'Gaza':['gaza'],'Israele':['israele','israelian','netanyahu'],'Sudan':['sudan'],
'Iran':['iran','teheran'],'Russia–Ucraina':['russia','russo','ucrain','mosca'],
'Taiwan':['taiwan','taipei'],'Libano':['libano','libanes','hezbollah'],
'Venezuela':['venezuela'],'Flotilla':['flotilla','flottigl'],'Ben Gvir':['ben gvir','gvir'],
'Fame e carestia':['fame','carestia','affamare','alimentare mondiale'],
'Asilo e migrazione':['asilo','migrant','frontiera','esternalizzazione','rifugiat'],
'ONU':['onu','consiglio di sicurezza','nazioni unite','risoluzione 2417'],
'Corte penale internazionale':['corte penale','statuto di roma','crimine di guerra','crimini di guerra',' aja'],
'Sanzioni':['sanzion'],'Genocidio':['genocidio'],
'Stati Uniti':['stati uniti','trump','washington'],
'Unione Europea':['unione europea','bruxelles','consiglio affari esteri',' ue '],
'Diritto internazionale':['diritto internazionale','carta onu','convenzione di vienna'],
}
import re as _re2
def _slug(t):
    s=t.lower().replace('–','-').replace('/','-')
    return _re2.sub(r'[^a-z0-9]+','-',s).strip('-')
SLUG={t:_slug(t) for t in VOC}
TAGNAME={
'Myanmar':{'it':'Myanmar','en':'Myanmar','fr':'Myanmar','de':'Myanmar','es':'Myanmar','pt':'Myanmar','tr':'Myanmar','zh':'缅甸','ar':'ميانمار','he':'מיאנמר'},
'Rohingya':{'it':'Rohingya','en':'Rohingya','fr':'Rohingya','de':'Rohingya','es':'Rohinyá','pt':'Rohingya','tr':'Rohingya','zh':'罗兴亚人','ar':'الروهينغا','he':'רוהינגה'},
'RD Congo':{'it':'RD Congo','en':'DR Congo','fr':'RD Congo','de':'DR Kongo','es':'RD Congo','pt':'RD Congo','tr':'DR Kongo','zh':'刚果(金)','ar':'الكونغو الديمقراطية','he':'קונגו הדמוקרטית'},
'Ruanda':{'it':'Ruanda','en':'Rwanda','fr':'Rwanda','de':'Ruanda','es':'Ruanda','pt':'Ruanda','tr':'Ruanda','zh':'卢旺达','ar':'رواندا','he':'רואנדה'},
'Gaza':{'it':'Gaza','en':'Gaza','fr':'Gaza','de':'Gaza','es':'Gaza','pt':'Gaza','tr':'Gazze','zh':'加沙','ar':'غزة','he':'עזה'},
'Israele':{'it':'Israele','en':'Israel','fr':'Israël','de':'Israel','es':'Israel','pt':'Israel','tr':'İsrail','zh':'以色列','ar':'إسرائيل','he':'ישראל'},
'Sudan':{'it':'Sudan','en':'Sudan','fr':'Soudan','de':'Sudan','es':'Sudán','pt':'Sudão','tr':'Sudan','zh':'苏丹','ar':'السودان','he':'סודאן'},
'Iran':{'it':'Iran','en':'Iran','fr':'Iran','de':'Iran','es':'Irán','pt':'Irão','tr':'İran','zh':'伊朗','ar':'إيران','he':'איראן'},
'Russia–Ucraina':{'it':'Russia–Ucraina','en':'Russia–Ukraine','fr':'Russie–Ukraine','de':'Russland–Ukraine','es':'Rusia–Ucrania','pt':'Rússia–Ucrânia','tr':'Rusya–Ukrayna','zh':'俄罗斯-乌克兰','ar':'روسيا–أوكرانيا','he':'רוסיה–אוקראינה'},
'Taiwan':{'it':'Taiwan','en':'Taiwan','fr':'Taïwan','de':'Taiwan','es':'Taiwán','pt':'Taiwan','tr':'Tayvan','zh':'台湾','ar':'تايوان','he':'טייוואן'},
'Libano':{'it':'Libano','en':'Lebanon','fr':'Liban','de':'Libanon','es':'Líbano','pt':'Líbano','tr':'Lübnan','zh':'黎巴嫩','ar':'لبنان','he':'לבנון'},
'Venezuela':{'it':'Venezuela','en':'Venezuela','fr':'Venezuela','de':'Venezuela','es':'Venezuela','pt':'Venezuela','tr':'Venezuela','zh':'委内瑞拉','ar':'فنزويلا','he':'ונצואלה'},
'Flotilla':{'it':'Flotilla','en':'Flotilla','fr':'Flottille','de':'Flottille','es':'Flotilla','pt':'Flotilha','tr':'Filo','zh':'船队','ar':'أسطول','he':'משט'},
'Ben Gvir':{'it':'Ben Gvir','en':'Ben Gvir','fr':'Ben Gvir','de':'Ben Gvir','es':'Ben Gvir','pt':'Ben Gvir','tr':'Ben Gvir','zh':'本-格维尔','ar':'بن غفير','he':'בן גביר'},
'Fame e carestia':{'it':'Fame e carestia','en':'Hunger and famine','fr':'Faim et famine','de':'Hunger und Hungersnot','es':'Hambre y hambruna','pt':'Fome e carestia','tr':'Açlık ve kıtlık','zh':'饥饿与饥荒','ar':'الجوع والمجاعة','he':'רעב ומחסור'},
'Asilo e migrazione':{'it':'Asilo e migrazione','en':'Asylum and migration','fr':'Asile et migration','de':'Asyl und Migration','es':'Asilo y migración','pt':'Asilo e migração','tr':'İltica ve göç','zh':'庇护与移民','ar':'اللجوء والهجرة','he':'מקלט והגירה'},
'ONU':{'it':'ONU','en':'UN','fr':'ONU','de':'UNO','es':'ONU','pt':'ONU','tr':'BM','zh':'联合国','ar':'الأمم المتحدة','he':'האו״ם'},
'Corte penale internazionale':{'it':'Corte penale internazionale','en':'International Criminal Court','fr':'Cour pénale internationale','de':'Internationaler Strafgerichtshof','es':'Corte Penal Internacional','pt':'Tribunal Penal Internacional','tr':'Uluslararası Ceza Mahkemesi','zh':'国际刑事法院','ar':'المحكمة الجنائية الدولية','he':'בית הדין הפלילי הבינלאומי'},
'Sanzioni':{'it':'Sanzioni','en':'Sanctions','fr':'Sanctions','de':'Sanktionen','es':'Sanciones','pt':'Sanções','tr':'Yaptırımlar','zh':'制裁','ar':'عقوبات','he':'סנקציות'},
'Genocidio':{'it':'Genocidio','en':'Genocide','fr':'Génocide','de':'Völkermord','es':'Genocidio','pt':'Genocídio','tr':'Soykırım','zh':'种族灭绝','ar':'الإبادة الجماعية','he':'רצח עם'},
'Stati Uniti':{'it':'Stati Uniti','en':'United States','fr':'États-Unis','de':'USA','es':'Estados Unidos','pt':'Estados Unidos','tr':'ABD','zh':'美国','ar':'الولايات المتحدة','he':'ארצות הברית'},
'Unione Europea':{'it':'Unione Europea','en':'European Union','fr':'Union européenne','de':'Europäische Union','es':'Unión Europea','pt':'União Europeia','tr':'Avrupa Birliği','zh':'欧盟','ar':'الاتحاد الأوروبي','he':'האיחוד האירופי'},
'Diritto internazionale':{'it':'Diritto internazionale','en':'International law','fr':'Droit international','de':'Völkerrecht','es':'Derecho internacional','pt':'Direito internacional','tr':'Uluslararası hukuk','zh':'国际法','ar':'القانون الدولي','he':'משפט בינלאומי'},
}
T_ARG={'it':'Argomento','en':'Topic','fr':'Sujet','de':'Thema','es':'Tema','pt':'Tema','tr':'Konu','zh':'主题','ar':'موضوع','he':'נושא'}
T_CONT={'it':'contenuti','en':'items','fr':'contenus','de':'Inhalte','es':'contenidos','pt':'conteúdos','tr':'içerik','zh':'条内容','ar':'محتوى','he':'פריטים'}
T_ARGS={'it':'Argomenti','en':'Topics','fr':'Sujets','de':'Themen','es':'Temas','pt':'Temas','tr':'Konular','zh':'主题','ar':'المواضيع','he':'נושאים'}
T_ARGS_SUB={'it':'Tutti gli argomenti analizzati','en':'All topics analysed','fr':'Tous les sujets analysés','de':'Alle analysierten Themen','es':'Todos los temas analizados','pt':'Todos os temas analisados','tr':'Analiz edilen tüm konular','zh':'已分析的全部主题','ar':'كل المواضيع المحلَّلة','he':'כל הנושאים שנותחו'}
T_FT={'it':'Fonti e metodo','en':'Sources and method','fr':'Sources et méthode','de':'Quellen und Methode','es':'Fuentes y método','pt':'Fontes e método','tr':'Kaynaklar ve yöntem','zh':'来源与方法','ar':'المصادر والمنهج','he':'מקורות ושיטה'}
T_FH={'it':'Come verifichiamo','en':'How we verify','fr':'Comment nous vérifions','de':'Wie wir prüfen','es':'Cómo verificamos','pt':'Como verificamos','tr':'Nasıl doğrularız','zh':'我们如何核实','ar':'كيف نتحقق','he':'כיצד אנו מאמתים'}
T_FB={
'it':"Ogni fatto pubblicato è verificato su più fonti internazionali indipendenti prima della pubblicazione. Citiamo le fonti primarie — testi ufficiali di ONU, Corte penale internazionale, trattati — e le testate riconosciute, con i link in ogni pagina. Distinguiamo sempre il fatto documentato dall'analisi.",
'en':"Every fact we publish is checked against several independent international sources before publication. We cite primary sources — official UN and ICC texts, treaties — and recognised outlets, with links on every page. We always separate documented fact from analysis.",
'fr':"Chaque fait publié est vérifié sur plusieurs sources internationales indépendantes avant publication. Nous citons les sources primaires — textes officiels de l'ONU et de la CPI, traités — et les médias reconnus, avec les liens sur chaque page. Nous distinguons toujours le fait documenté de l'analyse.",
'de':"Jeder veröffentlichte Fakt wird vor der Veröffentlichung anhand mehrerer unabhängiger internationaler Quellen geprüft. Wir zitieren Primärquellen — offizielle Texte von UNO und IStGH, Verträge — und anerkannte Medien, mit Links auf jeder Seite. Wir trennen stets die belegte Tatsache von der Analyse.",
'es':"Cada hecho que publicamos se verifica con varias fuentes internacionales independientes antes de publicarse. Citamos las fuentes primarias — textos oficiales de la ONU y la CPI, tratados — y medios reconocidos, con enlaces en cada página. Siempre separamos el hecho documentado del análisis.",
'pt':"Cada facto que publicamos é verificado em várias fontes internacionais independentes antes da publicação. Citamos as fontes primárias — textos oficiais da ONU e do TPI, tratados — e órgãos reconhecidos, com ligações em cada página. Separamos sempre o facto documentado da análise.",
'tr':"Yayımladığımız her olgu, yayından önce birden çok bağımsız uluslararası kaynakla doğrulanır. Birincil kaynakları — BM ve UCM resmî metinleri, antlaşmalar — ve tanınmış yayın organlarını her sayfada bağlantılarla aktarırız. Belgelenmiş olguyu her zaman yorumdan ayırırız.",
'zh':"我们发布的每一个事实，在发布前都会对照多个独立的国际来源进行核实。我们引用一手来源——联合国与国际刑事法院的官方文本、条约——以及受认可的媒体，并在每页附上链接。我们始终把有据可查的事实与分析区分开。",
'ar':"كل واقعة ننشرها تُدقَّق على عدة مصادر دولية مستقلة قبل النشر. نستشهد بالمصادر الأولية — النصوص الرسمية للأمم المتحدة والمحكمة الجنائية الدولية والمعاهدات — وبالمنابر المعترف بها، مع الروابط في كل صفحة. ونفصل دائماً الواقعة الموثَّقة عن التحليل.",
'he':"כל עובדה שאנו מפרסמים נבדקת מול כמה מקורות בינלאומיים בלתי תלויים לפני הפרסום. אנו מצטטים מקורות ראשוניים — טקסטים רשמיים של האו״ם ובית הדין הפלילי הבינלאומי, אמנות — וכלי תקשורת מוכרים, עם קישורים בכל עמוד. אנו תמיד מפרידים בין עובדה מתועדת לבין ניתוח.",
}
T_FSUB={'it':'Testate e fonti consultate','en':'Outlets and sources consulted','fr':'Médias et sources consultés','de':'Konsultierte Medien und Quellen','es':'Medios y fuentes consultados','pt':'Órgãos e fontes consultados','tr':'Başvurulan yayın organları ve kaynaklar','zh':'已查阅的媒体与来源','ar':'المنابر والمصادر','he':'כלי תקשורת ומקורות'}
T_LT={'it':'Lingue','en':'Languages','fr':'Langues','de':'Sprachen','es':'Idiomas','pt':'Línguas','tr':'Diller','zh':'语言','ar':'اللغات','he':'שפות'}
T_LB={'it':'Questo sito è interamente disponibile in 11 lingue. Scegli la tua:','en':'This site is fully available in 11 languages. Choose yours:','fr':'Ce site est entièrement disponible en 11 langues. Choisissez la vôtre :','de':'Diese Seite ist vollständig in 11 Sprachen verfügbar. Wähle deine:','es':'Este sitio está disponible íntegramente en 11 idiomas. Elige el tuyo:','pt':'Este site está totalmente disponível em 11 línguas. Escolha a sua:','tr':'Bu site tümüyle 11 dilde mevcuttur. Kendi dilinizi seçin:','zh':'本网站提供全部11种语言版本。选择你的语言：','ar':'هذا الموقع متاح بالكامل بإحدى عشرة لغة. اختر لغتك:','he':'אתר זה זמין במלואו ב-11 שפות. בחרו את שלכם:'}
NATIVE=[('it','Italiano','/'),('en','English','/en/'),('fr','Français','/fr/'),('de','Deutsch','/de/'),('es','Español','/es/'),('pt','Português','/pt/'),('tr','Türkçe','/tr/'),('zh','中文','/zh/'),('ar','العربية','/ar/'),('he','עברית','/he/'),('ru','Русский','/ru/')]

# compute canonical tags + meta + sources from IT
_hit=open(fpath('it'),encoding='utf-8').read()
meta={}
for _k in NEWS: meta[_k]={'kind':'news'}
for _k in SHARES: meta[_k]={'kind':'manifesto'}
def _txt(key):
    if meta[key]['kind']=='news': d=extract_news(_hit,key); return (d['title']+' '+' '.join(d['bodies'])).lower()
    d=extract_manifesto(_hit,key); return (d['title']+' '+d['body']).lower()
itemtags={}
for _k in list(NEWS)+list(SHARES):
    t=_txt(_k); itemtags[_k]=[tg for tg,kw in VOC.items() if any(w in t for w in kw)]
if 'nd-mona' in itemtags: itemtags['nd-mona']=['Libano','ONU','Diritto internazionale']
if 'nd-coi' in itemtags: itemtags['nd-coi']=['Israele','Gaza','ONU','Diritto internazionale','Genocidio']
if 'nd-rdc' in itemtags: itemtags['nd-rdc']=['RD Congo','Ruanda','ONU','Diritto internazionale']
if 'nd-mya' in itemtags: itemtags['nd-mya']=['Myanmar','Rohingya','Genocidio','ONU','Diritto internazionale']
if 'm1' in itemtags: itemtags['m1']=['Israele','ONU','Diritto internazionale']
if 'm-ru' in itemtags: itemtags['m-ru']=['Russia–Ucraina','ONU','Corte penale internazionale','Diritto internazionale']
if 'm-sd' in itemtags: itemtags['m-sd']=['Sudan','Genocidio','ONU','Diritto internazionale']
if 'm-us' in itemtags: itemtags['m-us']=['Stati Uniti','Venezuela','Sanzioni','Diritto internazionale']
if 'm-fl' in itemtags: itemtags['m-fl']=['Flotilla','Gaza','Israele','Diritto internazionale']
if 'm-im' in itemtags: itemtags['m-im']=['Asilo e migrazione','Unione Europea','Diritto internazionale']
if 'm-fame' in itemtags: itemtags['m-fame']=['Fame e carestia','Gaza','ONU','Diritto internazionale']
if 'nd-sd' in itemtags: itemtags['nd-sd']=['Sudan','Genocidio','Fame e carestia','ONU','Diritto internazionale']
tagkeys={tg:[k for k in list(NEWS)+list(SHARES) if tg in itemtags[k]] for tg in VOC}
TAGS_ORDER=sorted(VOC, key=lambda t:(-len(tagkeys[t]), t))
TOTAL=len(NEWS)+len(SHARES)
_doms=set()
for _k in NEWS:
    for u in _re2.findall(r'https?://([^/"]+)', extract_news(_hit,_k)['src']):
        u=u.replace('www.','')
        if all(x not in u for x in ['iwillnotlookaway','facebook','googleapis']): _doms.add(u)
for _k in SHARES:
    for u in _re2.findall(r'https?://([^/"]+)', extract_manifesto(_hit,_k)['body']):
        u=u.replace('www.','')
        if all(x not in u for x in ['iwillnotlookaway','facebook','googleapis']): _doms.add(u)
SOURCE_LIST=sorted(_doms)

CHIPCSS=("a{color:var(--glow)}"
"#main-nav{position:sticky;top:0;z-index:100;background:rgba(8,8,8,.97);border-bottom:1px solid var(--line)}"
"#nav-logo-wrap{display:flex;justify-content:center;padding:10px 0 6px;border-bottom:1px solid var(--line)}"
"#nav-logo{width:280px;max-width:80%;height:auto;display:block}"
"#nav-links{display:flex;justify-content:center;flex-wrap:wrap;border-bottom:1px solid var(--line)}"
".nav-link{font-family:'Source Serif 4',serif;font-size:.7rem;font-weight:600;letter-spacing:.18em;text-transform:uppercase;color:var(--ash);padding:10px 18px;text-decoration:none}"
".nav-link:hover{color:var(--glow)}"
"#lang-bar{display:flex;justify-content:center;flex-wrap:wrap}"
".lang-btn{font-size:.68rem;font-weight:600;letter-spacing:.1em;text-transform:uppercase;color:var(--ash);padding:8px 12px;text-decoration:none;display:inline-block}"
".lang-btn.active{color:var(--glow)}"
".chips{max-width:720px;margin:30px auto 0;padding:0 24px;display:flex;flex-wrap:wrap}"
".chip{display:inline-block;text-decoration:none;border:1px solid var(--line);color:var(--dust);font-size:11px;letter-spacing:.12em;text-transform:uppercase;padding:6px 12px;margin:0 8px 8px 0}"
".chip:hover{border-color:var(--ember);color:var(--bone)}"
".phead{max-width:720px;margin:0 auto;padding:54px 24px 6px}"
".phead .k{color:var(--glow);font-size:12px;letter-spacing:.3em;text-transform:uppercase;margin:0 0 14px}"
".phead h1{font-family:'EB Garamond',serif;font-weight:700;font-size:44px;color:var(--bone);margin:0;line-height:1.12}"
".phead .count{color:var(--dust);font-size:15px;margin:12px 0 0}"
".plist{max-width:720px;margin:24px auto 0;padding:0 24px}"
".tag-item{display:block;text-decoration:none;border-top:1px solid var(--line);padding:22px 0}"
".tag-item:hover .ti-title{color:var(--glow)}"
".ti-cat{display:block;color:var(--glow);font-size:11px;letter-spacing:.22em;text-transform:uppercase;margin-bottom:8px}"
".ti-title{display:block;font-family:'EB Garamond',serif;font-size:24px;color:var(--bone);line-height:1.25}"
".ti-date{display:block;color:var(--dust);font-size:13px;margin-top:8px}"
".idxlist{max-width:720px;margin:24px auto 0;padding:0 24px;display:flex;flex-wrap:wrap}"
".idx{text-decoration:none;border:1px solid var(--line);color:var(--pale);padding:10px 16px;margin:0 10px 10px 0}"
".idx:hover{border-color:var(--ember);color:var(--bone)}"
".idx .n{color:var(--dust);font-size:.82em;margin-left:6px}"
".prose{max-width:720px;margin:0 auto;padding:0 24px}.prose p{margin:0 0 18px}"
".srcgrid{max-width:720px;margin:10px auto 0;padding:0 24px;display:flex;flex-wrap:wrap}"
".srcgrid span,.srcgrid a{border:1px solid var(--line);color:var(--dust);font-size:13px;padding:6px 12px;margin:0 8px 8px 0;text-decoration:none}.srcgrid a:hover{color:var(--glow);border-color:var(--glow)}"
".ling{max-width:560px;margin:10px auto 0;padding:0 24px}"
".ling a{display:block;font-family:'EB Garamond',serif;font-size:26px;color:var(--bone);text-decoration:none;border-top:1px solid var(--line);padding:18px 4px}"
".ling a:hover{color:var(--glow)}"
"[dir=rtl] .idx .n{margin-left:0;margin-right:6px}")
CSS=CSS.replace('</style>', CHIPCSS+'</style>')
CSS=CSS.replace('</style>', "a.ref{color:inherit;text-decoration:underline;text-decoration-color:var(--ash);text-underline-offset:3px;text-decoration-thickness:1px}a.ref:hover{color:var(--bone);text-decoration-color:var(--glow)}"+'</style>')
CSS=CSS.replace('</style>', ".actions{display:flex;gap:10px;flex-wrap:wrap;margin:34px 0 6px}.btn-share,.btn-pdf{font-size:.72rem;font-weight:600;letter-spacing:.12em;text-transform:uppercase;color:var(--dust);background:none;border:1px solid var(--line);padding:9px 16px;border-radius:2px;cursor:pointer;text-decoration:none;font-family:inherit;display:inline-flex;align-items:center;gap:7px}.btn-share:hover,.btn-pdf:hover{color:var(--glow);border-color:var(--glow)}"+'</style>')
CSS=CSS.replace('</style>', ".section-inner{max-width:800px;margin:0 auto;padding:10px 0 40px}.section-header{font-size:.62rem;letter-spacing:.4em;text-transform:uppercase;color:var(--glow);margin-bottom:40px;display:flex;align-items:center;gap:20px}.page-title{font-family:'EB Garamond',serif;font-size:clamp(2.2rem,5vw,3.6rem);font-weight:800;color:var(--bone);letter-spacing:-.01em;line-height:1.05;margin-bottom:18px}.page-desc{font-size:1.05rem;font-style:italic;color:var(--dust);line-height:1.75;max-width:620px;margin-bottom:48px}.about-block p{font-size:1.08rem;line-height:1.95;color:var(--dust);margin-bottom:20px;text-align:justify;hyphens:auto}.manifesto-card{border:1px solid var(--line);padding:32px;margin-bottom:24px}.manifesto-card-title{font-family:'EB Garamond',serif;font-size:1.4rem;font-weight:700;color:var(--bone);margin-bottom:10px}.manifesto-card-sub{font-size:.9rem;font-style:italic;color:var(--ash);margin-bottom:20px}.manifesto-card-actions{display:flex;gap:16px;flex-wrap:wrap;align-items:center}.btn-read{font-size:.75rem;font-weight:600;letter-spacing:.15em;text-transform:uppercase;color:var(--glow);text-decoration:none;border:1px solid var(--blood);padding:10px 24px;display:inline-block}.btn-read:hover{background:var(--blood);color:var(--bone)}"+'</style>')

import unicodedata as _ud
def asciislug(s):
    s=s.lower().replace('–','-').replace('/','-')
    for a,b in {'ı':'i','İ':'i','ş':'s','ğ':'g','ç':'c','ö':'o','ü':'u','é':'e','è':'e','ê':'e','á':'a','à':'a','â':'a','í':'i','î':'i','ó':'o','ô':'o','ú':'u','ñ':'n','ã':'a','õ':'o','ä':'a'}.items(): s=s.replace(a,b)
    s=_ud.normalize('NFKD',s).encode('ascii','ignore').decode()
    return _re2.sub(r'[^a-z0-9]+','-',s).strip('-')
_LATIN={'it','en','fr','de','es','pt','tr'}
TAGSLUG={t:{l:(asciislug(TAGNAME[t][l]) if l in _LATIN else asciislug(TAGNAME[t]['en'])) for l in LANGS} for t in VOC}
IDX_SLUG={'it':'argomenti','en':'topics','fr':'sujets','de':'themen','es':'temas','pt':'temas','tr':'konular','zh':'topics','ar':'topics','he':'topics'}
FONTI_SLUG={'it':'fonti','en':'sources','fr':'sources','de':'quellen','es':'fuentes','pt':'fontes','tr':'kaynaklar','zh':'sources','ar':'sources','he':'sources'}
LINGUE_SLUG={'it':'lingue','en':'languages','fr':'langues','de':'sprachen','es':'idiomas','pt':'linguas','tr':'diller','zh':'languages','ar':'languages','he':'languages'}
CHISONO_SLUG={'it':'chi-sono','en':'about','fr':'a-propos','de':'ueber-mich','es':'sobre-mi','pt':'sobre-mim','tr':'hakkimda','zh':'about','ar':'about','he':'about','ru':'about'}
PETIZIONI_SLUG={'it':'petizioni','en':'petitions','fr':'petitions','de':'petitionen','es':'peticiones','pt':'peticoes','tr':'dilekceler','zh':'petitions','ar':'petitions','he':'petitions','ru':'petitions'}

def chrome(l, langfn):
    nlx=NAV[l]; H=home(l)
    nv=('<div id="nav-links">'
        +'<a class="nav-link" href="%s">%s</a>'%(H,html.escape(nlx['nav_scopo']))
        +'<a class="nav-link" href="/s/%s/%s.html">%s</a>'%(l,CHISONO_SLUG[l],html.escape(nlx['nav_chisono']))
        +'<a class="nav-link" href="%s?page=manifesti">%s</a>'%(H,html.escape(nlx['nav_manifesti']))
        +'<a class="nav-link" href="%s?page=notizie">%s</a>'%(H,html.escape(nlx['nav_notizie']))
        +'<a class="nav-link" href="/s/%s/%s.html">%s</a>'%(l,PETIZIONI_SLUG[l],html.escape(nlx['nav_petizioni']))
        +'<a class="nav-link" href="/s/%s/%s.html">%s</a>'%(l,IDX_SLUG[l],html.escape(T_ARGS[l]))
        +'<a class="nav-link" href="/s/%s/%s.html">%s</a>'%(l,norme.NORME_SLUG[l],html.escape(norme.N_TITLE[l]))
        +'</div>')
    lb='<div id="lang-bar">'+''.join('<a class="lang-btn%s" href="%s">%s</a>'%(' active' if x==l else '',langfn(x),LANGLABEL[x]) for x in LANGORDER)+'</div>'
    return '<nav id="main-nav"><div id="nav-logo-wrap"><a href="%s"><img id="nav-logo" src="/logo.png" alt="I Will Not Look Away"/></a></div>%s%s</nav>'%(H,nv,lb)

def tail(l):
    ref='<p style="margin-top:10px;font-size:13px;letter-spacing:.04em"><a href="/s/%s/%s.html">%s</a> · <a href="/s/%s/%s.html">%s</a> · <a href="/s/%s/%s.html">%s</a> · <a href="/s/%s/%s.html">%s</a></p>'%(l,IDX_SLUG[l],html.escape(T_ARGS[l]), l,FONTI_SLUG[l],html.escape(T_FT[l]), l,norme.NORME_SLUG[l],html.escape(norme.N_TITLE[l]), l,LINGUE_SLUG[l],html.escape(T_LT[l]))
    return NLSEC[l]+'\n<footer>\n<p>I Will Not Look Away · iwillnotlookaway.org · 2026</p>\n'+ref+'\n<p style="margin-top:8px"><a href="mailto:iwillnotlookaway@gmail.com">iwillnotlookaway@gmail.com</a> · <a href="https://www.facebook.com/iwillnotlookaway" target="_blank" rel="noopener noreferrer">Facebook</a></p>\n</footer>\n<script>'+NLJS+'</script>'

SCRIPTF={'he':("Frank+Ruhl+Libre:wght@400;500;700","Frank Ruhl Libre"),'ar':("Amiri:wght@400;700","Amiri")}
ZH_STACK='"Songti SC","Noto Serif CJK SC","Source Han Serif SC",STSong,SimSun,serif'
RU_STACK='Georgia,"PT Serif","Times New Roman","DejaVu Serif",serif'
def fonthead(l):
    if l in ('zh','ru'): return ''  # Cina/Russia: nessun Google Fonts (accesso pieno)
    return FONTLINK.replace('&amp;display=swap','&amp;family=%s&amp;display=swap'%SCRIPTF[l][0]) if l in SCRIPTF else FONTLINK
def fontover(l):
    if l=='zh': return '<style>html[lang="zh"] *{font-family:%s}</style>'%ZH_STACK
    if l=='ru': return '<style>html[lang="ru"] *{font-family:%s}</style>'%RU_STACK
    return "<style>html[lang=\"%s\"] *{font-family:'%s','EB Garamond',Georgia,serif}</style>"%(l,SCRIPTF[l][1]) if l in SCRIPTF else ''
def hreflangs(urlfn):
    s=''.join('<link rel="alternate" hreflang="%s" href="%s"/>\n'%(x,urlfn(x)) for x in LANGS)
    return s+'<link rel="alternate" hreflang="x-default" href="%s"/>'%urlfn('it')

GA_BLOCK = '<!-- Google Analytics 4 + Consent Mode v2 -->\n<script async="" src="https://www.googletagmanager.com/gtag/js?id=G-RTTRBJLDQQ"></script>\n<script>\nwindow.dataLayer = window.dataLayer || [];\nfunction gtag(){dataLayer.push(arguments);}\ngtag(\'consent\', \'default\', {\n  \'analytics_storage\': \'denied\',\n  \'ad_storage\': \'denied\',\n  \'ad_user_data\': \'denied\',\n  \'ad_personalization\': \'denied\'\n});\ngtag(\'js\', new Date());\ngtag(\'config\', \'G-RTTRBJLDQQ\');\n</script>\n'
def ga_head(l):
    return '' if l in ('zh','ru') else GA_BLOCK

def shead(l,title,desc,url,alts=''):
    da=' dir="rtl"' if l in RTL else ''
    return ('<!doctype html>\n<html lang="%s"%s>\n<head>\n<meta charset="utf-8"/>\n<meta name="viewport" content="width=device-width,initial-scale=1"/>\n<link rel="preload" as="image" href="/logo.png"/>\n'%(l,da)+ga_head(l)
      +'<title>%s — I Will Not Look Away</title>\n<meta name="description" content="%s"/>\n<link rel="canonical" href="%s"/>\n'%(html.escape(title),html.escape(desc),url)+alts
      +'<meta property="og:type" content="website"/>\n<meta property="og:site_name" content="I Will Not Look Away"/>\n<meta property="og:locale" content="%s"/>\n'%LOCALE[l]
      +'<meta property="og:title" content="%s — I Will Not Look Away"/>\n<meta property="og:description" content="%s"/>\n<meta property="og:url" content="%s"/>\n'%(html.escape(title),html.escape(desc),url)
      +fonthead(l)+'\n'+CSS+fontover(l)+'\n</head>')

def chips_html(l,key):
    tg=itemtags.get(key,[])
    if not tg: return ''
    return '<div class="chips">'+''.join('<a class="chip" href="/s/%s/tag/%s.html">%s</a>'%(l,TAGSLUG[t][l],html.escape(TAGNAME[t][l])) for t in tg)+'</div>'
def tagmeta_html(l,key):
    return ''.join('<meta property="article:tag" content="%s"/>\n'%html.escape(TAGNAME[t][l]) for t in itemtags.get(key,[]))

def gen_tagpage(l,tag):
    keys=sorted(tagkeys[tag], key=lambda k: meta[k]['kind']!='news')
    url='%s/s/%s/tag/%s.html'%(BASE,l,TAGSLUG[tag][l]); name=TAGNAME[tag][l]
    rows=''
    for k in keys:
        cat=(CAT_N if meta[k]['kind']=='news' else CAT_M)[l]
        rows+='<a class="tag-item" href="/s/%s/%s.html"><span class="ti-cat">%s</span><span class="ti-title">%s</span><span class="ti-date">%s</span></a>'%(l,k,cat,html.escape(ITITLE[l][k]),html.escape(IDATE[l][k]))
    body='<div class="phead"><p class="k">%s</p><h1>%s</h1><p class="count">%d / %d %s</p></div><div class="plist">%s</div>'%(T_ARG[l],html.escape(name),len(keys),TOTAL,T_CONT[l],rows)
    return shead(l,name,'%s: %d %s.'%(name,len(keys),T_CONT[l]),url,hreflangs(lambda x:'%s/s/%s/tag/%s.html'%(BASE,x,TAGSLUG[tag][x])))+'\n<body>\n'+chrome(l,lambda x:'/s/%s/tag/%s.html'%(x,TAGSLUG[tag][x]))+'\n'+body+'\n'+tail(l)+'\n</body>\n</html>\n'

def gen_index(l):
    url='%s/s/%s/%s.html'%(BASE,l,IDX_SLUG[l])
    chips=''.join('<a class="idx" href="/s/%s/tag/%s.html">%s<span class="n">%d</span></a>'%(l,TAGSLUG[t][l],html.escape(TAGNAME[t][l]),len(tagkeys[t])) for t in TAGS_ORDER)
    body='<div class="phead"><p class="k">%s</p><h1>%s</h1><p class="count">%s</p></div><div class="idxlist">%s</div>'%(T_ARG[l],html.escape(T_ARGS[l]),html.escape(T_ARGS_SUB[l]),chips)
    return shead(l,T_ARGS[l],T_ARGS_SUB[l],url,hreflangs(lambda x:'%s/s/%s/%s.html'%(BASE,x,IDX_SLUG[x])))+'\n<body>\n'+chrome(l,lambda x:'/s/%s/%s.html'%(x,IDX_SLUG[x]))+'\n'+body+'\n'+tail(l)+'\n</body>\n</html>\n'

def gen_fonti(l):
    url='%s/s/%s/%s.html'%(BASE,l,FONTI_SLUG[l])
    srcs='<div class="srcgrid">'+''.join('<a href="https://%s" target="_blank" rel="noopener noreferrer">%s</a>'%(d,html.escape(d)) for d in SOURCE_LIST)+'</div>'
    body=('<div class="phead"><p class="k">%s</p><h1>%s</h1></div>'%(html.escape(T_FH[l]),html.escape(T_FT[l]))
      +'<div class="prose"><p>%s</p></div>'%html.escape(T_FB[l])
      +'<div class="phead" style="padding-top:30px"><p class="k">%s</p></div>'%html.escape(T_FSUB[l])+srcs)
    return shead(l,T_FT[l],T_FB[l][:150],url,hreflangs(lambda x:'%s/s/%s/%s.html'%(BASE,x,FONTI_SLUG[x])))+'\n<body>\n'+chrome(l,lambda x:'/s/%s/%s.html'%(x,FONTI_SLUG[x]))+'\n'+body+'\n'+tail(l)+'\n</body>\n</html>\n'

def gen_lingue(l):
    url='%s/s/%s/%s.html'%(BASE,l,LINGUE_SLUG[l])
    rows=''.join('<a href="%s" lang="%s">%s</a>'%(u,code,html.escape(nm)) for code,nm,u in NATIVE)
    body='<div class="phead"><p class="k">%s</p><h1>%s</h1><p class="count">%s</p></div><div class="ling">%s</div>'%('11 ·',html.escape(T_LT[l]),html.escape(T_LB[l]),rows)
    return shead(l,T_LT[l],T_LB[l],url,hreflangs(lambda x:'%s/s/%s/%s.html'%(BASE,x,LINGUE_SLUG[x])))+'\n<body>\n'+chrome(l,lambda x:'/s/%s/%s.html'%(x,LINGUE_SLUG[x]))+'\n'+body+'\n'+tail(l)+'\n</body>\n</html>\n'
# ============ END TAG SYSTEM ============


import srcdata
import norme
import reflinks
for _lst in srcdata.EXTRA_SOURCES.values():
    for _n,_u in _lst:
        for _d in re.findall(r'https?://([^/"]+)', _u):
            _d=_d.replace('www.','')
            if all(x not in _d for x in ['iwillnotlookaway','facebook','googleapis']): _doms.add(_d)
SOURCE_LIST=sorted(_doms)
EXTRA_SOURCES=srcdata.EXTRA_SOURCES; FLABEL=srcdata.FLABEL
def extralinks(key):
    e=EXTRA_SOURCES.get(key)
    if not e: return ''
    return ' · '.join('<a href="%s" target="_blank" rel="noopener noreferrer">%s</a>'%(u,html.escape(n)) for n,u in e)

def gen_norme(l):
    url='%s/s/%s/%s.html'%(BASE,l,norme.NORME_SLUG[l])
    rows=''
    for key,year,spec,host,names in norme.NORME:
        u=norme.norma_url(spec,l)
        linklang=(l if l in norme.UN6 else 'en') if callable(spec) else 'en'
        badge=' <span style="color:var(--ash)">(EN)</span>' if linklang!=l else ''
        rows+=('<div id="%s" style="padding:18px 0;border-bottom:1px solid var(--line);scroll-margin-top:90px">'%key+
          '<div style="font-size:21px;line-height:1.35;color:var(--bone)">%s <span style="color:var(--ash);font-size:14px;letter-spacing:.05em">\u00b7 %s</span></div>'
          '<a href="%s" target="_blank" rel="noopener noreferrer" style="display:inline-block;margin-top:7px;color:var(--glow);font-size:13px;letter-spacing:.08em;text-transform:uppercase">%s \u2192 <span style="color:var(--ash);text-transform:none;letter-spacing:0">%s</span>%s</a>'
          '</div>')%(html.escape(names[l]),year,u,html.escape(norme.N_OFF[l]),html.escape(host),badge)
    body=('<div class="phead"><p class="k">%s</p><h1>%s</h1></div>'%('1945 \u2014 1998',html.escape(norme.N_TITLE[l]))
      +'<div class="prose" style="max-width:760px"><p>%s</p>%s</div>'%(html.escape(norme.N_INTRO[l]),rows))
    return shead(l,norme.N_TITLE[l],norme.N_INTRO[l][:150],url,hreflangs(lambda x:'%s/s/%s/%s.html'%(BASE,x,norme.NORME_SLUG[x])))+'\n<body>\n'+chrome(l,lambda x:'/s/%s/%s.html'%(x,norme.NORME_SLUG[x]))+'\n'+body+'\n'+tail(l)+'\n</body>\n</html>\n'

SHARE_LBL={'it':'Condividi','en':'Share','fr':'Partager','de':'Teilen','es':'Compartir','pt':'Partilhar','tr':'Payla\u015f','zh':'\u5206\u4eab','ar':'\u0645\u0634\u0627\u0631\u0643\u0629','he':'\u05e9\u05d9\u05ea\u05d5\u05e3','ru':'\u041f\u043e\u0434\u0435\u043b\u0438\u0442\u044c\u0441\u044f'}
DL_LBL={'it':'Scarica PDF','en':'Download PDF','fr':'T\u00e9l\u00e9charger le PDF','de':'PDF herunterladen','es':'Descargar PDF','pt':'Descarregar PDF','tr':'PDF indir','zh':'\u4e0b\u8f7d PDF','ar':'\u062a\u0646\u0632\u064a\u0644 PDF','he':'\u05d4\u05d5\u05e8\u05d3\u05ea PDF','ru':'\u0421\u043a\u0430\u0447\u0430\u0442\u044c PDF'}
COPIED={'it':'Link copiato','en':'Link copied','fr':'Lien copi\u00e9','de':'Link kopiert','es':'Enlace copiado','pt':'Link copiado','tr':'Ba\u011flant\u0131 kopyaland\u0131','zh':'\u94fe\u63a5\u5df2\u590d\u5236','ar':'\u062a\u0645 \u0646\u0633\u062e \u0627\u0644\u0631\u0627\u0628\u0637','he':'\u05d4\u05e7\u05d9\u05e9\u05d5\u05e8 \u05d4\u05d5\u05e2\u05ea\u05e7','ru':'\u0421\u0441\u044b\u043b\u043a\u0430 \u0441\u043a\u043e\u043f\u0438\u0440\u043e\u0432\u0430\u043d\u0430'}
PDF_MAN={'m1','m-ru','m-sd','m-us','m-fl'}
def man_pdf(sk,l):
    if sk not in PDF_MAN or l=='ru': return None
    return ('/manifesto_%s.pdf'%l) if sk=='m1' else ('/manifesto_%s_%s.pdf'%(sk[2:],l))

def page(l,key,kind,data):
    dirattr=' dir="rtl"' if l in RTL else ''
    cat=(CAT_N if kind=='news' else CAT_M)[l]
    title_h=html.escape(data['title'],quote=True)
    if kind=='news':
        desc=html.escape(plain(data['bodies'][0])[:155] if data['bodies'] else plain(data['title']),quote=True)
    else:
        desc=html.escape(plain(data['sub'])[:155] or plain(data['title']),quote=True)
    img='%s/s/%s/%s.jpg'%(BASE,l,key); url='%s/s/%s/%s.html'%(BASE,l,key)
    alts='\n'.join('<link rel="alternate" hreflang="%s" href="%s/s/%s/%s.html"/>'%(x,BASE,x,key) for x in LANGS)
    alts+='\n<link rel="alternate" hreflang="x-default" href="%s/s/it/%s.html"/>'%(BASE,key)
    if kind=='news':
        ld={"@context":"https://schema.org","@type":"NewsArticle","headline":plain(data['title']),"inLanguage":l,
            "image":[img],"mainEntityOfPage":url,"author":{"@type":"Organization","name":"I Will Not Look Away"},
            "publisher":{"@type":"Organization","name":"I Will Not Look Away","url":BASE},"description":plain(data['bodies'][0])[:200] if data['bodies'] else ''}
        if NISO.get(key): ld["datePublished"]=ld["dateModified"]=NISO[key]
    else:
        ld={"@context":"https://schema.org","@type":"Article","headline":plain(data['title']),"inLanguage":l,
            "image":[img],"mainEntityOfPage":url,"author":{"@type":"Organization","name":"I Will Not Look Away"},
            "publisher":{"@type":"Organization","name":"I Will Not Look Away","url":BASE},"description":plain(data['sub'])[:200]}
    jsonld=json.dumps(ld,ensure_ascii=False)
    # body
    if kind=='news':
        _lk=set()
        secs=''.join('<h2 class="lab">%s</h2>\n<p>%s</p>\n'%(html.escape(lab),reflinks.linkify_refs(body,l,_lk)) for lab,body in zip(data['labels'],data['bodies']))
        datel=html.escape(data['date'])
        artbody='<div class="quote">%s</div>\n%s<p class="src">%s</p>'%(data['quote'],secs,data['src']+((' \u00b7 '+extralinks(key)) if EXTRA_SOURCES.get(key) else ''))
    else:
        datel=html.escape(data['sub'])
        artbody=reflinks.linkify_refs(data['body'],l)+(('\n<p class="src">%s: %s</p>'%(html.escape(FLABEL[l]),extralinks(key))) if EXTRA_SOURCES.get(key) else '')
    arrow=(BACK[l]+' →') if l in RTL else ('← '+BACK[l])
    nvh=chrome(l, lambda x:'/s/%s/%s.html'%(x,key)); tl=tail(l); chips=chips_html(l,key); tm=tagmeta_html(l,key); fh=fonthead(l); fov=fontover(l)
    _sb='<button class="btn-share" type="button" onclick="shareThis()"><span>%s</span></button>'%html.escape(SHARE_LBL[l])
    _dl=''
    if kind=='manifesto':
        _p=man_pdf(key,l)
        if _p: _dl='<a class="btn-pdf" href="%s" target="_blank" rel="noopener noreferrer"><span>%s</span></a>'%(_p,html.escape(DL_LBL[l]))
    actions='<div class="actions">%s%s</div>'%(_sb,_dl)
    sharejs='<script>function shareThis(){var u=location.href,t=document.title;if(navigator.share){navigator.share({title:t,url:u}).catch(function(){});}else if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(u).then(function(){alert(%s);});}else{window.prompt(%s,u);}}</script>'%(json.dumps(COPIED[l],ensure_ascii=False),json.dumps(COPIED[l],ensure_ascii=False))
    return f'''<!doctype html>
<html lang="{l}"{dirattr}>
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<link rel="preload" as="image" href="/logo.png"/>
{ga_head(l)}<title>{title_h} — I Will Not Look Away</title>
<meta name="description" content="{desc}"/>
<link rel="canonical" href="{url}"/>
{alts}
<meta property="og:type" content="article"/>
<meta property="og:site_name" content="I Will Not Look Away"/>
<meta property="og:locale" content="{LOCALE[l]}"/>
<meta property="og:title" content="{title_h}"/>
<meta property="og:description" content="{desc}"/>
<meta property="og:image" content="{img}"/>
<meta property="og:image:width" content="1200"/>
<meta property="og:image:height" content="630"/>
<meta property="og:url" content="{url}"/>
<meta name="twitter:card" content="summary_large_image"/>
<meta name="twitter:title" content="{title_h}"/>
<meta name="twitter:description" content="{desc}"/>
<meta name="twitter:image" content="{img}"/>
{tm}{fh}
<script type="application/ld+json">{jsonld}</script>
{CSS}{fov}
</head>
<body>
{nvh}
<article class="wrap">
<p class="cat">{cat}</p>
<h1>{data['title']}</h1>
<p class="date">{datel}</p>
{artbody}
{actions}
{chips}
<p class="back"><a href="{home(l)}">{arrow}</a></p>
</article>
{sharejs}
{tl}
</body>
</html>
'''

def _sec_inner(l,pid):
    hh=open(fpath(l),encoding='utf-8').read(); i=hh.find('id="%s"'%pid)
    si=hh.find('section-inner',i); start=hh.rfind('<div',0,si); depth=0
    for m in re.finditer(r'<div\b|</div>',hh[start:]):
        depth+=(1 if m.group(0).startswith('<div') else -1)
        if depth==0: return hh[start:start+m.end()]
    return ''
def _sec_meta(inner):
    t=re.search(r'page-title"[^>]*>([^<]*)<',inner); d=re.search(r'page-desc"[^>]*>([^<]*)<',inner)
    return (t.group(1).strip() if t else ''),(d.group(1).strip() if d else '')
def gen_chisono(l):
    inner=_sec_inner(l,'page-chisono'); ttl,dsc=_sec_meta(inner); url='%s/s/%s/%s.html'%(BASE,l,CHISONO_SLUG[l])
    body='<article class="wrap">'+inner+'</article>'
    return shead(l,ttl,dsc,url,hreflangs(lambda x:'%s/s/%s/%s.html'%(BASE,x,CHISONO_SLUG[x])))+'\n<body>\n'+chrome(l,lambda x:'/s/%s/%s.html'%(x,CHISONO_SLUG[x]))+'\n'+body+'\n'+tail(l)+'\n</body>\n</html>\n'
def gen_petizioni(l):
    inner=_sec_inner(l,'page-petizioni'); ttl,dsc=_sec_meta(inner); url='%s/s/%s/%s.html'%(BASE,l,PETIZIONI_SLUG[l])
    body='<article class="wrap">'+inner+'</article>'
    return shead(l,ttl,dsc,url,hreflangs(lambda x:'%s/s/%s/%s.html'%(BASE,x,PETIZIONI_SLUG[x])))+'\n<body>\n'+chrome(l,lambda x:'/s/%s/%s.html'%(x,PETIZIONI_SLUG[x]))+'\n'+body+'\n'+tail(l)+'\n</body>\n</html>\n'

# === RU - 11a lingua (infrastruttura). 'ru' entra in LANGS/LANGORDER/NATIVE quando il contenuto e pronto. ===
LOCALE['ru']='ru_RU'
CAT_N['ru']='\u041d\u041e\u0412\u041e\u0421\u0422\u042c'
CAT_M['ru']='\u041c\u0410\u041d\u0418\u0424\u0415\u0421\u0422'
BACK['ru']='\u0412\u0441\u0435 \u043d\u043e\u0432\u043e\u0441\u0442\u0438 \u0438 \u043c\u0430\u043d\u0438\u0444\u0435\u0441\u0442\u044b'
NLSUB['ru']='\u041a\u0440\u0430\u0442\u043a\u0430\u044f \u0441\u0432\u043e\u0434\u043a\u0430 \u2014 \u0442\u043e\u043b\u044c\u043a\u043e \u043a\u043e\u0433\u0434\u0430 \u0444\u0430\u043a\u0442 \u0442\u043e\u0433\u043e \u0437\u0430\u0441\u043b\u0443\u0436\u0438\u0432\u0430\u0435\u0442.'
NLBTN['ru']='\u041f\u043e\u0434\u043f\u0438\u0441\u0430\u0442\u044c\u0441\u044f \u043d\u0430 \u0440\u0430\u0441\u0441\u044b\u043b\u043a\u0443'
LANGLABEL['ru']='RU'
IDX_SLUG['ru']='topics'; FONTI_SLUG['ru']='sources'; LINGUE_SLUG['ru']='languages'
T_ARG['ru']='\u0422\u0435\u043c\u0430'
T_CONT['ru']='\u043c\u0430\u0442\u0435\u0440\u0438\u0430\u043b\u043e\u0432'
T_ARGS['ru']='\u0422\u0435\u043c\u044b'
T_ARGS_SUB['ru']='\u0412\u0441\u0435 \u043f\u0440\u043e\u0430\u043d\u0430\u043b\u0438\u0437\u0438\u0440\u043e\u0432\u0430\u043d\u043d\u044b\u0435 \u0442\u0435\u043c\u044b'
T_FT['ru']='\u0418\u0441\u0442\u043e\u0447\u043d\u0438\u043a\u0438 \u0438 \u043c\u0435\u0442\u043e\u0434'
T_FH['ru']='\u041a\u0430\u043a \u043c\u044b \u043f\u0440\u043e\u0432\u0435\u0440\u044f\u0435\u043c'
T_FB['ru']='\u041a\u0430\u0436\u0434\u044b\u0439 \u0444\u0430\u043a\u0442, \u043a\u043e\u0442\u043e\u0440\u044b\u0439 \u043c\u044b \u043f\u0443\u0431\u043b\u0438\u043a\u0443\u0435\u043c, \u043f\u0435\u0440\u0435\u0434 \u043f\u0443\u0431\u043b\u0438\u043a\u0430\u0446\u0438\u0435\u0439 \u043f\u0440\u043e\u0432\u0435\u0440\u044f\u0435\u0442\u0441\u044f \u043f\u043e \u043d\u0435\u0441\u043a\u043e\u043b\u044c\u043a\u0438\u043c \u043d\u0435\u0437\u0430\u0432\u0438\u0441\u0438\u043c\u044b\u043c \u043c\u0435\u0436\u0434\u0443\u043d\u0430\u0440\u043e\u0434\u043d\u044b\u043c \u0438\u0441\u0442\u043e\u0447\u043d\u0438\u043a\u0430\u043c. \u041c\u044b \u0441\u0441\u044b\u043b\u0430\u0435\u043c\u0441\u044f \u043d\u0430 \u043f\u0435\u0440\u0432\u043e\u0438\u0441\u0442\u043e\u0447\u043d\u0438\u043a\u0438 \u2014 \u043e\u0444\u0438\u0446\u0438\u0430\u043b\u044c\u043d\u044b\u0435 \u0442\u0435\u043a\u0441\u0442\u044b \u0438 \u0434\u043e\u0433\u043e\u0432\u043e\u0440\u044b \u041e\u041e\u041d \u0438 \u041c\u0435\u0436\u0434\u0443\u043d\u0430\u0440\u043e\u0434\u043d\u043e\u0433\u043e \u0443\u0433\u043e\u043b\u043e\u0432\u043d\u043e\u0433\u043e \u0441\u0443\u0434\u0430 \u2014 \u0430 \u0442\u0430\u043a\u0436\u0435 \u043d\u0430 \u0430\u0432\u0442\u043e\u0440\u0438\u0442\u0435\u0442\u043d\u044b\u0435 \u0421\u041c\u0418, \u0438 \u043d\u0430 \u043a\u0430\u0436\u0434\u043e\u0439 \u0441\u0442\u0440\u0430\u043d\u0438\u0446\u0435 \u043f\u0440\u0438\u0432\u043e\u0434\u0438\u043c \u0441\u0441\u044b\u043b\u043a\u0438. \u041c\u044b \u0432\u0441\u0435\u0433\u0434\u0430 \u043e\u0442\u0434\u0435\u043b\u044f\u0435\u043c \u0434\u043e\u043a\u0443\u043c\u0435\u043d\u0442\u0430\u043b\u044c\u043d\u043e \u043f\u043e\u0434\u0442\u0432\u0435\u0440\u0436\u0434\u0451\u043d\u043d\u044b\u0435 \u0444\u0430\u043a\u0442\u044b \u043e\u0442 \u0430\u043d\u0430\u043b\u0438\u0437\u0430.'
T_FSUB['ru']='\u0418\u0437\u0434\u0430\u043d\u0438\u044f \u0438 \u0438\u0441\u0442\u043e\u0447\u043d\u0438\u043a\u0438'
T_LT['ru']='\u042f\u0437\u044b\u043a\u0438'
T_LB['ru']='\u042d\u0442\u043e\u0442 \u0441\u0430\u0439\u0442 \u043f\u043e\u043b\u043d\u043e\u0441\u0442\u044c\u044e \u0434\u043e\u0441\u0442\u0443\u043f\u0435\u043d \u043d\u0430 11 \u044f\u0437\u044b\u043a\u0430\u0445. \u0412\u044b\u0431\u0435\u0440\u0438\u0442\u0435 \u0441\u0432\u043e\u0439:'
for _k,_v in {'Myanmar':'Мьянма','Rohingya':'рохинджа','RD Congo':'ДР Конго','Ruanda':'Руанда','Gaza':'\u0413\u0430\u0437\u0430','Israele':'\u0418\u0437\u0440\u0430\u0438\u043b\u044c','Sudan':'\u0421\u0443\u0434\u0430\u043d','Iran':'\u0418\u0440\u0430\u043d','Russia\u2013Ucraina':'\u0420\u043e\u0441\u0441\u0438\u044f\u2013\u0423\u043a\u0440\u0430\u0438\u043d\u0430','Taiwan':'\u0422\u0430\u0439\u0432\u0430\u043d\u044c','Libano':'\u041b\u0438\u0432\u0430\u043d','Venezuela':'\u0412\u0435\u043d\u0435\u0441\u0443\u044d\u043b\u0430','Flotilla':'\u0424\u043b\u043e\u0442\u0438\u043b\u0438\u044f','Ben Gvir':'\u0411\u0435\u043d-\u0413\u0432\u0438\u0440','Fame e carestia':'\u0413\u043e\u043b\u043e\u0434','Asilo e migrazione':'\u0423\u0431\u0435\u0436\u0438\u0449\u0435 \u0438 \u043c\u0438\u0433\u0440\u0430\u0446\u0438\u044f','ONU':'\u041e\u041e\u041d','Corte penale internazionale':'\u041c\u0435\u0436\u0434\u0443\u043d\u0430\u0440\u043e\u0434\u043d\u044b\u0439 \u0443\u0433\u043e\u043b\u043e\u0432\u043d\u044b\u0439 \u0441\u0443\u0434','Sanzioni':'\u0421\u0430\u043d\u043a\u0446\u0438\u0438','Genocidio':'\u0413\u0435\u043d\u043e\u0446\u0438\u0434','Stati Uniti':'\u0421\u0428\u0410','Unione Europea':'\u0415\u0432\u0440\u043e\u043f\u0435\u0439\u0441\u043a\u0438\u0439 \u0441\u043e\u044e\u0437','Diritto internazionale':'\u041c\u0435\u0436\u0434\u0443\u043d\u0430\u0440\u043e\u0434\u043d\u043e\u0435 \u043f\u0440\u0430\u0432\u043e'}.items():
    if _k in TAGNAME: TAGNAME[_k]['ru']=_v


cnt=0; oggen=0; ogerr=0
ITITLE={l:{} for l in LANGS}; IDATE={l:{} for l in LANGS}
for l in LANGS:
    h=open(fpath(l),encoding='utf-8').read()
    outdir=os.path.join(REPO,'s',l); os.makedirs(outdir,exist_ok=True)
    for key in NEWS:
        data=extract_news(h,key); ITITLE[l][key]=data['title']; IDATE[l][key]=data['date']
        jpg=os.path.join(outdir,key+'.jpg')
        if not os.path.exists(jpg):
            try: og_gen.make_og(data['title'],CAT_N[l],l,jpg); oggen+=1
            except Exception as e: ogerr+=1
        open(os.path.join(outdir,key+'.html'),'w',encoding='utf-8').write(page(l,key,'news',data)); cnt+=1
    for sk in SHARES:
        data=extract_manifesto(h,sk); ITITLE[l][sk]=data['title']; IDATE[l][sk]=data['sub']
        jpg=os.path.join(outdir,sk+'.jpg')
        if not os.path.exists(jpg):
            try: og_gen.make_og(data['title'],OGCAT_M[l],l,jpg); oggen+=1
            except Exception as e: ogerr+=1
        open(os.path.join(outdir,sk+'.html'),'w',encoding='utf-8').write(page(l,sk,'manifesto',data)); cnt+=1
print('pagine contenuto:',cnt,'| OG:',oggen,'| OG saltate:',ogerr)
tp=0
for l in LANGS:
    tagdir=os.path.join(REPO,'s',l,'tag'); os.makedirs(tagdir,exist_ok=True)
    for tg in VOC:
        open(os.path.join(tagdir,TAGSLUG[tg][l]+'.html'),'w',encoding='utf-8').write(gen_tagpage(l,tg)); tp+=1
    base=os.path.join(REPO,'s',l)
    open(os.path.join(base,IDX_SLUG[l]+'.html'),'w',encoding='utf-8').write(gen_index(l))
    open(os.path.join(base,FONTI_SLUG[l]+'.html'),'w',encoding='utf-8').write(gen_fonti(l))
    open(os.path.join(base,LINGUE_SLUG[l]+'.html'),'w',encoding='utf-8').write(gen_lingue(l))
    open(os.path.join(base,norme.NORME_SLUG[l]+'.html'),'w',encoding='utf-8').write(gen_norme(l))
    open(os.path.join(base,CHISONO_SLUG[l]+'.html'),'w',encoding='utf-8').write(gen_chisono(l))
    open(os.path.join(base,PETIZIONI_SLUG[l]+'.html'),'w',encoding='utf-8').write(gen_petizioni(l))
print('pagine tag:',tp,'| index+fonti+lingue x',len(LANGS))
urls=[BASE+'/']+['%s/%s/'%(BASE,l) for l in LANGS if l!='it']
for l in LANGS:
    for key in list(NEWS)+list(SHARES): urls.append('%s/s/%s/%s.html'%(BASE,l,key))
    for tg in VOC: urls.append('%s/s/%s/tag/%s.html'%(BASE,l,TAGSLUG[tg][l]))
    for pg in [IDX_SLUG[l],FONTI_SLUG[l],LINGUE_SLUG[l],norme.NORME_SLUG[l],CHISONO_SLUG[l],PETIZIONI_SLUG[l]]: urls.append('%s/s/%s/%s.html'%(BASE,l,pg))
sm='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
for u in urls: sm+='<url><loc>%s</loc></url>\n'%u
sm+='</urlset>\n'
open(os.path.join(REPO,'sitemap.xml'),'w',encoding='utf-8').write(sm)
open(os.path.join(REPO,'robots.txt'),'w',encoding='utf-8').write('User-agent: *\nAllow: /\n\nSitemap: %s/sitemap.xml\n'%BASE)
print('sitemap URL:',len(urls))
