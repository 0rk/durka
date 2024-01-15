class Console:
    def __init__(self, hospital, dialog_with_user):
        self.hospital = hospital
        self.dialog_with_user = dialog_with_user

    def get_patient_status(self):
        patient_status = self.perform_patient_action(self.hospital.get_patient_status)
        self.dialog_with_user.patient_status(patient_status)

    def increase_patient_status(self):
        patient_id, patient_status, possibility_discharge = self.perform_patient_action(
            self.hospital.increase_patient_status)
        if possibility_discharge:
            confirm = self.dialog_with_user.proposal_discharge_patient()
            if confirm == "да":
                self.hospital.discharge_patient(patient_id)
                self.dialog_with_user.discharge_patient()
            elif confirm == "нет":
                self.dialog_with_user.remind_patient_status(patient_status)

        else:
            self.dialog_with_user.new_patient_status(patient_status)

    def decrease_patient_status(self):
        patient_status = self.perform_patient_action(self.hospital.decrease_patient_status)
        self.dialog_with_user.new_patient_status(patient_status)

    def discharge_patient(self):
        self.perform_patient_action(self.hospital.discharge_patient)
        self.dialog_with_user.discharge_patient()

    def perform_patient_action(self, action_function):
        patient_id = self.dialog_with_user.get_patient_id(self.hospital)
        if patient_id is not None:
            return action_function(patient_id)

    def return_statistics(self):
        total_patients, statuses_count = self.hospital.calculate_statistics()
        self.dialog_with_user.return_statistics(total_patients, statuses_count)
