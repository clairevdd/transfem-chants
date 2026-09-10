# -*- coding: utf-8 -*-
"""Tags de genre/style/scène par morceau, pour la page tags.html.

Sources, par ordre : styles Discogs (`discogs_styles`), genres MusicBrainz
(union enregistrement + groupe, `mb_genres_union`), tags de genre Last.fm
(`lfm_tags_genre`). Les trois viennent d'API, contrairement à Bandcamp, qui
n'en a pas : Bandcamp est donc exclu ici, y compris pour les quelques
morceaux où un relevé manuel existe déjà (4 sur 146), pour que la couverture
reste homogène à mesure que la playlist s'augmente plutôt que de dépendre de
qui a pensé à relever une page Bandcamp à la main.

Granularité réelle des trois sources, à garder en tête en la lisant :
Discogs tague au niveau de la sortie ou de l'artiste, pas du morceau, d'où
les mêmes styles répétés sur plusieurs titres d'un même disque. MusicBrainz
et Last.fm sont plus fins mais inégaux : sur les 146 morceaux, Last.fm ne
tient un tag propre au morceau que pour 17 d'entre eux, retombe sur les tags
de l'artiste pour 110, et n'en a aucun pour 19. Un morceau sans aucun tag,
des trois sources confondues, est un morceau `unclassified` : 10 sur 146.

Fusion des seuls doublons de pure graphie, jamais des synonymes conceptuels :
avant-garde/avantgarde, experimental hip hop/-hip-hop, hip hop/hip-hop,
hip-house/hip house, j-pop/jpop, nu disco/nu-disco, synth-pop/synth pop/
synthpop, v-pop/vpop. Chaque paire désigne la même chaîne, à l'orthographe
près : la forme la plus fréquente devient la forme canonique. `rap` et
`hip hop` restent deux tags distincts : arbitrage de Claire, 10 septembre
2026, alors que d'autres puces de la page auraient pu les present comme un
duo.

Écarté aussi, silencieusement : trois tags de type Last.fm qui n'étaient pas
des genres musicaux mais des mots-clés communautaires sur l'identité de
l'artiste (« transwoman », « transexual » sur Coccinelle, « woman » sur
femtanyl/ISSBROKIE). Le tag Last.fm est une folksonomie libre, pas un
vocabulaire de genre encadré, et rien n'empêche quelqu'un d'y écrire un mot
sur l'identité d'une artiste plutôt que sur sa musique. Cette page classe de
la musique, pas des personnes : ces trois entrées sont retirées de TAGS,
jamais publiées, quelle que soit la source qui les a produites.

TAGS : identifiant Spotify -> liste de tags canoniques (list vide si aucun
tag trouvé dans les trois sources, ce qui devient `unclassified` sur la page).
"""

