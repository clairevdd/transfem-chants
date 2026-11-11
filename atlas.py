# -*- coding: utf-8 -*-
"""Génère les deux pages annexes : countries.html et languages.html.

Appelé par build.py, jamais seul. Comme index.html, les pages produites sont
autonomes : aucune police distante, aucun script, aucun CDN.

La carte est un aplat de couleur par pays, d'autant plus dense que la liste y
compte d'artistes. Elle est faite pour montrer le vide autant que le plein :
les pays gris ne sont pas des pays sans artistes transféminines, ce sont des
pays sans sources publiques lisibles d'ici. La page le dit.
"""
import roman
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
    "Estonia": ("EE", "Europe"),
    "France": ("FR", "Europe"),
    "Germany": ("DE", "Europe"),
    "Lithuania": ("LT", "Europe"),
    "Switzerland": ("CH", "Europe"),
    "Ghana": ("GH", "Africa"),
    "Indonesia": ("ID", "Asia"),
    "Ireland": ("IE", "Europe"),
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
    "Poland": ("PL", "Europe"),
    "Portugal": ("PT", "Europe"),
    "Puerto Rico": ("PR", "North America"),
    "Russia": ("RU", "Europe"),
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
            if (sid, title, credit) not in by_artist[key]["tracks"]:
                by_artist[key]["tracks"].append((sid, title, credit))
            by_artist[key]["names"].add(name)

    rows = []
    for key, d in by_artist.items():
        v = ART[key]
        countries = [] if v[1] == "Unknown" else [
            aliases.get(c.strip(), c.strip()) for c in v[1].split(" / ")]
        languages = [] if v[2] == "—" else [l.strip() for l in v[2].split(",")]
        rows.append({"name": key, "status": v[0], "countries": countries,
                     "languages": languages, "tracks": d["tracks"],
                     "names": d["names"]})
    rows.sort(key=lambda r: roman.sort_key(r["name"]))
    return rows


def _others(credit, header_names):
    """Les noms crédités autres que l'artiste de l'en-tête, déjà nommée juste
    au-dessus. Demande de Claire, 29 septembre 2026 : la répétition sur
    chaque ligne était redondante.

    Un alias de la même personne (un nom de groupe : Against Me!, Antony and
    the Johnsons) reste affiché tel quel, sans « with » : c'est le crédit
    sous lequel le morceau est paru, pas une invitée."""
    names = [n.strip() for n in credit.split(",")]
    header, aliases = header_names
    if header in names:
        alias = []
    else:
        alias = [n for n in names if n in aliases]
    rest = [n for n in names if n != header and n not in aliases]
    out = ", ".join(alias)
    if rest:
        out = (out + " " if out else "") + "with " + ", ".join(rest)
    return out


def _track_list(tracks, esc, header_names=("", frozenset())):
    def cr(credit):
        o = _others(credit, header_names)
        return f' <span class="cr">{roman.rom_html(o, esc)}</span>' if o else ""
    items = "".join(
        f'<li><a href="https://open.spotify.com/track/{sid}" target="_blank" rel="noopener">'
        f'{roman.rom_html(title, esc)}</a>{cr(credit)}</li>'
        for sid, title, credit in tracks)
    return f'<ul class="atlas-tracks">{items}</ul>'


def _artist_block(row, esc, slug, badge):
    label, cls = badge[row["status"]]
    return (f'<div class="atlas-artist">'
            f'<h4><a href="index.html#{slug(row["name"])}">{roman.rom_html(row["name"], esc)}</a>'
            f' <span class="st {cls}">{label}</span></h4>'
            f'{_track_list(row["tracks"], esc, (row["name"], frozenset(row["names"]) - {row["name"]}))}</div>')


def _shell(title, description, css, body, nav):
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<script>(function(){{var d=document.documentElement;try{{if(localStorage.getItem("tc-theme")==="light")d.dataset.theme="light"}}catch(e){{}}window.tcToggleTheme=function(){{var l=d.dataset.theme!=="light";if(l)d.dataset.theme="light";else delete d.dataset.theme;try{{localStorage.setItem("tc-theme",l?"light":"dark")}}catch(e){{}}document.dispatchEvent(new Event("tc-themechange"))}}}})()</script>
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


