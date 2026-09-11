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
import urllib.parse

import atlas
import chrono
import tagcloud
import sonic

from data import ART
from tracks import SECTIONS, all_tracks
from years import YEARS
from lyrics import LYRICS, SEARCH
from tags import TAGS

PLAYLIST = "https://open.spotify.com/playlist/4rK80rB8ycyAUdIKX6FOIk"
ISSUES = "https://github.com/clairevdd/transfem-chants/issues"

# Canal privé pour tout ce qui touche à l'identité d'une personne : demande de
# retrait, passage en stealth, changement d'identité.
#
# Les issues GitHub sont PUBLIQUES et le restent. Demander à quelqu'un d'annoncer
# sur un fil indexé qu'elle passe en stealth défait exactement ce qu'elle
# demande. D'où ce second canal.
#
# CONTRAINTE ABSOLUE : mettre ici l'URL d'un FORMULAIRE, jamais une adresse
# e-mail. L'adresse de destination se configure chez le prestataire du
# formulaire et ne doit apparaître dans aucun fichier du dépôt — ni dans les
# pages générées, ni dans l'historique git, qui est public et définitif.
# Le contrôle _no_email() ci-dessous refuse de générer les pages si une adresse
# ou un lien mailto s'y glisse.
CONTACT = "https://tally.so/r/2EWdyg"

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


# Une adresse écrite dans un fichier du dépôt y reste : les pages se regénèrent,
# l'historique git non. Ce motif attrape aussi bien un mailto: qu'une adresse
# laissée en clair dans une note de data.py ou de years.py.
MAIL = re.compile(r"mailto:|[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")


def _no_email(name, text):
    """Refuse d'écrire une page qui contient une adresse e-mail ou un mailto.

    Claire a demandé que son adresse personnelle n'apparaisse nulle part sur
    internet : le canal privé passe donc par un formulaire, dont le prestataire
    seul connaît la destination. Ce contrôle est le filet, pour le jour où une
    adresse se glisserait dans une source, une note ou une citation.
    """
    hit = MAIL.search(text)
    if hit:
        raise SystemExit(
            f"build.py : {name} contient une adresse e-mail ou un lien mailto "
            f"(« {hit.group(0)} »). Le dépôt est public et son historique est "
            f"définitif : aucune adresse ne doit y entrer. Passer par l'URL d'un "
            f"formulaire (constante CONTACT).")


