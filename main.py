from Console import Console
from Hospital import Hospital
from Patient import Patient
from DialogWithUser import DialogWithUser
from Application import Application

if __name__ == "__main__":
    '''Основной объект госпиталя'''
    hospital = Hospital([Patient(patient_id) for patient_id in range(1, 201)])

    '''Обработчик инпутов пользователя'''
    dialog_with_user = DialogWithUser()

    '''Интерфейс обращения в госпиталь'''
    commands = Console(hospital, dialog_with_user)

    '''Общие приложение и соединение'''
    app = Application(commands, dialog_with_user)
    app.run()
