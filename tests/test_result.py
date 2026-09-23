from dataclasses import FrozenInstanceError

import pytest

from mars_rover.result import SimulationResult
from mars_rover.rover import Direction, Position


def test_simulation_result_defaults_to_no_error_message():
    result = SimulationResult(Position(0, 0), Direction.N, blocked=False)

    assert result.error_message is None


def test_simulation_result_is_immutable():
    result = SimulationResult(Position(0, 0), Direction.N, blocked=False)

    with pytest.raises(FrozenInstanceError):
        result.blocked = True  # type: ignore[misc]
