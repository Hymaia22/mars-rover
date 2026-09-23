# Intent : Simulateur de déplacement Mars Rover
Auteur : non renseigné.

## Problème
Il faut du temps pour qu'une commande atteigne le vrai rover et pour recevoir sa réponse. L'équipe ne peut donc pas connaître rapidement le résultat d'une série de commandes.

## Résultat proposé
Un simulateur qui se comporte comme un clone du vrai rover. Il reçoit un point de départ, une orientation, une carte et une liste de commandes. Il exécute les commandes et affiche la position et la direction finales du rover. Sa position est comparée régulièrement à celle du vrai rover pour garder le clone aligné.

## Utilisateurs et systèmes concernés
- Utilisateurs : les développeurs de l'équipe Mars Rover.
- Systèmes : aucun système connecté pour l'instant.

## Contraintes
- Entrées : un point (x, y), une orientation parmi N, S, E ou W, une carte qui place les obstacles et une liste de commandes.
- Le rover peut avancer, ou tourner de 90 degrés à droite ou à gauche.
- Le rover reste immobile quand un obstacle bloque son avancée, et il renvoie un message d'erreur.
- La carte n'a pas de bord.
- La carte utilise soit les symboles 🟩 et 🌳, soit les symboles 🟫 et 🪨.

## Questions ouvertes
- Qui est l'auteur de cette intention, et quel est son rôle ?
- Face à un obstacle, le rover peut-il changer de position à cause d'une chute, ou reste-t-il toujours immobile ?
- Le rover évolue-t-il sur Mars ou sur la Lune ?
- Quel est le format de la grille ?
- Dans chaque paire de symboles, lequel représente un obstacle et lequel un terrain libre ?
- La carte n'a pas de bord : que se passe-t-il quand le rover dépasse les limites de la carte fournie ?
- Quels caractères représentent les commandes (avancer, tourner à droite, tourner à gauche) ?
- Quels sont le format et le contenu du message d'erreur ?
- Le simulateur continue-t-il les commandes suivantes après un obstacle, ou s'arrête-t-il ?
- À quelle fréquence et comment compare-t-on la position du simulateur à celle du vrai rover ?
