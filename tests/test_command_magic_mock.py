from Hospital import Hospital
from Command import Command
from DialogWithUser import DialogWithUser
from Patient import Patient, PatientStatus
from custom_exceptions import PatientIdNotIntAndPositiveError

from unittest.mock import MagicMock, patch
from io import StringIO
import sys
import pytest


@pytest.fixture
def command():
    hospital = Hospital([Patient(patient_id) for patient_id in range(1, 201)])
    dialog_with_user = DialogWithUser()
    return Command(hospital, dialog_with_user)


@pytest.fixture
def command_all_status():
    patients = [Patient(patient_id, status) for patient_id, status in zip(range(1, 5), PatientStatus)]
    hospital = Hospital(patients)
    dialog_with_user = DialogWithUser()
    return Command(hospital, dialog_with_user)


@patch('builtins.input', lambda _: "1.5")
def test_get_patient_status_invalid_id_solo(command):
    """Тест проверки получение статуса некорректный ID"""
    with patch('builtins.input', lambda _: "input_value"):
        buffer = StringIO()
        sys.stdout = buffer
        command.get_patient_status()
        output = buffer.getvalue()
        assert output == "Ошибка. ID пациента должно быть числом (целым, положительным)\n"


@pytest.mark.parametrize("input_value", ["1.5", "0", "1.5", "str", "строка"])
def test_get_patient_status_invalid_id(input_value):
    """Тест проверки получения статуса некорректный ID"""
    with patch('builtins.input', return_value=input_value):

        command = Command(MagicMock(), MagicMock())
        command._dialog_with_user.get_patient_id = MagicMock(side_effect=PatientIdNotIntAndPositiveError(
            "Ошибка. ID пациента должно быть числом (целым, положительным)"))
        command.get_patient_status()
        command._dialog_with_user.give_message_to_user.assert_called_with(
            "Ошибка. ID пациента должно быть числом (целым, положительным)"
        )


@patch('builtins.input', lambda _: "201")
def test_get_patient_status_absent_id(command):
    """Тест проверки получение статуса некорректный ID"""
    buffer = StringIO()
    sys.stdout = buffer
    command.get_patient_status()
    output = buffer.getvalue()
    assert output == "Ошибка. В больнице нет пациента с таким ID\n"


@pytest.mark.parametrize("valid_id", [1, 50, 200])
def test_get_patient_status_valid_id(command, valid_id):
    """Тест проверки получение статуса корректный ID"""
    command._dialog_with_user.get_patient_id = MagicMock(return_value=valid_id)
    buffer = StringIO()
    sys.stdout = buffer
    command.get_patient_status()
    output = buffer.getvalue()
    assert output == "Статус пациента: 'Болен'\n"


@pytest.mark.parametrize("valid_id, status", [(1, "Тяжело болен"), (2, "Болен"),
                                              (3, "Слегка болен"), (4, "Готов к выписке")])
def test_get_patient_all_status(command_all_status, valid_id, status):
    """Тест проверки получение статуса все возможные виды статусов"""
    command_all_status._dialog_with_user.get_patient_id = MagicMock(return_value=valid_id)
    buffer = StringIO()
    sys.stdout = buffer
    command_all_status.get_patient_status()
    output = buffer.getvalue()
    assert output == f"Статус пациента: '{status}'\n"


@pytest.mark.parametrize("invalid_id", ["-1", "0", "1.5", "str", "строка"])
def test_increase_patient_status_invalid_id(command, invalid_id):
    """Тест увеличения статуса пациента невалидный ID"""
    with patch('builtins.input', return_value=invalid_id):
        buffer = StringIO()
        sys.stdout = buffer
        command.increase_patient_status()
        output = buffer.getvalue()
        assert output == "Ошибка. ID пациента должно быть числом (целым, положительным)\n"


@patch('builtins.input', lambda _: "201")
def test_increase_patient_status_absent_id(command):
    """Тест увеличения статуса пациента невалидный ID"""
    buffer = StringIO()
    sys.stdout = buffer
    command.increase_patient_status()
    output = buffer.getvalue()
    assert output == "Ошибка. В больнице нет пациента с таким ID\n"


@pytest.mark.parametrize("valid_id", [1, 50, 200])
def test_increase_patient_status_valid_id(command, valid_id):
    """Тест увеличения статуса пациента валидный ID"""
    command._dialog_with_user.get_patient_id = MagicMock(return_value=valid_id)
    buffer = StringIO()
    sys.stdout = buffer
    command.increase_patient_status()
    output = buffer.getvalue()
    assert output == "Новый статус пациента: 'Слегка болен'\n"
