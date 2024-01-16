from enum import Enum


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

    def increase_status(self):
        if self.status.value < PatientStatus.READY_TO_DISCHARGE.value:
            self.status = PatientStatus(self.status.value + 1)
            status_increased = True
        else:
            status_increased = False
        return status_increased

    def decrease_status(self):
        if self.status.value > PatientStatus.SEVERELY_ILL.value:
            self.status = PatientStatus(self.status.value - 1)
            status_decreased = True
        else:
            status_decreased = False
        return status_decreased

    @staticmethod
    def get_status_name(status):
        return Patient.STATUS_NAMES.get(status, "Неизвестный статус")
