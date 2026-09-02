# -*- coding: utf-8 -*-
"""Génère index.html, la page de sources publiée sur GitHub Pages.

    python3 build.py

Trois entrées, une sortie :

    data.py    les artistes (ART) — fait foi pour tout statut ou source
    tracks.py  les morceaux, groupés par section
    style.css  la feuille de style, inlinée dans la page

La page produite est autonome : aucune police distante, aucun script, aucun CDN.
Le build échoue si un nom crédité dans tracks.py n'existe pas dans data.py.
"""
import html
import re

from data import ART
from tracks import SECTIONS, all_tracks

PLAYLIST = "https://open.spotify.com/playlist/4rK80rB8ycyAUdIKX6FOIk"
ISSUES = "https://github.com/clairevdd/transfem-chants/issues"

BADGE = {
    "verified": ("verified", "st-ok"),
    "partial": ("partial", "st-her"),
    "unresolved": ("unresolved", "st-flag"),
    "guest": ("featured", "st-note"),
}

ACCENTS = {"é": "e", "è": "e", "ê": "e", "ë": "e", "à": "a", "â": "a", "ä": "a",
           "î": "i", "ï": "i", "ô": "o", "ö": "o", "ù": "u", "û": "u", "ü": "u",
           "ç": "c", "ı": "i", "ğ": "g", "ş": "s", "ơ": "o", "ư": "u", "ạ": "a",
           "ề": "e", "ầ": "a", "ồ": "o", "ỏ": "o", "ị": "i"}

TRACKS = [(t, c) for _, t, c in all_tracks()]


def artists_of(credit):
    return [a.strip() for a in credit.split(",")]


def esc(s):
    return html.escape(s, quote=True)


def slug(name):
    s = name.lower()
    for k, v in ACCENTS.items():
        s = s.replace(k, v)
    return "a-" + re.sub(r"[^a-z0-9]+", "-", s).strip("-")


def check():
    """Vérifie tracks.py contre data.py avant de générer quoi que ce soit."""
    missing = sorted({a for _, c in TRACKS for a in artists_of(c) if a not in ART})
    if missing:
        raise SystemExit("Crédité dans tracks.py mais absent de data.py : " + ", ".join(missing))
    credited = {a for _, c in TRACKS for a in artists_of(c)}
    for name in sorted(set(ART) - credited):
        print(f"  note : {name} est dans data.py mais n'a aucun morceau, "
              f"donc n'apparaîtra pas sur la page.")
    ids = [i for i, _, _ in all_tracks()]
    if len(set(ids)) != len(ids):
        raise SystemExit("Identifiant Spotify en double dans tracks.py")


# Entrées distinctes de data.py qui désignent la même personne : un projet solo et
# le groupe qu'elle mène. Comptées une seule fois dans les statistiques.
SAME_PERSON = {
    "Antony and the Johnsons": "ANOHNI",
    "Against Me!": "Laura Jane Grace",
    "Venus de Mars and All the Pretty Horses": "Venus De Mars",
}

# "Scotland, UK" et "UK" désignent le même État pour le décompte.
COUNTRY_ALIASES = {"Scotland, UK": "UK"}


def stats():
    """Compte artistes, pays et langues. Les invitées ne comptent pas : le critère
    d'inclusion ne leur applique pas. Les cas `unresolved` sont comptés à part,
    parce que la page ne les présente justement pas comme transféminines.

    Ne comptent que les artistes qui ont effectivement un morceau dans la
    playlist. Une fiche écrite d'avance, en attente d'un titre, ne doit pas
    gonfler un compteur public : la page annoncerait une artiste, un pays ou
    une langue que le lecteur ne trouverait nulle part en écoutant."""
    on_playlist = {n for _, credit in TRACKS for n in artists_of(credit)}
    leads = {n: v for n, v in ART.items() if v[0] != "guest" and n in on_playlist}
    people = lambda names: {SAME_PERSON.get(n, n) for n in names}

    presented = people(n for n, v in leads.items() if v[0] in ("verified", "partial"))
    open_cases = people(n for n, v in leads.items() if v[0] == "unresolved")

    countries, languages = set(), set()
    for n, v in leads.items():
        if v[1] != "Unknown":
            for c in v[1].split(" / "):
                countries.add(COUNTRY_ALIASES.get(c.strip(), c.strip()))
        if v[2] != "—":
            for l in v[2].split(","):
                languages.add(l.strip())
    return {"tracks": len(TRACKS), "presented": len(presented),
            "open_cases": len(open_cases), "countries": len(countries),
            "languages": len(languages), "country_list": sorted(countries),
            "language_list": sorted(languages)}


