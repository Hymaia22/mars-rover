from mars_rover.engine import simulate
from mars_rover.grid import Grid
from mars_rover.rover import Direction, Position, Rover


def _free_grid(width: int = 5, height: int = 5) -> Grid:
    return Grid([["🟩"] * width for _ in range(height)])


def test_forward_moves_rover_one_cell_on_free_cell():
    rover = Rover(Position(2, 2), Direction.N)

    result = simulate(rover, _free_grid(), "F")

    assert result.position == Position(2, 3)
    assert result.direction is Direction.N
    assert result.blocked is False
    assert result.error_message is None


def test_forward_beyond_provided_grid_continues_on_free_default_terrain():
    rover = Rover(Position(0, 0), Direction.N)

    result = simulate(rover, Grid([["🟩"]]), "FFF")

    assert result.position == Position(0, 3)
    assert result.blocked is False

