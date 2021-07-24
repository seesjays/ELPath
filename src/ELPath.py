from time import sleep
from dearpygui.core import *
from dearpygui.simple import *
from algohost import AlgorithmHost
from algowindow import AlgorithmWindow
import consts as cnsts
from pathingwindow import PathingWindow


class ELPath():
    def __init__(self):
        self.step_sleep = 5
        self.algorithms = AlgorithmWindow()
        self.pathing = PathingWindow()

        self.mode = "Pathfinding"

        self.all_algorithms = {}
        for algname in self.algorithms.algorithms_host.alg_list:
            self.all_algorithms[algname] = "Sorting"
        for algname in self.pathing.pathing_host.alg_list:
            self.all_algorithms[algname] = "Pathfinding"

        self.sorting_callbacks = {
            "next_step": self.update_info(self.algorithms.next_step),
            "original": self.update_info(self.algorithms.original_data),
            "run_sim": self.run_sim,
            "randomize": self.update_info(self.algorithms.new_dataset),
            "set_algorithm": self.update_info(self.algorithms.change_algorithm)
        }

        self.pathfinding_callbacks = {
            "run_sim": self.run_pathfinding,
            "next_step": self.pathing.next_step,
            "reset": self.pathing.reset,
            "retry": self.pathing.retry
        }

        self.__initialize_window()

    def __initialize_window(self):
        # Window settings
        set_global_font_scale(1.2)
        set_theme("Dark Grey")
        set_main_window_size(cnsts.WINDOW_WIDTH, cnsts.WINDOW_HEIGHT)
        set_style_window_border_size(0)
        set_style_window_rounding(0)
        set_style_window_padding(0, 0)

        add_additional_font(
            "resources/fonts/Roboto_Mono/static/RobotoMono-Regular.ttf", 20)

        with window("ELPath", width=1200, height=1000):
            pass
        with window("Info", width=cnsts.SIDEBAR_WIDTH-5, height=800, **cnsts.CHILD_WINDOW_FILL_PARAMS):
            set_window_pos("Info", 5, 350)
            add_text("Info:", wrap=300)
            add_text("alginfo", wrap=300)
            set_value("alginfo", "")
            pass
        with window("Simulation", height=800, width=800, no_scrollbar=True, x_pos=cnsts.SIDEBAR_WIDTH, y_pos=30, **cnsts.CHILD_WINDOW_FILL_PARAMS):
            pass

            #
            self.__switch_mode(self.mode)

    def __switch_mode(self, newmode):
        self.__unlink_controls()

        if (self.mode != newmode):  # swapping
            if (newmode == "Sorting"):
                self.pathing.unmount()
                self.__link__sorting_controls()
                self.algorithms.initialize_plot()
                self.algorithms.reset_plot()
            else:
                self.algorithms.unmount()
                self.pathing.initialize_grid()
                self.__link_pathing_controls()

            self.mode = newmode
        else:  # init
            if (self.mode == "Sorting"):
                self.algorithms.initialize_plot()
                self.algorithms.reset_plot()
                self.__link__sorting_controls()

            else:
                self.pathing.initialize_grid()
                self.__link_pathing_controls()

    def __link__sorting_controls(self):
        add_text("Algorithm:", parent="ELPath")
        add_combo("algorithm_combobox", label="", parent="ELPath",
                  default_value=self.algorithms.algorithms_host.alg_name,
                  items=list(self.all_algorithms.keys()),
                  callback=self.change_algorithm,
                  width=300)

        add_spacing(parent="ELPath", count=5)

        add_checkbox("run_sim_checkbox", label="Run",
                     parent="ELPath", callback=self.sorting_callbacks["run_sim"])
        add_same_line(parent="ELPath")
        add_button("next_step_button", label="Next Step",
                   parent="ELPath", callback=self.sorting_callbacks["next_step"])

        add_spacing(parent="ELPath", count=5)

        add_text("Speed:", parent="ELPath")
        add_slider_int("step_sleep_slider", label="", parent="ELPath", width=300,
                       default_value=self.step_sleep, clamped=True, min_value=0, max_value=100)

        add_spacing(parent="ELPath", count=5)

        add_text("Data:", parent="ELPath")
        add_button("original_data_button", label="Original Data",
                   parent="ELPath", callback=self.sorting_callbacks["original"])
        add_button("randomize_button", label="Randomize Data",
                   parent="ELPath", callback=self.sorting_callbacks["randomize"])

        add_spacing(parent="ELPath", count=5)

    def __link_pathing_controls(self):
        add_text("Algorithm:", parent="ELPath")
        add_combo("algorithm_combobox", label="", parent="ELPath",
                  default_value=self.pathing.pathing_host.alg_name,
                  items=list(self.all_algorithms.keys()),
                  callback=self.change_algorithm,
                  width=300)

        add_spacing(parent="ELPath", count=5)

        add_checkbox("run_sim_checkbox", label="Run",
                     parent="ELPath", callback=self.pathfinding_callbacks["run_sim"])
        add_same_line(parent="ELPath")
        add_button("next_step_button", label="Next Step",
                   parent="ELPath", callback=self.pathfinding_callbacks["next_step"])

        add_spacing(parent="ELPath", count=5)

        add_text("Speed:", parent="ELPath")
        add_slider_int("step_sleep_slider", label="", parent="ELPath", width=300,
                       default_value=self.step_sleep, clamped=True, min_value=0, max_value=100)

        add_spacing(parent="ELPath", count=5)

        add_text("Maze:", parent="ELPath")
        add_button("original_data_button", label="Retry Maze",
                   parent="ELPath", callback=self.pathfinding_callbacks["retry"])
        add_button("randomize_button", label="Reset",
                   parent="ELPath", callback=self.pathfinding_callbacks["reset"])

    def __unlink_controls(self):
        delete_item("ELPath", children_only=True)

    def change_algorithm(self):
        newalgmode = self.all_algorithms[get_value("algorithm_combobox")]
        if self.mode == "Sorting" and newalgmode == self.mode:
            self.sorting_callbacks["set_algorithm"]()
        elif self.mode == "Pathfinding" and newalgmode == self.mode:
            pass
        else:  # mismatch
            self.__switch_mode(newalgmode)

    def run_sim(self, sender):
        configure_item("algorithm_combobox", enabled=False)
        configure_item("original_data_button", enabled=False)
        configure_item("randomize_button", enabled=False)
        configure_item("next_step_button", enabled=False)
        while get_value(sender):
            i = self.algorithms.next_step()
            self.update_info_no_wrapper()

            sleep(get_value("step_sleep_slider")/100)

            if (not i):
                set_value(sender, False)
                self.update_info_no_wrapper()
                break

        configure_item("algorithm_combobox", enabled=True)
        configure_item("original_data_button", enabled=True)
        configure_item("randomize_button", enabled=True)
        configure_item("next_step_button", enabled=True)

    def run_pathfinding(self, sender):
        configure_item("algorithm_combobox", enabled=False)
        configure_item("next_step_button", enabled=False)

        while get_value(sender):
            i = self.pathing.next_step()
            sleep(get_value("step_sleep_slider")/100)
            if (not i):
                set_value(sender, False)
                break

        configure_item("algorithm_combobox", enabled=True)
        configure_item("next_step_button", enabled=True)

    def update_info(self, func):
        def wrapper():
            func()
            set_value("alginfo", self.algorithms.message)
        return wrapper

    def update_info_no_wrapper(self):
        set_value("alginfo", self.algorithms.message)
