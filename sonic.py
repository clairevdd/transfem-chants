# -*- coding: utf-8 -*-
"""Génère sonic.html, la page de profil sonore.

Deuxième page du dépôt à embarquer un script, après tags.html, et la première
à charger une dépendance externe (three.js, pour le nuage 3D). Arbitrages de
Claire du 10 septembre 2026, tous deux demandés explicitement avant que quoi
que ce soit ne soit codé : elle a autorisé cette double entorse au principe
« aucun script, aucun CDN » plutôt qu'un moteur 3D fait main, en échange de
volumes semi-transparents par cluster et de contrôles orbite fluides que je
n'aurais pas pu offrir sans bibliothèque.

## Ce que cette page mesure, et ce qu'elle ne republie pas

La source est un relevé manuel de 13 « audio features » Tunebat pour les 146
morceaux (tb_key, tb_camelot, tb_bpm, tb_duration, tb_popularity, tb_energy,
tb_danceability, tb_happiness, tb_acousticness, tb_instrumentalness,
tb_liveness, tb_speechiness, tb_loudness), collecté par Claire avec
l'autorisation de Tunebat. Les conditions d'utilisation de Tunebat interdisent
de republier ces valeurs par morceau. Conséquence directe sur ce fichier :
aucune des 13 valeurs brutes, pour aucun morceau, ne figure ici ni nulle part
dans le dépôt public. Le tableur original (`relevetunebat.xlsx`) vit dans le
projet Claude, jamais dans le dépôt.

Ce qui est publié à la place, ce sont deux résultats dérivés d'un calcul
statistique, et qui ne permettent pas de reconstituer les valeurs d'origine :

- pour chaque morceau, sa position sur 3 axes calculés par ACP (voir plus
  bas) et le numéro du groupe auquel il appartient (`TRACKS`, ci-dessous) ;
- pour chaque groupe, la moyenne de chacune des 9 features retenues,
  calculée sur au moins 10 morceaux (`CLUSTERS`, ci-dessous). Claire a fixé
  le plancher à 4 morceaux minimum précisément pour qu'une moyenne ne puisse
  jamais se ramener aux valeurs d'un morceau unique ; tous les groupes ici en
  comptent nettement plus.

## La méthode, en bref (le détail et les chiffres sont dans le projet Claude,
`claude/METHODE-SONIC.md`)

Popularity et duration sont écartées d'entrée : la première mesure une
audience Spotify, pas un son, et varie dans le temps ; la seconde décrit une
durée plutôt qu'une texture. Key et camelot sont écartées aussi, à la
demande de Claire du 10 septembre 2026 : ce sont des variables catégorielles
que l'ACP ne sait pas traiter nativement, et la seule information qui s'en
approcherait, le mode majeur/mineur, est de toute façon mieux captée par
`happiness`, qui est continue.

Restent 9 dimensions (bpm, energy, danceability, happiness, acousticness,
instrumentalness, liveness, speechiness, loudness), standardisées puis
réduites par ACP. Les 3 premières composantes expliquent 62 % de la
variance ; le reste n'est pas montré, ce qui est dit explicitement sur la
page plutôt que caché. Le classement en groupes est calculé par classification
ascendante hiérarchique (Ward) sur les 9 dimensions complètes, pas sur les 3
axes de la vue 3D, pour ne pas perdre les 38 % restants. Claire a choisi 6
groupes (le maximum qu'elle avait fixé) après avoir vu que chacun restait
musicalement distinct ; aucune fusion pour cause de petit effectif n'a été
nécessaire, tous les groupes dépassant largement le plancher de 4.

## Recalcul futur

Une augmentation de la playlist qui ajoute des morceaux à `relevetunebat.xlsx`
change la moyenne et l'écart-type de chaque feature, donc les coordonnées
ACP et potentiellement l'appartenance aux groupes de tous les morceaux, pas
seulement des nouveaux. C'est le comportement normal d'une ACP et d'un
clustering, pas un bug, mais cela veut dire que les données de ce fichier ne
se mettent pas à jour par simple ajout : il faut relancer le calcul complet
sur l'ensemble du tableur, puis régénérer `TRACKS` et `CLUSTERS` en entier.
Procédure détaillée dans `claude/METHODE-SONIC.md`.

## Retours de Claire du 10 septembre 2026, après la première version

Cinq changements sur la première mise en ligne, tous à sa demande :

- **Le risque de réidentification des valeurs Tunebat par les moyennes de
  groupe n'inquiète pas Claire** : reconstituer statistiquement les 9 valeurs
  d'un morceau à partir de moyennes de groupe est bien plus coûteux que
  d'aller simplement les consulter sur Tunebat. Le plancher de 4 morceaux par
  groupe reste en place par prudence, mais la mise en garde sur ce point est
  allégée en conséquence.
- **Couleurs de cluster corrigées.** La palette précédente employait deux
  bleus Okabe-Ito (`#56B4E9` et `#0072B2`) sur des groupes proches dans
  l'espace ACP, illisibles l'un contre l'autre. La nouvelle palette
  n'emploie plus qu'un bleu, et répartit les six teintes en priorisant
  l'écart entre les paires de groupes les plus proches par distance de
  centroïde (calculée sur les 146 positions ACP) plutôt qu'un ordre arbitraire.
- **Nuage 3D : axes rendus visibles**, un trait par composante avec, à
  chaque extrémité, le pôle correspondant en clair (« loud, energetic » /
  « hushed, acoustic », etc.), pour s'orienter dans l'espace sans redescendre
  à la section qui décrit les trois axes.
- **Survol et clic corrigés.** Le survol testait une intersection 3D exacte
  contre des sphères minuscules, ce qui les rendait quasiment impossibles à
  viser : la détection se fait maintenant par distance à l'écran, en pixels,
  ce qui rend chaque point beaucoup plus facile à atteindre. Le clic sur un
  point précis renvoie désormais au morceau lui-même (ouvre sa liste si elle
  est repliée, et le met en évidence) ; le clic sur le volume colorisé, hors
  d'un point, renvoie à la section du groupe, comme avant.
- **Page réordonnée.** « The six groups » remonte en tête, les six groupes se
  suivant immédiatement pour comparer les radar plots d'un coup d'œil ; la
  liste des morceaux de chaque groupe est repliée par défaut, visible à la
  demande sous son radar. Le nuage 3D et « The three dimensions » descendent
  en fin de page : Claire les juge plus difficiles à lire et moins riches en
  information musicale que le classement en groupes lui-même, en partie parce
  que le classement se fait sur les 9 dimensions complètes et non sur les 3
  seuls axes de la vue 3D, ce qui produit des volumes qui se chevauchent
  visuellement sans rien perdre côté musical.
- **Définitions des 9 features ajoutées** (`FEATURE_INFO`), avec l'échelle
  théorique de Tunebat quand elle existe (0 à 100 pour tout sauf le tempo et
  le volume), affichées en infobulle sur chaque nom de feature et réunies
  dans une section « The nine measurements ».
- **Colonne de moyenne playlist ajoutée** (`PLAYLIST_MEANS`) à côté de la
  moyenne de chaque groupe dans les tableaux de valeurs, pour que l'écart
  d'un groupe à l'ensemble de la playlist se lise directement plutôt que de
  se déduire de mémoire.
"""
import json
import math
from collections import defaultdict

from data import ART
from tracks import all_tracks

import atlas

# three.js, chargée depuis jsdelivr (miroir direct de npm, mêmes chemins) :
# c'est la seule bibliothèque externe de tout le dépôt. Version figée pour
# que la page ne change jamais de rendu sous les pieds de quelqu'un.
THREE_VERSION = "0.186.0"

# Les 9 dimensions retenues, dans l'ordre où elles apparaissent sur les
# radar plots. min/max observés sur les 146 morceaux, utilisés pour mettre
# chaque axe à la même échelle visuelle malgré des unités très différentes
# (bpm de 71 à 203, loudness de -18 à 2 dB, le reste de 0 à 100).
FEATURES = [
    # (clé, libellé complet, libellé court pour l'axe du radar, unité, min, max)
    ("tb_bpm", "Tempo", "Tempo", "BPM", 71, 203),
    ("tb_energy", "Energy", "Energy", "", 9, 100),
    ("tb_danceability", "Danceability", "Dance", "", 10, 90),
    ("tb_happiness", "Happiness", "Happy", "", 5, 93),
    ("tb_acousticness", "Acousticness", "Acoustic", "", 0, 99),
    ("tb_instrumentalness", "Instrumentalness", "Instrum.", "", 0, 91),
    ("tb_liveness", "Liveness", "Live", "", 4, 96),
    ("tb_speechiness", "Speechiness", "Speech", "", 3, 52),
    ("tb_loudness", "Loudness", "Loud", "dB", -18, 2),
]

# Moyenne de chaque feature sur l'ensemble des 146 morceaux (pas seulement
# ceux d'un groupe). Publiable au même titre que les moyennes de groupe : une
# moyenne sur 146 valeurs ne se ramène à aucune valeur individuelle. Ajoutée
# le 10 septembre 2026 à la demande de Claire, en colonne de comparaison à
# côté de la moyenne de chaque groupe dans les tableaux de valeurs.
PLAYLIST_MEANS = {
    "tb_bpm": 124.7, "tb_energy": 66.2, "tb_danceability": 58.3,
    "tb_happiness": 46.7, "tb_acousticness": 22.6,
    "tb_instrumentalness": 6.7, "tb_liveness": 22.8,
    "tb_speechiness": 11.3, "tb_loudness": -7.2,
}