# Bouton de choix du thème (sombre par défaut, clair au choix), ajouté le
# 9 novembre 2026 à la demande de Claire. Le script qui le fait marcher est
# dans l'en-tête de chaque page.
THEME_BUTTON = ('<button type="button" class="themebtn" onclick="tcToggleTheme()" aria-label="Switch between dark and light theme"><span class="to-light">Light theme</span><span class="to-dark">Dark theme</span></button>')


# Recherche (artistes et titres), ajoutée le 10 novembre 2026 à la demande de
# Claire : une loupe dans la barre de navigation ouvre un champ. L'index
# (search-index.json) est généré par build.py et chargé seulement à
# l'ouverture. Tout se passe dans le navigateur, sans service extérieur. Sans
# JavaScript, la loupe reste masquée.
SEARCH_UI = (
    '<button type="button" class="searchbtn" id="tcs-btn" hidden aria-label="Search artists and songs" aria-expanded="false" aria-controls="tcs-panel">'
    '<svg viewBox="0 0 20 20" width="15" height="15" aria-hidden="true"><circle cx="8.5" cy="8.5" r="5.5" fill="none" stroke="currentColor" stroke-width="2"/><path d="M13 13l4.5 4.5" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>'
    '</button>'
    '<div class="searchpanel" id="tcs-panel" hidden>'
    '<input type="search" id="tcs-in" placeholder="Search an artist or a song" autocomplete="off" spellcheck="false" aria-label="Search an artist or a song">'
    '<ul id="tcs-out" class="searchout"></ul>'
    '</div>'
    '<script>(function(){var b=document.getElementById("tcs-btn"),p=document.getElementById("tcs-panel"),'
    'i=document.getElementById("tcs-in"),o=document.getElementById("tcs-out"),D=null,L=null;b.hidden=false;'
    'function n(s){return s.normalize("NFD").replace(/[\\u0300-\\u036f]/g,"").toLowerCase()'
    '.replace(/\\u0153/g,"oe").replace(/\\u00e6/g,"ae").replace(/\\u00df/g,"ss").replace(/[\x27\\u2019]/g,"").replace(/[^\\p{L}\\p{N}]+/gu," ").trim()}'
    'function e(s){return s.replace(/[&<>"]/g,function(c){return{"&":"&amp;","<":"&lt;",">":"&gt;","\\"":"&quot;"}[c]})}'
    'function ld(){if(!L)L=fetch("search-index.json").then(function(r){return r.json()}).then(function(j){'
    'j.forEach(function(x){x.k=n(x.r||x.t);x.q=" "+n(x.t+" "+(x.r||"")+" "+(x.s||""))});D=j;return j});return L}'
    'function run(){var q=n(i.value.trim());if(!q){o.innerHTML="";return}ld().then(function(d){'
    'var w=q.split(" "),r=d.filter(function(x){return w.every(function(v){return x.q.indexOf(" "+v)>=0})});'
    'r.sort(function(a,c){var sa=a.k.indexOf(q)===0?0:1,sc=c.k.indexOf(q)===0?0:1;'
    'return sa-sc||(a.c==="artist"?0:1)-(c.c==="artist"?0:1)||a.k.localeCompare(c.k)});'
    'o.innerHTML=r.length?r.slice(0,30).map(function(x){return\'<li><a href="\'+x.h+\'"><span class="sk">\'+x.c+\'</span>\'+e(x.t)'
    '+(x.r?\' <span class="sr">\'+e(x.r)+"</span>":"")+(x.s?\'<span class="ss">\'+e(x.s)+"</span>":"")+"</a></li>"}).join("")+(r.length>30?\'<li class="more">\'+(r.length-30)+" more, keep typing</li>":"")'
    ':\'<li class="more">Nothing found</li>\'})}'
    'function sh(v){p.hidden=!v;b.setAttribute("aria-expanded",v?"true":"false");if(v){ld();i.focus()}}'
    'b.addEventListener("click",function(){sh(p.hidden)});i.addEventListener("input",run);'
    'i.addEventListener("keydown",function(k){if(k.key==="Escape"){sh(false);b.focus()}'
    'else if(k.key==="Enter"){var f=o.querySelector("a");if(f){k.preventDefault();f.click()}}});'
    'o.addEventListener("click",function(k){if(k.target.closest("a"))sh(false)})})()</script>'
)


