from enum import Enum


class PatientStatus(Enum):
    SEVERELY_ILL = 0
    ILL = 1
    SLIGHTLY_ILL = 2
    READY_TO_DISCHARGE = 3


class Patient:
    def __init__(self, patient_id, status=PatientStatus.ILL):
        self.id = patient_id
        self.status = status

    def increase_status(self):
        if self.status.value < PatientStatus.READY_TO_DISCHARGE.value:
            self.status = PatientStatus(self.status.value + 1)
            return True
        else:
            return False

    def decrease_status(self):
        if self.status.value > PatientStatus.SEVERELY_ILL.value:
            self.status = PatientStatus(self.status.value - 1)
            return True
        else:
            return False
