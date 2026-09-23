from mars_rover.commands import Command, parse_commands


def test_parses_valid_commands_in_order():
    assert parse_commands("FRL") == [Command.FORWARD, Command.RIGHT, Command.LEFT]


def test_ignores_invalid_characters():
    assert parse_commands("FXR L") == [Command.FORWARD, Command.RIGHT, Command.LEFT]


def test_empty_command_list_returns_no_commands():
    assert parse_commands("") == []
