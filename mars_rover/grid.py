"""Carte du terrain : grille rectangulaire de symboles, interprétée en cases libres ou obstacles."""
from __future__ import annotations

OBSTACLE_SYMBOLS = frozenset({"🌳", "🪨"})


class Grid:
    """Grille rectangulaire de dimensions fixes.

    Toute case hors de la grille fournie est considérée libre par défaut (réserve R4).
    """

    def __init__(self, rows: list[list[str]]):
        self._rows = rows
        self._height = len(rows)
        self._width = len(rows[0]) if rows else 0

    def is_free(self, x: int, y: int) -> bool:
        if not self._contains(x, y):
            return True
        return self._rows[y][x] not in OBSTACLE_SYMBOLS

    def _contains(self, x: int, y: int) -> bool:
        return 0 <= y < self._height and 0 <= x < self._width