def check():
    if not CONTACT:
        raise SystemExit(
            "build.py : CONTACT est vide. Renseigner en tête de build.py l'URL du "
            "formulaire privé avant de générer les pages. Sans elle, les demandes "
            "de retrait repartiraient vers les issues publiques, c'est-à-dire "
            "exactement le défaut que ce canal corrige.")
    if "github.com" in CONTACT:
        raise SystemExit(
            "build.py : CONTACT pointe vers GitHub. Les issues et les discussions "
            "y sont publiques : ce canal doit être privé.")
    if MAIL.search(CONTACT):
        raise SystemExit(
            "build.py : CONTACT contient une adresse e-mail. Mettre l'URL d'un "
            "formulaire, dont le prestataire seul connaît la destination.")

    ids = {sid for sid, _, _ in all_tracks()}
    manquants = sorted(ids - set(YEARS))
    if manquants:
        raise SystemExit(f"build.py : morceaux absents de years.py : {manquants}")
    orphelins = sorted(set(YEARS) - ids)
    if orphelins:
        raise SystemExit(f"build.py : years.py garde des morceaux retirés de la playlist : {orphelins}")
    manquants_lyrics = sorted(ids - set(LYRICS))
    if manquants_lyrics:
        raise SystemExit(f"build.py : morceaux absents de lyrics.py : {manquants_lyrics}")
    orphelins_lyrics = sorted(set(LYRICS) - ids)
    if orphelins_lyrics:
        raise SystemExit(f"build.py : lyrics.py garde des morceaux retirés de la playlist : {orphelins_lyrics}")
    manquants_tags = sorted(ids - set(TAGS))
    if manquants_tags:
        raise SystemExit(f"build.py : morceaux absents de tags.py : {manquants_tags}")
    orphelins_tags = sorted(set(TAGS) - ids)
    if orphelins_tags:
        raise SystemExit(f"build.py : tags.py garde des morceaux retirés de la playlist : {orphelins_tags}")
    orphelins_sonic = sorted(set(sonic.TRACKS) - ids)
    if orphelins_sonic:
        raise SystemExit(f"build.py : sonic.py garde des morceaux retirés de la playlist : {orphelins_sonic}")
    # Contrairement à years.py/lyrics.py/tags.py, sonic.py n'est pas mis à jour
    # morceau par morceau : ses données viennent d'un relevé Tunebat manuel,
    # recalculé par lots. Un morceau récent sans profil sonore n'est donc pas
    # une erreur, juste un signal à ne pas laisser passer en silence.
    manquants_sonic = sorted(ids - set(sonic.TRACKS))
    if manquants_sonic:
        print(f"  note : {len(manquants_sonic)} morceau(x) sans profil sonore "
              f"(sonic.py), en attente d'un relevé Tunebat : {manquants_sonic}")
    for sid, v in YEARS.items():
        if v["status"] == "verified" and not (v["url"] and v["checked"] and v["first_public"]):
            raise SystemExit(f"build.py : {sid} est verified sans source, date ou contrôle datés")

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
            "languages": len(languages), "country_list": sorted(countries, key=str.lower),
            "language_list": sorted(languages, key=str.lower)}


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
            # L'année de première parution vient de years.py. La page « by year »
            # porte la source et la réserve ; ici on ne donne que le millésime.
            yv = YEARS[sid]
            yr = str(yv["first_public"])[:4] if yv["first_public"] else "—"
            ttl = "first published " + str(yv["first_public"]) if yv["first_public"] else "date not established"
            # Lien externe vers les paroles. Un lien de type "recherche" (aucune
            # fiche précise confirmée) le dit dans son titre plutôt que de se
            # faire passer pour une fiche trouvée. Dans ce cas, on ne pointe pas
            # vers une recherche à l'aveugle sur Genius, mais vers une recherche
            # DuckDuckGo (nom de l'artiste + titre + "lyrics"), généralement
            # plus fiable pour retrouver la bonne page quel que soit le site.
            lyr_url = LYRICS.get(sid)
            if lyr_url:
                if sid in SEARCH:
                    leads = [name for name in artists_of(credit) if ART[name][0] != "guest"]
                    lead_name = leads[0] if leads else artists_of(credit)[0]
                    q = urllib.parse.quote_plus(f"{lead_name} {title} lyrics")
                    lyr_url = f"https://duckduckgo.com/?q={q}"
                    lyr_ttl = "search results, no exact page confirmed"
                else:
                    lyr_ttl = "lyrics"
                lyr_cell = (f'<a href="{esc(lyr_url)}" target="_blank" rel="noopener" '
                           f'title="{esc(lyr_ttl)}">lyrics{"&nbsp;?" if sid in SEARCH else ""}</a>')
            else:
                lyr_cell = ""
            out.append(f'<tr><td class="n">{n}</td>'
                       f'<td class="ti"><a href="{esc(url)}" target="_blank" rel="noopener">{esc(title)}</a></td>'
                       f'<td class="cr">{" · ".join(links)}</td>'
                       f'<td class="yr"><a href="years.html" title="{esc(ttl)}">{yr}</a></td>'
                       f'<td class="ly">{lyr_cell}</td></tr>')
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
    # Une fiche peut citer plusieurs sources plutôt qu'une seule : src vaut
    # alors None et srcurl une liste/un tuple de paires (nom, URL), au lieu
    # d'une URL unique. Voir Ella, entrée du 11 septembre 2026.
    if isinstance(srcurl, (list, tuple)) and srcurl and isinstance(srcurl[0], (list, tuple)):
        links_html = ", ".join(
            f'<a href="{esc(u)}" target="_blank" rel="noopener">{esc(nm)}</a>'
            for nm, u in srcurl)
        s = f'<p class="src">Sources: {links_html}</p>'
    elif srcurl:
        s = f'<p class="src">Source: <a href="{esc(srcurl)}" target="_blank" rel="noopener">{esc(src)}</a></p>'
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
{atlas._nav("index.html")}
<header>
<h1>Transfem chants</h1>
<p class="sub">{count} songs <em>sung</em> by transfeminine artists: trans women, and non-binary or agender people assigned male at birth. This page gives, for every artist, the gender identity as they have made it public, and the source for it.</p>
<p class="stats"><strong>{st["tracks"]}</strong> tracks &middot; <strong>{st["presented"]}</strong> artists presented here as transfeminine, and <strong>{st["open_cases"]}</strong> entries marked unresolved and not counted among them &middot; <strong>{st["countries"]}</strong> countries and territories &middot; <strong>{st["languages"]}</strong> languages</p>
<a class="hero-link" href="{PLAYLIST}" target="_blank" rel="noopener">Open the playlist on Spotify</a>
</header>

