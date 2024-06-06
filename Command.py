from custom_exceptions import PatientIdNotIntAndPositiveError, MinimalStatusCantDownError, PatientNotExistsError


class Command:
    def __init__(self, hospital, dialog_with_user):
        self._hospital = hospital
        self._dialog_with_user = dialog_with_user

    def get_patient_status(self):
        """Команда: выводит статус пациента"""
        try:
            patient_id = self._get_patient_id()
            patient_status = self._hospital.get_patient_status(patient_id)
            self._dialog_with_user.patient_status(patient_status)
        except PatientNotExistsError as exception:
            self._dialog_with_user.return_message_to_user(str(exception))

    def increase_patient_status(self):
        """Команда: увеличивает статус пациента"""
        try:
            patient_id = self._get_patient_id()
            possibility_increase_status = self._hospital.possibility_increase_status(patient_id)
            if possibility_increase_status:
                self._hospital.increase_patient_status(patient_id)
                new_patient_status = self._hospital.get_patient_status(patient_id)
                self._dialog_with_user.new_patient_status(new_patient_status)
            else:
                """Если статус пациента повысить нельзя, предполагаем что его пора выписывать"""
                confirm = self._dialog_with_user.proposal_discharge_patient()
                if confirm:
                    self._hospital.discharge_patient(patient_id)
                    self._dialog_with_user.discharge_patient()
                else:
                    patient_status = self._hospital.get_patient_status(patient_id)
                    self._dialog_with_user.remind_patient_status(patient_status)
        except PatientIdNotIntAndPositiveError as exception:
            self._dialog_with_user.return_message_to_user(exception)

    def decrease_patient_status(self):
        """Команда: уменьшает статус пациента"""
        try:
            patient_id = self._get_patient_id()
            self._hospital.decrease_patient_status(patient_id)
            patient_status = self._hospital.get_patient_status(patient_id)
            self._dialog_with_user.new_patient_status(patient_status)
        except (MinimalStatusCantDownError, PatientIdNotIntAndPositiveError) as exception:
            self._dialog_with_user.return_message_to_user(exception)

    def discharge_patient(self):
        """Команда: выписывает пациента"""
        try:
            patient_id = self._get_patient_id()
            self._hospital.discharge_patient(patient_id)
            self._dialog_with_user.discharge_patient()
        except PatientIdNotIntAndPositiveError as exception:
            self._dialog_with_user.return_message_to_user(exception)

    def show_statistics(self):
        """Команда: выводит статистику по пациентам"""
        total_patients, statuses_count = self._hospital.calculate_statistics()
        self._dialog_with_user.return_message_to_user(f"В больнице на данный момент находится "
                                                      f"{total_patients} чел., из них:")
        for status_name, count in statuses_count.items():
            if count > 0:
                self._dialog_with_user.return_message_to_user(f"\tв статусе '{status_name}': {count} чел.")

    def _get_patient_id(self):
        """Запрос: получает ID пациента от пользователя"""
        patient_id = self._dialog_with_user.get_patient_id()
        self._hospital.patient_exist(patient_id)
        return patient_id
