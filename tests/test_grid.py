from mars_rover.grid import Grid


def _grid():
    return Grid([
        ["🟩", "🌳"],
        ["🟫", "🪨"],
    ])


def test_recognizes_free_symbols():
    grid = _grid()

    assert grid.is_free(0, 0) is True  # 🟩
    assert grid.is_free(0, 1) is True  # 🟫


def test_recognizes_obstacle_symbols():
    grid = _grid()

    assert grid.is_free(1, 0) is False  # 🌳
    assert grid.is_free(1, 1) is False  # 🪨


def test_cell_beyond_provided_grid_is_free_by_default():
    grid = _grid()

    assert grid.is_free(100, 100) is True
    assert grid.is_free(-5, -5) is True
