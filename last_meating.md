1) Application разгрузить от условий и добавить тесты
2) patient_status_invalid_id изменить тестовые данные
3) test_get_patient_all_status 2 пациентов а не 5
4) Добавить метод eq для patient и переписать тест test_increase_patient_status_valid_id
5) Добавить исключение для попытки повышения максимального статуса 
6) get_patient конкретизировать проверки на None
7) Commands.increase_patient_status объединить разбитые методы в один для большой читаемости
8) В тестах Hospital добавить тест на получение статистики
9) Изменить нейминг метода DialogWithUser.give_proposal_discharge_patient
10) Райзить ошибки понижения/повышения статуса в пациенте
11) Переписать остановку Application без исключения 
12) Убрать в Application exception CommandError, тем самым убрать try except из данного класса
13) Для Application попытаться сделать метод который кидает команду, а в run выполнять
14) Переписать Application и переписать тесты если возможно
