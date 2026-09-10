# -*- coding: utf-8 -*-
"""Génère years.html, la page chronologique.

Appelée par build.py, jamais seule. Comme les autres pages du dépôt, la page
produite est autonome : aucune police distante, aucun script, aucun CDN. Le tri
du tableau se fait par boutons radio et par la propriété CSS order, dont les
règles sont écrites au build.

Trois panneaux :

1. La frise. Axe uniforme, années vides comprises. Une marque par morceau,
   empilée dans la colonne de son année. Toutes les marques font une année de
   large : encoder la précision sur la largeur chargeait la frise sans être
   lisible, arbitrage de Claire du 4 septembre 2026. La couleur dit le statut.

2. Les écarts. Une ligne par morceau dont la date Spotify s'éloigne de la
   première parution. Même axe que la frise. Ce panneau ne montre PLUS l'année
   d'enregistrement : un seul morceau la porte, et son point restait seul sur sa
   ligne, sans écart Spotify en face. Arbitrage de Claire du 6 septembre 2026.
   L'année d'enregistrement continue de vivre dans la fiche du morceau.

3. Le tableau, triable, chaque ligne dépliable sur sa fiche. Trois tris
   seulement : le tri « largest gap » a été retiré le 6 septembre 2026, faute de
   colonne disant l'écart et parce qu'il faisait doublon avec le panneau 2.

Aucun nombre n'est écrit en dur dans cette page : tout se recalcule depuis
years.py. Le titre affichait « cent quarante-cinq » alors que la playlist en
comptait cent quarante-six, ce qui est exactement le genre d'erreur qu'une
constante recopiée fabrique toute seule.

Le vide n'est pas recadré : les années sans morceau gardent leur largeur réelle.
C'est le même parti pris que les pays gris de la carte.
"""
from data import ART
from tracks import SECTIONS
from years import YEARS

def _span():
    """Bornes de l'axe : les seules dates effectivement dessinées.

    L'année d'enregistrement en est sortie le 6 septembre 2026, en même temps que
    du panneau 2 : garder 1962 pour Jackie Shane ajoutait une colonne vide en tête
    d'axe pour une donnée qui ne s'y trouve plus.
    """
    ys = []
    for v in YEARS.values():
        if v["first_public"]:
            ys.append(int(str(v["first_public"])[:4]))
        if v["spotify"]:
            ys.append(int(str(v["spotify"])[:4]))
    return min(ys), max(ys)


UNITS = ("zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
         "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
         "sixteen", "seventeen", "eighteen", "nineteen")
TENS = ("", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy",
        "eighty", "ninety")


def _words(n):
    """Le compte en toutes lettres, pour le titre. Sous mille, ce qui suffit."""
    if n < 20:
        return UNITS[n]
    if n < 100:
        t, u = divmod(n, 10)
        return TENS[t] + (f"-{UNITS[u]}" if u else "")
    h, r = divmod(n, 100)
    return UNITS[h] + " hundred" + (f" and {_words(r)}" if r else "")


Y0, Y1 = _span()
NY = Y1 - Y0 + 1

DAYS = (0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334)


def _parts(v):
    """(année, fraction dans l'année, précision) pour une valeur de date."""
    s = str(v)
    y = int(s[:4])
    if len(s) >= 10:
        m, d = int(s[5:7]), int(s[8:10])
        return y, min(0.999, (DAYS[m - 1] + d - 1) / 365.0), "day"
    if len(s) >= 7:
        return y, (DAYS[int(s[5:7]) - 1]) / 365.0, "month"
    return y, 0.0, "year"


