import dearpygui.dearpygui as dpg
from algohost import AlgorithmHost
from pathfindhost import PathfindingHost
import consts as cnsts
from random import randint
from time import sleep


class AlgorithmWindow:
    def __init__(self, window_id=None):
        self.algorithms_host = AlgorithmHost()

        self.message = self.algorithms_host.alg_name

        self.highlight_list = []

        self.window_id = window_id

        self.plot = None
        self.plot_x_axis = None
        self.plot_y_axis = None
        self.default_graph = None

        self.plots = {
            "red": None,
            "green": None,
            "yellow": None
        }

    def load_themes(self):
        with dpg.theme() as red:
            dpg.add_theme_color(dpg.mvPlotCol_Fill,
                                (196, 78, 82), category=dpg.mvThemeCat_Plots)
        with dpg.theme() as green:
            dpg.add_theme_color(dpg.mvPlotCol_Fill,
                                (85, 168, 104), category=dpg.mvThemeCat_Plots)
        with dpg.theme() as yellow:
            dpg.add_theme_color(dpg.mvPlotCol_Fill,
                                (204, 185, 116), category=dpg.mvThemeCat_Plots)

        dpg.set_item_theme(self.plots["red"], red)
        dpg.set_item_theme(self.plots["green"], green)
        dpg.set_item_theme(self.plots["yellow"], yellow)

    def set_limits(self):
        # Because we initialize our plots starting at 0 now, we just need to see everything from -1 (to include the 0 position) to
        # the end of the dataset's length. The Y limit is gonna be a bit more than the highest y value, to provide breathing room
        XLow = -1
        XHigh = self.algorithms_host.data_set_size
        # We can just use the data_set_size for the y limit, because that's the max of the randint function when generating random data
        YLimit = self.algorithms_host.data_set_size+5

        dpg.set_axis_limits(self.plot_x_axis, XLow, XHigh)
        dpg.set_axis_limits(self.plot_y_axis, 0, YLimit)

    def initialize_plot(self):
        self.plot = dpg.add_plot(
            label=self.algorithms_host.alg_name, width=-1, height=-1, parent=self.window_id, no_menus=True,
            no_box_select=True,
            no_mouse_pos=True,
            crosshairs=False)

        self.plot_x_axis = dpg.add_plot_axis(dpg.mvXAxis, label="", no_gridlines=True, no_tick_marks=True,
                                             no_tick_labels=True, lock_min=True, lock_max=True, parent=self.plot)
        self.plot_y_axis = dpg.add_plot_axis(dpg.mvYAxis, label="", no_gridlines=True, no_tick_marks=True,
                                             no_tick_labels=True, lock_min=True, lock_max=True,  parent=self.plot)

        self.default_graph = dpg.add_bar_series(
            self.algorithms_host.data_x, self.algorithms_host.data_y, label="", weight=0.5, parent=self.plot_y_axis)

        self.plots["red"] = dpg.add_bar_series(
            self.algorithms_host.data_x, self.algorithms_host.data_y, label="", weight=0.5, parent=self.plot_y_axis)
        self.plots["green"] = dpg.add_bar_series(
            self.algorithms_host.data_x, self.algorithms_host.data_y, label="", weight=0.5, parent=self.plot_y_axis)
        self.plots["yellow"] = dpg.add_bar_series(
            self.algorithms_host.data_x, self.algorithms_host.data_y, label="", weight=0.5, parent=self.plot_y_axis)

        self.load_themes()

        self.set_limits()

    def reset_plot(self):
        dpg.set_item_label(self.plot, f"{self.algorithms_host.alg_name}")
        self.message = f"{self.algorithms_host.alg_name}"

        dpg.set_value(self.default_graph, [
                      self.algorithms_host.data_x, self.algorithms_host.data_y])

        self.clear_highlights()
        self.set_limits()

    def update(self, new_data):
        dpg.set_value(self.default_graph, [
                      self.algorithms_host.data_x, self.algorithms_host.data_y])

        if (not new_data):
            self.clear_highlights()
            dpg.set_value(self.plots["green"], [
                          self.algorithms_host.data_x, self.algorithms_host.data_y])

            self.message = f"{self.algorithms_host.alg_name}: Complete in {self.algorithms_host.step_counter} steps."

        else:
            self.clear_highlights()
            for highlight in new_data:
                print(new_data)
                if (highlight != "message"):
                    x_highlight = new_data[highlight]

                    dpg.set_value(self.plots[highlight], [x_highlight, [
                        self.algorithms_host.data_y[x_value] for x_value in x_highlight]])

            self.message = f"{self.algorithms_host.alg_name} Step {self.algorithms_host.step_counter}: {new_data['message']}"

    def clear_highlights(self):
        dpg.set_value(self.plots["red"], [[0], [0]])
        dpg.set_value(self.plots["green"], [[0], [0]])
        dpg.set_value(self.plots["yellow"], [[0], [0]])

    def new_dataset(self):
        self.algorithms_host.set_random_data()
        self.reset_plot()

    def set_speed(self, speed):
        self.step_sleep = speed

    def next_step(self):
        value = self.algorithms_host.next_step()
        self.update(value)
        return value

    def change_algorithm(self, newalg):
        self.clear_highlights()
        self.algorithms_host.set_algorithm(newalg)
        self.original_data()

    def original_data(self):
        self.clear_highlights()
        self.algorithms_host.reset_data()
        self.reset_plot()

    def unmount(self):
        dpg.delete_item(self.plot)
        self.algorithms_host = None

    def current_alg(self):
        return self.algorithms_host.alg_name

    def is_initial(self):
        if self.algorithms_host.step_counter == 0:
            return True
        return False
