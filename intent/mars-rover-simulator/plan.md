# Plan de réalisation : Simulateur de rover Mars

Documents de référence : intent/mars-rover-simulator/intent.md,
intent/mars-rover-simulator/spec.md

Stack technique retenue : TypeScript / Node.js (décision Build, hors
périmètre spec — confirmée par le Product Owner le 2026-09-22).

## Prérequis bloquants (rappel depuis spec.md)

Ces points sont marqués bloquants dans spec.md et n'ont pas de décision
humaine à ce jour. Ils ne sont pas tranchés ici ; chaque étape ci-dessous
indique explicitement si elle en dépend.

- RES-01 — convention N/S/E/W ↔ signe/axe de x, y (bloque EX-02 à EX-07)
- Q1 — sémantique et coexistence des jeux de symboles 🟩/🌳 et 🟫/🪨 (bloque EX-08)
- Q2 — format d'entrée de la liste de commandes (bloque EX-06)
- Q3 — format de restitution du résultat (bloque EX-07)
- Q4 — comportement aux limites de la carte (bloque EX-09)
- Q5 — comportement en cas d'entrées invalides (bloque EX-10)

Tant qu'un point n'est pas tranché (via `/spec` ou une mise à jour de
spec.md), l'étape qu'il bloque reste en attente : elle peut être conçue au
niveau de l'interface, mais pas implémentée ni testée de façon vérifiable.

## Architecture proposée

- `src/domain/orientation.ts` — type Orientation (N/E/S/W), `turnRight`,
  `turnLeft` (EX-03, EX-04). Indépendant des points bloquants.
- `src/domain/rover.ts` — état du rover `{ position: {x, y}, orientation }`
  et son initialisation (EX-01). Indépendant des points bloquants.
- `src/domain/movement.ts` — calcul de la case visée par une avancée
  (EX-02, EX-05). **Bloqué par RES-01.**
- `src/domain/map.ts` — lecture de la carte, détermination praticable vs
  obstacle par case (EX-08). **Bloqué par Q1.**
- `src/domain/boundary.ts` — comportement en bordure de carte (EX-09).
  **Bloqué par Q4** (et dépend de `movement.ts`).
- `src/commands/parser.ts` — conversion de l'entrée liste de commandes vers
  une représentation interne (partie entrée d'EX-06). **Bloqué par Q2.**
- `src/simulate.ts` — orchestrateur séquentiel : applique chaque commande
  interne à l'état courant du rover (EX-06), en s'appuyant sur
  `movement.ts`, `map.ts`, `orientation.ts`. Structurable dès que
  `orientation.ts`/`rover.ts` existent ; le branchement complet attend
  `movement.ts`/`map.ts`/`parser.ts`.
- `src/output/formatResult.ts` — restitution de l'état final au système
  appelant (EX-07). **Bloqué par Q3.**
- `src/validation/validateInput.ts` — rejet/signalement des entrées
  invalides (commande, carte, point de départ) (EX-10). **Bloqué par Q5**
  (et par Q2 pour la forme des commandes invalides).
- Scaffolding : `package.json`, `tsconfig.json`, `vitest.config.ts`.

## Ordre de réalisation

1. Committer ce `plan.md` (fait dans cette session, avant tout code).
2. Scaffolding du projet : `package.json`, `tsconfig.json`, config de test
   (vitest). Pas de dépendance aux points bloquants.
3. `orientation.ts` + tests (EX-03, EX-04) — réalisable immédiatement.
4. `rover.ts` (état + initialisation, EX-01) + tests — réalisable
   immédiatement.
5. Obtenir la décision RES-01 (via `/spec`) → `movement.ts` (EX-02) + tests.
6. Obtenir la décision Q1 (via `/spec`) → `map.ts` (EX-08) + tests.
7. `movement.ts` + `map.ts` combinés → avancée bloquée par un obstacle
   (EX-05) + tests. Nécessite RES-01 et Q1.
8. Obtenir la décision Q4 → `boundary.ts` (EX-09) + tests.
9. Obtenir la décision Q2 → `commands/parser.ts` + tests d'entrée (partie
   EX-06).
10. `simulate.ts` : orchestrateur séquentiel (EX-06) + tests bout-en-bout,
    une fois les étapes 5 à 9 disponibles.
11. Obtenir la décision Q3 → `output/formatResult.ts` (EX-07) + tests.
12. Obtenir la décision Q5 → `validateInput.ts` (EX-10) + tests, branché en
    entrée de `simulate.ts`.

## Tests prévus (mêmes scénarios que dans spec.md)

- `tests/orientation.test.ts` — EX-03 (droite N→E), EX-04 (gauche N→W),
  cycle complet dans les deux sens.
- `tests/rover.test.ts` — EX-01 : état initial = (x, y) + orientation
  fournis.
- `tests/movement.test.ts` — EX-02 : avancée sans obstacle déplace le
  rover d'une case dans la direction courante sans changer l'orientation.
  Bloqué tant que RES-01 n'est pas tranché (le sens exact x/y à vérifier
  dépend de la convention retenue).
- `tests/map.test.ts` — EX-08 : lecture praticable/obstacle par case selon
  le jeu de symboles retenu. Bloqué tant que Q1 n'est pas tranché.
- `tests/movement.test.ts` (cas complémentaire) — EX-05 : avancée bloquée
  par un obstacle ne déplace pas le rover. Bloqué tant que RES-01 et Q1 ne
  sont pas tranchés.
- `tests/boundary.test.ts` — EX-09 : comportement en bordure de carte.
  Bloqué tant que Q4 n'est pas tranché.
- `tests/parser.test.ts` — entrée de la liste de commandes dans le format
  retenu. Bloqué tant que Q2 n'est pas tranché.
- `tests/simulate.test.ts` — EX-06 : une séquence de commandes est
  appliquée dans l'ordre à partir de l'état initial ; test bout-en-bout
  combinant toutes les étapes précédentes.
- `tests/formatResult.test.ts` — EX-07 : restitution de l'état final dans
  le format retenu. Bloqué tant que Q3 n'est pas tranché.
- `tests/validateInput.test.ts` — EX-10 : entrée invalide (commande, carte,
  point de départ) traitée selon la décision retenue. Bloqué tant que Q5
  n'est pas tranché.

## Notes

Ce plan ne tranche aucune décision produit : les points RES-01/Q1–Q5
restent à valider par le Product Owner, idéalement via `/spec` pour que
`spec.md` reste la source de vérité et que ce plan reste synchronisé avec
elle.
