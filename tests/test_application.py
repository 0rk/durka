from unittest.mock import MagicMock
from custom_exceptions import CommandError
from Application import Application


def test_application_run_stop_command():
    commands = MagicMock()
    dialog_with_user = MagicMock()
    dialog_with_user.get_command.side_effect = ["stop"]

    app = Application(commands, dialog_with_user)
    app.run()

    dialog_with_user.give_exit_message.assert_called_once()


def test_application_run_unknown_command():
    commands = MagicMock()
    dialog_with_user = MagicMock()
    dialog_with_user.get_command.side_effect = ["unknown command", "stop"]

    app = Application(commands, dialog_with_user)
    app.run()

    dialog_with_user.give_message_to_user.assert_called_once()
    assert isinstance(dialog_with_user.give_message_to_user.call_args[0][0], CommandError)
    assert str(dialog_with_user.give_message_to_user.call_args[0][0]) == "Неизвестная команда! Попробуйте ещё раз"

    dialog_with_user.give_exit_message.assert_called_once()


def test_application_run_get_status_command():
    commands = MagicMock()
    dialog_with_user = MagicMock()
    dialog_with_user.get_command.side_effect = ["get status", "stop"]

    app = Application(commands, dialog_with_user)
    app.run()

    commands.get_patient_status.assert_called_once()


def test_application_run_increase_status_command():
    commands = MagicMock()
    dialog_with_user = MagicMock()
    dialog_with_user.get_command.side_effect = ["status up", "stop"]

    app = Application(commands, dialog_with_user)
    app.run()

    commands.increase_patient_status.assert_called_once()


def test_application_run_decrease_status_command():
    commands = MagicMock()
    dialog_with_user = MagicMock()
    dialog_with_user.get_command.side_effect = ["status down", "stop"]

    app = Application(commands, dialog_with_user)
    app.run()

    commands.decrease_patient_status.assert_called_once()


def test_application_run_discharge_command():
    commands = MagicMock()
    dialog_with_user = MagicMock()
    dialog_with_user.get_command.side_effect = ["discharge", "stop"]

    app = Application(commands, dialog_with_user)
    app.run()

    commands.discharge_patient.assert_called_once()


def test_application_run_calculate_statistics_command():
    commands = MagicMock()
    dialog_with_user = MagicMock()
    dialog_with_user.get_command.side_effect = ["calculate statistics", "stop"]

    app = Application(commands, dialog_with_user)
    app.run()

    commands.show_statistics.assert_called_once()
