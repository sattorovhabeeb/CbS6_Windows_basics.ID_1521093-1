# Подключаем библиотеки
from pynput import keyboard
import statistics
import time

# Переменные для хранения данных
key_times = []
stop_listening = False


# Функция: что делать когда нажата клавиша
def on_press(key):
    global stop_listening
    
    # Записываем время нажатия
    current_time = time.time()
    key_times.append(current_time)
    
    # Если нажали Enter - останавливаемся
    try:
        if key == keyboard.Key.enter:
            stop_listening = True
            return False
    except AttributeError:
        pass


# Функция: собираем времена нажатий
def collect_timings():
    global key_times, stop_listening
    
    # Очищаем старые данные
    key_times = []
    stop_listening = False
    
    print("Печатай текст. В конце нажми Enter.")
    
    # Запускаем прослушивание клавиатуры
    listener = keyboard.Listener(on_press=on_press)
    listener.start()
    
    # Ждем пока не нажмут Enter
    while not stop_listening:
        time.sleep(0.1)
    
    listener.stop()
    
    # Считаем промежутки между нажатиями
    intervals = []
    for i in range(1, len(key_times)):
        interval = key_times[i] - key_times[i-1]
        intervals.append(interval)
    
    return intervals


# Функция: сравниваем два набора времен
def compare(times1, times2):
    if len(times1) < 2 or len(times2) < 2:
        print("Мало данных!")
        return
    
    # Считаем средние значения
    avg1 = statistics.mean(times1)
    avg2 = statistics.mean(times2)
    
    # Считаем разницу
    difference = abs(avg1 - avg2)
    
    # Показываем результаты
    print("\n" + "="*40)
    print(f"Среднее время 1: {avg1:.4f} сек")
    print(f"Среднее время 2: {avg2:.4f} сек")
    print(f"Разница: {difference:.4f} сек")
    print("="*40)
    
    # Выводим вердикт
    if difference > 0.1:
        print("\nОбнаружены отклонения в поведении.")
        print("Возможно, вводил другой человек.")
    else:
        print("\nВвод соответствует исходному пользователю.")


# ГЛАВНАЯ ПРОГРАММА
print("="*40)
print("АНАЛИЗ КЛАВИАТУРЫ")
print("="*40)

phrase = input("\nКакую фразу будешь печатать? ")

print("\n--- ПЕРВЫЙ РАЗ ---")
print(f"Напечатай: {phrase}")
first = collect_timings()

print("\nПодожди 2 секунды...")
time.sleep(2)

print("\n--- ВТОРОЙ РАЗ ---")
print(f"Напечатай снова: {phrase}")
second = collect_timings()

compare(first, second)