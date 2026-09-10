# -*- coding: utf-8 -*-
"""Génère tags.html, la page de tags de genre/style/scène.

Appelée par build.py, jamais seule. Seule page du dépôt qui embarque un script :
toutes les autres suivent le principe "aucune police distante, aucun script,
aucun CDN" affiché dans le README, mais un filtre combinant librement N tags
parmi plusieurs centaines ne se laisse pas écrire en pur CSS comme le tri de
`years.html`, qui ne gère que deux ou trois alternatives figées. Arbitrage de
Claire, 10 septembre 2026 : un petit script autonome, sans dépendance ni appel
réseau, uniquement sur cette page. La page reste utilisable sans script : la
liste complète des morceaux est déjà dans le HTML au chargement, groupée par
artiste, chaque tag sourcé ; le script prend le relais au chargement pour la
rendre interactive.

Deux modes de combinaison, choisis par Claire le 10 septembre 2026 :

- **intersection** (par défaut) : les morceaux qui portent TOUS les tags
  choisis. Sans aucun tag choisi, rien n'est filtré : les 146 morceaux
  s'affichent. Choisir un tag de plus resserre toujours la liste, jamais
  l'inverse.
- **union** : les morceaux qui portent AU MOINS UN des tags choisis. Sans
  aucun tag choisi, la liste est vide : l'union de rien est rien. Choisir un
  tag l'agrandit toujours, jamais l'inverse.

En mode intersection seulement, un mécanisme de resserrement dynamique :
chaque tag encore cliquable affiche, non plus son volume sur toute la
playlist, mais son volume **parmi les morceaux qui satisfont déjà la
sélection en cours** ; un tag qui tomberait à zéro dans ces conditions
disparaît plutôt que de rester affiché à zéro, et un tag qui n'était pas
assez fréquent pour figurer dans le nuage peut y entrer si son volume relatif,
recalculé, l'y qualifie désormais. Rien de tel en mode union, où le nuage
reste construit sur les volumes globaux : la mécanique demandée par Claire
n'a de sens que pour un resserrement, pas pour un cumul.

Deux zones de tags : un nuage pour les tags dominants (jusqu'à 30), classés
par ordre alphabétique mais dont la taille suit le volume, plutôt qu'une
disposition resserrée avec les plus gros au centre — celle-ci demanderait un
algorithme de tassement, se comporterait mal en responsive et serait peu
accessible aux lecteurs d'écran. Le reste va dans une liste alphabétique à
taille fixe, repliée par défaut : elle occupait trop de place ouverte
d'emblée pour un usage qui reste occasionnel.

`unclassified`, le tag synthétique des morceaux sans source, reste toujours
présent dans le nuage tant que son compteur n'est pas nul, quel que soit son
rang : c'est l'absence de source elle-même qui est l'information, et elle ne
doit pas pouvoir se retrouver reléguée dans la liste repliée simply parce
qu'une future augmentation de la playlist l'y ferait descendre. Cette
garantie ne vaut que pour le nuage de départ (aucun tag choisi, ou mode
union) : une fois un premier tag choisi en mode intersection, `unclassified`
suit la même règle que n'importe quel autre tag et disparaît si son compteur
recalculé tombe à zéro, ce qui est presque toujours le cas puisqu'un morceau
`unclassified` ne porte par définition aucun autre tag.

Chaque tag affiché sous un morceau porte sa source : une ligne par source
parmi Discogs, MusicBrainz et Last.fm qui en a fourni au moins un pour ce
morceau, jamais plus de trois lignes. Les doublons entre sources ne sont pas
supprimés à cet endroit : Claire les a acceptés pour garder la ligne lisible
et fidèle à ce que chaque source a effectivement renvoyé.

Trois filtres retirent des tags avant qu'ils n'atteignent cette page :
identité, géographie et bruit. Le détail et les arbitrages sont dans
`tags.py`, pas ici.
"""
import json
from collections import Counter

from data import ART
from tracks import all_tracks
from tags import TAGS

import atlas

