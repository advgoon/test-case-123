import tkinter as tk
import psutil
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

class CPULoadPlotter:
    def __init__(self, master):
        self.master = master
        self.master.title("CPU Load")
        self.master.attributes('-topmost', True)  # Окно всегда поверх!
        # опционально: убрать с панели задач
        # self.master.overrideredirect(1)

        self.x_data = list(range(60))
        self.y_data = [0]*60

        self.figure, self.ax = plt.subplots(figsize=(8,3))
        self.line, = self.ax.plot(self.x_data, self.y_data, label='CPU %')
        self.ax.set_ylim(0, 100)
        self.ax.set_xlim(0, 59)
        self.ax.set_xlabel("Время (сек)")
        self.ax.set_ylabel("Загрузка CPU (%)")
        self.ax.set_title("График загрузки процессора")
        self.ax.grid(True)
        self.ax.legend()

        self.canvas = FigureCanvasTkAgg(self.figure, master=self.master)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=1)

        self.update_plot()

    def update_plot(self):
        # Получить загрузку за последнее мгновение
        cpu = psutil.cpu_percent(interval=None)
        self.y_data.append(cpu)
        self.y_data.pop(0)

        self.line.set_ydata(self.y_data)
        self.canvas.draw()
        # Запланировать обновление через 1 секунду
        self.master.after(1000, self.update_plot)

def main():
    root = tk.Tk()
    app = CPULoadPlotter(root)
    root.mainloop()

if __name__ == '__main__':
    main()


    print("1 ")