# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

This is not a software project with a build/test toolchain. It is a **process dojo**: a repo used to practice and codify a staged, human-gated product workflow (Intent → Spec → Build) through custom Claude Code skills, applied to a running example (the "Mars Rover simulator" kata). There is no application code, no package manifest, and no test suite here — the deliverables are structured Markdown documents produced under skill discipline, and the skills themselves.

Repo (GitHub): `Hymaia22/mars-rover`.

## Structure

- `.claude/skills/<name>/SKILL.md` — the custom skills that drive this workflow. Currently on `main`: `intent`. A `spec` skill exists only on the unmerged branch `claude/skill-spec` (see below) — read it there if asked to work on the Spec phase.
- `intent/<slug>/intent.md` — the accepted (or in-progress) intent document for a given need, one folder per slug.
- `intent/<slug>/spec.md` — the corresponding specification, once the Design phase has run.

## The workflow these skills encode

Each need moves through phases, each with its own skill and its own document, and each requiring an explicit human (Product Owner) decision before advancing:

1. **Intent** (`intent` skill) — turns a raw idea into a structured `intent.md`: Problème / Résultat proposé / Utilisateurs et systèmes concernés / Contraintes / Questions ouvertes. The skill asks one clarifying question at a time, never decides on the author's behalf, and only writes the file after the author explicitly validates a drafted version.
2. **Spec** (`spec` skill, branch `claude/skill-spec`) — turns an *accepted* intent into `spec.md`: numbered requirements (`EX-01`, ...) each traced back to the intent, a proposed design, and explicitly tracked "réserves" (open technical/product ambiguities) that get resolved one at a time with the Product Owner, never invented.
3. **Build** — not yet represented by a skill in this repo as of this writing.

Common rules across these skills, worth preserving if you write or edit one:
- Never invent decisions, constraints, authors, or approvals on the human's behalf — track them as open questions/réserves instead.
- Writing to `intent/` or `spec.md` requires prior explicit human validation of a presented draft.
- File writes happen on a dedicated branch (`claude/intent-<slug>`, `claude/spec-<slug>`, ...) created from the latest `main`, never directly on `main`.
- Nothing is committed, pushed, or opened as a PR without explicit confirmation, and the skill never merges its own PR — the Product Owner does that after review.
- `spec.md` must record its own generation context: the exact prompt/command used, and the Git commit of each skill version applied — so the document is reproducible/auditable.

## Working in this repo

- If asked to advance the Mars Rover example past the current spec (`intent/mars-rover-simulateur/`), use the relevant skill (`intent` or `spec`) rather than editing the Markdown by hand — the skills' human-in-the-loop steps (drafts, one-question-at-a-time, validation gates) are the point.
- If asked to work on the `spec` skill itself, note it currently lives only on `origin/claude/skill-spec`, not on `main`.
- There is nothing to build, lint, or test — verification here means checking that a skill's own rules (drafting, validation gates, branch/PR discipline) were followed, and that produced documents (`intent.md`, `spec.md`) match the format each skill defines.

## Erreurs récurrentes

Lorsqu’une même erreur se répète deux fois, propose une instruction courte et précise pour l’éviter. Appuie-toi sur les erreurs observées et fais valider cette instruction avant de l’ajouter à CLAUDE.md.

Si une instruction devient obsolète, propose sa correction ou son retrait et attends la validation avant de modifier le fichier.