# Tags dominants affichés en nuage ; le reste va dans la liste alphabétique
# repliée. Doit rester identique à DOMINANT_N dans le script embarqué plus bas.
DOMINANT_N = 30

SOURCE_LABELS = [("discogs", "Discogs"), ("musicbrainz", "MusicBrainz"), ("lastfm", "Last.fm")]


def _primary(credit, artists_of):
    """Le premier nom crédité qui n'est pas une invitée, pour grouper les
    résultats par artiste. Une invitée en tête de crédit (un producteur, par
    exemple) ne doit pas devenir la clé de regroupement : même règle que sur
    les pages pays et langue, qui l'excluent déjà de leur propre index."""
    names = artists_of(credit)
    leads = [n for n in names if ART[n][0] != "guest"]
    return leads[0] if leads else names[0]


def _records(artists_of):
    out = []
    for sid, title, credit in all_tracks():
        entry = TAGS.get(sid) or {"discogs": [], "musicbrainz": [], "lastfm": []}
        union = []
        for key, _ in SOURCE_LABELS:
            for t in entry.get(key) or []:
                if t not in union:
                    union.append(t)
        out.append({
            "id": sid, "title": title, "credit": credit,
            "sources": entry, "tags": union if union else ["unclassified"],
            "primary": _primary(credit, artists_of),
        })
    return out


def _freq(records):
    c = Counter()
    for r in records:
        c.update(r["tags"])
    return c


def _split_dominant(freq):
    """Les tags dominants (jusqu'à DOMINANT_N), `unclassified` toujours parmi
    eux tant que son compteur n'est pas nul ; le reste, alphabétique."""
    force = "unclassified" if freq.get("unclassified", 0) > 0 else None
    rest = [(t, n) for t, n in freq.items() if t != force]
    rest.sort(key=lambda kv: (-kv[1], kv[0]))
    dom_n = DOMINANT_N - 1 if force else DOMINANT_N
    dominant = [t for t, _ in rest[:dom_n]]
    if force:
        dominant.append(force)
    dominant_set = set(dominant)
    tail = sorted(t for t in freq if t not in dominant_set)
    return sorted(dominant), tail


def _size_rem(n, lo, hi):
    if hi <= lo:
        return 1.0
    t = (n ** 0.5 - lo ** 0.5) / (hi ** 0.5 - lo ** 0.5)
    return round(0.85 + t * (2.15 - 0.85), 2)


def _chip(tag, count, esc, size=None, extra=""):
    style = f' style="font-size:{size}rem"' if size else ""
    cls = "tag" + (f" {extra}" if extra else "")
    return (f'<button type="button" class="{cls}" data-tag="{esc(tag)}"'
            f' aria-pressed="false"{style}>{esc(tag)} '
            f'<span class="cnt">{count}</span></button>')


def _cloud_html(freq, esc):
    dominant, tail = _split_dominant(freq)
    counts = [freq[t] for t in dominant]
    lo, hi = (min(counts), max(counts)) if counts else (0, 0)
    cloud = "".join(
        _chip(t, freq[t], esc, size=_size_rem(freq[t], lo, hi),
              extra="tag-unclassified" if t == "unclassified" else "")
        for t in dominant)
    tail_html = "".join(
        _chip(t, freq[t], esc, extra="tag-tail" + (" tag-unclassified" if t == "unclassified" else ""))
        for t in tail)
    return cloud, tail_html, len(dominant), len(tail)


def _track_line(r, esc, slug):
    url = "https://open.spotify.com/track/" + r["id"]
    names = [n.strip() for n in r["credit"].split(",")]
    cr = " · ".join(
        f'<a class="{"guest" if ART[n][0] == "guest" else "lead"}" '
        f'href="index.html#{slug(n)}">{esc(n)}</a>' for n in names)
    tags_json = esc(json.dumps(r["tags"]))
    src_lines = "".join(
        f'<div class="srcline"><b>{label}</b> {esc(", ".join(r["sources"].get(key) or []))}</div>'
        for key, label in SOURCE_LABELS if r["sources"].get(key))
    if not src_lines:
        src_lines = '<div class="srcline none">No source tag found (unclassified)</div>'
    return (f'<li data-tags="{tags_json}">'
            f'<a href="{esc(url)}" target="_blank" rel="noopener">{esc(r["title"])}</a> '
            f'<span class="cr">{cr}</span>'
            f'{src_lines}</li>')


