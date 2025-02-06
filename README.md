# Projet Optimisation Appliquée : conception d’un jeu combinatoire
## Contexte
Le jeu « monstres-sous-le-lit » est un puzzle combinatoire qui consiste à positionner des formes
géométriques sur un plateau afin de ne laisser apparaitre que certaines images. Différents niveaux de
difficultés sont définis pour ces défis.
Le descriptif du jeu est disponible ici : https://www.smartgames.eu/fr/jeux-pour-1-joueur/monstressous-le-lit
Il existe d’autres variantes de ce même jeu (Cache-cache Safari ou encore Pirates Cache-cache).
## Objectifs
L’objectif du projet est d’utiliser la programmation par contraintes pour résoudre plusieurs tâches.
- Moteur de résolution : il s’agira de modéliser le problème sous forme d’un problème de
satisfaction de contraintes (CSP). Ce modèle permettra alors de calculer la solution unique
d’un défi donné. Il est possible d’utiliser les ressources disponibles pour trouver les défis.
Vous analyser la difficulté des défis relativement à la difficulté de la résolution de votre CSP.
- Générateur de défis : utiliser le modèle précédent pour générer des défis réalisables, c’est-àdire pour lesquels il n’existe qu’une seule solution. On pourra demander à l’utilisateur de
fournir un défi et vérifier s’il est jouable.
- Construire un nouveau jeu : on pourra fixer dans un premier temps un plateau de jeu avec
des dessins ainsi que les formes des pièces à cacher. Les paramètres sont alors le nombre de
dessins différents ainsi que le nombre d’occurrences de chaque dessin. On devra alors
générer la liste des défis réalisables. Il sera intéressant d’autoriser la modification des formes
des pièces pour voir l’impact sur les défis.
On pourra ensuite explorer une situation inverse : à savoir pour un défi fixé, générer un
plateau et des pièces de telles sorte qu’il n’y ait qu’une seule solution pour ce défi. On peut
ensuite augmenter progressivement le nombre de défis à satisfaire.
## Interface graphique
Réaliser une interface permettant de jouer à ce jeu et d’utiliser les aides à la conception de jeu qui
auront été mises en œuvre. 