# -*- coding: utf-8 -*-
"""Tags de genre/style/scène par morceau, pour la page tags.html.

Sources, par ordre : styles Discogs (`discogs_styles`), genres MusicBrainz
(union enregistrement + groupe, `mb_genres_union`), tags de genre Last.fm
(`lfm_tags_genre`). Les trois viennent d'API, contrairement à Bandcamp, qui
n'en a pas : Bandcamp est donc exclu ici, y compris pour les quelques
morceaux où un relevé manuel existe déjà, pour que la couverture reste
homogène à mesure que la playlist s'augmente plutôt que de dépendre de qui a
pensé à relever une page Bandcamp à la main.

TAGS : identifiant Spotify -> {'discogs': [...], 'musicbrainz': [...],
'lastfm': [...]}, chaque liste déjà passée par la fusion orthographique et les
trois filtres ci-dessous. Un morceau sans aucun tag dans les trois est
`unclassified` sur la page (13 sur 146) : c'est une absence de source, pas une
absence de genre, et la page le dit.

Granularité réelle des trois sources, à garder en tête en la lisant : Discogs
tague au niveau de la sortie ou de l'artiste, pas du morceau, d'où les mêmes
styles répétés sur plusieurs titres d'un même disque. Last.fm ne tient un tag
propre au morceau que pour une minorité des 146 ; le reste retombe sur les
tags de l'artiste entier.

Fusion des seuls doublons de pure graphie, jamais des synonymes conceptuels :
avant-garde/avantgarde, experimental hip hop/-hip-hop, hip hop/hip-hop,
hip-house/hip house, j-pop/jpop, nu disco/nu-disco, synth-pop/synth pop/
synthpop, v-pop/vpop. `rap` et `hip hop` restent deux tags distincts :
arbitrage de Claire, 10 septembre 2026.

Trois filtres, tous par égalité de chaîne exacte plutôt que par mot-clé dans
la chaîne, pour ne jamais toucher un nom de genre composé qui contient
lui-même l'un de ces mots :

- **Identité** (`IDENTITY_BLOCK`). Last.fm est une folksonomie libre, pas un
  vocabulaire de genre encadré : rien n'empêche quelqu'un d'y écrire un mot
  sur l'identité d'une personne plutôt que sur sa musique. Trois occurrences
  relevées le 10 septembre 2026 (« transwoman » et « transexual » sur
  Coccinelle, « woman » sur femtanyl/ISSBROKIE) en sont la preuve : cette page
  classe des morceaux, pas des personnes.
- **Géographie** (`GEO_BLOCK`), à la demande de Claire, 10 septembre 2026 :
  un nom de pays ou un gentilé nu (« ghana », « thailand », « sweden »,
  « french », « american »…) n'est pas un genre, sa source Last.fm est
  majoritairement non officielle, et il fait double emploi avec la page
  « by country » (ou « by language » pour un gentilé qui nomme surtout une
  langue). Un nom de genre composé qui contient un mot géographique reste en
  revanche en place s'il désigne une scène ou un genre reconnu comme tel plutôt
  que la seule origine de l'artiste : `chanson française`, `ottoman classical`,
  `turk sanat muzigi`/`tsm`, `volksmusik`, `j-pop`, `k-pop`, `v-pop`, `uk bass`,
  `brazilian funk`, `brazilian bass`, `funk brasileiro`, `funk mandelao`,
  `latin`, `latin electronic`, `latin pop`, `americana` sont tous conservés.
  Seul appel plus incertain de ce filtre : `french rap` est écarté malgré son
  statut de scène reconnue, parce qu'il ne fait ici que répéter langue et
  genre déjà présents ailleurs sur la page ; à rouvrir si Claire n'est pas
  d'accord.
- **Bruit** (`JUNK_BLOCK`), relevé en construisant ce fichier : des mots-clés
  Last.fm qui ne décrivent ni identité ni géographie mais autre chose —
  un pseudonyme (`slowsilver03`), une liste personnelle (`my top songs`,
  `played with i h8 it here`), un nom de classement ou d'émission
  (`offizielle charts`, `melodifestivalen`), une réaction subjective en
  allemand sur Romy Haag (`verrucht`, `unglaublich`, `unfassbar`, `himmlisch`,
  `so scharf`), le nom d'un autre artiste que Last.fm associe sans le dire
  (`booba` sur JEDET, `urias` sur les morceaux d'Urias elle-même), ou des
  fragments sans sens musical (`pa`, `3`, `hora` — ce dernier écarté par
  prudence : usage incertain, éventuellement une insulte en espagnol, sur un
  titre suédois où aucun des deux sens n'a de raison de figurer).
"""

IDENTITY_BLOCK = {
    "transwoman", "trans woman", "transexual", "transsexual", "transgender",
    "trans", "queer", "lgbt", "lgbtq", "lgbtqia", "nonbinary", "non-binary",
    "non binary", "gay", "lesbian", "bisexual", "woman", "women", "female",
    "ftm", "mtf", "cisgender", "cis", "genderqueer", "two spirit", "two-spirit",
}

GEO_BLOCK = {
    "angola", "argentina", "australia", "brazilian", "canada", "canadian",
    "french", "german", "ghana", "korean", "malaysia", "mexico",
    "puerto rico", "south african", "spain", "spanish", "sweden", "swedish",
    "thailand", "turkish", "united states", "american", "japanese",
    "french rap",
}

JUNK_BLOCK = {
    "3", "1–4 wochen", "offizielle charts", "melfest", "melodifestivalen",
    "melodifestivalen 2022", "my top songs", "pop court with manda m",
    "slowsilver03", "played with i h8 it here", "upcoming album 2022",
    "artist on cover", "verrucht", "unglaublich", "unfassbar", "himmlisch",
    "so scharf", "booba", "urias", "wsum 91.7 fm madison", "pa",
    "minneapolis", "freelance", "hora", "rpa",
}

