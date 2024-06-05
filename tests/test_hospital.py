from Hospital import Hospital
from Patient import Patient, PatientStatus
from custom_exceptions import PatientNotExistsError

import pytest


def test_get_patient_status_valid_id():
    """Тест проверки получение статуса корректный ID"""
    hospital = Hospital([Patient(1, PatientStatus.ILL)])
    output = hospital.get_patient_status(1)
    assert str(output) == "Болен"


@pytest.mark.parametrize("invalid_id", [-1, 0, 1.5, 201, "str", "строка"])
def test_get_patient_status_invalid_id(invalid_id):
    """Тест проверки получение статуса некорректный ID"""
    with pytest.raises(PatientNotExistsError) as exception:
        hospital = Hospital([Patient(1, PatientStatus.ILL)])
        hospital.get_patient_status(invalid_id)
    assert str(exception.value) == "Ошибка. Введите корректный ID пациента."


def test_get_patient_all_status():
    hospital_all_status = Hospital([Patient(1, PatientStatus.SEVERELY_ILL),
                                    Patient(2, PatientStatus.ILL),
                                    Patient(3, PatientStatus.SLIGHTLY_ILL),
                                    Patient(4, PatientStatus.READY_TO_DISCHARGE),])
    """Тест проверки получение статуса все возможные виды статусов"""
    output = hospital_all_status.get_patient_status(4)
    assert str(output) == "Готов к выписке"


@pytest.mark.parametrize("invalid_id", [-1, 0, 1.5, 201, "str", "строка"])
def test_increase_patient_status_invalid_id(invalid_id):
    """Тест увеличения статуса пациента невалидный ID"""
    with pytest.raises(PatientNotExistsError) as exception:
        hospital = Hospital([Patient(1, PatientStatus.ILL)])
        hospital.increase_patient_status(invalid_id)
    assert str(exception.value) == "Ошибка. Введите корректный ID пациента."


def test_increase_patient_status_valid_id():
    """Тест увеличения статуса пациента валидный ID"""
    hospital = Hospital([Patient(1, PatientStatus.ILL),
                         Patient(2, PatientStatus.ILL),
                         Patient(3, PatientStatus.ILL)])
    hospital.increase_patient_status(3)
    assert hospital._patients[2].status == PatientStatus.SLIGHTLY_ILL