# Barre de navigation collée en haut au défilement, avec le nom du site
# (10 novembre 2026, à la demande de Claire). Sur écran étroit, les onglets
# passent derrière un bouton « Menu » (choix de Claire) ; sans JavaScript, ils
# restent affichés en clair et la barre n'est pas collée.
MENU_SCRIPT = (
    '<script>(function(){var n=document.getElementById("tc-nav"),b=document.getElementById("tc-menu"),'
    'l=document.getElementById("tc-links");n.classList.add("js");b.hidden=false;'
    'function s(v){n.classList.toggle("open",v);b.setAttribute("aria-expanded",v?"true":"false")}'
    'var sb=document.getElementById("tcs-btn"),sp=document.getElementById("tcs-panel");'
    # Menu et recherche ne s'ouvrent jamais ensemble : ouvrir l'un ferme l'autre.
    'if(sb)sb.addEventListener("click",function(){s(false)});'
    'b.addEventListener("click",function(e){e.stopPropagation();var v=!n.classList.contains("open");'
    'if(v&&sp&&!sp.hidden){sp.hidden=true;sb.setAttribute("aria-expanded","false")}s(v)});'
    'l.addEventListener("click",function(e){if(e.target.closest("a"))s(false)});'
    'document.addEventListener("click",function(e){if(!n.contains(e.target))s(false)});'
    'document.addEventListener("keydown",function(e){if(e.key==="Escape"&&n.classList.contains("open")){s(false);b.focus()}});'
    # Arrivée sur une ancre depuis une autre page : saut immédiat, pas de
    # défilement animé sur des pages de plusieurs dizaines de milliers de
    # pixels (il s'interrompait sur Android). La page « by year » a son propre
    # saut, qui ouvre la fiche.
    'if(location.hash){var t=0;addEventListener("touchstart",function(){t=1},{passive:true});addEventListener("wheel",function(){t=1},{passive:true});'
    'var j=function(){if(t)return;var e=document.getElementById(decodeURIComponent(location.hash.slice(1)));'
    'if(e&&e.tagName!=="DETAILS")e.scrollIntoView({behavior:"instant"})};'
    'document.addEventListener("DOMContentLoaded",j);addEventListener("load",function(){setTimeout(j,50)});[300,900].forEach(function(d){setTimeout(j,d)})}'
    '})()</script>'
)


# Formulaire de suggestion d'artistes (Tally), arbitrage de Claire du
# 11 novembre 2026 : il remplace les issues GitHub pour les nouvelles
# artistes ; les issues restent pour les dates et les sources, le formulaire
# de retrait pour tout ce qui touche l'identité. Contrôlé par build.py.
SUGGEST = "https://tally.so/r/xVMa9o"

# Formulaire privé de modification et de retrait (Tally). Il remplace la
# page Removals, supprimée le 11 novembre 2026 à la demande de Claire : un
# clic sur « Removals » mène directement au formulaire. Contrôlé par build.py.
# Jamais d'adresse e-mail ici : la destination se règle chez Tally.
CONTACT = "https://tally.so/r/2EWdyg"


