from time import sleep
from dearpygui.core import *
from dearpygui.simple import *
from algohost import AlgorithmHost
from algowindow import AlgorithmWindow
import consts as cnsts

class ELPath():
    def __init__(self):
        self.step_sleep = 5
        self.algorithms = AlgorithmWindow()
        self.callbacks = {
            "next_step": self.algorithms.next_step,
            "original": self.algorithms.original_data,
            "run_sim": self.run_sim,
            "randomize": self.algorithms.new_dataset,
            "set_algorithm": self.algorithms.change_algorithm
        }
        self.__initialize_window()
        self.__link_controls()
        

    def __initialize_window(self):
        # Window settings
        set_global_font_scale(1.2);
        set_theme("Dark Grey")
        set_main_window_size(cnsts.WINDOW_WIDTH, cnsts.WINDOW_HEIGHT)
        add_additional_font("resources/fonts/Roboto_Mono/static/RobotoMono-Regular.ttf", 20)

        with window("ELPath", width=1200, height=700):
            pass
        with window("Info", width=cnsts.SIDEBAR_WIDTH-5, height=800, **cnsts.CHILD_WINDOW_FILL_PARAMS):
            set_window_pos("Info", 5, 350)
            add_text("Info:", wrap=300)
            add_text("alginfo", wrap=300)
            set_value("alginfo", "")
            pass
        with window("SortSim", height=800, width=800, no_scrollbar=True, **cnsts.CHILD_WINDOW_FILL_PARAMS):
            set_window_pos("SortSim", cnsts.SIDEBAR_WIDTH, 25)
            set_style_window_border_size(0)
            add_plot("Algorithm", height=790, width=790,  **cnsts.UNINTERACTIVE_GRAPH_PARAMS)
            self.algorithms.initialize_plot()

            
    def __link_controls(self):
        # Have to use a list for callback_data because for some reason, passing in a function reference as the data runs said function 
        add_text("Algorithm:", parent="ELPath")
        add_combo("algorithm_combobox", label="", parent="ELPath", 
        default_value=self.algorithms.algorithms_host.alg_name, 
        items=tuple(self.algorithms.algorithms_host.alg_list.keys()), 
        callback=self.callbacks["set_algorithm"],
        width=300)
        
        add_spacing(parent="ELPath", count=5)
        
        add_checkbox("run_sim_checkbox", label="Run", parent="ELPath", callback=self.callbacks["run_sim"])
        add_same_line(parent="ELPath")
        add_button("next_step_button", label="Next Step", parent="ELPath", callback=self.callbacks["next_step"])
        
        add_spacing(parent="ELPath", count=5)

        add_text("Speed:", parent="ELPath")
        add_slider_int("step_sleep_slider", label="", parent="ELPath", width=300, default_value=self.step_sleep, clamped=True, min_value=0, max_value=100)
        
        add_spacing(parent="ELPath", count=5)

        add_text("Data:", parent="ELPath")
        add_button("original_data_button", label="Original Data", parent="ELPath", callback=self.callbacks["original"])        
        add_button("randomize_button", label="Randomize Data", parent="ELPath", callback=self.callbacks["randomize"])

    def update_info(self, message):
        set_value("alginfo", f"{message}")

    def run_sim(self, sender):
        while get_value(sender):
            i = self.algorithms.next_step()
            m = self.algorithms.message
            self.update_info(m)

            
            sleep(get_value("step_sleep_slider")/100)
            
            configure_item("algorithm_combobox", enabled=False)
            configure_item("original_data_button", enabled=False)
            configure_item("randomize_button", enabled=False)
            configure_item("next_step_button", enabled=False)
            
            if (not i):
                set_value(sender, False)
                break

        configure_item("algorithm_combobox", enabled=True)
        configure_item("original_data_button", enabled=True)
        configure_item("randomize_button", enabled=True)
        configure_item("next_step_button", enabled=True)
        