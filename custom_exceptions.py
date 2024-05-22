class CommandError(Exception):
    """Исключение для неизвестных команд"""
    pass


class PatientNotExistsError(Exception):
    """Исключение для отсутствия пациента"""
    pass


class PatientIdNotIntAndPositiveError(Exception):
    """Исключение для корректности id пациента"""
    pass


class MinimalStatusCantDownError(Exception):
    """Исключение для корректности id пациента"""
    pass


