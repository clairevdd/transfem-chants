# -*- coding: utf-8 -*-
"""Sections et morceaux de la playlist. Ordre identique à la playlist Spotify.

Recatégorisation par familles de genres/scènes, remplaçant le découpage
géographique et de genre mêlé qui précédait. Voir claude/PROPOSITION-FAMILLES.md
pour la méthode : source de genre par ordre de fiabilité (Discogs > Last.fm au
morceau > Last.fm à l'artiste > Bandcamp > intensité audio), et les arbitrages
pris pour construire une proposition complète. Réordonnancement Spotify
effectué par Claire le 10 septembre 2026, à l'identique de la proposition.

L'ordre des morceaux à l'intérieur de chaque famille suit les « mouvements »
par intensité (energy - acousticness/2) arbitrés dans claude/MOUVEMENTS.md,
sauf Rap and hip-hop, séquencée par langue puis par artiste. Ces mouvements ne
sont pas des sous-sections publiées ; ils ne vivent que dans cet ordre et dans
le fichier de travail cité ci-dessus.
"""

SECTIONS = [
    {
        "title": 'Voice and few instruments',
        "blurb": 'Concert repertoire, folk revival and ballad, held together by very little besides a voice: a Handel aria, an Ottoman classical standard, an Andean vidalita, a Vietnamese nhạc vàng ballad, and the American folk circuit Beth Elliott sang on before anyone recorded her.',
        "tracks": [
            # I — plus nu
            ('1ovz0bZeO5YTBQTXIFf5Am', 'Ombra Mai Fu', 'Daniela Vega'),
            ('5l2zYkyTXtYa8xk965ofqD', 'Dream Variations', 'Tona Brown, Geraldine Boone'),
            ('1AHPsqF3EtHeWpOM06Y3Y4', 'Hope There\'s Someone', 'Antony and the Johnsons, ANOHNI'),
            ('5P9EKJfOZtuwtTR5C5362i', 'Sposa Son Disprezzata', 'Daniela Vega'),
            ('02L1ngagXNRt8W3Flbe9Sw', 'Boy in a Dress', 'Namoli Brennet'),
            ('1OpCGPKSq4IfpvLptsSMR9', 'I, Too', 'Tona Brown, Geraldine Boone'),
            ('1QrL7ucS71Ih4HXBOsuajv', 'Laabe Muxhe', 'La Bruja de Texcoco'),
            ('3nxFYWNFG2qGYEuhEzomtO', 'Vidalita, Vidalita', 'Susy Shock'),
            # II — plus saturé
            ('5e0ZXu358l51ckAZvai2Ef', 'Geceler', 'Bülent Ersoy'),
            ('4Ykmj47fulJ1FTeCXctW91', 'Anh Ta Bỏ Em Rồi', 'Hương Giang'),
            ('07m5UbUHOQCofRK16k83Eg', 'Duniya', 'Shyraa Roy, Kashif Ali'),
            ('73xUwV4DkcelY7seMyY0PY', 'Lady on the Subway', 'Beth Elliott'),
            ('4dtyeDMnVKKo89QbbDtD5M', 'Ballad of the Oklahoma Women\'s Liberation Front', 'Beth Elliott'),
            ('3BYSoeWlqUgIwfY77C8VgE', 'Té de Malvón', 'La Bruja de Texcoco'),
            ('7KtbrK74NNA4ySRZ49DC7R', 'Where the Lavender Grows', 'Mya Byrne'),
            ('0XIutL5epZuYV91bhCfFsR', 'Ümit Hırsızı', 'Bülent Ersoy'),
        ],
    },
    {
        "title": 'Soul, R&B and cabaret',
        "blurb": 'From Jackie Shane’s 1960s soul to contemporary R&B and gospel, with the cabaret and music-hall tradition running alongside it, from a steampunk revue to Coccinelle’s Paris stage.',
        "tracks": [
            # I — plus nu
            ('3MZjOGeXhpHbQ9ESMNFFnH', 'Honeybee', 'Steam Powered Giraffe'),
            ('3ApVA7ID6PkS0fGzNF4mFw', 'A Girl Like Me', 'Peppermint'),
            ('4CuivW1JgPauXPA4wYsf5K', 'Chercher la femme', 'Coccinelle'),
            ('5dtUOwEmnDAzsdodWJk4DA', 'Any Other Way', 'Jackie Shane'),
            ('5NnQ2xIeHDKc1B19rxfcV3', 'I Will Survive', 'Veronica Klaus'),
            ('0VhGzYfT2ZOFz31b5IH7yJ', 'Un garçon qui pleure', 'Marie France, Chrissie Hynde'),
            # II — plus saturé
            ('4P9LdSPrnQl7KQwml4DUtq', 'Baby 95', 'Liniker'),
            ('56xBg5e9rfrFqcqa4llUw7', 'Just Me (The Gender Binary Blues)', 'Jinkx Monsoon'),
            ('5WttRLHcZHhaIii5KwKh3Y', 'I Am Her', 'Shea Diamond'),
            ('0rK7QTyYjhPFadLH2YDl84', 'Picture of a Man', 'Our Lady J'),
            ('0gm0OruZdJlu8jamJe5OCh', 'Keisha Complexion', 'Shea Diamond'),
        ],
    },
    {
        "title": 'Electronic and auteur pop',
        "blurb": 'Producers and singer-songwriters writing in an electronic idiom of their own, from SOPHIE and Arca to ANOHNI — the most multilingual family on the playlist, reaching from South African art pop to Japanese, Thai and Hebrew ballads.',
        "tracks": [
            # I — plus nu
            ('3XdXixlx3MoVzfL7pu9hx6', 'Time', 'Arca'),
            ('0QA1xpUuqHDHWZhi0eAbH7', 'It\'s Okay To Cry', 'SOPHIE'),
            ('6EjxYTyXiBzJz6PeOvPiou', 'きみがすきだよ', 'Ataru Nakamura'),
            ('1N1F6UsRGILux57U0YbxJQ', 'Giọt Tình', 'Cindy Thái Tài'),
            ('7l8D5tXUVsdq95VQWn034C', '애지몽', 'Harisu'),
            ('0DZapO0gUF8XZpk2bu8AeL', 'היו לילות', 'Aderet'),
            ('3r0gvoaAkWmLdJO4UUv94v', 'Desafío', 'Arca'),
            ('2Ff6Ghw8TRJGuAbJamtt4X', 'Serotonin Serenade', 'SuperKnova'),
            ('48XnOS1vTyzqaPps0Dalzp', 'Ponyboy', 'SOPHIE'),
            ('7tktCNlB0877dhdPZSRb7T', 'Is It Cold In The Water?', 'SOPHIE'),
            # II — médian
            ('6JZfK4Z75nZm3VcZOVrpy0', 'Drone Bomb Me', 'ANOHNI'),
            ('0kNjtDBxrpjJTZn9w5Eq3C', 'I Take All the Blame', 'Vivek Shraya'),
            ('7EPHu29KqhsGk4dZAjM0o4', 'Cvnty', 'Stef Aranas'),
            ('2fB0l9upVjg0QTeMyrIVtc', 'Part-Time Woman', 'Vivek Shraya, Queer Songbook Orchestra'),
            ('2rN1ODOsaNfYu782rw36jR', 'Faceshopping', 'SOPHIE'),
            ('4lUlYGT5VvZWN3GBDIc9KT', 'Nonbinary', 'Arca'),
            ('2KryklrVDGmWL8IvoGNbb5', 'Zulu Lami', 'Umlilo'),
            ('5nnBHHzUDOGvdMBiXofB00', 'Exiliades', 'Luisa Almaguer'),
            ('5rOzcHIZaF038jMeHkUZR0', 'Reverie', 'Arca'),
            # III — plus saturé
            ('6jiumfqTwOpXW6PDzsIBKl', 'I Keep Doing This to Myself', 'Sonja Sajzor'),
            ('6JGJdnIbq4UqKgzFaOIXwE', 'Mataronomatar', 'Luisa Almaguer'),
            ('0NOume8OgBz4FCnP1QVr9A', 'Paradise', 'Bell Nuntita'),
            ('3z4KIXgkhLauhNP3ubB8cF', '6 Feet', 'Left at London'),
            ('2BQZhUPXdP9Nk1X84c7PtP', 'Unseen (feat. Celeste)', 'Lauren Auder, Celeste'),
            ('2CznvTOsuLh0USpHJqEc6V', 'Motorcycle', 'June Jones, Geryon'),
            ('3IDQXyHYuX2rdLnNfVzT3g', '4 DEGREES', 'ANOHNI'),
            ('1huN927tTdSiwF90FBHXkT', 'Immaterial', 'SOPHIE'),
            ('3qBg6BeHJlGgwl5aCa09EC', 'Revolution Lover', 'Left at London'),
            ('6RJiY28t9jWpdy1JkUhNgK', 'Mequetrefe', 'Arca'),
            ('2PaTBoG5uDz6H3xPhnnDLz', 'Digital Empathy', 'Trevi Moran'),
        ],
    },
    {
        "title": 'Punk, rock and metal',
        "blurb": 'Four generations of guitars, from Jayne County in the 1970s to Grenoble trap metal in the 2020s: punk, hardcore, glam and heartland rock, by way of Paris and the Palace.',
        "tracks": [
            # I — plus nu
            ('3Vk1AHIh1CoiQzFroldMhO', 'Take My Shoulder (feat. Laura Jane Grace)', 'Venus De Mars'),
            ('2DUAIlPmzV2is5OQIZASUA', 'T4T', 'Anita Velveeta'),
            ('3ShIGvHRm0q9iIDowUMjls', 'The Best Ever Death Metal Band in Denton', 'Laura Jane Grace'),
            ('2jFP4mAHcDmGe7DEKKLyJa', 'Skin On Skin', 'jasmine.4.t'),
            ('7GAI6zWpmst6dSfu1wIA1O', 'White Horses', 'Venus de Mars and All the Pretty Horses'),
            ('3RXajeZOzqXWrQwLDfTzKK', 'JUSTE AMIS', 'THÉA'),
            ('0bWpWsvZeTTNLQ9nuXqKIN', 'Guillotine', 'THÉA'),
            # II — médian
            ('3zGmkzXqXsXYVlGzJFpgCW', 'Boys', 'Venus de Mars and All the Pretty Horses'),
            ('4ltqfN12ohaVZdM6C45gMg', 'American Teenager', 'Ethel Cain'),
            ('14uL43Gg4ujizaATehrryk', 'The Ocean', 'Against Me!'),
            ('7zBUh6s2Ca8eAURfnVHCTS', 'ANXIOLYTIQUES', 'THÉA'),
            ('3bnvoYUrPkgh0E3ZeYZ3me', 'OCTOPUS.LADY', 'Changeline'),
            ('7lc4ue2LiSfYRaABxq4YkT', 'JE.DÉTESTE.LA.FRANCE.pt1 (il y aura pas de pt2)', 'Changeline'),
            ('0wIpjjcXFgGtJUmBIRAAju', 'Black Me Out', 'Against Me!'),
            ('2inX5xyazBvcZYLx3wRBwh', 'Berubah', 'Tingtongketz'),
            # III — plus saturé
            ('0ZQLRkRyn3300WyapdPoWT', 'CAVALE! CAVALE!', 'THÉA'),
            ('4NYRtDYROQW2D2ctcylcri', 'Targets of Men Targets of Men', 'G.L.O.S.S.'),
            ('1IF61ped0XehHvw2CFXP3B', 'Man Enough To Be A Woman', 'Jayne County'),
            ('7yeRNInEt2DOFYW0BkETEe', 'Restless Year', 'Ezra Furman'),
            ('4b1Y41U44kP7gzO7MUNGbe', 'Transgender Dysphoria Blues', 'Against Me!'),
            ('0a0CwJBn8lmT5ifk63EUbP', 'True Trans Soul Rebel', 'Against Me!'),
            ('20JYh6XUjLjiN1CyJ32ZiY', 'ANARCONNASSE', 'Changeline, Stolas'),
        ],
    },
    {
        "title": 'Rap and hip-hop',
        "blurb": 'The most directly political stretch, from Ghana to the Buenos Aires conurbano, by way of Casablanca and the French rap underground.',
        "tracks": [
            # anglais
            ('3eBY8aZZdWNnNhNbc8B0yp', 'Power', 'Andra Venus'),
            ('3FysLYckiMCMzjYLIgo45U', 'BLACK SAILOR MOON', 'Backxwash'),
            ('37OSQm8Gy5strUT24vn6ef', 'I LIE HERE BURIED WITH MY RINGS AND MY DRESSES', 'Backxwash, Ada Rook'),
            ('2iqTYCPRTqojxM7QJvBtk2', 'Breakdown', 'Ms. Boogie'),
            ('6JrmHzxhaaavRtlXTOhm63', 'Queen Of This Shit', 'Quay Dash'),
            # twi/anglais (Ghana)
            ('3QF7smzmw2WWm7M1jt2Rac', 'Wo Fie', 'Angel Maxine, Wanlov The Kubolor, Sister Deborah'),
            # espagnol (Argentine)
            ('1RkB4Dk0CDzpaSySq91JEA', 'AKA LESBIANA SERPIENTA', 'Sasha Sathya'),
            # darija/français (Maroc)
            ('4UfEEnq70NgLeq7NRfXPiD', 'INCHALLAH', 'LALLA RAMI'),
            ('5nWecUJF2pytSxsSpylzZw', '9A7BA', 'LALLA RAMI'),
            # français
            ('0A2tFUYLertZLltvvY5uyr', 'KAYFABE', 'Ptite Soeur, Gemroz'),
            ('5Gp1fkuPV7CPtzKHfMH0kd', 'ANFO჻', 'Ptite Soeur, neophron'),
        ],
    },
    {
        "title": 'Hyperpop and digicore',
        "blurb": 'The playlist’s online-native scene, and its most anglophone stretch: digicore, breakcore and bubblegum bass, almost all of it from the years either side of 2020.',
        "tracks": [
            # I — plus nu
            ('0ZeVhHgvMsF6dqo2AFSfut', "i'm 2 years on hormones and i'm still sad i want a refund", 'TAMAGOTCHI MASSACRE'),
            ('1PEPcLm2QEo0HCRIhQjPq1', 'Second hand embarrassment', 'underscores'),
            ('7n7GrVTBmZMG4EULD5g0i3', 'warm and fuzzy', 'osquinn'),
            ('0VNjaRcmIowjLbPtYDhLuh', 'Your favorite sidekick', 'underscores, 8485'),
            ('1d3hBkCcMvVzsZjaMiVvNs', 'SRS', 'Chase Icon'),
            ('1RXkdiCc4TtwPacmIKyUnX', 'Vacation Bible School', 'Ayesha Erotica'),
            ('54n3iwz9mr7yxZi1EOX1Mz', 'Locals (Girls like us) [with gabby start]', 'underscores, gabby start'),
            ('6WkiWn8bf8S29wSk0VwK7h', 'Falling', 'Frost Children'),
            ('724utiMbqUfT1g3tqbfQYu', 'Spoiled little brat', 'underscores'),
            ('3RLI8S7KpEZs4SqePGjM2R', 'dui', 'estelle allen'),
            ('1XD4K4CGAKTIBmFpvuaFru', 'Dancing with your eyes closed', 'Jane Remover'),
            ('2gmwvGC1yOw8NdMcZE8nfo', 'Literal Legend', 'Ayesha Erotica'),
            # II — plus saturé
            ('1toNKayLMeCcVlsLGXJl7n', 'Haunted', 'Laura Les'),
            ('18QS9wnUr7DOhMb73monpK', 'Tongues', 'Mel 4Ever, Ayesha Erotica'),
            ('0Irj6PuEEGzi7JGJvAhdZ8', 'I Can\'t Quit', 'Mel 4Ever'),
            ('06kFuqzhMk4E6IYeO0sTfx', 'RADIO (feat. Kim Petras)', 'Frost Children, Kim Petras'),
            ('2sVjF25Z4JTJxi9BXm5GtJ', 'ACT RIGHT', 'femtanyl'),
            ('51NYFGDXYKS4FkRqkw98hx', 'Like Me', 'Chase Icon'),
            ('5iTzaatezJzsUhX1QjT0Kp', 'Person - Angel Mix', 'Petal Supply'),
            ('7kvQptbfqq5b4MWRQOMrZC', 'NASTYWERKKKK!', 'femtanyl, ISSBROKIE'),
            ('6XeW8fjwoAFQeQpYojPtVI', 'GIRL HELL 1999', 'femtanyl'),
            ('5iAE3uBqaZm9aHUx9yy6a0', 'KATAMARI', 'femtanyl'),
            ('1w0AFg23E67l57A3RMiXjC', 'P3T', 'femtanyl'),
            ('4DfHQvIAZmSmqcZbuO80sZ', 'Days of Girlhood', 'Dylan Mulvaney'),
        ],
    },
    {
        "title": 'Club, funk and dance-pop',
        "blurb": 'The largest family on the playlist: house, disco, favela funk, kuduro and dance-pop from four continents, from Berlin schlager to Rio funk carioca.',
        "tracks": [
            # I — plus nu
            ('5PMtJGEDIO0eIToF0YRUQ5', 'VENENO PA\' TU PIEL', 'JEDET'),
            ('2qpx5shtNEO1DuK8iEoJoB', 'Best Sex', 'Peppermint'),
            ('3BqWvhPear6eKPwhwJRFpO', 'Bruised', 'Mila Jam'),
            ('1jFN0stMzLepoPxvPywGZj', 'Heart to Break', 'Kim Petras'),
            ('4QnHaiWq1oJiTgMnRFE0q8', 'Mi Amor Soy Yo', 'Zemmoa, Tessa Ia, Trans-X'),
            ('2Of9piZALXa4CC7Unxoeeg', 'KLK', 'Villano Antillano'),
            ('5lz6U9dCYBmEY6oLrW22VE', 'Olha a Banana', 'Titica, Kelmer Pastilha, Mauro Xtraga'),
            ('5srzGYocC4qYFvckQm5AfC', 'To2i W Far2a3i', 'Haiifa Magic'),
            ('4xhYxKvAxtrRd83MiqOy29', 'I Don\'t Want It At All', 'Kim Petras'),
            ('1AFPmwB6mGMCcMI2hFh7c8', 'Enviadescer', 'Linn da Quebrada'),
            ('1RmXibCbfLIVrN8ZRdoYbW', 'Foi Mal', 'Urias'),
            ('5pkemVhnBiIzMs2NLsXomQ', 'Clarity', 'Kim Petras'),
            # II — médian
            ('4ED8r6i90zmUG4kfbiVoou', 'Heartbreaker', 'Ah-Mer-Ah-Su'),
            ('4hceSKjrkDTO0nMKFcb3sj', 'Villano Antillano: Bzrp Music Sessions, Vol. 51/66', 'Bizarrap, Villano Antillano'),
            ('46uGvJVhYHOVRRNnRPbkYm', 'Mantan Tanpa Status - Lucinta Luna Version', 'Lucinta Luna, Dede Satria'),
            ('1YsFdaP9QG9NhjYS3o0g5P', 'Olha o Boneco', 'Titica, Ary'),
            ('7luHAaHXty1Nl3AcscZIDT', 'Faces', 'Mila Jam'),
            ('78iHtTxYIK2mD6oL6lXqFF', 'Travesti del Perú', 'Gad Yola'),
            ('4Zhxtm6x56wEiRtSMAl28n', 'Diaba', 'Urias'),
            ('5dIPCgTEDagbcs5QGmni8V', 'CISPHOBIC', 'MONĀE, Cae Monāe'),
            ('6yAc1rz1RXRlYJac99xusK', 'Girls & Dolls', 'Tone Sekelius'),
            ('376mhFeloWqzQJQsqZpm9A', 'Las Defectos', 'Pupi Poisson, Arantxa Castilla-La Mancha, CARLES CUEVAS'),
            ('4OI2gBlHqyNks8cbIBIKYw', 'Like A Girl', 'Angel-Ho, K Rizz'),
            # III — plus saturé
            ('6D7zTed8zrkuKBPca2AqSI', 'Medley do Submundo', 'Irmãs de Pau, Brunoso'),
            ('71yN0yrHej3jhKXewbmtEh', 'Coconuts', 'Kim Petras'),
            ('7bNgXJ9MgGG7xOkyz9SLOY', 'SEQUÊNCIA CUNT (feat. Clementaum)', 'PEDRO SAMPAIO, Irmãs de Pau, Mc Gw, Tasha Kaiala, Clementaum'),
            ('4WhyfhjZaX6AVjAZslQAFs', 'Parceira', 'Mulher Pepita, Brabo'),
            ('75HFFq9W7Em0dTBG8QeGcT', 'There Will Be Blood', 'Kim Petras'),
            ('1EPYnBjYhYHcNthEnVWk18', '됐거든', 'Harisu'),
            ('0GSW6V6GJc4xYi8c5jOu60', 'さそり座の女', 'Ai Haruna'),
            ('2lgwylOpGMtkvhwdnUOArt', 'Memories Are Made Of This - Radio', 'Romy Haag'),
            ('4X6PkqzKUvWWKoq4YiiM1V', 'Snow White', 'Harisu'),
            ('4yBfzgV6YA9dTKP8KUD35j', 'VI ÄR SVERIGE (VM-låt 2023)', 'Lia Larsson, Tone Sekelius, Lisa Ajax'),
            ('29Ga6IgetN8Xah85ZHZ8AC', 'Full Lace y el Tuck', 'Samantha Hudson, Villano Antillano'),
            ('0pe5NUU9uGwFpj637ot84D', 'Conquistador', 'Patricia Ribeiro'),
            ('3qDqg53YIe9mM5Ehx9v9FZ', 'El Rap de la Veneno', 'La Veneno'),
            ('6fd79PtewFZgLXYiIYhhLJ', 'La Drácula', 'Ella'),
            ('4OF1mdSkA2z05DSwHNKVnz', 'Hasta Que Salga el Sol', 'Wendy Guevara'),
        ],
    },
]


def all_tracks():
    return [t for s in SECTIONS for t in s["tracks"]]


assert len(all_tracks()) == 152