def order_of_appearance():
    order, seen = [], set()
    for _, credit in TRACKS:
        for name in artists_of(credit):
            if name not in seen:
                seen.add(name)
                order.append(name)
    return order


def tracklist():
    out, n = [], 0
    for sec in SECTIONS:
        out.append(f'<h3 class="sec">{esc(sec["title"])}</h3>'
                   f'<p class="secblurb">{sec["blurb"]}</p>')
        out.append('<div class="tablewrap"><table class="tl"><tbody>')
        for sid, title, credit in sec["tracks"]:
            n += 1
            links = []
            for name in artists_of(credit):
                cls = "guest" if ART[name][0] == "guest" else "lead"
                links.append(f'<a class="{cls}" href="#{slug(name)}">{esc(name)}</a>')
            url = "https://open.spotify.com/track/" + sid
            out.append(f'<tr><td class="n">{n}</td>'
                       f'<td class="ti"><a href="{esc(url)}" rel="noopener">{esc(title)}</a></td>'
                       f'<td class="cr">{" · ".join(links)}</td></tr>')
        out.append('</tbody></table></div>')
    return "\n".join(out)


def card(name):
    status, country, lang, identity, quote, src, srcurl = ART[name]
    label, cls = BADGE[status]
    n = sum(1 for _, c in TRACKS if name in artists_of(c))
    plural = "s" if n > 1 else ""
    meta = (f'{esc(country)} &middot; {esc(lang)} &middot; {n} track{plural}'
            if lang != "—" else f'{esc(country)} &middot; {n} track{plural}')
    q = f'<blockquote>{esc(quote)}</blockquote>' if quote else ''
    if srcurl:
        s = f'<p class="src">Source: <a href="{esc(srcurl)}" rel="noopener">{esc(src)}</a></p>'
    elif status in ("unresolved", "guest"):
        s = '<p class="src none">No public source found.</p>'
    else:
        s = ''
    extra = " card-note" if status == "guest" else ""
    return (f'<article class="card{extra}" id="{slug(name)}">'
            f'<h4>{esc(name)}<span class="st {cls}">{esc(label)}</span></h4>'
            f'<p class="meta">{meta}</p><p class="desc">{esc(identity)}</p>{q}{s}</article>')


def page():
    order = order_of_appearance()
    leads = '<div class="cards">' + "\n".join(
        card(n) for n in order if ART[n][0] != "guest") + '</div>'
    guests = '<div class="cards">' + "\n".join(
        card(n) for n in order if ART[n][0] == "guest") + '</div>'
    css = open("style.css", encoding="utf-8").read()
    count = len(TRACKS)
    st = stats()

    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Transfem chants — sources</title>
<meta name="description" content="Every track in the Transfem chants playlist, with each artist's publicly stated gender identity and the source for it.">
<style>{css}</style>
</head>
<body>
<div class="wrap">

<header>
<h1>Transfem chants</h1>
<p class="sub">{count} songs <em>sung</em> by transfeminine artists: trans women, and non-binary or agender people assigned male at birth. This page gives, for every artist, the gender identity as they have made it public, and the source for it.</p>
<p class="stats"><strong>{st["tracks"]}</strong> tracks &middot; <strong>{st["presented"]}</strong> artists presented here as transfeminine, and <strong>{st["open_cases"]}</strong> open cases counted separately &middot; <strong>{st["countries"]}</strong> countries and territories &middot; <strong>{st["languages"]}</strong> languages</p>
<p class="statnote">Countries and languages are counted per artist, not per track: they record where an artist is from and which languages she records in, so a language listed here does not guarantee a song in that language on the playlist.</p>
<a class="hero-link" href="{PLAYLIST}" rel="noopener">Open the playlist on Spotify</a>
</header>

