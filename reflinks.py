# -*- coding: utf-8 -*-
# Punto 2: link in linea. Riconosce i nomi degli strumenti giuridici nei corpi
# degli articoli e li collega alla pagina Riferimenti normativi (ancora #chiave).
# Linka una sola volta per strumento per pagina; salta i tag HTML e gli <a> esistenti.
import re, norme

# Ordine: i nomi più specifici (rifugiati = "Ginevra 1951") prima di Ginevra generica.
ORDER=['charter','rome','udhr','genocide','refugees','geneva']

LINKPATS={
'charter':{'it':['Carta delle Nazioni Unite','Carta ONU'],'en':['Charter of the United Nations','UN Charter'],
 'fr':['Charte des Nations unies'],'de':['UN-Charta','Charta der Vereinten Nationen'],
 'es':['Carta de las Naciones Unidas'],'pt':['Carta das Na\u00e7\u00f5es Unidas'],
 'tr':['Birle\u015fmi\u015f Milletler Antla\u015fmas\u0131','BM Antla\u015fmas\u0131'],
 'zh':['\u8054\u5408\u56fd\u5baa\u7ae0'],'ar':['\u0645\u064a\u062b\u0627\u0642 \u0627\u0644\u0623\u0645\u0645 \u0627\u0644\u0645\u062a\u062d\u062f\u0629'],
 'he':['\u05de\u05d2\u05d9\u05dc\u05ea \u05d4\u05d0\u05d5\u05de\u05d5\u05ea \u05d4\u05de\u05d0\u05d5\u05d7\u05d3\u05d5\u05ea']},
'rome':{'it':['Statuto di Roma'],'en':['Rome Statute'],'fr':['Statut de Rome'],
 'de':['R\u00f6misches Statut','R\u00f6mische Statut'],'es':['Estatuto de Roma'],'pt':['Estatuto de Roma'],
 'tr':['Roma Stat\u00fcs\u00fc'],'zh':['\u7f57\u9a6c\u89c4\u7ea6'],
 'ar':['\u0646\u0638\u0627\u0645 \u0631\u0648\u0645\u0627 \u0627\u0644\u0623\u0633\u0627\u0633\u064a','\u0646\u0638\u0627\u0645 \u0631\u0648\u0645\u0627'],
 'he':['\u05d7\u05d5\u05e7\u05ea \u05e8\u05d5\u05de\u05d0']},
'udhr':{'it':['Dichiarazione universale dei diritti umani'],'en':['Universal Declaration of Human Rights'],
 'fr':['D\u00e9claration universelle des droits de l\u2019homme','D\u00e9claration universelle des droits de l\'homme'],
 'de':['Allgemeine Erkl\u00e4rung der Menschenrechte'],'es':['Declaraci\u00f3n Universal de los Derechos Humanos'],
 'pt':['Declara\u00e7\u00e3o Universal dos Direitos Humanos'],'tr':['\u0130nsan Haklar\u0131 Evrensel Beyannamesi'],
 'zh':['\u4e16\u754c\u4eba\u6743\u5ba3\u8a00'],'ar':['\u0627\u0644\u0625\u0639\u0644\u0627\u0646 \u0627\u0644\u0639\u0627\u0644\u0645\u064a \u0644\u062d\u0642\u0648\u0642 \u0627\u0644\u0625\u0646\u0633\u0627\u0646'],
 'he':['\u05d4\u05d4\u05db\u05e8\u05d6\u05d4 \u05dc\u05db\u05dc \u05d1\u05d0\u05d9 \u05e2\u05d5\u05dc\u05dd \u05d1\u05d3\u05d1\u05e8 \u05d6\u05db\u05d5\u05d9\u05d5\u05ea \u05d4\u05d0\u05d3\u05dd']},
'genocide':{'it':['Convenzione per la prevenzione e la repressione del crimine di genocidio','Convenzione sul genocidio'],
 'en':['Genocide Convention'],'fr':['Convention sur le g\u00e9nocide','Convention pour la pr\u00e9vention'],
 'de':['V\u00f6lkermordkonvention'],'es':['Convenci\u00f3n sobre el Genocidio','Convenci\u00f3n para la Prevenci\u00f3n'],
 'pt':['Conven\u00e7\u00e3o sobre o Genoc\u00eddio'],'tr':['Soyk\u0131r\u0131m S\u00f6zle\u015fmesi'],
 'zh':['\u706d\u7edd\u79cd\u65cf\u7f6a\u516c\u7ea6','\u79cd\u65cf\u706d\u7edd\u516c\u7ea6'],
 'ar':['\u0627\u062a\u0641\u0627\u0642\u064a\u0629 \u0645\u0646\u0639 \u062c\u0631\u064a\u0645\u0629 \u0627\u0644\u0625\u0628\u0627\u062f\u0629 \u0627\u0644\u062c\u0645\u0627\u0639\u064a\u0629','\u0627\u062a\u0641\u0627\u0642\u064a\u0629 \u0627\u0644\u0625\u0628\u0627\u062f\u0629 \u0627\u0644\u062c\u0645\u0627\u0639\u064a\u0629'],
 'he':['\u05d0\u05de\u05e0\u05ea \u05e8\u05e6\u05d7 \u05d4\u05e2\u05dd']},
'refugees':{'it':['Convenzione di Ginevra del 1951','Convenzione sui rifugiati','status dei rifugiati'],
 'en':['1951 Refugee Convention','Refugee Convention'],'fr':['Convention de 1951','Convention relative au statut des r\u00e9fugi\u00e9s'],
 'de':['Genfer Fl\u00fcchtlingskonvention','Fl\u00fcchtlingskonvention'],
 'es':['Convenci\u00f3n sobre el Estatuto de los Refugiados','Convenci\u00f3n de Refugiados'],
 'pt':['Conven\u00e7\u00e3o relativa ao Estatuto dos Refugiados'],
 'tr':['M\u00fclteci S\u00f6zle\u015fmesi','M\u00fcltecilerin Hukuki Durumuna Dair S\u00f6zle\u015fme'],
 'zh':['\u96be\u6c11\u5730\u4f4d\u516c\u7ea6','\u96be\u6c11\u516c\u7ea6'],
 'ar':['\u0627\u062a\u0641\u0627\u0642\u064a\u0629 \u0627\u0644\u0644\u0627\u062c\u0626\u064a\u0646','\u0627\u0644\u0627\u062a\u0641\u0627\u0642\u064a\u0629 \u0627\u0644\u062e\u0627\u0635\u0629 \u0628\u0648\u0636\u0639 \u0627\u0644\u0644\u0627\u062c\u0626\u064a\u0646'],
 'he':['\u05d0\u05de\u05e0\u05ea \u05d4\u05e4\u05dc\u05d9\u05d8\u05d9\u05dd']},
'geneva':{'it':['Convenzioni di Ginevra','Convenzione di Ginevra'],'en':['Geneva Conventions','Geneva Convention'],
 'fr':['Conventions de Gen\u00e8ve','Convention de Gen\u00e8ve'],'de':['Genfer Abkommen'],
 'es':['Convenios de Ginebra','Convenio de Ginebra'],'pt':['Conven\u00e7\u00f5es de Genebra','Conven\u00e7\u00e3o de Genebra'],
 'tr':['Cenevre S\u00f6zle\u015fmeleri','Cenevre S\u00f6zle\u015fmesi'],
 'zh':['\u65e5\u5185\u74e6\u516c\u7ea6'],'ar':['\u0627\u062a\u0641\u0627\u0642\u064a\u0627\u062a \u062c\u0646\u064a\u0641','\u0627\u062a\u0641\u0627\u0642\u064a\u0629 \u062c\u0646\u064a\u0641'],
 'he':['\u05d0\u05de\u05e0\u05d5\u05ea \u05d6\'\u05e0\u05d1\u05d4','\u05d0\u05de\u05e0\u05ea \u05d6\'\u05e0\u05d1\u05d4']},
}

