# -*- coding: utf-8 -*-
"""Génère tags.html, la page de tags de genre/style/scène.

Appelée par build.py, jamais seule. Seule page du dépôt qui embarque un script :
toutes les autres suivent le principe "aucune police distante, aucun script,
aucun CDN" affiché dans le README, mais un filtre combinant librement N tags
parmi près de trois cents ne se laisse pas écrire en pur CSS comme le tri de
`years.html`, qui ne gère que deux ou trois alternatives figées. Arbitrage de
Claire, 10 septembre 2026 : un petit script autonome, sans dépendance ni appel
réseau, uniquement sur cette page. La page reste utilisable sans script : la
liste complète des morceaux est déjà dans le HTML au chargement, groupée par
artiste ; le script ne fait qu'y montrer et cacher des lignes.

Deux zones de tags, choisies par Claire le 10 septembre 2026 :

- un nuage pour les tags dominants (les 30 les plus fréquents), classés par
  ordre alphabétique mais dont la taille de police suit le volume, plutôt
  qu'une disposition resserrée avec les plus gros au centre. Cette dernière
  demanderait un algorithme de tassement, se comporterait mal en responsive et
  serait peu accessible aux lecteurs d'écran ; ce nuage-ci reste une liste,
  donc lisible dans l'ordre par n'importe quel outil.
- une liste alphabétique, à taille fixe, pour tous les autres. La moitié des
  tags de cette page n'apparaissent que sur un seul morceau ; les noyer dans
  un nuage les aurait rendus illisibles ou aurait demandé de les cacher, ce
  que cette page ne fait pas plus qu'elle ne cache les pays vides de la carte.

Un tag synthétique, `unclassified`, représente les morceaux sans aucun tag
dans les trois sources. Il se comporte comme n'importe quel autre tag pour le
filtre, avec une puce à bordure pointillée plutôt qu'une case à part : même
absence de source, même traitement que les pays gris de la carte.
"""
import json
from collections import Counter

from data import ART
from tracks import all_tracks
from tags import TAGS

import atlas

# Tags dominants affichés en nuage ; le reste va dans la liste alphabétique.
DOMINANT_N = 30


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
        tags = TAGS.get(sid) or []
        out.append({
            "id": sid, "title": title, "credit": credit,
            "tags": tags if tags else ["unclassified"],
            "primary": _primary(credit, artists_of),
        })
    return out


def _freq(records):
    c = Counter()
    for r in records:
        c.update(r["tags"])
    return c


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


def _cloud(freq, esc):
    ordered = freq.most_common()
    dominant = sorted(ordered[:DOMINANT_N], key=lambda kv: kv[0])
    tail = sorted(ordered[DOMINANT_N:], key=lambda kv: kv[0])
    counts = [n for _, n in dominant]
    lo, hi = min(counts), max(counts)
    cloud = "".join(
        _chip(t, n, esc, size=_size_rem(n, lo, hi),
              extra="tag-unclassified" if t == "unclassified" else "")
        for t, n in dominant)
    tail_html = "".join(
        _chip(t, n, esc, extra="tag-tail" + (" tag-unclassified" if t == "unclassified" else ""))
        for t, n in tail)
    return (f'<div class="tagcloud">{cloud}</div>'
            f'<div class="tagtail">{tail_html}</div>'), len(dominant), len(tail)


def _track_line(r, esc, slug):
    url = "https://open.spotify.com/track/" + r["id"]
    names = [n.strip() for n in r["credit"].split(",")]
    cr = " · ".join(
        f'<a class="{"guest" if ART[n][0] == "guest" else "lead"}" '
        f'href="index.html#{slug(n)}">{esc(n)}</a>' for n in names)
    tags_json = esc(json.dumps(r["tags"]))
    ttags = ", ".join(r["tags"])
    return (f'<li data-tags="{tags_json}">'
            f'<a href="{esc(url)}" target="_blank" rel="noopener">{esc(r["title"])}</a> '
            f'<span class="cr">{cr}</span>'
            f'<span class="ttags">{esc(ttags)}</span></li>')


def _results(records, esc, slug):
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


SCRIPT = """
<script>
(function () {
  var tags = Array.prototype.slice.call(document.querySelectorAll('.tag'));
  var items = Array.prototype.slice.call(document.querySelectorAll('#tagres li[data-tags]'));
  var groups = Array.prototype.slice.call(document.querySelectorAll('#tagres .atlas-group'));
  var countEl = document.getElementById('tagres-count');
  var clearBtn = document.getElementById('tagres-clear');
  var selected = new Set();

  function apply() {
    var shown = 0;
    items.forEach(function (li) {
      var t = JSON.parse(li.getAttribute('data-tags'));
      var ok = true;
      selected.forEach(function (s) { if (t.indexOf(s) === -1) ok = false; });
      li.hidden = !ok;
      if (ok) shown++;
    });
    groups.forEach(function (g) {
      g.hidden = g.querySelectorAll('li:not([hidden])').length === 0;
    });
    countEl.textContent = shown + ' of ' + items.length + ' tracks shown';
    clearBtn.hidden = selected.size === 0;
  }

  tags.forEach(function (btn) {
    btn.addEventListener('click', function () {
      var t = btn.getAttribute('data-tag');
      var on = btn.getAttribute('aria-pressed') === 'true';
      btn.setAttribute('aria-pressed', on ? 'false' : 'true');
      if (on) { selected.delete(t); } else { selected.add(t); }
      apply();
    });
  });
  clearBtn.addEventListener('click', function () {
    selected.clear();
    tags.forEach(function (b) { b.setAttribute('aria-pressed', 'false'); });
    apply();
  });
  apply();
})();
</script>
"""