# Définitions des 9 features, en anglais (champ publié) : ce qu'elles
# mesurent et leur échelle théorique selon Tunebat, quand elle existe.
# Tunebat reprend le schéma de l'ancienne API "audio features" de Spotify
# (0-100 pour la plupart des mesures, dB pour le volume, aucune borne fixe
# pour le tempo) ; les phrases ci-dessous sont une reformulation, pas une
# citation. Affichées en infobulle sur chaque nom de feature et réunies dans
# la section "The nine measurements". Ajouté le 10 septembre 2026 à la
# demande de Claire.
FEATURE_INFO = {
    "tb_bpm": (
        "The track's estimated tempo, in beats per minute. Tunebat reports "
        "this directly; there is no fixed theoretical scale."
    ),
    "tb_energy": (
        "A measure of intensity and activity, 0 to 100. Energetic tracks "
        "tend to feel fast, loud and noisy."
    ),
    "tb_danceability": (
        "How suitable a track is for dancing, 0 to 100, from its tempo, "
        "rhythm stability, beat strength and overall regularity."
    ),
    "tb_happiness": (
        "Tunebat's name for what Spotify's discontinued audio-features API "
        "called \"valence\": how musically positive a track sounds, 0 to "
        "100. Higher sounds more cheerful; lower sounds more sombre or tense."
    ),
    "tb_acousticness": (
        "Confidence that a track is acoustic rather than electronically "
        "produced, 0 to 100."
    ),
    "tb_instrumentalness": (
        "Confidence that a track has no vocals, 0 to 100. Every song on "
        "this playlist is sung, so scores here reflect long instrumental "
        "passages rather than a fully instrumental track."
    ),
    "tb_liveness": (
        "Confidence that the recording captures a live performance in "
        "front of an audience, 0 to 100."
    ),
    "tb_speechiness": (
        "How much a track resembles spoken word rather than sung music, "
        "0 to 100."
    ),
    "tb_loudness": (
        "The track's overall loudness, averaged across its length, in "
        "decibels. Tunebat's scale runs roughly from -60 dB (very quiet) up "
        "to 0 dB, though a very loudly mastered track can go slightly above."
    ),
}

# Les 3 axes calculés par ACP : nom bipolaire, part de variance expliquée,
# description musicale des coefficients qui dominent chaque pôle, et une
# étiquette courte par pôle (positif, négatif) affichée aux deux extrémités
# de chaque axe dans le nuage 3D — ajoutée le 10 septembre 2026 pour que les
# axes s'y voient, ce qui n'était pas le cas dans la première version.
AXES = [
    {
        "name": "Loud and energetic ↔ hushed and acoustic",
        "variance": 33.6,
        "poles": ("loud, energetic", "hushed, acoustic"),
        "blurb": (
            "The single largest source of variation in this playlist. High "
            "values mean loud, energetic, upbeat and danceable; low values "
            "mean quiet and acoustic. It is the axis that separates a "
            "solo voice-and-guitar recording from a track at full club "
            "volume."
        ),
    },
    {
        "name": "Sung and danceable ↔ instrumental and fast",
        "variance": 16.2,
        "poles": ("sung, danceable", "instrumental, fast"),
        "blurb": (
            "One pole is fast-tempo and heavily instrumental; the other is "
            "slower, sung throughout and danceable. It sets tracks built "
            "around extended instrumental sections apart from vocal-forward, "
            "groove-driven ones."
        ),
    },
    {
        "name": "Live and spoken ↔ studio-sung",
        "poles": ("live, spoken", "studio-sung"),
        "variance": 12.2,
        "blurb": (
            "The most narrowly defined of the three: almost entirely "
            "liveness and speechiness. High values sound like a live take "
            "with a spoken or rapped cadence; low values sound like a sung "
            "vocal recorded in a studio."
        ),
    },
]

CLUSTERS = {
    1: {
        "name": "Club and dance-pop energy",
        "n": 46,
        "blurb": (
            "The highest average danceability and happiness of any group "
            "here, and the lowest average acousticness: upbeat, danceable "
            "productions built to move to."
        ),
        "means": {
            "tb_bpm": 121.7, "tb_energy": 76.0, "tb_danceability": 71.9,
            "tb_happiness": 63.5, "tb_acousticness": 8.1,
            "tb_instrumentalness": 1.0, "tb_liveness": 16.7,
            "tb_speechiness": 11.0, "tb_loudness": -5.8,
        },
    },
    2: {
        "name": "Low-key and moderate",
        "n": 44,
        "blurb": (
            "Moderate on every measure without standing out on any single "
            "one: more acoustic and less overtly upbeat than the dance-pop "
            "cluster, but nowhere near as hushed as the acoustic one. The "
            "playlist's broad middle ground, and its second-largest group."
        ),
        "means": {
            "tb_bpm": 114.9, "tb_energy": 56.9, "tb_danceability": 52.1,
            "tb_happiness": 32.1, "tb_acousticness": 26.5,
            "tb_instrumentalness": 1.2, "tb_liveness": 15.2,
            "tb_speechiness": 10.1, "tb_loudness": -8.2,
        },
    },
    3: {
        "name": "Fast and high-voltage",
        "n": 17,
        "blurb": (
            "By far the fastest average tempo of any group (167 BPM against "
            "a playlist median of 124), paired with high energy."
        ),
        "means": {
            "tb_bpm": 167.2, "tb_energy": 80.6, "tb_danceability": 48.9,
            "tb_happiness": 54.3, "tb_acousticness": 16.2,
            "tb_instrumentalness": 1.1, "tb_liveness": 24.1,
            "tb_speechiness": 10.4, "tb_loudness": -5.8,
        },
    },
    4: {
        "name": "Live-sounding and speech-forward",
        "n": 16,
        "blurb": (
            "Far and away the highest average liveness and speechiness: a "
            "spoken or rapped cadence, recorded with the ambience of a live "
            "take rather than a polished studio vocal."
        ),
        "means": {
            "tb_bpm": 122.1, "tb_energy": 77.0, "tb_danceability": 63.4,
            "tb_happiness": 54.7, "tb_acousticness": 14.8,
            "tb_instrumentalness": 6.2, "tb_liveness": 66.8,
            "tb_speechiness": 23.9, "tb_loudness": -5.9,
        },
    },
    5: {
        "name": "Acoustic and understated",
        "n": 13,
        "blurb": (
            "The most acoustic, least energetic and quietest group by a "
            "wide margin: its average acousticness score is more than ten "
            "times the playlist median."
        ),
        "means": {
            "tb_bpm": 107.0, "tb_energy": 23.8, "tb_danceability": 41.4,
            "tb_happiness": 25.0, "tb_acousticness": 88.8,
            "tb_instrumentalness": 2.5, "tb_liveness": 13.4,
            "tb_speechiness": 4.0, "tb_loudness": -12.4,
        },
    },
    6: {
        "name": "Extended instrumental passages",
        "n": 10,
        "blurb": (
            "A strikingly high average instrumentalness even though every "
            "track here has vocals: long instrumental intros, breakdowns or "
            "outros pull the average up. The smallest of the six groups, "
            "comfortably above the four-track floor set to keep an averaged "
            "profile from ever reading back as a single track's numbers."
        ),
        "means": {
            "tb_bpm": 137.2, "tb_energy": 75.1, "tb_danceability": 52.5,
            "tb_happiness": 35.5, "tb_acousticness": 10.1,
            "tb_instrumentalness": 73.4, "tb_liveness": 23.6,
            "tb_speechiness": 8.8, "tb_loudness": -7.3,
        },
    },
}

# Couleurs par cluster : palette Okabe-Ito, choisie pour rester distinguable
# en daltonisme. Une couleur par groupe, jamais réutilisée ailleurs sur le
# site.
#
# Révision du 10 septembre 2026 : la version précédente employait deux bleus
# de la palette (#56B4E9 et #0072B2, qui ne diffèrent que par la clarté) sur
# les groupes 2 et 5, proches l'un de l'autre dans l'espace ACP — illisibles
# ensemble d'après Claire. Un seul bleu est conservé désormais, et les six
# teintes sont réparties pour maximiser l'écart de teinte sur les paires de
# groupes les plus proches par distance de centroïde sur les 146 positions
# ACP (1-3 : 1,80 ; 3-6 : 1,48 ; 1-2 : 2,14 ; 2-3 : 2,06), ces quatre groupes
# se tenant nettement plus près les uns des autres que 4 et 5, plus isolés.
CLUSTER_COLORS = {
    1: "#56B4E9",  # bleu ciel
    2: "#E69F00",  # orange
    3: "#CC79A7",  # violet rosé
    4: "#F0E442",  # jaune
    5: "#D55E00",  # vermillon
    6: "#009E73",  # vert bleuté
}

