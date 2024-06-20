from unittest.mock import MagicMock
from Application import Application


def test_find_action_by_command_known_command():
    """Тест нахождения действия для известной команды"""
    commands = MagicMock()
    dialog_with_user = MagicMock()
    app = Application(commands, dialog_with_user)

    command = "get status"
    action = app.find_action_by_command(command)

    assert action == commands.get_patient_status


def test_find_action_by_command_unknown_command():
    """Тест нахождения действия для неизвестной команды"""
    commands = MagicMock()
    dialog_with_user = MagicMock()
    app = Application(commands, dialog_with_user)

    command = "unknown command"
    action = app.find_action_by_command(command)

    assert action is None
