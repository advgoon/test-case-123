import pyautogui
import time

print("=" * 50)
print("Автоматическое нажатие клавиши A с повторением")
print("=" * 50)
print("Клавиша: A")
print("Длительность нажатия: 5 секунд")
print("Пауза: 30 секунд")
print("Нажмите Ctrl+C для остановки")
print("=" * 50)

try:
    cycle_count = 0

    while True:
        cycle_count += 1
        print(f"\n[Цикл {cycle_count}] Начинаю нажатие клавиши A...")

        # Нажимаем A в течение 5 секунд
        start_time = time.time()
        press_count = 0

        while time.time() - start_time < 5:
            pyautogui.press('a')
            press_count += 1
            time.sleep(0.01)  # 10мс между нажатиями

        print(f"[Цикл {cycle_count}] Выполнено {press_count} нажатий")

        # Ждем 30 секунд перед следующим циклом
        print(f"Ждем 30 секунд до следующего цикла... (нажмите Ctrl+C для остановки)")

        # Обратный отсчет для наглядности
        for i in range(30, 0, -1):
            print(f"\rОсталось: {i} секунд", end="", flush=True)
            time.sleep(1)
        print()  # Переход на новую строку

except KeyboardInterrupt:
    print("\n\nПрограмма остановлена пользователем")
    print(f"Всего выполнено циклов: {cycle_count}")
except Exception as e:
    print(f"\nОшибка: {e}")

input("\nНажмите Enter для выхода...")aaaaaaaaaaaaaaa