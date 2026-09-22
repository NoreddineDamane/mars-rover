"""Simulateur de rover martien — scaffold minimal et provisoire.

Ce module a ete cree uniquement pour permettre `make test` et `make run` de
fonctionner. Les choix ci-dessous (convention orientation <-> (x, y), format
des commandes, format de sortie, comportement aux limites et sur entree
invalide) sont provisoires : ils comblent des decisions encore ouvertes dans
intent/mars-rover-simulator/spec.md (RES-01, Q1 a Q5) et devront etre revus
une fois ces decisions actees par le Product Owner.
"""

DIRECTIONS = ["N", "E", "S", "W"]

MOVES = {
    "N": (0, 1),
    "E": (1, 0),
    "S": (0, -1),
    "W": (-1, 0),
}


class Rover:
    def __init__(self, x, y, orientation, obstacles=None):
        self.x = x
        self.y = y
        self.orientation = orientation
        self.obstacles = obstacles or set()

    def turn_left(self):
        idx = DIRECTIONS.index(self.orientation)
        self.orientation = DIRECTIONS[(idx - 1) % 4]

    def turn_right(self):
        idx = DIRECTIONS.index(self.orientation)
        self.orientation = DIRECTIONS[(idx + 1) % 4]

    def move_forward(self):
        dx, dy = MOVES[self.orientation]
        nx, ny = self.x + dx, self.y + dy
        if (nx, ny) in self.obstacles:
            return
        self.x, self.y = nx, ny

    def execute(self, commands):
        for command in commands:
            if command == "F":
                self.move_forward()
            elif command == "L":
                self.turn_left()
            elif command == "R":
                self.turn_right()

    def state(self):
        return (self.x, self.y, self.orientation)


def parse_scenario(text):
    x = y = 0
    orientation = "N"
    obstacles = set()
    commands = ""
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        parts = line.split()
        if parts[0] == "START":
            x, y, orientation = int(parts[1]), int(parts[2]), parts[3]
        elif parts[0] == "OBSTACLE":
            obstacles.add((int(parts[1]), int(parts[2])))
        elif parts[0] == "COMMANDS":
            commands = parts[1]
    return x, y, orientation, obstacles, commands


def run_scenario(text):
    x, y, orientation, obstacles, commands = parse_scenario(text)
    rover = Rover(x, y, orientation, obstacles)
    rover.execute(commands)
    return rover.state()
