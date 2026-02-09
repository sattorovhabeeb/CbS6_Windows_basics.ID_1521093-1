#!/usr/bin/env python3
"""
TCP Message Sender Script using Scapy
Отправляет сообщение на localhost:12345 по протоколу TCP
Версия для новичков с подробными комментариями
"""

from scapy.all import *
import time
import sys

def check_privileges():
    """Проверяем, запущен ли скрипт с правами root"""
    if os.geteuid() != 0:
        print("❌ ОШИБКА: Скрипт должен быть запущен с правами root!")
        print("Используйте: sudo python3 tcp_sender.py")
        sys.exit(1)

def send_tcp_message():
    """Основная функция отправки TCP сообщения"""
    
    # Параметры соединения
    target_ip = "127.0.0.1"  # localhost (наш же компьютер)
    target_port = 12345      # Порт назначения
    source_port = 54321      # Наш порт (можно любой свободный)
    
    # Сообщение про хомяка Pinkie
    message = "Dear Steel Cat! This is no attack, it's my humster Pinkie you should track"
    
    print(f"🎯 Цель: {target_ip}:{target_port}")
    print(f"📝 Сообщение: {message}")
    print(f"📦 Размер сообщения: {len(message)} байт")
    print("-" * 60)
    
    # Создаем ОДИН пакет с данными
    # IP заголовок + TCP заголовок + наше сообщение
    data_packet = IP(dst=target_ip, src="127.0.0.1") / TCP(
        dport=target_port,
        sport=source_port,
        flags="PA",    # Push + ACK (передача данных)
        seq=1000,      # Sequence number
        ack=1,         # Acknowledgment number
        window=8192
    ) / Raw(load=message.encode('utf-8'))  # Наше сообщение в байтах
    
    print("📡 Отправляем TCP пакет с сообщением...")
    
    try:
        # Отправляем пакет (verbose=1 покажет детали)
        send(data_packet, verbose=1)  # Убираем iface для L3 пакетов
        
        print("✅ Пакет успешно отправлен!")
        print(f"📋 Проверьте Wireshark на интерфейсе Loopback")
        print(f"🔍 Используйте фильтр: tcp.port == {target_port}")
        
    except PermissionError:
        print("❌ Нет прав для отправки пакетов!")
        print("Запустите с sudo: sudo python3 tcp_sender.py")
    except Exception as e:
        print(f"❌ Ошибка при отправке: {e}")

def main():
    """Главная функция"""
    print("🐹 TCP Message Sender для хомяка Pinkie")
    print("=" * 50)
    
    # Проверяем права
    check_privileges()
    
    # Проверяем, установлен ли scapy
    try:
        import scapy
        print(f"✅ Scapy версия {scapy.__version__} найден")
    except ImportError:
        print("❌ Scapy не установлен!")
        print("Установите: sudo apt install python3-scapy")
        sys.exit(1)
    
    # Даем время подготовиться
    print("\n🚀 Начинаем отправку через 3 секунды...")
    print("Убедитесь, что Wireshark уже запущен и слушает Loopback!")
    
    for i in range(3, 0, -1):
        print(f"⏰ {i}...")
        time.sleep(1)
    
    # Отправляем сообщение
    send_tcp_message()

if __name__ == "__main__":
    main()