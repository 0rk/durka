import re
from custom_exceptions import CommandError


class Application:
    def __init__(self, commands, dialog_with_user):
        self._commands = commands
        self._dialog_with_user = dialog_with_user

    def run(self):
        while True:
            command = self._dialog_with_user.get_command()
            try:
                if any(re.search(command, keyword)
                       for keyword in ["stop", "стоп"]):
                    self._dialog_with_user.exit_message()
                    break
                elif any(re.search(command, keyword)
                         for keyword in ["get status", "узнать статус пациента"]):
                    self._commands.get_patient_status()
                elif any(re.search(command, keyword)
                         for keyword in ["status up", "повысить статус пациента"]):
                    self._commands.increase_patient_status()
                elif any(re.search(command, keyword)
                         for keyword in ["status down", "понизить статус пациента"]):
                    self._commands.decrease_patient_status()
                elif any(re.search(command, keyword)
                         for keyword in ["discharge", "выписать пациента"]):
                    self._commands.discharge_patient()
                elif any(re.search(command, keyword)
                         for keyword in ["calculate statistics", "рассчитать статистику"]):
                    self._commands.show_statistics()
                else:
                    raise CommandError("Неизвестная команда! Попробуйте ещё раз")
            except CommandError as exception:
                self._dialog_with_user.return_message_to_user(exception)
