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


def test_get_patient_status_invalid_id(command):
    """Тест проверки получение статуса некорректный ID"""
    invalid_ids = ["-1", "0", "1.5", "str", "строка"]
    for invalid_id in invalid_ids:
        with mock.patch('builtins.input', return_value=invalid_id):
            buffer = StringIO()
            sys.stdout = buffer
            command.get_patient_status()
            # f = open("demofile3.txt", "a+")
            # f.write(str(output))
            # f.close()
        output = buffer.getvalue()
        assert output == "Ошибка. ID пациента должно быть числом (целым, положительным)\n"


def test_get_patient_status_absent_id(command):
    """Тест проверки получение статуса некорректный ID"""
    invalid_ids = ["201"]
    for invalid_id in invalid_ids:
        with mock.patch('builtins.input', return_value=invalid_id):
            buffer = StringIO()
            sys.stdout = buffer
            command.get_patient_status()
        output = buffer.getvalue()
        assert output == "Ошибка. В больнице нет пациента с таким ID\n"


def test_get_patient_status_valid_id(command):
    """Тест проверки получение статуса корректный ID"""
    valid_ids = ["1", "50", "200"]
    for invalid_id in valid_ids:
        with mock.patch('builtins.input', return_value=invalid_id):
            buffer = StringIO()
            sys.stdout = buffer
            command.get_patient_status()
        output = buffer.getvalue()
        assert output == "Статус пациента: 'Болен'\n"


def test_get_patient_all_status(command_all_status):
    """Тест проверки получение статуса все возможные виды статусов"""
    valid_ids = ["1", "2", "3", "4"]
    status = list(Patient.STATUS_NAMES.values())

    for valid_id, valid_name in zip(valid_ids, status):
        with mock.patch('builtins.input', return_value=valid_id):
            buffer = StringIO()
            sys.stdout = buffer
            command_all_status.get_patient_status()
        output = buffer.getvalue()
        assert output == f"Статус пациента: '{valid_name}'\n"


def test_increase_patient_status_invalid_id(command):
    """Тест увеличения статуса пациента невалидный ID"""
    invalid_ids = ["-1", "0", "1.5", "str", "строка"]
    for invalid_id in invalid_ids:
        with mock.patch('builtins.input', return_value=invalid_id):
            buffer = StringIO()
            sys.stdout = buffer
            command.increase_patient_status()
        output = buffer.getvalue()
        assert output == "Ошибка. ID пациента должно быть числом (целым, положительным)\n"


def test_increase_patient_status_absent_id(command):
    """Тест увеличения статуса пациента невалидный ID"""
    invalid_ids = ["201"]
    for invalid_id in invalid_ids:
        with mock.patch('builtins.input', return_value=invalid_id):
            buffer = StringIO()
            sys.stdout = buffer
            command.increase_patient_status()
        output = buffer.getvalue()
        assert output == "Ошибка. В больнице нет пациента с таким ID\n"


def test_increase_patient_status_valid_id(command):
    """Тест увеличения статуса пациента валидный ID"""
    valid_ids = ["1", "50", "200"]
    for valid_id in valid_ids:
        with mock.patch('builtins.input', return_value=valid_id):
            buffer = StringIO()
            sys.stdout = buffer
            command.increase_patient_status()
        output = buffer.getvalue()
        assert output == "Новый статус пациента: 'Слегка болен'\n"


def test_increase_patient_all_status_with_discharge(command_all_status):
    """Тест увеличения статуса пациента валидный ID все возможные виды статусов"""
    valid_ids = ["1", "2", "3", "4"]
    with mock.patch('builtins.input', side_effect=['1', '2', '3', '4', 'да']):
        buffer = StringIO()
        sys.stdout = buffer
        for patients in range(len(valid_ids)):
            command_all_status.increase_patient_status()
        output = buffer.getvalue()
        assert output == "Новый статус пациента: 'Болен'\n" \
                         "Новый статус пациента: 'Слегка болен'\n" \
                         "Новый статус пациента: 'Готов к выписке'\n" \
                         "Пациент выписан из больницы\n"


def test_increase_patient_all_status_without_discharge(command_all_status):
    """Тест увеличения статуса пациента валидный ID все возможные виды статусов"""
    valid_ids = ["1", "2", "3", "4"]
    with mock.patch('builtins.input', side_effect=['1', '2', '3', '4', 'нет']):
        buffer = StringIO()
        sys.stdout = buffer
        for patients in range(len(valid_ids)):
            command_all_status.increase_patient_status()
        output = buffer.getvalue()
        assert output == "Новый статус пациента: 'Болен'\n" \
                         "Новый статус пациента: 'Слегка болен'\n" \
                         "Новый статус пациента: 'Готов к выписке'\n" \
                         "Пациент остался в статусе 'Готов к выписке'\n"
