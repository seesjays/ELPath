from time import sleep
from dearpygui.core import *
from dearpygui.simple import *
from algohost import AlgorithmHost
from algowindow import AlgorithmWindow

# For maximum compat (and because I don't see any real reason not to,) the window is designed to fit in smaller screens (laptops, etc)
WINDOW_WIDTH, WINDOW_HEIGHT = 1200, 900
FILL_WIDTH = WINDOW_WIDTH-15
VAL_CNT = 20

CHILD_WINDOW_FILL_PARAMS = {
    "width": FILL_WIDTH, 
    "no_resize": True, 
    "no_collapse": True, 
    "no_close": True, 
    "no_move": True
}

class ELPath():
    def __init__(self):
        self.step_sleep = 5
        self.algorithms = AlgorithmWindow()
        self.callbacks = {
            "next_step": self.algorithms.next_step,
            "run_sim": self.run_sim,
            "randomize": self.algorithms.new_dataset,
            "set_algorithm": self.algorithms.change_algorithm
        }
        self.__initialize_window()
        self.__link_controls()
        

    def __initialize_window(self):
        # Window settings
        set_global_font_scale(1.5);
        set_theme("Dark Grey")
        set_main_window_size(WINDOW_WIDTH, WINDOW_HEIGHT)
        set_style_window_padding(10, 10)
        add_additional_font("resources/fonts/Roboto_Mono/static/RobotoMono-Regular.ttf", 20)

        with window("ELPath", width=880, height=880):
            set_window_pos("ELPath", 0, 0)

        with window("Main Controls", x_pos=0, y_pos=0, height=WINDOW_HEIGHT//3, **CHILD_WINDOW_FILL_PARAMS): # hardcoded for now, since we only have bubble sort haha
            add_spacing(count=5, name="spacing1")

    def __link_controls(self):
        # Have to use a list for callback_data because for some reason, passing in a function reference as the data runs said function 
        add_text("Algorithm:", parent="Main Controls")
        add_same_line(parent="Main Controls")
        add_combo("algorithm_combobox", label="", parent="Main Controls", 
        default_value="Bubble Sort", 
        items=tuple(self.algorithms.algorithms_host.alg_list.keys()), 
        callback=self.callbacks["set_algorithm"],
        width=400)
        
        add_spacing(parent="Main Controls", count=5)
        
        add_checkbox("run_sim_checkbox", label="Run Simulation", parent="Main Controls", callback=self.callbacks["run_sim"])
        add_same_line(parent="Main Controls")
        add_button("next_step_button", label="Next Step", parent="Main Controls", callback=self.callbacks["next_step"])
        
        add_spacing(parent="Main Controls", count=5)

        add_text("Time:", parent="Main Controls")
        add_same_line(parent="Main Controls")
        add_slider_int("step_sleep_slider", label="", parent="Main Controls", width=400, default_value=self.step_sleep, clamped=True, min_value=0, max_value=100)
        
        add_spacing(parent="Main Controls", count=5)
        
        add_button("randomize_button", label="Randomize Data", parent="Main Controls", callback=self.callbacks["randomize"])


    def run_sim(self, sender):
        while get_value(sender):
            i = self.algorithms.next_step()
            sleep(get_value("step_sleep_slider")/100)
            
            configure_item("algorithm_combobox", enabled=False)
            configure_item("randomize_button", enabled=False)
            configure_item("next_step_button", enabled=False)
            
            if (not i):
                set_value(sender, False)
                break

        configure_item("algorithm_combobox", enabled=True)
        configure_item("randomize_button", enabled=True)
        configure_item("next_step_button", enabled=True)
        