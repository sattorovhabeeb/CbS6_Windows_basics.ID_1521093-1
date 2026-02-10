#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
MongoDB Scanner - Скрипт для поиска незащищённых баз данных MongoDB

Назначение: Сканирование сети на наличие открытых MongoDB серверов
"""

# ============================================================================
# ИМПОРТ БИБЛИОТЕК
# ============================================================================

import socket          # Для работы с сетевыми соединениями
import sys            # Для работы с системными параметрами
import ipaddress      # Для работы с IP-адресами и сетями
from pymongo import MongoClient, errors  # Для подключения к MongoDB
from datetime import datetime             # Для работы с датой и временем

# ============================================================================
# КОНСТАНТЫ
# ============================================================================

# Стандартный порт MongoDB
DEFAULT_MONGODB_PORT = 27017

# Таймаут подключения в секундах (чтобы не ждать слишком долго)
TIMEOUT = 2

# Цвета для красивого вывода в терминал (ANSI escape коды)
COLOR_GREEN = '\033[92m'   # Зелёный - успешное подключение
COLOR_RED = '\033[91m'     # Красный - ошибка
COLOR_YELLOW = '\033[93m'  # Жёлтый - предупреждение
COLOR_BLUE = '\033[94m'    # Синий - информация
COLOR_RESET = '\033[0m'    # Сброс цвета

# ============================================================================
# ФУНКЦИЯ: Проверка доступности порта
# ============================================================================

def check_port_open(ip, port):
    """
    Проверяет, открыт ли указанный порт на хосте.
    
    Параметры:
        ip (str): IP-адрес хоста для проверки
        port (int): Номер порта для проверки
    
    Возвращает:
        bool: True если порт открыт, False если закрыт
    """
    # Создаём сокет (это как "телефонная линия" для сети)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Устанавливаем таймаут, чтобы не ждать вечно
    sock.settimeout(TIMEOUT)
    
    try:
        # Пытаемся подключиться к IP:порту
        result = sock.connect_ex((ip, port))
        
        # Закрываем соединение
        sock.close()
        
        # Если result == 0, значит порт открыт
        return result == 0
    
    except socket.error:
        # Если произошла ошибка - порт недоступен
        return False

# ============================================================================
# ФУНКЦИЯ: Попытка подключения к MongoDB
# ============================================================================

def try_mongodb_connection(ip, port):
    """
    Пытается подключиться к MongoDB без аутентификации.
    
    Параметры:
        ip (str): IP-адрес MongoDB сервера
        port (int): Порт MongoDB сервера
    
    Возвращает:
        dict или None: Информация о сервере если подключение успешно, 
                       None если не удалось подключиться
    """
    try:
        # Формируем строку подключения (URI)
        # mongodb://IP:ПОРТ/ - это адрес MongoDB сервера
        connection_string = f"mongodb://{ip}:{port}/"
        
        # Создаём клиент для подключения
        # serverSelectionTimeoutMS - сколько ждать ответа (в миллисекундах)
        client = MongoClient(
            connection_string,
            serverSelectionTimeoutMS=TIMEOUT * 1000,
            directConnection=True
        )
        
        # Пытаемся получить информацию о сервере
        # Это проверка, что мы действительно подключились
        server_info = client.server_info()
        
        # Получаем список всех баз данных
        databases = client.list_database_names()
        
        # Создаём словарь с информацией о сервере
        info = {
            'ip': ip,
            'port': port,
            'version': server_info.get('version', 'Unknown'),
            'databases': databases,
            'database_count': len(databases)
        }
        
        # Закрываем соединение
        client.close()
        
        return info
    
    # Обработка различных ошибок подключения
    except errors.ServerSelectionTimeoutError:
        # Сервер не ответил вовремя
        return None
    
    except errors.ConnectionFailure:
        # Не удалось установить соединение
        return None
    
    except errors.OperationFailure as e:
        # MongoDB требует аутентификацию
        if "authentication failed" in str(e).lower() or "auth" in str(e).lower():
            return None
        return None
    
    except Exception as e:
        # Любая другая ошибка
        return None

# ============================================================================
# ФУНКЦИЯ: Красивый вывод результатов
# ============================================================================

def print_result(info):
    """
    Красиво выводит информацию о найденном MongoDB сервере.
    
    Параметры:
        info (dict): Словарь с информацией о сервере
    """
    print(f"\n{COLOR_GREEN}{'='*70}{COLOR_RESET}")
    print(f"{COLOR_GREEN}[НАЙДЕНА НЕЗАЩИЩЁННАЯ БАЗА ДАННЫХ!]{COLOR_RESET}")
    print(f"{COLOR_GREEN}{'='*70}{COLOR_RESET}")
    
    print(f"{COLOR_BLUE}IP адрес:{COLOR_RESET} {info['ip']}")
    print(f"{COLOR_BLUE}Порт:{COLOR_RESET} {info['port']}")
    print(f"{COLOR_BLUE}Версия MongoDB:{COLOR_RESET} {info['version']}")
    print(f"{COLOR_BLUE}Количество баз данных:{COLOR_RESET} {info['database_count']}")
    
    print(f"\n{COLOR_YELLOW}Список баз данных:{COLOR_RESET}")
    for db in info['databases']:
        print(f"  • {db}")
    
    print(f"{COLOR_GREEN}{'='*70}{COLOR_RESET}\n")

# ============================================================================
# ФУНКЦИЯ: Сканирование одного IP-адреса
# ============================================================================

def scan_single_ip(ip, port):
    """
    Сканирует один IP-адрес на наличие открытой MongoDB.
    
    Параметры:
        ip (str): IP-адрес для сканирования
        port (int): Порт для проверки
    """
    # Выводим информацию о текущем сканировании
    print(f"Сканирую {ip}:{port}...", end=' ')
    
    # Сначала проверяем, открыт ли порт
    if not check_port_open(ip, port):
        print(f"{COLOR_RED}[Порт закрыт]{COLOR_RESET}")
        return
    
    print(f"{COLOR_YELLOW}[Порт открыт, проверяю MongoDB...]{COLOR_RESET}")
    
    # Пытаемся подключиться к MongoDB
    info = try_mongodb_connection(ip, port)
    
    if info:
        # Если подключились - выводим информацию
        print_result(info)
    else:
        # Если не подключились - сообщаем об этом
        print(f"{COLOR_RED}[MongoDB недоступна или требует аутентификацию]{COLOR_RESET}")

# ============================================================================
# ФУНКЦИЯ: Сканирование диапазона IP-адресов
# ============================================================================

def scan_network(network, port):
    """
    Сканирует целую сеть на наличие открытых MongoDB серверов.
    
    Параметры:
        network (str): Сеть в формате CIDR (например, 192.168.1.0/24)
        port (int): Порт для проверки
    """
    try:
        # Преобразуем строку сети в объект сети
        net = ipaddress.ip_network(network, strict=False)
        
        print(f"{COLOR_BLUE}Начинаю сканирование сети: {network}{COLOR_RESET}")
        print(f"{COLOR_BLUE}Количество хостов для проверки: {net.num_addresses}{COLOR_RESET}")
        print(f"{COLOR_BLUE}Порт: {port}{COLOR_RESET}")
        print(f"{COLOR_BLUE}Время начала: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{COLOR_RESET}\n")
        
        # Счётчик найденных серверов
        found_count = 0
        
        # Перебираем все IP-адреса в сети
        for ip in net.hosts():
            ip_str = str(ip)
            
            # Проверяем порт
            if check_port_open(ip_str, port):
                print(f"\n{COLOR_YELLOW}[{ip_str}] Порт {port} открыт! Проверяю MongoDB...{COLOR_RESET}")
                
                # Пытаемся подключиться к MongoDB
                info = try_mongodb_connection(ip_str, port)
                
                if info:
                    found_count += 1
                    print_result(info)
        
        # Выводим итоги сканирования
        print(f"\n{COLOR_BLUE}{'='*70}{COLOR_RESET}")
        print(f"{COLOR_BLUE}Сканирование завершено!{COLOR_RESET}")
        print(f"{COLOR_BLUE}Найдено незащищённых серверов: {found_count}{COLOR_RESET}")
        print(f"{COLOR_BLUE}Время окончания: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{COLOR_RESET}")
        print(f"{COLOR_BLUE}{'='*70}{COLOR_RESET}\n")
    
    except ValueError as e:
        print(f"{COLOR_RED}Ошибка: Неверный формат сети. Используйте формат CIDR (например, 192.168.1.0/24){COLOR_RESET}")
        sys.exit(1)

# ============================================================================
# ФУНКЦИЯ: Вывод справки
# ============================================================================

def print_help():
    """
    Выводит справку по использованию скрипта.
    """
    help_text = f"""
{COLOR_BLUE}{'='*70}
MongoDB Scanner - Инструмент для поиска незащищённых баз данных
{'='*70}{COLOR_RESET}

