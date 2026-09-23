from mars_rover.rover import Direction, Position, Rover


def test_turn_right_changes_orientation_not_position():
    rover = Rover(Position(2, 2), Direction.N)

    turned = rover.turned_right()

    assert turned.direction is Direction.E
    assert turned.position == Position(2, 2)


def test_turn_left_changes_orientation_not_position():
    rover = Rover(Position(2, 2), Direction.N)

    turned = rover.turned_left()

    assert turned.direction is Direction.W
    assert turned.position == Position(2, 2)


def test_turn_right_full_cycle_returns_to_original_orientation():
    rover = Rover(Position(0, 0), Direction.N)

    for _ in range(4):
        rover = rover.turned_right()

    assert rover.direction is Direction.N


def test_advance_moves_one_cell_in_current_direction():
    rover = Rover(Position(2, 2), Direction.N)

    advanced = rover.advanced()

    assert advanced.position == Position(2, 3)
    assert advanced.direction is Direction.N
