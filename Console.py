from Hospital import Hospital


class Console:
    @staticmethod
    def run():
        hospital = Hospital()

        while True:
            command = input("Введите команду: ").lower()

            if command in ["стоп", "stop"]:
                Console.print_exit_message()
                break
            elif command in ["узнать статус пациента", "get status"]:
                Console.get_patient_status(hospital)
            elif command in ["повысить статус пациента", "status up"]:
                Console.increase_patient_status(hospital)
            elif command in ["понизить статус пациента", "status down"]:
                Console.decrease_patient_status(hospital)
            elif command in ["выписать пациента", "discharge"]:
                Console.discharge_patient(hospital)
            elif command in ["рассчитать статистику", "calculate statistics"]:
                Console.print_statistics(hospital)
            else:
                Console.print_unknown_command()

    @staticmethod
    def get_patient_status(hospital):
        Console._perform_patient_action(hospital, hospital.get_patient_status)

    @staticmethod
    def increase_patient_status(hospital):
        Console._perform_patient_action(hospital, hospital.increase_patient_status)

    @staticmethod
    def decrease_patient_status(hospital):
        Console._perform_patient_action(hospital, hospital.decrease_patient_status)

    @staticmethod
    def discharge_patient(hospital):
        Console._perform_patient_action(hospital, hospital.discharge_patient)

    @staticmethod
    def _perform_patient_action(hospital, action_function):
        patient_id = Console.get_patient_id(hospital)
        if patient_id is not None:
            print(action_function(patient_id))

    @staticmethod
    def print_statistics(hospital):
        hospital.calculate_statistics()

    @staticmethod
    def print_exit_message():
        print("Сеанс завершён.")

    @staticmethod
    def print_unknown_command():
        print("Неизвестная команда! Попробуйте ещё раз")

    @staticmethod
    def print_error_is_positive_integer():
        print("Ошибка. ID пациента должно быть числом (целым, положительным)")

    @staticmethod
    def print_error_no_such_id():
        print("Ошибка. В больнице нет пациента с таким ID")

    @staticmethod
    def is_positive_integer(value):
        try:
            return int(value) > 0
        except ValueError:
            return False

    @staticmethod
    def get_patient_id(hospital):
        patient_id = input("Введите ID пациента: ")
        if Console.is_positive_integer(patient_id):
            if int(patient_id) <= len(hospital.patients):
                return int(patient_id)
            else:
                Console.print_error_no_such_id()
                return None

        Console.print_error_is_positive_integer()
        return None


if __name__ == "__main__":
    Console.run()
