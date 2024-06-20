import re


class Application:
    def __init__(self, commands, dialog_with_user):
        self._running = True
        self._commands = commands
        self._dialog_with_user = dialog_with_user
        self._command_map = {
            "stop": self._stop,
            "стоп": self._stop,
            "get status": self._commands.get_patient_status,
            "узнать статус пациента": self._commands.get_patient_status,
            "status up": self._commands.increase_patient_status,
            "повысить статус пациента": self._commands.increase_patient_status,
            "status down": self._commands.decrease_patient_status,
            "понизить статус пациента": self._commands.decrease_patient_status,
            "discharge": self._commands.discharge_patient,
            "выписать пациента": self._commands.discharge_patient,
            "calculate statistics": self._commands.show_statistics,
            "рассчитать статистику": self._commands.show_statistics,
        }

    def _stop(self):
        self._dialog_with_user.give_exit_message()
        self._running = False

    def run(self):
        while self._running:
            command = self._dialog_with_user.get_command()
            action = self.find_action_by_command(command)
            if action is None:
                self._dialog_with_user.give_message_to_user("Неизвестная команда! Попробуйте ещё раз")
            else:
                action()

    def find_action_by_command(self, command):
        for keyword, action in self._command_map.items():
            if re.fullmatch(command, keyword):
                return action
        return None
