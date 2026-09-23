---
name: diag
description: >-
  Établit le diagnostic d'un écart signalé par une détection, en séparant les
  faits des hypothèses, puis le fait enregistrer comme intention une fois
  accepté. À utiliser quand une mesure suivie sort de ses limites.
disable-model-invocation: true
---

# Diagnostiquer un écart signalé

## Quand utiliser cette skill

Utilise cette skill quand une détection a signalé un écart et que son diagnostic est demandé, avant toute correction.

## Sur quoi t'appuyer

1. La sortie de la détection, qui dit le palier atteint.
2. Les données que la détection a lues.
3. Le code concerné par l'écart.

## Comment rendre le diagnostic

- Rends trois ensembles distincts, les faits, les hypothèses, puis les questions ouvertes. Termine par le résultat que tu proposes de rechercher.
- Pour chaque fait, donne la ligne de données ou le fichier qui l'établit.
- Pour chaque hypothèse, dis ce qui la confirmerait ou l'écarterait.

## Une fois le diagnostic rendu

Arrête-toi et demande s'il est accepté. Ne poursuis pas sans cette acceptation.

Poursuis ensuite selon l'action que le palier déclare et que l'on t'a donnée.

- `propose` : enregistre le diagnostic accepté comme une nouvelle intention, avec la skill `intent`. Transmets-lui le diagnostic accepté, le slug et l'auteur que l'on t'a donnés.
- `diagnose` : arrête-toi sur le diagnostic accepté. Tu n'écris rien.

## Ce que tu ne fais pas

- Ne modifie aucun fichier tant que le diagnostic n'est pas accepté.
- Ne propose aucun correctif. Le diagnostic précède la décision.
- Ne comble pas une donnée manquante par une supposition présentée comme un fait. Dis ce qui manque.
- N'écris pas l'intention toi-même. La skill `intent` porte son format, son emplacement et son circuit de branche.
