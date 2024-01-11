import re


class Application:
    def __init__(self, commands):
        self.commands = commands

    def run(self):
        while True:
            command = input("Введите команду: ").lower()

            if (command in ["stop"] or
                    self.typo_checking(command, "стоп")):
                self.commands.print_exit_message()
                break
            elif (command in ["get status"] or
                  self.typo_checking(command, "узнать статус пациента")):
                self.commands.get_patient_status()
            elif (command in ["status up"] or
                  self.typo_checking(command, "повысить статус пациента")):
                self.commands.increase_patient_status()
            elif (command in ["status down"]
                  or self.typo_checking(command, "понизить статус пациента")):
                self.commands.decrease_patient_status()
            elif (command in ["discharge"] or
                  self.typo_checking(command, "выписать пациента")):
                self.commands.discharge_patient()
            elif (command in ["calculate statistics"] or
                  self.typo_checking(command, "рассчитать статистику")):
                self.commands.print_statistics()
            else:
                raise ValueError("Неизвестная команда! Попробуйте ещё раз")


    @staticmethod
    def typo_checking(command, reference):
        # Заменяем в строке символы [ао] на [ао] и символы [ие] на [ие]
        modified_command = re.sub(r'[ао]', '[ао]', reference, flags=re.IGNORECASE | re.UNICODE)
        modified_command = re.sub(r'[ие]', '[ие]', modified_command, flags=re.IGNORECASE | re.UNICODE)

        # Создаем паттерн из модифицированной строки с добавлением границ слов
        pattern = re.compile(r'\b' + modified_command + r'\b', re.IGNORECASE | re.UNICODE)
        match = re.search(pattern, command)
        return match
