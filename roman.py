"""Transcriptions latines des noms et titres en écriture non latine.

Arbitrage de Claire, 11 novembre 2026 : tout nom d'artiste ou titre de
morceau en écriture non latine a aussi sa transcription latine. Elle est
affichée à côté de l'original (jamais à sa place), sert au tri alphabétique
et à la recherche.

Règle : la graphie latine publiée par l'artiste ou son label quand elle
existe ; sinon le système de référence de la langue (Hepburn pour le
japonais, romanisation révisée pour le coréen, pinyin pour le mandarin,
BGN/PCGN pour le russe, translittération courante pour l'hébreu).

Le build échoue si un nom ou un titre non latin n'a pas d'entrée ici, ou si
une entrée ne correspond plus à rien.

Clé : le texte exact tel qu'il figure dans data.py (nom) ou tracks.py
(titre). Valeur : (transcription, étiquette de langue BCP 47).
"""
import unicodedata

ROMAN = {
    # Nom crédité ; son propre nom latin (Discogs, master 2959375).
    "鍾潔希": ("Jessie Chung", "zh-Latn"),
    # Titres. Aucune graphie latine officielle trouvée (Discogs, Spotify,
    # recherche, 11 novembre 2026), sauf « Hayu leilot », graphie d'usage
    # de ce standard israélien.
    "愛在轉瞬間": ("Ài zài zhuǎnshùn jiān", "zh-Latn-pinyin"),
    "きみがすきだよ": ("Kimi ga suki da yo", "ja-Latn"),
    "さそり座の女": ("Sasoriza no onna", "ja-Latn"),
    "애지몽": ("Aejimong", "ko-Latn"),
    "됐거든": ("Dwaetgeodeun", "ko-Latn"),
    "היו לילות": ("Hayu leilot", "he-Latn"),
    "שיר גאווה": ("Shir ga'ava", "he-Latn"),
    "Голоса В Раю": ("Golosa v rayu", "ru-Latn"),
}


def non_latin(s):
    return any(ch.isalpha() and "LATIN" not in unicodedata.name(ch, "")
               for ch in s)


def sort_key(s):
    """Clé de tri : la transcription si elle existe, sans casse ni accents."""
    s = ROMAN.get(s, (s,))[0]
    return "".join(ch for ch in unicodedata.normalize("NFKD", s)
                   if not unicodedata.combining(ch)).casefold()


def rom_html(s, esc):
    """Texte échappé, chaque original suivi de sa transcription en petit."""
    out = esc(s)
    for k, (v, lang) in ROMAN.items():
        ek = esc(k)
        if ek in out:
            out = out.replace(
                ek, f'{ek} <span class="rom" lang="{lang}">{esc(v)}</span>')
    return out


def rom_text(s):
    """Version texte brut (infobulles, SVG, JSON) : « original (latin) »."""
    for k, (v, _) in ROMAN.items():
        if k in s:
            s = s.replace(k, f"{k} ({v})")
    return s


def check(names, titles):
    """names : noms crédités ; titles : titres de la playlist."""
    texts = set(names) | set(titles)
    missing = sorted(t for t in texts if non_latin(t) and t not in ROMAN)
    stale = sorted(k for k in ROMAN if k not in texts)
    if missing:
        raise SystemExit(f"roman.py : transcription manquante pour {missing}")
    if stale:
        raise SystemExit(f"roman.py : entrée sans objet {stale}")
