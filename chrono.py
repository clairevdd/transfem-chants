# -*- coding: utf-8 -*-
"""Génère years.html, la page chronologique.

Appelée par build.py, jamais seule. Comme les autres pages du dépôt, la page
produite est autonome : aucune police distante, aucun script, aucun CDN. Le tri
du tableau se fait par boutons radio et par la propriété CSS order, dont les
règles sont écrites au build.

Trois panneaux :

1. La frise. Axe uniforme de 1963 à 2026, années vides comprises. Une marque par
   morceau, empilée dans la colonne de son année. La largeur de la marque dit la
   précision de la date : un trait fin pour une date au jour, la colonne entière
   pour une date connue à l'année près. Les anciennes sont donc visiblement plus
   floues, et c'est de la donnée, pas de la mise en page.

2. Les écarts. Une ligne par morceau dont la date affichée par la plateforme, ou
   la date d'enregistrement, s'éloigne de la parution. Même axe que la frise.

3. Le tableau des 145 morceaux, triable, chaque ligne dépliable sur sa fiche.

Le vide n'est pas recadré. Sur les 64 années de l'axe, 42 sont sans morceau, et
cette traîne est le résultat autant que les pics. C'est le même parti pris que
les pays gris de la carte : montrer ce qui manque à sa taille réelle.
"""
from data import ART
from tracks import SECTIONS
from years import YEARS