def _nav(here):
    def link(href, label):
        if href == here:
            return f'<span class="here">{label}</span>'
        return f'<a href="{href}">{label}</a>'
    return ('<nav class="pagenav" id="tc-nav">'
            + '<a class="brand" href="index.html">Transfem Tracks</a>'
            + '<button type="button" class="menubtn" id="tc-menu" hidden aria-expanded="false" aria-controls="tc-links">'
            + '<svg viewBox="0 0 20 20" width="15" height="15" aria-hidden="true"><path d="M3 5h14M3 10h14M3 15h14" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>'
            + '<span>Menu</span></button>'
            + '<span class="navlinks" id="tc-links">'
            + link("index.html", "Sources")
            + link("countries.html", "By country")
            + link("languages.html", "By language")
            + link("years.html", "By year")
            + link("tags.html", "By tags")
            + link("sonic.html", "By sonic profile")
            + f'<a href="{SUGGEST}" target="_blank" rel="noopener">Suggest</a>'
            + f'<a href="{CONTACT}" target="_blank" rel="noopener">Removals</a>'
            + '</span>'
            + '<span class="navtools">' + SEARCH_UI + THEME_BUTTON + '</span>'
            + '</nav>' + MENU_SCRIPT)


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
<p>Companion page to the Spotify playlist <a href="{playlist}" target="_blank" rel="noopener"><strong>Transfem Tracks</strong></a>. Every statement of identity, with its source, is on the <a href="index.html">sources page</a>.</p>
<p class="colophon">Country boundaries derived from the public-domain world map shipped with pygal_maps_world, simplified for weight. Borders shown are those of that dataset and are not a position on any of them.</p>
<p class="colophon">To have an entry taken down, or to raise anything about a person’s identity, use the <a href="{CONTACT}" target="_blank" rel="noopener">private channel</a> rather than a public issue thread.</p>
<p class="colophon"><a href="index.html#legal">Legal notice and privacy</a></p>
</footer>
"""
    return _shell("Transfem Tracks — by country",
                  "The Transfem Tracks playlist mapped by country, and what the "
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
<p>Companion page to the Spotify playlist <a href="{playlist}" target="_blank" rel="noopener"><strong>Transfem Tracks</strong></a>. Every statement of identity, with its source, is on the <a href="index.html">sources page</a>.</p>
<p class="colophon">A missing language is a missing source, not a missing artist. If you know of one, <a href="{SUGGEST}" target="_blank" rel="noopener">suggest her</a> through the form. To have an entry taken down, or to raise anything about a person’s identity, use the <a href="{CONTACT}" target="_blank" rel="noopener">private channel</a> instead: issue threads are public.</p>
<p class="colophon"><a href="index.html#legal">Legal notice and privacy</a></p>
</footer>
"""
    return _shell("Transfem Tracks — by language",
                  "The Transfem Tracks playlist broken down by the languages its "
                  "artists record in, and why the distribution is so uneven.",
                  css, body, _nav("languages.html"))


def legal_html():
    """Mentions légales et confidentialité, en bas de l'accueil (ancre #legal).

    Vivaient sur la page Removals ; déplacées sur l'accueil le 11 novembre
    2026, quand cette page a été remplacée par le formulaire Tally, la loi
    demandant qu'elles figurent sur le site lui-même.
    """
    return f"""
<h2 id="legal">Legal notice and privacy</h2>
<div class="note">
<p><strong>Publisher and host.</strong> This site is published on a personal, non-commercial basis by the person who compiled the playlist. As French law allows for non-professional publishers (LCEN, article 1-1, II), her identity has been given to the host rather than shown here. The site is hosted on GitHub Pages by GitHub, Inc., 88 Colin P Kelly Jr St, San Francisco, CA 94107, United States.</p>
<p><strong>About the artists.</strong> These pages publish information about real people: the name each artist records under, the gender identity she has stated in public, and where she said it. Only what an artist has made public herself is used here (GDPR, article 9(2)(e)), and only to document the playlist. The publisher is responsible for this use. Anyone concerned can have an entry changed or removed through the <a href="{CONTACT}" target="_blank" rel="noopener">private form for changes and removals</a>, which is also the way to exercise any other right under the GDPR. You can also lodge a complaint with the French data protection authority, the <a href="https://www.cnil.fr/fr/plaintes" target="_blank" rel="noopener">CNIL</a>.</p>
<p><strong>About visitors.</strong> No cookies, no analytics, no tracking. Your choice of light or dark theme is stored in your own browser and never leaves it. As host, GitHub receives the technical data of any web request, such as your IP address (<a href="https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement" target="_blank" rel="noopener">GitHub's privacy statement</a>). The sonic profile page loads its 3D library from the jsDelivr network, which receives your IP address in the same way (<a href="https://www.jsdelivr.com/terms" target="_blank" rel="noopener">jsDelivr's terms</a>). The two forms, for changes and removals and for suggesting an artist, are hosted by Tally, which receives the technical data of anyone who opens them, such as the IP address, as well as what is sent through them (<a href="https://tally.so/help/privacy-policy" target="_blank" rel="noopener">Tally's privacy notice</a>). What you send is read only to handle your request, and deleted once it has been dealt with.</p>
</div>
"""
