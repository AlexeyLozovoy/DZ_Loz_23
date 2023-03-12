import threading
import requests
import json
import time

# Событие для управления потоком №1
event = threading.Event()
  
# Функция для чтения данных из файла "get.txt"
def read_data():
    with open("get.txt", "r") as f:
        return [json.loads(line) for line in f]

# Функция для вывода данных на экран в зависимости от выбранного пункта меню
import threading
import requests
import json
import time

# Событие для управления потоком №1
event = threading.Event()

# Функция для обработки ввода пользователя
def handle_user_input():
    while True:
        print("""
        Меню:
    1.1 Текущая Температура
    1.2 Средняя Температура среднее 6 последних записей
    2.1 Электроенергия # показания счетчика, текущий расход
    2.2 Газ # показания счетчика, текущий расход
    2.3 Вода # показания счетчика, текущий расход
    3.1 Состояние # Включен/Выключен, температура, давление
    3.2 Включить # Команда на включение
    3.3 Выключить # Команда на выключение
    4. Журнал # все записи из файла
    q Выход
        """)
        # Ожидание ввода от пользователя
        user_input = input("Введите команду: ")

        # Обработка команды
        if user_input == "1.1":
            print_last_record("temperature")
        elif user_input == "1.2":
            print_average("temperature")
        elif user_input == "2.1":
            print_last_record("meter/electricity/consumption")
        elif user_input == "2.2":
            print_last_record("meter/gas/consumption")
        elif user_input == "2.3":
            print_last_record("meter/water/consumption")
        elif user_input == "3.1":
            print_boiler_status()
        elif user_input == "3.2":
            turn_boiler_on()
        elif user_input == "3.3":
            turn_boiler_off()
        elif user_input == "4":
            print_all_records()
        elif user_input == "q":
            event.set() # Остановка потока №2
            break

# Функция для вывода последней записи по указанному ключу
def print_last_record(key):
    last_record = None
    with open("get.txt", "r") as f:
        for line in f:
            data = json.loads(line)
            if key in data:
                last_record = data[key]
    if last_record:
        print(f"Последняя запись по ключу '{key}': {last_record}")
    else:
        print(f"Нет записей по ключу '{key}'")


# Функция для вывода среднего значения по указанному ключу за последние 6 записей
def print_average(key):
    values = []
    with open("get.txt", "r") as f:
        for line in f:
            data = json.loads(line)
            if key in data:
                values.append(data[key])
    if values:
        average = sum(values[-6:]) / len(values[-6:])
        print(f"Среднее значение по ключу '{key}' за последние 6 записей: {average}")
    else:
        print(f"Нет записей по ключу '{key}'")

# Функция для вывода текущего состояния котла
def print_boiler_status():
    last_boiler_data = None
    with open("get.txt", "r") as f:
        for line in f:
            data = json.loads(line)
            if "boiler" in data:
                last_boiler_data = data["boiler"]
    if last_boiler_data:
        status = "включен" if last_boiler_data["isRun"] else "выключен"
        print(f"Состояние котла: {status}, температура: {last_boiler_data['temperature']}, давление: {last_boiler_data['pressure']}")
    else:
        print("Нет данных о котле")

# Функция для включения котла
def turn_boiler_on():
    print("Включение котла")
    # Здесь можно отправить POST-запрос на сервер, чтобы включить котел

# Функция для выключения котла
def turn_boiler_off():
    print("Выключение котла")
    # Здесь можно отправить POST

# Функция для вывода всех записей из файла
def print_all_records():
    with open("get.txt", "r") as f:
        for line in f:
            print(line.strip())



# Функция для отправки запросов на сервер и записи результатов в файл
def send_requests():
    while not event.is_set():
        # Отправка GET-запроса на сервер
        response = requests.get("https://dzloz35-production-0f7d.up.railway.app/api")

        # Обработка ответа в формате JSON
        data = json.loads(response.text)
        data["timestamp"] = time.time() # Добавление времени запроса в ответ

        # Запись данных в файл
        with open("get.txt", "a") as f:
            f.write(json.dumps(data) + "\n")

        # Ожидание 5 секунд перед следующим запросом
        event.wait(5)

# Запуск двух потоков
t1 = threading.Thread(target=handle_user_input)
t2 = threading.Thread(target=send_requests)
t2.start()
t1.start()

# Ожидание завершения работы потоков
t2.join()
t1.join()