# Position (ACP sur 3 axes) et groupe de chacun des 146 morceaux. Dérivé,
# pas brut : voir le docstring de ce fichier.
TRACKS = {
    '02L1ngagXNRt8W3Flbe9Sw': {'cluster': 5, 'pc': (-3.19, 0.32, 0.11)},
    '06kFuqzhMk4E6IYeO0sTfx': {'cluster': 4, 'pc': (2.00, -0.11, 1.06)},
    '07m5UbUHOQCofRK16k83Eg': {'cluster': 5, 'pc': (-2.82, 1.07, -0.19)},
    '0A2tFUYLertZLltvvY5uyr': {'cluster': 4, 'pc': (1.76, 0.55, 2.57)},
    '0DZapO0gUF8XZpk2bu8AeL': {'cluster': 2, 'pc': (-2.86, 0.14, -0.15)},
    '0GSW6V6GJc4xYi8c5jOu60': {'cluster': 1, 'pc': (1.28, -0.76, -1.34)},
    '0Irj6PuEEGzi7JGJvAhdZ8': {'cluster': 1, 'pc': (1.73, 0.44, -0.84)},
    '0NOume8OgBz4FCnP1QVr9A': {'cluster': 3, 'pc': (0.94, -0.14, -0.82)},
    '0QA1xpUuqHDHWZhi0eAbH7': {'cluster': 2, 'pc': (-3.12, 0.26, 1.18)},
    '0VNjaRcmIowjLbPtYDhLuh': {'cluster': 1, 'pc': (0.92, 1.70, -0.06)},
    '0VhGzYfT2ZOFz31b5IH7yJ': {'cluster': 2, 'pc': (-0.93, 0.46, -0.67)},
    '0XIutL5epZuYV91bhCfFsR': {'cluster': 1, 'pc': (0.15, 0.67, -1.00)},
    '0ZQLRkRyn3300WyapdPoWT': {'cluster': 4, 'pc': (1.91, 0.85, 2.04)},
    '0a0CwJBn8lmT5ifk63EUbP': {'cluster': 3, 'pc': (0.92, -2.54, 0.37)},
    '0bWpWsvZeTTNLQ9nuXqKIN': {'cluster': 4, 'pc': (0.02, -0.77, 2.71)},
    '0gm0OruZdJlu8jamJe5OCh': {'cluster': 3, 'pc': (1.73, -0.08, 1.09)},
    '0kNjtDBxrpjJTZn9w5Eq3C': {'cluster': 2, 'pc': (-1.82, -0.09, -0.31)},
    '0pe5NUU9uGwFpj637ot84D': {'cluster': 1, 'pc': (2.01, 0.06, -0.88)},
    '0rK7QTyYjhPFadLH2YDl84': {'cluster': 2, 'pc': (-0.95, 0.21, -0.40)},
    '0wIpjjcXFgGtJUmBIRAAju': {'cluster': 1, 'pc': (0.91, -0.02, -1.26)},
    '14uL43Gg4ujizaATehrryk': {'cluster': 6, 'pc': (0.45, -1.55, -0.28)},
    '18QS9wnUr7DOhMb73monpK': {'cluster': 1, 'pc': (1.47, 0.64, -1.03)},
    '1AFPmwB6mGMCcMI2hFh7c8': {'cluster': 1, 'pc': (1.68, 1.20, -0.17)},
    '1AHPsqF3EtHeWpOM06Y3Y4': {'cluster': 5, 'pc': (-3.91, -0.34, 0.66)},
    '1EPYnBjYhYHcNthEnVWk18': {'cluster': 4, 'pc': (2.12, -0.25, 0.24)},
    '1IF61ped0XehHvw2CFXP3B': {'cluster': 2, 'pc': (0.37, -0.92, -0.70)},
    '1N1F6UsRGILux57U0YbxJQ': {'cluster': 4, 'pc': (-1.76, -1.79, 2.68)},
    '1OpCGPKSq4IfpvLptsSMR9': {'cluster': 5, 'pc': (-4.66, 0.48, 0.86)},
    '1PEPcLm2QEo0HCRIhQjPq1': {'cluster': 1, 'pc': (0.21, 2.27, -0.89)},
    '1QrL7ucS71Ih4HXBOsuajv': {'cluster': 5, 'pc': (-3.13, 0.41, 1.08)},
    '1RXkdiCc4TtwPacmIKyUnX': {'cluster': 1, 'pc': (-0.08, 1.03, -0.12)},
    '1RkB4Dk0CDzpaSySq91JEA': {'cluster': 1, 'pc': (0.45, 1.78, 0.68)},
    '1RmXibCbfLIVrN8ZRdoYbW': {'cluster': 3, 'pc': (0.24, -0.35, -1.20)},
    '1XD4K4CGAKTIBmFpvuaFru': {'cluster': 3, 'pc': (0.91, -0.71, -0.42)},
    '1YsFdaP9QG9NhjYS3o0g5P': {'cluster': 1, 'pc': (2.07, 1.48, -0.24)},
    '1d3hBkCcMvVzsZjaMiVvNs': {'cluster': 2, 'pc': (-0.94, -0.23, -0.05)},
    '1huN927tTdSiwF90FBHXkT': {'cluster': 1, 'pc': (1.62, 0.63, -0.49)},
    '1jFN0stMzLepoPxvPywGZj': {'cluster': 1, 'pc': (1.52, 1.63, -0.10)},
    '1ovz0bZeO5YTBQTXIFf5Am': {'cluster': 5, 'pc': (-4.71, -0.30, 0.68)},
    '1toNKayLMeCcVlsLGXJl7n': {'cluster': 3, 'pc': (0.45, -1.11, -0.81)},
    '1w0AFg23E67l57A3RMiXjC': {'cluster': 6, 'pc': (2.40, -3.31, 0.61)},
    '20JYh6XUjLjiN1CyJ32ZiY': {'cluster': 6, 'pc': (2.67, -0.83, 0.08)},
    '29Ga6IgetN8Xah85ZHZ8AC': {'cluster': 1, 'pc': (1.72, -0.71, -0.85)},
    '2BQZhUPXdP9Nk1X84c7PtP': {'cluster': 2, 'pc': (-1.32, -1.86, -0.44)},
    '2CznvTOsuLh0USpHJqEc6V': {'cluster': 2, 'pc': (-0.66, -1.45, -0.39)},
    '2DUAIlPmzV2is5OQIZASUA': {'cluster': 2, 'pc': (-2.42, -0.49, 0.01)},
    '2Ff6Ghw8TRJGuAbJamtt4X': {'cluster': 2, 'pc': (-0.80, 0.94, -0.81)},
    '2KryklrVDGmWL8IvoGNbb5': {'cluster': 1, 'pc': (0.36, 1.41, -0.92)},
    '2Of9piZALXa4CC7Unxoeeg': {'cluster': 1, 'pc': (0.78, 1.43, -1.19)},
    '2fB0l9upVjg0QTeMyrIVtc': {'cluster': 2, 'pc': (-1.04, 0.29, -0.39)},
    '2gmwvGC1yOw8NdMcZE8nfo': {'cluster': 1, 'pc': (2.01, 0.66, -0.49)},
    '2inX5xyazBvcZYLx3wRBwh': {'cluster': 3, 'pc': (0.96, -2.86, 1.12)},
    '2iqTYCPRTqojxM7QJvBtk2': {'cluster': 2, 'pc': (-1.59, 1.51, -0.20)},
    '2jFP4mAHcDmGe7DEKKLyJa': {'cluster': 2, 'pc': (-0.66, 0.59, -0.72)},
    '2lgwylOpGMtkvhwdnUOArt': {'cluster': 1, 'pc': (1.81, 0.49, -0.51)},
    '2qpx5shtNEO1DuK8iEoJoB': {'cluster': 1, 'pc': (-0.14, 0.25, -0.59)},
    '2rN1ODOsaNfYu782rw36jR': {'cluster': 2, 'pc': (-0.26, 0.85, 0.03)},
    '2sVjF25Z4JTJxi9BXm5GtJ': {'cluster': 3, 'pc': (1.35, -2.15, -0.56)},
    '376mhFeloWqzQJQsqZpm9A': {'cluster': 1, 'pc': (1.04, 0.61, -1.25)},
    '37OSQm8Gy5strUT24vn6ef': {'cluster': 2, 'pc': (0.93, -0.79, 1.02)},
    '3ApVA7ID6PkS0fGzNF4mFw': {'cluster': 5, 'pc': (-2.48, 0.02, -0.25)},
    '3BYSoeWlqUgIwfY77C8VgE': {'cluster': 4, 'pc': (0.67, 2.17, 2.39)},
    '3BqWvhPear6eKPwhwJRFpO': {'cluster': 2, 'pc': (-0.66, -0.03, -0.71)},
    '3FysLYckiMCMzjYLIgo45U': {'cluster': 4, 'pc': (1.68, 1.24, 2.72)},
    '3IDQXyHYuX2rdLnNfVzT3g': {'cluster': 2, 'pc': (-0.54, -0.64, -0.43)},
    '3MZjOGeXhpHbQ9ESMNFFnH': {'cluster': 5, 'pc': (-3.99, 0.57, 0.40)},
    '3QF7smzmw2WWm7M1jt2Rac': {'cluster': 4, 'pc': (2.06, 0.26, 1.61)},
    '3RLI8S7KpEZs4SqePGjM2R': {'cluster': 3, 'pc': (0.89, -1.16, -0.53)},
    '3RXajeZOzqXWrQwLDfTzKK': {'cluster': 2, 'pc': (-0.29, 0.94, 0.44)},
    '3ShIGvHRm0q9iIDowUMjls': {'cluster': 1, 'pc': (-1.23, 1.24, -0.22)},
    '3Vk1AHIh1CoiQzFroldMhO': {'cluster': 5, 'pc': (-3.81, 0.62, 0.59)},
    '3XdXixlx3MoVzfL7pu9hx6': {'cluster': 5, 'pc': (-2.96, 0.22, 0.05)},
    '3bnvoYUrPkgh0E3ZeYZ3me': {'cluster': 4, 'pc': (2.97, 0.48, 4.43)},
    '3eBY8aZZdWNnNhNbc8B0yp': {'cluster': 6, 'pc': (-1.53, -3.21, 0.83)},
    '3nxFYWNFG2qGYEuhEzomtO': {'cluster': 2, 'pc': (-1.57, 1.55, 2.00)},
    '3qBg6BeHJlGgwl5aCa09EC': {'cluster': 3, 'pc': (1.16, -0.41, 0.56)},
    '3r0gvoaAkWmLdJO4UUv94v': {'cluster': 6, 'pc': (-2.35, -3.13, 1.33)},
    '3z4KIXgkhLauhNP3ubB8cF': {'cluster': 2, 'pc': (-0.93, 0.72, -0.86)},
    '3zGmkzXqXsXYVlGzJFpgCW': {'cluster': 3, 'pc': (0.81, -0.57, -1.20)},
    '46uGvJVhYHOVRRNnRPbkYm': {'cluster': 3, 'pc': (0.94, -1.26, 0.14)},
    '48XnOS1vTyzqaPps0Dalzp': {'cluster': 1, 'pc': (-0.10, 1.30, -0.58)},
    '4CuivW1JgPauXPA4wYsf5K': {'cluster': 2, 'pc': (-1.63, 1.03, 0.02)},
    '4ED8r6i90zmUG4kfbiVoou': {'cluster': 1, 'pc': (0.09, 0.41, -0.94)},
    '4NYRtDYROQW2D2ctcylcri': {'cluster': 6, 'pc': (0.25, -3.02, 0.46)},
    '4OI2gBlHqyNks8cbIBIKYw': {'cluster': 1, 'pc': (0.42, 0.19, -0.72)},
    '4P9LdSPrnQl7KQwml4DUtq': {'cluster': 2, 'pc': (-0.80, 0.16, -0.42)},
    '4QnHaiWq1oJiTgMnRFE0q8': {'cluster': 1, 'pc': (0.64, 0.72, -1.19)},
    '4UfEEnq70NgLeq7NRfXPiD': {'cluster': 1, 'pc': (1.04, 0.68, 0.34)},
    '4WhyfhjZaX6AVjAZslQAFs': {'cluster': 1, 'pc': (1.93, 0.62, -0.35)},
    '4X6PkqzKUvWWKoq4YiiM1V': {'cluster': 1, 'pc': (1.52, -0.20, -0.77)},
    '4Ykmj47fulJ1FTeCXctW91': {'cluster': 2, 'pc': (-1.83, -0.18, -0.48)},
    '4Zhxtm6x56wEiRtSMAl28n': {'cluster': 2, 'pc': (0.96, 0.92, 0.32)},
    '4b1Y41U44kP7gzO7MUNGbe': {'cluster': 1, 'pc': (1.06, -0.57, -0.48)},
    '4dtyeDMnVKKo89QbbDtD5M': {'cluster': 3, 'pc': (0.03, -1.08, -1.19)},
    '4hceSKjrkDTO0nMKFcb3sj': {'cluster': 4, 'pc': (0.96, 0.28, 1.00)},
    '4lUlYGT5VvZWN3GBDIc9KT': {'cluster': 2, 'pc': (-0.79, 1.56, 0.47)},
    '4ltqfN12ohaVZdM6C45gMg': {'cluster': 2, 'pc': (-0.36, -1.06, -0.85)},
    '4xhYxKvAxtrRd83MiqOy29': {'cluster': 1, 'pc': (1.23, 1.17, -1.43)},
    '4yBfzgV6YA9dTKP8KUD35j': {'cluster': 1, 'pc': (1.78, -0.33, -0.95)},
    '51NYFGDXYKS4FkRqkw98hx': {'cluster': 1, 'pc': (1.79, 0.54, -1.13)},
    '54n3iwz9mr7yxZi1EOX1Mz': {'cluster': 1, 'pc': (0.95, 0.56, -0.51)},
    '56xBg5e9rfrFqcqa4llUw7': {'cluster': 2, 'pc': (-0.85, -0.60, -0.41)},
    '5Gp1fkuPV7CPtzKHfMH0kd': {'cluster': 2, 'pc': (0.26, -0.17, 0.53)},
    '5NnQ2xIeHDKc1B19rxfcV3': {'cluster': 4, 'pc': (-1.25, 0.01, 2.21)},
    '5P9EKJfOZtuwtTR5C5362i': {'cluster': 5, 'pc': (-3.99, -0.25, 0.39)},
    '5PMtJGEDIO0eIToF0YRUQ5': {'cluster': 2, 'pc': (-1.69, -0.39, -0.42)},
    '5WttRLHcZHhaIii5KwKh3Y': {'cluster': 1, 'pc': (-0.27, 0.06, -0.89)},
    '5dIPCgTEDagbcs5QGmni8V': {'cluster': 6, 'pc': (0.69, -2.06, -0.27)},
    '5dtUOwEmnDAzsdodWJk4DA': {'cluster': 2, 'pc': (-1.43, 0.68, -0.70)},
    '5e0ZXu358l51ckAZvai2Ef': {'cluster': 5, 'pc': (-2.81, 0.76, -0.08)},
    '5iAE3uBqaZm9aHUx9yy6a0': {'cluster': 4, 'pc': (4.12, -2.28, 1.94)},
    '5iTzaatezJzsUhX1QjT0Kp': {'cluster': 6, 'pc': (1.38, -2.97, -0.71)},
    '5l2zYkyTXtYa8xk965ofqD': {'cluster': 5, 'pc': (-4.84, 1.43, 0.92)},
    '5lz6U9dCYBmEY6oLrW22VE': {'cluster': 1, 'pc': (1.70, 1.08, 0.47)},
    '5nWecUJF2pytSxsSpylzZw': {'cluster': 1, 'pc': (0.84, 1.20, -1.34)},
    '5nnBHHzUDOGvdMBiXofB00': {'cluster': 2, 'pc': (-1.33, -0.22, -0.61)},
    '5pkemVhnBiIzMs2NLsXomQ': {'cluster': 1, 'pc': (1.22, -0.28, -0.59)},
    '5rOzcHIZaF038jMeHkUZR0': {'cluster': 2, 'pc': (-1.82, -1.77, 0.07)},
    '5srzGYocC4qYFvckQm5AfC': {'cluster': 1, 'pc': (0.54, 2.06, -0.51)},
    '6D7zTed8zrkuKBPca2AqSI': {'cluster': 1, 'pc': (2.03, 0.53, -0.83)},
    '6EjxYTyXiBzJz6PeOvPiou': {'cluster': 2, 'pc': (-1.82, 0.96, -0.40)},
    '6JGJdnIbq4UqKgzFaOIXwE': {'cluster': 6, 'pc': (-0.32, -2.58, -0.12)},
    '6JZfK4Z75nZm3VcZOVrpy0': {'cluster': 2, 'pc': (-2.08, -0.49, -0.15)},
    '6JrmHzxhaaavRtlXTOhm63': {'cluster': 2, 'pc': (0.46, 2.24, 1.34)},
    '6RJiY28t9jWpdy1JkUhNgK': {'cluster': 4, 'pc': (1.37, 1.14, 1.88)},
    '6WkiWn8bf8S29wSk0VwK7h': {'cluster': 2, 'pc': (-0.40, -1.30, -0.75)},
    '6XeW8fjwoAFQeQpYojPtVI': {'cluster': 3, 'pc': (1.49, -1.35, -0.01)},
    '6jiumfqTwOpXW6PDzsIBKl': {'cluster': 1, 'pc': (0.42, 0.72, -0.59)},
    '6yAc1rz1RXRlYJac99xusK': {'cluster': 3, 'pc': (0.62, -0.74, 0.37)},
    '71yN0yrHej3jhKXewbmtEh': {'cluster': 1, 'pc': (1.08, 0.43, -0.92)},
    '724utiMbqUfT1g3tqbfQYu': {'cluster': 3, 'pc': (0.79, -1.38, 0.26)},
    '73xUwV4DkcelY7seMyY0PY': {'cluster': 3, 'pc': (-0.80, -0.11, -0.93)},
    '75HFFq9W7Em0dTBG8QeGcT': {'cluster': 1, 'pc': (1.03, 0.22, -0.77)},
    '78iHtTxYIK2mD6oL6lXqFF': {'cluster': 4, 'pc': (2.12, 0.32, 0.15)},
    '7EPHu29KqhsGk4dZAjM0o4': {'cluster': 2, 'pc': (0.29, 2.76, -0.09)},
    '7GAI6zWpmst6dSfu1wIA1O': {'cluster': 6, 'pc': (-0.67, -1.42, -0.56)},
    '7KtbrK74NNA4ySRZ49DC7R': {'cluster': 2, 'pc': (-0.90, 0.61, -0.87)},
    '7bNgXJ9MgGG7xOkyz9SLOY': {'cluster': 1, 'pc': (1.94, 0.70, -1.19)},
    '7kvQptbfqq5b4MWRQOMrZC': {'cluster': 1, 'pc': (1.29, 0.02, -0.83)},
    '7l8D5tXUVsdq95VQWn034C': {'cluster': 2, 'pc': (-1.43, -0.85, -0.65)},
    '7lc4ue2LiSfYRaABxq4YkT': {'cluster': 4, 'pc': (3.25, 1.31, 3.53)},
    '7luHAaHXty1Nl3AcscZIDT': {'cluster': 2, 'pc': (0.10, -0.73, -0.27)},
    '7n7GrVTBmZMG4EULD5g0i3': {'cluster': 2, 'pc': (-0.20, 1.06, 1.56)},
    '7tktCNlB0877dhdPZSRb7T': {'cluster': 2, 'pc': (-1.90, -2.54, -0.20)},
    '7yeRNInEt2DOFYW0BkETEe': {'cluster': 1, 'pc': (1.25, 0.64, -1.14)},
    '7zBUh6s2Ca8eAURfnVHCTS': {'cluster': 2, 'pc': (0.43, -0.52, 1.17)},
}


