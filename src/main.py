from dearpygui.core import *
from dearpygui.simple import *
from random import randint
from time import sleep

# For maximum compat (and because I don't see any real reason not to,) the window is designed to fit in smaller screens (laptops, etc)
WINDOW_WIDTH, WINDOW_HEIGHT = 1200, 900
FILL_WIDTH = WINDOW_WIDTH-15
testvalset = [i for i in range(0, 5)]

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

# Window settings
set_global_font_scale(1.5);
set_theme("Dark Grey")
set_main_window_size(WINDOW_WIDTH, WINDOW_HEIGHT)
set_style_window_padding(10, 10)
add_additional_font("resources/fonts/Roboto_Mono/static/RobotoMono-Regular.ttf", 20)

with window("ELPath", width=880, height=880):
    set_window_pos("ELPath", 0, 0)

with window("Main Controls", height=WINDOW_HEIGHT//6, **CHILD_WINDOW_FILL_PARAMS):
    add_text("This is the start of something interestnig")
    set_window_pos("Main Controls", 0, 0)

def calclimits(dataset):
    return (min(dataset)-1, max(dataset)+1, len(dataset)+1)

def bubble(data):
    n = len(data)
    for i in range(n-1):
        for j in range(0, n-i-1):
            if data[j] > data[j + 1]:
                sleep(1)
                data[j], data[j + 1] = data[j + 1], data[j]
                set_value("Simpleplot2", data)
    print(data)

valz = [i for i in range(1, 51)]

def highlighttest(leng):
    leng = len(valz)
    position = get_data("position")
    position += 1

    if(position == leng):
        position = 0

    print(position)

    add_data("position", position)

    
    add_bar_series("Simpleplot2", "selection", [valz[position]], [valz[position]], weight=0.5)
    sleep(0.5)




with window("SortSim", height=5*WINDOW_HEIGHT//6, **CHILD_WINDOW_FILL_PARAMS):
    add_plot("Simpleplot2", height=380, width=-1, **UNINTERACTIVE_GRAPH_PARAMS)
    add_bar_series("Simpleplot2", "", valz, valz, weight=0.5)
    
    add_data("position", 0)

    limits = calclimits(valz)
    set_plot_xlimits("Simpleplot2", limits[0], limits[1])
    set_plot_ylimits("Simpleplot2", 0, limits[2])

    set_render_callback(highlighttest)

    set_window_pos("SortSim", 0, WINDOW_HEIGHT//6)

start_dearpygui(primary_window="ELPath") 


