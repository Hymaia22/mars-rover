"""Message d'erreur renvoyé quand le rover est bloqué par un obstacle (réserve R6)."""
from __future__ import annotations

from .rover import Direction, Position


def format_obstacle_error(position: Position, direction: Direction) -> str:
    return f"Obstacle détecté en ({position.x}, {position.y}), orientation {direction.value}"
