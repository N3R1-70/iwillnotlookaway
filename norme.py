# -*- coding: utf-8 -*-
# Riferimenti normativi: testi giuridici primari, link al testo ufficiale integrale.
# URL VERIFICATI (un.org, OHCHR, ICRC). Default inglese (le pagine ufficiali hanno selettore lingua).

NORME_SLUG={'it':'riferimenti-normativi','en':'legal-references','fr':'references-juridiques',
 'de':'rechtsgrundlagen','es':'referencias-normativas','pt':'referencias-normativas',
 'tr':'hukuki-kaynaklar','zh':'legal-references','ar':'legal-references','he':'legal-references'}

UN6={'en','fr','es','ar','zh'}  # lingue ONU presenti sul sito
def _un(slug):
    return lambda l: 'https://www.un.org/%s/about-us/%s'%(l if l in UN6 else 'en', slug)
def norma_url(spec,l):
    return spec(l) if callable(spec) else spec

NORME=[
 ('charter','1945',_un('un-charter/full-text'),'un.org',{
   'it':'Carta delle Nazioni Unite','en':'Charter of the United Nations','fr':'Charte des Nations Unies',
   'de':'Charta der Vereinten Nationen','es':'Carta de las Naciones Unidas','pt':'Carta das Nações Unidas',
   'tr':'Birleşmiş Milletler Antlaşması','zh':'联合国宪章','ar':'ميثاق الأمم المتحدة','he':'מגילת האומות המאוחדות'}),
 ('udhr','1948','https://www.un.org/en/about-us/universal-declaration-of-human-rights','un.org',{
   'it':'Dichiarazione universale dei diritti umani','en':'Universal Declaration of Human Rights',
   'fr':"Déclaration universelle des droits de l'homme",'de':'Allgemeine Erklärung der Menschenrechte',
   'es':'Declaración Universal de Derechos Humanos','pt':'Declaração Universal dos Direitos Humanos',
   'tr':'İnsan Hakları Evrensel Beyannamesi','zh':'世界人权宣言','ar':'الإعلان العالمي لحقوق الإنسان',
   'he':'ההכרזה לכל באי עולם בדבר זכויות האדם'}),
 ('genocide','1948','https://www.ohchr.org/en/instruments-mechanisms/instruments/convention-prevention-and-punishment-crime-genocide','OHCHR',{
   'it':'Convenzione per la prevenzione e la repressione del crimine di genocidio',
   'en':'Convention on the Prevention and Punishment of the Crime of Genocide',
   'fr':'Convention pour la prévention et la répression du crime de génocide',
   'de':'Konvention über die Verhütung und Bestrafung des Völkermordes',
   'es':'Convención para la Prevención y la Sanción del Delito de Genocidio',
   'pt':'Convenção para a Prevenção e Repressão do Crime de Genocídio',
   'tr':'Soykırım Suçunun Önlenmesine ve Cezalandırılmasına Dair Sözleşme',
   'zh':'防止及惩治灭绝种族罪公约','ar':'اتفاقية منع جريمة الإبادة الجماعية والمعاقبة عليها',
   'he':"האמנה בדבר מניעתו וענישתו של הפשע השמדת עם"}),
 ('geneva','1949','https://ihl-databases.icrc.org/en/ihl-treaties/gciv-1949','ICRC',{
   'it':'IV Convenzione di Ginevra (1949) e Protocolli aggiuntivi (1977)',
   'en':'Fourth Geneva Convention (1949) and Additional Protocols (1977)',
   'fr':'IVe Convention de Genève (1949) et Protocoles additionnels (1977)',
   'de':'IV. Genfer Abkommen (1949) und Zusatzprotokolle (1977)',
   'es':'IV Convenio de Ginebra (1949) y Protocolos adicionales (1977)',
   'pt':'IV Convenção de Genebra (1949) e Protocolos Adicionais (1977)',
   'tr':'IV. Cenevre Sözleşmesi (1949) ve Ek Protokoller (1977)',
   'zh':'日内瓦第四公约（1949）及附加议定书（1977）','ar':'اتفاقية جنيف الرابعة (1949) والبروتوكولات الإضافية (1977)',
   'he':"אמנת ז'נבה הרביעית (1949) והפרוטוקולים הנוספים (1977)"}),
 ('refugees','1951','https://www.ohchr.org/en/instruments-mechanisms/instruments/convention-relating-status-refugees','OHCHR',{
   'it':'Convenzione sullo status dei rifugiati (1951) e Protocollo (1967)',
   'en':'Convention relating to the Status of Refugees (1951) and 1967 Protocol',
   'fr':'Convention relative au statut des réfugiés (1951) et Protocole (1967)',
   'de':'Genfer Flüchtlingskonvention (1951) und Protokoll (1967)',
   'es':'Convención sobre el Estatuto de los Refugiados (1951) y Protocolo (1967)',
   'pt':'Convenção relativa ao Estatuto dos Refugiados (1951) e Protocolo (1967)',
   'tr':'Mültecilerin Hukuki Durumuna Dair Sözleşme (1951) ve 1967 Protokolü',
   'zh':'关于难民地位的公约（1951）及议定书（1967）','ar':'الاتفاقية الخاصة بوضع اللاجئين (1951) وبروتوكولها (1967)',
   'he':'האמנה בדבר מעמדם של פליטים (1951) והפרוטוקול (1967)'}),
 ('crc','1989','https://www.ohchr.org/en/instruments-mechanisms/instruments/convention-rights-child','OHCHR',{
   'it':"Convenzione sui diritti dell'infanzia",'en':'Convention on the Rights of the Child',
   'fr':"Convention relative aux droits de l'enfant",'de':'Übereinkommen über die Rechte des Kindes',
   'es':'Convención sobre los Derechos del Niño','pt':'Convenção sobre os Direitos da Criança',
   'tr':'Çocuk Haklarına Dair Sözleşme','zh':'儿童权利公约','ar':'اتفاقية حقوق الطفل',
   'he':'האמנה בדבר זכויות הילד'}),
 ('opac','2000','https://www.ohchr.org/en/instruments-mechanisms/instruments/optional-protocol-convention-rights-child-involvement-children','OHCHR',{
   'it':"Protocollo opzionale alla Convenzione sui diritti dell'infanzia (coinvolgimento dei minori nei conflitti armati)",
   'en':'Optional Protocol on the involvement of children in armed conflict',
   'fr':"Protocole facultatif concernant l'implication d'enfants dans les conflits armés",
   'de':'Fakultativprotokoll betreffend die Beteiligung von Kindern an bewaffneten Konflikten',
   'es':'Protocolo facultativo relativo a la participación de niños en los conflictos armados',
   'pt':'Protocolo facultativo relativo à participação de crianças em conflitos armados',
   'tr':'Çocukların Silahlı Çatışmalara Dâhil Olmasına İlişkin İhtiyari Protokol',
   'zh':'关于儿童卷入武装冲突问题的任择议定书','ar':'البروتوكول الاختياري بشأن اشتراك الأطفال في النزاعات المسلحة',
   'he':'הפרוטוקול האופציונלי בדבר מעורבות ילדים בסכסוכים מזוינים'}),
 ('rome','1998','https://www.ohchr.org/en/instruments-mechanisms/instruments/rome-statute-international-criminal-court','OHCHR',{
   'it':'Statuto di Roma della Corte penale internazionale',
   'en':'Rome Statute of the International Criminal Court',
   'fr':'Statut de Rome de la Cour pénale internationale',
   'de':'Römisches Statut des Internationalen Strafgerichtshofs',
   'es':'Estatuto de Roma de la Corte Penal Internacional',
   'pt':'Estatuto de Roma do Tribunal Penal Internacional',
   'tr':'Uluslararası Ceza Mahkemesi Roma Statüsü',
   'zh':'国际刑事法院罗马规约','ar':'نظام روما الأساسي للمحكمة الجنائية الدولية',
   'he':'חוקת רומא של בית הדין הפלילי הבינלאומי'}),
]

