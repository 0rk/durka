from Console import Console
from Hospital import Hospital
from Patient import Patient
from DialogWithUser import DialogWithUser
from Application import Application

from unittest import mock
from io import StringIO
import sys
import pytest


@pytest.fixture
def hospital():
    hospital = Hospital([Patient(patient_id) for patient_id in range(1, 201)])
    dialog_with_user = DialogWithUser()

    return Console(hospital, dialog_with_user)


@pytest.fixture
def application():
    hospital = Hospital([Patient(patient_id) for patient_id in range(1, 201)])
    dialog_with_user = DialogWithUser()
    commands = Console(hospital, dialog_with_user)
    return Application(commands)


def test_increase_patient_status_valid(hospital):
    """Тест увеличения статуса пациента валидный ID"""
    with mock.patch('builtins.input', return_value="1"):
        buffer = StringIO()
        sys.stdout = buffer
        Console.increase_patient_status(hospital)
        output = buffer.getvalue()
        assert output == "Новый статус пациента: 'Слегка болен'\n"


def test_increase_patient_status_absent_id(hospital):
    """Тест увеличения статуса пациента невалидный ID"""
    invalid_ids = ["201"]
    for invalid_id in invalid_ids:
        with mock.patch('builtins.input', return_value=invalid_id):
            buffer = StringIO()
            sys.stdout = buffer
            with pytest.raises(ValueError) as exception:
                Console.increase_patient_status(hospital)
            assert str(exception.value) == "Ошибка. В больнице нет пациента с таким ID"


def test_increase_patient_status_invalid_id(hospital):
    """Тест увеличения статуса пациента некорректный ID"""
    invalid_ids = ["0", "-2", "1.5"]
    for invalid_id in invalid_ids:
        with mock.patch('builtins.input', return_value=invalid_id):
            with pytest.raises(TypeError) as exception:
                Console.increase_patient_status(hospital)
            assert str(exception.value) == "Ошибка. ID пациента должно быть числом (целым, положительным)"


def test_increase_patient_status_maximun_discharge(hospital):
    """Тест увеличения статуса пациента до максимального значения с выпиской"""
    with mock.patch('builtins.input', side_effect=['1', '1', '1', 'да']):
        buffer = StringIO()
        sys.stdout = buffer
        for time in range(3):
            Console.increase_patient_status(hospital)
        output = buffer.getvalue()
        assert output == "Новый статус пациента: 'Слегка болен'\n" \
                         "Новый статус пациента: 'Готов к выписке'\n" \
                         "Пациент выписан из больницы\n"


def test_increase_patient_status_maximun_without_discharge(hospital):
    """Тест увеличения статуса пациента до максимального значения без выписки"""
    with mock.patch('builtins.input', side_effect=['1', '1', '1', 'нет']):
        buffer = StringIO()
        sys.stdout = buffer
        for time in range(3):
            Console.increase_patient_status(hospital)
        output = buffer.getvalue()
        assert output == "Новый статус пациента: 'Слегка болен'\n" \
                         "Новый статус пациента: 'Готов к выписке'\n" \
                         "Пациент остался в статусе 'Готов к выписке'\n"


def test_print_statistics(hospital):
    """Расчет статистики"""
    buffer = StringIO()
    sys.stdout = buffer
    Console.print_statistics(hospital)
    output = buffer.getvalue()
    assert output == "В больнице на данный момент находится 200 чел., из них:\n" \
                     "\tв статусе 'Болен': 200 чел.\n"


def test_print_statistics_all_status(hospital):
    """Расчет статистики все варианты статусов"""
    with mock.patch('builtins.input', side_effect=['1', '2', '3', '3']):
        buffer = StringIO()
        sys.stdout = buffer
        Console.decrease_patient_status(hospital)
        for time in range(3):
            Console.increase_patient_status(hospital)
        Console.print_statistics(hospital)
        output = buffer.getvalue()
        assert output == "Новый статус пациента: 'Тяжело болен'\n" \
                         "Новый статус пациента: 'Слегка болен'\n" \
                         "Новый статус пациента: 'Слегка болен'\n" \
                         "Новый статус пациента: 'Готов к выписке'\n" \
                         "В больнице на данный момент находится 200 чел., из них:\n" \
                         "\tв статусе 'Тяжело болен': 1 чел.\n" \
                         "\tв статусе 'Болен': 197 чел.\n" \
                         "\tв статусе 'Слегка болен': 1 чел.\n" \
                         "\tв статусе 'Готов к выписке': 1 чел.\n"


