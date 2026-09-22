# Spec : Simulateur de rover Mars

Intention de référence : intent/mars-rover-simulator/intent.md

## Périmètre

Besoin couvert : fournir un simulateur qui, à partir d'un point de départ (x, y), d'une orientation initiale (N, S, E ou W), d'une carte indiquant les obstacles et d'une liste de commandes, interprète ces commandes et détermine la position et l'orientation finales du rover, afin qu'un système plus large (type mission control / API) puisse piloter le rover et connaître son état.

Exclusions présentes dans l'intention : aucun utilisateur final direct n'est identifié à ce stade — le simulateur est destiné à être appelé par un système plus large, pas par une interface utilisateur humaine directe.

## Exigences

### EX-01 — État initial du rover

Origine dans l'intention : « à partir d'un point de départ (x, y), d'une orientation initiale (N, S, E ou W) [...] »
Comportement attendu : le simulateur initialise l'état du rover à partir du point de départ (x, y) et de l'orientation fournis, avant tout traitement de commande.

Scénario
- Situation de départ : un point de départ (x, y) et une orientation initiale parmi N, S, E, W sont fournis.
- Action : initialisation du simulateur avec ces valeurs.
- Résultat attendu : le rover est positionné en (x, y) avec l'orientation fournie, prêt à recevoir les commandes.

### EX-02 — Avancer sans obstacle

Origine dans l'intention : « Le rover avance ou tourne de 90 degrés à droite ou à gauche. »
Comportement attendu : lorsqu'une commande d'avancée est traitée et que la case dans la direction courante n'est pas un obstacle, le rover se déplace d'une case dans cette direction ; son orientation ne change pas.

Scénario
- Situation de départ : le rover est en (x, y), orienté dans une direction donnée ; la case immédiatement devant lui n'est pas un obstacle.
- Action : traitement d'une commande d'avancée.
- Résultat attendu : le rover occupe la case adjacente dans la direction où il était orienté, avec la même orientation. La correspondance exacte entre une orientation (N/S/E/W) et le sens de variation des coordonnées (x, y) n'est pas précisée dans l'intention — voir Réserves.

### EX-03 — Tourner à droite

Origine dans l'intention : « Le rover avance ou tourne de 90 degrés à droite ou à gauche. »
Comportement attendu : lorsqu'une commande de rotation à droite est traitée, l'orientation du rover pivote de 90° dans le sens horaire (N→E→S→W→N) ; sa position ne change pas.

Scénario
- Situation de départ : le rover est en (x, y), orienté N.
- Action : traitement d'une commande de rotation à droite.
- Résultat attendu : le rover reste en (x, y), désormais orienté E.

### EX-04 — Tourner à gauche

Origine dans l'intention : « Le rover avance ou tourne de 90 degrés à droite ou à gauche. »
Comportement attendu : lorsqu'une commande de rotation à gauche est traitée, l'orientation du rover pivote de 90° dans le sens antihoraire (N→W→S→E→N) ; sa position ne change pas.

Scénario
- Situation de départ : le rover est en (x, y), orienté N.
- Action : traitement d'une commande de rotation à gauche.
- Résultat attendu : le rover reste en (x, y), désormais orienté W.

### EX-05 — Avancée bloquée par un obstacle

Origine dans l'intention : « il reste immobile lorsqu'un obstacle bloque son avancée » ; « Le rover reste immobile si une commande d'avancée le mènerait sur un obstacle. »
Comportement attendu : lorsqu'une commande d'avancée est traitée et que la case dans la direction courante est un obstacle, le rover ne se déplace pas ; son orientation ne change pas.

Scénario
- Situation de départ : le rover est en (x, y), orienté dans une direction donnée ; la case immédiatement devant lui est un obstacle.
- Action : traitement d'une commande d'avancée.
- Résultat attendu : le rover reste en (x, y) avec la même orientation. L'intention ne précise pas si le fait d'avoir été bloqué doit être signalé au système appelant en plus de la position et de l'orientation finales — voir Réserves.

### EX-06 — Traitement séquentiel de la liste de commandes

Origine dans l'intention : « une liste de commandes [...] interprète ces commandes et affiche la position et la direction finales du rover »
Comportement attendu : le simulateur applique les commandes de la liste dans leur ordre d'arrivée, chacune transformant l'état courant du rover (position, orientation) selon EX-02 à EX-05, jusqu'à la dernière commande.

