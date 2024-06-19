from custom_exceptions import PatientIdNotIntAndPositiveError, MinimalStatusCantDownError, PatientNotExistsError


class Command:
    def __init__(self, hospital, dialog_with_user):
        self._hospital = hospital
        self._dialog_with_user = dialog_with_user

    def get_patient_status(self):
        """Команда: выводит статус пациента"""
        try:
            patient_id = self._dialog_with_user.get_patient_id()
            patient_status = self._hospital.get_patient_status(patient_id)
            self._dialog_with_user.give_patient_status(patient_status)
        except (PatientNotExistsError, PatientIdNotIntAndPositiveError) as exception:
            self._dialog_with_user.give_message_to_user(str(exception))

    def increase_patient_status(self):
        """Команда: увеличивает статус пациента"""
        try:
            patient_id = self._dialog_with_user.get_patient_id()
            self._process_patient_status_increase(patient_id)
        except (PatientIdNotIntAndPositiveError, PatientNotExistsError) as exception:
            self._dialog_with_user.give_message_to_user(exception)

    def _process_patient_status_increase(self, patient_id):
        """Обработка увеличения статуса пациента"""
        if self._hospital.can_increase_patient_status(patient_id):
            self._hospital.increase_patient_status(patient_id)
            new_patient_status = self._hospital.get_patient_status(patient_id)
            self._dialog_with_user.give_new_patient_status(new_patient_status)
        else:
            self._handle_discharge_process(patient_id)

    def _handle_discharge_process(self, patient_id):
        """Обработка процесса выписки пациента"""
        confirm = self._dialog_with_user.give_proposal_discharge_patient()
        if confirm:
            self._hospital.discharge_patient(patient_id)
            self._dialog_with_user.give_discharge_patient()
        else:
            patient_status = self._hospital.get_patient_status(patient_id)
            self._dialog_with_user.give_remind_patient_status(patient_status)

    def decrease_patient_status(self):
        """Команда: уменьшает статус пациента"""
        try:
            patient_id = self._dialog_with_user.get_patient_id()
            self._hospital.decrease_patient_status(patient_id)
            patient_status = self._hospital.get_patient_status(patient_id)
            self._dialog_with_user.give_new_patient_status(patient_status)
        except (MinimalStatusCantDownError, PatientIdNotIntAndPositiveError) as exception:
            self._dialog_with_user.give_message_to_user(exception)

    def discharge_patient(self):
        """Команда: выписывает пациента"""
        try:
            patient_id = self._dialog_with_user.get_patient_id()
            self._hospital.discharge_patient(patient_id)
            self._dialog_with_user.give_discharge_patient()
        except PatientIdNotIntAndPositiveError as exception:
            self._dialog_with_user.give_message_to_user(exception)

    def show_statistics(self):
        """Команда: выводит статистику по пациентам"""
        total_patients, statuses_count = self._hospital.calculate_statistics()
        self._dialog_with_user.give_message_to_user(f"В больнице на данный момент находится "
                                                    f"{total_patients} чел., из них:")
        for status_name, count in statuses_count.items():
            if count > 0:
                self._dialog_with_user.give_message_to_user(f"\tв статусе '{status_name}': {count} чел.")
