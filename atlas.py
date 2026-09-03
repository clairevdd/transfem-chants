# -*- coding: utf-8 -*-
"""Génère les deux pages annexes : countries.html et languages.html.

Appelé par build.py, jamais seul. Comme index.html, les pages produites sont
autonomes : aucune police distante, aucun script, aucun CDN.

La carte est un aplat de couleur par pays, d'autant plus dense que la liste y
compte d'artistes. Elle est faite pour montrer le vide autant que le plein :
les pays gris ne sont pas des pays sans artistes transféminines, ce sont des
pays sans sources publiques lisibles d'ici. La page le dit.
"""
from data import ART
from tracks import all_tracks
from worldmap import SHAPES, VIEWBOX

# Code ISO et continent pour chaque pays employé dans data.py.
# Le build échoue si un pays n'y figure pas, pour qu'aucun n'apparaisse
# silencieusement hors carte.
COUNTRIES = {
    "Angola": ("AO", "Africa"),
    "Argentina": ("AR", "South America"),
    "Australia": ("AU", "Oceania"),
    "Brazil": ("BR", "South America"),
    "Canada": ("CA", "North America"),
    "Chile": ("CL", "South America"),
    "France": ("FR", "Europe"),
    "Germany": ("DE", "Europe"),
    "Ghana": ("GH", "Africa"),
    "Indonesia": ("ID", "Asia"),
    "Israel": ("IL", "Asia"),
    "Japan": ("JP", "Asia"),
    "Lebanon": ("LB", "Asia"),
    "Malaysia": ("MY", "Asia"),
    "Mexico": ("MX", "North America"),
    "Morocco": ("MA", "Africa"),
    "Netherlands": ("NL", "Europe"),
    "Pakistan": ("PK", "Asia"),
    "Peru": ("PE", "South America"),
    "Philippines": ("PH", "Asia"),
    "Portugal": ("PT", "Europe"),
    "Puerto Rico": ("PR", "North America"),
    "Serbia": ("RS", "Europe"),
    "South Africa": ("ZA", "Africa"),
    "South Korea": ("KR", "Asia"),
    "Spain": ("ES", "Europe"),
    "Sweden": ("SE", "Europe"),
    "Thailand": ("TH", "Asia"),
    "Türkiye": ("TR", "Asia"),
    "UK": ("GB", "Europe"),
    "United States": ("US", "North America"),
    "Venezuela": ("VE", "South America"),
    "Vietnam": ("VN", "Asia"),
    "Zambia": ("ZM", "Africa"),
}

CONTINENT_ORDER = ["Africa", "Asia", "Europe", "North America",
                   "South America", "Oceania"]


def _index(esc, slug, artists_of, aliases, same_person):
    """Construit l'index artiste -> pays, langues, morceaux.

    Les invitées sont exclues : le critère d'inclusion ne leur applique pas, et
    les compter fausserait la carte. Les alias de personne (ANOHNI et Antony,
    Venus De Mars et son groupe) sont fusionnés pour ne pas compter deux fois
    la même artiste.
    """
    by_artist = {}
    for sid, title, credit in all_tracks():
        for name in artists_of(credit):
            if ART[name][0] == "guest":
                continue
            key = same_person.get(name, name)
            by_artist.setdefault(key, {"tracks": [], "names": set()})
            by_artist[key]["tracks"].append((sid, title, credit))
            by_artist[key]["names"].add(name)

    rows = []
    for key, d in by_artist.items():
        v = ART[key]
        countries = [] if v[1] == "Unknown" else [
            aliases.get(c.strip(), c.strip()) for c in v[1].split(" / ")]
        languages = [] if v[2] == "—" else [l.strip() for l in v[2].split(",")]
        rows.append({"name": key, "status": v[0], "countries": countries,
                     "languages": languages, "tracks": d["tracks"]})
    rows.sort(key=lambda r: r["name"].lower())
    return rows


def _track_list(tracks, esc):
    items = "".join(
        f'<li><a href="https://open.spotify.com/track/{sid}" rel="noopener">'
        f'{esc(title)}</a> <span class="cr">{esc(credit)}</span></li>'
        for sid, title, credit in tracks)
    return f'<ul class="atlas-tracks">{items}</ul>'


def _artist_block(row, esc, slug, badge):
    label, cls = badge[row["status"]]
    return (f'<div class="atlas-artist">'
            f'<h4><a href="index.html#{slug(row["name"])}">{esc(row["name"])}</a>'
            f' <span class="st {cls}">{label}</span></h4>'
            f'{_track_list(row["tracks"], esc)}</div>')


