import re
from Patient import PatientStatus


class DialogWithUser:
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
    def get_patient_id():
        patient_id = input("Введите ID пациента: ")
        if DialogWithUser.is_positive_integer(patient_id):
            return int(patient_id)

        raise ValueError("Ошибка. ID пациента должно быть числом (целым, положительным)")

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

    def patient_status(self, patient_status):
        self.return_message_to_user(f"Статус пациента: '{patient_status}'")

    def new_patient_status(self, patient_status):
        self.return_message_to_user(f"Новый статус пациента: '{patient_status}'")

    def remind_patient_status(self, patient_status):
        self.return_message_to_user(f"Пациент остался в статусе '{patient_status}'")

    def discharge_patient(self):
        self.return_message_to_user("Пациент выписан из больницы")
