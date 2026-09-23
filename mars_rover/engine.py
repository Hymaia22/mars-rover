"""Moteur d'exécution : applique séquentiellement les commandes sur l'état du rover.

Ne déplace jamais le rover sur un obstacle (réserve R1) et arrête l'exécution
au premier obstacle rencontré, sans exécuter les commandes restantes (réserve R7).
"""
from __future__ import annotations

from typing import Callable

from .commands import Command, parse_commands
from .errors import format_obstacle_error
from .grid import Grid
from .result import SimulationResult
from .rover import Rover

OnCommandExecuted = Callable[[Rover], None]


def simulate(
    rover: Rover,
    grid: Grid,
    commands: str,
    on_command_executed: OnCommandExecuted | None = None,
) -> SimulationResult:
    for command in parse_commands(commands):
        if command is Command.LEFT:
            rover = rover.turned_left()
        elif command is Command.RIGHT:
            rover = rover.turned_right()
        elif command is Command.FORWARD:
            advanced = rover.advanced()
            if not grid.is_free(advanced.position.x, advanced.position.y):
                error_message = format_obstacle_error(rover.position, rover.direction)
                return SimulationResult(rover.position, rover.direction, blocked=True, error_message=error_message)
            rover = advanced

        if on_command_executed is not None:
            on_command_executed(rover)

    return SimulationResult(rover.position, rover.direction, blocked=False)
