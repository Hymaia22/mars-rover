"""Résultat final d'une simulation : position et orientation, avec un message d'erreur en cas de blocage (PO-3)."""
from __future__ import annotations

from dataclasses import dataclass

from .rover import Direction, Position


@dataclass(frozen=True)
class SimulationResult:
    position: Position
    direction: Direction
    blocked: bool
    error_message: str | None = None