TAGS = {
    '1ovz0bZeO5YTBQTXIFf5Am': {'discogs': [], 'musicbrainz': ['ambient', 'classical', 'downtempo', 'electronic', 'house', 'modern classical', 'musical'], 'lastfm': []},  # Daniela Vega — Ombra Mai Fu
    '5l2zYkyTXtYa8xk965ofqD': {'discogs': [], 'musicbrainz': ['classical'], 'lastfm': []},  # Tona Brown, Geraldine Boone — Dream Variations
    '1AHPsqF3EtHeWpOM06Y3Y4': {'discogs': ['art rock', 'avant-garde', 'alternative rock', 'ballad'], 'musicbrainz': ['alternative rock', 'experimental', 'folk rock', 'hip hop', 'indie rock', 'lo-fi', 'math rock', 'pop', 'pop rock', 'post-hardcore', 'punk', 'rock', 'rock and roll', 'space rock', 'stoner rock', 'turntablism'], 'lastfm': ['singer-songwriter', 'chamber pop', 'indie', 'alternative', 'folk']},  # Antony and the Johnsons, ANOHNI — Hope There’s Someone
    '5P9EKJfOZtuwtTR5C5362i': {'discogs': [], 'musicbrainz': ['ambient', 'classical', 'downtempo', 'electronic', 'house', 'modern classical', 'musical'], 'lastfm': []},  # Daniela Vega — Sposa Son Disprezzata
    '02L1ngagXNRt8W3Flbe9Sw': {'discogs': ['poetry', 'folk', 'folk rock'], 'musicbrainz': [], 'lastfm': ['folk', 'acoustic']},  # Namoli Brennet — Boy in a Dress
    '1OpCGPKSq4IfpvLptsSMR9': {'discogs': [], 'musicbrainz': ['classical'], 'lastfm': []},  # Tona Brown, Geraldine Boone — I, Too
    '1QrL7ucS71Ih4HXBOsuajv': {'discogs': ['son'], 'musicbrainz': [], 'lastfm': ['folk', 'acoustic', 'latin']},  # La Bruja de Texcoco — Laabe Muxhe
    '3nxFYWNFG2qGYEuhEzomtO': {'discogs': ['cumbia'], 'musicbrainz': [], 'lastfm': []},  # Susy Shock — Vidalita, Vidalita
    '5e0ZXu358l51ckAZvai2Ef': {'discogs': ['ottoman classical', 'volksmusik', 'éntekhno', 'folk'], 'musicbrainz': [], 'lastfm': ['turk sanat muzigi', 'tsm', 'diva']},  # Bülent Ersoy — Geceler
    '4Ykmj47fulJ1FTeCXctW91': {'discogs': ['v-pop', 'nhạc vàng', 'ballad', 'comedy'], 'musicbrainz': [], 'lastfm': ['v-pop']},  # Hương Giang — Anh Ta Bỏ Em Rồi
    '07m5UbUHOQCofRK16k83Eg': {'discogs': [], 'musicbrainz': [], 'lastfm': []},  # Shyraa Roy, Kashif Ali — Duniya
    '73xUwV4DkcelY7seMyY0PY': {'discogs': [], 'musicbrainz': [], 'lastfm': ['folk']},  # Beth Elliott — Lady on the Subway
    '4dtyeDMnVKKo89QbbDtD5M': {'discogs': [], 'musicbrainz': [], 'lastfm': ['folk']},  # Beth Elliott — Ballad of the Oklahoma Women’s Liberation Front
    '3BYSoeWlqUgIwfY77C8VgE': {'discogs': ['son'], 'musicbrainz': ['latin'], 'lastfm': ['folk', 'acoustic', 'latin']},  # La Bruja de Texcoco — Té de Malvón
    '7KtbrK74NNA4ySRZ49DC7R': {'discogs': ['country', 'alternative rock', 'folk', 'folk rock'], 'musicbrainz': [], 'lastfm': ['country', 'folk', 'americana', 'blues']},  # Mya Byrne — Where the Lavender Grows
    '0XIutL5epZuYV91bhCfFsR': {'discogs': ['ottoman classical', 'volksmusik', 'éntekhno', 'folk'], 'musicbrainz': [], 'lastfm': ['turk sanat muzigi', 'tsm', 'diva']},  # Bülent Ersoy — Ümit Hırsızı
    '3MZjOGeXhpHbQ9ESMNFFnH': {'discogs': ['folk', 'folk rock', 'vocal', 'indie pop'], 'musicbrainz': [], 'lastfm': ['steampunk', 'cabaret', 'folk', 'cabaret folk']},  # Steam Powered Giraffe — Honeybee
    '3ApVA7ID6PkS0fGzNF4mFw': {'discogs': ['hi nrg', 'disco', 'house', 'rnb/swing'], 'musicbrainz': [], 'lastfm': ['drag', 'rnb', 'electro']},  # Peppermint — A Girl Like Me
    '4CuivW1JgPauXPA4wYsf5K': {'discogs': ['chanson', 'vocal', 'music hall', 'disco'], 'musicbrainz': [], 'lastfm': ['cabaret', 'chanson française', 'madame arthur']},  # Coccinelle — Chercher la femme
    '5dtUOwEmnDAzsdodWJk4DA': {'discogs': ['soul', 'rhythm & blues'], 'musicbrainz': [], 'lastfm': ['soul', 'northern soul']},  # Jackie Shane — Any Other Way
    '5NnQ2xIeHDKc1B19rxfcV3': {'discogs': ['cabaret', 'cool jazz', 'vocal', 'smooth jazz'], 'musicbrainz': [], 'lastfm': ['pop']},  # Veronica Klaus — I Will Survive
    '0VhGzYfT2ZOFz31b5IH7yJ': {'discogs': ['chanson', 'pop rock', 'garage rock', 'punk'], 'musicbrainz': ['pop'], 'lastfm': ['punk']},  # Marie France, Chrissie Hynde — Un garçon qui pleure
    '4P9LdSPrnQl7KQwml4DUtq': {'discogs': ['mpb', 'rhythm & blues', 'latin pop', 'soul'], 'musicbrainz': ['mpb'], 'lastfm': ['soul', 'mpb', 'black music']},  # Liniker — Baby 95
    '56xBg5e9rfrFqcqa4llUw7': {'discogs': ['vocal', 'easy listening', 'soul-jazz', 'alternative rock'], 'musicbrainz': [], 'lastfm': ['drag queen', 'cabaret', 'drag performer']},  # Jinkx Monsoon — Just Me (The Gender Binary Blues)
    '5WttRLHcZHhaIii5KwKh3Y': {'discogs': ['alternative rock'], 'musicbrainz': [], 'lastfm': ['rnb', 'soul']},  # Shea Diamond — I Am Her
    '0rK7QTyYjhPFadLH2YDl84': {'discogs': [], 'musicbrainz': [], 'lastfm': []},  # Our Lady J — Picture of a Man
    '0gm0OruZdJlu8jamJe5OCh': {'discogs': ['alternative rock'], 'musicbrainz': [], 'lastfm': ['rnb', 'soul']},  # Shea Diamond — Keisha Complexion
    '3XdXixlx3MoVzfL7pu9hx6': {'discogs': ['experimental', 'bass music', 'reggaeton', 'deconstructed club'], 'musicbrainz': ['electronic', 'ambient', 'art pop', 'cumbia', 'deconstructed club', 'epic collage', 'experimental', 'experimental hip hop', 'glitch hop', 'glitch pop', 'idm', 'industrial hip hop', 'latin', 'leftfield', 'neoperreo', 'noise', 'pop', 'post-industrial', 'reggaeton', 'latin electronic', 'nsfw cover art'], 'lastfm': ['electronic', 'experimental', 'ambient', 'glitch', 'idm']},  # Arca — Time
    '0QA1xpUuqHDHWZhi0eAbH7': {'discogs': ['hyperpop', 'bass music', 'experimental', 'dance-pop'], 'musicbrainz': ['art pop', 'synth-pop', 'avant-garde', 'deconstructed club', 'electronic', 'experimental', 'hyperpop', 'pop', 'post-industrial', 'double album', 'uk bass'], 'lastfm': ['bubblegum bass', 'electronic', 'deconstructed club', 'experimental', 'uk bass', 'wonky', 'hyperpop']},  # SOPHIE — It’s Okay To Cry
    '6EjxYTyXiBzJz6PeOvPiou': {'discogs': ['j-pop', 'ballad'], 'musicbrainz': [], 'lastfm': ['jazz', 'j-pop']},  # Ataru Nakamura — きみがすきだよ
    '1N1F6UsRGILux57U0YbxJQ': {'discogs': [], 'musicbrainz': [], 'lastfm': []},  # Cindy Thái Tài — Giọt Tình
    '7l8D5tXUVsdq95VQWn034C': {'discogs': ['k-pop', 'house', 'rnb/swing', 'ballad'], 'musicbrainz': [], 'lastfm': ['k-pop']},  # Harisu — 애지몽
    '0DZapO0gUF8XZpk2bu8AeL': {'discogs': ['dance-pop', 'euro house', 'house'], 'musicbrainz': [], 'lastfm': []},  # Aderet — היו לילות
    '3r0gvoaAkWmLdJO4UUv94v': {'discogs': ['experimental', 'bass music', 'reggaeton', 'deconstructed club'], 'musicbrainz': ['ambient', 'electronic', 'experimental', 'leftfield', 'ambient pop', 'art pop', 'deconstructed club', 'deep house', 'ghettotech', 'glitch pop', 'hip hop', 'idm', 'jazz', 'pop', 'post-industrial', 'singer-songwriter', 'techno', 'abstract electronic'], 'lastfm': ['electronic', 'experimental', 'ambient', 'glitch', 'idm']},  # Arca — Desafío
    '2Ff6Ghw8TRJGuAbJamtt4X': {'discogs': ['alternative rock', 'indie pop', 'indie rock', 'electro'], 'musicbrainz': [], 'lastfm': ['dream pop', 'indie pop', 'guitar']},  # SuperKnova — Serotonin Serenade
    '48XnOS1vTyzqaPps0Dalzp': {'discogs': ['hyperpop', 'bass music', 'experimental', 'dance-pop'], 'musicbrainz': ['bubblegum bass', 'deconstructed club', 'avant-garde', 'electronic', 'experimental', 'hyperpop', 'pop', 'post-industrial', 'rock', 'double album', 'uk bass'], 'lastfm': ['bubblegum bass', 'deconstructed club', 'wonky', 'experimental', 'hyperpop']},  # SOPHIE — Ponyboy
    '7tktCNlB0877dhdPZSRb7T': {'discogs': ['hyperpop', 'bass music', 'experimental', 'dance-pop'], 'musicbrainz': ['art pop', 'avant-garde', 'deconstructed club', 'electronic', 'experimental', 'hyperpop', 'pop', 'post-industrial', 'double album', 'uk bass'], 'lastfm': ['bubblegum bass', 'electronic', 'deconstructed club', 'experimental', 'uk bass', 'wonky', 'hyperpop']},  # SOPHIE — Is It Cold In The Water?
    '6JZfK4Z75nZm3VcZOVrpy0': {'discogs': ['avant-garde', 'alternative rock', 'indie pop', 'vocal'], 'musicbrainz': [], 'lastfm': ['electronic', 'art pop', 'chamber pop', 'experimental']},  # ANOHNI — Drone Bomb Me
    '0kNjtDBxrpjJTZn9w5Eq3C': {'discogs': ['indie pop'], 'musicbrainz': ['indie rock', 'pop', 'rock'], 'lastfm': ['electropop', 'pop']},  # Vivek Shraya — I Take All the Blame
    '7EPHu29KqhsGk4dZAjM0o4': {'discogs': [], 'musicbrainz': [], 'lastfm': []},  # Stef Aranas — Cvnty
    '2fB0l9upVjg0QTeMyrIVtc': {'discogs': ['indie pop'], 'musicbrainz': ['pop', 'indie'], 'lastfm': ['electropop', 'pop']},  # Vivek Shraya, Queer Songbook Orchestra — Part-Time Woman
    '2rN1ODOsaNfYu782rw36jR': {'discogs': ['hyperpop', 'bass music', 'experimental', 'dance-pop'], 'musicbrainz': ['electronic', 'yassification'], 'lastfm': ['bubblegum bass', 'experimental', 'deconstructed club', 'hyperpop', 'wonky']},  # SOPHIE — Faceshopping
    '4lUlYGT5VvZWN3GBDIc9KT': {'discogs': ['experimental', 'bass music', 'reggaeton', 'deconstructed club'], 'musicbrainz': [], 'lastfm': ['electronic', 'experimental', 'ambient', 'glitch', 'idm']},  # Arca — Nonbinary
    '2KryklrVDGmWL8IvoGNbb5': {'discogs': ['african'], 'musicbrainz': [], 'lastfm': ['electronic']},  # Umlilo — Zulu Lami
    '5nnBHHzUDOGvdMBiXofB00': {'discogs': ['experimental', 'abstract', 'cumbia'], 'musicbrainz': [], 'lastfm': ['synth-pop', 'alternative', 'experimental', 'drone', 'art rock']},  # Luisa Almaguer — Exiliades
    '5rOzcHIZaF038jMeHkUZR0': {'discogs': ['experimental', 'bass music', 'reggaeton', 'deconstructed club'], 'musicbrainz': ['ambient pop', 'art pop', 'deconstructed club', 'electronic', 'experimental', 'glitch pop', 'idm', 'pop', 'post-industrial', 'singer-songwriter'], 'lastfm': ['electronic', 'experimental', 'ambient', 'glitch', 'idm']},  # Arca — Reverie
    '6jiumfqTwOpXW6PDzsIBKl': {'discogs': ['pop rock'], 'musicbrainz': [], 'lastfm': ['pop', 'electronic', 'indie pop', 'synth-pop', 'indie rock', 'pop rock']},  # Sonja Sajzor — I Keep Doing This to Myself
    '6JGJdnIbq4UqKgzFaOIXwE': {'discogs': ['experimental', 'abstract', 'cumbia'], 'musicbrainz': [], 'lastfm': ['synth-pop', 'alternative', 'experimental', 'drone', 'art rock']},  # Luisa Almaguer — Mataronomatar
    '0NOume8OgBz4FCnP1QVr9A': {'discogs': [], 'musicbrainz': [], 'lastfm': ['pop']},  # Bell Nuntita — Paradise
    '3z4KIXgkhLauhNP3ubB8cF': {'discogs': ['acoustic', 'alternative rock', 'indie rock', 'indie pop'], 'musicbrainz': ['folk', 'indie'], 'lastfm': ['indie', 'singer-songwriter', 'indie pop', 'alternative']},  # Left at London — 6 Feet
    '2BQZhUPXdP9Nk1X84c7PtP': {'discogs': ['experimental', 'ambient', 'alt-pop', 'baroque pop'], 'musicbrainz': [], 'lastfm': ['post-rock', 'chamber pop', 'electronic', 'art pop']},  # Lauren Auder, Celeste — Unseen (feat. Celeste)
    '2CznvTOsuLh0USpHJqEc6V': {'discogs': ['synth-pop', 'alt-pop', 'hyperpop', 'indie pop'], 'musicbrainz': [], 'lastfm': ['indie pop', 'electronic', 'synth-pop']},  # June Jones, Geryon — Motorcycle
    '3IDQXyHYuX2rdLnNfVzT3g': {'discogs': ['avant-garde', 'alternative rock', 'indie pop', 'vocal'], 'musicbrainz': ['art pop', 'electropop', 'avant-garde', 'glitch pop', 'idm'], 'lastfm': ['electronic', 'art pop', 'chamber pop', 'experimental']},  # ANOHNI — 4 DEGREES
    '1huN927tTdSiwF90FBHXkT': {'discogs': ['hyperpop', 'bass music', 'experimental', 'dance-pop'], 'musicbrainz': ['bubblegum bass', 'electropop', 'avant-garde', 'deconstructed club', 'electronic', 'experimental', 'hyperpop', 'indie pop', 'indie rock', 'pop', 'post-industrial', 'post-rock', 'rock', 'double album', 'uk bass'], 'lastfm': ['bubblegum bass', 'hyperpop', 'electropop', 'electronic']},  # SOPHIE — Immaterial
    '3qBg6BeHJlGgwl5aCa09EC': {'discogs': ['acoustic', 'alternative rock', 'indie rock', 'indie pop'], 'musicbrainz': ['folk', 'indie'], 'lastfm': ['indie', 'singer-songwriter', 'indie pop', 'alternative']},  # Left at London — Revolution Lover
    '6RJiY28t9jWpdy1JkUhNgK': {'discogs': ['experimental', 'bass music', 'reggaeton', 'deconstructed club'], 'musicbrainz': ['deconstructed club', 'electronic', 'ambient', 'art pop', 'cumbia', 'epic collage', 'experimental', 'experimental hip hop', 'glitch hop', 'glitch pop', 'idm', 'industrial hip hop', 'latin', 'leftfield', 'neoperreo', 'noise', 'pop', 'post-industrial', 'reggaeton', 'latin electronic', 'nsfw cover art'], 'lastfm': ['electronic', 'experimental', 'ambient', 'glitch', 'idm']},  # Arca — Mequetrefe
    '3Vk1AHIh1CoiQzFroldMhO': {'discogs': ['glam', 'goth rock', 'punk'], 'musicbrainz': [], 'lastfm': []},  # Venus De Mars — Take My Shoulder (feat. Laura Jane Grace)
    '2DUAIlPmzV2is5OQIZASUA': {'discogs': ['hyperpop', 'emo', 'alternative rock', 'indie rock'], 'musicbrainz': [], 'lastfm': ['digital hardcore', 'punk', 'breakcore', 'bounce hardcore']},  # Anita Velveeta — T4T
    '3ShIGvHRm0q9iIDowUMjls': {'discogs': ['acoustic', 'punk', 'folk', 'alternative rock'], 'musicbrainz': ['alternative rock', 'folk rock', 'indie rock', 'lo-fi', 'rock'], 'lastfm': ['folk punk', 'punk rock', 'singer-songwriter', 'punk']},  # Laura Jane Grace — The Best Ever Death Metal Band in Denton
    '2jFP4mAHcDmGe7DEKKLyJa': {'discogs': ['alternative rock', 'folk', 'indie rock'], 'musicbrainz': ['alternative rock', 'indie rock', 'rock'], 'lastfm': ['singer-songwriter', 'indie', 'folk']},  # jasmine.4.t — Skin On Skin
    '7GAI6zWpmst6dSfu1wIA1O': {'discogs': [], 'musicbrainz': [], 'lastfm': []},  # Venus de Mars and All the Pretty Horses — White Horses
    '3RXajeZOzqXWrQwLDfTzKK': {'discogs': ['acoustic', 'emo', 'hyperpop', 'indie pop'], 'musicbrainz': [], 'lastfm': ['hyperpop', 'punk', 'emo']},  # THÉA — JUSTE AMIS
    '0bWpWsvZeTTNLQ9nuXqKIN': {'discogs': ['acoustic', 'emo', 'hyperpop', 'indie pop'], 'musicbrainz': ['electropop', 'hyperpop', 'techno', 'trap'], 'lastfm': ['hyperpop', 'punk', 'emo']},  # THÉA — Guillotine
    '3zGmkzXqXsXYVlGzJFpgCW': {'discogs': [], 'musicbrainz': [], 'lastfm': []},  # Venus de Mars and All the Pretty Horses — Boys
    '4ltqfN12ohaVZdM6C45gMg': {'discogs': ['indie rock', 'ambient', 'ethereal', 'experimental'], 'musicbrainz': ['americana', 'dream pop', 'heartland rock', 'indie rock', 'pop rock', 'synth-pop', 'big music'], 'lastfm': ['dream pop', 'heartland rock', 'pop rock']},  # Ethel Cain — American Teenager
    '14uL43Gg4ujizaATehrryk': {'discogs': ['techno', 'broken beat', 'hardcore', 'sound collage'], 'musicbrainz': ['alternative rock', 'folk punk', 'pop rock', 'punk', 'rock', 'punk rock', 'rock and indie'], 'lastfm': ['punk', 'punk rock', 'folk punk', 'rock']},  # Against Me! — The Ocean
    '7zBUh6s2Ca8eAURfnVHCTS': {'discogs': ['acoustic', 'emo', 'hyperpop', 'indie pop'], 'musicbrainz': [], 'lastfm': ['hyperpop', 'punk', 'emo']},  # THÉA — ANXIOLYTIQUES
    '3bnvoYUrPkgh0E3ZeYZ3me': {'discogs': ['dark electro', 'horrorcore', 'trap', 'pop rap'], 'musicbrainz': [], 'lastfm': ['trap metal', 'rap', 'hip hop']},  # Changeline — OCTOPUS.LADY
    '7lc4ue2LiSfYRaABxq4YkT': {'discogs': ['dark electro', 'horrorcore', 'trap', 'pop rap'], 'musicbrainz': [], 'lastfm': ['trap metal', 'rap', 'hip hop']},  # Changeline — JE.DÉTESTE.LA.FRANCE.pt1 (il y aura pas de pt2)
    '0wIpjjcXFgGtJUmBIRAAju': {'discogs': ['techno', 'broken beat', 'hardcore', 'sound collage'], 'musicbrainz': ['punk', 'rock'], 'lastfm': ['punk', 'punk rock', 'folk punk', 'rock']},  # Against Me! — Black Me Out
    '2inX5xyazBvcZYLx3wRBwh': {'discogs': [], 'musicbrainz': [], 'lastfm': ['indie', 'punk']},  # Tingtongketz — Berubah
    '0ZQLRkRyn3300WyapdPoWT': {'discogs': ['acoustic', 'emo', 'hyperpop', 'indie pop'], 'musicbrainz': ['hyperpop'], 'lastfm': ['hyperpop', 'punk', 'emo']},  # THÉA — CAVALE! CAVALE!
    '4NYRtDYROQW2D2ctcylcri': {'discogs': ['progressive house', 'progressive trance', 'pop rock', 'punk'], 'musicbrainz': [], 'lastfm': ['hardcore punk', 'hardcore', 'punk', 'queercore', 'd-beat']},  # G.L.O.S.S. — Targets of Men Targets of Men
    '1IF61ped0XehHvw2CFXP3B': {'discogs': ['punk', 'rock & roll', 'euro house', 'house'], 'musicbrainz': [], 'lastfm': ['punk', 'punk rock', 'garage rock', 'rock']},  # Jayne County — Man Enough To Be A Woman
    '7yeRNInEt2DOFYW0BkETEe': {'discogs': ['indie rock', 'rock & roll', 'blues rock', 'alternative rock'], 'musicbrainz': ['indie rock', 'rock', 'indie'], 'lastfm': ['indie rock', 'rock', 'folk', 'indie']},  # Ezra Furman — Restless Year
    '4b1Y41U44kP7gzO7MUNGbe': {'discogs': ['techno', 'broken beat', 'hardcore', 'sound collage'], 'musicbrainz': [], 'lastfm': ['punk', 'punk rock', 'folk punk', 'rock']},  # Against Me! — Transgender Dysphoria Blues
    '0a0CwJBn8lmT5ifk63EUbP': {'discogs': ['techno', 'broken beat', 'hardcore', 'sound collage'], 'musicbrainz': ['acoustic rock', 'alternative rock', 'punk', 'rock', 'folk punk', 'folk rock'], 'lastfm': ['punk', 'punk rock', 'folk punk', 'rock']},  # Against Me! — True Trans Soul Rebel
    '20JYh6XUjLjiN1CyJ32ZiY': {'discogs': ['dark electro', 'horrorcore', 'trap', 'pop rap'], 'musicbrainz': [], 'lastfm': ['trap metal', 'rap', 'hip hop']},  # Changeline, Stolas — ANARCONNASSE
    '3eBY8aZZdWNnNhNbc8B0yp': {'discogs': [], 'musicbrainz': [], 'lastfm': []},  # Andra Venus — Power
    '3FysLYckiMCMzjYLIgo45U': {'discogs': ['horrorcore', 'electro', 'dubstep', 'industrial'], 'musicbrainz': [], 'lastfm': ['horrorcore', 'industrial hip hop', 'trap', 'experimental hip hop']},  # Backxwash — BLACK SAILOR MOON
    '37OSQm8Gy5strUT24vn6ef': {'discogs': ['horrorcore', 'electro', 'dubstep', 'industrial'], 'musicbrainz': ['horrorcore', 'industrial hip hop'], 'lastfm': ['horrorcore', 'industrial hip hop', 'trap', 'experimental hip hop']},  # Backxwash, Ada Rook — I LIE HERE BURIED WITH MY RINGS AND MY DRESSES
    '2iqTYCPRTqojxM7QJvBtk2': {'discogs': ['drill', 'conscious'], 'musicbrainz': [], 'lastfm': ['drill', 'rap', 'hip hop']},  # Ms. Boogie — Breakdown
    '6JrmHzxhaaavRtlXTOhm63': {'discogs': [], 'musicbrainz': [], 'lastfm': ['rap', 'hip hop']},  # Quay Dash — Queen Of This Shit
    '3QF7smzmw2WWm7M1jt2Rac': {'discogs': [], 'musicbrainz': [], 'lastfm': []},  # Angel Maxine, Wanlov The Kubolor, Sister Deborah — Wo Fie
    '1RkB4Dk0CDzpaSySq91JEA': {'discogs': [], 'musicbrainz': [], 'lastfm': ['pop', 'acoustic', 'hip hop', 'trap', 'mathcore']},  # Sasha Sathya — AKA LESBIANA SERPIENTA
    '4UfEEnq70NgLeq7NRfXPiD': {'discogs': [], 'musicbrainz': [], 'lastfm': ['rap']},  # LALLA RAMI — INCHALLAH
    '5nWecUJF2pytSxsSpylzZw': {'discogs': [], 'musicbrainz': [], 'lastfm': ['rap']},  # LALLA RAMI — 9A7BA
    '0A2tFUYLertZLltvvY5uyr': {'discogs': ['experimental', 'horrorcore', 'thug rap', 'trap'], 'musicbrainz': [], 'lastfm': ['electronic', 'experimental hip hop', 'hip hop', 'digicore']},  # Ptite Soeur, Gemroz — KAYFABE
    '5Gp1fkuPV7CPtzKHfMH0kd': {'discogs': ['experimental', 'horrorcore', 'thug rap', 'trap'], 'musicbrainz': [], 'lastfm': ['electronic', 'experimental hip hop', 'hip hop', 'digicore']},  # Ptite Soeur, neophron — ANFO჻
    '0ZeVhHgvMsF6dqo2AFSfut': {'discogs': ['punk', 'hyperpop'], 'musicbrainz': [], 'lastfm': ['indie pop', 'indie', 'glitchcore', 'synth pop', 'glitch punk', 'glitch pop']},  # TAMAGOTCHI MASSACRE — i'm 2 years on hormones and i'm still sad i want a refund
    '1PEPcLm2QEo0HCRIhQjPq1': {'discogs': ['future bass', 'indie pop', 'trap', 'leftfield'], 'musicbrainz': ['live'], 'lastfm': ['hyperpop', 'alt-pop', 'pop', 'indie']},  # underscores — Second hand embarrassment
    '7n7GrVTBmZMG4EULD5g0i3': {'discogs': ['hyperpop', 'hip hop', 'experimental', 'glitch'], 'musicbrainz': [], 'lastfm': ['digicore', 'emo rap', 'trap']},  # osquinn — warm and fuzzy
    '0VNjaRcmIowjLbPtYDhLuh': {'discogs': ['future bass', 'indie pop', 'trap', 'leftfield'], 'musicbrainz': ['alternative pop', 'alternative r&b', 'alternative rock', 'electronic', 'experimental', 'glitch pop', 'hyperpop', 'indie pop', 'indie rock', 'leftfield', 'pop', 'pop rock', 'rock', 'synth-pop'], 'lastfm': ['hyperpop', 'indie pop', 'electronic', 'indietronica', 'indie rock']},  # underscores, 8485 — Your favorite sidekick
    '1d3hBkCcMvVzsZjaMiVvNs': {'discogs': ['bubblegum', 'electroclash', 'house', 'hyperpop'], 'musicbrainz': ['dance-pop', 'electronic', 'pop'], 'lastfm': ['pop', 'electronic', 'hyperpop', 'electropop']},  # Chase Icon — SRS
    '1RXkdiCc4TtwPacmIKyUnX': {'discogs': ['electroclash', 'dance-pop', 'hyperpop', 'hip-house'], 'musicbrainz': ['bitpop', 'bubblegum bass', 'dance-pop', 'electro house', 'electropop', 'euro-trance', 'miami bass', 'contemporary r&b', 'pop', 'atlanta bass'], 'lastfm': ['electropop', 'pop', 'dance-pop', 'electronic', 'bitpop', 'electro house', 'dance']},  # Ayesha Erotica — Vacation Bible School
    '54n3iwz9mr7yxZi1EOX1Mz': {'discogs': ['future bass', 'indie pop', 'trap', 'leftfield'], 'musicbrainz': [], 'lastfm': ['electropop', 'indietronica', 'new rave', 'dance-pop', 'electroclash']},  # underscores, gabby start — Locals (Girls like us) [with gabby start]
    '6WkiWn8bf8S29wSk0VwK7h': {'discogs': ['hyperpop', 'dance-pop', 'electro', 'indie pop'], 'musicbrainz': [], 'lastfm': ['hyperpop', 'electropop', 'indie pop', 'electronic']},  # Frost Children — Falling
    '724utiMbqUfT1g3tqbfQYu': {'discogs': ['future bass', 'indie pop', 'trap', 'leftfield'], 'musicbrainz': [], 'lastfm': ['hyperpop', 'pop punk', 'emo-pop', 'glitch']},  # underscores — Spoiled little brat
    '3RLI8S7KpEZs4SqePGjM2R': {'discogs': ['experimental'], 'musicbrainz': [], 'lastfm': ['hyperpop', 'indie rock']},  # estelle allen — dui
    '1XD4K4CGAKTIBmFpvuaFru': {'discogs': ['trap', 'hyperpop', 'hardcore hip-hop', 'experimental'], 'musicbrainz': ['bass house', 'dariacore', 'digicore', 'electro hop', 'electroclash', 'electropop', 'experimental hip hop', 'future bass', 'hyperpop', 'rage'], 'lastfm': ['hyperpop', 'electropop']},  # Jane Remover — Dancing with your eyes closed
    '2gmwvGC1yOw8NdMcZE8nfo': {'discogs': ['electroclash', 'dance-pop', 'hyperpop', 'hip-house'], 'musicbrainz': [], 'lastfm': ['hip-house', 'ballroom', 'hyperpop']},  # Ayesha Erotica — Literal Legend
    '1toNKayLMeCcVlsLGXJl7n': {'discogs': ['bubblegum', 'hyperpop', 'emo', 'experimental'], 'musicbrainz': ['electroclash', 'electropop', 'electronic', 'experimental', 'hyperpop', 'electroclash + electropop'], 'lastfm': ['hyperpop']},  # Laura Les — Haunted
    '18QS9wnUr7DOhMb73monpK': {'discogs': [], 'musicbrainz': [], 'lastfm': ['hyperpop', 'pop', 'dance', 'electronic']},  # Mel 4Ever, Ayesha Erotica — Tongues
    '0Irj6PuEEGzi7JGJvAhdZ8': {'discogs': [], 'musicbrainz': [], 'lastfm': ['hyperpop', 'pop', 'dance', 'electronic']},  # Mel 4Ever — I Can’t Quit
    '06kFuqzhMk4E6IYeO0sTfx': {'discogs': ['hyperpop', 'dance-pop', 'electro', 'indie pop'], 'musicbrainz': [], 'lastfm': ['fidget house', 'electropop', 'electroclash', 'electro house']},  # Frost Children, Kim Petras — RADIO (feat. Kim Petras)
    '2sVjF25Z4JTJxi9BXm5GtJ': {'discogs': ['breakcore', 'hardcore', 'footwork', 'juke'], 'musicbrainz': ['hexd', 'dance', 'digicore', 'digital hardcore', 'electronic', 'footwork', 'footwork jungle', 'gabber', 'hardcore breaks', 'horrorcore', 'juke', 'rave', 'techno', 'cringecore', 'jungle dnb', 'rap', 'scream rap'], 'lastfm': ['dance', 'digital hardcore', 'breakcore', 'electronic']},  # femtanyl — ACT RIGHT
    '51NYFGDXYKS4FkRqkw98hx': {'discogs': ['bubblegum', 'electroclash', 'house', 'hyperpop'], 'musicbrainz': ['dance-pop', 'electro house', 'electronic', 'hip hop', 'pop'], 'lastfm': ['pop', 'electronic', 'hyperpop', 'electropop']},  # Chase Icon — Like Me
    '5iTzaatezJzsUhX1QjT0Kp': {'discogs': ['ambient', 'trance', 'electro', 'abstract'], 'musicbrainz': [], 'lastfm': ['hyperpop', 'electronic']},  # Petal Supply — Person - Angel Mix
    '7kvQptbfqq5b4MWRQOMrZC': {'discogs': ['breakcore', 'hardcore', 'footwork', 'juke'], 'musicbrainz': [], 'lastfm': ['hardcore', 'hip hop', 'rap']},  # femtanyl, ISSBROKIE — NASTYWERKKKK!
    '6XeW8fjwoAFQeQpYojPtVI': {'discogs': ['breakcore', 'hardcore', 'footwork', 'juke'], 'musicbrainz': ['dance', 'digicore', 'digital hardcore', 'electronic', 'footwork', 'footwork jungle', 'gabber', 'hardcore breaks', 'hexd', 'horrorcore', 'juke', 'rave', 'techno', 'cringecore', 'jungle dnb', 'rap', 'scream rap'], 'lastfm': ['electronic', 'rap', 'digital hardcore', 'drum and bass', 'energetic', 'edgy', 'dnb', 'edm', 'yumi', 'y2k']},  # femtanyl — GIRL HELL 1999
    '5iAE3uBqaZm9aHUx9yy6a0': {'discogs': ['breakcore', 'hardcore', 'footwork', 'juke'], 'musicbrainz': ['dance', 'digicore', 'digital hardcore', 'electronic', 'footwork', 'footwork jungle', 'gabber', 'hardcore breaks', 'hexd', 'horrorcore', 'juke', 'rave', 'techno', 'cringecore', 'jungle dnb', 'rap', 'scream rap'], 'lastfm': ['digital hardcore', 'hardcore', 'electronic', 'dance']},  # femtanyl — KATAMARI
    '1w0AFg23E67l57A3RMiXjC': {'discogs': ['breakcore', 'hardcore', 'footwork', 'juke'], 'musicbrainz': ['dance', 'digicore', 'digital hardcore', 'electronic', 'footwork', 'footwork jungle', 'gabber', 'hardcore breaks', 'hardstyle', 'hexd', 'horrorcore', 'hyperpop', 'juke', 'rave', 'techno', 'cringecore', 'jungle dnb', 'rap', 'scream rap'], 'lastfm': ['pop']},  # femtanyl — P3T
    '5PMtJGEDIO0eIToF0YRUQ5': {'discogs': [], 'musicbrainz': [], 'lastfm': []},  # JEDET — VENENO PA’ TU PIEL
    '2qpx5shtNEO1DuK8iEoJoB': {'discogs': ['hi nrg', 'disco', 'house', 'rnb/swing'], 'musicbrainz': [], 'lastfm': ['drag', 'rnb', 'electro']},  # Peppermint — Best Sex
    '3BqWvhPear6eKPwhwJRFpO': {'discogs': ['house', 'dance-pop', 'disco'], 'musicbrainz': [], 'lastfm': ['diva']},  # Mila Jam — Bruised
    '1jFN0stMzLepoPxvPywGZj': {'discogs': ['synth-pop', 'vocal', 'tribal house', 'house'], 'musicbrainz': ['dance-pop', 'electro-disco', 'electronic', 'electropop', 'nu disco', 'pop', 'synth-pop'], 'lastfm': ['pop', 'electropop', 'electronic']},  # Kim Petras — Heart to Break
    '4QnHaiWq1oJiTgMnRFE0q8': {'discogs': ['electro', 'dance-pop', 'disco', 'house'], 'musicbrainz': [], 'lastfm': ['pop', 'electronic']},  # Zemmoa, Tessa Ia, Trans-X — Mi Amor Soy Yo
    '2Of9piZALXa4CC7Unxoeeg': {'discogs': ['hip-house', 'tech house', 'hip hop', 'trap'], 'musicbrainz': [], 'lastfm': []},  # Villano Antillano — KLK
    '5lz6U9dCYBmEY6oLrW22VE': {'discogs': ['african', 'hip hop', 'techno', 'folk'], 'musicbrainz': [], 'lastfm': ['kuduro', 'pop']},  # Titica, Kelmer Pastilha, Mauro Xtraga — Olha a Banana
    '5srzGYocC4qYFvckQm5AfC': {'discogs': [], 'musicbrainz': [], 'lastfm': []},  # Haiifa Magic — To2i W Far2a3i
    '4xhYxKvAxtrRd83MiqOy29': {'discogs': ['synth-pop', 'vocal', 'tribal house', 'house'], 'musicbrainz': ['alternative pop', 'contemporary r&b', 'dance-pop', 'electronic', 'electropop', 'funktronica', 'nu disco', 'pop', 'pop rap', 'synth funk', 'synth-pop', 'teen pop'], 'lastfm': ['pop', 'electropop', 'electronic']},  # Kim Petras — I Don’t Want It At All
    '1AFPmwB6mGMCcMI2hFh7c8': {'discogs': ['abstract', 'funk', 'techno', 'favela funk'], 'musicbrainz': [], 'lastfm': ['funk', 'rap', 'experimental', 'brazil']},  # Linn da Quebrada — Enviadescer
    '1RmXibCbfLIVrN8ZRdoYbW': {'discogs': ['hyperpop', 'dance-pop', 'favela funk', 'house'], 'musicbrainz': [], 'lastfm': ['pop', 'electronic']},  # Urias — Foi Mal
    '5pkemVhnBiIzMs2NLsXomQ': {'discogs': ['synth-pop', 'vocal', 'tribal house', 'house'], 'musicbrainz': ['contemporary r&b', 'pop rap', 'alternative r&b', 'bubblegum pop', 'dance-pop', 'disco', 'electronic', 'electropop', 'emo', 'glam rock', 'hip hop', 'pop', 'r&b', 'trap'], 'lastfm': ['pop', 'electropop', 'electronic']},  # Kim Petras — Clarity
    '4ED8r6i90zmUG4kfbiVoou': {'discogs': ['house', 'nu disco', 'disco', 'rhythm & blues'], 'musicbrainz': ['alternative pop', 'chamber pop'], 'lastfm': ['rnb']},  # Ah-Mer-Ah-Su — Heartbreaker
    '4hceSKjrkDTO0nMKFcb3sj': {'discogs': ['techno', 'trap', 'reggaeton', 'electro'], 'musicbrainz': [], 'lastfm': ['rap', 'trap', 'latin']},  # Bizarrap, Villano Antillano — Villano Antillano: Bzrp Music Sessions, Vol. 51/66
    '46uGvJVhYHOVRRNnRPbkYm': {'discogs': [], 'musicbrainz': [], 'lastfm': []},  # Lucinta Luna, Dede Satria — Mantan Tanpa Status - Lucinta Luna Version
    '1YsFdaP9QG9NhjYS3o0g5P': {'discogs': ['african', 'hip hop', 'techno', 'folk'], 'musicbrainz': [], 'lastfm': ['kuduro', 'pop']},  # Titica, Ary — Olha o Boneco
    '7luHAaHXty1Nl3AcscZIDT': {'discogs': ['house', 'dance-pop', 'disco'], 'musicbrainz': [], 'lastfm': ['diva']},  # Mila Jam — Faces
    '78iHtTxYIK2mD6oL6lXqFF': {'discogs': [], 'musicbrainz': [], 'lastfm': []},  # Gad Yola — Travesti del Perú
    '4Zhxtm6x56wEiRtSMAl28n': {'discogs': ['hyperpop', 'dance-pop', 'favela funk', 'house'], 'musicbrainz': ['pop'], 'lastfm': ['pop', 'electronic']},  # Urias — Diaba
    '5dIPCgTEDagbcs5QGmni8V': {'discogs': ['house', 'electro house', 'contemporary r&b', 'neo soul'], 'musicbrainz': [], 'lastfm': []},  # MONĀE, Cae Monāe — CISPHOBIC
    '6yAc1rz1RXRlYJac99xusK': {'discogs': ['holiday', 'dance-pop', 'ballad', 'europop'], 'musicbrainz': [], 'lastfm': []},  # Tone Sekelius — Girls & Dolls
    '376mhFeloWqzQJQsqZpm9A': {'discogs': ['dance-pop', 'europop'], 'musicbrainz': [], 'lastfm': []},  # Pupi Poisson, Arantxa Castilla-La Mancha, CARLES CUEVAS — Las Defectos
    '4OI2gBlHqyNks8cbIBIKYw': {'discogs': ['bass music', 'experimental', 'mandopop', 'idm'], 'musicbrainz': [], 'lastfm': ['sound collage', 'electronic', 'ballroom', 'kuduro', 'uk bass']},  # Angel-Ho, K Rizz — Like A Girl
    '6D7zTed8zrkuKBPca2AqSI': {'discogs': [], 'musicbrainz': [], 'lastfm': ['electronic', 'brazilian bass', 'funk brasileiro', 'brazilian funk', 'funk mandelao', 'rap']},  # Irmãs de Pau, Brunoso — Medley do Submundo
    '71yN0yrHej3jhKXewbmtEh': {'discogs': ['synth-pop', 'vocal', 'tribal house', 'house'], 'musicbrainz': ['contemporary r&b', 'dance-pop', 'electronic', 'electropop', 'europop', 'house', 'nu disco', 'pop', 'synth-pop'], 'lastfm': ['pop', 'electropop', 'electronic']},  # Kim Petras — Coconuts
    '7bNgXJ9MgGG7xOkyz9SLOY': {'discogs': ['mpb', 'favela funk', 'funk', 'reggae'], 'musicbrainz': [], 'lastfm': ['loonaids']},  # PEDRO SAMPAIO, Irmãs de Pau, Mc Gw, Tasha Kaiala, Clementaum — SEQUÊNCIA CUNT (feat. Clementaum)
    '4WhyfhjZaX6AVjAZslQAFs': {'discogs': [], 'musicbrainz': [], 'lastfm': ['urban conceitual', 'grunge', 'funk', 'indie funk']},  # Mulher Pepita, Brabo — Parceira
    '75HFFq9W7Em0dTBG8QeGcT': {'discogs': ['synth-pop', 'vocal', 'tribal house', 'house'], 'musicbrainz': ['dance-pop', 'electropop', 'synth-pop'], 'lastfm': ['pop', 'electropop', 'electronic']},  # Kim Petras — There Will Be Blood
    '1EPYnBjYhYHcNthEnVWk18': {'discogs': ['k-pop', 'house', 'rnb/swing', 'ballad'], 'musicbrainz': [], 'lastfm': ['k-pop']},  # Harisu — 됐거든
    '0GSW6V6GJc4xYi8c5jOu60': {'discogs': [], 'musicbrainz': [], 'lastfm': ['j-pop']},  # Ai Haruna — さそり座の女
    '2lgwylOpGMtkvhwdnUOArt': {'discogs': ['schlager', 'euro-disco', 'dance-pop', 'chanson'], 'musicbrainz': [], 'lastfm': ['pop']},  # Romy Haag — Memories Are Made Of This - Radio
    '4X6PkqzKUvWWKoq4YiiM1V': {'discogs': ['k-pop', 'house', 'rnb/swing', 'ballad'], 'musicbrainz': [], 'lastfm': ['k-pop']},  # Harisu — Snow White
    '4yBfzgV6YA9dTKP8KUD35j': {'discogs': ['dance-pop'], 'musicbrainz': [], 'lastfm': ['pop']},  # Lia Larsson, Tone Sekelius, Lisa Ajax — VI ÄR SVERIGE (VM-låt 2023)
    '29Ga6IgetN8Xah85ZHZ8AC': {'discogs': ['villancicos', 'electroclash', 'holiday', 'euro house'], 'musicbrainz': [], 'lastfm': ['pop', 'indie', 'alternative', 'electronic', 'electrotrash']},  # Samantha Hudson, Villano Antillano — Full Lace y el Tuck
    '0pe5NUU9uGwFpj637ot84D': {'discogs': [], 'musicbrainz': [], 'lastfm': []},  # Patricia Ribeiro — Conquistador
    '3qDqg53YIe9mM5Ehx9v9FZ': {'discogs': [], 'musicbrainz': [], 'lastfm': []},  # La Veneno — El Rap de la Veneno
    '6fd79PtewFZgLXYiIYhhLJ': {'discogs': [], 'musicbrainz': [], 'lastfm': []},  # Ella — La Drácula
}
