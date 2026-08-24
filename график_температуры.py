import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import wmi
import time
from datetime import datetime
import threading


class CPUMonitorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Монитор температуры CPU")
        self.root.geometry("800x600")

        # Переменные для данных
        self.temperatures = []
        self.timestamps = []
        self.max_points = 60  # Показываем последние 60 значений
        self.running = True

        # Пробуем подключиться к LibreHardwareMonitor
        self.w = None
        self.sensor = None
        self.setup_wmi()

        # Создаем интерфейс
        self.setup_ui()

        # Запускаем обновление данных
        self.update_data()

    def setup_wmi(self):
        """Настройка подключения к WMI и поиск датчика CPU"""
        try:
            # Правильное имя пространства имен - с обратным слешем
            self.w = wmi.WMI(namespace="root\\LibreHardwareMonitor")

            # Ищем датчик температуры CPU
            sensors = self.w.Sensor()
            for sensor in sensors:
                if sensor.Name and "CPU" in sensor.Name and "Temperature" in str(sensor.SensorType):
                    self.sensor = sensor
                    print(f"Найден датчик: {sensor.Name} ({sensor.Identifier})")
                    break

            if not self.sensor:
                print("Датчик температуры CPU не найден. Проверьте, запущен ли LibreHardwareMonitor.")

        except Exception as e:
            print(f"Ошибка подключения к LibreHardwareMonitor: {e}")
            print("\nВозможные решения:")
            print("1. Установите и запустите LibreHardwareMonitor")
            print("2. Скачайте с https://github.com/LibreHardwareMonitor/LibreHardwareMonitor/releases")
            print("3. Запустите LibreHardwareMonitor от имени администратора")
            print("4. Убедитесь, что в настройках LibreHardwareMonitor включен WMI")

    def setup_ui(self):
        """Создание элементов интерфейса"""
        # Верхняя панель с информацией
        self.info_frame = tk.Frame(self.root)
        self.info_frame.pack(pady=10)

        self.temp_label = tk.Label(self.info_frame, text="Температура: -- °C", font=("Arial", 16))
        self.temp_label.pack(side=tk.LEFT, padx=20)

        self.status_label = tk.Label(self.info_frame, text="Статус: Ожидание...", font=("Arial", 12))
        self.status_label.pack(side=tk.LEFT, padx=20)

        # График
        self.fig, self.ax = plt.subplots(figsize=(8, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack(pady=10)

        # Настройка графика
        self.ax.set_title("Температура CPU")
        self.ax.set_xlabel("Время")
        self.ax.set_ylabel("Температура (°C)")
        self.ax.grid(True, alpha=0.3)

        # Кнопки управления
        self.btn_frame = tk.Frame(self.root)
        self.btn_frame.pack(pady=10)

        self.start_btn = tk.Button(self.btn_frame, text="Старт", command=self.start_monitoring)
        self.start_btn.pack(side=tk.LEFT, padx=5)

        self.stop_btn = tk.Button(self.btn_frame, text="Стоп", command=self.stop_monitoring)
        self.stop_btn.pack(side=tk.LEFT, padx=5)

        self.clear_btn = tk.Button(self.btn_frame, text="Очистить график", command=self.clear_graph)
        self.clear_btn.pack(side=tk.LEFT, padx=5)

    def get_temperature(self):
        """Получение текущей температуры"""
        if self.sensor:
            try:
                # Обновляем значение датчика
                sensors = self.w.Sensor(Identifier=self.sensor.Identifier)
                for s in sensors:
                    if s.Value is not None:
                        return round(s.Value, 1)
            except Exception as e:
                print(f"Ошибка получения температуры: {e}")
        return None

    def update_data(self):
        """Обновление данных каждую секунду"""
        if not self.running:
            return

        temp = self.get_temperature()

        if temp is not None:
            self.temperatures.append(temp)
            self.timestamps.append(datetime.now().strftime("%H:%M:%S"))

            # Ограничиваем количество точек
            if len(self.temperatures) > self.max_points:
                self.temperatures.pop(0)
                self.timestamps.pop(0)

            # Обновляем метку температуры
            self.temp_label.config(text=f"Температура: {temp} °C")
            self.status_label.config(text="Статус: Работает", fg="green")
        else:
            self.status_label.config(text="Статус: Нет данных", fg="red")

        # Обновляем график
        self.update_graph()

        # Запускаем следующее обновление через 1000 мс
        self.root.after(1000, self.update_data)

    def update_graph(self):
        """Обновление графика"""
        self.ax.clear()

        if self.temperatures:
            self.ax.plot(self.timestamps, self.temperatures, marker='o', linestyle='-', linewidth=2)
            self.ax.set_ylim(min(20, min(self.temperatures) - 5), max(80, max(self.temperatures) + 5))

            # Добавляем цветную заливку в зависимости от температуры
            if self.temperatures:
                last_temp = self.temperatures[-1]
                if last_temp > 80:
                    self.ax.axhline(y=80, color='red', linestyle='--', alpha=0.5, label='Критично (80°C)')
                elif last_temp > 70:
                    self.ax.axhline(y=70, color='orange', linestyle='--', alpha=0.5, label='Высокая (70°C)')

        self.ax.set_title("Температура CPU")
        self.ax.set_xlabel("Время")
        self.ax.set_ylabel("Температура (°C)")
        self.ax.grid(True, alpha=0.3)
        self.ax.legend(loc='upper right')

        # Поворачиваем подписи оси X
        plt.setp(self.ax.xaxis.get_majorticklabels(), rotation=45, ha='right')
        self.fig.tight_layout()

        self.canvas.draw()

    def start_monitoring(self):
        """Запуск мониторинга"""
        self.running = True
        self.status_label.config(text="Статус: Запущен", fg="green")
        self.update_data()

    def stop_monitoring(self):
        """Остановка мониторинга"""
        self.running = False
        self.status_label.config(text="Статус: Остановлен", fg="orange")

    def clear_graph(self):
        """Очистка графика"""
        self.temperatures.clear()
        self.timestamps.clear()
        self.update_graph()
        self.temp_label.config(text="Температура: -- °C")


def run_app():
    root = tk.Tk()
    app = CPUMonitorApp(root)
    root.mainloop()


if __name__ == "__main__":
    run_app()