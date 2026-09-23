"""Comparateur avec le vrai rover (EX-07) : déclenché après chaque commande exécutée.

La source réelle de la position du vrai rover reste hors périmètre (réserve
R8) ; ce module ne fournit qu'un point d'extension (Protocol), pas
d'implémentation réelle.
"""
from __future__ import annotations

from typing import Callable, Protocol

from .rover import Position


class RealRoverPositionProvider(Protocol):
    def get_position(self) -> Position: ...


AlertCallback = Callable[[Position, Position], None]


class AlignmentMonitor:
    """Compare la position simulée à celle du vrai rover et alerte en cas d'écart."""

    def __init__(self, provider: RealRoverPositionProvider, alert: AlertCallback):
        self._provider = provider
        self._alert = alert

    def check(self, simulated_position: Position) -> bool:
        real_position = self._provider.get_position()
        aligned = real_position == simulated_position
        if not aligned:
            self._alert(simulated_position, real_position)
        return aligned
