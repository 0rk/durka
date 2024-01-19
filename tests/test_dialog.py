from DialogWithUser import DialogWithUser

from unittest import mock
from io import StringIO
import sys
import pytest


@pytest.fixture
def dialog():
    return DialogWithUser()


def test_get_patient_id_invalid_id(dialog):
    """Тест проверки получение статуса некорректный ID"""
    invalid_ids = ["-1", "0", "1.5", "str", "строка"]
    for invalid_id in invalid_ids:
        with mock.patch('builtins.input', return_value=invalid_id):
            with pytest.raises(ValueError) as exception:
                dialog.get_patient_id()
            assert str(exception.value) == "Ошибка. ID пациента должно быть числом (целым, положительным)"

def test_get_patient_id_absent_id(dialog):
    """Тест проверки получение статуса некорректный ID"""
    invalid_ids = ["201"]
    for invalid_id in invalid_ids:
        with mock.patch('builtins.input', return_value=invalid_id):
            patient_id = dialog.get_patient_id()
        assert patient_id == int(invalid_id)


def test_get_patient_id_valid_id(dialog):
    """Тест проверки получение статуса некорректный ID"""
    valid_ids = ["1", "50", "200"]
    for valid_id in valid_ids:
        with mock.patch('builtins.input', return_value=valid_id):
            patient_id = dialog.get_patient_id()
        assert patient_id == int(valid_id)


def test_discharge_patient_valid_input(dialog):
    """Тест проверки получение статуса некорректный ID"""
    valid_ids = ["да", "нет"]
    for valid_id in valid_ids:
        with mock.patch('builtins.input', return_value=valid_id):
            confirm = dialog.proposal_discharge_patient()
        assert confirm == valid_id


def test_discharge_patient_invalid_input(dialog):
    """Тест проверки получение статуса некорректный ID"""
    invalid_ids = ["yes", "no", "123", "до", "нит"]
    for invalid_id in invalid_ids:
        with mock.patch('builtins.input', return_value=invalid_id):
            with pytest.raises(ValueError) as exception:
                dialog.proposal_discharge_patient()
        assert str(exception.value) == "Некорректный ввод."
