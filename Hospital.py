from Patient import Patient
from custom_exceptions import PatientNotExistsError


class Hospital:
    def __init__(self, patients=None):
        if patients is None:
            patients = [Patient(patient_id) for patient_id in range(1, 201)]
        self._patients = patients

    def get_patient_status(self, patient_id):
        """Запрос: возвращает статус пациента"""
        patient = self.get_patient(patient_id)
        return Patient.get_status_name(patient.status)

    def can_increase_patient_status(self, patient_id):
        """Запрос: проверяет, можно ли повысить статус пациента"""
        patient = self.get_patient(patient_id)
        return patient.can_increase_status()

    def can_decrease_patient_status(self, patient_id):
        """Запрос: проверяет, можно ли понизить статус пациента"""
        patient = self.get_patient(patient_id)
        return patient.can_decrease_status()

    def increase_patient_status(self, patient_id):
        """Команда: повышает статус пациента, если это возможно"""
        patient = self.get_patient(patient_id)
        patient.increase_status()

    def decrease_patient_status(self, patient_id):
        """Команда: понижает статус пациента, если это возможно"""
        patient = self.get_patient(patient_id)
        patient.decrease_status()

    def discharge_patient(self, patient_id):
        """Команда: выписывает пациента, если это возможно"""
        patient = self.get_patient(patient_id)
        self._patients.remove(patient)

    def calculate_statistics(self):
        """Запрос: вычисляет статистику по пациентам"""
        total_patients = len(self._patients)
        statuses_count = {status: 0 for status in Patient.STATUS_NAMES}

        for patient in self._patients:
            statuses_count[patient.status] += 1

        return total_patients, {
            Patient.get_status_name(status): count for status, count in statuses_count.items()
        }

    def get_patient(self, patient_id):
        """Запрос: возвращает объект пациента по ID или вызывает исключение, если пациент не существует"""
        patient = next((patient for patient in self._patients if patient.id == patient_id), None)
        if patient is None:
            raise PatientNotExistsError
        return patient