def _results_html(records, esc, slug):
    by_artist = {}
    for r in records:
        by_artist.setdefault(r["primary"], []).append(r)
    blocks = []
    for name in sorted(by_artist, key=str.lower):
        rows = by_artist[name]
        blocks.append(
            f'<section class="atlas-group" data-artist="{esc(name)}">'
            f'<h4 class="ctry"><a href="index.html#{slug(name)}">{esc(name)}</a> '
            f'<span class="cnt">{len(rows)}</span></h4>'
            f'<ul class="atlas-tracks">'
            + "".join(_track_line(r, esc, slug) for r in rows)
            + '</ul></section>')
    return "".join(blocks)


# Le moteur d'interactivité. Lit `data-tags` sur chaque <li> une fois au
# chargement (pas de blob JSON séparé : le DOM déjà rendu est la seule source
# de données), puis recalcule tout à chaque clic plutôt que de maintenir un
# état complexe : à cette échelle (146 morceaux, quelques centaines de tags),
# tout recalculer est instantané et bien plus sûr qu'une mise à jour partielle.
SCRIPT = """
<script>
(function () {
  var DOMINANT_N = 30; // doit rester identique à DOMINANT_N dans tagcloud.py

  var items = Array.prototype.slice.call(document.querySelectorAll('#tagres li[data-tags]')).map(function (li) {
    return { li: li, group: li.closest('.atlas-group'), tags: JSON.parse(li.getAttribute('data-tags')) };
  });
  var groups = Array.prototype.slice.call(document.querySelectorAll('#tagres .atlas-group'));

  var globalCounts = new Map();
  items.forEach(function (it) {
    it.tags.forEach(function (t) { globalCounts.set(t, (globalCounts.get(t) || 0) + 1); });
  });

  var cloudEl = document.getElementById('tagcloud');
  var tailEl = document.getElementById('tagtail');
  var tailWrap = document.getElementById('tagtail-wrap');
  var tailBtn = document.getElementById('tagtail-toggle');
  var activeEl = document.getElementById('tagactive');
  var countEl = document.getElementById('tagres-count');
  var clearBtn = document.getElementById('tagres-clear');
  var modeInter = document.getElementById('mode-inter');
  var modeUnion = document.getElementById('mode-union');

  var selected = [];          // ordre de sélection, préservé pour l'affichage
  var tailOpen = false;

  function mode() { return modeUnion.checked ? 'union' : 'inter'; }

  function matches(tags) {
    var sel = selected;
    if (mode() === 'union') {
      if (sel.length === 0) return false;
      return sel.some(function (t) { return tags.indexOf(t) !== -1; });
    }
    if (sel.length === 0) return true;
    return sel.every(function (t) { return tags.indexOf(t) !== -1; });
  }

  function splitDominant(counts, forceUnclassified) {
    var entries = [];
    counts.forEach(function (n, t) { if (n > 0) entries.push([t, n]); });
    var force = (forceUnclassified && counts.get('unclassified') > 0) ? 'unclassified' : null;
    var rest = entries.filter(function (e) { return e[0] !== force; });
    rest.sort(function (a, b) { return b[1] - a[1] || a[0].localeCompare(b[0]); });
    var domN = force ? DOMINANT_N - 1 : DOMINANT_N;
    var dominant = rest.slice(0, domN).map(function (e) { return e[0]; });
    if (force) dominant.push(force);
    var domSet = {};
    dominant.forEach(function (t) { domSet[t] = true; });
    var tail = entries.filter(function (e) { return !domSet[e[0]]; }).map(function (e) { return e[0]; });
    dominant.sort();
    tail.sort();
    return { dominant: dominant, tail: tail };
  }

  function chip(tag, count, size, extra) {
    var btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'tag' + (extra ? ' ' + extra : '');
    btn.setAttribute('data-tag', tag);
    btn.setAttribute('aria-pressed', 'false');
    if (size) btn.style.fontSize = size + 'rem';
    var span = document.createElement('span');
    span.className = 'cnt';
    span.textContent = count;
    btn.appendChild(document.createTextNode(tag + ' '));
    btn.appendChild(span);
    return btn;
  }

  function sizeRem(n, lo, hi) {
    if (hi <= lo) return null;
    var t = (Math.sqrt(n) - Math.sqrt(lo)) / (Math.sqrt(hi) - Math.sqrt(lo));
    return (0.85 + t * (2.15 - 0.85)).toFixed(2);
  }

  function render() {
    var m = mode();
    var matched = items.filter(function (it) { return matches(it.tags); });
    var matchedSet = new Set();
    matched.forEach(function (it) { matchedSet.add(it); });

    items.forEach(function (it) { it.li.hidden = !matchedSet.has(it); });
    groups.forEach(function (g) {
      g.hidden = g.querySelectorAll('li:not([hidden])').length === 0;
    });

    if (m === 'union' && selected.length === 0) {
      countEl.textContent = '0 of ' + items.length + ' tracks shown — pick a tag to begin';
    } else {
      countEl.textContent = matched.length + ' of ' + items.length + ' tracks shown';
    }
    clearBtn.hidden = selected.length === 0;

    // Active filters, always shown regardless of mode.
    activeEl.innerHTML = '';
    selected.forEach(function (t) {
      var b = document.createElement('button');
      b.type = 'button';
      b.className = 'tag tag-active';
      b.setAttribute('data-tag', t);
      b.textContent = t + ' ✕';
      activeEl.appendChild(b);
    });

    // Candidate pool: static (global counts) at baseline or in union mode;
    // dynamic (recomputed on the current intersection) once a first tag is
    // picked in intersection mode.
    var pool = new Map();
    var staticPool = (m === 'union' || selected.length === 0);
    if (staticPool) {
      globalCounts.forEach(function (n, t) {
        if (selected.indexOf(t) === -1) pool.set(t, n);
      });
    } else {
      matched.forEach(function (it) {
        it.tags.forEach(function (t) {
          if (selected.indexOf(t) === -1) pool.set(t, (pool.get(t) || 0) + 1);
        });
      });
    }

    var split = splitDominant(pool, staticPool);
    var counts = split.dominant.map(function (t) { return pool.get(t); });
    var lo = counts.length ? Math.min.apply(null, counts) : 0;
    var hi = counts.length ? Math.max.apply(null, counts) : 0;

    cloudEl.innerHTML = '';
    split.dominant.forEach(function (t) {
      cloudEl.appendChild(chip(t, pool.get(t), sizeRem(pool.get(t), lo, hi),
        t === 'unclassified' ? 'tag-unclassified' : ''));
    });
    tailEl.innerHTML = '';
    split.tail.forEach(function (t) {
      cloudEl && tailEl.appendChild(chip(t, pool.get(t), null,
        'tag-tail' + (t === 'unclassified' ? ' tag-unclassified' : '')));
    });
    tailBtn.textContent = (tailOpen ? 'Hide' : 'Show') + ' ' + split.tail.length + ' more tags';
    tailBtn.hidden = split.tail.length === 0;
    tailWrap.hidden = !tailOpen || split.tail.length === 0;
  }

  document.addEventListener('click', function (e) {
    var btn = e.target.closest('button[data-tag]');
    if (btn) {
      var t = btn.getAttribute('data-tag');
      var i = selected.indexOf(t);
      if (i === -1) selected.push(t); else selected.splice(i, 1);
      render();
      return;
    }
    if (e.target === clearBtn) {
      selected = [];
      render();
      return;
    }
    if (e.target === tailBtn) {
      tailOpen = !tailOpen;
      render();
    }
  });
  modeInter.addEventListener('change', function () { selected = []; render(); });
  modeUnion.addEventListener('change', function () { selected = []; render(); });

  render();
})();
</script>
"""

