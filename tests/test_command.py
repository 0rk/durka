from Hospital import Hospital
from Command import Command
from DialogWithUser import DialogWithUser
from Patient import Patient, PatientStatus

from unittest import mock
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
    hospital = Hospital([Patient(patient_id, patient_status)
                         for patient_id, patient_status in zip(range(1, 5), PatientStatus)])
    dialog_with_user = DialogWithUser()

    return Command(hospital, dialog_with_user)


@pytest.mark.parametrize("invalid_id", ["-1", "0", "1.5", "str", "строка"])
def test_get_patient_status_invalid_id(command, invalid_id):
    """Тест проверки получение статуса некорректный ID"""
    with mock.patch('builtins.input', return_value=invalid_id):
        buffer = StringIO()
        sys.stdout = buffer
        command.get_patient_status()
    output = buffer.getvalue()
    assert output == "Ошибка. ID пациента должно быть числом (целым, положительным)\n"


@pytest.mark.parametrize("invalid_id", ["201"])
def test_get_patient_status_absent_id(command, invalid_id):
    """Тест проверки получение статуса некорректный ID"""
    with mock.patch('builtins.input', return_value=invalid_id):
        buffer = StringIO()
        sys.stdout = buffer
        command.get_patient_status()
    output = buffer.getvalue()
    assert output == "Ошибка. В больнице нет пациента с таким ID\n"


@pytest.mark.parametrize("valid_id", ["1", "50", "200"])
def test_get_patient_status_valid_id(command, valid_id):
    """Тест проверки получение статуса корректный ID"""
    with mock.patch('builtins.input', return_value=valid_id):
        buffer = StringIO()
        sys.stdout = buffer
        command.get_patient_status()
    output = buffer.getvalue()
    assert output == "Статус пациента: 'Болен'\n"


@pytest.mark.parametrize("valid_id,status", [("1", "Тяжело болен"), ("2", "Болен"),
                                             ("3", "Слегка болен"), ("4", "Готов к выписке")])
def test_get_patient_all_status(command_all_status, valid_id, status):
    """Тест проверки получение статуса все возможные виды статусов"""
    with mock.patch('builtins.input', return_value=valid_id):
        buffer = StringIO()
        sys.stdout = buffer
        command_all_status.get_patient_status()
    output = buffer.getvalue()
    assert output == f"Статус пациента: '{status}'\n"


@pytest.mark.parametrize("invalid_id", ["-1", "0", "1.5", "str", "строка"])
def test_increase_patient_status_invalid_id(command, invalid_id):
    """Тест увеличения статуса пациента невалидный ID"""
    with mock.patch('builtins.input', return_value=invalid_id):
        buffer = StringIO()
        sys.stdout = buffer
        command.increase_patient_status()
    output = buffer.getvalue()
    assert output == "Ошибка. ID пациента должно быть числом (целым, положительным)\n"


@pytest.mark.parametrize("invalid_id", ["201"])
def test_increase_patient_status_absent_id(command, invalid_id):
    """Тест увеличения статуса пациента невалидный ID"""
    with mock.patch('builtins.input', return_value=invalid_id):
        buffer = StringIO()
        sys.stdout = buffer
        command.increase_patient_status()
    output = buffer.getvalue()
    assert output == "Ошибка. В больнице нет пациента с таким ID\n"


@pytest.mark.parametrize("valid_id", ["1", "50", "200"])
def test_increase_patient_status_valid_id(command, valid_id):
    """Тест увеличения статуса пациента валидный ID"""
    with mock.patch('builtins.input', return_value=valid_id):
        buffer = StringIO()
        sys.stdout = buffer
        command.increase_patient_status()
    output = buffer.getvalue()
    assert output == "Новый статус пациента: 'Слегка болен'\n"


@pytest.mark.parametrize("valid_id,console_msg", [('1', "Новый статус пациента: 'Болен'\n"),
                                                  ('2', "Новый статус пациента: 'Слегка болен'\n"),
                                                  ('3', "Новый статус пациента: 'Готов к выписке'\n"),
                                                  (['4', 'да'], "Пациент выписан из больницы\n")])
def test_increase_patient_all_status_with_discharge(command_all_status, valid_id, console_msg):
    """Тест увеличения статуса пациента валидный ID все возможные виды статусов"""
    with mock.patch('builtins.input', side_effect=valid_id):
        buffer = StringIO()
        sys.stdout = buffer
        command_all_status.increase_patient_status()
        output = buffer.getvalue()
        assert output == console_msg


@pytest.mark.parametrize("valid_id,console_msg", [('1', "Новый статус пациента: 'Болен'\n"),
                                                  ('2', "Новый статус пациента: 'Слегка болен'\n"),
                                                  ('3', "Новый статус пациента: 'Готов к выписке'\n"),
                                                  (['4', 'нет'], "Пациент остался в статусе 'Готов к выписке'\n")])
def test_increase_patient_all_status_without_discharge(command_all_status, valid_id, console_msg):
    """Тест увеличения статуса пациента валидный ID все возможные виды статусов"""
    with mock.patch('builtins.input', side_effect=valid_id):
        buffer = StringIO()
        sys.stdout = buffer
        command_all_status.increase_patient_status()
        output = buffer.getvalue()
        assert output == console_msg
