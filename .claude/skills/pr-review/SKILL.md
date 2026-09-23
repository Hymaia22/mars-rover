---
name: pr-review
description: >-
  Relit une pull request en appliquant les critères de REVIEW.md. À utiliser
  quand une pull request ouverte doit être relue avant la décision de merge.
disallowed-tools: Edit Write
---

# Relire une pull request

## Quand utiliser cette skill

Utilise cette skill quand une pull request ouverte doit être relue avant la décision de merge.

## Ce qu'il faut lire

1. REVIEW.md à la racine du repository, qui porte les critères de la review.
2. Les documents que REVIEW.md désigne.
3. Le diff entre main et la branche de la pull request.

## Comment rendre les constats

- Groupe les constats par passe, dans l'ordre que REVIEW.md fixe, et place les Important d'abord.
- Pour chaque constat, donne le fichier et la ligne, ce qui ne va pas, et ce qui se passerait sans correction.
- Termine par le nombre d'Important et le nombre de remarques mineures.

## Ce que tu ne fais pas

- N'applique aucun critère absent de REVIEW.md. Les critères lui appartiennent.
- Ne modifie aucun fichier.
- Ne dis pas si la pull request est prête. La décision appartient au Code Owner.
