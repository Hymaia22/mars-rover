"""Un test par scénario décrit dans spec.md (EX-01 à EX-07)."""
from mars_rover.comparator import AlignmentMonitor
from mars_rover.engine import simulate
from mars_rover.grid import Grid
from mars_rover.rover import Direction, Position, Rover


def _free_grid(width: int = 5, height: int = 5) -> Grid:
    return Grid([["🟩"] * width for _ in range(height)])


def test_ex01_receives_inputs_and_starts_executing_commands():
    rover = Rover(Position(0, 0), Direction.N)

    result = simulate(rover, _free_grid(), "F")

    assert result.blocked is False


def test_ex02_rotation_changes_orientation_not_position():
    rover = Rover(Position(2, 2), Direction.N)

    result = simulate(rover, _free_grid(), "R")

    assert result.direction is Direction.E
    assert result.position == Position(2, 2)


def test_ex03_forward_moves_one_cell_in_current_direction():
    rover = Rover(Position(2, 2), Direction.N)

    result = simulate(rover, _free_grid(), "F")

    assert result.position == Position(2, 3)


def test_ex04_forward_blocked_by_obstacle_keeps_rover_immobile_and_returns_error():
    rover = Rover(Position(0, -1), Direction.N)
    grid = Grid([["🌳"]])

    result = simulate(rover, grid, "F")

    assert result.position == Position(0, -1)
    assert result.direction is Direction.N
    assert result.blocked is True
    assert result.error_message == "Obstacle détecté en (0, -1), orientation N"


def test_ex05_map_symbols_are_interpreted_as_free_or_obstacle():
    grid = Grid([["🌳", "🪨", "🟩", "🟫"]])

    assert grid.is_free(0, 0) is False
    assert grid.is_free(1, 0) is False
    assert grid.is_free(2, 0) is True
    assert grid.is_free(3, 0) is True


def test_ex07_alert_triggered_when_simulated_position_diverges_from_real_rover():
    class _FakeProvider:
        def get_position(self) -> Position:
            return Position(9, 9)

    alerts = []
    monitor = AlignmentMonitor(_FakeProvider(), lambda sim, real: alerts.append((sim, real)))
    rover = Rover(Position(0, 0), Direction.N)

    simulate(rover, _free_grid(), "F", on_command_executed=lambda r: monitor.check(r.position))

    assert alerts == [(Position(0, 1), Position(9, 9))]
