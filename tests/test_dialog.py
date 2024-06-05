from DialogWithUser import DialogWithUser

from unittest import mock
import pytest
from custom_exceptions import PatientIdNotIntAndPositiveError


@pytest.fixture
def dialog():
    return DialogWithUser()


@pytest.mark.parametrize("invalid_id", ["-1", "0", "1.5", "str", "строка"])
def test_get_patient_id_invalid_id(dialog, invalid_id):
    """Тест проверки получение статуса некорректный ID"""
    with mock.patch('builtins.input', return_value=invalid_id):
        with pytest.raises(PatientIdNotIntAndPositiveError) as exception:
            dialog.get_patient_id()
        assert str(exception.value) == "Ошибка. ID пациента должно быть числом (целым, положительным)"


@pytest.mark.parametrize("invalid_id, int_patient_id", [("201", 201)])
def test_get_patient_id_absent_id(dialog, invalid_id, int_patient_id):
    """Тест проверки получение статуса некорректный ID"""
    with mock.patch('builtins.input', return_value=invalid_id):
        patient_id = dialog.get_patient_id()
    assert patient_id == int_patient_id


@pytest.mark.parametrize("valid_id, int_patient_id", [("1", 1), ("50", 50), ("200", 200)])
def test_get_patient_id_valid_id(dialog, valid_id, int_patient_id):
    """Тест проверки получение статуса некорректный ID"""
    with mock.patch('builtins.input', return_value=valid_id):
        patient_id = dialog.get_patient_id()
    assert patient_id == int_patient_id


@pytest.mark.parametrize("valid_id, discharge_avalible", [("да", True), ("нет", False)])
def test_discharge_patient_valid_input(dialog, valid_id, discharge_avalible):
    """Тест проверки получение статуса некорректный ID"""
    with mock.patch('builtins.input', return_value=valid_id):
        confirm = dialog.proposal_discharge_patient()
    assert confirm == discharge_avalible


@pytest.mark.parametrize("invalid_id", ["yes", "no", "123", "до", "нит"])
def test_discharge_patient_invalid_input(dialog, invalid_id):
    """Тест проверки получение статуса некорректный ID"""
    with mock.patch('builtins.input', return_value=invalid_id):
        with pytest.raises(ValueError) as exception:
            dialog.proposal_discharge_patient()
    assert str(exception.value) == "Некорректный ввод."
