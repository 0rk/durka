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


@pytest.mark.parametrize("invalid_id", [-1, 0, 1.5, 201, "str", "строка"])
def test_get_patient_status_invalid_id(hospital, invalid_id):
    """Тест проверки получение статуса некорректный ID"""
    with pytest.raises(ValueError) as exception:
        hospital.get_patient_status(invalid_id)
    assert str(exception.value) == "Ошибка. Введите корректный ID пациента."


@pytest.mark.parametrize("valid_id", [1, 50, 200])
def test_get_patient_status_valid_id(hospital, valid_id):
    """Тест проверки получение статуса корректный ID"""
    output = hospital.get_patient_status(valid_id)
    assert str(output) == "Болен"


@pytest.mark.parametrize("valid_id, status", [(1, "Тяжело болен"),
                                              (2, "Болен"),
                                              (3, "Слегка болен"),
                                              (4, "Готов к выписке")])
def test_get_patient_all_status(hospital_all_status, valid_id, status):
    """Тест проверки получение статуса все возможные виды статусов"""
    output = hospital_all_status.get_patient_status(valid_id)
    assert str(output) == status


@pytest.mark.parametrize("invalid_id", [-1, 0, 1.5, 201, "str", "строка"])
def test_increase_patient_status_invalid_id(hospital, invalid_id):
    """Тест увеличения статуса пациента невалидный ID"""
    with pytest.raises(ValueError) as exception:
        hospital.increase_patient_status(invalid_id)
    assert str(exception.value) == "Ошибка. Введите корректный ID пациента."


@pytest.mark.parametrize("valid_id", [1, 50, 200])
def test_increase_patient_status_valid_id(hospital, valid_id):
    """Тест увеличения статуса пациента валидный ID"""
    possibility_discharge = hospital.can_discharge_patient(valid_id)
    hospital.increase_patient_status(valid_id)
    output = (hospital.get_patient_status(valid_id), possibility_discharge)
    assert output == ('Слегка болен', False)


@pytest.mark.parametrize("valid_id, status", [(1, ('Болен', False)),
                                              (2, ('Слегка болен', False)),
                                              (3, ('Готов к выписке', False)),
                                              (4, ('Готов к выписке', True))])
def test_increase_patient_all_status(hospital_all_status, valid_id, status):
    """Тест увеличения статуса пациента валидный ID все возможные виды статусов"""
    possibility_discharge = hospital_all_status.can_discharge_patient(valid_id)
    hospital_all_status.increase_patient_status(valid_id)
    output = (hospital_all_status.get_patient_status(valid_id), possibility_discharge)
    assert output == status