<h2>The tracks</h2>
<p>In playlist order. Each title links to Spotify; each artist name links to their entry below.</p>

{tracklist()}

<h2>How this list was built</h2>
<p>Four inclusion criteria, applied artist by artist.</p>
<ul class="plain">
<li><strong>Singing, not only composing.</strong> The artist has to carry the vocal. Trans composers and producers whose relevant work is instrumental were left out for that reason alone.</li>
<li><strong>A transfeminine identity.</strong> Anyone who does not recognise herself in the masculine gender she was assigned at birth — nearly every modern society assigns one administratively. Trans women, and non-binary or agender people assigned male at birth, but also artists whose own word for themselves comes from a tradition that maps onto none of those. Where an artist names her identity in her own terms, this page keeps her terms rather than translating them into ours.</li>
<li><strong>Made public by the artist.</strong> An identity inferred from gender expression, with no statement or confirmation, is not enough.</li>
<li><strong>Still current, and still willing.</strong> Artists who no longer identify this way were left out. So is anyone still trans who has since chosen to live stealth and would rather their transness not be published. That second case cannot be established from outside, so it rests on being told: any artist here who wants their entry taken down can <a href="{ISSUES}" rel="noopener">open an issue</a>, or have someone open one for them, and it will be removed without argument and without being asked to explain.</li>
<li><strong>Arbitrary inclusions.</strong> Where a case did not resolve cleanly, the track was kept and the doubt written down instead. See the <span class="st st-her">partial</span> and <span class="st st-flag">unresolved</span> entries.</li>
</ul>

<div class="note">
<h4>What the sources are worth</h4>
<p>Not every line here carries the same weight, and the page says so rather than hiding it. <span class="st st-ok">verified</span> means the source was opened and read, and states the claim explicitly. <span class="st st-her">partial</span> means the source is suggestive but carries no explicit first-person statement, or the artist’s own position is more complicated than the label. <span class="st st-flag">unresolved</span> marks an open case, set out in full below. <span class="st st-note">featured</span> marks someone credited on a track without being its lead artist.</p>
<p>Where an artist has described themselves in their own words, those words are quoted rather than paraphrased. The distinction matters: the criterion is what the artist said, not what the compiler concluded.</p>
<p>A <span class="st st-ok">verified</span> mark is never permanent. It records that a source was read on a given day; it does not close the question. This page began after an artist was nearly cut from the playlist on the strength of an unsourced claim about their gender, apparently confused with a different musician entirely. The correction was made, and then sat untouched until it too had quietly stopped being true. Both mistakes came from the same habit: repeating what was already written instead of going back to look.</p>
<p>Rechecking older entries on a schedule would not fix that, and would make something else worse. The artists easiest to recheck are the ones a press already follows; those who speak to their audience only through their own accounts would be rechecked last and least, which is the bias set out further down, reintroduced as a maintenance routine. So this page relies on being told instead. Anyone at all, artists first among them, can <a href="{ISSUES}" rel="noopener">open an issue</a> to say that someone’s identity has changed, that they now live stealth, or that they want their entry taken down.</p>
</div>

<h2>The artists</h2>
<p>In order of appearance.</p>
<ul class="legend">
<li><span class="st st-ok">verified</span> source read directly</li>
<li><span class="st st-her">partial</span> no explicit self-statement</li>
<li><span class="st st-flag">unresolved</span> open case</li>
</ul>

{leads}

<h2>Featured credits</h2>
<p>People credited on a track without being its lead artist. The inclusion criterion does not apply to them, so their gender identity is not a condition of anything here. It is documented anyway, for completeness, and the same rule holds: where nothing has been publicly stated, nothing is inferred. Being referred to with he/him or she/her in the press is not a statement of identity, and this page does not treat it as one.</p>

{guests}

<h2>Unresolved cases</h2>

