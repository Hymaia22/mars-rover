# Spec : Simulateur de déplacement Mars Rover

Intention de référence : intent/mars-rover-simulateur/intent.md

## Périmètre

Besoin couvert : un simulateur qui se comporte comme un clone du vrai rover. Il reçoit un point de départ, une orientation, une carte et une liste de commandes. Il exécute les commandes et affiche la position et la direction finales du rover. Sa position est comparée régulièrement à celle du vrai rover pour garder le clone aligné.

Utilisateurs : les développeurs de l'équipe Mars Rover.

Exclusions : aucun système connecté pour l'instant. La source de la position du vrai rover et le mécanisme d'accès à cette position sont hors périmètre de cette spec (voir réserve R8) ; ils seront traités dans une intention/spec séparée.

## Exigences

### EX-01 — Réception des entrées du simulateur

Origine dans l'intention : « Entrées : un point (x, y), une orientation parmi N, S, E ou W, une carte qui place les obstacles et une liste de commandes. »
Comportement attendu : Le simulateur reçoit en entrée un point de départ (x, y), une orientation initiale parmi N, S, E, W, une carte plaçant les obstacles et une liste de commandes à exécuter.

Scénario
- Situation de départ : Un point de départ, une orientation, une carte et une liste de commandes sont fournis.
- Action : Le simulateur est lancé avec ces entrées.
- Résultat attendu : Le simulateur accepte les entrées et démarre l'exécution des commandes. La carte est une grille rectangulaire de dimensions fixes, chaque case portant l'un des quatre symboles (décision du 23/09/2026, voir réserve R3 tranchée). Les commandes sont F (avancer), R (tourner à droite), L (tourner à gauche) (décision du 23/09/2026, voir réserve R5 tranchée).

### EX-02 — Rotation du rover

Origine dans l'intention : « Le rover peut avancer, ou tourner de 90 degrés à droite ou à gauche. »
Comportement attendu : Une commande de rotation fait tourner le rover de 90 degrés à droite ou à gauche, sans changer sa position.

Scénario
- Situation de départ : Le rover est à une position donnée, orienté N.
- Action : Le simulateur exécute la commande R (tourner à droite).
- Résultat attendu : Le rover est orienté E ; sa position (x, y) est inchangée.

### EX-03 — Avancée du rover

Origine dans l'intention : « Le rover peut avancer... La carte n'a pas de bord. »
Comportement attendu : Une commande d'avancée déplace le rover d'une case dans la direction de son orientation courante, sur une carte sans bord déclaré.

Scénario
- Situation de départ : Le rover est à une position donnée, orienté N, avec une case libre devant lui.
- Action : Le simulateur exécute la commande F (avancer).
- Résultat attendu : Le rover avance d'une case dans la direction N. Au-delà des limites de la grille fournie, le terrain est considéré comme libre par défaut et le rover continue d'avancer normalement (décision du 23/09/2026, voir réserve R4 tranchée).

### EX-04 — Blocage sur obstacle

Origine dans l'intention : « Le rover reste immobile quand un obstacle bloque son avancée, et il renvoie un message d'erreur. »
Comportement attendu : Quand une commande d'avancée rencontre un obstacle, le rover reste immobile et un message d'erreur est renvoyé.

Scénario
- Situation de départ : Le rover est orienté vers une case marquée comme obstacle.
- Action : Le simulateur exécute une commande d'avancer.
- Résultat attendu : Le rover reste à sa position et son orientation d'origine ; un message d'erreur est renvoyé. Le rover ne change jamais de position face à un obstacle (décision du 23/09/2026, voir réserve R1 tranchée). Le message d'erreur est un texte donnant la position et l'orientation du rover au moment du blocage (décision du 23/09/2026, voir réserve R6 tranchée). L'exécution s'arrête au premier obstacle rencontré ; les commandes restantes ne sont pas exécutées (décision du 23/09/2026, voir réserve R7 tranchée).

### EX-05 — Interprétation de la carte

Origine dans l'intention : « La carte utilise soit les symboles 🟩 et 🌳, soit les symboles 🟫 et 🪨. »
Comportement attendu : Le simulateur interprète chaque case de la carte fournie, selon l'une des deux paires de symboles, pour déterminer si elle est libre ou occupée par un obstacle.

Scénario
- Situation de départ : Une carte utilisant l'une des deux paires de symboles est fournie.
- Action : Le simulateur charge la carte.
- Résultat attendu : Chaque case est reconnue comme libre ou comme obstacle. 🌳 et 🪨 sont des obstacles ; 🟩 et 🟫 sont des terrains libres (décision du 23/09/2026, voir réserve R2 tranchée). La carte est une grille rectangulaire de dimensions fixes (décision du 23/09/2026, voir réserve R3 tranchée).

