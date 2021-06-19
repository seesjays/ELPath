from dearpygui.core import *
from dearpygui.simple import *
from math import cos, sin

def plot_callback(sender, data):

    data1x = []
    data1y = []
    for i in range(0, 100):
        data1x.append(3.14 * i / 180)
        data1y.append(cos(3 * 3.14 * i / 180))

    data2x = []
    data2y = []
    for i in range(0, 100):
        data2x.append(3.14 * i / 180)
        data2y.append(sin(2 * 3.14 * i / 180))

    print(data1x[0:50])
    print(data1y[0:50])
    add_bar_series("Plot", "Cos", [i for i in range(0, 100)], [i for i in range(1, 101)], weight=0.5)
    add_shade_series("Plot", "Cos", data1x, data1y, weight=2, fill=[255, 0, 0, 100])
    add_scatter_series("Plot", "Sin", data2x, data2y, outline=[0, 255, 0, 100])

with window("Tutorial"):
    add_button("Plot data", callback=plot_callback)
    add_plot("Plot", height=-1)

start_dearpygui()