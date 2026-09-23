# Plan : Simulateur de déplacement Mars Rover

Spec de référence : intent/mars-rover-simulateur/spec.md (exigences EX-01 à EX-07, réserves R1-R8 toutes tranchées le 23/09/2026, sauf R8 partiellement hors périmètre).

## Statut

Aucune ligne de code, aucun manifest, aucune configuration de test n'existe à ce jour dans le dépôt ni sur aucune branche (vérifié sur `main` et sur toutes les branches locales/distantes). Il n'existe pas encore de skill `build` dans ce dépôt (voir CLAUDE.md). Ce document sert de plan d'implémentation de la phase Build, en l'absence de skill dédié pour l'encadrer.

## Points ouverts (à trancher avant d'écrire du code)

### PO-1 — Choix du stack technique

Ni l'intention, ni la spec, ni le dépôt n'imposent un langage ou un framework de test. Question posée à l'auteur de ce plan le 23/09/2026 ; réponse : à trancher plus tard. Ce point doit être tranché avec le Product Owner avant l'étape 1 de code (voir « Ordre de travail »).

### PO-2 — Caractère de commande invalide

La spec (EX-01, réserve R5 tranchée) définit F, R, L comme les seuls caractères valides, mais ne précise pas le comportement du simulateur si un autre caractère apparaît dans la liste de commandes. Non tranché : à poser au Product Owner avant d'implémenter l'interpréteur de commandes (module 3).

### PO-3 — Mécanisme du message d'erreur de blocage

La réserve R6 (tranchée) fixe le **contenu** du message d'erreur (texte donnant position et orientation au blocage) mais pas le **mécanisme** de restitution (valeur de retour structurée, exception, sortie standard...). Non tranché : à poser au Product Owner avant d'implémenter le module « Erreur de blocage » (module 5), ou à défaut à documenter comme décision technique d'implémentation sans incidence produit.

## Correspondance exigence → module

| Exigence | Comportement attendu | Module(s) concerné(s) |
| --- | --- | --- |
| EX-01 | Réception des entrées (point de départ, orientation, carte, commandes) | Interpréteur de commandes, Moteur d'exécution |
| EX-02 | Rotation 90° droite/gauche sans déplacement | Rover / état |
| EX-03 | Avancée d'une case, carte sans bord (hors grille fournie = libre) | Carte / grille, Moteur d'exécution |
| EX-04 | Blocage sur obstacle, immobilité stricte, message d'erreur | Carte / grille, Moteur d'exécution, Erreur de blocage |
| EX-05 | Interprétation des symboles de la carte | Carte / grille |
| EX-06 | Affichage de la position/orientation finales | Résultat final |
| EX-07 | Comparaison périodique avec le vrai rover, alerte sur écart | Comparateur avec le vrai rover |

## Architecture proposée (modules logiques, indépendants du stack)

1. **Rover / état** — position (x, y) + orientation (N/E/S/W) ; rotation gauche/droite sans changement de position. → EX-02.
2. **Carte / grille** — grille rectangulaire de dimensions fixes ; interprétation des symboles (🌳/🪨 = obstacle, 🟩/🟫 = libre, réserve R2) ; toute case hors de la grille fournie est considérée libre par défaut (réserve R4). → EX-05, R2, R3, R4.
3. **Interpréteur de commandes** — traduit la chaîne de commandes en liste ordonnée d'actions F (avancer), R (droite), L (gauche) (réserve R5). → EX-01, R5.
4. **Moteur d'exécution** — applique les commandes séquentiellement sur l'état du rover ; interroge la carte avant chaque avancée ; ne déplace jamais le rover sur un obstacle (réserve R1) ; arrête l'exécution au premier obstacle rencontré, sans exécuter les commandes restantes (réserve R7). → EX-01, EX-03, EX-04, EX-06, R1, R4, R7.
5. **Erreur de blocage** — construit le message texte donnant la position et l'orientation au moment du blocage (réserve R6). → EX-04, R6.
6. **Résultat final** — position et orientation finales : celles du blocage en cas d'arrêt prématuré (réserve R7), sinon celles obtenues après la dernière commande exécutée. → EX-06, R7.
7. **Comparateur avec le vrai rover** — déclenché après chaque commande exécutée par le simulateur ; reçoit la position du vrai rover via un point d'extension (interface/port) et déclenche une alerte visible pour le développeur en cas d'écart. La source réelle de cette position reste hors périmètre (réserve R8) : seule une implémentation factice (fake) sera fournie pour les tests ; l'intégration réelle sera traitée dans une intention/spec séparée. → EX-07, R8.