<h2>The tracks</h2>
<p>In playlist order. Each title links to Spotify; each artist name links to their entry below; the year links to <a href="years.html">when the song first existed</a>; and, where one was found, <em>lyrics</em> links to an external page. A question mark after that link means no exact page could be confirmed, and it points to a DuckDuckGo search (artist name, title, and "lyrics") instead.</p>

{tracklist()}

<h2>How this list was built</h2>
<p>Four inclusion criteria, applied artist by artist.</p>
<ul class="plain">
<li><strong>Singing, not only composing.</strong> The artist has to carry the vocal. Trans composers and producers whose relevant work is instrumental were left out for that reason alone.</li>
<li><strong>A transfeminine identity.</strong> Anyone who does not recognise herself in the masculine gender she was assigned at birth — nearly every modern society assigns one administratively. Trans women, and non-binary or agender people assigned male at birth, but also artists whose own word for themselves comes from a tradition that maps onto none of those. Where an artist names her identity in her own terms, this page keeps her terms rather than translating them into ours.</li>
<li><strong>Made public by the artist.</strong> An identity inferred from gender expression, with no statement or confirmation, is not enough.</li>
<li><strong>Still current, and still willing.</strong> Artists who no longer identify this way were left out. So is anyone still trans who has since chosen to live stealth and would rather their transness not be published. That second case cannot be established from outside, so it rests on being told — and on being told somewhere that costs the person telling nothing. See <a href="takedown.html">taking an entry down</a>.</li>
<li><strong>Arbitrary inclusions.</strong> Where a case did not resolve cleanly, the track was kept and the doubt written down instead. See the <span class="st st-her">partial</span> and <span class="st st-flag">unresolved</span> entries.</li>
</ul>

<div class="note">
<h4>What the sources are worth</h4>
<p>Not every line here carries the same weight, and the page says so rather than hiding it. <span class="st st-ok">verified</span> means the source was opened and read, and states the claim explicitly. <span class="st st-her">partial</span> means the source is suggestive but carries no explicit first-person statement, or the artist’s own position is more complicated than the label. <span class="st st-flag">unresolved</span> marks an open case, set out in full below. <span class="st st-note">featured</span> marks someone credited on a track without being its lead artist.</p>
<p>Where an artist has described themselves in their own words, those words are quoted rather than paraphrased. The distinction matters: the criterion is what the artist said, not what the compiler concluded.</p>
<p>A <span class="st st-ok">verified</span> mark is never permanent. It records that a source was read on a given day; it does not close the question. This page began after an artist was nearly cut from the playlist on the strength of an unsourced claim about their gender, apparently confused with a different musician entirely. The correction was made, and then sat untouched until it too had quietly stopped being true. Both mistakes came from the same habit: repeating what was already written instead of going back to look.</p>
<p>Rechecking older entries on a schedule would not fix that, and would make something else worse. The artists easiest to recheck are the ones a press already follows; those who speak to their audience only through their own accounts would be rechecked last and least, which is the bias set out further down, reintroduced as a maintenance routine. So this page relies on being told instead — that someone’s identity has changed, that she now lives stealth, that she wants her entry gone. All of that goes through <a href="takedown.html">a private channel, on its own page</a>, never through a public thread.</p>
</div>

<h2>The artists</h2>
<p>In order of appearance.</p>
<p class="statnote">Countries and languages are counted per artist, not per track: they record where an artist is from and which languages she records in, so a language listed here does not guarantee a song in that language on the playlist.</p>
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
<p>Two of these carry the <span class="st st-flag">unresolved</span> mark above and are not counted as transfeminine artists. The third, Jackie Shane, is counted and kept: what is open in her case is not whether she belongs on the playlist, but which words she would have accepted for herself.</p>

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

