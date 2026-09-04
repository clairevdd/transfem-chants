# Transfem chants — pages de sources

Pages compagnon de la playlist Spotify [**Transfem chants**](https://open.spotify.com/playlist/4rK80rB8ycyAUdIKX6FOIk).

Elles donnent, pour chaque artiste, l'identité de genre telle que l'artiste l'a
rendue publique et la source de cette affirmation, puis la même matière par pays,
par langue et par année de première parution. Elles sont en anglais et publiées
sur <https://clairevdd.github.io/transfem-chants>.

Les quatre pages sont autonomes : pas de police distante, pas de script, pas de
CDN. Elles fonctionnent hors ligne et suivent le thème clair ou sombre du
navigateur. Le tri du tableau chronologique se fait par boutons radio et ordre
CSS, dont les règles sont écrites au build.

- `index.html` — les sources, artiste par artiste
- `countries.html` — la même matière par pays, avec une carte du monde en aplats
- `languages.html` — la même matière par langue
- `years.html` — quand chaque morceau a existé pour la première fois, et de
  combien les métadonnées de streaming le déplacent

## Structure

| Fichier | Rôle |
|---|---|
| `data.py` | les artistes : statut, pays, langue, description, citation, source. **Fait foi pour l'identité.** |
| `years.py` | les dates : première parution, précision, nature, statut, source, date de contrôle, réserve. **Fait foi pour les dates.** |
| `tracks.py` | les morceaux, groupés par section |
| `style.css` | la feuille de style, inlinée dans les pages au build |
| `build.py` | génère les quatre pages ; porte les contrôles d'intégrité |
| `atlas.py` | construit `countries.html` et `languages.html` ; appelé par `build.py` |
| `chrono.py` | construit `years.html` ; appelé par `build.py` |
| `worldmap.py` | géométries des pays pour la carte, dérivées de pygal_maps_world |
| `index.html`, `countries.html`, `languages.html`, `years.html` | les pages publiées, **générées** : ne pas les éditer à la main |
| `ARTISTES.md` | export lisible de `data.py`, à consulter plutôt que de mémoire |

## Régénérer les pages

```sh
python3 build.py
```

Le build écrit les quatre pages. Il échoue si :

- un nom crédité dans `tracks.py` n'existe pas dans `data.py` ;
- un pays de `data.py` n'a pas de code ISO dans `atlas.py`, sans quoi il
  disparaîtrait silencieusement de la carte ;
- un morceau de `tracks.py` n'a pas d'entrée dans `years.py` ;
- `years.py` garde un morceau retiré de la playlist ;
- une ligne de `years.py` est `verified` sans source, sans date ou sans date de
  contrôle.

Il signale aussi les artistes présentes dans `data.py` sans morceau associé.

**Ajouter un pays** suppose donc d'ajouter son code ISO 3166-1 alpha-2 et son
continent dans le dictionnaire `COUNTRIES` de `atlas.py`.

## Ajouter un morceau

Trois gestes, dans cet ordre.

Si l'artiste n'est pas déjà dans `data.py`, l'y ajouter avec sa source. Puis une
ligne dans la section voulue de `tracks.py` :

```python
("73xUwV4DkcelY7seMyY0PY", "Lady on the Subway", "Beth Elliott"),
```

L'identifiant est les 22 caractères qui suivent `/track/` dans une URL Spotify.
**Il doit provenir d'une URL réellement ouverte, jamais être reconstitué.**

Puis une entrée dans `years.py`, sous le même identifiant, avec la date, sa
source et la date à laquelle cette source a été lue.

Enfin `python3 build.py`, et committer les pages avec le reste.

## Retirer un morceau

Deux gestes : la ligne de `tracks.py` **et** l'entrée de `years.py`. Le build
échoue si l'un des deux manque.

## Les quatre statuts

Les mêmes noms servent pour l'identité dans `data.py` et pour les dates dans
`years.py`.

| Statut | Libellé affiché | Sens |
|---|---|---|
| `verified` | verified | source ouverte et lue, affirmation explicite |
| `partial` | partial | source suggestive, unique ou tertiaire ; pas de déclaration à la première personne |
| `unresolved` | unresolved | cas ouvert, sources en conflit, détaillé sur la page |
| `guest` | featured | personne créditée sans être l'artiste principale |

Aucun statut ne monte d'un cran sans une nouvelle source lue. Un statut peut
descendre. Le doute se documente, il ne se lisse pas.

Deux champs de `years.py` portent le reste de la nuance : `kind` distingue une
première parution établie d'une simple borne (`earliest_known`, « aucune trace
avant cette date »), et `first_record` ne se remplit que lorsqu'une année
d'enregistrement est documentée **et différente** de la parution, pour rendre
visible l'écart entre le moment où une musique existe et le moment où elle
circule.

Les citations d'artistes sont reproduites mot pour mot, jamais reformulées, et
les identités sont nommées dans les termes de l'artiste plutôt que traduites.

## Signaler une erreur

[Ouvrir une issue](https://github.com/clairevdd/transfem-chants/issues). Les
demandes de retrait n'ont pas à être justifiées.