def _rows():
    """Une entrée par morceau, dans l'ordre de la playlist."""
    out = []
    for sec in SECTIONS:
        for sid, title, credit in sec["tracks"]:
            v = YEARS[sid]
            py, pf, _ = _parts(v["first_public"])
            sy = _parts(v["spotify"])[0] if v["spotify"] else None
            ry = int(str(v["first_record"])[:4]) if v["first_record"] else None
            out.append({
                "id": sid, "title": title, "credit": credit,
                "y": py, "f": pf, "prec": v["precision"] or "year",
                "kind": v["kind"], "status": v["status"],
                "pub": str(v["first_public"]), "spot": v["spotify"],
                "sy": sy, "ry": ry,
                "gap_plat": (sy - py) if sy is not None else None,
                "gap_rec": (py - ry) if ry is not None else None,
                "source": v["source"] or "", "url": v["url"] or "",
                "checked": v["checked"] or "", "note": v["note"] or "",
            })
    return out


# ---------------------------------------------------------------- panneau 1

def _timeline(rows, esc, badge):
    W, PAD = 960.0, 10.0
    plot = W - 2 * PAD
    colw = plot / NY
    rowh, base = 11.0, 0.0

    by_year = {}
    for r in rows:
        by_year.setdefault(r["y"], []).append(r)
    for y in by_year:
        by_year[y].sort(key=lambda r: (r["pub"], r["title"]))
    tallest = max(len(v) for v in by_year.values())
    base = 18 + tallest * rowh
    H = base + 34

    CLS = {"verified": "m-ok", "partial": "m-her",
           "unresolved": "m-flag", "absent": "m-none"}

    g = []
    for d in range(1960, 2031, 10):
        if Y0 <= d <= Y1:
            x = PAD + (d - Y0) * colw
            g.append(f'<line class="grid" x1="{x:.1f}" y1="10" x2="{x:.1f}" y2="{base:.1f}"/>')
            g.append(f'<text class="ax" x="{x:.1f}" y="{base + 16:.1f}">{d}</text>')
    g.append(f'<line class="axis" x1="{PAD}" y1="{base:.1f}" x2="{W - PAD:.1f}" y2="{base:.1f}"/>')

    marks = []
    for y in sorted(by_year):
        for k, r in enumerate(by_year[y]):
            # Largeur fixe d'une annee. Encoder la precision sur la largeur
            # chargeait trop la frise, et la finesse au jour pres n'est de
            # toute facon pas lisible a l'oeil : elle vit dans le tableau.
            x = PAD + (r["y"] - Y0) * colw
            w = colw
            yy = base - (k + 1) * rowh + 1.4
            lab = f'{esc(r["credit"])} — {esc(r["title"])} — {esc(r["pub"])}'
            marks.append(
                f'<rect class="mk {CLS[r["status"]]}" x="{x:.2f}" y="{yy:.1f}" '
                f'width="{w:.2f}" height="{rowh - 2.8:.1f}" rx="1">'
                f'<title>{lab}</title></rect>')

    empty = NY - len(by_year)
    svg = (f'<svg class="chart" viewBox="0 0 {W:.0f} {H:.0f}" role="img" '
           f'aria-label="Timeline of the {len(rows)} songs from {Y0} to {Y1}, '
           f'one mark per song">'
           + "".join(g) + "".join(marks) + "</svg>")

    # La legende ne montre que les statuts effectivement presents : afficher
    # « unresolved » quand aucune ligne ne l'est laisse croire a une categorie
    # vide plutot qu'a une categorie absente.
    present = {r["status"] for r in rows}
    leg = "".join(f'<li><span class="sw {CLS[s]}"></span>{s}</li>'
                  for s in ("verified", "partial", "unresolved", "absent")
                  if s in present)
    return svg, f'<ul class="legend">{leg}</ul>', empty, tallest


# ---------------------------------------------------------------- panneau 2

