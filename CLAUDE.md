# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project state

This repository has no application code yet. It currently holds only the
process artifacts (`intent/`) and the custom skills (`.claude/skills/`) that
produce them. There is no build, lint, or test tooling to run — do not
assume a language/framework or invent one; confirm with the Product Owner
before scaffolding the actual Mars rover simulator implementation.

## Workflow: Intent → Spec → Build

This repo follows a staged, document-driven process before any code is
written, implemented as two custom skills invoked via slash commands. Both
skills are written in French and drive their documents in French — follow
that convention when working within this workflow.

1. **Intent** (`/intent`, skill at `.claude/skills/intent/SKILL.md`)
   Turns a raw idea into a structured `intent/<slug>/intent.md`. The skill
   must not make product decisions or invent constraints on the author's
   behalf; anything undecided goes into that document's "Questions
   ouvertes" section. It asks one clarifying question at a time, presents
   drafts for validation, and only writes to disk / creates a branch /
   opens a PR after explicit human confirmation at each step.

2. **Spec** (`/spec <path/to/intent.md>`, skill at `.claude/skills/spec/SKILL.md`,
   `disable-model-invocation: true` — must be invoked explicitly)
   Reads an *accepted* intent (accepted = merged to `main` via PR, verified
   via the PR decision, not just presence on main) and writes
   `spec.md` alongside it with numbered requirements (`EX-01`, `EX-02`, …),
   each with an origin quote from the intent, expected behavior, and a
   scenario (starting situation / action / expected result). It also
   tracks:
   - **Réserves** (reservations): things needed to make a requirement
     verifiable but not supplied by the intent — e.g. `RES-01` here (the
     coordinate/orientation convention).
   - **Questions ouvertes**: carried over from the intent, each marked open
     or resolved with the human decision, author, date, and justification.
   - **Contexte de génération**: the exact prompt/command used, which
     skill files (with git commit hash) were used to generate it, and a
     revision log.
   This skill never writes code or a build plan — that belongs to a later
   Build phase — and never decides open questions itself; it walks the
   Product Owner through open reservations/questions one at a time and
   waits for an answer before moving to the next.

Both skills: create a dedicated working branch before writing (naming
pattern `claude/intent-<slug>` for the intent phase), never commit/push/open
a PR without explicit confirmation, and never merge the PR themselves — the
Product Owner merges after review.

## Current domain content

`intent/mars-rover-simulator/` describes a Mars rover simulator: given a
starting `(x, y)` position, an initial orientation (N/S/E/W), an obstacle
map, and a list of movement commands, it must compute the rover's final
position/orientation. The rover moves forward, turns 90° left/right, and
stays put if a forward move would hit an obstacle. `spec.md` is in progress
under a draft PR and currently has multiple **blocking** open items before
Build can start — check `spec.md`'s "Réserves" and "Questions ouvertes"
sections for current status before assuming any of these are settled:

- `RES-01`: no agreed convention linking N/S/E/W to the sign/axis of x/y
  changes (open as of 2026-09-22 — PO could not yet answer).
- `Q1`: meaning/coexistence of the two obstacle-map symbol sets (🟩/🌳 vs
  🟫/🪨) is undefined.
- `Q2`/`Q3`: exact input format for commands and output format for the
  final state are undefined.
- `Q4`/`Q5`: behavior at map boundaries and on invalid input are undefined.

When resuming work on this spec, treat these as still open unless `spec.md`
has been updated to record a human decision.