def _primary(credit, artists_of):
    """Même règle que sur les autres pages : le premier nom crédité qui
    n'est pas une invitée sert de clé de regroupement par artiste."""
    names = artists_of(credit)
    leads = [n for n in names if ART[n][0] != "guest"]
    return leads[0] if leads else names[0]


def _cluster_tracks(cluster_id, artists_of):
    out = []
    for sid, title, credit in all_tracks():
        info = TRACKS.get(sid)
        if info and info["cluster"] == cluster_id:
            out.append({
                "id": sid, "title": title, "credit": credit,
                "primary": _primary(credit, artists_of),
            })
    return out


def _track_line(r, esc, slug):
    url = "https://open.spotify.com/track/" + r["id"]
    names = [n.strip() for n in r["credit"].split(",")]
    cr = " · ".join(
        f'<a class="{"guest" if ART[n][0] == "guest" else "lead"}" '
        f'href="index.html#{slug(n)}">{esc(n)}</a>' for n in names)
    # id="track-<spotify id>" : cible d'ancrage pour le clic sur un point du
    # nuage 3D, qui doit renvoyer au morceau lui-même et pas seulement à la
    # section de son groupe. Ajouté le 10 septembre 2026 à la demande de
    # Claire.
    return (f'<li id="track-{esc(r["id"])}"><a href="{esc(url)}" target="_blank" '
            f'rel="noopener">{esc(r["title"])}</a> <span class="cr">{cr}</span></li>')