N_TITLE={'it':'Riferimenti normativi','en':'Legal references','fr':'Références juridiques',
 'de':'Rechtsgrundlagen','es':'Referencias normativas','pt':'Referências normativas',
 'tr':'Hukuki kaynaklar','zh':'法律依据','ar':'المراجع القانونية','he':'מקורות משפטיים'}

N_INTRO={
 'it':'I testi giuridici primari su cui si misura ogni analisi di questa piattaforma. Ogni voce rimanda al testo ufficiale integrale. I trattati delle Nazioni Unite hanno valore ufficiale in sei lingue (arabo, cinese, francese, inglese, russo, spagnolo); dove non esiste una versione ufficiale nella lingua di questa pagina, il link porta al testo inglese — le pagine ufficiali includono comunque un selettore di lingua.',
 'en':"The primary legal texts against which every analysis on this platform is measured. Each entry links to the official full text. United Nations treaties are authoritative in six languages (Arabic, Chinese, English, French, Russian, Spanish); where no official version exists in this page's language, the link points to the English text — the official pages still include a language selector.",
 'fr':"Les textes juridiques primaires à l'aune desquels chaque analyse de cette plateforme est mesurée. Chaque entrée renvoie au texte officiel intégral. Les traités des Nations unies font foi en six langues (arabe, chinois, français, anglais, russe, espagnol) ; à défaut de version officielle dans la langue de cette page, le lien renvoie au texte anglais — les pages officielles proposent un sélecteur de langue.",
 'de':'Die primären Rechtstexte, an denen jede Analyse dieser Plattform gemessen wird. Jeder Eintrag verweist auf den amtlichen Volltext. Verträge der Vereinten Nationen sind in sechs Sprachen verbindlich (Arabisch, Chinesisch, Französisch, Englisch, Russisch, Spanisch); fehlt eine amtliche Fassung in der Sprache dieser Seite, führt der Link zum englischen Text — die amtlichen Seiten bieten eine Sprachauswahl.',
 'es':'Los textos jurídicos primarios con los que se contrasta cada análisis de esta plataforma. Cada entrada enlaza al texto oficial íntegro. Los tratados de las Naciones Unidas son auténticos en seis idiomas (árabe, chino, francés, inglés, ruso, español); cuando no existe versión oficial en el idioma de esta página, el enlace lleva al texto en inglés — las páginas oficiales incluyen un selector de idioma.',
 'pt':'Os textos jurídicos primários com que se mede cada análise desta plataforma. Cada entrada remete para o texto oficial integral. Os tratados das Nações Unidas são autênticos em seis línguas (árabe, chinês, francês, inglês, russo, espanhol); quando não existe versão oficial na língua desta página, a ligação leva ao texto inglês — as páginas oficiais incluem um seletor de idioma.',
 'tr':'Bu platformdaki her analizin kendisine göre ölçüldüğü birincil hukuki metinler. Her madde, resmî tam metne bağlanır. Birleşmiş Milletler antlaşmaları altı dilde resmîdir (Arapça, Çince, Fransızca, İngilizce, Rusça, İspanyolca); bu sayfanın dilinde resmî bir sürüm yoksa bağlantı İngilizce metne gider — resmî sayfalarda dil seçici bulunur.',
 'zh':'本平台每一项分析所对照的首要法律文本。每一条目均链接至官方完整文本。联合国条约以六种语言为准（阿拉伯文、中文、法文、英文、俄文、西班牙文）；若本页语言无官方版本，链接指向英文文本——官方页面均设有语言选择器。',
 'ar':'النصوص القانونية الأساسية التي يُقاس عليها كل تحليل في هذه المنصّة. تُحيل كل مادة إلى النص الرسمي الكامل. معاهدات الأمم المتحدة مُعتمَدة بست لغات (العربية والصينية والفرنسية والإنجليزية والروسية والإسبانية)؛ وحيث لا توجد نسخة رسمية بلغة هذه الصفحة، يقود الرابط إلى النص الإنجليزي — والصفحات الرسمية تتضمّن مُحدِّد لغة.',
 'he':'הטקסטים המשפטיים הראשוניים שמולם נמדד כל ניתוח בפלטפורמה זו. כל ערך מקשר לטקסט הרשמי המלא. אמנות האומות המאוחדות תקפות בשש שפות (ערבית, סינית, צרפתית, אנגלית, רוסית, ספרדית); היכן שאין גרסה רשמית בשפת עמוד זה, הקישור מוביל לטקסט האנגלי — בעמודים הרשמיים יש בורר שפה.'}

