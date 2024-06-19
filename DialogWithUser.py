import re
from custom_exceptions import PatientIdNotIntAndPositiveError


class DialogWithUser:
    @staticmethod
    def _is_positive_integer(value):
        """Запрос: проверяет, является ли значение положительным целым числом"""
        try:
            return int(value) > 0
        except ValueError:
            return False

    @staticmethod
    def _typo_checking(command):
        """Запрос: проверяет опечатки в команде"""
        # Заменяем в строке символы [ао] на [ао] и символы [ие] на [ие]
        modified_command = re.sub(r'[ао]', '[ао]', command, flags=re.IGNORECASE | re.UNICODE)
        modified_command = re.sub(r'[ие]', '[ие]', modified_command, flags=re.IGNORECASE | re.UNICODE)

        # Создаем паттерн из модифицированной строки с добавлением границ слов
        pattern = re.compile(r'\b' + modified_command + r'\b', re.IGNORECASE | re.UNICODE)
        return pattern

    def get_patient_id(self):
        """Запрос: получает ID пациента от пользователя"""
        patient_id = input("Введите ID пациента: ")
        if self._is_positive_integer(patient_id):
            return int(patient_id)
        raise PatientIdNotIntAndPositiveError

    @staticmethod
    def get_command(prompt="Введите команду: "):
        """Запрос: получает команду от пользователя"""
        command = input(prompt).lower()
        return DialogWithUser._typo_checking(command)

    @staticmethod
    def give_proposal_discharge_patient():
        """Запрос: спрашивает пользователя, желает ли он выписать пациента"""
        confirm = input("Желаете этого клиента выписать? (да/нет): ").lower()
        if confirm in ["да", "нет"]:
            if confirm == "да":
                return True
            else:
                return False
        else:
            raise ValueError("Некорректный ввод.")

    @staticmethod
    def give_message_to_user(message):
        """Команда: выводит сообщение пользователю"""
        print(message)

    def give_exit_message(self):
        """Команда: выводит сообщение о завершении сеанса"""
        self.give_message_to_user("Сеанс завершён.")

    def give_patient_status(self, patient_status):
        """Команда: выводит статус пациента"""
        self.give_message_to_user(f"Статус пациента: '{patient_status}'")

    def give_new_patient_status(self, patient_status):
        """Команда: выводит новый статус пациента"""
        self.give_message_to_user(f"Новый статус пациента: '{patient_status}'")

    def give_remind_patient_status(self, patient_status):
        """Команда: напоминает о текущем статусе пациента"""
        self.give_message_to_user(f"Пациент остался в статусе '{patient_status}'")

    def give_discharge_patient(self):
        """Команда: сообщает о выписке пациента"""
        self.give_message_to_user("Пациент выписан из больницы")
