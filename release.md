# Dossier de livraison : Simulateur Mars Rover

## Version candidate

- Version du projet (`pyproject.toml`) : `0.1.0`.
- Commit de merge de la pull request sur `main` : `35e270c` (« Merge pull request #4 from Hymaia22/phase-build »), qui intègre l'implémentation des exigences EX-01 à EX-07 de `intent/mars-rover-simulateur/spec.md`.

## Vérifications disponibles

### `make test`

```
.venv/bin/python -m pytest
============================= test session starts ==============================
platform darwin -- Python 3.12.14, pytest-9.1.1, pluggy-1.6.0
rootdir: /Users/francois/Documents/Documents - MacBook Air de Francois - 1/Hymaia/Fresques/.claude/skills/fresque-cartes-visuelles/scripts/Dojo-thiga
configfile: pyproject.toml
testpaths: tests
collected 22 items

tests/test_acceptance.py ......                                          [ 27%]
tests/test_commands.py ...                                               [ 40%]
tests/test_comparator.py ..                                              [ 50%]
tests/test_engine.py ..                                                  [ 59%]
tests/test_grid.py ...                                                   [ 72%]
tests/test_result.py ..                                                  [ 81%]
tests/test_rover.py ....                                                 [100%]

============================== 22 passed in 0.03s ==============================
```

### `make run`

```
.venv/bin/python -m examples.run_demo
Position finale : (2, 3)
Orientation finale : N
```

## Cible de production

### Ce qui est établi

- Ce projet n'a pas de cible de production réelle : `make deploy` et `make rollback` ne contactent aucune machine, ils enregistrent seulement un identifiant de version dans `.deploy/<ENV>.current` et `.deploy/<ENV>.previous` (état local, non versionné — voir `.gitignore`).
- La gate `.claude/hooks/production_gate.py` bloque toute commande Bash contenant à la fois `deploy` et `production` tant que `release-approval.txt` n'existe pas à la racine ; le message renvoyé demande l'autorisation nommée du Release Manager.
- `release-approval.txt` existe désormais à la racine, commité sur `main` (commit `70b3bb7`) : « Mise en production de la version candidate autorisée par François Laurain, le 2026-09-23. »
- Avec cette autorisation en place, `make deploy ENV=production` a été relancé et est passé : `deploy production: (aucune) -> 70b3bb7`. C'est le seul déploiement simulé effectué sur `production` à ce jour.
- Le rollback (`make rollback ENV=staging`) a été exercé sur l'environnement `staging` : il échoue proprement (message explicite, exit 2) en l'absence de version précédente, et restaure la version précédente quand elle existe.

### Ce qui reste à définir ou à essayer

- Aucune cible de production réelle n'existe ni n'est prévue à ce stade ; ce dossier ne déclare aucune livraison vers un environnement réel.
- `make rollback ENV=production` n'a pas encore été exercé : à ce jour, `production` n'a reçu qu'un seul déploiement simulé, donc aucune version précédente n'existe pour ce rollback (il échouerait avec le message « aucune version précédente »).
- Le processus réel d'obtention et de vérification de l'autorisation du Release Manager (au-delà du dépôt du fichier `release-approval.txt`) reste à définir : qui peut légitimement créer ce fichier, et selon quel processus.