def test_work_day_basic_version(application):
    """Тест базового сценария"""
    with mock.patch('builtins.input', side_effect=['узнать статус пациента', '200',
                                                   'status up', '2',
                                                   'status down', '3',
                                                   'discharge', '4',
                                                   'рассчитать статистику',
                                                   'стоп']):
        buffer = StringIO()
        sys.stdout = buffer
        application.run()
        output = buffer.getvalue()
        assert output == "Статус пациента: 'Болен'\n" \
                         "Новый статус пациента: 'Слегка болен'\n" \
                         "Новый статус пациента: 'Тяжело болен'\n" \
                         "Пациент выписан из больницы\n" \
                         "В больнице на данный момент находится 199 чел., из них:\n" \
                         "\tв статусе 'Тяжело болен': 1 чел.\n" \
                         "\tв статусе 'Болен': 197 чел.\n" \
                         "\tв статусе 'Слегка болен': 1 чел.\n" \
                         "Сеанс завершён.\n"


def test_work_day_patient_discharge(application):
    """Тест повышения статус на максимальное значение, которая приводит к выписке пациента"""
    with mock.patch('builtins.input', side_effect=['повысить статус пациента', '1',
                                                   'повысить статус пациента', '1',
                                                   'повысить статус пациента', '1', 'да',
                                                   'рассчитать статистику',
                                                   'стоп']):
        buffer = StringIO()
        sys.stdout = buffer
        application.run()
        output = buffer.getvalue()
        assert output == "Новый статус пациента: 'Слегка болен'\n" \
                         "Новый статус пациента: 'Готов к выписке'\n" \
                         "Пациент выписан из больницы\n" \
                         "В больнице на данный момент находится 199 чел., из них:\n" \
                         "\tв статусе 'Болен': 199 чел.\n" \
                         "Сеанс завершён.\n"


def test_work_day_patient_without_discharge(application):
    """Тест повышения статус на максимальное значение, которая приводит к выписке пациента"""
    with mock.patch('builtins.input', side_effect=['повысить статус пациента', '1',
                                                   'повысить статус пациента', '1',
                                                   'повысить статус пациента', '1', 'нет',
                                                   'рассчитать статистику',
                                                   'стоп']):
        buffer = StringIO()
        sys.stdout = buffer
        application.run()
        output = buffer.getvalue()
        assert output == "Новый статус пациента: 'Слегка болен'\n" \
                         "Новый статус пациента: 'Готов к выписке'\n" \
                         "Пациент остался в статусе 'Готов к выписке'\n" \
                         "В больнице на данный момент находится 200 чел., из них:\n" \
                         "\tв статусе 'Болен': 199 чел.\n" \
                         "\tв статусе 'Готов к выписке': 1 чел.\n" \
                         "Сеанс завершён.\n"


def test_work_day_failed_attempt_to_demote_lowest_status(application):
    """Тест неудачная попытка понизить самый низкий статус"""
    with mock.patch('builtins.input', side_effect=['понизить статус пациента', '1',
                                                   'понизить статус пациента', '1',
                                                   'рассчитать статистику',
                                                   'стоп']):
        buffer = StringIO()
        sys.stdout = buffer
        application.run()
        output = buffer.getvalue()
        assert output == "Новый статус пациента: 'Тяжело болен'\n" \
                         "Ошибка. Нельзя понизить самый низкий статус (наши пациенты не умирают).\n" \
                         "В больнице на данный момент находится 200 чел., из них:\n" \
                         "\tв статусе 'Тяжело болен': 1 чел.\n" \
                         "\tв статусе 'Болен': 199 чел.\n" \
                         "Сеанс завершён.\n"
