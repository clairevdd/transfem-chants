# -*- coding: utf-8 -*-
"""Régénère ARTISTES.md, miroir lisible de data.py. data.py fait foi."""
import datetime
from collections import Counter
from data import ART
from tracks import all_tracks
from build import SAME_PERSON, COUNTRY_ALIASES

STATUS_ORDER = list(ART.keys())
counts = Counter(c for _, _, c in all_tracks() for c in [c])
per_artist = Counter()
for _, _, credit in all_tracks():
    names = [n.strip() for n in credit.split(",")]
    for n in names:
        per_artist[n] += 1

def esc(s):
    return s.replace("|", "\\|")

def src(name):
    e = ART[name]
    return "[%s](%s)" % (e[5], e[6]) if len(e) == 7 else "[%s](%s)" % (e[6], e[7])

mains = [n for n, e in ART.items() if e[0] != "guest"]
guests = [n for n, e in ART.items() if e[0] == "guest"]
orphans = [n for n in mains if per_artist.get(n, 0) == 0]

# comptages publics
on_playlist = set(per_artist)
canon = {}
for n in mains:
    if n in on_playlist:
        canon[SAME_PERSON.get(n, n)] = ART[n]
transfem = [n for n, e in canon.items() if e[0] != "unresolved"]
open_cases = [n for n, e in canon.items() if e[0] == "unresolved"]
countries, langs = set(), set()
for n, e in canon.items():
    if e[1] != "Unknown":
        for c in e[1].split(" / "):
            c = c.strip()
            countries.add(COUNTRY_ALIASES.get(c, c))
    if e[2] != "\u2014":
        for l in e[2].split(","):
            langs.add(l.strip())

L = []
L.append("# Transfem chants — table des artistes\n")
L.append("Export lisible de `data.py`. **`data.py` fait foi.**\n")
L.append("## Où on en est\n")
L.append("- **%d morceaux**" % len(all_tracks()))
L.append("- **%d artistes présentées comme transféminines**, plus **%d cas ouverts**"
         % (len(transfem), len(open_cases)))
L.append("- **%d pays ou territoires** : %s" % (len(countries), ", ".join(sorted(countries))))
L.append("- **%d langues** : %s\n" % (len(langs), ", ".join(sorted(langs))))
L.append("Généré le %s\n" % datetime.date.today().isoformat())

L.append("## Artistes principales\n")
L.append("| Artiste | Statut | Pays | Langue | Titres | Source |")
L.append("|---|---|---|---|---|---|")
for n in mains:
    e = ART[n]
    L.append("| **%s** | `%s` | %s | %s | %d | %s |"
             % (esc(n), e[0], esc(e[1]), esc(e[2]), per_artist.get(n, 0), src(n)))
L.append("")

L.append("## Crédits invités\n")
L.append("| Artiste | Pays | Source |")
L.append("|---|---|---|")
for n in guests:
    e = ART[n]
    s = src(n) if e[6] else "_aucune_"
    L.append("| %s | %s | %s |" % (esc(n), esc(e[1]), s))
L.append("")

if orphans:
    L.append("## Vérifiées mais sans morceau associé\n")
    L.append("Prêtes à entrer dès qu'un titre leur est associé.\n")
    for n in orphans:
        e = ART[n]
        L.append("- **%s** — `%s`, %s, %s. Source : %s" % (n, e[0], e[1], e[2], src(n)))
    L.append("")

L.append("## Citations retenues\n")
L.append("Reproduites mot pour mot.\n")
for n in mains:
    e = ART[n]
    q = e[4]
    if q:
        L.append("- **%s** — « %s » (%s)" % (n, q, e[5]))
L.append("")

open("ARTISTES.md", "w").write("\n".join(L))
print("ARTISTES.md : %d artistes, %d invitées, %d orphelines" % (len(mains), len(guests), len(orphans)))