def _protected(s):
    r=[]
    for m in re.finditer(r'<a\b[^>]*>.*?</a>', s, re.S): r.append((m.start(),m.end()))
    for m in re.finditer(r'<[^>]+>', s): r.append((m.start(),m.end()))
    return r
def _inside(pos,r): return any(a<=pos<b for a,b in r)

def linkify_refs(s, l, linked=None):
    if linked is None: linked=set()
    slug=norme.NORME_SLUG[l]; base='/s/%s/%s.html'%(l,slug)
    for key in ORDER:
        if key in linked: continue
        for ph in LINKPATS.get(key,{}).get(l,[]):
            done=False
            for m in re.finditer(re.escape(ph), s):
                if not _inside(m.start(), _protected(s)):
                    a='<a class="ref" href="%s#%s">%s</a>'%(base,key,s[m.start():m.end()])
                    s=s[:m.start()]+a+s[m.end():]; linked.add(key); done=True; break
            if done: break
    return s


# === RU (11a lingua) ===
for _k,_v in {
 'charter':['Устав ООН','Устав Организации Объединённых Наций'],
 'rome':['Римский статут'],
 'udhr':['Всеобщая декларация прав человека'],
 'genocide':['Конвенция о предупреждении преступления геноцида','Конвенция о геноциде'],
 'refugees':['Конвенция о статусе беженцев','Конвенция 1951 года'],
 'geneva':['Женевские конвенции','Женевская конвенция'],
}.items(): LINKPATS[_k]['ru']=_v

