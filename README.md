
###############################################################################################################################
# Leiticia Raab                                                                                                               #
# Projet réalisé dans le cadre d’un exercice Python pour comprendre la logique du Mastermind et manipuler les bases de Pygame.#
###############################################################################################################################

Mastermind revisité

Une version terminal (pour jouer directement dans la console)
Une version graphique 
Le but du jeu est simple : retrouver la combinaison secrète de couleurs en un nombre limité de tentatives.

Installation
Avant de lancer le jeu, installe les dépendances nécessaires avec la commande suivante :
pip install -r requirements.txt


Fonctionnement
À chaque tentative, tu proposes une combinaison de 4 couleurs.
Le jeu t’indique :
* (ou "Validée") → couleur bien placée
° (ou "À déplacer") → couleur présente mais mal placée
Si tu trouves les 4 bonnes couleurs au bon endroit, tu gagnes !
Si tu dépasses 10 essais… la combinaison secrète t’est révélée 

La version console te permet de jouer directement dans le terminal.
Elle est idéale pour comprendre la logique du jeu :
Aucune dépendance externe (juste Python ≥ 3.6)
Réponses en texte clair
Historique des essais affiché à chaque tour

