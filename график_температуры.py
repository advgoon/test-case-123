import matplotlib
matplotlib.use('TkAgg')  # Для Tkinter

import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import wmi
import time

class CPUMonitorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Температура процессора (LibreHardwareMonitor + WMI)")

        self.x_data = []
        self.y_data = []

        self.fig, self.ax = plt.subplots(figsize=(9, 4))
        self.comp_graph, = self.ax.plot(self.x_data, self.y_data, label='CPU Temp (°C)')

        self.ax.set_title('Температура процессора')
        self.ax.set_xlabel('Время, с')
        self.ax.set_ylabel('Температура, °C')
        self.ax.grid(True)
        self.ax.legend()

        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self.running = True
        self.seconds = 0

        self.w = wmi.WMI(namespace="rootLibreHardwareMonitor")

        self.update_graph()

    def get_cpu_temp(self):
        temperature_infos = self.w.Sensor()
        for sensor in temperature_infos:
            if sensor.SensorType == u'Temperature' and 'cpu' in sensor.Name.lower():
                return float(sensor.Value)
        return None

    def update_graph(self):
        if not self.running:
            return
        temp = self.get_cpu_temp()
        if temp is None:
            temp = 0

        self.x_data.append(self.seconds)
        self.y_data.append(temp)
        if len(self.x_data) > 100:
            self.x_data = self.x_data[-100:]
            self.y_data = self.y_data[-100:]

        self.comp_graph.set_data(self.x_data, self.y_data)
        self.ax.set_xlim(max(0, self.seconds - 90), self.seconds + 10)
        self.ax.set_ylim(min(self.y_data) - 2, max(self.y_data) + 2)

        self.canvas.draw()
        self.seconds += 1

        self.root.after(1000, self.update_graph)

def run_app():
    root = tk.Tk()
    app = CPUMonitorApp(root)
    root.protocol("WM_DELETE_WINDOW", lambda: (setattr(app, 'running', False), root.destroy()))
    root.mainloop()

if __name__ == '__main__':
    run_app()