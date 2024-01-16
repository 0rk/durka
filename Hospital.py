from Patient import Patient


class Hospital:
    def __init__(self, patients=None):
        if patients is None:
            patients = [Patient(patient_id) for patient_id in range(1, 201)]
        self._patients = patients

    def get_patient_status(self, patient_id):
        patient = self.get_patient(patient_id)
        if patient:
            return Patient.get_status_name(patient.status)
        else:
            raise ValueError("Ошибка. Введите корректный ID пациента.")

    def increase_patient_status(self, patient_id):
        patient = self.get_patient(patient_id)
        if patient:
            if patient.increase_status():
                possibility_discharge = False
            else:
                possibility_discharge = True
            return Patient.get_status_name(patient.status), possibility_discharge
        else:
            raise ValueError("Ошибка. Введите корректный ID пациента.")

    def decrease_patient_status(self, patient_id):
        patient = self.get_patient(patient_id)
        if patient and patient.decrease_status():
            return Patient.get_status_name(patient.status)
        else:
            raise ValueError("Ошибка. Нельзя понизить самый низкий статус (наши пациенты не умирают).")

    def discharge_patient(self, patient_id):
        patient = self.get_patient(patient_id)
        if patient:
            self._patients.remove(patient)
            return True
        else:
            raise ValueError("Ошибка. Введите корректный ID пациента.")

    def calculate_statistics(self):
        total_patients = len(self._patients)
        statuses_count = {status: 0 for status in Patient.STATUS_NAMES}

        for patient in self._patients:
            statuses_count[patient.status] += 1

        return total_patients, {
            Patient.get_status_name(status): count for status, count in statuses_count.items()
        }

    def get_patient(self, patient_id):
        return next((patient for patient in self._patients if patient.id == patient_id), None)
