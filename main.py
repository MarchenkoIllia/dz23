import threading, time, json, requests, sys


json_response = ''
lock_json_response = threading.Lock()
event_json_response = threading.Event()

def request():
    global json_response
    if event_json_response.is_set():
        return
    response = requests.get('http://localhost:8000/cgi-bin/rest.py')
    lock_json_response.acquire()
    json_response = json.loads(response.text)
    time.sleep(5)
    lock_json_response.release()

def menu():
    while True:
        choise = input('''Меню:
1. Температура/Влажность
    1.1 Текущая # последняя запись в файле
    1.2 Средняя # среднее 6 последних записей
2. Счетчики
    2.1 Электроенергия # показания счетчика, текущий расход
    2.2 Газ # показания счетчика, текущий расход
    2.3 Вода # показания счетчика, текущий расход
3. Котел
    3.1 Состояние # Включен/Выключен, температура, давление
    3.2 Включить # Команда на включение
    3.3 Выключить # Команда на выключение
4. Журнал # все записи из файла
5. Завершение работы программы
''')
        if choise == '1.1':
            temperature = json_response['temperature']
            humidity = json_response['humidity']
            lock_json_response.acquire()
            with open('result.txt', 'a', encoding='utf-8') as f:
                f.write(f'{time.asctime()} Температура - {temperature}, Давление - {humidity}')
            lock_json_response.release()
            print(f'Температура - {temperature}, Давление - {humidity}')
        elif choise == '2.1':
            el_reading = json_response['meter']['electricity']['reading']
            el_consumption = json_response['meter']['electricity']['consumption']
            with open('result.txt', 'a', encoding='utf-8') as f:
                f.write(f'{time.asctime()} ЭЛЕКТРОЕНЕРГИЯ - Показание счётчика - {el_reading}, Текущий расход - {el_consumption}')
            lock_json_response.release()
            print(f'ЭЛЕКТРОЕНЕРГИЯ - Показание счётчика - {el_reading}, Текущий расход - {el_consumption}')
        elif choise == '2.2':
            gas_reading = json_response['meter']['gas']['reading']
            gas_consumption = json_response['meter']['gas']['consumption']
                