### EX-06 — Affichage du résultat final

Origine dans l'intention : « Il exécute les commandes et affiche la position et la direction finales du rover. »
Comportement attendu : Après exécution de la liste de commandes, le simulateur affiche la position (x, y) et l'orientation finales du rover.

Scénario
- Situation de départ : Une liste de commandes a été exécutée.
- Action : Le simulateur termine l'exécution.
- Résultat attendu : La position (x, y) et l'orientation finales du rover sont affichées. Si un obstacle a bloqué le rover, l'exécution s'est arrêtée à cet obstacle et la position/orientation affichées sont celles du blocage (décision du 23/09/2026, voir réserve R7 tranchée).

### EX-07 — Comparaison avec le vrai rover

Origine dans l'intention : « Sa position est comparée régulièrement à celle du vrai rover pour garder le clone aligné. »
Comportement attendu : La position du simulateur est comparée régulièrement à celle du vrai rover afin de détecter un désalignement.

Scénario
- Situation de départ : Le simulateur vient d'exécuter une commande.
- Action : Le simulateur compare sa position à celle du vrai rover.
- Résultat attendu : En cas d'écart, une alerte visible pour le développeur est déclenchée (décision du 23/09/2026, voir réserve R8). La source de la position du vrai rover n'est pas définie dans cette spec (voir réserve R8, hors périmètre) : cette exigence couvre le déclenchement de la comparaison et la réaction du simulateur, pas l'obtention de la position du vrai rover.

## Conception proposée

Statut : proposition à valider dans son ensemble ; l'intention ne fixe aucun choix technique, seulement le comportement attendu.

- Un modèle de position et d'orientation (x, y, direction parmi N, S, E, W), porté par l'état du rover. Justification : reprend directement les entrées et sorties décrites dans l'intention (EX-01, EX-06).
- Un modèle de carte : une grille rectangulaire de dimensions fixes, indexée par coordonnées (x, y), chaque case portant un état libre ou obstacle déduit du symbole qu'elle contient (🌳/🪨 = obstacle, 🟩/🟫 = libre). Justification : découle de EX-05 et des réserves R2 et R3, désormais tranchées.
- Un interpréteur de commandes qui traduit chaque caractère de la liste de commandes (F, R, L) en une action parmi avancer, tourner à droite, tourner à gauche. Justification : découle de EX-01, EX-02, EX-03 et de la réserve R5, désormais tranchée.
- Un moteur d'exécution séquentiel qui applique les commandes une à une sur l'état du rover, gère le blocage sur obstacle sans jamais déplacer le rover (R1 tranchée) et arrête l'exécution au premier obstacle rencontré (R7 tranchée). Justification : découle de EX-04 et EX-06.
- Un point de comparaison, déclenché après chaque commande exécutée, qui reçoit la position du vrai rover et alerte le développeur en cas d'écart. Justification : découle de EX-07 et de la réserve R8 ; l'obtention de la position du vrai rover reste hors périmètre (source à définir dans une intention/spec séparée).

Aucun de ces éléments n'est encore accepté par le Product Owner ; ils sont proposés comme découpage cohérent avec les exigences ci-dessus.

## Réserves

### R1 — Comportement du rover face à un obstacle (immobilité stricte ou déplacement par chute)

