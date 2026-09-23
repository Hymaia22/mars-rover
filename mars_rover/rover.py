"""État du rover : position et orientation, avec ses rotations.

Convention : Nord = y croissant, Est = x croissant.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Direction(Enum):
    N = "N"
    E = "E"
    S = "S"
    W = "W"


_CLOCKWISE = [Direction.N, Direction.E, Direction.S, Direction.W]

_FORWARD_DELTA = {
    Direction.N: (0, 1),
    Direction.E: (1, 0),
    Direction.S: (0, -1),
    Direction.W: (-1, 0),
}


@dataclass(frozen=True)
class Position:
    x: int
    y: int

    def moved(self, direction: Direction) -> Position:
        dx, dy = _FORWARD_DELTA[direction]
        return Position(self.x + dx, self.y + dy)


@dataclass(frozen=True)
class Rover:
    position: Position
    direction: Direction

    def turned_right(self) -> Rover:
        index = _CLOCKWISE.index(self.direction)
        return Rover(self.position, _CLOCKWISE[(index + 1) % 4])

    def turned_left(self) -> Rover:
        index = _CLOCKWISE.index(self.direction)
        return Rover(self.position, _CLOCKWISE[(index - 1) % 4])

    def advanced(self) -> Rover:
        return Rover(self.position.moved(self.direction), self.direction)
