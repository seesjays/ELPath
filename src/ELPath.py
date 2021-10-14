import dearpygui.dearpygui as dpg
from time import sleep
from algowindow import AlgorithmWindow
from pathingwindow import PathingWindow
import definitions as defs


class ELPath():
    def __init__(self):
        self.WINDOW_WIDTH, self.WINDOW_HEIGHT = 1250, 950
        self.SIDEBAR_WIDTH = 350

        self.step_sleep = 5
        self.algorithms = None
        self.pathing = None

        self.mode = "Pathfinding"

        self.all_algorithms = {}

        self.curr_window = None

        self.ELPath_window = None
        self.controls_panel = None
        self.simulation_window = None

        self.combobox = dpg.generate_uuid()
        self.sleepslider = dpg.generate_uuid()
        self.infotext = dpg.generate_uuid()

        self.transient_controls = []

        self.__init_window()

        self.__mount(self.mode, "Breadth-First Search")

    def viewport_config(self):
        # Necessary to set the window size
        dpg.create_viewport()
        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.set_viewport_title("ELPath")
        dpg.set_viewport_width(self.WINDOW_WIDTH)
        dpg.set_viewport_height(self.WINDOW_HEIGHT)

    def __init_window(self):
        with dpg.font_registry():
            dpg.bind_font(dpg.add_font(
                "resources/fonts/Roboto_Mono/static/RobotoMono-Regular.ttf", 20))
            dpg.set_global_font_scale(1.2)

        with dpg.window(label="ELPath") as self.ELPath_window:
            with dpg.child_window(label="Controls_Info", width=self.SIDEBAR_WIDTH, pos=[10, 10], border=False, no_scrollbar=True):
                with dpg.collapsing_header(label="Controls", default_open=True) as self.controls_panel:
                    pass
                with dpg.collapsing_header(label="Info", default_open=True):
                    self.infotext = dpg.add_text("alginfo", wrap=300)

            with dpg.child_window(label="Simulation", height=815, width=815, no_scrollbar=True, pos=[self.SIDEBAR_WIDTH+20, 10]) as simulation_window:
                self.simulation_window = simulation_window

        dpg.set_primary_window(self.ELPath_window, True)

        # populate alg list for combobox
        tempalgs = AlgorithmWindow()
        for algname in tempalgs.algorithms_host.alg_list:
            self.all_algorithms[algname] = "Sorting"
        tempalgs = PathingWindow()
        for algname in tempalgs.pathing_host.alg_list:
            self.all_algorithms[algname] = "Pathfinding"
        tempalgs = None

    def __unmount(self):
        dpg.delete_item(self.controls_panel,
                        children_only=True)  # remove controls

        if self.mode == "Sorting":
            self.algorithms.unmount()
            self.algorithms = None
        elif self.mode == "Pathfinding":
            self.pathing.unmount()
            self.pathing = None

        # Should be cleared in the unmounting functions, but this is here for extra insurance.
        dpg.delete_item(self.simulation_window, children_only=True)

    def change_algorithm(self):
        newalg = dpg.get_value(self.combobox)
        newalgmode = self.all_algorithms[newalg]

        # User was on a sorting simulation and swapped to another sorting simulation
        if self.mode == "Sorting" and newalgmode == self.mode:
            self.sorting_callbacks["set_algorithm"](newalg)

        # User was on a pathfinding simulation and swapped to another sorting simulation
        elif self.mode == "Pathfinding" and newalgmode == self.mode:
            self.pathfinding_callbacks["set_algorithm"](newalg)

        # User swapped between a sorting/pathfinding simulation
        else:
            self.__unmount()
            self.__mount(newalgmode, newalg)

        self.update_info_no_wrapper()
        self.update_info_alg_definition()

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
        self.update_info_alg_definition()

    def __mount_sorting(self, alg):
        self.algorithms = AlgorithmWindow(window_tag=self.simulation_window)
        self.sorting_callbacks = {
            "decrease": self.update_info(self.algorithms.decrease_dataset),
            "increase": self.update_info(self.algorithms.increase_dataset),
            "next_step": self.update_info(self.algorithms.next_step),
            "original": self.update_info(self.algorithms.original_data),
            "randomize": self.update_info(self.algorithms.new_dataset),
            "run_sim": self.run_sim,
            "set_algorithm": self.algorithms.change_algorithm
        }
        self.algorithms.initialize_plot()
        self.algorithms.reset_plot()
        self.algorithms.change_algorithm(alg)

    def __mount_pathing(self, alg):
        self.pathing = PathingWindow(window_tag=self.simulation_window)
        self.pathfinding_callbacks = {
            "decrease": self.update_info(self.pathing.shrink_maze),
            "generate_maze": self.update_info(self.pathing.randmaze),
            "increase": self.update_info(self.pathing.grow_maze),
            "next_step": self.update_info(self.pathing.next_step),
            "reset": self.update_info(self.pathing.reset),
            "retry": self.update_info(self.pathing.retry),
            "run_sim": self.run_sim,
            "set_algorithm": self.pathing.change_algorithm,
        }
        self.pathing.initialize_grid()
        self.pathing.change_algorithm(alg)

    def __link_sorting_controls(self):
        self.transient_controls = []

        dpg.add_text("Algorithm:", parent=self.controls_panel)
        self.transient_controls.append(dpg.add_combo(label="", parent=self.controls_panel,
                                                     default_value=self.algorithms.algorithms_host.alg_name,
                                                     items=list(
                                                         self.all_algorithms.keys()),
                                                     callback=self.change_algorithm,
                                                     width=300,
                                                     tag=self.combobox))

        dpg.add_spacer(parent=self.controls_panel, width=5)

        dpg.add_checkbox(label="Run",
                         parent=self.controls_panel, callback=self.sorting_callbacks["run_sim"])

        dpg.add_same_line(parent=self.controls_panel)
        self.transient_controls.append(dpg.add_button(label="Next Step",
                                                      parent=self.controls_panel, callback=self.sorting_callbacks["next_step"]))

        dpg.add_spacer(parent=self.controls_panel, width=5)

        dpg.add_text("Speed:", parent=self.controls_panel)
        dpg.add_slider_int(label="", parent=self.controls_panel, width=300,
                           default_value=self.step_sleep, clamped=True, min_value=0, max_value=50, tag=self.sleepslider)

        dpg.add_spacer(parent=self.controls_panel, width=5)

        dpg.add_text("Data:", parent=self.controls_panel)
        self.transient_controls.append(dpg.add_button(label="Increase",
                                                      parent=self.controls_panel, callback=self.sorting_callbacks["increase"]))
        dpg.add_same_line(parent=self.controls_panel)
        self.transient_controls.append(dpg.add_button(label="Decrease",
                                                      parent=self.controls_panel, callback=self.sorting_callbacks["decrease"]))

        self.transient_controls.append(dpg.add_button(label="Original Data",
                                                      parent=self.controls_panel, callback=self.sorting_callbacks["original"]))
        self.transient_controls.append(dpg.add_button(label="Randomize Data",
                                                      parent=self.controls_panel, callback=self.sorting_callbacks["randomize"]))
        dpg.add_spacer(parent=self.controls_panel, width=5)

    def __link_pathing_controls(self):
        self.transient_controls = []

        dpg.add_text("Algorithm:", parent=self.controls_panel)
        self.transient_controls.append(dpg.add_combo(label="", parent=self.controls_panel,
                                                     default_value=self.pathing.pathing_host.alg_name,
                                                     items=list(
                                                         self.all_algorithms.keys()),
                                                     callback=self.change_algorithm,
                                                     width=300, tag=self.combobox))

        dpg.add_spacer(parent=self.controls_panel, width=5)

        with dpg.group(horizontal=True, parent=self.controls_panel):
            dpg.add_checkbox(label="Run",
                             callback=self.pathfinding_callbacks["run_sim"])

            self.transient_controls.append(dpg.add_button(label="Next Step",
                                                          callback=self.pathfinding_callbacks["next_step"]))

        dpg.add_spacer(parent=self.controls_panel, width=5)

        dpg.add_text("Speed:", parent=self.controls_panel)
        dpg.add_slider_int(label="", parent=self.controls_panel, width=300,
                           default_value=self.step_sleep, clamped=True, min_value=0, max_value=100, tag=self.sleepslider)

        dpg.add_spacer(parent=self.controls_panel, width=5)
        dpg.add_text("Maze:", parent=self.controls_panel)
        with dpg.group(horizontal=True, parent=self.controls_panel):
            self.transient_controls.append(dpg.add_button(label="Grow",
                                                          callback=self.pathfinding_callbacks["increase"]))
            self.transient_controls.append(dpg.add_button(label="Shrink",
                                                          callback=self.pathfinding_callbacks["decrease"]))

        with dpg.group(horizontal=True, parent=self.controls_panel):
            self.transient_controls.append(dpg.add_button(label="Random Maze",
                                                          callback=self.pathfinding_callbacks["generate_maze"]))
            self.transient_controls.append(dpg.add_button(label="Retry Maze",
                                                          callback=self.pathfinding_callbacks["retry"]))

        self.transient_controls.append(dpg.add_button(label="Reset",
                                                      parent=self.controls_panel, callback=self.pathfinding_callbacks["reset"]))

    def run_sim(self, sender):
        for control in self.transient_controls:
            dpg.configure_item(control, enabled=False)

        while dpg.get_value(sender):
            i = self.curr_window.next_step()
            self.update_info_no_wrapper()

            sleep(dpg.get_value(self.sleepslider)/100)

            if (not i):
                dpg.set_value(sender, False)
                self.update_info_no_wrapper()
                break
        for control in self.transient_controls:
            dpg.configure_item(control, enabled=True)

    # Info

    def update_info(self, func):
        def wrapper():
            func()
            dpg.set_value(self.infotext, self.curr_window.message)
            if self.curr_window.is_initial():
                self.update_info_alg_definition()

        return wrapper

    def update_info_no_wrapper(self):
        dpg.set_value(self.infotext, self.curr_window.message)
        if self.curr_window.is_initial():
            self.update_info_alg_definition()

    def update_info_alg_definition(self):
        definition = defs.DEFINITIONS[self.curr_window.current_alg()]

        algtype = definition[0]
        cases = definition[1]
        desc = definition[2]

        defstring = f"{self.curr_window.current_alg()}\n\n"
        defstring += "Type: " + algtype + '\n\n'

        defstring += "Time Complexities:" if len(
            cases) > 1 else "Time Complexity:"
        for case in cases:
            defstring += '\n' + case

        defstring += "\n\n"

        desc = desc.replace("\n", "").replace("\t", "").strip()
        desc = ' '.join(desc.split())
        defstring += desc

        dpg.set_value(self.infotext, defstring)