Origine : Intention, questions ouvertes (« Face à un obstacle, le rover peut-il changer de position à cause d'une chute, ou reste-t-il toujours immobile ? »), qui interroge la contrainte « Le rover reste immobile quand un obstacle bloque son avancée ».
Exigences concernées : EX-04.
Conséquences : Si une chute est possible, le résultat d'une commande bloquée n'est plus un simple statu quo ; le scénario et le message d'erreur de EX-04 doivent en tenir compte.
Décision attendue : Confirmer si le rover reste toujours immobile face à un obstacle, ou s'il peut chuter et changer de position.
Décision : Le rover reste toujours immobile face à un obstacle ; aucune chute n'est possible.
Auteur : François Laurain (Product Owner).
Date : 2026-09-23.
Justification : Confirme la contrainte déjà énoncée dans l'intention.
Statut : tranchée.

### R2 — Rôle de chaque symbole dans les paires de la carte

Origine : Intention, questions ouvertes (« Dans chaque paire de symboles, lequel représente un obstacle et lequel un terrain libre ? »).
Exigences concernées : EX-05, et par dépendance EX-03 et EX-04 (détection d'obstacle).
Conséquences : Sans cette correspondance, le simulateur ne peut pas distinguer une case libre d'un obstacle.
Décision attendue : Indiquer, pour chaque paire (🟩/🌳 et 🟫/🪨), quel symbole désigne l'obstacle et quel symbole désigne le terrain libre.
Décision : 🌳 et 🪨 sont des obstacles ; 🟩 et 🟫 sont des terrains libres.
Auteur : François Laurain (Product Owner).
Date : 2026-09-23.
Justification : Choix retenu pour lever l'ambiguïté sur l'interprétation de la carte.
Statut : tranchée.

### R3 — Format de la grille

Origine : Intention, questions ouvertes (« Quel est le format de la grille ? »).
Exigences concernées : EX-01, EX-05.
Conséquences : La structure d'entrée de la carte (dimensions, représentation, orientation des axes) n'est pas connue.
Décision attendue : Préciser le format attendu de la carte.
Décision : La carte est une grille rectangulaire de dimensions fixes (largeur × hauteur), chaque case portant l'un des quatre symboles ; les coordonnées (x, y) correspondent à la position dans la grille.
Auteur : François Laurain (Product Owner).
Date : 2026-09-23.
Justification : Format simple, cohérent avec des entrées (x, y) et avec l'usage de symboles par case déjà décrit dans l'intention.
Statut : tranchée.

### R4 — Comportement du rover au-delà des limites de la carte fournie

Origine : Intention, contrainte « La carte n'a pas de bord » et question ouverte associée.
Exigences concernées : EX-03.
Conséquences : Sans règle, l'avancée du rover hors de la carte fournie ne peut pas être simulée de façon prévisible (retour au bord opposé, extension implicite, autre règle).
Décision attendue : Définir le comportement du rover quand il dépasse les limites de la carte fournie.
Décision : Au-delà des limites de la grille fournie, le terrain est considéré comme libre par défaut (aucun obstacle connu) ; le rover continue d'avancer normalement.
Auteur : François Laurain (Product Owner).
Date : 2026-09-23.
Justification : Cohérent avec « La carte n'a pas de bord » : la grille fournie décrit les obstacles connus, pas les limites du terrain.
Statut : tranchée.

### R5 — Caractères représentant les commandes

Origine : Intention, questions ouvertes (« Quels caractères représentent les commandes (avancer, tourner à droite, tourner à gauche) ? »).
Exigences concernées : EX-01, EX-02, EX-03.
Conséquences : Le format exact de la liste de commandes en entrée ne peut pas être précisé.
Décision attendue : Indiquer les caractères représentant chacune des trois commandes.
Décision : F = avancer, R = tourner à droite, L = tourner à gauche.
Auteur : François Laurain (Product Owner).
Date : 2026-09-23.
Justification : Convention anglaise usuelle du kata Mars Rover (forward, right, left).
Statut : tranchée.

### R6 — Format et contenu du message d'erreur

Origine : Intention, questions ouvertes (« Quels sont le format et le contenu du message d'erreur ? »).
Exigences concernées : EX-04.
Conséquences : Le résultat attendu du scénario EX-04 ne peut pas être vérifié précisément.
Décision attendue : Préciser le format et le contenu du message d'erreur renvoyé après un blocage.
Décision : Un message textuel donnant la position (x, y) où le rover est bloqué et son orientation à ce moment (par exemple « Obstacle détecté en (x, y), orientation N »).
Auteur : François Laurain (Product Owner).
Date : 2026-09-23.
Justification : Donne au développeur l'information nécessaire pour localiser le blocage sans avoir à la déduire d'ailleurs.
Statut : tranchée.

### R7 — Poursuite ou arrêt de la liste de commandes après un obstacle

Origine : Intention, questions ouvertes (« Le simulateur continue-t-il les commandes suivantes après un obstacle, ou s'arrête-t-il ? »).
Exigences concernées : EX-04, EX-06.
Conséquences : Le résultat final affiché (EX-06) dépend de savoir si toutes les commandes ont été tentées ou si l'exécution s'est arrêtée au premier obstacle.
Décision attendue : Indiquer si l'exécution s'arrête au premier obstacle rencontré ou si elle continue avec les commandes suivantes.
Décision : L'exécution s'arrête au premier obstacle rencontré ; les commandes restantes de la liste ne sont pas exécutées.
Auteur : François Laurain (Product Owner).
Date : 2026-09-23.
Justification : Cohérent avec le clonage du vrai rover, qui ne peut pas non plus exécuter les commandes suivantes une fois bloqué.
Statut : tranchée.

### R8 — Fréquence et méthode de comparaison avec le vrai rover

Origine : Intention, questions ouvertes (« À quelle fréquence et comment compare-t-on la position du simulateur à celle du vrai rover ? »).
Exigences concernées : EX-07.
Conséquences : Le mécanisme de comparaison ne peut pas être précisé (déclenchement périodique, sur demande, à chaque commande, etc.), ni le comportement attendu en cas d'écart détecté.
Décision attendue : Préciser la fréquence de comparaison, la méthode utilisée, et le comportement attendu en cas d'écart.
Décision : La comparaison a lieu après chaque commande exécutée par le simulateur ; un écart avec la position du vrai rover déclenche une alerte visible pour le développeur. La source de la position du vrai rover (API, fichier, autre système) et le mécanisme de rapprochement restent hors du périmètre de cette spec : l'intention précise qu'aucun système n'est connecté pour l'instant, ce point sera traité dans une intention/spec séparée.
Auteur : François Laurain (Product Owner).
Date : 2026-09-23.
Justification : Fixe la fréquence et la réaction du simulateur sans anticiper sur l'intégration avec le vrai rover, non encore définie.
Statut : tranchée pour le simulateur ; source de la position du vrai rover hors périmètre (nouvelle intention à ouvrir).

## Questions ouvertes

| # | Question (intention) | Réponse humaine | Effet sur le passage à la phase Build |
| --- | --- | --- | --- |
| 1 | Qui est l'auteur de cette intention, et quel est son rôle ? | Laissée ouverte (François Laurain, 23/09/2026). | Sans effet direct sur les exigences ou la conception ; n'empêche pas le passage à la phase Build. |
| 2 | Face à un obstacle, le rover peut-il changer de position à cause d'une chute, ou reste-t-il toujours immobile ? | Le rover reste toujours immobile ; aucune chute possible (François Laurain, 23/09/2026). | Tranchée. EX-04 précisée en conséquence. |
| 3 | Le rover évolue-t-il sur Mars ou sur la Lune ? | Mars (François Laurain, 23/09/2026 — correction après une première réponse « Lune »). | Tranchée, cohérente avec le titre de l'intention et le nom du dossier `intent/mars-rover-simulateur/`. Sans effet identifié sur les exigences actuelles. |
| 4 | Quel est le format de la grille ? | Grille rectangulaire de dimensions fixes, une case par symbole (François Laurain, 23/09/2026). | Tranchée. EX-01 et EX-05 précisées en conséquence. |
| 5 | Dans chaque paire de symboles, lequel représente un obstacle et lequel un terrain libre ? | 🌳 et 🪨 sont des obstacles ; 🟩 et 🟫 sont des terrains libres (François Laurain, 23/09/2026). | Tranchée. EX-05 précisée en conséquence. |
| 6 | La carte n'a pas de bord : que se passe-t-il quand le rover dépasse les limites de la carte fournie ? | Au-delà des limites fournies, le terrain est libre par défaut (François Laurain, 23/09/2026). | Tranchée. EX-03 précisée en conséquence. |
| 7 | Quels caractères représentent les commandes (avancer, tourner à droite, tourner à gauche) ? | F = avancer, R = droite, L = gauche (François Laurain, 23/09/2026). | Tranchée. EX-01, EX-02, EX-03 précisées en conséquence. |
| 8 | Quels sont le format et le contenu du message d'erreur ? | Texte donnant la position et l'orientation au blocage (François Laurain, 23/09/2026). | Tranchée. EX-04 précisée en conséquence. |
| 9 | Le simulateur continue-t-il les commandes suivantes après un obstacle, ou s'arrête-t-il ? | S'arrête au premier obstacle (François Laurain, 23/09/2026). | Tranchée. EX-04 et EX-06 précisées en conséquence. |
| 10 | À quelle fréquence et comment compare-t-on la position du simulateur à celle du vrai rover ? | Comparaison après chaque commande, alerte en cas d'écart ; source de la position du vrai rover hors périmètre (François Laurain, 23/09/2026). | Fréquence et réaction tranchées. La source de la position du vrai rover reste ouverte, hors périmètre de cette spec — à traiter dans une intention/spec séparée avant que cette partie du Build ne démarre. |

## Contexte de génération

### Demande initiale

Commande : `/spec intent/mars-rover/intent.md`

Note : le dépôt ne contient qu'une seule intention, à `intent/mars-rover-simulateur/intent.md`. L'argument fourni a été résolu vers ce fichier.

### Skills utilisées

| Chemin | Commit Git de la version utilisée |
| --- | --- |
| .claude/skills/spec/SKILL.md | 74721ac (branche `claude/skill-spec`, non fusionnée dans `main` au moment de la rédaction — pull request #2 ouverte) |

### Révisions

Aucune révision pour l'instant.