<div class="note">
<h4>takihasdied, featured on “MURDER EVERY 1 U KNOW!”</h4>
<p>No public source about this artist’s gender identity was found, across Bandcamp, SoundCloud, Rate Your Music, Apple Music and press listings. That is information in itself: nobody owes a declaration.</p>
<p>The track stays because femtanyl, a trans woman, is its lead artist. But it should be confirmed that she carries part of the vocal. Every credit source found lists takihasdied as “featured artist” with no breakdown of the role, and takihasdied is a credited co-producer elsewhere, so a production-only feature cannot be ruled out. If takihasdied sings alone, the track falls outside the criterion and should come off.</p>
</div>

<div class="note">
<h4>Frost Children</h4>
<p>Angel and Lulu Prost are consistently referred to with she/her in the press, and their lyrics deal with gender dysphoria. But across the interviews read here, neither sibling makes a first-person statement about her own gender identity. What Angel says is about other people: “I care about trans people,” and “I would give every trans girl a gun to defend themselves.” Solidarity is not a declaration, and this page does not read it as one.</p>
<p>A second question is open alongside the first: which sibling carries the vocal on these tracks could not be established from any source found, so the singing criterion is unverified too. Both tracks are kept and both questions are left visible.</p>
</div>

<div class="note">
<h4>Haiifa Magic</h4>
<p>Her identity as a trans woman rests here on a single i-D article from 2018. No first-person statement by the artist was found, and no more recent source. This is the weakest line on the page. It is flagged rather than quietly dropped.</p>
</div>

<div class="note">
<h4>Jackie Shane</h4>
<p>Shane lived and was addressed as a woman and used she/her pronouns. But in a 2017 interview she declined the labels applied to her, rejecting both “transgender” and “queer” and preferring “gay” as an umbrella for the whole alphabet. She is widely described posthumously as a trans woman, a framing she herself largely avoided while alive.</p>
<p>She is kept on the playlist, with the tension left visible rather than resolved in her place. A page built on the principle of taking artists at their own word cannot then quietly overwrite one of them.</p>
</div>

<h2>What this list does not show</h2>
<p>There is a bias built into the third criterion, and it is better named than hidden. Requiring a public statement means requiring that someone was interviewed, recorded and published — which happens to artists a press has already decided are worth covering. An artist with no interviews, no profile and no biography cannot meet the criterion however out she is among the people who know her. So this page over-represents the already visible and under-represents the precarious, the very young, and anyone working outside the reach of a music press. Several artists were left off these pages for that reason alone, and their absence says nothing about them.</p>

<p>Several language areas are still missing: nothing in Persian, Hindi, Mandarin, Urdu, or the languages of East Africa. That is not an absence of artists. It is an absence of usable public sources. In a number of those contexts, declaring yourself publicly carries real risk, and the shape of this page reflects that before it reflects anything about the music. The gaps do close: German and Indonesian were both named here as missing until an artist turned up who had said something about herself in public, in her own words, and could be read.</p>
<p>Found an error, a better source, or an artist who should be here? <a href="{ISSUES}" rel="noopener">Open an issue</a>.</p>

<footer>
<p>Companion page to the Spotify playlist <a href="{PLAYLIST}" rel="noopener"><strong>Transfem chants</strong></a>. The identities described here are the ones the artists have made public themselves; every link goes to the source for the claim beside it.</p>
<p class="colophon">Compiled <time datetime="2026-08">August 2026</time>. The playlist is by <a href="https://github.com/clairevdd" rel="noopener">Claire</a>, who set the criteria and made every call about what stays and what goes. The source research behind this page, the verification of each artist’s public statement, and the page itself were done by Claude, Anthropic’s AI assistant, working from those criteria. Where a claim could not be verified, that is written down rather than smoothed over.</p>
</footer>

</div>
</body>
</html>
"""


if __name__ == "__main__":
    check()
    out = page()
    open("index.html", "w", encoding="utf-8").write(out)
    st = stats()
    print(f"index.html écrit : {st['tracks']} morceaux, {len(ART)} entrées, {len(out)} octets")
    print(f"  {st['presented']} artistes présentées comme transfem + {st['open_cases']} cas ouverts")
    print(f"  {st['countries']} pays/territoires : {', '.join(st['country_list'])}")
    print(f"  {st['languages']} langues : {', '.join(st['language_list'])}")