{COLOR_YELLOW}ИСПОЛЬЗОВАНИЕ:{COLOR_RESET}
    python3 scan.py <IP или СЕТЬ> [ПОРТ]

{COLOR_YELLOW}ПАРАМЕТРЫ:{COLOR_RESET}
    <IP или СЕТЬ>  - Один IP-адрес (например, 192.168.1.10)
                     или сеть в формате CIDR (например, 192.168.1.0/24)
    [ПОРТ]         - Порт MongoDB (по умолчанию: 27017)

{COLOR_YELLOW}ПРИМЕРЫ:{COLOR_RESET}
    # Сканировать один IP на стандартном порту:
    python3 scan.py 192.168.1.10

    # Сканировать один IP на нестандартном порту:
    python3 scan.py 192.168.1.10 27018

    # Сканировать всю подсеть:
    python3 scan.py 192.168.1.0/24

    # Сканировать подсеть на нестандартном порту:
    python3 scan.py 192.168.1.0/24 27018

{COLOR_YELLOW}ПРИМЕЧАНИЯ:{COLOR_RESET}
    • Скрипт ищет только НЕЗАЩИЩЁННЫЕ базы данных (без пароля)
    • Для больших сетей сканирование может занять много времени
    • Убедитесь, что у вас есть разрешение на сканирование сети

