class Console:
    def __init__(self, hospital, dialog_with_user):
        self._hospital = hospital
        self._dialog_with_user = dialog_with_user

    def get_patient_status(self):
        try:
            patient_id = self.get_patient_id()
            patient_status = self._hospital.get_patient_status(patient_id)
            self._dialog_with_user.patient_status(patient_status)
        except ValueError as exception:
            self._dialog_with_user.return_message_to_user(exception)

    def increase_patient_status(self):
        try:
            patient_id = self.get_patient_id()
            patient_status, possibility_discharge = self._hospital.increase_patient_status(patient_id)
            if possibility_discharge:
                confirm = self._dialog_with_user.proposal_discharge_patient()
                if confirm == "да":
                    self._hospital.discharge_patient(patient_id)
                    self._dialog_with_user.discharge_patient()
                elif confirm == "нет":
                    self._dialog_with_user.remind_patient_status(patient_status)

            else:
                self._dialog_with_user.new_patient_status(patient_status)
        except ValueError as exception:
            self._dialog_with_user.return_message_to_user(exception)

    def decrease_patient_status(self):
        try:
            patient_id = self.get_patient_id()
            patient_status = self._hospital.decrease_patient_status(patient_id)
            self._dialog_with_user.new_patient_status(patient_status)
        except ValueError as exception:
            self._dialog_with_user.return_message_to_user(exception)

    def discharge_patient(self):
        try:
            patient_id = self.get_patient_id()
            self._hospital.discharge_patient(patient_id)
            self._dialog_with_user.discharge_patient()
        except ValueError as exception:
            self._dialog_with_user.return_message_to_user(exception)

    def return_statistics(self):
        total_patients, statuses_count = self._hospital.calculate_statistics()
        self._dialog_with_user.return_message_to_user(f"В больнице на данный момент находится "
                                                      f"{total_patients} чел., из них:")
        for status_name, count in statuses_count.items():
            if count > 0:
                self._dialog_with_user.return_message_to_user(f"\tв статусе '{status_name}': {count} чел.")

    def get_patient_id(self):
        patient_id = self._dialog_with_user.get_patient_id()
        if self._hospital.get_patient(patient_id) and patient_id is not None:
            return patient_id
        else:
            raise ValueError("Ошибка. В больнице нет пациента с таким ID")
