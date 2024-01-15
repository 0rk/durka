import re
from Patient import PatientStatus


class DialogWithUser:
    @staticmethod
    def get_status_name(status):
        status_names = {
            PatientStatus.SEVERELY_ILL: "Тяжело болен",
            PatientStatus.ILL: "Болен",
            PatientStatus.SLIGHTLY_ILL: "Слегка болен",
            PatientStatus.READY_TO_DISCHARGE: "Готов к выписке"
        }
        return status_names.get(status, "Неизвестный статус")

    @staticmethod
    def is_positive_integer(value):
        try:
            return int(value) > 0
        except ValueError:
            return False

    @staticmethod
    def typo_checking(command):
        # Заменяем в строке символы [ао] на [ао] и символы [ие] на [ие]
        modified_command = re.sub(r'[ао]', '[ао]', command, flags=re.IGNORECASE | re.UNICODE)
        modified_command = re.sub(r'[ие]', '[ие]', modified_command, flags=re.IGNORECASE | re.UNICODE)

        # Создаем паттерн из модифицированной строки с добавлением границ слов
        pattern = re.compile(r'\b' + modified_command + r'\b', re.IGNORECASE | re.UNICODE)
        return pattern

    @staticmethod
    def get_patient_id(hospital):
        patient_id = input("Введите ID пациента: ")
        if DialogWithUser.is_positive_integer(patient_id):
            if int(patient_id) <= len(hospital.patients):
                return int(patient_id)
            else:
                raise ValueError("Ошибка. В больнице нет пациента с таким ID")

        raise TypeError("Ошибка. ID пациента должно быть числом (целым, положительным)")

    @staticmethod
    def get_command(prompt="Введите команду: "):
        command = input(prompt).lower()
        return DialogWithUser.typo_checking(command)

    @staticmethod
    def proposal_discharge_patient():
        confirm = input("Желаете этого клиента выписать? (да/нет): ").lower()
        if confirm in ["да", "нет"]:
            return confirm
        else:
            raise ValueError("Некорректный ввод.")

    @staticmethod
    def return_message_to_user(message):
        print(message)

    def exit_message(self):
        self.return_message_to_user("Сеанс завершён.")

    def return_statistics(self, total_patients, statuses_count):
        self.return_message_to_user(f"В больнице на данный момент находится {total_patients} чел., из них:")
        self.print_status_count("Тяжело болен", PatientStatus.SEVERELY_ILL, statuses_count)
        self.print_status_count("Болен", PatientStatus.ILL, statuses_count)
        self.print_status_count("Слегка болен", PatientStatus.SLIGHTLY_ILL, statuses_count)
        self.print_status_count("Готов к выписке", PatientStatus.READY_TO_DISCHARGE, statuses_count)

    def print_status_count(self, status_name, status_enum, statuses_count):
        if statuses_count[status_enum] > 0:
            self.return_message_to_user(f"\tв статусе '{status_name}': {statuses_count[status_enum]} чел.")

    def patient_status(self, patient):
        self.return_message_to_user(f"Статус пациента: '{self.get_status_name(patient)}'")

    def new_patient_status(self, patient):
        self.return_message_to_user(f"Новый статус пациента: '{self.get_status_name(patient)}'")

    def remind_patient_status(self, patient):
        self.return_message_to_user(f"Пациент остался в статусе '{self.get_status_name(patient)}'")

    def discharge_patient(self):
        self.return_message_to_user("Пациент выписан из больницы")