{COLOR_RED}ВНИМАНИЕ:{COLOR_RESET}
    Используйте этот инструмент только в учебных целях
    или на системах, которыми вы владеете!

{COLOR_BLUE}{'='*70}{COLOR_RESET}
    """
    print(help_text)

# ============================================================================
# ГЛАВНАЯ ФУНКЦИЯ
# ============================================================================

def main():
    """
    Главная функция программы - точка входа.
    """
    # Проверяем количество аргументов командной строки
    # sys.argv[0] - это имя скрипта
    # sys.argv[1] - первый аргумент (IP или сеть)
    # sys.argv[2] - второй аргумент (порт, необязательный)
    
    if len(sys.argv) < 2:
        # Если аргументов недостаточно - показываем справку
        print_help()
        sys.exit(1)
    
    # Получаем IP-адрес или сеть из первого аргумента
    target = sys.argv[1]
    
    # Получаем порт (если указан) или используем стандартный
    if len(sys.argv) >= 3:
        try:
            port = int(sys.argv[2])
        except ValueError:
            print(f"{COLOR_RED}Ошибка: Порт должен быть числом!{COLOR_RESET}")
            sys.exit(1)
    else:
        port = DEFAULT_MONGODB_PORT
    
    # Выводим заголовок программы
    print(f"\n{COLOR_BLUE}{'='*70}")
    print("MongoDB Scanner v1.0")
    print(f"{'='*70}{COLOR_RESET}\n")
    
    # Определяем, что сканировать: один IP или сеть
    if '/' in target:
        # Если есть '/' - это сеть в формате CIDR
        scan_network(target, port)
    else:
        # Иначе - это один IP-адрес
        scan_single_ip(target, port)

# ============================================================================
# ТОЧКА ВХОДА В ПРОГРАММУ
# ============================================================================

# Эта проверка нужна, чтобы код выполнялся только при прямом запуске скрипта
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        # Обработка прерывания (Ctrl+C)
        print(f"\n\n{COLOR_YELLOW}Сканирование прервано пользователем.{COLOR_RESET}")
        sys.exit(0)
    except Exception as e:
        # Обработка любых других ошибок
        print(f"\n{COLOR_RED}Произошла ошибка: {str(e)}{COLOR_RESET}")
        sys.exit(1)