def _shell(title, description, css, body, nav):
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<style>{css}</style>
</head>
<body>
<div class="wrap">
{nav}
{body}
</div>
</body>
</html>
"""


def _nav(here):
    def link(href, label):
        if href == here:
            return f'<span class="here">{label}</span>'
        return f'<a href="{href}">{label}</a>'
    return ('<nav class="pagenav">'
            + link("index.html", "Sources")
            + link("countries.html", "By country")
            + link("languages.html", "By language")
            + '</nav>')


# Paliers fixes plutôt que relatifs au maximum : les effectifs sont petits, et
# une légende qui dit « 1 », « 2 », « 3 à 5 » se lit sans avoir à deviner un
# seuil calculé. BUCKETS donne, pour chaque palier, sa borne haute et son
# libellé ; le dernier palier n'a pas de borne.
BUCKETS = [(1, "1"), (2, "2"), (5, "3–5"), (10, "6–10"), (None, "11 and up")]


def _scale(n):
    if n <= 0:
        return 0
    for i, (hi, _) in enumerate(BUCKETS, start=1):
        if hi is None or n <= hi:
            return i
    return len(BUCKETS)


def countries_page(css, esc, slug, artists_of, aliases, same_person, badge,
                   playlist, issues):
    rows = _index(esc, slug, artists_of, aliases, same_person)

    counts, tracks_by_country = {}, {}
    for r in rows:
        for c in r["countries"]:
            counts[c] = counts.get(c, 0) + 1
            tracks_by_country[c] = tracks_by_country.get(c, 0) + len(r["tracks"])
    unknown = [r for r in rows if not r["countries"]]

    missing = sorted(set(counts) - set(COUNTRIES))
    if missing:
        raise SystemExit(f"atlas.py : pays sans code ISO : {missing}")

    top_country = max(counts, key=lambda c: counts[c]) if counts else None
    by_code = {COUNTRIES[c][0]: c for c in counts}

    shapes = []
    for code, d in sorted(SHAPES.items()):
        if code == "AQ":
            continue
        name = by_code.get(code)
        if name:
            lvl = _scale(counts[name])
            n, t = counts[name], tracks_by_country[name]
            label = (f'{name}: {n} artist{"s" if n > 1 else ""}, '
                     f'{t} track{"s" if t > 1 else ""}')
            shapes.append(
                f'<a href="#c-{code}" class="mc l{lvl}">'
                f'<title>{esc(label)}</title>'
                f'<path d="{d}"/></a>')
        else:
            shapes.append(f'<path class="mc l0" d="{d}"/>')

    legend = "".join(
        f'<span class="key"><i class="l{i}"></i>{lab}</span>'
        for i, lab in [(0, "none")] + [(i, lab) for i, (_, lab)
                                       in enumerate(BUCKETS, start=1)])

    blocks = []
    for cont in CONTINENT_ORDER:
        names = sorted(c for c in counts if COUNTRIES[c][1] == cont)
        if not names:
            continue
        n_art = sum(counts[c] for c in names)
        blocks.append(f'<h3 class="cont">{cont} '
                      f'<span class="cnt">{n_art}</span></h3>')
        for c in names:
            code = COUNTRIES[c][0]
            here = [r for r in rows if c in r["countries"]]
            blocks.append(
                f'<section class="atlas-group" id="c-{code}">'
                f'<h4 class="ctry">{esc(c)} '
                f'<span class="cnt">{counts[c]}</span></h4>'
                + "".join(_artist_block(r, esc, slug, badge) for r in here)
                + '</section>')

    if unknown:
        blocks.append('<h3 class="cont">Not stated</h3>')
        blocks.append('<section class="atlas-group">'
                      + "".join(_artist_block(r, esc, slug, badge)
                                for r in unknown)
                      + '</section>')

    share = f"{esc(top_country)} alone accounts for {counts[top_country]} of the {len(rows)} artists here." if top_country else ""

    body = f"""
<header>
<h1>By country</h1>
<p class="sub">Where the artists on this playlist are from, and what that map leaves out.</p>
<p class="stats"><strong>{len(counts)}</strong> countries and territories &middot; <strong>{len(rows)}</strong> artists &middot; <strong>{len(all_tracks())}</strong> tracks</p>
</header>

<figure class="mapfig">
<svg viewBox="0 0 2477 1170" role="img" aria-label="World map shaded by the number of artists from each country" class="worldmap">
{''.join(shapes)}
</svg>
<figcaption>
<div class="legend">{legend}</div>
<p>Shading counts artists, not tracks. Click a country to jump to it.</p>
</figcaption>
</figure>

