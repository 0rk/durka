class CommandError(Exception):
    """Исключение для неизвестных команд"""
    def __init__(self, message="Неизвестная команда! Попробуйте ещё раз"):
        self.message = message
        super().__init__(self.message)


class PatientNotExistsError(Exception):
    """Исключение для отсутствия пациента"""
    def __init__(self, message="Ошибка. В больнице нет пациента с таким ID"):
        self.message = message
        super().__init__(self.message)


class PatientIdNotIntAndPositiveError(Exception):
    """Исключение для корректности id пациента"""
    def __init__(self, message="Ошибка. ID пациента должно быть числом (целым, положительным)"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message


class MinimalStatusCantDownError(Exception):
    """Исключение для попытки понизить минимальный статус"""
    def __init__(self, message="Ошибка. Нельзя понизить самый низкий статус (наши пациенты не умирают)."):
        self.message = message
        super().__init__(self.message)


class MaximumStatusCantUpError(Exception):
    """Исключение для попытки повысить максимальный статус"""
    def __init__(self, message="Ошибка. Нельзя повысить самый высокий статус (наши пациенты не боги)."):
        self.message = message
        super().__init__(self.message)
