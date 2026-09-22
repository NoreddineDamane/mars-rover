# Intent : Simulateur de rover Mars
Auteur : non renseigné.

## Problème
L'équipe qui construit Mars Rover doit fournir un simulateur capable d'interpréter une liste de commandes de déplacement pour un rover et d'en déterminer l'état final, afin qu'un système plus large puisse piloter le rover et connaître sa position.

## Résultat proposé
Un simulateur qui, à partir d'un point de départ (x, y), d'une orientation initiale (N, S, E ou W), d'une carte indiquant les obstacles et d'une liste de commandes, interprète ces commandes et affiche la position et la direction finales du rover. Le rover avance ou tourne de 90 degrés à droite ou à gauche ; il reste immobile lorsqu'un obstacle bloque son avancée.

## Utilisateurs et systèmes concernés
Le simulateur est intégré à un système plus large (type mission control / API), qui envoie les commandes et récupère l'état final du rover. Aucun utilisateur final direct n'est identifié à ce stade.

## Contraintes
- Entrées : point de départ (x, y), orientation initiale (N, S, E, W), carte des obstacles, liste de commandes.
- Le rover peut avancer, ou tourner de 90° à droite ou à gauche.
- Le rover reste immobile si une commande d'avancée le mènerait sur un obstacle.
- La carte peut employer deux jeux de symboles : 🟩 et 🌳, ou 🟫 et 🪨.

## Questions ouvertes
- Les deux jeux de symboles (🟩/🌳 et 🟫/🪨) doivent-ils être supportés simultanément, ou correspondent-ils à des contextes différents ? Quelle est la signification exacte de chaque symbole (terrain praticable vs obstacle) ?
- Quel format précis pour la liste de commandes en entrée (ex : chaîne de caractères, liste d'objets) ?
- Quel format précis pour le résultat affiché (texte, JSON, autre) et comment est-il consommé par le système appelant ?
- Quel comportement attendu si le rover atteint les limites de la carte ?
- Quel comportement attendu en cas de commande, carte ou point de départ invalides ?
