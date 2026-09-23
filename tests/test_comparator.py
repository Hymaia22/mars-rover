from mars_rover.comparator import AlignmentMonitor
from mars_rover.rover import Position


class _FakeProvider:
    def __init__(self, position: Position):
        self._position = position

    def get_position(self) -> Position:
        return self._position


def test_no_alert_when_positions_match():
    alerts = []
    monitor = AlignmentMonitor(_FakeProvider(Position(1, 1)), lambda sim, real: alerts.append((sim, real)))

    assert monitor.check(Position(1, 1)) is True
    assert alerts == []


def test_alert_triggered_on_mismatch():
    alerts = []
    monitor = AlignmentMonitor(_FakeProvider(Position(5, 5)), lambda sim, real: alerts.append((sim, real)))

    assert monitor.check(Position(1, 1)) is False
    assert alerts == [(Position(1, 1), Position(5, 5))]