def _cluster_results_html(tracks, esc, slug):
    by_artist = defaultdict(list)
    for r in tracks:
        by_artist[r["primary"]].append(r)
    blocks = []
    for name in sorted(by_artist, key=str.lower):
        rows = by_artist[name]
        blocks.append(
            f'<div class="atlas-artist"><h4><a href="index.html#{slug(name)}">'
            f'{esc(name)}</a></h4><ul class="atlas-tracks">'
            + "".join(_track_line(r, esc, slug) for r in rows)
            + '</ul></div>')
    return "".join(blocks)


def _cluster_tracklist_html(cluster_id, esc, slug, artists_of):
    """La liste des morceaux d'un groupe, repliée par défaut derrière un
    <details> natif plutôt qu'un bouton en JavaScript : elle reste ouvrable
    sans script, comme le reste de cette section, et le clic sur un point du
    nuage 3D peut l'ouvrir par simple assignation de `.open`. Arbitrage de
    Claire du 10 septembre 2026 : les listes encombraient la comparaison des
    six radar plots quand elles restaient dépliées par défaut."""
    tracks = _cluster_tracks(cluster_id, artists_of)
    results = _cluster_results_html(tracks, esc, slug)
    n = len(tracks)
    return (f'<details class="tracklist" id="tracklist-{cluster_id}">'
            f'<summary>Show {n} track{"s" if n != 1 else ""}</summary>'
            f'{results}</details>')