CSS = """
.tagcloud{display:flex;flex-wrap:wrap;gap:.35em .6em;align-items:baseline;
 justify-content:center;padding:10px 4px}
.tagtail{display:flex;flex-wrap:wrap;gap:.3em .45em;margin-top:16px}
.tag{font-family:ui-sans-serif,system-ui,-apple-system,sans-serif;
 border:1px solid var(--line);background:var(--panel);color:var(--ink);
 border-radius:99px;padding:.15em .75em;cursor:pointer;line-height:1.35}
.tag:hover{border-color:var(--accent)}
.tag .cnt{color:var(--muted);font-size:.72em;margin-left:.35em}
.tag[aria-pressed="true"]{background:var(--accent);border-color:var(--accent);color:var(--bg)}
.tag[aria-pressed="true"] .cnt{color:var(--bg);opacity:.82}
.tag-tail{font-size:.78rem;padding:.1em .55em}
.tag-unclassified{border-style:dashed}
.tagres-controls{display:flex;align-items:center;gap:14px;flex-wrap:wrap;
 margin:22px 0 10px;font-family:ui-sans-serif,system-ui,sans-serif;
 font-size:.88rem;color:var(--muted)}
#tagres-count strong{color:var(--ink)}
.clearbtn{font-family:ui-sans-serif,system-ui,sans-serif;font-size:.82rem;
 border:1px solid var(--line);background:var(--panel);color:var(--muted);
 border-radius:99px;padding:.3em .9em;cursor:pointer}
.clearbtn:hover{border-color:var(--accent);color:var(--accent)}
.ttags{display:block;margin-top:1px;font-size:.76rem;color:var(--muted)}
"""


def tags_page(css, esc, slug, artists_of, aliases, same_person, badge,
              playlist, issues):
    records = _records(artists_of)
    freq = _freq(records)
    cloud_html, n_dom, n_tail = _cloud(freq, esc)
    results = _results(records, esc, slug)
    n_unclassified = freq.get("unclassified", 0)
    n_tracks = len(records)

    nav = atlas._nav("tags.html")

    body = f"""
<header>
<h1>By musical tags</h1>
<p class="sub">Genre, style and scene tags pulled from Discogs, MusicBrainz
and Last.fm, one API each, and combined per track. Pick one or several tags
to narrow the list below to songs carrying all of them.</p>
<p class="stats"><strong>{len(freq)}</strong> distinct tags &middot;
<strong>{n_dom}</strong> shown by size above, <strong>{n_tail}</strong> more
listed alphabetically below &middot; <strong>{n_unclassified}</strong> of
{n_tracks} tracks carry none, marked <code>unclassified</code></p>
</header>

<h2>Pick one or more tags</h2>
<p>Sized by how many tracks carry it, the {n_dom} most common tags first,
in alphabetical order; every other tag follows below, at a fixed size,
also alphabetical. Selecting several narrows the list to tracks carrying
<em>all</em> of them, not any one of them.</p>

{cloud_html}

<div class="note">
<h4>What "tag" means here, and what it does not</h4>
<p>Discogs tags at the level of a release, sometimes an artist, rarely a
single track, so the same handful of styles often repeats across an artist's
whole discography here. MusicBrainz and Last.fm can tag a single recording,
but unevenly: of the tracks with a Last.fm genre tag, only a minority carry
one written for that specific song, most fall back to tags written for the
artist as a whole, and the fallback is not marked apart on this page. Treat a
tag as a description of the surrounding scene more than a precise label for
the four minutes it is attached to.</p>
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
not a controlled genre vocabulary. A small number of tags that named a
person rather than a piece of music were dropped before they ever reached
this page: this page classifies songs, not people, and the two should not be
allowed to blur into each other.</p>
<p><code>unclassified</code> is not a musical style. It means none of the
three sources returned a genre tag for that song, which is itself worth
seeing rather than hiding: a gap in Discogs, MusicBrainz and Last.fm
coverage, not a gap in the music.</p>
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
<meta name="description" content="The {n_tracks} songs on Transfem chants, tagged by genre, style and scene from Discogs, MusicBrainz and Last.fm, filterable by combination.">
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
