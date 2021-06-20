from dearpygui.core import *
from dearpygui.simple import *
import initialwindows
from random import randint
from time import sleep

# For maximum compat (and because I don't see any real reason not to,) the window is designed to fit in smaller screens (laptops, etc)
WINDOW_WIDTH, WINDOW_HEIGHT = 1200, 900
FILL_WIDTH = WINDOW_WIDTH-15

CHILD_WINDOW_FILL_PARAMS = {
    "width": FILL_WIDTH, 
    "no_resize": True, 
    "no_collapse": True, 
    "no_close": True, 
    "no_move": True
}

UNINTERACTIVE_GRAPH_PARAMS= {
    "xaxis_no_tick_labels": True, 
    "xaxis_no_gridlines": True, 
    "x_axis_name": "", 
    "xaxis_no_tick_marks": True,
    "yaxis_no_tick_labels": True, 
    "yaxis_no_gridlines": True, 
    "y_axis_name": "", 
    "yaxis_no_tick_marks": True,
    "no_box_select": True,
    "xaxis_lock_min": True,
    "xaxis_lock_max": True,
    "yaxis_lock_min": True,
    "yaxis_lock_max": True,
    "no_legend": True,
    "no_mouse_pos": True,
}

initialwindows.intializeElPath()

# Bar plots are initialized at 0 now.

VAL_CNT = 20
xVals = [i for i in range(VAL_CNT)]
yVals = [randint(1, VAL_CNT) for i in range(VAL_CNT)]

def setLimits(dataset):
    # Because we initialize our plots starting at 0 now, we just need to see everything from -1 (to include the 0 position) to
    # the end of the dataset's length. The Y limit is gonna be a bit more than the highest y value, to provide breathing room
    XLow = -1
    XHigh = len(dataset)
    YLimit = max(dataset)+5
    set_plot_xlimits("Algorithm", XLow, XHigh)
    set_plot_ylimits("Algorithm", 0, YLimit)

def highlighttest(dataset):
    leng = len(dataset)
    position = get_data("position")
    position += 1

    if(position == leng):
        position = 0

    print(position)

    add_data("position", position)    
    add_bar_series("Algorithm", "selection", [position], [yVals[position]], weight=0.5)
    sleep(0.5)

def bubble(data):
    n = len(data)
    for i in range(n-1):
        for j in range(0, n-i-1):
            if data[j] > data[j + 1]:
                data[j], data[j + 1] = data[j + 1], data[j]
            add_bar_series("Algorithm", "selection", [xVals[j], xVals[j+1]], [data[j], data[j+1]], weight=0.5)
            add_bar_series("Algorithm", "data", xVals, data, weight=0.5)
            sleep(0.1)
            

with window("SortSim", height=5*WINDOW_HEIGHT//6, **CHILD_WINDOW_FILL_PARAMS):
    add_button("bubble", callback=(lambda bub: bubble(yVals)))
    add_plot("Algorithm", height=380, width=-1, **UNINTERACTIVE_GRAPH_PARAMS)
    add_bar_series("Algorithm", "data", xVals, yVals, weight=0.5)
    
    add_data("position", 0)

    setLimits(yVals)
    set_window_pos("SortSim", 0, WINDOW_HEIGHT//6)

start_dearpygui(primary_window="ELPath") 


