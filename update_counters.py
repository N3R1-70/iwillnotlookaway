#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# update_counters.py — ricalcola i contatori della home (lingue/manifesti/notizie)
# dal sorgente repo_bak e li scrive in tutte le home repo/. Da lanciare dopo ogni
# integrazione di una notizia/manifesto. NON tocca 'fonti' (contatore curato a mano).
#
# Uso:  python3 update_counters.py
import re, os

SRC = 'repo_bak/index.html'   # sorgente notizie/manifesti
LANGS = ['it','en','fr','de','es','pt','tr','zh','ar','he','ru']

h = open(SRC, encoding='utf-8').read()
notizie   = len(set(re.findall(r'data-news="(nd-[^"]+)"', h)))
manifesti = len(set(re.findall(r'data-share-key="(m[^"]*)"', h)))
lingue    = len(LANGS)

counts = {'lingue': lingue, 'manifesti': manifesti, 'notizie': notizie}
print(f"Conteggi dal sorgente: lingue={lingue} manifesti={manifesti} notizie={notizie} (fonti: invariato)")

changed = 0
for l in LANGS:
    p = 'repo/index.html' if l == 'it' else f'repo/{l}/index.html'
    if not os.path.exists(p):
        print(f"  ATTENZIONE: manca {p}"); continue
    txt = open(p, encoding='utf-8').read()
    new = txt
    for k, v in counts.items():
        new = re.sub(rf'(cnt-{k}">)\d+(<)', rf'\g<1>{v}\g<2>', new)
    if new != txt:
        open(p, 'w', encoding='utf-8').write(new); changed += 1

print(f"Home aggiornate: {changed}/{len(LANGS)}")
