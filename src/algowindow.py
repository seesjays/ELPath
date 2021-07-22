from dearpygui.core import *
from dearpygui.simple import *
from algohost import AlgorithmHost
from pathfindhost import PathfindingHost
import consts as cnsts
from random import randint
from time import sleep


class AlgorithmWindow:
    def __init__(self):
        self.algorithms_host = AlgorithmHost()
        self.message = self.algorithms_host.alg_name

        self.highlight_list = []
        

    def set_limits(self):
        # Because we initialize our plots starting at 0 now, we just need to see everything from -1 (to include the 0 position) to
        # the end of the dataset's length. The Y limit is gonna be a bit more than the highest y value, to provide breathing room
        XLow = -1
        XHigh = self.algorithms_host.data_set_size
        # We can just use the data_set_size for the y limit, because that's the max of the randint function when generating random data
        YLimit = self.algorithms_host.data_set_size+5

        set_plot_xlimits("Algorithm", XLow, XHigh)
        set_plot_ylimits("Algorithm", 0, YLimit)

    def initialize_plot(self):
        add_plot("Algorithm", parent="Simulation", height=790, width=790,
                 **cnsts.UNINTERACTIVE_GRAPH_PARAMS)

    def reset_plot(self):
        set_item_label("Algorithm", f"{self.algorithms_host.alg_name}")
        self.message = f"{self.algorithms_host.alg_name}"
        add_bar_series("Algorithm", "data", self.algorithms_host.data_x,
                       self.algorithms_host.data_y, weight=0.5)
        # clear other series
        add_bar_series("Algorithm", "highlight", [0], [0], weight=0.5)
        add_bar_series("Algorithm", "highlight-special", [0], [0], weight=0.5)
        self.set_limits()

    # For now, just redraw everything, specific graph redraw can be slated for later
    # 6/21/21 Multipurpose function: if new_data == 1, clear out highlight
    # 6/30/21 new_data structure as follows: [[red highlight x's], [green highlight x's], "step_desc"]
    # 7/2/21 new_data structure as follows:
    """
    {
        "highlight-tier": [highlight x's],
        "highlight-tier": [highlight x's],
        "highlight-tier": [highlight x's],
        "message": "message to user"
    }
    """

    def update(self, new_data):
        add_bar_series("Algorithm", "data", self.algorithms_host.data_x,
                       self.algorithms_host.data_y, weight=0.5)

        if (not new_data):
            self.clear_highlights()

            add_bar_series("Algorithm", "highlight-special",
                           self.algorithms_host.data_x, self.algorithms_host.data_y, weight=0.5)
            self.message = f"{self.algorithms_host.alg_name}: Complete in {self.algorithms_host.step_counter} steps."

        else:
            self.clear_highlights()
            for highlight in new_data:

                if highlight not in self.highlight_list:
                    self.highlight_list.append(highlight)

                if (highlight != "message"):
                    add_bar_series("Algorithm", highlight,
                                   [0], [0], weight=0.5)
                    x_highlight = new_data[highlight]
                    add_bar_series("Algorithm", highlight, x_highlight, [
                                   self.algorithms_host.data_y[x_value] for x_value in x_highlight], weight=0.5)

            self.message = f"{self.algorithms_host.alg_name} Step {self.algorithms_host.step_counter}: {new_data['message']}"

    def clear_highlights(self):
        for highlight in self.highlight_list:
            add_bar_series("Algorithm", highlight, [0], [0], weight=0.5)

    def new_dataset(self):
        self.clear_highlights()
        self.algorithms_host.set_random_data()
        self.reset_plot()

    def set_speed(self, speed):
        self.step_sleep = speed

    def next_step(self):
        value = self.algorithms_host.next_step()
        self.update(value)
        return value

    def change_algorithm(self):
        self.clear_highlights()
        self.algorithms_host.set_algorithm(get_value("algorithm_combobox"))
        self.original_data()

    def original_data(self):
        self.clear_highlights()
        self.algorithms_host.reset_data()
        self.reset_plot()

    def unmount(self):
        self.new_dataset()
        self.clear_highlights()
        self.reset_plot()

        delete_item("Algorithm")
        self.algorithms_host = AlgorithmHost()
