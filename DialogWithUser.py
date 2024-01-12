class DialogWithUser:
    @staticmethod
    def get_patient_id(hospital):
        try:
            patient_id = input("Введите ID пациента: ")
            if DialogWithUser.is_positive_integer(patient_id):
                if int(patient_id) <= len(hospital.patients):
                    return int(patient_id)
                else:
                    raise ValueError

            raise TypeError
        except ValueError:
            print("Ошибка. В больнице нет пациента с таким ID")
        except TypeError:
            print("Ошибка. ID пациента должно быть числом (целым, положительным)")

    @staticmethod
    def is_positive_integer(value):
        try:
            return int(value) > 0
        except ValueError:
            return False
