class Console:
    def __init__(self, hospital, dialog_with_user):
        self.hospital = hospital
        self.dialog_with_user = dialog_with_user

    def get_patient_status(self):
        self.perform_patient_action(self.hospital.get_patient_status)

    def increase_patient_status(self):
        self.perform_patient_action(self.hospital.increase_patient_status)

    def decrease_patient_status(self):
        self.perform_patient_action(self.hospital.decrease_patient_status)

    def discharge_patient(self):
        self.perform_patient_action(self.hospital.discharge_patient)

    def perform_patient_action(self, action_function):
        patient_id = self.dialog_with_user.get_patient_id(self.hospital)
        if patient_id is not None:
            print(action_function(patient_id))

    def print_statistics(self):
        self.hospital.calculate_statistics()

    @staticmethod
    def print_exit_message():
        print("Сеанс завершён.")