<h2>Five other ways in</h2>
<p>The same artists and the same tracks, cut differently. All five pages are built from the entries above, so nothing on them is claimed that is not sourced here.</p>
<ul class="plain">
<li><strong><a href="countries.html">By country</a></strong> — a world map shaded by how many artists each country contributes, and the list behind it. The empty parts of that map are the argument.</li>
<li><strong><a href="languages.html">By language</a></strong> — which languages these artists record in, and how lopsided the distribution is.</li>
<li><strong><a href="years.html">By year</a></strong> — when each song first existed, on a single timeline, and how far streaming metadata moves some of them from that date.</li>
<li><strong><a href="tags.html">By tags</a></strong> — genre, style and scene tags pulled from Discogs, MusicBrainz and Last.fm, filterable by combination. Uses a script.</li>
<li><strong><a href="sonic.html">By sonic profile</a></strong> — a 3D map of how these songs actually sound, grouped by tempo, energy and production rather than by genre label. Uses a script and, alone on this site, an external library.</li>
</ul>

<h2>What this list does not show</h2>
<p>There is a bias built into the third criterion, and it is better named than hidden. Requiring a public statement means requiring that someone was interviewed, recorded and published — which happens to artists a press has already decided are worth covering. An artist with no interviews, no profile and no biography cannot meet the criterion however out she is among the people who know her. So this page over-represents the already visible and under-represents the precarious, the very young, and anyone working outside the reach of a music press. Several artists were left off these pages for that reason alone, and their absence says nothing about them.</p>

<p>Several language areas are still missing: nothing in Persian, Hindi, Mandarin, or the languages of East Africa, and one song each in most of what is here. That is not an absence of artists. It is an absence of usable public sources. In a number of those contexts, declaring yourself publicly carries real risk, and the shape of this page reflects that before it reflects anything about the music. The gaps do close: German, Indonesian and Urdu were each named here as missing until an artist turned up who had said something about herself in public, in her own words, and could be read.</p>
<p>Found an error, a better source, or an artist who should be here? <a href="{ISSUES}" target="_blank" rel="noopener">Open an issue</a> — that thread is public, which is fine for a date or a citation. Anything touching a particular person’s identity, taking an entry down first among them, goes through <a href="takedown.html">a channel of its own</a> instead.</p>

<footer>
<p>Companion page to the Spotify playlist <a href="{PLAYLIST}" target="_blank" rel="noopener"><strong>Transfem chants</strong></a>. The identities described here are the ones the artists have made public themselves; every link goes to the source for the claim beside it.</p>
<p class="colophon">Compiled <time datetime="2026-08">August 2026</time>. The playlist is by <a href="https://github.com/clairevdd" target="_blank" rel="noopener">Claire</a>, who set the criteria and made every call about what stays and what goes. The source research behind this page, the verification of each artist’s public statement, and the page itself were done by Claude, Anthropic’s AI assistant, working from those criteria. Where a claim could not be verified, that is written down rather than smoothed over.</p>
</footer>

</div>
</body>
</html>
"""


if __name__ == "__main__":
    check()
    css = open("style.css", encoding="utf-8").read()
    st = stats()

    out = page()
    _no_email("index.html", out)
    open("index.html", "w", encoding="utf-8").write(out)
    print(f"index.html écrit : {st['tracks']} morceaux, {len(ART)} entrées, {len(out)} octets")

    args = (css, esc, slug, artists_of, COUNTRY_ALIASES, SAME_PERSON, BADGE,
            PLAYLIST, ISSUES)
    for name, fn in (("countries.html", atlas.countries_page),
                     ("languages.html", atlas.languages_page),
                     ("years.html", chrono.years_page),
                     ("tags.html", tagcloud.tags_page),
                     ("sonic.html", sonic.sonic_page)):
        text = fn(*args)
        _no_email(name, text)
        open(name, "w", encoding="utf-8").write(text)
        print(f"{name} écrit : {len(text)} octets")

    # La politique de retrait, sur sa propre page depuis le 9 septembre 2026 :
    # elle prenait trop de place dans index.html.
    take = atlas.takedown_page(css, PLAYLIST, ISSUES, CONTACT)
    _no_email("takedown.html", take)
    open("takedown.html", "w", encoding="utf-8").write(take)
    print(f"takedown.html écrit : {len(take)} octets")

    print(f"  {st['presented']} artistes présentées comme transfem + {st['open_cases']} cas ouverts")
    print(f"  {st['countries']} pays/territoires : {', '.join(st['country_list'])}")
    print(f"  {st['languages']} langues : {', '.join(st['language_list'])}")
