#!/usr/bin/env sh
# Publie le dépôt public en UN SEUL COMMIT, sans historique.
#
# Pourquoi. Une fiche retirée à la demande d'une artiste sortirait des pages mais
# resterait dans l'historique git, publiquement et pour toujours. Plutôt que de
# purger l'historique le jour du retrait, geste manuel à exécuter sans erreur au
# moment le plus difficile, le dépôt public n'a jamais d'historique du tout :
# chaque publication remplace la branche par un commit unique.
#
# L'historique de travail reste chez Claire, en local ou dans un dépôt privé.
#
# Usage, depuis Git Bash, dans le dossier du dépôt :
#     sh publier.sh "état au 9 septembre 2026"
set -e

MSG="${1:-Transfem chants}"

if [ ! -f index.html ]; then
  echo "À lancer depuis le dossier du dépôt (index.html introuvable ici)." >&2
  exit 1
fi

# La régénération n'est faite que si Python est installé. Quand les pages
# viennent d'un zip déjà compilé, il n'y a rien à régénérer et c'est normal.
if command -v python3 >/dev/null 2>&1; then
  echo "Régénération des pages…"
  python3 build.py
elif command -v python >/dev/null 2>&1; then
  echo "Régénération des pages…"
  python build.py
else
  echo "Python absent : publication des pages telles qu'elles sont dans le dossier."
  echo "C'est le cas normal si tu viens de décompresser le zip par-dessus."
fi

BRANCHE=$(git symbolic-ref --short HEAD)
echo
echo "Ce script va REMPLACER la branche « $BRANCHE » de origin par un commit unique."
echo "C'est le fonctionnement normal, à CHAQUE publication et pas seulement les"
echo "jours de retrait : un historique effacé de temps en temps se remarquerait,"
echo "un dépôt qui n'a jamais d'historique ne dit rien de particulier."
echo
echo "Le dépôt local perd aussi son historique. Pour en garder une copie, faire"
echo "  git branch archive-\$(date +%F)"
echo "avant de continuer. Elle reste chez toi et n'est jamais poussée."
printf "Continuer ? [oui/non] "
read REPONSE
[ "$REPONSE" = "oui" ] || { echo "Annulé."; exit 1; }

git checkout --orphan _publication
git add -A
git commit -m "$MSG"
git branch -D "$BRANCHE"
git branch -m "$BRANCHE"
git push --force origin "$BRANCHE"

echo
echo "Publié. Le dépôt public ne contient plus qu'un commit."
echo
echo "APRÈS UN RETRAIT D'ARTISTE, une étape de plus : un push forcé rend les"
echo "anciens objets inaccessibles mais ne les efface pas immédiatement des"
echo "serveurs de GitHub. Pour une garantie complète, supprimer le dépôt sur"
echo "GitHub et le recréer, puis pousser ce commit unique. On y perd les issues"
echo "et les étoiles ; on y gagne qu'il ne reste rien à retrouver."
