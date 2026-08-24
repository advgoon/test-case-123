import obd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque
import time

# 1. Подключение к адаптеру (ELM327)
connection = obd.OBD()  # авто-поиск порта
if not connection.is_connected():
    print("Ошибка подключения к адаптеру!")
    exit()

# 2. Проверка поддержки скорости Fabia (EOBD совместима)
cmd = obd.commands.SPEED
if cmd not in connection.supported_commands:
    print("Команда SPEED не поддерживается авто!")
    # Можно попробовать RPM как запасной вариант
    cmd = obd.commands.RPM

# 3. Настройка графика
max_points = 50  # отображаем последние 50 точек
times = deque(maxlen=max_points)
speeds = deque(maxlen=max_points)

fig, ax = plt.subplots()
line, = ax.plot([], [])
ax.set_title('Skoda Fabia - Speed (km/h)')
ax.set_xlabel('Time (s)')
ax.set_ylabel('Speed (km/h)')
ax.grid(True)


# 4. Функция обновления графика
def update(frame):
    response = connection.query(cmd)
    if not response.is_null():
        speed = response.value.magnitude  # число в км/ч
        speeds.append(speed)
        times.append(time.time())

        # Показываем только последние max_points точек
        start_time = times[0] if times else time.time()
        x = [t - start_time for t in times]

        line.set_data(x, list(speeds))
        ax.relim()
        ax.autoscale_view()
    return line,


# 5. Анимация (обновление каждую секунду)
ani = animation.FuncAnimation(fig, update, interval=1000, cache_frame_data=False)
plt.show()