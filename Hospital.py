from Patient import Patient, PatientStatus
from custom_exceptions import MinimalStatusCantDownError, PatientNotExistsError


class Hospital:
    def __init__(self, patients=None):
        if patients is None:
            patients = [Patient(patient_id) for patient_id in range(1, 201)]
        self._patients = patients

    def get_patient_status(self, patient_id):
        """Запрос: возвращает статус пациента"""
        patient = self.get_patient(patient_id)
        if patient:
            return Patient.get_status_name(patient.status)
        else:
            raise PatientNotExistsError("Ошибка. Введите корректный ID пациента.")

    def can_increase_patient_status(self, patient_id):
        """Запрос: проверяет, можно ли повысить статус пациента"""
        patient = self.get_patient(patient_id)
        if patient:
            return patient.can_increase_status()
        else:
            raise PatientNotExistsError("Ошибка. Введите корректный ID пациента.")

    def can_decrease_patient_status(self, patient_id):
        """Запрос: проверяет, можно ли понизить статус пациента"""
        patient = self.get_patient(patient_id)
        if patient:
            return patient.can_decrease_status()
        else:
            raise PatientNotExistsError("Ошибка. Введите корректный ID пациента.")

    def possibility_increase_status(self, patient_id):
        """Запрос: проверяет, можно ли выписать пациента"""
        patient = self.get_patient(patient_id)
        if patient:
            return patient.status != PatientStatus.READY_TO_DISCHARGE
        else:
            raise PatientNotExistsError("Ошибка. Введите корректный ID пациента.")

    def increase_patient_status(self, patient_id):
        """Команда: повышает статус пациента, если это возможно"""
        patient = self.get_patient(patient_id)
        if patient and patient.can_increase_status():
            patient.increase_status()
        else:
            if not patient:
                raise PatientNotExistsError("Ошибка. Введите корректный ID пациента.")
            if not patient.can_increase_status():
                pass

    def decrease_patient_status(self, patient_id):
        """Команда: понижает статус пациента, если это возможно"""
        patient = self.get_patient(patient_id)
        if patient and patient.can_decrease_status():
            patient.decrease_status()
        else:
            raise MinimalStatusCantDownError("Ошибка. Нельзя понизить самый низкий статус (наши пациенты не умирают).")

    def discharge_patient(self, patient_id):
        """Команда: выписывает пациента, если это возможно"""
        patient = self.get_patient(patient_id)
        if patient:
            self._patients.remove(patient)
        else:
            raise PatientNotExistsError("Ошибка. Введите корректный ID пациента.")

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
        """Запрос: возвращает объект пациента по ID"""
        return next((patient for patient in self._patients if patient.id == patient_id), None)

    def patient_exist(self, patient_id):
        """Запрос: проверяет, существует ли пациент с данным ID"""
        if not self.get_patient(patient_id):
            raise PatientNotExistsError("Ошибка. В больнице нет пациента с таким ID")