CSS = """
.modepick{display:flex;gap:16px;align-items:center;flex-wrap:wrap;margin:14px 0 2px;
 font-family:ui-sans-serif,system-ui,-apple-system,sans-serif;font-size:.88rem}
.modepick label{display:inline-flex;align-items:center;gap:6px;cursor:pointer;color:var(--muted)}
.modepick input:checked+span{color:var(--ink);font-weight:600}
.modehint{font-size:.82rem;color:var(--muted);margin:2px 0 0}
.tagactive{display:flex;flex-wrap:wrap;gap:.3em .5em;margin:10px 0 0;min-height:1.6em}
.tagcloud{display:flex;flex-wrap:wrap;gap:.35em .6em;align-items:baseline;
 justify-content:center;padding:10px 4px}
.tagtail{display:flex;flex-wrap:wrap;gap:.3em .45em}
#tagtail-wrap{margin-top:10px}
.tag{font-family:ui-sans-serif,system-ui,-apple-system,sans-serif;
 border:1px solid var(--line);background:var(--panel);color:var(--ink);
 border-radius:99px;padding:.15em .75em;cursor:pointer;line-height:1.35}
.tag:hover{border-color:var(--accent)}
.tag .cnt{color:var(--muted);font-size:.72em;margin-left:.35em}
.tag[aria-pressed="true"]{background:var(--accent);border-color:var(--accent);color:var(--bg)}
.tag[aria-pressed="true"] .cnt{color:var(--bg);opacity:.82}
.tag-active{background:var(--accent);border-color:var(--accent);color:var(--bg);font-size:.85rem}
.tag-tail{font-size:.78rem;padding:.1em .55em}
.tag-unclassified{border-style:dashed}
.tagtail-toggle{font-family:ui-sans-serif,system-ui,sans-serif;font-size:.82rem;
 border:1px solid var(--line);background:var(--panel);color:var(--muted);
 border-radius:99px;padding:.3em .9em;cursor:pointer;margin-top:12px}
.tagtail-toggle:hover{border-color:var(--accent);color:var(--accent)}
.tagres-controls{display:flex;align-items:center;gap:14px;flex-wrap:wrap;
 margin:22px 0 10px;font-family:ui-sans-serif,system-ui,sans-serif;
 font-size:.88rem;color:var(--muted)}
#tagres-count strong{color:var(--ink)}
.clearbtn{font-family:ui-sans-serif,system-ui,sans-serif;font-size:.82rem;
 border:1px solid var(--line);background:var(--panel);color:var(--muted);
 border-radius:99px;padding:.3em .9em;cursor:pointer}
.clearbtn:hover{border-color:var(--accent);color:var(--accent)}
.srcline{font-size:.76rem;color:var(--muted);margin-top:1px}
.srcline b{color:var(--muted);font-weight:600}
.srcline.none{font-style:italic}
"""