# CRC — Convenzione sui diritti dell'infanzia (aggiunto)
LINKPATS['crc']={
  'it':["Convenzione sui Diritti dell'Infanzia","Convenzione sui diritti dell'infanzia"],
  'en':['Convention on the Rights of the Child'],
  'fr':['Convention relative aux droits de l’enfant',"Convention relative aux droits de l'enfant"],
  'de':['Kinderrechtskonvention','Übereinkommen über die Rechte des Kindes'],
  'es':['Convención sobre los Derechos del Niño'],
  'pt':['Convenção sobre os Direitos da Criança'],
  'tr':['Çocuk Haklarına Dair Sözleşme'],
  'zh':['儿童权利公约'],
  'ar':['اتفاقية حقوق الطفل'],
  'he':['אמנת זכויות הילד','האמנה בדבר זכויות הילד'],
  'ru':['Конвенция о правах ребёнка'],
}
if 'crc' not in ORDER: ORDER.append('crc')

# genocide — varianti di forma/casatura usate nei corpi (nd-coi, nd-mya)
for _l,_extra in {'it':['Convenzione sul Genocidio'],'zh':['灭绝种族公约'],'ar':['اتفاقية منع الإبادة الجماعية'],'he':['אמנת מניעת רצח העם']}.items():
    LINKPATS['genocide'].setdefault(_l,[]).extend(_extra)

# OPAC — Protocollo opzionale (coinvolgimento minori nei conflitti armati). Va PRIMA di crc nell'ORDER
# perché la frase lunga contiene il nome della CRC.
LINKPATS['opac']={
 'it':["Protocollo opzionale alla Convenzione sui diritti dell'infanzia"],
 'en':['Optional Protocol to the Convention on the Rights of the Child'],
 'fr':["Protocole facultatif à la Convention relative aux droits de l'enfant"],
 'de':['Fakultativprotokoll zum Übereinkommen über die Rechte des Kindes'],
 'es':['Protocolo facultativo de la Convención sobre los Derechos del Niño'],
 'pt':['Protocolo facultativo à Convenção sobre os Direitos da Criança'],
 'tr':["Çocuk Haklarına Dair Sözleşme'ye Ek İhtiyari Protokol"],
 'zh':['关于儿童卷入武装冲突问题的任择议定书'],
 'ar':['البروتوكول الاختياري لاتفاقية حقوق الطفل'],
 'he':['הפרוטוקול האופציונלי לאמנה בדבר זכויות הילד'],
 'ru':['Факультативный протокол к Конвенции о правах ребёнка'],
}
if 'opac' not in ORDER:
    ORDER.insert(ORDER.index('crc') if 'crc' in ORDER else len(ORDER), 'opac')

# russo: forme declinate usate nei corpi (nd-ht)
LINKPATS['opac']['ru'].append('Факультативным протоколом к Конвенции о правах ребёнка')
LINKPATS['crc']['ru'].append('Конвенцию о правах ребёнка')
