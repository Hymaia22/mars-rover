"""Interpréteur de commandes : traduit la liste de commandes en actions (F, R, L).

Un caractère qui n'est ni F, ni R, ni L est ignoré (décision PO-2 du plan).
"""
from __future__ import annotations

from enum import Enum


class Command(Enum):
    FORWARD = "F"
    RIGHT = "R"
    LEFT = "L"


_VALID_CHARACTERS = {command.value for command in Command}


def parse_commands(commands: str) -> list[Command]:
    return [Command(char) for char in commands if char in _VALID_CHARACTERS]
