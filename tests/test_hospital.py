from Hospital import Hospital
from Patient import Patient, PatientStatus

import pytest


@pytest.fixture
def hospital():
    return Hospital([Patient(patient_id) for patient_id in range(1, 201)])


@pytest.fixture
def hospital_all_status():
    return Hospital([Patient(patient_id, patient_status)
                     for patient_id, patient_status in zip(range(1, 5), PatientStatus)])


def test_get_patient_status_invalid_id(hospital):
    """Тест проверки получение статуса некорректный ID"""
    invalid_ids = [-1, 0, 1.5, 201, "str", "строка"]
    for invalid_id in invalid_ids:
        with pytest.raises(ValueError) as exception:
            hospital.get_patient_status(invalid_id)
        assert str(exception.value) == "Ошибка. Введите корректный ID пациента."


def test_get_patient_status_valid_id(hospital):
    """Тест проверки получение статуса корректный ID"""
    valid_ids = [1, 50, 200]
    for valid_id in valid_ids:
        output = hospital.get_patient_status(valid_id)
        assert str(output) == "Болен"


def test_get_patient_all_status(hospital_all_status):
    """Тест проверки получение статуса все возможные виды статусов"""
    valid_ids = [1, 2, 3, 4]
    status = list(Patient.STATUS_NAMES.values())

    for valid_id, valid_name in zip(valid_ids, status):
        output = hospital_all_status.get_patient_status(valid_id)
        assert str(output) == valid_name


def test_increase_patient_status_invalid_id(hospital):
    """Тест увеличения статуса пациента невалидный ID"""
    invalid_ids = [-1, 0, 1.5, 201, "str", "строка"]
    for invalid_id in invalid_ids:
        with pytest.raises(ValueError) as exception:
            hospital.increase_patient_status(invalid_id)
        assert str(exception.value) == "Ошибка. Введите корректный ID пациента."


def test_increase_patient_status_valid_id(hospital):
    """Тест увеличения статуса пациента валидный ID"""
    valid_ids = [1, 50, 200]
    for valid_id in valid_ids:
        output = hospital.increase_patient_status(valid_id)
        assert output == ('Слегка болен', False)


def test_increase_patient_all_status(hospital_all_status):
    """Тест увеличения статуса пациента валидный ID все возможные виды статусов"""
    valid_ids = [1, 2, 3, 4]
    statuses = [('Болен', False), ('Слегка болен', False), ('Готов к выписке', False), ('Готов к выписке', True)]
    for valid_id, status in zip(valid_ids, statuses):
        output = hospital_all_status.increase_patient_status(valid_id)
        assert output == status
