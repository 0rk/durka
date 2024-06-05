class CommandError(Exception):
    """Исключение для неизвестных команд"""
    pass


class PatientNotExistsError(Exception):
    """Исключение для отсутствия пациента"""


class PatientIdNotIntAndPositiveError(Exception):
    """Исключение для корректности id пациента"""
    def __init__(self, message="Ошибка. ID пациента должно быть числом (целым, положительным)"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message


class MinimalStatusCantDownError(Exception):
    """Исключение для корректности id пациента"""
    pass


