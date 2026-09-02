# Transfem chants — page de sources

Page compagnon de la playlist Spotify [**Transfem chants**](https://open.spotify.com/playlist/4rK80rB8ycyAUdIKX6FOIk).

Elle donne, pour chaque artiste, l'identité de genre telle que l'artiste l'a
rendue publique, et la source de cette affirmation. La page est en anglais et
publiée sur <https://clairevdd.github.io/transfem-chants>.

`index.html` est autonome : pas de police distante, pas de script, pas de CDN.
Elle fonctionne hors ligne et suit le thème clair ou sombre du navigateur.

## Structure

| Fichier | Rôle |
|---|---|
| `data.py` | les artistes : statut, pays, langue, description, citation, source. **Fait foi.** |
| `tracks.py` | les morceaux, groupés par section |
| `style.css` | la feuille de style, inlinée dans la page au build |
| `build.py` | génère `index.html` à partir des trois précédents |
| `index.html` | la page publiée, **générée** : ne pas l'éditer à la main |
| `ARTISTES.md` | export lisible de `data.py`, à consulter plutôt que de mémoire |
| `PROJET-CLAUDE.md` | critères, règles de vérification, journal des exclusions |

## Régénérer la page

```sh
python3 build.py
```

Le build échoue si un nom crédité dans `tracks.py` n'existe pas dans `data.py`,
et signale les artistes présentes dans `data.py` sans morceau associé.

## Ajouter un morceau

Une seule ligne à insérer dans la section voulue de `tracks.py` :

```python
("5UmAcaY8TNcsIAfZO8mZYr", "1000", "Ptite Soeur"),
```

L'identifiant est les 22 caractères qui suivent `/track/` dans une URL Spotify.
**Il doit provenir d'une URL réellement ouverte, jamais être reconstitué.**

Si l'artiste n'est pas déjà dans `data.py`, l'y ajouter d'abord, avec sa source.
Puis relancer `python3 build.py` et committer `index.html` avec le reste.

## Les quatre statuts

| Statut | Libellé affiché | Sens |
|---|---|---|
| `verified` | verified | source ouverte et lue, affirmation explicite |
| `partial` | partial | source suggestive, pas de déclaration à la première personne |
| `unresolved` | unresolved | cas ouvert, détaillé dans « Unresolved cases » |
| `guest` | featured | personne créditée sans être l'artiste principale |

Aucun statut ne monte d'un cran sans une nouvelle source lue. Le doute se
documente, il ne se lisse pas.

Les citations d'artistes sont reproduites mot pour mot, jamais reformulées.
Voir `PROJET-CLAUDE.md` pour la règle complète et le journal des exclusions.

## Signaler une erreur

[Ouvrir une issue](https://github.com/clairevdd/transfem-chants/issues).
