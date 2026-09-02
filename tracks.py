# -*- coding: utf-8 -*-
"""Les morceaux de la playlist, dans l'ordre, groupés par section.

Chaque morceau est un triplet (identifiant Spotify, titre, crédit).
L'identifiant est les 22 caractères qui suivent /track/ dans une URL Spotify :
il doit toujours provenir d'une URL réellement consultée, jamais être reconstitué.

Le crédit liste les artistes séparés par des virgules ; chaque nom doit exister
comme clé dans data.py, sinon le build échoue.

Ordre repris de la playlist Spotify elle-même (export du 28 août 2026, 119 titres).
Ajouter un morceau : insérer une ligne dans la section voulue. Rien d'autre.
"""

SECTIONS = [
 {
  "title": "Electronic and art pop",
  "blurb": "From SOPHIE to Arca, with a detour into Turkish classical singing at the point where ANOHNI’s register invites it.",
  "tracks": [
   ("0QA1xpUuqHDHWZhi0eAbH7", "It's Okay To Cry", "SOPHIE"),
   ("1huN927tTdSiwF90FBHXkT", "Immaterial", "SOPHIE"),
   ("2rN1ODOsaNfYu782rw36jR", "Faceshopping", "SOPHIE"),
   ("7tktCNlB0877dhdPZSRb7T", "Is It Cold In The Water?", "SOPHIE"),
   ("48XnOS1vTyzqaPps0Dalzp", "Ponyboy", "SOPHIE"),
   ("4lUlYGT5VvZWN3GBDIc9KT", "Nonbinary", "Arca"),
   ("3XdXixlx3MoVzfL7pu9hx6", "Time", "Arca"),
   ("5rOzcHIZaF038jMeHkUZR0", "Reverie", "Arca"),
   ("3r0gvoaAkWmLdJO4UUv94v", "Desafío", "Arca"),
   ("6RJiY28t9jWpdy1JkUhNgK", "Mequetrefe", "Arca"),
   ("6JZfK4Z75nZm3VcZOVrpy0", "Drone Bomb Me", "ANOHNI"),
   ("3IDQXyHYuX2rdLnNfVzT3g", "4 DEGREES", "ANOHNI"),
   ("2BQZhUPXdP9Nk1X84c7PtP", "Unseen (feat. Celeste)", "Lauren Auder, Celeste"),
   ("5e0ZXu358l51ckAZvai2Ef", "Geceler", "Bülent Ersoy"),
   ("0XIutL5epZuYV91bhCfFsR", "Ümit Hırsızı", "Bülent Ersoy"),
   ("1AHPsqF3EtHeWpOM06Y3Y4", "Hope There's Someone", "Antony and the Johnsons, ANOHNI"),
  ],
 },
 {
  "title": "Hyperpop and club",
  "blurb": "The dancing core of the playlist, shifting gradually from English into Spanish and then Angolan Portuguese.",
  "tracks": [
   ("1jFN0stMzLepoPxvPywGZj", "Heart to Break", "Kim Petras"),
   ("5pkemVhnBiIzMs2NLsXomQ", "Clarity", "Kim Petras"),
   ("4xhYxKvAxtrRd83MiqOy29", "I Don't Want It At All", "Kim Petras"),
   ("75HFFq9W7Em0dTBG8QeGcT", "There Will Be Blood", "Kim Petras"),
   ("71yN0yrHej3jhKXewbmtEh", "Coconuts", "Kim Petras"),
   ("1toNKayLMeCcVlsLGXJl7n", "Haunted", "Laura Les"),
   ("1w0AFg23E67l57A3RMiXjC", "P3T", "femtanyl"),
   ("2sVjF25Z4JTJxi9BXm5GtJ", "ACT RIGHT", "femtanyl"),
   ("6XeW8fjwoAFQeQpYojPtVI", "GIRL HELL 1999", "femtanyl"),
   ("5iAE3uBqaZm9aHUx9yy6a0", "KATAMARI", "femtanyl"),
   ("17iGTeBSC6VtWESUk1YqYh", "MURDER EVERY 1 U KNOW!", "femtanyl, takihasdied"),
   ("7kvQptbfqq5b4MWRQOMrZC", "NASTYWERKKKK!", "femtanyl, ISSBROKIE"),
   ("724utiMbqUfT1g3tqbfQYu", "Spoiled little brat", "underscores"),
   ("1PEPcLm2QEo0HCRIhQjPq1", "Second hand embarrassment", "underscores"),
   ("0VNjaRcmIowjLbPtYDhLuh", "Your favorite sidekick", "underscores, 8485"),
   ("54n3iwz9mr7yxZi1EOX1Mz", "Locals (Girls like us) [with gabby start]", "underscores, gabby start"),
   ("5dIPCgTEDagbcs5QGmni8V", "CISPHOBIC", "MONĀE, Cae Monāe"),
   ("5iTzaatezJzsUhX1QjT0Kp", "Person - Angel Mix", "Petal Supply"),
   ("51NYFGDXYKS4FkRqkw98hx", "Like Me", "Chase Icon"),
   ("1d3hBkCcMvVzsZjaMiVvNs", "SRS", "Chase Icon"),
   ("0Irj6PuEEGzi7JGJvAhdZ8", "I Can't Quit", "Mel 4Ever"),
   ("18QS9wnUr7DOhMb73monpK", "Tongues", "Mel 4Ever, Ayesha Erotica"),
   ("7EPHu29KqhsGk4dZAjM0o4", "Cvnty", "Stef Aranas"),
   ("1RXkdiCc4TtwPacmIKyUnX", "Vacation Bible School", "Ayesha Erotica"),
   ("2gmwvGC1yOw8NdMcZE8nfo", "Literal Legend", "Ayesha Erotica"),
   ("1XD4K4CGAKTIBmFpvuaFru", "Dancing with your eyes closed", "Jane Remover"),
   ("3RLI8S7KpEZs4SqePGjM2R", "dui", "estelle allen"),
   ("7n7GrVTBmZMG4EULD5g0i3", "warm and fuzzy", "osquinn"),
   ("6WkiWn8bf8S29wSk0VwK7h", "Falling", "Frost Children"),
   ("06kFuqzhMk4E6IYeO0sTfx", "RADIO (feat. Kim Petras)", "Frost Children, Kim Petras"),
   ("2Of9piZALXa4CC7Unxoeeg", "KLK", "Villano Antillano"),
   ("4hceSKjrkDTO0nMKFcb3sj", "Villano Antillano: Bzrp Music Sessions, Vol. 51/66", "Bizarrap, Villano Antillano"),
   ("5PMtJGEDIO0eIToF0YRUQ5", "VENENO PA' TU PIEL", "JEDET"),
   ("1YsFdaP9QG9NhjYS3o0g5P", "Olha o Boneco", "Titica, Ary"),
   ("5lz6U9dCYBmEY6oLrW22VE", "Olha a Banana", "Titica, Kelmer Pastilha, Mauro Xtraga"),
  ],
 },
 {
  "title": "Punk and rock",
  "blurb": "Three generations of trans glam and punk, from Jayne County in the 1970s to Venus De Mars in 1988, by way of Paris and the Palace.",
  "tracks": [
   ("0a0CwJBn8lmT5ifk63EUbP", "True Trans Soul Rebel", "Against Me!"),
   ("4b1Y41U44kP7gzO7MUNGbe", "Transgender Dysphoria Blues", "Against Me!"),
   ("14uL43Gg4ujizaATehrryk", "The Ocean", "Against Me!"),
   ("0wIpjjcXFgGtJUmBIRAAju", "Black Me Out", "Against Me!"),
   ("2DUAIlPmzV2is5OQIZASUA", "T4T", "Anita Velveeta"),
   ("7yeRNInEt2DOFYW0BkETEe", "Restless Year", "Ezra Furman"),
   ("4NYRtDYROQW2D2ctcylcri", "Targets of Men Targets of Men", "G.L.O.S.S."),
   ("3ShIGvHRm0q9iIDowUMjls", "The Best Ever Death Metal Band in Denton", "Laura Jane Grace"),
   ("1IF61ped0XehHvw2CFXP3B", "Man Enough To Be A Woman", "Jayne County"),
   ("0VhGzYfT2ZOFz31b5IH7yJ", "Un garçon qui pleure", "Marie France, Chrissie Hynde"),
   ("3zGmkzXqXsXYVlGzJFpgCW", "Boys", "Venus de Mars and All the Pretty Horses"),
   ("7GAI6zWpmst6dSfu1wIA1O", "White Horses", "Venus de Mars and All the Pretty Horses"),
   ("3Vk1AHIh1CoiQzFroldMhO", "Take My Shoulder (feat. Laura Jane Grace)", "Venus De Mars"),
   ("2inX5xyazBvcZYLx3wRBwh", "Berubah", "Tingtongketz"),
  ],
 },
 {
  "title": "Indie, folk and traditional music",
  "blurb": "The inward-facing stretch, where Mexican and Argentine traditional forms are reclaimed from a transfeminine position.",
  "tracks": [
   ("4dtyeDMnVKKo89QbbDtD5M", "Ballad of the Oklahoma Women's Liberation Front", "Beth Elliott"),
   ("02L1ngagXNRt8W3Flbe9Sw", "Boy in a Dress", "Namoli Brennet"),
   ("7KtbrK74NNA4ySRZ49DC7R", "Where the Lavender Grows", "Mya Byrne"),
   ("3qBg6BeHJlGgwl5aCa09EC", "Revolution Lover", "Left at London"),
   ("3z4KIXgkhLauhNP3ubB8cF", "6 Feet", "Left at London"),
   ("2CznvTOsuLh0USpHJqEc6V", "Motorcycle", "June Jones, Geryon"),
   ("2jFP4mAHcDmGe7DEKKLyJa", "Skin On Skin", "jasmine.4.t"),
   ("0kNjtDBxrpjJTZn9w5Eq3C", "I Take All the Blame", "Vivek Shraya"),
   ("2fB0l9upVjg0QTeMyrIVtc", "Part-Time Woman", "Vivek Shraya, Queer Songbook Orchestra"),
   ("5nnBHHzUDOGvdMBiXofB00", "Exiliades", "Luisa Almaguer"),
   ("6JGJdnIbq4UqKgzFaOIXwE", "Mataronomatar", "Luisa Almaguer"),
   ("3nxFYWNFG2qGYEuhEzomtO", "Vidalita, Vidalita", "Susy Shock"),
   ("3BYSoeWlqUgIwfY77C8VgE", "Té de Malvón", "La Bruja de Texcoco"),
   ("1QrL7ucS71Ih4HXBOsuajv", "Laabe Muxhe", "La Bruja de Texcoco"),
   ("4ltqfN12ohaVZdM6C45gMg", "American Teenager", "Ethel Cain"),
   ("3MZjOGeXhpHbQ9ESMNFFnH", "Honeybee", "Steam Powered Giraffe"),
   ("2Ff6Ghw8TRJGuAbJamtt4X", "Serotonin Serenade", "SuperKnova"),
  ],
 },
 {
  "title": "Soul and R&B",
  "blurb": "From Jackie Shane’s 1960s soul to contemporary R&B.",
  "tracks": [
   ("5dtUOwEmnDAzsdodWJk4DA", "Any Other Way", "Jackie Shane"),
   ("5NnQ2xIeHDKc1B19rxfcV3", "I Will Survive", "Veronica Klaus"),
   ("56xBg5e9rfrFqcqa4llUw7", "Just Me (The Gender Binary Blues)", "Jinkx Monsoon"),
   ("5WttRLHcZHhaIii5KwKh3Y", "I Am Her", "Shea Diamond"),
   ("0gm0OruZdJlu8jamJe5OCh", "Keisha Complexion", "Shea Diamond"),
   ("3BqWvhPear6eKPwhwJRFpO", "Bruised", "Mila Jam"),
   ("7luHAaHXty1Nl3AcscZIDT", "Faces", "Mila Jam"),
   ("2qpx5shtNEO1DuK8iEoJoB", "Best Sex", "Peppermint"),
   ("3ApVA7ID6PkS0fGzNF4mFw", "A Girl Like Me", "Peppermint"),
   ("4ED8r6i90zmUG4kfbiVoou", "Heartbreaker", "Ah-Mer-Ah-Su"),
   ("0rK7QTyYjhPFadLH2YDl84", "Picture of a Man", "Our Lady J"),
  ],
 },
 {
  "title": "International pop",
  "blurb": "Portugal, Lebanon, South Korea, Vietnam, Thailand, Japan. The section furthest from the anglophone axis.",
  "tracks": [
   ("0pe5NUU9uGwFpj637ot84D", "Conquistador", "Patricia Ribeiro"),
   ("5srzGYocC4qYFvckQm5AfC", "To2i W Far2a3i", "Haiifa Magic"),
   ("4X6PkqzKUvWWKoq4YiiM1V", "Snow White", "Harisu"),
   ("7l8D5tXUVsdq95VQWn034C", "애지몽", "Harisu"),
   ("1EPYnBjYhYHcNthEnVWk18", "됐거든", "Harisu"),
   ("4Ykmj47fulJ1FTeCXctW91", "Anh Ta Bỏ Em Rồi", "Hương Giang"),
   ("0NOume8OgBz4FCnP1QVr9A", "Paradise", "Bell Nuntita"),
   ("0GSW6V6GJc4xYi8c5jOu60", "さそり座の女", "Ai Haruna"),
   ("6EjxYTyXiBzJz6PeOvPiou", "きみがすきだよ", "Ataru Nakamura"),
  ],
 },
 {
  "title": "Lusophone",
  "blurb": "Funk carioca, MPB and Brazilian soul.",
  "tracks": [
   ("4Zhxtm6x56wEiRtSMAl28n", "Diaba", "Urias"),
   ("1RmXibCbfLIVrN8ZRdoYbW", "Foi Mal", "Urias"),
   ("4P9LdSPrnQl7KQwml4DUtq", "Baby 95", "Liniker"),
   ("1AFPmwB6mGMCcMI2hFh7c8", "Enviadescer", "Linn da Quebrada"),
   ("4WhyfhjZaX6AVjAZslQAFs", "Parceira", "Mulher Pepita, Brabo"),
  ],
 },
 {
  "title": "Rap and hip-hop",
  "blurb": "The most directly political stretch, from Ghana to the Buenos Aires conurbano.",
  "tracks": [
   ("3FysLYckiMCMzjYLIgo45U", "BLACK SAILOR MOON", "Backxwash"),
   ("37OSQm8Gy5strUT24vn6ef", "I LIE HERE BURIED WITH MY RINGS AND MY DRESSES", "Backxwash, Ada Rook"),
   ("3QF7smzmw2WWm7M1jt2Rac", "Wo Fie", "Angel Maxine, Wanlov The Kubolor, Sister Deborah"),
   ("6JrmHzxhaaavRtlXTOhm63", "Queen Of This Shit", "Quay Dash"),
   ("2iqTYCPRTqojxM7QJvBtk2", "Breakdown", "Ms. Boogie"),
   ("3eBY8aZZdWNnNhNbc8B0yp", "Power", "Andra Venus"),
   ("1RkB4Dk0CDzpaSySq91JEA", "AKA LESBIANA SERPIENTA", "Sasha Sathya"),
   ("4UfEEnq70NgLeq7NRfXPiD", "INCHALLAH", "LALLA RAMI"),
   ("5nWecUJF2pytSxsSpylzZw", "9A7BA", "LALLA RAMI"),
   ("5Gp1fkuPV7CPtzKHfMH0kd", "ANFO჻", "Ptite Soeur, neophron"),
   ("0A2tFUYLertZLltvvY5uyr", "KAYFABE", "Ptite Soeur, Gemroz"),
  ],
 },
 {
  "title": "Closing",
  "blurb": "A historical citation: the first French public figure to change her civil status, in 1959, singing “Chercher la femme”.",
  "tracks": [
   ("4CuivW1JgPauXPA4wYsf5K", "Chercher la femme", "Coccinelle"),
  ],
 },
]


def all_tracks():
    """Les morceaux à plat, dans l'ordre de la playlist."""
    return [t for s in SECTIONS for t in s["tracks"]]


if __name__ == "__main__":
    ts = all_tracks()
    ids = [t[0] for t in ts]
    assert len(set(ids)) == len(ids), "identifiant Spotify en double"
    assert all(len(i) == 22 for i in ids), "identifiant Spotify de longueur inattendue"
    print(len(ts), "morceaux,", len(SECTIONS), "sections")