def _radar_svg(cluster_id, esc):
    """Radar plot statique (pas besoin de script : les moyennes ne changent
    pas au clic). Chaque axe est mis à l'échelle sur le min/max observé sur
    les 146 morceaux, pas sur celui du cluster, pour que les neuf formes
    restent comparables entre elles d'un cluster à l'autre."""
    means = CLUSTERS[cluster_id]["means"]
    color = CLUSTER_COLORS[cluster_id]
    n = len(FEATURES)
    # viewBox large et centre décalé : les libellés d'axe débordent hors du
    # nonagone (fine sur des mots comme "Instrum.") et ont besoin de marge de
    # chaque côté, faute de quoi le SVG les découpe silencieusement.
    cx, cy = 150.0, 120.0
    vb_w, vb_h = 300.0, 240.0
    r = 68.0

    def point(i, frac):
        angle = -math.pi / 2 + 2 * math.pi * i / n
        return (cx + r * frac * math.cos(angle), cy + r * frac * math.sin(angle))

    rings = []
    for frac in (0.25, 0.5, 0.75, 1.0):
        pts = " ".join(f"{x:.1f},{y:.1f}" for x, y in (point(i, frac) for i in range(n)))
        rings.append(f'<polygon points="{pts}" class="radar-grid"/>')

    axes = []
    labels = []
    poly_pts = []
    for i, (key, label, short, unit, lo, hi) in enumerate(FEATURES):
        x2, y2 = point(i, 1.0)
        axes.append(f'<line x1="{cx}" y1="{cy}" x2="{x2:.1f}" y2="{y2:.1f}" class="radar-axis"/>')
        angle = -math.pi / 2 + 2 * math.pi * i / n
        lx, ly = cx + (r + 18) * math.cos(angle), cy + (r + 18) * math.sin(angle)
        anchor = "middle"
        if math.cos(angle) > 0.35:
            anchor = "start"
        elif math.cos(angle) < -0.35:
            anchor = "end"
        dy = "0.9em" if math.sin(angle) > 0.35 else ("-0.3em" if math.sin(angle) < -0.35 else "0.35em")
        # <title> imbriqué : tooltip natif au survol, sans script, avec la
        # définition complète de la feature. Ajouté le 10 septembre 2026.
        labels.append(f'<text x="{lx:.1f}" y="{ly:.1f}" dy="{dy}" text-anchor="{anchor}" '
                       f'class="radar-label">{esc(short)}'
                       f'<title>{esc(label)}: {esc(FEATURE_INFO[key])}</title></text>')
        val = means[key]
        t = 0.0 if hi <= lo else max(0.0, min(1.0, (val - lo) / (hi - lo)))
        poly_pts.append(point(i, t))

    poly = " ".join(f"{x:.1f},{y:.1f}" for x, y in poly_pts)
    shape = (f'<polygon points="{poly}" fill="{color}" fill-opacity="0.28" '
             f'stroke="{color}" stroke-width="2"/>')
    dots = "".join(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="2.6" fill="{color}"/>' for x, y in poly_pts)

    name = esc(CLUSTERS[cluster_id]["name"])
    return (f'<svg class="radar" viewBox="0 0 {vb_w:.0f} {vb_h:.0f}" role="img" '
            f'aria-label="Radar plot for {name}">'
            + "".join(rings) + "".join(axes) + shape + dots + "".join(labels)
            + '</svg>')


def _radar_values_html(cluster_id, esc):
    """Trois colonnes depuis le 10 septembre 2026 : la feature, sa moyenne
    dans ce groupe, et sa moyenne sur l'ensemble de la playlist juste à côté
    — demandé par Claire pour lire l'écart d'un groupe directement, sans
    devoir se souvenir de la moyenne générale."""
    means = CLUSTERS[cluster_id]["means"]
    head = ('<div class="radar-row radar-head"><span class="rk"></span>'
            '<span class="rv">This group</span><span class="rp">Playlist</span></div>')
    rows = [head]
    for key, label, short, unit, lo, hi in FEATURES:
        v = means[key]
        p = PLAYLIST_MEANS[key]
        text = f"{v:g}{unit}" if unit else f"{v:g}"
        ptext = f"{p:g}{unit}" if unit else f"{p:g}"
        rows.append(
            f'<div class="radar-row"><span class="rk" title="{esc(FEATURE_INFO[key])}">'
            f'{esc(label)}</span><span class="rv">{esc(text)}</span>'
            f'<span class="rp">{esc(ptext)}</span></div>')
    return '<div class="radar-values">' + "".join(rows) + '</div>'


def _cluster_section(cluster_id, esc, slug, artists_of):
    c = CLUSTERS[cluster_id]
    color = CLUSTER_COLORS[cluster_id]
    tracklist = _cluster_tracklist_html(cluster_id, esc, slug, artists_of)
    return f"""
<section class="sonic-cluster" id="cluster-{cluster_id}">
<h3 class="cont"><span class="swatch" style="background:{color}"></span>
{esc(c['name'])} <span class="cnt">{c['n']} tracks</span></h3>
<p class="secblurb">{esc(c['blurb'])}</p>
<div class="radar-wrap">
{_radar_svg(cluster_id, esc)}
{_radar_values_html(cluster_id, esc)}
</div>
{tracklist}
</section>
"""


def _axis_html(esc):
    blocks = []
    for i, ax in enumerate(AXES, start=1):
        blocks.append(
            f'<div class="axis-card"><h4>Axis {i}: {esc(ax["name"])} '
            f'<span class="cnt">{ax["variance"]:.1f}% of the variation</span></h4>'
            f'<p>{esc(ax["blurb"])}</p></div>')
    return "".join(blocks)


def _feature_glossary_html(esc):
    """Section "The nine measurements", ajoutée le 10 septembre 2026 à la
    demande de Claire : les définitions étaient auparavant seulement en
    infobulle, nulle part lisibles d'un coup."""
    rows = []
    for key, label, short, unit, lo, hi in FEATURES:
        if key == "tb_bpm":
            scale = "no fixed scale; 71-203 BPM on this playlist"
        elif unit == "dB":
            scale = "theoretically about −60 dB to 0 dB"
        else:
            scale = "0 to 100"
        rows.append(
            f'<div class="feat-row"><span class="fk">{esc(label)}</span>'
            f'<span class="fs">{esc(scale)}</span>'
            f'<span class="fd">{esc(FEATURE_INFO[key])}</span></div>')
    return '<div class="feat-glossary">' + "".join(rows) + '</div>'


def _legend_html(esc):
    items = []
    for cid in sorted(CLUSTERS):
        c = CLUSTERS[cid]
        color = CLUSTER_COLORS[cid]
        items.append(
            f'<a class="legend-item" href="#cluster-{cid}" data-cluster="{cid}">'
            f'<span class="swatch" style="background:{color}"></span>'
            f'{esc(c["name"])} <span class="cnt">{c["n"]}</span></a>')
    return '<div class="sonic-legend" id="sonic-legend">' + "".join(items) + '</div>'


def _scene_json(artists_of):
    """Un seul bloc JSON, lu une fois au chargement par le script : il n'y a
    ici aucune représentation DOM équivalente à dupliquer (contrairement à
    tags.html, où le tableau HTML sert déjà de source de données), donc
    aucune raison de faire autrement."""
    rows = []
    for sid, title, credit in all_tracks():
        info = TRACKS.get(sid)
        if not info:
            continue
        rows.append({
            "id": sid,
            "t": title,
            "a": _primary(credit, artists_of),
            "c": info["cluster"],
            "p": list(info["pc"]),
        })
    return json.dumps(rows)


def _cluster_meta_json():
    return json.dumps({
        str(cid): {"name": CLUSTERS[cid]["name"], "color": CLUSTER_COLORS[cid]}
        for cid in CLUSTERS
    })


def _axes_json():
    """Étiquettes de pôle pour les 3 axes, lues par le script afin de rendre
    les axes visibles dans le nuage 3D. Ajouté le 10 septembre 2026 : la
    première version ne montrait aucun repère d'orientation dans la scène."""
    return json.dumps([{"pos": ax["poles"][0], "neg": ax["poles"][1]} for ax in AXES])


# Import map : OrbitControls et ConvexGeometry importent 'three' par son nom
# nu ("import ... from 'three'"), ce que seul un import map sait résoudre
# côté navigateur, sans étape de build.
IMPORTMAP = """
<script type="importmap">
{{
  "imports": {{
    "three": "https://cdn.jsdelivr.net/npm/three@{v}/build/three.module.js",
    "three/addons/": "https://cdn.jsdelivr.net/npm/three@{v}/examples/jsm/"
  }}
}}
</script>
""".format(v=THREE_VERSION)

# Le nuage 3D. Contrairement à tags.html, il n'y a pas de repli sans script
# qui vaille : un <noscript> le dit clairement, et les sections de chaque
# cluster plus bas (nuage radar, liste des morceaux) restent, elles,
# entièrement lisibles sans JavaScript.
SCRIPT = """
<script type="module">
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { ConvexGeometry } from 'three/addons/geometries/ConvexGeometry.js';

(function () {
  var mount = document.getElementById('sonic3d');
  if (!mount) return;
  var dataEl = document.getElementById('sonic-data');
  var metaEl = document.getElementById('cluster-meta');
  var axesEl = document.getElementById('sonic-axes');
  if (!dataEl || !metaEl) return;
  var rows = JSON.parse(dataEl.textContent);
  var meta = JSON.parse(metaEl.textContent);
  var axesMeta = axesEl ? JSON.parse(axesEl.textContent) : [];
  if (!rows.length) return;

  mount.querySelector('.sonic3d-noscript-msg').hidden = true;
  var canvasWrap = mount.querySelector('.sonic3d-canvas');
  canvasWrap.hidden = false;

  var W = canvasWrap.clientWidth, H = Math.round(W * 0.72);

  var scene = new THREE.Scene();
  var camera = new THREE.PerspectiveCamera(45, W / H, 0.1, 500);
  var renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
  renderer.setSize(W, H);
  canvasWrap.appendChild(renderer.domElement);

  var byCluster = {};
  var axisExtent = { x: 0.5, y: 0.5, z: 0.5 };
  rows.forEach(function (r) {
    (byCluster[r.c] = byCluster[r.c] || []).push(r);
    axisExtent.x = Math.max(axisExtent.x, Math.abs(r.p[0]));
    axisExtent.y = Math.max(axisExtent.y, Math.abs(r.p[1]));
    axisExtent.z = Math.max(axisExtent.z, Math.abs(r.p[2]));
  });

  var box = new THREE.Box3();
  var pointMeshes = [];
  var hullMeshes = [];
  var sphereGeo = new THREE.SphereGeometry(0.09, 14, 10);

  Object.keys(byCluster).forEach(function (cid) {
    var color = new THREE.Color((meta[cid] || {}).color || '#888');
    var group = new THREE.Group();
    group.userData.cluster = cid;
    var pts = [];
    byCluster[cid].forEach(function (r) {
      var v = new THREE.Vector3(r.p[0], r.p[1], r.p[2]);
      pts.push(v);
      box.expandByPoint(v);
      var mesh = new THREE.Mesh(sphereGeo, new THREE.MeshStandardMaterial({
        color: color, roughness: 0.5, metalness: 0.05
      }));
      mesh.position.copy(v);
      mesh.userData.track = r;
      group.add(mesh);
      pointMeshes.push(mesh);
    });
    // Volume englobant semi-transparent, un par cluster. ConvexGeometry
    // veut au moins 4 points non coplanaires ; tous nos clusters en ont
    // largement plus, mais on protège quand même contre une future
    // augmentation qui produirait un petit groupe dégénéré.
    if (pts.length >= 4) {
      try {
        var hullGeo = new ConvexGeometry(pts);
        var hull = new THREE.Mesh(hullGeo, new THREE.MeshBasicMaterial({
          color: color, transparent: true, opacity: 0.16,
          side: THREE.DoubleSide, depthWrite: false
        }));
        hull.userData.cluster = cid;
        group.add(hull);
        hullMeshes.push(hull);
      } catch (e) { /* groupe dégénéré : on garde les points, pas le volume */ }
    }
    scene.add(group);
  });

  // Axes de l'ACP, rendus visibles : un trait neutre par composante, du
  // négatif au positif, avec le pôle correspondant écrit à chaque bout.
  // Ajouté le 10 septembre 2026 : sans repère, la scène ne permettait pas de
  // s'orienter dans l'espace musical.
  var axisColor = 0x9992a0;
  var axisMat = new THREE.LineBasicMaterial({ color: axisColor, transparent: true, opacity: 0.55 });
  var axisEnds = [
    { a: new THREE.Vector3(-axisExtent.x * 1.08, 0, 0), b: new THREE.Vector3(axisExtent.x * 1.08, 0, 0) },
    { a: new THREE.Vector3(0, -axisExtent.y * 1.08, 0), b: new THREE.Vector3(0, axisExtent.y * 1.08, 0) },
    { a: new THREE.Vector3(0, 0, -axisExtent.z * 1.08), b: new THREE.Vector3(0, 0, axisExtent.z * 1.08) }
  ];
  axisEnds.forEach(function (seg) {
    var geo = new THREE.BufferGeometry().setFromPoints([seg.a, seg.b]);
    scene.add(new THREE.Line(geo, axisMat));
  });
  var axisLabelEls = [];
  axisEnds.forEach(function (seg, i) {
    var poles = axesMeta[i] || { pos: 'PC' + (i + 1) + ' +', neg: 'PC' + (i + 1) + ' −' };
    [[seg.b, poles.pos], [seg.a, poles.neg]].forEach(function (pair) {
      var el = document.createElement('div');
      el.className = 'axis-label';
      el.textContent = pair[1];
      mount.appendChild(el);
      axisLabelEls.push({ el: el, pos: pair[0] });
    });
  });

  scene.add(new THREE.AmbientLight(0xffffff, 0.8));
  var dl = new THREE.DirectionalLight(0xffffff, 0.6);
  dl.position.set(4, 6, 8);
  scene.add(dl);

  var center = box.getCenter(new THREE.Vector3());
  var size = box.getSize(new THREE.Vector3());
  var dist = Math.max(size.x, size.y, size.z, 1) * 1.15;
  camera.position.set(center.x + dist * 0.6, center.y + dist * 0.4, center.z + dist);
  camera.lookAt(center);

  var controls = new OrbitControls(camera, renderer.domElement);
  controls.target.copy(center);
  controls.enableDamping = true;
  controls.dampingFactor = 0.08;
  controls.update();

  var raycaster = new THREE.Raycaster();
  var tooltip = mount.querySelector('.sonic3d-tooltip');
  var projected = new THREE.Vector3();

  function toScreen(worldPos) {
    projected.copy(worldPos).project(camera);
    return {
      x: (projected.x * 0.5 + 0.5) * W,
      y: (-projected.y * 0.5 + 0.5) * H,
      z: projected.z
    };
  }

  // Repérage par distance à l'écran plutôt que par intersection 3D exacte :
  // corrigé le 10 septembre 2026. Les sphères mesurent 0.09 unité de rayon,
  // ce qui les rend minuscules et quasiment impossibles à viser au pixel
  // près une fois projetées ; un seuil en pixels les rend faciles à
  // atteindre, comme des points de nuage de dispersion classiques.
  var PICK_PX = 15;
  function pickPoint(clientX, clientY) {
    var rect = renderer.domElement.getBoundingClientRect();
    var px = clientX - rect.left, py = clientY - rect.top;
    var best = null, bestDist = PICK_PX;
    pointMeshes.forEach(function (mesh) {
      if (!mesh.parent.visible) return;
      var s = toScreen(mesh.position);
      if (s.z < -1 || s.z > 1) return;
      var dx = s.x - px, dy = s.y - py;
      var d = Math.sqrt(dx * dx + dy * dy);
      if (d < bestDist) { bestDist = d; best = mesh; }
    });
    return best;
  }

  function pickHull(clientX, clientY) {
    var rect = renderer.domElement.getBoundingClientRect();
    var mouse = new THREE.Vector2(
      ((clientX - rect.left) / rect.width) * 2 - 1,
      -((clientY - rect.top) / rect.height) * 2 + 1
    );
    raycaster.setFromCamera(mouse, camera);
    var visible = hullMeshes.filter(function (h) { return h.parent.visible; });
    var hits = raycaster.intersectObjects(visible);
    return hits.length ? hits[0].object.userData.cluster : null;
  }

  // Ouvre la liste (repliée par défaut) du groupe d'un morceau et met le
  // morceau en évidence : c'est ce que le clic sur un point déclenche
  // désormais, plutôt que de renvoyer seulement à la section du groupe.
  function openTrack(cid, trackId) {
    var details = document.getElementById('tracklist-' + cid);
    if (details) details.open = true;
    var row = document.getElementById('track-' + trackId);
    var target = row || document.getElementById('cluster-' + cid);
    if (!target) return;
    target.scrollIntoView({ behavior: 'smooth', block: 'center' });
    if (row) {
      row.classList.add('track-flash');
      setTimeout(function () { row.classList.remove('track-flash'); }, 1800);
    }
  }

  renderer.domElement.addEventListener('pointermove', function (e) {
    var hit = pickPoint(e.clientX, e.clientY);
    if (hit) {
      var t = hit.userData.track;
      var name = (meta[t.c] || {}).name || ('Cluster ' + t.c);
      tooltip.innerHTML = '<strong>' + t.t + '</strong><br>' + t.a + '<br><em>' + name + '</em>';
      tooltip.style.left = e.clientX - mount.getBoundingClientRect().left + 14 + 'px';
      tooltip.style.top = e.clientY - mount.getBoundingClientRect().top + 10 + 'px';
      tooltip.hidden = false;
      renderer.domElement.style.cursor = 'pointer';
    } else {
      tooltip.hidden = true;
      renderer.domElement.style.cursor = 'grab';
    }
  });
  renderer.domElement.addEventListener('pointerleave', function () { tooltip.hidden = true; });
  renderer.domElement.addEventListener('click', function (e) {
    var hit = pickPoint(e.clientX, e.clientY);
    if (hit) {
      openTrack(hit.userData.track.c, hit.userData.track.id);
      return;
    }
    // Rien sous le pixel exact du clic : un clic sur le volume colorisé,
    // hors d'un point précis, renvoie seulement à la section du groupe.
    var cid = pickHull(e.clientX, e.clientY);
    if (cid) {
      var el = document.getElementById('cluster-' + cid);
      if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  });

  // Légende : clic pour isoler/réafficher un cluster dans la scène plutôt
  // que de filtrer quoi que ce soit (la légende reste aussi un lien
  // d'ancrage classique, qui marche sans JavaScript).
  var legend = document.getElementById('sonic-legend');
  if (legend) {
    legend.querySelectorAll('.legend-item').forEach(function (a) {
      a.addEventListener('click', function (e) {
        var cid = a.getAttribute('data-cluster');
        var group = scene.children.find(function (g) { return g.userData && g.userData.cluster === cid; });
        if (!group) return;
        e.preventDefault();
        var willHide = group.visible;
        group.visible = !willHide;
        a.classList.toggle('legend-off', willHide);
      });
    });
  }

  window.addEventListener('resize', function () {
    W = canvasWrap.clientWidth;
    H = Math.round(W * 0.72);
    camera.aspect = W / H;
    camera.updateProjectionMatrix();
    renderer.setSize(W, H);
  });

  (function animate() {
    requestAnimationFrame(animate);
    controls.update();
    axisLabelEls.forEach(function (a) {
      var s = toScreen(a.pos);
      // Un pôle d'axe peut passer très près de la caméra selon l'angle de
      // vue, et sa projection en pixels s'emballer même si sa profondeur
      // reste dans les bornes du frustum : masquer hors d'une marge autour
      // du canevas plutôt que de laisser une étiquette pousser la largeur de
      // la page. Corrigé le 10 septembre 2026 (débordement horizontal
      // observé à largeur mobile). Le calcul ne porte que sur le centre de
      // l'étiquette (transform:translate(-50%,-50%) en CSS) : sa moitié de
      // largeur peut encore dépasser cette marge de quelques pixels près du
      // bord, d'où le overflow:hidden posé sur #sonic3d en filet de
      // sécurité — une étiquette qui déborde du cadre est coupée plutôt que
      // d'élargir la page.
      var margin = 60;
      var onScreen = s.z >= -1 && s.z <= 1 &&
        s.x > -margin && s.x < W + margin && s.y > -margin && s.y < H + margin;
      a.el.style.display = onScreen ? 'block' : 'none';
      if (onScreen) {
        a.el.style.left = s.x + 'px';
        a.el.style.top = s.y + 'px';
      }
    });
    renderer.render(scene, camera);
  })();
})();
</script>
"""

CSS = """
.sonic-legend{display:flex;flex-wrap:wrap;gap:8px 14px;margin:14px 0 8px;
 font-family:ui-sans-serif,system-ui,-apple-system,sans-serif;font-size:.85rem}
.legend-item{display:inline-flex;align-items:center;gap:7px;color:var(--ink);
 text-decoration:none;padding:3px 4px;border-radius:5px}
.legend-item:hover{background:var(--soft)}
.legend-item.legend-off{opacity:.4}
.legend-item .cnt{color:var(--muted)}
.swatch{width:13px;height:13px;border-radius:3px;display:inline-block;flex:none;
 outline:1px solid var(--line);outline-offset:-1px}
#sonic3d{margin:18px 0 8px;position:relative;overflow:hidden}
.sonic3d-canvas{width:100%;border-radius:10px;overflow:hidden;background:var(--soft);
 border:1px solid var(--line);position:relative;line-height:0}
.sonic3d-canvas canvas{display:block;width:100%!important;cursor:grab}
.sonic3d-tooltip{position:absolute;pointer-events:none;background:var(--panel);
 border:1px solid var(--line);border-radius:7px;padding:6px 10px;font-size:.82rem;
 font-family:ui-sans-serif,system-ui,-apple-system,sans-serif;box-shadow:0 4px 14px rgba(0,0,0,.18);
 max-width:220px;line-height:1.4}
.axis-label{position:absolute;pointer-events:none;font-size:.72rem;color:var(--muted);
 font-family:ui-sans-serif,system-ui,-apple-system,sans-serif;white-space:nowrap;
 transform:translate(-50%,-50%);background:var(--panel);border:1px solid var(--line);
 border-radius:99px;padding:1px 8px;opacity:.92}
.sonic3d-hint{font-size:.78rem;color:var(--muted);margin:6px 0 0;
 font-family:ui-sans-serif,system-ui,-apple-system,sans-serif}
.axis-card{background:var(--panel);border:1px solid var(--line);border-radius:9px;
 padding:14px 16px;margin:0 0 12px}
.axis-card h4{margin:0 0 6px;font-size:1rem;font-family:ui-sans-serif,system-ui,sans-serif;
 display:flex;flex-wrap:wrap;align-items:baseline;gap:8px}
.axis-card p{margin:0;max-width:none;font-size:.92rem}
.feat-glossary{border:1px solid var(--line);border-radius:9px;background:var(--panel);
 margin:0 0 28px;overflow:hidden}
.feat-row{display:grid;grid-template-columns:9em 11em 1fr;gap:4px 14px;padding:9px 14px;
 font-family:ui-sans-serif,system-ui,-apple-system,sans-serif;font-size:.85rem;
 border-bottom:1px solid var(--line)}
.feat-row:last-child{border-bottom:none}
.feat-row .fk{font-weight:600}
.feat-row .fs{color:var(--muted);font-variant-numeric:tabular-nums}
.feat-row .fd{color:var(--muted);max-width:none}
@media (max-width:640px){
 .feat-row{grid-template-columns:1fr;gap:2px}
 .feat-row .fs{order:-1}
}
.sonic-cluster{margin:40px 0 0;padding-top:8px}
.sonic-cluster h3.cont{display:flex;align-items:center;gap:9px}
.radar-wrap{display:flex;flex-wrap:wrap;align-items:center;gap:18px;margin:10px 0 14px}
svg.radar{width:280px;height:224px;flex:none}
.radar-grid{fill:none;stroke:var(--line);stroke-width:1}
.radar-axis{stroke:var(--line);stroke-width:1}
.radar-label{font-size:8.5px;fill:var(--muted);font-family:ui-sans-serif,system-ui,sans-serif}
.radar-values{display:grid;grid-template-columns:auto auto auto;gap:2px 14px;
 font-family:ui-sans-serif,system-ui,-apple-system,sans-serif;font-size:.85rem}
.radar-row{display:contents}
.radar-row .rk{color:var(--muted)}
.radar-row .rv{font-variant-numeric:tabular-nums;font-weight:600}
.radar-row .rp{font-variant-numeric:tabular-nums;color:var(--muted)}
.radar-row.radar-head .rv,.radar-row.radar-head .rp{font-weight:600;font-size:.76rem;
 color:var(--muted);text-transform:uppercase;letter-spacing:.03em}
.tracklist{margin:6px 0 0}
.tracklist summary{font-family:ui-sans-serif,system-ui,-apple-system,sans-serif;
 font-size:.82rem;border:1px solid var(--line);background:var(--panel);color:var(--muted);
 border-radius:99px;padding:.3em .9em;cursor:pointer;display:inline-block;list-style:none}
.tracklist summary::-webkit-details-marker{display:none}
.tracklist summary:hover{border-color:var(--accent);color:var(--accent)}
.tracklist[open] summary{margin-bottom:12px}
.track-flash{animation:sonic-flash 1.8s ease-out;border-radius:5px}
@keyframes sonic-flash{
 0%{background:var(--soft);box-shadow:0 0 0 3px var(--accent)}
 100%{background:transparent;box-shadow:0 0 0 0 transparent}
}
"""


def sonic_page(css, esc, slug, artists_of, aliases, same_person, badge,
               playlist, issues):
    n_tracks = len(TRACKS)
    scene_json = _scene_json(artists_of)
    cluster_meta_json = _cluster_meta_json()
    axes_json = _axes_json()
    legend = _legend_html(esc)
    axes_html = _axis_html(esc)
    glossary_html = _feature_glossary_html(esc)
    clusters_html = "".join(
        _cluster_section(cid, esc, slug, artists_of) for cid in sorted(CLUSTERS))

    nav = atlas._nav("sonic.html")

    # Ordre remanié le 10 septembre 2026, à la demande de Claire : les six
    # groupes remontent en tête (comparaison directe des radar plots, listes
    # de morceaux repliées par défaut), le nuage 3D et la description des
    # trois axes de l'ACP qui le sous-tendent descendent en fin de page.
    # Claire les juge plus difficiles à lire et moins riches en information
    # musicale que le classement en groupes, en partie parce que celui-ci se
    # fait sur les 9 dimensions complètes plutôt que sur les 3 seuls axes du
    # nuage, ce qui produit des volumes qui se chevauchent visuellement sans
    # rien perdre côté musical.
    body = f"""
<header>
<h1>By sonic profile</h1>
<p class="sub">The {n_tracks} songs on this playlist, positioned by how they
sound rather than how they are labelled, from audio features licensed from
Tunebat and reduced to three dimensions and six groups. No individual
track's raw feature values are published here or anywhere in this
repository: Tunebat's terms do not allow it. See the note at the bottom of
this page for exactly what is shown instead, and why.</p>
</header>

<h2>The nine measurements</h2>
<p class="secblurb">Nine Tunebat audio features go into everything on this
page. Hover a feature's name anywhere below for this same description.</p>
{glossary_html}

<h2>The six groups</h2>
<p class="secblurb">Computed by hierarchical clustering (Ward's method) on
all nine standardised features rather than on the three-axis reduction shown
further down, so nothing is lost at this step. Claire set two constraints
going in: at most six groups, so a 3D view of them could stay legible, and
at least four songs per group, so that no averaged profile could ever be
narrow enough to read back as a single track's numbers, though this was
never a serious risk of reconstructing individual Tunebat values in the
first place; a margin of safety costs nothing here. Sizes run from 10 to
46; no group needed to be merged into another to clear that floor. Each
radar plot is scaled to the same axis range across all six groups, so the
shapes are directly comparable to one another; each group's average sits
next to the same feature's average across the whole playlist, to read at
a glance how far a group departs from the middle of this playlist. A
group's full track list is folded by default: open "Show N tracks" under
its radar to see it.</p>
{clusters_html}

<h2>The cloud</h2>
<p class="secblurb">Each point is one song, positioned by its value on the
three axes described below and coloured by the group it belongs to. The
three grey lines are those axes, labelled at each end with the pole they
point towards. Drag to rotate, scroll to zoom, hover a point for its title.
Click a point to jump to it in its group's track list above, opening that
list if it is folded; click elsewhere on a coloured volume to jump to that
group's section instead. Click a name in the legend to hide or show that
group in the scene. This view is the hardest to read on the page and shows
less than the grouping above it: clustering was done on all nine features,
so groups that overlap visually here are still fully distinct in the
underlying data.</p>
{legend}
<div id="sonic3d">
<div class="sonic3d-canvas" hidden></div>
<p class="sonic3d-noscript-msg sonic3d-hint">The 3D cloud needs JavaScript
and WebGL. Every song is already listed, grouped and described above without
either.</p>
<div class="sonic3d-tooltip" hidden></div>
</div>
<p class="sonic3d-hint">Loaded from <a href="https://threejs.org/"
target="_blank" rel="noopener">three.js</a>, the only external library on
this site.</p>

<h2>The three dimensions</h2>
<p class="secblurb">The nine features above, standardised and reduced by
principal component analysis to the three axes drawn in the cloud. Together
they explain 62% of how the nine features vary across the playlist; the
remaining 38% is not shown, in the cloud or anywhere else on this page.</p>
{axes_html}

<div class="note">
<h4>What this page does and does not show</h4>
<p>The underlying audio-feature values for each track come from Tunebat,
collected by hand with Tunebat's permission. Tunebat's terms do not allow
republishing those values per track, so none are published here: not the
nine used in the analysis, not the four left out, and not the spreadsheet
they came from. What is published instead is derived from that data rather
than a copy of it: each track's position on the three axes above and which
of the six groups it falls into, plus, for each group, the average of each
feature taken over at least ten tracks, next to the same average across the
whole playlist. A three-axis position keeps 62% of the original
nine-dimension picture and cannot be inverted back to the original values;
a group average taken over ten or more tracks cannot be read back to any one
of them either.</p>
<p>Genre and style, as tagged by people, are on <a href="tags.html">the tags
page</a>. The two do not track each other closely: several of the groups
here mix tracks from multiple genre families on this site's own tag and
family groupings, held together by production choices, tempo or vocal
delivery rather than by scene or lineage. That mismatch is itself worth
seeing, which is the reason this page exists alongside the others rather
than restating them.</p>
<p>Adding songs to the playlist changes the average and spread of every
feature, which can shift the three-axis position and even the group of
songs already here, not only the new ones. Recomputing this page after an
addition is therefore a full recalculation over every track with usable
Tunebat data, not an append.</p>
</div>

<footer>
<p>Companion page to the Spotify playlist <a href="{playlist}" target="_blank" rel="noopener"><strong>Transfem chants</strong></a>. Every artist's stated gender identity, with its source, is on the <a href="index.html">sources page</a>; this page is about the sound only.</p>
<p class="colophon">Audio features licensed from <a href="https://tunebat.com/" target="_blank" rel="noopener">Tunebat</a>. Found an error in a title or credit? <a href="{issues}" target="_blank" rel="noopener">Open an issue</a>. To have an entry taken down, or to raise anything about a person's identity, use the <a href="takedown.html">private channel</a> instead.</p>
</footer>

<script type="application/json" id="sonic-data">{scene_json}</script>
<script type="application/json" id="cluster-meta">{cluster_meta_json}</script>
<script type="application/json" id="sonic-axes">{axes_json}</script>
"""

    full_css = css + CSS
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Transfem chants — by sonic profile</title>
<meta name="description" content="The {n_tracks} songs on Transfem chants, grouped by sound rather than by label, from Tunebat audio features reduced to three dimensions and six groups.">
<style>{full_css}</style>
{IMPORTMAP}
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