def _gaps(rows, esc):
    # Un seul critere : l'ecart entre la premiere parution et la date Spotify.
    # Une ligne dont seul l'enregistrement s'ecartait — Jackie Shane — n'avait
    # aucun point Spotify en face et ne disait donc rien de ce que le panneau
    # mesure. Retiree le 6 septembre 2026.
    sel = [r for r in rows if (r["gap_plat"] or 0) >= 1]
    sel.sort(key=lambda r: (r["y"], r["sy"] or 0))

    W, LAB, PAD = 960.0, 272.0, 12.0
    plot = W - LAB - PAD
    rowh = 17.0
    H = 20 + len(sel) * rowh + 26
    sx = lambda y: LAB + (y - Y0) / (NY - 1) * plot

    g = []
    for d in range(1970, 2031, 10):
        if Y0 <= d <= Y1:
            x = sx(d)
            g.append(f'<line class="grid" x1="{x:.1f}" y1="12" x2="{x:.1f}" y2="{H - 24:.1f}"/>')
            g.append(f'<text class="ax" x="{x:.1f}" y="{H - 8:.1f}">{d}</text>')

    body = []
    for i, r in enumerate(sel):
        yy = 20 + i * rowh
        xp, xs = sx(r["y"]), sx(r["sy"]) if r["sy"] is not None else None
        name = f'{r["credit"]} — {r["title"]}'
        if len(name) > 36:
            name = name[:35] + "…"
        body.append(f'<text class="lb" x="{LAB - 10:.1f}" y="{yy + 4:.1f}">{esc(name)}</text>')
        if xs is not None:
            body.append(f'<line class="plat" x1="{xp:.1f}" y1="{yy:.1f}" x2="{xs:.1f}" y2="{yy:.1f}"/>')
            body.append(f'<circle class="dot-spot" cx="{xs:.1f}" cy="{yy:.1f}" r="3.1">'
                        f'<title>Spotify shows {r["spot"]}</title></circle>')
        body.append(f'<circle class="dot-pub" cx="{xp:.1f}" cy="{yy:.1f}" r="3.4">'
                    f'<title>first published {esc(r["pub"])}</title></circle>')

    svg = (f'<svg class="chart" viewBox="0 0 {W:.0f} {H:.0f}" role="img" '
           f'aria-label="Gap between first publication and the date Spotify shows, '
           f'for the {len(sel)} songs where the two differ">'
           + "".join(g) + "".join(body) + "</svg>")
    total = sum(r["gap_plat"] for r in sel)
    leg = ('<ul class="legend">'
           '<li><span class="sw dot-pub"></span>first published</li>'
           '<li><span class="sw dot-spot"></span>date Spotify shows</li>'
           '</ul>')
    return svg, leg, len(sel), total


# ---------------------------------------------------------------- panneau 3

# Trois tris, pas quatre. « Largest gap » a été retiré le 6 septembre 2026 :
# il ordonnait le tableau sur une grandeur qu'aucune colonne n'affichait, et
# cette grandeur est déjà le sujet entier du panneau 2.
SORTS = [
    ("s0", "Playlist order", lambda rows: list(range(len(rows)))),
    ("s1", "Earliest first", None),
    ("s2", "Latest first", None),
]


def _order_css(rows):
    """Une règle par ligne et par tri. Pas de script : c'est l'ordre CSS qui trie."""
    keys = {
        "s1": lambda r: (r["pub"], r["credit"]),
        "s2": lambda r: (tuple(-ord(c) for c in r["pub"]), r["credit"]),
    }
    out = []
    for sid, key in keys.items():
        rank = {id(r): i for i, r in enumerate(sorted(rows, key=key))}
        for i, r in enumerate(rows):
            out.append(f"#{sid}:checked~.rows>.k{i}{{order:{rank[id(r)]}}}")
    return "".join(out)


