from Patient import Patient, PatientStatus


class Hospital:
    def __init__(self, patients=None):
        if patients is None:
            patients = [Patient(patient_id) for patient_id in range(1, 201)]
        self.patients = patients

    def get_patient_status(self, patient_id):
        patient = self.get_patient(patient_id)
        if patient:
            return patient.status
        else:
            raise ValueError("Ошибка. Введите корректный ID пациента.")

    def increase_patient_status(self, patient_id):
        patient = self.get_patient(patient_id)
        if patient:
            if patient.increase_status():
                return patient_id, patient.status, False
            else:
                return patient_id, patient.status, True
        else:
            raise ValueError("Ошибка. Введите корректный ID пациента.")

    def decrease_patient_status(self, patient_id):
        patient = self.get_patient(patient_id)
        if patient and patient.decrease_status():
            return patient.status
        else:
            raise ValueError("Ошибка. Нельзя понизить самый низкий статус (наши пациенты не умирают).")

    def discharge_patient(self, patient_id):
        patient = self.get_patient(patient_id)
        if patient:
            self.patients.remove(patient)
            return True
        else:
            raise ValueError("Ошибка. Введите корректный ID пациента.")

    def calculate_statistics(self):
        total_patients = len(self.patients)
        statuses_count = {status: 0 for status in PatientStatus}

        for patient in self.patients:
            statuses_count[patient.status] += 1

        return total_patients, statuses_count

    def get_patient(self, patient_id):
        return next((patient for patient in self.patients if patient.id == patient_id), None)
