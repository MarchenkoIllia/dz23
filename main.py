import threading, time, json, requests, sys


json_response = ''
lock_json_response = threading.Lock()
event_exit = threading.Event()

def request():
    global json_response
    while True:
        if event_exit.is_set():
            return
        response = requests.get('http://localhost:8000/cgi-bin/rest.py')
        lock_json_response.acquire()
        json_response = json.loads(response.text)
        lock_json_response.release()
        time.sleep(5)

def menu():
    while True:
        choise = input('''\nМеню:
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
                f.write(f'\n{time.asctime()} Температура - {temperature}, Давление - {humidity}')
            lock_json_response.release()
            print(f'Температура - {temperature}, Давление - {humidity}')
        elif choise == '2.1':
            el_reading = json_response['meter']['electricity']['reading']
            el_consumption = json_response['meter']['electricity']['consumption']
            lock_json_response.acquire()
            with open('result.txt', 'a', encoding='utf-8') as f:
                f.write(f'\n{time.asctime()} ЭЛЕКТРОЕНЕРГИЯ - Показание счётчика - {el_reading}, Текущий расход - {el_consumption}')
            lock_json_response.release()
            print(f'ЭЛЕКТРОЕНЕРГИЯ - Показание счётчика - {el_reading}, Текущий расход - {el_consumption}')
        elif choise == '2.2':
            gas_reading = json_response['meter']['gas']['reading']
            gas_consumption = json_response['meter']['gas']['consumption']
            lock_json_response.acquire()
            with open('result.txt', 'a', encoding='utf-8') as f:
                f.write(f'\n{time.asctime()} ГАЗ - Показание счётчика - {gas_reading}, Текущий расход - {gas_consumption}')
            lock_json_response.release()
            print(f'ГАЗ - Показание счётчика - {gas_reading}, Текущий расход - {gas_consumption}')
        elif choise == '2.3':
            water_reading = json_response['meter']['water']['reading']
            water_consumption = json_response['meter']['water']['consumption']
            lock_json_response.acquire()
            with open('result.txt', 'a', encoding='utf-8') as f:
                f.write(f'\n{time.asctime()} ВОДА - Показание счётчика - {water_reading}, Текущий расход - {water_consumption}')
            lock_json_response.release()
            print(f'ВОДА - Показание счётчика - {water_reading}, Текущий расход - {water_consumption}')
        elif choise == '3.1':
            boiler_status = json_response['boiler']['isRun']
            boiler_temperature = json_response['boiler']['temperature']
            boiler_pressure = json_response['boiler']['pressure']
            
            if boiler_status == True:    #проверка бойлера на включённость
                boiler_status_str = 'Бойлер включён'
            else:
                boiler_status_str = 'Бойлер выключен'
            
            lock_json_response.acquire()
            with open('result.txt', 'a', encoding='utf-8') as f:
                f.write(f'\n{time.asctime()} {boiler_status_str}, Температура - {boiler_temperature}, Давление - {boiler_pressure}')
            lock_json_response.release()
            print(f'{boiler_status_str}, Температура - {boiler_temperature}, Давление - {boiler_pressure}')

        elif choise == '3.2':
            boiler_status = True
            lock_json_response.acquire()
            with open('result.txt', 'a', encoding='utf-8') as f:
                f.write(f'\n{time.asctime()} Бойлер включён')
            lock_json_response.release()

        elif choise == '3.3':
            boiler_status = False
            lock_json_response.acquire()
            with open('result.txt', 'a', encoding='utf-8') as f:
                f.write(f'\n{time.asctime()} Бойлер выключён')
            lock_json_response.release()
        
        elif choise == "5":
            sys.exit()
        event_exit.set()

th1 = threading.Thread(target=menu)
th2 = threading.Thread(target=request, daemon=True)

th1.start()
th2.start()

th1.join()
th2.join()