N_OFF={'it':'Testo ufficiale','en':'Official text','fr':'Texte officiel','de':'Amtlicher Text',
 'es':'Texto oficial','pt':'Texto oficial','tr':'Resmî metin','zh':'官方文本','ar':'النص الرسمي','he':'טקסט רשמי'}


# === RU (11a lingua) ===
NORME_SLUG['ru']='legal-references'
UN6.add('ru')
N_TITLE['ru']='Правовые источники'
N_OFF['ru']='Официальный текст'
N_INTRO['ru']='Первичные правовые тексты, по которым сверяется каждый анализ на этой платформе. Каждый пункт ведёт к официальному полному тексту. Договоры ООН аутентичны на шести языках (английский, арабский, испанский, китайский, русский, французский); где официальной версии на языке этой страницы нет, ссылка ведёт к английскому тексту — на официальных страницах есть переключатель языка.'
_RU_NAMES={
 'charter':'Устав Организации Объединённых Наций',
 'udhr':'Всеобщая декларация прав человека',
 'genocide':'Конвенция о предупреждении преступления геноцида и наказании за него',
 'geneva':'Четвёртая Женевская конвенция (1949) и Дополнительные протоколы (1977)',
 'refugees':'Конвенция о статусе беженцев (1951) и Протокол (1967)',
 'crc':'Конвенция о правах ребёнка',
 'opac':'Факультативный протокол, касающийся участия детей в вооружённых конфликтах',
 'rome':'Римский статут Международного уголовного суда'}
for _e in NORME: _e[4]['ru']=_RU_NAMES[_e[0]]