def _sources(source, url, esc):
    """Chaque source annoncée porte sa propre URL, ou aucune.

    `url` est une chaîne pour une source unique, un tuple pour plusieurs, apparié
    positionnellement aux segments de `source` séparés par des points-virgules.
    Un segment sans URL reste en texte simple : mieux vaut une source sans lien
    qu'une source pointant vers le lien d'une autre, défaut relevé par Claire le
    6 septembre 2026 sur les deux fiches Beth Elliott.
    """
    if not source:
        return ""
    urls = [url] if isinstance(url, str) else list(url or ())
    parts = [p.strip() for p in source.split(";")]
    if len(urls) > len(parts):          # plus d'URL que de segments : on ne devine pas
        parts = [source.strip()]
        urls = urls[:1]
    out = []
    for i, p in enumerate(parts):
        u = urls[i] if i < len(urls) and urls[i] else None
        out.append(f'<a href="{esc(u)}" target="_blank" rel="noopener">{esc(p)}</a>'
                   if u else esc(p))
    return " · ".join(out)


def _table(rows, esc, badge):
    # Les boutons radio sont des frères de .rows, sans quoi le sélecteur
    # #s1:checked~.rows ne peut pas les atteindre. Les libellés viennent après.
    ctrl = []
    for i, (sid, label, _) in enumerate(SORTS):
        chk = " checked" if i == 0 else ""
        ctrl.append(f'<input class="sortin" type="radio" name="sort" id="{sid}"{chk}>')
    ctrl.append('<div class="sorter">')
    for sid, label, _ in SORTS:
        ctrl.append(f'<label for="{sid}">{esc(label)}</label>')
    ctrl.append("</div>")

    items = []
    for i, r in enumerate(rows):
        lab, cls = badge.get(r["status"], (r["status"], "st-note"))
        gp = r["gap_plat"] or 0
        gr = r["gap_rec"] or 0
        chips = []
        if gr >= 1:
            chips.append(f'<span class="chip rec">recorded {r["ry"]}, '
                         f'{gr} year{"s" if gr > 1 else ""} earlier</span>')
        if gp >= 1:
            chips.append(f'<span class="chip plat">Spotify shows {esc(str(r["spot"]))}, '
                         f'{gp} year{"s" if gp > 1 else ""} later</span>')
        if r["kind"] == "earliest_known":
            chips.append('<span class="chip kind">at the latest</span>')
        src = _sources(r["source"], r["url"], esc)
        items.append(
            f'<details class="row k{i}">'
            f'<summary><span class="yr">{r["y"]}</span>'
            f'<span class="st {cls}">{esc(lab)}</span>'
            f'<span class="tt">{esc(r["title"])}</span>'
            f'<span class="cr">{esc(r["credit"])}</span></summary>'
            f'<div class="fiche">'
            f'<p class="meta">First publication held: <strong>{esc(r["pub"])}</strong>'
            f' · known to the {esc(r["prec"] or "year")}</p>'
            + (f'<p class="chips">{"".join(chips)}</p>' if chips else "")
            + (f'<p class="desc">{esc(r["note"])}</p>' if r["note"] else "")
            + f'<p class="src">{src} · checked {esc(r["checked"])} · '
            f'<a href="https://open.spotify.com/track/{r["id"]}" '
            f'target="_blank" rel="noopener">listen</a></p>'
            f"</div></details>")
    return "".join(ctrl) + '<div class="rows">' + "".join(items) + "</div>"


# ---------------------------------------------------------------- page