## Ordre de travail

Approche TDD, du module le plus isolé au plus intégré. Chaque étape associe code et tests, et fait l'objet d'un commit dédié une fois validée.

1. Squelette du projet (manifest, configuration des tests), une fois PO-1 tranché — commit séparé du code métier.
2. Rover / état + rotation (module 1), avec tests unitaires (EX-02).
3. Carte / grille + interprétation des symboles + règle « hors grille = libre » (module 2), avec tests (EX-05, R2, R3, R4).
4. Interpréteur de commandes (module 3), avec tests (EX-01, R5) ; PO-2 à trancher avant cette étape.
5. Moteur d'exécution : avancée sans obstacle, puis blocage sur obstacle avec arrêt immédiat (modules 4 et 5), avec tests reproduisant EX-03 et EX-04 ; PO-3 à trancher avant l'implémentation du module 5.
6. Résultat final affiché/retourné (module 6), avec test reproduisant EX-06 dans les deux cas (fin normale, arrêt sur obstacle).
7. Tests d'acceptation : un test par scénario déjà rédigé dans spec.md (EX-01 à EX-06), repris tels quels comme cas de test de bout en bout.
8. Comparateur avec le vrai rover (module 7) : interface + fake pour les tests ; alerte déclenchée en cas d'écart ; aucune tentative d'implémenter la vraie source de position (EX-07, R8).
9. Revue finale avec la checklist de la skill `clean-code` (lisibilité locale, noms, fonctions courtes, séparation commande/requête, chemin heureux propre, détails techniques hors du métier, tests exécutés) avant de proposer la Pull Request.

## Tests prévus

- Tests unitaires par module : rotation (module 1), interprétation des symboles et règle hors grille (module 2), parsing des commandes valides et cas PO-2 une fois tranché (module 3), détection d'obstacle et arrêt au premier obstacle (modules 4-5), construction du résultat final dans les deux cas (module 6), déclenchement/non-déclenchement de l'alerte du comparateur avec un fake de position du vrai rover (module 7).
- Tests d'acceptation : un test par scénario EX-01 à EX-06 de spec.md, utilisés comme cas de test de bout en bout du moteur d'exécution.
- Aucun test n'est prévu pour la source réelle de la position du vrai rover : explicitement hors périmètre (R8).

## Fichiers de code

Non encore déterminés : dépendent du stack tranché en PO-1. Ce plan sera complété (ou un plan.md révisé sera proposé) avec l'arborescence de fichiers exacte une fois ce point tranché avec le Product Owner.

## Contexte de génération

### Demande initiale

Demande : « Lis intent.md et spec.md, puis propose un plan de réalisation du simulateur. Précise les fichiers à créer ou modifier, l'ordre du travail et les tests prévus. Prévois comme première étape d'enregistrer le plan dans plan.md à côté de ces deux fichiers et de commiter uniquement ce fichier. »

### Skills consultées

| Chemin | État sur la branche courante (`phase-build`) |
| --- | --- |
| .claude/skills/clean-code/SKILL.md | Présent ; checklist appliquée à l'ordre de travail et à la revue finale. |
| .claude/skills/intent/SKILL.md | Présent ; discipline (jamais inventer, tracer en points ouverts, validation humaine avant écriture) reprise pour ce plan. |

Aucune skill `build` n'existe dans ce dépôt à ce jour (voir CLAUDE.md) ; ce plan n'est donc pas produit par une skill dédiée.

### Révisions

Aucune révision pour l'instant.
