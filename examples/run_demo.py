#!/usr/bin/env python3
"""Rejoue le scénario de démonstration et affiche la position et
l'orientation finales du rover.
"""
from pathlib import Path

from mars_rover.rover import Direction, Position, Rover

SCENARIO_PATH = Path(__file__).parent / "scenario.txt"
DEFAULT_SCENARIO = "FFRFFLF"

_ACTIONS = {
    "F": Rover.advanced,
    "R": Rover.turned_right,
    "L": Rover.turned_left,
}


def load_scenario() -> str:
    if not SCENARIO_PATH.exists():
        SCENARIO_PATH.write_text(DEFAULT_SCENARIO + "\n")
    return SCENARIO_PATH.read_text().strip()


def main() -> None:
    commands = load_scenario()
    rover = Rover(Position(0, 0), Direction.N)
    for command in commands:
        action = _ACTIONS.get(command)
        if action is not None:
            rover = action(rover)

    print(f"Position finale : ({rover.position.x}, {rover.position.y})")
    print(f"Orientation finale : {rover.direction.value}")


if __name__ == "__main__":
    main()
