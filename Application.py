import re


class CommandError(Exception):
    pass


class Application:
    def __init__(self, commands):
        self.commands = commands

    def run(self):
        while True:
            command = self.commands.dialog_with_user.get_command()
            try:
                if any(re.search(command, keyword)
                       for keyword in ["stop", "стоп"]):
                    self.commands.dialog_with_user.exit_message()
                    break
                elif any(re.search(command, keyword)
                         for keyword in ["get status", "узнать статус пациента"]):
                    self.commands.get_patient_status()
                elif any(re.search(command, keyword)
                         for keyword in ["status up", "повысить статус пациента"]):
                    self.commands.increase_patient_status()
                elif any(re.search(command, keyword)
                         for keyword in ["status down", "понизить статус пациента"]):
                    self.commands.decrease_patient_status()
                elif any(re.search(command, keyword)
                         for keyword in ["discharge", "выписать пациента"]):
                    self.commands.discharge_patient()
                elif any(re.search(command, keyword)
                         for keyword in ["calculate statistics", "рассчитать статистику"]):
                    self.commands.return_statistics()
                else:
                    raise CommandError("Неизвестная команда! Попробуйте ещё раз")
            except Exception as exception:
                self.commands.dialog_with_user.return_message_to_user(exception)