def tags_page(css, esc, slug, artists_of, aliases, same_person, badge,
              playlist, issues):
    records = _records(artists_of)
    freq = _freq(records)
    cloud_html, tail_html, n_dom, n_tail = _cloud_html(freq, esc)
    results = _results_html(records, esc, slug)
    n_unclassified = freq.get("unclassified", 0)
    n_tracks = len(records)

    nav = atlas._nav("tags.html")

    body = f"""
<header>
<h1>By musical tags</h1>
<p class="sub">Genre, style and scene tags pulled from Discogs, MusicBrainz
and Last.fm, one API each, and combined per track. Pick one or several tags
to filter the list below.</p>
<p class="stats"><strong>{len(freq)}</strong> distinct tags &middot;
<strong>{n_dom}</strong> shown by size below, <strong>{n_tail}</strong> more
available alphabetically &middot; <strong>{n_unclassified}</strong> of
{n_tracks} tracks carry none, marked <code>unclassified</code></p>
</header>

<h2>Pick one or more tags</h2>
<p>Sized by how many tracks carry it, most common first in alphabetical
order.</p>

<div class="modepick">
<label><input type="radio" name="mode" id="mode-inter" checked><span>Intersection</span></label>
<label><input type="radio" name="mode" id="mode-union"><span>Union</span></label>
</div>
<p class="modehint"><strong>Intersection</strong> (default): tracks carrying
<em>every</em> tag picked. With none picked, nothing is filtered.
<strong>Union</strong>: tracks carrying <em>any</em> tag picked. With none
picked, the list is empty. In intersection mode only, picking a tag narrows
every other tag's count to what remains, and a tag that would drop to zero
disappears rather than stay at zero.</p>

<div id="tagactive" class="tagactive"></div>
<div id="tagcloud" class="tagcloud">{cloud_html}</div>
<button type="button" id="tagtail-toggle" class="tagtail-toggle" hidden>Show {n_tail} more tags</button>
<div id="tagtail-wrap" hidden>
<div id="tagtail" class="tagtail">{tail_html}</div>
</div>

<h2>Tracks</h2>
<div class="tagres-controls">
<span id="tagres-count"><strong>{n_tracks}</strong> of {n_tracks} tracks shown</span>
<button type="button" id="tagres-clear" class="clearbtn" hidden>Clear selection</button>
</div>
<noscript><p><em>Filtering needs JavaScript. Without it, every track is
listed below, in full, grouped by artist, with its own tags shown
underneath.</em></p></noscript>
<div id="tagres">
{results}
</div>

<div class="note">
<h4>What "tag" means here, and what it does not</h4>
<p>Discogs tags at the level of a release, sometimes an artist, rarely a
single track, so the same handful of styles often repeats across an artist's
whole discography here. MusicBrainz and Last.fm can tag a single recording,
but unevenly: of the tracks with a Last.fm genre tag, only a minority carry
one written for that specific song, most fall back to tags written for the
artist as a whole, and the fallback is not marked apart on this page. Treat a
tag as a description of the surrounding scene more than a precise label for
the four minutes it is attached to. Each track below shows which source
contributed which tags, so this can be checked rather than taken on faith.</p>
<p>Bandcamp is deliberately left out, not for lack of coverage on this
playlist but because it has no API: relying on it here would mean every
future addition stays untagged unless someone happens to open its Bandcamp
page by hand, which is exactly the kind of silent, uneven coverage this page
exists to avoid.</p>
<p>Spelling variants of the same word are merged into one tag (<em>hip
hop</em> and <em>hip-hop</em>, <em>synth-pop</em> and <em>synthpop</em>, and
a handful of others). Genuinely distinct words are not, even where they name
close or overlapping scenes: <em>rap</em> and <em>hip hop</em> stay two
separate tags here, not one.</p>
<p>Last.fm tags are free text written by whoever felt like tagging an artist,
not a controlled genre vocabulary. Tags that named a person rather than a
piece of music, that only restated a country or nationality already covered
on <a href="countries.html">the country page</a> or <a href="languages.html">the
language page</a>, or that carried no discernible musical meaning at all,
were dropped before they ever reached this page.</p>
<p><code>unclassified</code> is not a musical style. It means none of the
three sources returned a usable genre tag for that song, which is itself
worth seeing rather than hiding: a gap in Discogs, MusicBrainz and Last.fm
coverage, not a gap in the music.</p>
</div>

<footer>
<p>Companion page to the Spotify playlist <a href="{playlist}" target="_blank" rel="noopener"><strong>Transfem chants</strong></a>. Every artist's stated gender identity, with its source, is on the <a href="index.html">sources page</a>; this page is about the music only.</p>
<p class="colophon">Tag data collected via the Discogs, MusicBrainz and Last.fm APIs. A missing tag is a missing source, not a missing genre: if you know a better one, <a href="{issues}" target="_blank" rel="noopener">open an issue</a>. To have an entry taken down, or to raise anything about a person's identity, use the <a href="takedown.html">private channel</a> instead.</p>
</footer>
"""

    full_css = css + CSS
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Transfem chants — by musical tags</title>
<meta name="description" content="The {n_tracks} songs on Transfem chants, tagged by genre, style and scene from Discogs, MusicBrainz and Last.fm, filterable by intersection or union.">
<style>{full_css}</style>
</head>
<body>
<div class="wrap">
{nav}
{body}
</div>
{SCRIPT}
</body>
</html>
"""