CSS = """
.chartwrap{overflow-x:auto;border:1px solid var(--line);border-radius:9px;
 background:var(--panel);padding:14px 12px;margin:18px 0 0}
svg.chart{display:block;width:100%;min-width:640px;height:auto}
svg.chart .grid{stroke:var(--line);stroke-width:1}
svg.chart .axis{stroke:var(--muted);stroke-width:1;opacity:.5}
svg.chart .ax{fill:var(--muted);font:11px ui-sans-serif,system-ui,sans-serif;text-anchor:middle}
svg.chart .lb{fill:var(--ink);font:11px ui-sans-serif,system-ui,sans-serif;text-anchor:end}
svg.chart .mk{shape-rendering:crispEdges}
.m-ok{fill:var(--ok)} .m-her{fill:var(--her)} .m-flag{fill:var(--flag)} .m-none{fill:var(--muted)}
svg.chart .plat{stroke:var(--accent);stroke-width:1.6;opacity:.55}
svg.chart .dot-pub{fill:var(--ink)}
svg.chart .dot-spot{fill:var(--bg);stroke:var(--accent);stroke-width:1.6}
.legend .sw{width:13px;height:13px;border-radius:3px;display:inline-block;flex:none}
.legend .sw.m-ok{background:var(--ok)}
.legend .sw.m-her{background:var(--her)}
.legend .sw.m-flag{background:var(--flag)}
.legend .sw.m-none{background:var(--muted)}
.legend .sw.dot-pub{background:var(--ink);border-radius:99px;width:9px;height:9px}
.legend .sw.dot-spot{background:transparent;border:2px solid var(--accent);border-radius:99px;width:10px;height:10px}
.sorter{display:flex;flex-wrap:wrap;gap:8px;margin:22px 0 12px;
 font-family:ui-sans-serif,system-ui,sans-serif;font-size:.84rem}
.sortin{position:absolute;opacity:0;pointer-events:none}
.sorter label{cursor:pointer;padding:5px 12px;border-radius:99px;
 border:1px solid var(--line);color:var(--muted);background:var(--panel)}
#s0:checked~.sorter label[for=s0],#s1:checked~.sorter label[for=s1],
#s2:checked~.sorter label[for=s2]{
 background:var(--accent);border-color:var(--accent);color:var(--bg);font-weight:600}
.rows{display:flex;flex-direction:column;border:1px solid var(--line);
 border-radius:9px;background:var(--panel);overflow:hidden}
details.row{border-bottom:1px solid var(--line)}
details.row:last-of-type{border-bottom:0}
details.row summary{cursor:pointer;padding:9px 14px;display:flex;flex-wrap:wrap;
 align-items:baseline;gap:10px;font-family:ui-sans-serif,system-ui,sans-serif;font-size:.9rem}
details.row summary::marker{color:var(--muted)}
details.row[open]{background:var(--soft)}
.yr{font-variant-numeric:tabular-nums;color:var(--ink);font-weight:600;font-size:.85rem;min-width:4.2ch}
.tt{font-weight:600;flex:1 1 16ch}
summary .cr{color:var(--muted);font-size:.85rem}
.fiche{padding:2px 14px 14px 14px;font-family:ui-sans-serif,system-ui,sans-serif}
.fiche p{max-width:74ch}
.fiche .meta{margin:0 0 8px;font-size:.8rem;color:var(--muted)}
.fiche .desc{margin:0 0 8px;font-size:.87rem;line-height:1.55}
.fiche .src{margin:0;font-size:.79rem;color:var(--muted)}
.chips{margin:0 0 8px;display:flex;flex-wrap:wrap;gap:6px}
.chip{font-size:.72rem;padding:2px 9px;border-radius:99px;border:1px solid var(--line);color:var(--muted)}
.chip.rec{border-color:var(--muted)}
.chip.plat{border-color:var(--accent);color:var(--accent)}
"""


