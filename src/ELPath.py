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
        self.algorithms = None
        self.pathing = None

        self.mode = "Sorting"

        self.all_algorithms = {}

        self.__initialize_window()
        self.__mount(self.mode, "Quick Sort")

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

        # populate alg list for combobox
        tempalgs = AlgorithmWindow()
        for algname in tempalgs.algorithms_host.alg_list:
            self.all_algorithms[algname] = "Sorting"
        tempalgs = PathingWindow()
        for algname in tempalgs.pathing_host.alg_list:
            self.all_algorithms[algname] = "Pathfinding"
        tempalgs = None

    def __unmount(self):
        delete_item("ELPath", children_only=True)  # remove controls
        if self.mode == "Sorting":
            self.algorithms.unmount()
            self.algorithms = None
        elif self.mode == "Pathfinding":
            self.pathing.unmount()
            self.pathing = None
        delete_item("Simulation", children_only=True)

    def change_algorithm(self):
        newalg = get_value("algorithm_combobox")
        newalgmode = self.all_algorithms[newalg]
        if self.mode == "Sorting" and newalgmode == self.mode:
            self.sorting_callbacks["set_algorithm"](newalg)
            self.update_info_no_wrapper()
        elif self.mode == "Pathfinding" and newalgmode == self.mode:
            self.pathfinding_callbacks["set_algorithm"](newalg)
            self.update_info_no_wrapper()
        else:  # mismatch
            self.__unmount()
            self.__mount(newalgmode, newalg)

    def __mount_sorting(self, alg):
        self.algorithms = AlgorithmWindow()
        self.sorting_callbacks = {
            "next_step": self.update_info(self.algorithms.next_step),
            "original": self.update_info(self.algorithms.original_data),
            "run_sim": self.run_sim,
            "randomize": self.update_info(self.algorithms.new_dataset),
            "set_algorithm": self.algorithms.change_algorithm
        }
        self.algorithms.initialize_plot()
        self.algorithms.reset_plot()
        self.algorithms.change_algorithm(alg)

    def __mount_pathing(self, alg):
        self.pathing = PathingWindow()
        self.pathfinding_callbacks = {
            "generate_maze": self.pathing.pathing_host.rand_maze,
            "set_algorithm": self.pathing.change_algorithm,
            "run_sim": self.run_pathfinding,
            "next_step": self.pathing.next_step,
            "reset": self.pathing.reset,
            "retry": self.pathing.retry
        }
        self.pathing.initialize_grid()
        self.pathing.change_algorithm(alg)

    def __mount(self, newmode, newalg):
        if (newmode == "Sorting"):
            self.__mount_sorting(newalg)
            self.__link_sorting_controls()
            self.curr_window = self.algorithms
        else:
            self.__mount_pathing(newalg)
            self.__link_pathing_controls()
            self.curr_window = self.pathing

        self.mode = newmode
        self.update_info_no_wrapper()

    def __link_sorting_controls(self):
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
                       default_value=self.step_sleep, clamped=True, min_value=0, max_value=50)

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
        add_button("random_maze", label="Random Maze",
                   parent="ELPath", callback=self.pathfinding_callbacks["generate_maze"])
        add_button("retry_button", label="Retry Maze",
                   parent="ELPath", callback=self.pathfinding_callbacks["retry"])
        add_button("reset_button", label="Reset",
                   parent="ELPath", callback=self.pathfinding_callbacks["reset"])

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
        configure_item("retry_button", enabled=False)
        configure_item("reset_button", enabled=False)

        while get_value(sender):
            updated = self.pathing.next_step()
            sleep(get_value("step_sleep_slider")/100)

            if (not updated):
                set_value(sender, False)
                break

        configure_item("algorithm_combobox", enabled=True)
        configure_item("next_step_button", enabled=True)
        configure_item("retry_button", enabled=True)
        configure_item("reset_button", enabled=True)


    def update_info(self, func):
        def wrapper():
            func()
            set_value("alginfo", self.curr_window.message)

        return wrapper

    def update_info_no_wrapper(self):
        set_value("alginfo", self.curr_window.message)