def _span():
    """Bornes de l'axe : la plus ancienne date du tableau, enregistrements compris.

    Jackie Shane a été enregistré en 1962 et paru en 1963 : sans cette borne,
    son point d'enregistrement tomberait hors du graphique.
    """
    ys = []
    for v in YEARS.values():
        if v["first_public"]:
            ys.append(int(str(v["first_public"])[:4]))
        if v["first_record"]:
            ys.append(int(str(v["first_record"])[:4]))
        if v["spotify"]:
            ys.append(int(str(v["spotify"])[:4]))
    return min(ys), max(ys)


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
    for si, sec in enumerate(SECTIONS):
        for sid, title, credit in sec["tracks"]:
            v = YEARS[sid]
            py, pf, _ = _parts(v["first_public"])
            sy = _parts(v["spotify"])[0] if v["spotify"] else None
            ry = int(str(v["first_record"])[:4]) if v["first_record"] else None
            out.append({
                "id": sid, "title": title, "credit": credit,
                "section": sec["title"], "sec": si,
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
           f'aria-label="Frise des 145 morceaux de 1963 à 2026, une marque par morceau">'
           + "".join(g) + "".join(marks) + "</svg>")

    leg = ('<ul class="legend">'
           '<li><span class="sw m-ok"></span>verified</li>'
           '<li><span class="sw m-her"></span>partial</li>'
           '<li><span class="sw m-flag"></span>unresolved</li>'
           '</ul>')
    return svg, leg, empty, tallest


# ---------------------------------------------------------------- panneau 2

def _gaps(rows, esc):
    sel = [r for r in rows
           if (r["gap_plat"] or 0) >= 1 or (r["gap_rec"] or 0) >= 1]
    sel.sort(key=lambda r: (r["ry"] or r["y"], r["y"]))

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
        if r["ry"] is not None and r["gap_rec"] >= 1:
            xr = sx(r["ry"])
            body.append(f'<line class="rec" x1="{xr:.1f}" y1="{yy:.1f}" x2="{xp:.1f}" y2="{yy:.1f}"/>')
            body.append(f'<circle class="dot-rec" cx="{xr:.1f}" cy="{yy:.1f}" r="3.1">'
                        f'<title>recorded in {r["ry"]}</title></circle>')
        if xs is not None and r["gap_plat"] >= 1:
            body.append(f'<line class="plat" x1="{xp:.1f}" y1="{yy:.1f}" x2="{xs:.1f}" y2="{yy:.1f}"/>')
            body.append(f'<circle class="dot-spot" cx="{xs:.1f}" cy="{yy:.1f}" r="3.1">'
                        f'<title>shown as {r["spot"]} by the platform</title></circle>')
        body.append(f'<circle class="dot-pub" cx="{xp:.1f}" cy="{yy:.1f}" r="3.4">'
                    f'<title>first published {esc(r["pub"])}</title></circle>')

    svg = (f'<svg class="chart" viewBox="0 0 {W:.0f} {H:.0f}" role="img" '
           f'aria-label="Écarts entre enregistrement, parution et date de plateforme">'
           + "".join(g) + "".join(body) + "</svg>")
    total = sum(r["gap_plat"] for r in rows if (r["gap_plat"] or 0) >= 1)
    leg = ('<ul class="legend">'
           '<li><span class="sw dot-rec"></span>recorded</li>'
           '<li><span class="sw dot-pub"></span>first published</li>'
           '<li><span class="sw dot-spot"></span>date shown by the platform</li>'
           '</ul>')
    return svg, leg, len(sel), total


# ---------------------------------------------------------------- panneau 3

SORTS = [
    ("s0", "Playlist order", lambda rows: list(range(len(rows)))),
    ("s1", "Earliest first", None),
    ("s2", "Latest first", None),
    ("s3", "Largest gap", None),
]


def _order_css(rows):
    """Une règle par ligne et par tri. Pas de script : c'est l'ordre CSS qui trie."""
    keys = {
        "s1": lambda r: (r["pub"], r["credit"]),
        "s2": lambda r: (tuple(-ord(c) for c in r["pub"]), r["credit"]),
        "s3": lambda r: (-(max(r["gap_plat"] or 0, r["gap_rec"] or 0)), r["pub"]),
    }
    out = []
    for sid, key in keys.items():
        rank = {id(r): i for i, r in enumerate(sorted(rows, key=key))}
        for i, r in enumerate(rows):
            out.append(f"#{sid}:checked~.rows>.k{i}{{order:{rank[id(r)]}}}")
    return "".join(out)


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
            chips.append(f'<span class="chip rec">recorded {r["ry"]}, {gr} years earlier</span>')
        if gp >= 1:
            chips.append(f'<span class="chip plat">platform says {esc(str(r["spot"]))}, {gp} years later</span>')
        if r["kind"] == "earliest_known":
            chips.append('<span class="chip kind">at the latest</span>')
        src = esc(r["source"])
        if r["url"]:
            src = f'<a href="{esc(r["url"])}" rel="noopener">{src}</a>'
        items.append(
            f'<details class="row k{i}">'
            f'<summary><span class="yr">{r["y"]}</span>'
            f'<span class="st {cls}">{esc(lab)}</span>'
            f'<span class="tt">{esc(r["title"])}</span>'
            f'<span class="cr">{esc(r["credit"])}</span></summary>'
            f'<div class="fiche">'
            f'<p class="meta">First publication held: <strong>{esc(r["pub"])}</strong>'
            f' · known to the {esc(r["prec"] or "year")} · {esc(r["section"])}</p>'
            + (f'<p class="chips">{"".join(chips)}</p>' if chips else "")
            + (f'<p class="desc">{esc(r["note"])}</p>' if r["note"] else "")
            + f'<p class="src">{src} · checked {esc(r["checked"])} · '
            f'<a href="https://open.spotify.com/track/{r["id"]}" rel="noopener">listen</a></p>'
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
svg.chart .rec{stroke:var(--muted);stroke-width:1.6;stroke-dasharray:3 3}
svg.chart .plat{stroke:var(--accent);stroke-width:1.6;opacity:.55}
svg.chart .dot-pub{fill:var(--ink)}
svg.chart .dot-rec{fill:var(--muted)}
svg.chart .dot-spot{fill:var(--bg);stroke:var(--accent);stroke-width:1.6}
.legend .sw{width:13px;height:13px;border-radius:3px;display:inline-block;flex:none}
.legend .sw.m-ok{background:var(--ok)}
.legend .sw.m-her{background:var(--her)}
.legend .sw.m-flag{background:var(--flag)}
.legend .sw.wide{background:var(--muted)}
.legend .sw.thin{background:var(--muted);width:3px;border-radius:1px}
.legend .sw.dot-pub{background:var(--ink);border-radius:99px;width:9px;height:9px}
.legend .sw.dot-rec{background:var(--muted);border-radius:99px;width:9px;height:9px}
.legend .sw.dot-spot{background:transparent;border:2px solid var(--accent);border-radius:99px;width:10px;height:10px}
.sorter{display:flex;flex-wrap:wrap;gap:8px;margin:22px 0 12px;
 font-family:ui-sans-serif,system-ui,sans-serif;font-size:.84rem}
.sortin{position:absolute;opacity:0;pointer-events:none}
.sorter label{cursor:pointer;padding:5px 12px;border-radius:99px;
 border:1px solid var(--line);color:var(--muted);background:var(--panel)}
#s0:checked~.sorter label[for=s0],#s1:checked~.sorter label[for=s1],
#s2:checked~.sorter label[for=s2],#s3:checked~.sorter label[for=s3]{
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
           '</nav>')

    body = f"""
<header>
<h1>One hundred and forty-five songs, and when they first existed</h1>
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

<h2>How far the platform moves them</h2>
<p>One line per song whose recording or streaming date sits away from its first
publication. The scale is the same as above. <strong>{ngap}</strong> of the
{n} songs are displaced, by <strong>{total_gap}</strong> years in total, and the
displacement runs one way only: towards the present.</p>
<div class="chartwrap">{gp}</div>
{gp_leg}
<div class="note">
<p>Unlike the chart above, this one does not depend on how the playlist was
assembled. Each song is compared with itself, so each artist is her own control.
The oldest songs are moved by decades and everything after 2010 barely moves at
all.</p>
</div>

<h2>Every track</h2>
<p>Sorted four ways. Each row opens on the source that fixed its date, when that
source was last checked, and whatever doubt remains. The badge sits beside the
year because it qualifies the year, not the artist.</p>
{table}

<footer>
<p class="colophon">Dates established between the sources listed on each row.
A date marked <em>at the latest</em> means the song existed by then and may be
older; nothing here claims to be the last word. Corrections, and requests for
removal, are welcome as an <a href="{issues}" rel="noopener">issue on the
repository</a>.</p>
<p class="colophon"><a href="{playlist}" rel="noopener">Listen to the playlist</a></p>
</footer>
"""

    full = css + CSS + _order_css(rows)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Transfem chants — by year</title>
<meta name="description" content="When each of the 145 songs first existed, and how far streaming metadata moves them.">
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