def years_page(css, esc, slug, artists_of, aliases, same_person, badge,
               playlist, issues):
    rows = _rows()
    tl, tl_leg, empty, tallest = _timeline(rows, esc, badge)
    gp, gp_leg, ngap, total_gap = _gaps(rows, esc)
    table = _table(rows, esc, badge)

    n = len(rows)
    verified = sum(1 for r in rows if r["status"] == "verified")
    partial = sum(1 for r in rows if r["status"] == "partial")
    unres = sum(1 for r in rows if r["status"] == "unresolved")
    occupied = len({r["y"] for r in rows})

    nav = ('<nav class="pagenav">'
           '<a href="index.html">Sources</a>'
           '<a href="countries.html">By country</a>'
           '<a href="languages.html">By language</a>'
           '<span class="here">By year</span>'
           '<a href="takedown.html">Removals</a>'
           '</nav>')

    body = f"""
<header>
<h1>{_words(n).capitalize()} songs, and when they first existed</h1>
<p class="sub">Every track on the playlist, placed on a single uniform axis from
{Y0} to {Y1}. The empty stretches are kept at full width, because they are part
of what this page measures.</p>
<p class="stats"><strong>{n}</strong> tracks · <strong>{verified}</strong> verified,
<strong>{partial}</strong> partial, <strong>{unres}</strong> unresolved ·
<strong>{occupied}</strong> years hold a track, <strong>{empty}</strong> hold none ·
tallest year: <strong>{tallest}</strong> tracks.</p>
</header>

<h2>When each song first existed</h2>
<p>One mark per song, one column per year, stacked. Every mark is one year wide,
whatever the precision of the date behind it: the exact day a song appeared is
recorded on its row further down, but it is far too fine a distinction to read on
a chart. Colour carries how firmly the date is established.</p>
<div class="chartwrap">{tl}</div>
{tl_leg}
<div class="note">
<h4>What this chart does and does not measure</h4>
<p>It measures this playlist. Its shape reflects how the playlist was built, which
follows collaborations, labels and scenes rather than press coverage, and which
therefore reaches recent and online-native artists more easily than older ones.
A thin left-hand tail is not a claim that transfeminine music began in the 2010s.</p>
<p>The empty years are shown at their real width for the same reason the grey
countries stay on the map: what is missing is not nothing, and hiding it would be
the more misleading choice.</p>
</div>

<h2>How far Spotify moves them</h2>
<p>One line per song that Spotify dates later than its first publication: the
filled dot is when the song first existed, the open dot is the year Spotify prints,
and the line between them is the distance. The scale is the same as above.
<strong>{ngap}</strong> of the {n} songs are displaced, by
<strong>{total_gap}</strong> years in total, and every one of them moves the same
way: towards the present. A reissue carries the date of its reissue, so a life's
work can arrive on a streaming platform looking like a debut.</p>
<div class="chartwrap">{gp}</div>
{gp_leg}
<div class="note">
<p>Unlike the chart above, this one does not depend on how the playlist was
assembled. Each song is compared with itself, so each artist is her own control.
The oldest songs are moved by decades and everything after 2010 barely moves at
all — which is the point: the further back a transfeminine singer worked, the
more the catalogue that carries her today misdates her.</p>
<p>Songs Spotify dates correctly do not appear here, and neither does the one
song whose recording year is documented and earlier than its first publication.
That gap is a different measurement, and it is written on the song's own row.</p>
</div>

<h2>Every track</h2>
<p><em>First publication</em> means the first time the song existed in public in
any form at all: a night on a stage counts, a cassette passed hand to hand counts,
a streaming release counts. It is not the recording date and not the release date,
though for a song made after about 2010 the three usually fall together. For a
cover version it is this singer's own first public performance, never the age of
the song she is singing.</p>
<p>Three orders: the playlist's own, oldest first, newest first. Each row opens on
the sources that fixed its date, each one linking to the page it names, on when
they were last checked, and on whatever doubt remains. The badge sits beside the
year because it qualifies the year, not the artist.</p>
{table}

<footer>
<p class="colophon">Dates established between the sources listed on each row.
A date marked <em>at the latest</em> means the song existed by then and may be
older; nothing here claims to be the last word. Corrections are welcome as an
<a href="{issues}" target="_blank" rel="noopener">issue on the repository</a>,
which is a public thread. To have an entry taken down, or to raise anything about
a person’s identity, use the
<a href="takedown.html">private channel</a> instead.</p>
<p class="colophon"><a href="{playlist}" target="_blank" rel="noopener">Listen to the playlist</a></p>
</footer>
"""

    full = css + CSS + _order_css(rows)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Transfem chants — by year</title>
<meta name="description" content="When each of the {n} songs first existed, and how far Spotify metadata moves them.">
<style>{full}</style>
</head>
<body>
<div class="wrap">
{nav}
{body}
</div>
</body>
</html>
"""
