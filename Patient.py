from enum import Enum
from custom_exceptions import MinimalStatusCantDownError, MaximumStatusCantUpError


class PatientStatus(Enum):
    SEVERELY_ILL = 0
    ILL = 1
    SLIGHTLY_ILL = 2
    READY_TO_DISCHARGE = 3


class Patient:
    STATUS_NAMES = {
        PatientStatus.SEVERELY_ILL: "Тяжело болен",
        PatientStatus.ILL: "Болен",
        PatientStatus.SLIGHTLY_ILL: "Слегка болен",
        PatientStatus.READY_TO_DISCHARGE: "Готов к выписке"
    }

    def __init__(self, patient_id, status=PatientStatus.ILL):
        self.id = patient_id
        self.status = status

    def __eq__(self, other):
        if isinstance(other, Patient):
            return self.id == other.id and self.status == other.status
        return False

    def can_increase_status(self):
        """Запрос: можно ли увеличить статус пациента"""
        return self.status.value < PatientStatus.READY_TO_DISCHARGE.value

    def can_decrease_status(self):
        """Запрос: можно ли уменьшить статус пациента"""
        return self.status.value > PatientStatus.SEVERELY_ILL.value

    def increase_status(self):
        """Команда: увеличивает статус пациента, если это возможно"""
        if self.can_increase_status():
            self.status = PatientStatus(self.status.value + 1)
        else:
            raise MaximumStatusCantUpError

    def decrease_status(self):
        """Команда: уменьшает статус пациента, если это возможно"""
        if self.can_decrease_status():
            self.status = PatientStatus(self.status.value - 1)
        else:
            raise MinimalStatusCantDownError

    @staticmethod
    def get_status_name(status):
        """Запрос: возвращает имя статуса пациента"""
        return Patient.STATUS_NAMES.get(status, "Неизвестный статус")
