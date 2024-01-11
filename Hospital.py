from Patient import Patient, PatientStatus


class Hospital:
    def __init__(self, patients=None):
        if patients is None:
            patients = [Patient(patient_id) for patient_id in range(1, 201)]
        self.patients = patients

    @staticmethod
    def get_status_name(status):
        status_names = {
            PatientStatus.SEVERELY_ILL: "Тяжело болен",
            PatientStatus.ILL: "Болен",
            PatientStatus.SLIGHTLY_ILL: "Слегка болен",
            PatientStatus.READY_TO_DISCHARGE: "Готов к выписке"
        }
        return status_names.get(status, "Неизвестный статус")

    def get_patient_status(self, patient_id):
        patient = self.get_patient(patient_id)
        return f"Статус пациента: '{self.get_status_name(patient.status)}'" \
            if patient else "Ошибка. Введите корректный ID пациента."

    def increase_patient_status(self, patient_id):
        patient = self.get_patient(patient_id)
        if patient:
            if patient.increase_status():
                return f"Новый статус пациента: '{self.get_status_name(patient.status)}'"
            else:
                confirm = input("Желаете этого клиента выписать? (да/нет): ").lower()
                if confirm == "да":
                    self.patients.remove(patient)
                    return "Пациент выписан из больницы"
                elif confirm == "нет":
                    return f"Пациент остался в статусе '{self.get_status_name(patient.status)}'"
                else:
                    return "Некорректный ввод."
        else:
            return "Ошибка. Введите корректный ID пациента."

    def decrease_patient_status(self, patient_id):
        patient = self.get_patient(patient_id)
        return f"Новый статус пациента: '{self.get_status_name(patient.status)}'" \
            if patient and patient.decrease_status() else \
            "Ошибка. Нельзя понизить самый низкий статус (наши пациенты не умирают)."

    def discharge_patient(self, patient_id):
        patient = self.get_patient(patient_id)
        if patient:
            self.patients.remove(patient)
            return "Пациент выписан из больницы"
        else:
            return "Ошибка. Введите корректный ID пациента."

    def calculate_statistics(self):
        total_patients = len(self.patients)
        statuses_count = {status: 0 for status in PatientStatus}

        for patient in self.patients:
            statuses_count[patient.status] += 1

        print(f"В больнице на данный момент находится {total_patients} чел., из них:")

        self._print_status_count("Тяжело болен", PatientStatus.SEVERELY_ILL, statuses_count)
        self._print_status_count("Болен", PatientStatus.ILL, statuses_count)
        self._print_status_count("Слегка болен", PatientStatus.SLIGHTLY_ILL, statuses_count)
        self._print_status_count("Готов к выписке", PatientStatus.READY_TO_DISCHARGE, statuses_count)

    @staticmethod
    def _print_status_count(status_name, status_enum, statuses_count):
        if statuses_count[status_enum] > 0:
            print(f"\tв статусе '{status_name}': {statuses_count[status_enum]} чел.")

    def get_patient(self, patient_id):
        return next((patient for patient in self.patients if patient.id == patient_id), None)