Scénario
- Situation de départ : un état initial de rover (EX-01) et une liste ordonnée de commandes d'avancée et de rotation.
- Action : traitement de la liste de commandes du début à la fin.
- Résultat attendu : l'état du rover après la dernière commande correspond à l'application successive de chaque commande à partir de l'état initial. Le format précis dans lequel les commandes sont fournies en entrée (ex. chaîne de caractères, liste d'objets) n'est pas précisé dans l'intention — voir Questions ouvertes.

### EX-07 — Restitution de l'état final au système appelant

Origine dans l'intention : « affiche la position et la direction finales du rover » ; « qui envoie les commandes et récupère l'état final du rover »
Comportement attendu : une fois la liste de commandes traitée, le simulateur restitue la position (x, y) et l'orientation finales du rover au système appelant.

Scénario
- Situation de départ : le traitement de la liste de commandes (EX-06) est terminé.
- Action : restitution du résultat par le simulateur.
- Résultat attendu : le système appelant reçoit la position et l'orientation finales du rover. Le format précis de cette restitution (texte, JSON, autre) et son mode de consommation par le système appelant ne sont pas précisés dans l'intention — voir Questions ouvertes.

### EX-08 — Lecture de la carte selon les jeux de symboles

Origine dans l'intention : « La carte peut employer deux jeux de symboles : 🟩 et 🌳, ou 🟫 et 🪨. »
Comportement attendu : le simulateur détermine, pour chaque case de la carte, si elle est praticable ou constitue un obstacle, à partir du symbole qui la représente.

Scénario
- Situation de départ : une carte utilisant l'un des jeux de symboles mentionnés dans l'intention.
- Action : lecture de la carte par le simulateur pour déterminer les cases praticables et les obstacles.
- Résultat attendu : manque une décision — l'intention ne précise pas laquelle des deux valeurs de chaque paire désigne le terrain praticable et laquelle désigne l'obstacle, ni si les deux jeux de symboles doivent être supportés simultanément ou correspondent à des contextes distincts — voir Questions ouvertes.

### EX-09 — Comportement aux limites de la carte

Origine dans l'intention : question ouverte « Quel comportement attendu si le rover atteint les limites de la carte ? »
Comportement attendu : manque une décision.

Scénario
- Situation de départ : le rover est sur une case en bordure de la carte, orienté vers l'extérieur de celle-ci.
- Action : traitement d'une commande d'avancée.
- Résultat attendu : manque une décision — l'intention ne précise pas si cette situation doit être traitée comme un blocage (au même titre qu'un obstacle, EX-05), comme une erreur, ou autrement — voir Questions ouvertes.

### EX-10 — Comportement en cas d'entrées invalides

Origine dans l'intention : question ouverte « Quel comportement attendu en cas de commande, carte ou point de départ invalides ? »
Comportement attendu : manque une décision.

Scénario
- Situation de départ : le simulateur reçoit une commande non reconnue, une carte mal formée, ou un point de départ situé hors de la carte ou sur un obstacle.
- Action : traitement de cette entrée par le simulateur.
- Résultat attendu : manque une décision — l'intention ne précise pas si le simulateur doit rejeter l'entrée, signaler une erreur au système appelant, ou adopter un autre comportement — voir Questions ouvertes.

## Conception proposée

