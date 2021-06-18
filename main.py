from dearpygui.core import *
from dearpygui.simple import *

# For maximum compat (and because I don't see any real reason not to,) the window is designed to fit in smaller screens (laptops, etc)
WINDOW_WIDTH, WINDOW_HEIGHT = 1200, 900

# Window settings
set_global_font_scale(1.5);
set_theme("Dark Grey")
set_main_window_size(WINDOW_WIDTH, WINDOW_HEIGHT)
set_style_window_padding(10, 10)
add_additional_font("resources/fonts/Roboto_Mono/static/RobotoMono-Regular.ttf", 20)
with window("ELPath", width=880, height=880):
    set_window_pos("ELPath", 0, 0)
    

with window("Main Controls", width=WINDOW_WIDTH-15, height=WINDOW_HEIGHT//6, no_resize=True, no_collapse=False, no_close=True, no_move=True):
    add_text("This is the start of something interestnig")
    set_window_pos("Main Controls", 0, 0)

with window("SortSim", width=WINDOW_WIDTH-15, height=5*WINDOW_HEIGHT//6, no_resize=True, no_collapse=False, no_close=True, no_move=True):
    add_text("This is the start of something interestnig")
    set_window_pos("SortSim", 0, WINDOW_HEIGHT//6)
    

start_dearpygui(primary_window="ELPath") 