TAGS = {
    '1ovz0bZeO5YTBQTXIFf5Am': ['ambient', 'classical', 'downtempo', 'electronic', 'house', 'modern classical', 'musical'],  # Daniela Vega — Ombra Mai Fu
    '5l2zYkyTXtYa8xk965ofqD': ['classical'],  # Tona Brown, Geraldine Boone — Dream Variations
    '1AHPsqF3EtHeWpOM06Y3Y4': ['art rock', 'avant-garde', 'alternative rock', 'ballad', 'experimental', 'folk rock', 'hip hop', 'indie rock', 'lo-fi', 'math rock', 'pop', 'pop rock', 'post-hardcore', 'punk', 'rock', 'rock and roll', 'space rock', 'stoner rock', 'turntablism', 'singer-songwriter', 'chamber pop', 'indie', 'alternative', 'folk'],  # Antony and the Johnsons, ANOHNI — Hope There’s Someone
    '5P9EKJfOZtuwtTR5C5362i': ['ambient', 'classical', 'downtempo', 'electronic', 'house', 'modern classical', 'musical'],  # Daniela Vega — Sposa Son Disprezzata
    '02L1ngagXNRt8W3Flbe9Sw': ['poetry', 'folk', 'folk rock', 'acoustic'],  # Namoli Brennet — Boy in a Dress
    '1OpCGPKSq4IfpvLptsSMR9': ['classical'],  # Tona Brown, Geraldine Boone — I, Too
    '1QrL7ucS71Ih4HXBOsuajv': ['son', 'mexico', 'folk', 'acoustic', 'latin'],  # La Bruja de Texcoco — Laabe Muxhe
    '3nxFYWNFG2qGYEuhEzomtO': ['cumbia'],  # Susy Shock — Vidalita, Vidalita
    '5e0ZXu358l51ckAZvai2Ef': ['ottoman classical', 'volksmusik', 'éntekhno', 'folk', 'turk sanat muzigi', 'turkish', 'tsm', 'diva'],  # Bülent Ersoy — Geceler
    '4Ykmj47fulJ1FTeCXctW91': ['v-pop', 'nhạc vàng', 'ballad', 'comedy'],  # Hương Giang — Anh Ta Bỏ Em Rồi
    '07m5UbUHOQCofRK16k83Eg': [],  # Shyraa Roy, Kashif Ali — Duniya
    '73xUwV4DkcelY7seMyY0PY': ['folk'],  # Beth Elliott — Lady on the Subway
    '4dtyeDMnVKKo89QbbDtD5M': ['folk'],  # Beth Elliott — Ballad of the Oklahoma Women’s Liberation Front
    '3BYSoeWlqUgIwfY77C8VgE': ['son', 'latin', 'mexico', 'folk', 'acoustic'],  # La Bruja de Texcoco — Té de Malvón
    '7KtbrK74NNA4ySRZ49DC7R': ['country', 'alternative rock', 'folk', 'folk rock', 'americana', 'blues'],  # Mya Byrne — Where the Lavender Grows
    '0XIutL5epZuYV91bhCfFsR': ['ottoman classical', 'volksmusik', 'éntekhno', 'folk', 'turk sanat muzigi', 'turkish', 'tsm', 'diva'],  # Bülent Ersoy — Ümit Hırsızı
    '3MZjOGeXhpHbQ9ESMNFFnH': ['folk', 'folk rock', 'vocal', 'indie pop', 'steampunk', 'cabaret', 'cabaret folk'],  # Steam Powered Giraffe — Honeybee
    '3ApVA7ID6PkS0fGzNF4mFw': ['hi nrg', 'disco', 'house', 'rnb/swing', 'drag', 'rnb', 'electro', 'american'],  # Peppermint — A Girl Like Me
    '4CuivW1JgPauXPA4wYsf5K': ['chanson', 'vocal', 'music hall', 'disco', 'french', 'cabaret', 'chanson française', 'madame arthur'],  # Coccinelle — Chercher la femme
    '5dtUOwEmnDAzsdodWJk4DA': ['soul', 'rhythm & blues', 'northern soul'],  # Jackie Shane — Any Other Way
    '5NnQ2xIeHDKc1B19rxfcV3': ['cabaret', 'cool jazz', 'vocal', 'smooth jazz', 'pop'],  # Veronica Klaus — I Will Survive
    '0VhGzYfT2ZOFz31b5IH7yJ': ['chanson', 'pop rock', 'garage rock', 'punk', 'pop', 'french'],  # Marie France, Chrissie Hynde — Un garçon qui pleure
    '4P9LdSPrnQl7KQwml4DUtq': ['mpb', 'rhythm & blues', 'latin pop', 'soul', 'black music', 'brazilian'],  # Liniker — Baby 95
    '56xBg5e9rfrFqcqa4llUw7': ['vocal', 'easy listening', 'soul-jazz', 'alternative rock', 'drag queen', 'cabaret', 'drag performer'],  # Jinkx Monsoon — Just Me (The Gender Binary Blues)
    '5WttRLHcZHhaIii5KwKh3Y': ['alternative rock', 'rnb', 'soul'],  # Shea Diamond — I Am Her
    '0rK7QTyYjhPFadLH2YDl84': ['pa'],  # Our Lady J — Picture of a Man
    '0gm0OruZdJlu8jamJe5OCh': ['alternative rock', 'rnb', 'soul'],  # Shea Diamond — Keisha Complexion
    '3XdXixlx3MoVzfL7pu9hx6': ['experimental', 'bass music', 'reggaeton', 'deconstructed club', 'electronic', 'ambient', 'art pop', 'cumbia', 'epic collage', 'experimental hip hop', 'glitch hop', 'glitch pop', 'idm', 'industrial hip hop', 'latin', 'leftfield', 'neoperreo', 'noise', 'pop', 'post-industrial', 'latin electronic', 'nsfw cover art', 'glitch'],  # Arca — Time
    '0QA1xpUuqHDHWZhi0eAbH7': ['hyperpop', 'bass music', 'experimental', 'dance-pop', 'art pop', 'synth-pop', 'avant-garde', 'deconstructed club', 'electronic', 'pop', 'post-industrial', 'double album', 'uk bass', 'bubblegum bass', 'wonky'],  # SOPHIE — It’s Okay To Cry
    '6EjxYTyXiBzJz6PeOvPiou': ['j-pop', 'ballad', 'japanese', 'jazz'],  # Ataru Nakamura — きみがすきだよ
    '1N1F6UsRGILux57U0YbxJQ': [],  # Cindy Thái Tài — Giọt Tình
    '7l8D5tXUVsdq95VQWn034C': ['k-pop', 'house', 'rnb/swing', 'ballad', 'korean'],  # Harisu — 애지몽
    '0DZapO0gUF8XZpk2bu8AeL': ['dance-pop', 'euro house', 'house'],  # Aderet — היו לילות
    '3r0gvoaAkWmLdJO4UUv94v': ['experimental', 'bass music', 'reggaeton', 'deconstructed club', 'ambient', 'electronic', 'leftfield', 'ambient pop', 'art pop', 'deep house', 'ghettotech', 'glitch pop', 'hip hop', 'idm', 'jazz', 'pop', 'post-industrial', 'singer-songwriter', 'techno', 'abstract electronic', 'glitch'],  # Arca — Desafío
    '2Ff6Ghw8TRJGuAbJamtt4X': ['alternative rock', 'indie pop', 'indie rock', 'electro', 'dream pop', 'guitar'],  # SuperKnova — Serotonin Serenade
    '48XnOS1vTyzqaPps0Dalzp': ['hyperpop', 'bass music', 'experimental', 'dance-pop', 'bubblegum bass', 'deconstructed club', 'avant-garde', 'electronic', 'pop', 'post-industrial', 'rock', 'double album', 'uk bass', 'wonky'],  # SOPHIE — Ponyboy
    '7tktCNlB0877dhdPZSRb7T': ['hyperpop', 'bass music', 'experimental', 'dance-pop', 'art pop', 'avant-garde', 'deconstructed club', 'electronic', 'pop', 'post-industrial', 'double album', 'uk bass', 'bubblegum bass', 'wonky'],  # SOPHIE — Is It Cold In The Water?
    '6JZfK4Z75nZm3VcZOVrpy0': ['avant-garde', 'alternative rock', 'indie pop', 'vocal', 'electronic', 'art pop', 'chamber pop', 'experimental'],  # ANOHNI — Drone Bomb Me
    '0kNjtDBxrpjJTZn9w5Eq3C': ['indie pop', 'indie rock', 'pop', 'rock', 'electropop', 'canadian', 'canada'],  # Vivek Shraya — I Take All the Blame
    '7EPHu29KqhsGk4dZAjM0o4': [],  # Stef Aranas — Cvnty
    '2fB0l9upVjg0QTeMyrIVtc': ['indie pop', 'pop', 'indie', 'electropop', 'canadian', 'canada'],  # Vivek Shraya, Queer Songbook Orchestra — Part-Time Woman
    '2rN1ODOsaNfYu782rw36jR': ['hyperpop', 'bass music', 'experimental', 'dance-pop', 'electronic', 'yassification', 'bubblegum bass', 'deconstructed club', 'wonky'],  # SOPHIE — Faceshopping
    '4lUlYGT5VvZWN3GBDIc9KT': ['experimental', 'bass music', 'reggaeton', 'deconstructed club', 'electronic', 'ambient', 'glitch', 'idm'],  # Arca — Nonbinary
    '2KryklrVDGmWL8IvoGNbb5': ['african', 'south african', 'electronic'],  # Umlilo — Zulu Lami
    '5nnBHHzUDOGvdMBiXofB00': ['experimental', 'abstract', 'cumbia', 'synth-pop', 'alternative', 'drone', 'art rock', 'mexico'],  # Luisa Almaguer — Exiliades
    '5rOzcHIZaF038jMeHkUZR0': ['experimental', 'bass music', 'reggaeton', 'deconstructed club', 'ambient pop', 'art pop', 'electronic', 'glitch pop', 'idm', 'pop', 'post-industrial', 'singer-songwriter', 'ambient', 'glitch'],  # Arca — Reverie
    '6jiumfqTwOpXW6PDzsIBKl': ['pop rock', 'pop', 'electronic', 'indie pop', 'synth-pop', 'indie rock'],  # Sonja Sajzor — I Keep Doing This to Myself
    '6JGJdnIbq4UqKgzFaOIXwE': ['experimental', 'abstract', 'cumbia', 'synth-pop', 'alternative', 'drone', 'art rock', 'mexico'],  # Luisa Almaguer — Mataronomatar
    '0NOume8OgBz4FCnP1QVr9A': ['pop', 'thailand', 'freelance'],  # Bell Nuntita — Paradise
    '3z4KIXgkhLauhNP3ubB8cF': ['acoustic', 'alternative rock', 'indie rock', 'indie pop', 'folk', 'indie', 'singer-songwriter', 'alternative', 'american'],  # Left at London — 6 Feet
    '2BQZhUPXdP9Nk1X84c7PtP': ['experimental', 'ambient', 'alt-pop', 'baroque pop', 'post-rock', 'french', 'chamber pop', 'electronic', 'art pop'],  # Lauren Auder, Celeste — Unseen (feat. Celeste)
    '2CznvTOsuLh0USpHJqEc6V': ['synth-pop', 'alt-pop', 'hyperpop', 'indie pop', 'electronic', 'australia'],  # June Jones, Geryon — Motorcycle
    '3IDQXyHYuX2rdLnNfVzT3g': ['avant-garde', 'alternative rock', 'indie pop', 'vocal', 'art pop', 'electropop', 'glitch pop', 'idm', 'electronic', 'chamber pop', 'experimental'],  # ANOHNI — 4 DEGREES
    '1huN927tTdSiwF90FBHXkT': ['hyperpop', 'bass music', 'experimental', 'dance-pop', 'bubblegum bass', 'electropop', 'avant-garde', 'deconstructed club', 'electronic', 'indie pop', 'indie rock', 'pop', 'post-industrial', 'post-rock', 'rock', 'double album', 'uk bass'],  # SOPHIE — Immaterial
    '3qBg6BeHJlGgwl5aCa09EC': ['acoustic', 'alternative rock', 'indie rock', 'indie pop', 'folk', 'indie', 'singer-songwriter', 'alternative', 'american'],  # Left at London — Revolution Lover
    '6RJiY28t9jWpdy1JkUhNgK': ['experimental', 'bass music', 'reggaeton', 'deconstructed club', 'electronic', 'ambient', 'art pop', 'cumbia', 'epic collage', 'experimental hip hop', 'glitch hop', 'glitch pop', 'idm', 'industrial hip hop', 'latin', 'leftfield', 'neoperreo', 'noise', 'pop', 'post-industrial', 'latin electronic', 'nsfw cover art', 'glitch'],  # Arca — Mequetrefe
    '3Vk1AHIh1CoiQzFroldMhO': ['glam', 'goth rock', 'punk'],  # Venus De Mars — Take My Shoulder (feat. Laura Jane Grace)
    '2DUAIlPmzV2is5OQIZASUA': ['hyperpop', 'emo', 'alternative rock', 'indie rock', 'digital hardcore', 'punk', 'breakcore', 'united states', '3', 'minneapolis', 'bounce hardcore', 'upcoming album 2022', 'played with i h8 it here'],  # Anita Velveeta — T4T
    '3ShIGvHRm0q9iIDowUMjls': ['acoustic', 'punk', 'folk', 'alternative rock', 'folk rock', 'indie rock', 'lo-fi', 'rock', 'folk punk', 'punk rock', 'singer-songwriter'],  # Laura Jane Grace — The Best Ever Death Metal Band in Denton
    '2jFP4mAHcDmGe7DEKKLyJa': ['alternative rock', 'folk', 'indie rock', 'rock', 'singer-songwriter', 'indie'],  # jasmine.4.t — Skin On Skin
    '7GAI6zWpmst6dSfu1wIA1O': [],  # Venus de Mars and All the Pretty Horses — White Horses
    '3RXajeZOzqXWrQwLDfTzKK': ['acoustic', 'emo', 'hyperpop', 'indie pop', 'punk'],  # THÉA — JUSTE AMIS
    '0bWpWsvZeTTNLQ9nuXqKIN': ['acoustic', 'emo', 'hyperpop', 'indie pop', 'electropop', 'techno', 'trap', 'punk'],  # THÉA — Guillotine
    '3zGmkzXqXsXYVlGzJFpgCW': [],  # Venus de Mars and All the Pretty Horses — Boys
    '4ltqfN12ohaVZdM6C45gMg': ['indie rock', 'ambient', 'ethereal', 'experimental', 'americana', 'dream pop', 'heartland rock', 'pop rock', 'synth-pop', 'artist on cover', 'big music', 'wsum 91.7 fm madison'],  # Ethel Cain — American Teenager
    '14uL43Gg4ujizaATehrryk': ['techno', 'broken beat', 'hardcore', 'sound collage', 'alternative rock', 'folk punk', 'pop rock', 'punk', 'rock', 'punk rock', 'rock and indie'],  # Against Me! — The Ocean
    '7zBUh6s2Ca8eAURfnVHCTS': ['acoustic', 'emo', 'hyperpop', 'indie pop', 'punk'],  # THÉA — ANXIOLYTIQUES
    '3bnvoYUrPkgh0E3ZeYZ3me': ['dark electro', 'horrorcore', 'trap', 'pop rap', 'trap metal', 'rap', 'french', 'hip hop'],  # Changeline — OCTOPUS.LADY
    '7lc4ue2LiSfYRaABxq4YkT': ['dark electro', 'horrorcore', 'trap', 'pop rap', 'trap metal', 'rap', 'french', 'hip hop'],  # Changeline — JE.DÉTESTE.LA.FRANCE.pt1 (il y aura pas de pt2)
    '0wIpjjcXFgGtJUmBIRAAju': ['techno', 'broken beat', 'hardcore', 'sound collage', 'punk', 'rock', 'punk rock', 'folk punk'],  # Against Me! — Black Me Out
    '2inX5xyazBvcZYLx3wRBwh': ['indie', 'punk', 'malaysia'],  # Tingtongketz — Berubah
    '0ZQLRkRyn3300WyapdPoWT': ['acoustic', 'emo', 'hyperpop', 'indie pop', 'punk'],  # THÉA — CAVALE! CAVALE!
    '4NYRtDYROQW2D2ctcylcri': ['progressive house', 'progressive trance', 'pop rock', 'punk', 'hardcore punk', 'hardcore', 'queercore', 'd-beat'],  # G.L.O.S.S. — Targets of Men Targets of Men
    '1IF61ped0XehHvw2CFXP3B': ['punk', 'rock & roll', 'euro house', 'house', 'punk rock', 'garage rock', 'rock'],  # Jayne County — Man Enough To Be A Woman
    '7yeRNInEt2DOFYW0BkETEe': ['indie rock', 'rock & roll', 'blues rock', 'alternative rock', 'rock', 'indie', 'folk'],  # Ezra Furman — Restless Year
    '4b1Y41U44kP7gzO7MUNGbe': ['techno', 'broken beat', 'hardcore', 'sound collage', 'punk', 'punk rock', 'folk punk', 'rock'],  # Against Me! — Transgender Dysphoria Blues
    '0a0CwJBn8lmT5ifk63EUbP': ['techno', 'broken beat', 'hardcore', 'sound collage', 'acoustic rock', 'alternative rock', 'punk', 'rock', 'folk punk', 'folk rock', 'punk rock'],  # Against Me! — True Trans Soul Rebel
    '20JYh6XUjLjiN1CyJ32ZiY': ['dark electro', 'horrorcore', 'trap', 'pop rap', 'trap metal', 'rap', 'french', 'hip hop'],  # Changeline, Stolas — ANARCONNASSE
    '3eBY8aZZdWNnNhNbc8B0yp': [],  # Andra Venus — Power
    '3FysLYckiMCMzjYLIgo45U': ['horrorcore', 'electro', 'dubstep', 'industrial', 'industrial hip hop', 'trap', 'experimental hip hop'],  # Backxwash — BLACK SAILOR MOON
    '37OSQm8Gy5strUT24vn6ef': ['horrorcore', 'electro', 'dubstep', 'industrial', 'industrial hip hop', 'trap', 'experimental hip hop'],  # Backxwash, Ada Rook — I LIE HERE BURIED WITH MY RINGS AND MY DRESSES
    '2iqTYCPRTqojxM7QJvBtk2': ['drill', 'conscious', 'rap', 'hip hop'],  # Ms. Boogie — Breakdown
    '6JrmHzxhaaavRtlXTOhm63': ['rap', 'hip hop'],  # Quay Dash — Queen Of This Shit
    '3QF7smzmw2WWm7M1jt2Rac': ['ghana'],  # Angel Maxine, Wanlov The Kubolor, Sister Deborah — Wo Fie
    '1RkB4Dk0CDzpaSySq91JEA': ['pop', 'acoustic', 'argentina', 'hip hop', 'trap', 'mathcore'],  # Sasha Sathya — AKA LESBIANA SERPIENTA
    '4UfEEnq70NgLeq7NRfXPiD': ['french rap', 'rap'],  # LALLA RAMI — INCHALLAH
    '5nWecUJF2pytSxsSpylzZw': ['french rap', 'rap'],  # LALLA RAMI — 9A7BA
    '0A2tFUYLertZLltvvY5uyr': ['experimental', 'horrorcore', 'thug rap', 'trap', 'french', 'electronic', 'experimental hip hop', 'hip hop', 'digicore'],  # Ptite Soeur, Gemroz — KAYFABE
    '5Gp1fkuPV7CPtzKHfMH0kd': ['experimental', 'horrorcore', 'thug rap', 'trap', 'french', 'electronic', 'experimental hip hop', 'hip hop', 'digicore'],  # Ptite Soeur, neophron — ANFO჻
    '1PEPcLm2QEo0HCRIhQjPq1': ['future bass', 'indie pop', 'trap', 'leftfield', 'live', 'hyperpop', 'alt-pop', 'pop', 'indie'],  # underscores — Second hand embarrassment
    '7n7GrVTBmZMG4EULD5g0i3': ['hyperpop', 'hip hop', 'experimental', 'glitch', 'digicore', 'slowsilver03', 'emo rap', 'trap'],  # osquinn — warm and fuzzy
    '0VNjaRcmIowjLbPtYDhLuh': ['future bass', 'indie pop', 'trap', 'leftfield', 'alternative pop', 'alternative r&b', 'alternative rock', 'electronic', 'experimental', 'glitch pop', 'hyperpop', 'indie rock', 'pop', 'pop rock', 'rock', 'synth-pop', 'indietronica'],  # underscores, 8485 — Your favorite sidekick
    '1d3hBkCcMvVzsZjaMiVvNs': ['bubblegum', 'electroclash', 'house', 'hyperpop', 'dance-pop', 'electronic', 'pop', 'electropop'],  # Chase Icon — SRS
    '1RXkdiCc4TtwPacmIKyUnX': ['electroclash', 'dance-pop', 'hyperpop', 'hip-house', 'bitpop', 'bubblegum bass', 'electro house', 'electropop', 'euro-trance', 'miami bass', 'contemporary r&b', 'pop', 'atlanta bass', 'electronic', 'dance'],  # Ayesha Erotica — Vacation Bible School
    '54n3iwz9mr7yxZi1EOX1Mz': ['future bass', 'indie pop', 'trap', 'leftfield', 'electropop', 'indietronica', 'new rave', 'dance-pop', 'electroclash'],  # underscores, gabby start — Locals (Girls like us) [with gabby start]
    '6WkiWn8bf8S29wSk0VwK7h': ['hyperpop', 'dance-pop', 'electro', 'indie pop', 'electropop', 'electronic'],  # Frost Children — Falling
    '724utiMbqUfT1g3tqbfQYu': ['future bass', 'indie pop', 'trap', 'leftfield', 'hyperpop', 'pop punk', 'emo-pop', 'glitch'],  # underscores — Spoiled little brat
    '3RLI8S7KpEZs4SqePGjM2R': ['experimental', 'hyperpop', 'indie rock'],  # estelle allen — dui
    '1XD4K4CGAKTIBmFpvuaFru': ['trap', 'hyperpop', 'hardcore hip-hop', 'experimental', 'bass house', 'dariacore', 'digicore', 'electro hop', 'electroclash', 'electropop', 'experimental hip hop', 'future bass', 'rage', 'pop court with manda m', 'wsum 91.7 fm madison'],  # Jane Remover — Dancing with your eyes closed
    '2gmwvGC1yOw8NdMcZE8nfo': ['electroclash', 'dance-pop', 'hyperpop', 'hip-house', 'ballroom'],  # Ayesha Erotica — Literal Legend
    '1toNKayLMeCcVlsLGXJl7n': ['bubblegum', 'hyperpop', 'emo', 'experimental', 'electroclash', 'electropop', 'electronic', 'electroclash + electropop', 'my top songs'],  # Laura Les — Haunted
    '18QS9wnUr7DOhMb73monpK': ['hyperpop', 'pop', 'dance', 'electronic'],  # Mel 4Ever, Ayesha Erotica — Tongues
    '0Irj6PuEEGzi7JGJvAhdZ8': ['hyperpop', 'pop', 'dance', 'electronic'],  # Mel 4Ever — I Can’t Quit
    '06kFuqzhMk4E6IYeO0sTfx': ['hyperpop', 'dance-pop', 'electro', 'indie pop', 'fidget house', 'electropop', 'electroclash', 'electro house'],  # Frost Children, Kim Petras — RADIO (feat. Kim Petras)
    '2sVjF25Z4JTJxi9BXm5GtJ': ['breakcore', 'hardcore', 'footwork', 'juke', 'hexd', 'dance', 'digicore', 'digital hardcore', 'electronic', 'footwork jungle', 'gabber', 'hardcore breaks', 'horrorcore', 'rave', 'techno', 'cringecore', 'jungle dnb', 'rap', 'scream rap'],  # femtanyl — ACT RIGHT
    '51NYFGDXYKS4FkRqkw98hx': ['bubblegum', 'electroclash', 'house', 'hyperpop', 'dance-pop', 'electro house', 'electronic', 'hip hop', 'pop', 'electropop'],  # Chase Icon — Like Me
    '5iTzaatezJzsUhX1QjT0Kp': ['ambient', 'trance', 'electro', 'abstract', 'hyperpop', 'electronic'],  # Petal Supply — Person - Angel Mix
    '7kvQptbfqq5b4MWRQOMrZC': ['breakcore', 'hardcore', 'footwork', 'juke', 'hip hop', 'rap'],  # femtanyl, ISSBROKIE — NASTYWERKKKK!
    '6XeW8fjwoAFQeQpYojPtVI': ['breakcore', 'hardcore', 'footwork', 'juke', 'dance', 'digicore', 'digital hardcore', 'electronic', 'footwork jungle', 'gabber', 'hardcore breaks', 'hexd', 'horrorcore', 'rave', 'techno', 'cringecore', 'jungle dnb', 'rap', 'scream rap', 'drum and bass', 'energetic', 'edgy', 'dnb', 'edm', 'yumi', 'y2k'],  # femtanyl — GIRL HELL 1999
    '5iAE3uBqaZm9aHUx9yy6a0': ['breakcore', 'hardcore', 'footwork', 'juke', 'dance', 'digicore', 'digital hardcore', 'electronic', 'footwork jungle', 'gabber', 'hardcore breaks', 'hexd', 'horrorcore', 'rave', 'techno', 'cringecore', 'jungle dnb', 'rap', 'scream rap'],  # femtanyl — KATAMARI
    '1w0AFg23E67l57A3RMiXjC': ['breakcore', 'hardcore', 'footwork', 'juke', 'dance', 'digicore', 'digital hardcore', 'electronic', 'footwork jungle', 'gabber', 'hardcore breaks', 'hardstyle', 'hexd', 'horrorcore', 'hyperpop', 'rave', 'techno', 'cringecore', 'jungle dnb', 'rap', 'scream rap', 'pop'],  # femtanyl — P3T
    '5PMtJGEDIO0eIToF0YRUQ5': ['spanish', 'spain', 'booba'],  # JEDET — VENENO PA’ TU PIEL
    '2qpx5shtNEO1DuK8iEoJoB': ['hi nrg', 'disco', 'house', 'rnb/swing', 'drag', 'rnb', 'electro', 'american'],  # Peppermint — Best Sex
    '3BqWvhPear6eKPwhwJRFpO': ['house', 'dance-pop', 'disco', 'diva', 'american'],  # Mila Jam — Bruised
    '1jFN0stMzLepoPxvPywGZj': ['synth-pop', 'vocal', 'tribal house', 'house', 'dance-pop', 'electro-disco', 'electronic', 'electropop', 'nu disco', 'pop', 'german'],  # Kim Petras — Heart to Break
    '4QnHaiWq1oJiTgMnRFE0q8': ['electro', 'dance-pop', 'disco', 'house', 'pop', 'electronic', 'mexico', 'spanish'],  # Zemmoa, Tessa Ia, Trans-X — Mi Amor Soy Yo
    '2Of9piZALXa4CC7Unxoeeg': ['hip-house', 'tech house', 'hip hop', 'trap', 'puerto rico'],  # Villano Antillano — KLK
    '5lz6U9dCYBmEY6oLrW22VE': ['african', 'hip hop', 'techno', 'folk', 'angola', 'kuduro', 'pop'],  # Titica, Kelmer Pastilha, Mauro Xtraga — Olha a Banana
    '5srzGYocC4qYFvckQm5AfC': [],  # Haiifa Magic — To2i W Far2a3i
    '4xhYxKvAxtrRd83MiqOy29': ['synth-pop', 'vocal', 'tribal house', 'house', 'alternative pop', 'contemporary r&b', 'dance-pop', 'electronic', 'electropop', 'funktronica', 'nu disco', 'pop', 'pop rap', 'synth funk', 'teen pop', 'german'],  # Kim Petras — I Don’t Want It At All
    '1AFPmwB6mGMCcMI2hFh7c8': ['abstract', 'funk', 'techno', 'favela funk', 'brazilian', 'rap', 'experimental', 'brazil'],  # Linn da Quebrada — Enviadescer
    '1RmXibCbfLIVrN8ZRdoYbW': ['hyperpop', 'dance-pop', 'favela funk', 'house', 'pop', 'electronic', 'urias', 'brazilian'],  # Urias — Foi Mal
    '5pkemVhnBiIzMs2NLsXomQ': ['synth-pop', 'vocal', 'tribal house', 'house', 'contemporary r&b', 'pop rap', 'alternative r&b', 'bubblegum pop', 'dance-pop', 'disco', 'electronic', 'electropop', 'emo', 'glam rock', 'hip hop', 'pop', 'r&b', 'trap', 'german'],  # Kim Petras — Clarity
    '4ED8r6i90zmUG4kfbiVoou': ['house', 'nu disco', 'disco', 'rhythm & blues', 'alternative pop', 'chamber pop', 'rnb'],  # Ah-Mer-Ah-Su — Heartbreaker
    '4hceSKjrkDTO0nMKFcb3sj': ['techno', 'trap', 'reggaeton', 'electro', 'argentina', 'rap', 'latin'],  # Bizarrap, Villano Antillano — Villano Antillano: Bzrp Music Sessions, Vol. 51/66
    '46uGvJVhYHOVRRNnRPbkYm': [],  # Lucinta Luna, Dede Satria — Mantan Tanpa Status - Lucinta Luna Version
    '1YsFdaP9QG9NhjYS3o0g5P': ['african', 'hip hop', 'techno', 'folk', 'angola', 'kuduro', 'pop'],  # Titica, Ary — Olha o Boneco
    '7luHAaHXty1Nl3AcscZIDT': ['house', 'dance-pop', 'disco', 'diva', 'american'],  # Mila Jam — Faces
    '78iHtTxYIK2mD6oL6lXqFF': [],  # Gad Yola — Travesti del Perú
    '4Zhxtm6x56wEiRtSMAl28n': ['hyperpop', 'dance-pop', 'favela funk', 'house', 'pop', 'electronic', 'urias', 'brazilian'],  # Urias — Diaba
    '5dIPCgTEDagbcs5QGmni8V': ['house', 'electro house', 'contemporary r&b', 'neo soul'],  # MONĀE, Cae Monāe — CISPHOBIC
    '6yAc1rz1RXRlYJac99xusK': ['holiday', 'dance-pop', 'ballad', 'europop', 'swedish', 'melodifestivalen', 'melodifestivalen 2022', 'melfest'],  # Tone Sekelius — Girls & Dolls
    '376mhFeloWqzQJQsqZpm9A': ['dance-pop', 'europop'],  # Pupi Poisson, Arantxa Castilla-La Mancha, CARLES CUEVAS — Las Defectos
    '4OI2gBlHqyNks8cbIBIKYw': ['bass music', 'experimental', 'mandopop', 'idm', 'sound collage', 'electronic', 'ballroom', 'kuduro', 'uk bass', 'rpa'],  # Angel-Ho, K Rizz — Like A Girl
    '6D7zTed8zrkuKBPca2AqSI': ['brazilian', 'electronic', 'brazilian bass', 'funk brasileiro', 'brazilian funk', 'funk mandelao', 'rap'],  # Irmãs de Pau, Brunoso — Medley do Submundo
    '71yN0yrHej3jhKXewbmtEh': ['synth-pop', 'vocal', 'tribal house', 'house', 'contemporary r&b', 'dance-pop', 'electronic', 'electropop', 'europop', 'nu disco', 'pop', '1–4 wochen', 'offizielle charts', 'german'],  # Kim Petras — Coconuts
    '7bNgXJ9MgGG7xOkyz9SLOY': ['mpb', 'favela funk', 'funk', 'reggae', 'loonaids'],  # PEDRO SAMPAIO, Irmãs de Pau, Mc Gw, Tasha Kaiala, Clementaum — SEQUÊNCIA CUNT (feat. Clementaum)
    '4WhyfhjZaX6AVjAZslQAFs': ['urban conceitual', 'grunge', 'funk', 'indie funk'],  # Mulher Pepita, Brabo — Parceira
    '75HFFq9W7Em0dTBG8QeGcT': ['synth-pop', 'vocal', 'tribal house', 'house', 'dance-pop', 'electropop', 'pop', 'german', 'electronic'],  # Kim Petras — There Will Be Blood
    '1EPYnBjYhYHcNthEnVWk18': ['k-pop', 'house', 'rnb/swing', 'ballad', 'korean'],  # Harisu — 됐거든
    '0GSW6V6GJc4xYi8c5jOu60': ['j-pop'],  # Ai Haruna — さそり座の女
    '2lgwylOpGMtkvhwdnUOArt': ['schlager', 'euro-disco', 'dance-pop', 'chanson', 'verrucht', 'unglaublich', 'unfassbar', 'himmlisch', 'so scharf', 'pop'],  # Romy Haag — Memories Are Made Of This - Radio
    '4X6PkqzKUvWWKoq4YiiM1V': ['k-pop', 'house', 'rnb/swing', 'ballad', 'korean'],  # Harisu — Snow White
    '4yBfzgV6YA9dTKP8KUD35j': ['dance-pop', 'pop', 'sweden', 'hora'],  # Lia Larsson, Tone Sekelius, Lisa Ajax — VI ÄR SVERIGE (VM-låt 2023)
    '29Ga6IgetN8Xah85ZHZ8AC': ['villancicos', 'electroclash', 'holiday', 'euro house', 'pop', 'indie', 'alternative', 'electronic', 'spanish', 'electrotrash'],  # Samantha Hudson, Villano Antillano — Full Lace y el Tuck
    '0pe5NUU9uGwFpj637ot84D': [],  # Patricia Ribeiro — Conquistador
}