<div class="note">
<h4>What the grey means</h4>
<p>A grey country is not a country without transfeminine musicians. It is a country from which no usable public statement reached this page. The two are easy to confuse and the difference is the whole point of the map.</p>
<p>Three things shape it before the music does. A public declaration has to exist, which takes a press willing to publish one. It has to be findable in a language the compiler can read. And in a number of these countries, making that declaration carries a real risk, so the reasonable choice is not to make it. The map is a map of publishing and safety at least as much as of music.</p>
<p>Read the density with the same caution. {share} That is a fact about where music journalism is published, not about where transfeminine artists live.</p>
</div>

<h2>The artists, by continent</h2>
<p>Artists with more than one country are listed under each. Guest credits are not counted here, since the inclusion criteria do not apply to them.</p>
{''.join(blocks)}

<footer>
<p>Companion page to the Spotify playlist <a href="{playlist}" rel="noopener"><strong>Transfem chants</strong></a>. Every statement of identity, with its source, is on the <a href="index.html">sources page</a>.</p>
<p class="colophon">Country boundaries derived from the public-domain world map shipped with pygal_maps_world, simplified for weight. Borders shown are those of that dataset and are not a position on any of them.</p>
</footer>
"""
    return _shell("Transfem chants — by country",
                  "The Transfem chants playlist mapped by country, and what the "
                  "empty parts of that map actually record.",
                  css, body, _nav("countries.html"))


def languages_page(css, esc, slug, artists_of, aliases, same_person, badge,
                   playlist, issues):
    rows = _index(esc, slug, artists_of, aliases, same_person)

    counts, tracks_by_lang = {}, {}
    for r in rows:
        for l in r["languages"]:
            counts[l] = counts.get(l, 0) + 1
            tracks_by_lang[l] = tracks_by_lang.get(l, 0) + len(r["tracks"])

    order = sorted(counts, key=lambda l: (-counts[l], l.lower()))
    top = max(counts.values()) if counts else 1

    bars = "".join(
        f'<a class="bar" href="#l-{slug(l)}">'
        f'<span class="bl">{esc(l)}</span>'
        f'<span class="bt"><span class="bf" style="width:{max(2, round(100 * counts[l] / top))}%"></span></span>'
        f'<span class="bn">{counts[l]}</span></a>'
        for l in order)

    blocks = []
    for l in order:
        here = [r for r in rows if l in r["languages"]]
        blocks.append(
            f'<section class="atlas-group" id="l-{slug(l)}">'
            f'<h4 class="ctry">{esc(l)} '
            f'<span class="cnt">{counts[l]}</span></h4>'
            + "".join(_artist_block(r, esc, slug, badge) for r in here)
            + '</section>')

    body = f"""
<header>
<h1>By language</h1>
<p class="sub">Which languages the artists on this playlist record in, and how unevenly.</p>
<p class="stats"><strong>{len(counts)}</strong> languages &middot; <strong>{len(rows)}</strong> artists &middot; <strong>{len(all_tracks())}</strong> tracks</p>
</header>

<figure class="mapfig">
<div class="bars">{bars}</div>
<figcaption><p>Artists per language. An artist recording in two languages is counted in both.</p></figcaption>
</figure>

<div class="note">
<h4>How to read this</h4>
<p>The languages here are the ones an artist records in, taken from her own catalogue, not the language of the particular song on the playlist. Where an artist speaks about herself in one language and sings in another, this page follows what she sings. So a language appearing here does not guarantee a song in that language on the playlist.</p>
<p>The shape of this chart is not a fact about music. English runs away with it because the English-language press publishes the interviews that the third inclusion criterion requires, so an artist who sings in English is far likelier to have a statement this page can cite. Every other language on the list had to clear a higher bar to get here at all.</p>
</div>

<h2>The artists, by language</h2>
<p>Most spoken first. Guest credits are not counted here, since the inclusion criteria do not apply to them.</p>
{''.join(blocks)}

<footer>
<p>Companion page to the Spotify playlist <a href="{playlist}" rel="noopener"><strong>Transfem chants</strong></a>. Every statement of identity, with its source, is on the <a href="index.html">sources page</a>.</p>
<p class="colophon">A missing language is a missing source, not a missing artist. If you know of one, <a href="{issues}" rel="noopener">open an issue</a>.</p>
</footer>
"""
    return _shell("Transfem chants — by language",
                  "The Transfem chants playlist broken down by the languages its "
                  "artists record in, and why the distribution is so uneven.",
                  css, body, _nav("languages.html"))