- **Modèle d'état du rover** (proposition) : l'état du rover est représenté par sa position (x, y) et son orientation (N, S, E ou W). Chaque commande de la liste transforme cet état en un nouvel état, selon les règles d'EX-02 à EX-05. Ce modèle découle directement des entrées et du comportement décrits dans l'intention.
- **Rotation** (proposition) : les orientations N, S, E, W forment un cycle ; une rotation à droite avance d'un cran dans le sens N→E→S→W→N, une rotation à gauche recule d'un cran dans ce même cycle. Ce choix découle directement de « tourne de 90 degrés à droite ou à gauche » et n'introduit pas de règle nouvelle.
- **Modèle de carte** (proposition à valider) : la carte est représentée comme une grille de cases indexées par (x, y), chaque case étant associée à un statut praticable ou obstacle déterminé par son symbole. La correspondance symbole → statut reste à valider (voir EX-08 et Questions ouvertes).
- **Interpréteur séquentiel** (proposition) : le simulateur traite la liste de commandes comme une séquence d'étapes appliquées une à une à l'état courant du rover, produisant un état final restitué au système appelant (EX-06, EX-07). Ce choix découle directement de « interprète ces commandes et affiche la position et la direction finales ».
- **Frontière du composant** (déjà présent dans l'intention) : le simulateur est un composant appelé par un système plus large (mission control / API) qui fournit toutes les entrées (point de départ, orientation, carte, commandes) et récupère l'état final ; aucune interface utilisateur humaine directe n'est nécessaire à ce stade.
- **Formats d'entrée et de sortie** : volontairement non fixés dans cette conception — le format des commandes (EX-06) et le format de restitution de l'état final (EX-07) dépendent de décisions encore ouvertes (voir Questions ouvertes) et de la convention de repère (voir Réserves).

## Réserves

### RES-01 — Convention de repère entre orientations et coordonnées

Origine : nécessaire pour rendre EX-02 (et par extension EX-03 à EX-07) vérifiable, mais non fournie par l'intention.
Exigences concernées : EX-02, EX-03, EX-04, EX-05, EX-06, EX-07.
Conséquences : sans cette convention (par exemple, quel axe et quel sens correspondent à N, S, E, W, et si elle doit correspondre à une convention attendue par le système appelant), il n'est pas possible de vérifier de façon univoque le résultat d'une avancée sur des coordonnées concrètes.
Décision attendue : le Product Owner doit préciser ou valider la convention de repère (correspondance entre N/S/E/W et le sens de variation de x et y), en tenant compte le cas échéant de ce qu'attend le système appelant.
Décision humaine : le Product Owner (auteur non précisé) indique le 2026-09-22 ne pas pouvoir encore répondre à cette question ; la réserve reste ouverte.
Statut : ouverte — bloquant pour le passage à la phase Build sur EX-02 à EX-07 : sans cette convention, l'avancée du rover et l'état final restitué ne peuvent pas être vérifiés sur des coordonnées concrètes, ni donc implémentés de façon testable. Reste visible avant le passage en Build.

## Questions ouvertes

### Q1 — Signification et coexistence des jeux de symboles de la carte

Question de l'intention : « Les deux jeux de symboles (🟩/🌳 et 🟫/🪨) doivent-ils être supportés simultanément, ou correspondent-ils à des contextes différents ? Quelle est la signification exacte de chaque symbole (terrain praticable vs obstacle) ? »
Réponse humaine : aucune à ce stade.
Exigences concernées : EX-08.
Effet sur le passage à la phase Build : bloquant — sans cette réponse, la lecture de la carte (EX-08) ne peut pas être implémentée. Reste visible avant le passage en Build.

### Q2 — Format d'entrée de la liste de commandes

Question de l'intention : « Quel format précis pour la liste de commandes en entrée (ex : chaîne de caractères, liste d'objets) ? »
Réponse humaine : aucune à ce stade.
Exigences concernées : EX-06.
Effet sur le passage à la phase Build : bloquant — sans ce format, l'interface d'entrée du simulateur ne peut pas être définie. Reste visible avant le passage en Build.

### Q3 — Format de restitution du résultat

Question de l'intention : « Quel format précis pour le résultat affiché (texte, JSON, autre) et comment est-il consommé par le système appelant ? »
Réponse humaine : aucune à ce stade.
Exigences concernées : EX-07.
Effet sur le passage à la phase Build : bloquant — sans ce format, l'interface de sortie du simulateur ne peut pas être définie. Reste visible avant le passage en Build.

### Q4 — Comportement aux limites de la carte

Question de l'intention : « Quel comportement attendu si le rover atteint les limites de la carte ? »
Réponse humaine : aucune à ce stade.
Exigences concernées : EX-09 (et, selon la réponse, potentiellement EX-02).
Effet sur le passage à la phase Build : bloquant — sans cette réponse, le comportement du rover en bordure de carte ne peut pas être implémenté. Reste visible avant le passage en Build.

### Q5 — Comportement en cas d'entrées invalides

Question de l'intention : « Quel comportement attendu en cas de commande, carte ou point de départ invalides ? »
Réponse humaine : aucune à ce stade.
Exigences concernées : EX-10 (et, selon la réponse, potentiellement EX-01, EX-06).
Effet sur le passage à la phase Build : bloquant — sans cette réponse, la validation des entrées ne peut pas être implémentée. Reste visible avant le passage en Build.

## Contexte de génération

### Demande initiale

Commande : `/spec intent/mars-rover-simulator/intent.md`

### Skills utilisées

| Chemin | Commit Git de la version utilisée |
| --- | --- |
| .claude/skills/spec/SKILL.md | 9a14bc67c3cb892a4ef0e2b50b2207a074ec0ce5 |

### Révisions

Aucune révision à ce stade.
