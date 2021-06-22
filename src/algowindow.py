from dearpygui.core import *
from dearpygui.simple import *
from algohost import AlgorithmHost
from consts import *
from random import randint
from time import sleep

class AlgorithmWindow:
    def __init__(self):
        self.AlgorithmController = AlgorithmHost(self.update) 
        
        with window("SortSim", height=5*WINDOW_HEIGHT//6, **CHILD_WINDOW_FILL_PARAMS):
            add_plot("Algorithm", height=380, width=-1, **UNINTERACTIVE_GRAPH_PARAMS)
            set_window_pos("SortSim", 0, WINDOW_HEIGHT//6)
            self.initialize_plot()
            self.set_limits()

    def set_limits(self):
        # Because we initialize our plots starting at 0 now, we just need to see everything from -1 (to include the 0 position) to
        # the end of the dataset's length. The Y limit is gonna be a bit more than the highest y value, to provide breathing room
        XLow = -1
        XHigh = self.AlgorithmController.data_set_size
        # We can just use the data_set_size for the y limit, because that's the max of the randint function when generating random data
        YLimit = self.AlgorithmController.data_set_size+5

        set_plot_xlimits("Algorithm", XLow, XHigh)
        set_plot_ylimits("Algorithm", 0, YLimit)

    def initialize_plot(self):
        add_bar_series("Algorithm", "data", self.AlgorithmController.data_x, self.AlgorithmController.data_y, weight=0.5)

    # For now, just redraw everything, specific graph redraw can be slated for later
    # 6/21/21 Multipurpose function: if new_data == 1, clear out highlight
    def update(self, new_data):
        if (new_data == 1):
            add_bar_series("Algorithm", "highlight", [0], [0], weight=0.5)
            add_bar_series("Algorithm", "highlight-special", [0], [0], weight=0.5)
        else:
            add_bar_series("Algorithm", "data", self.AlgorithmController.data_x, self.AlgorithmController.data_y, weight=0.5)
            add_bar_series("Algorithm", "highlight", new_data[1], [self.AlgorithmController.data_y[x_value] for x_value in new_data[1]], weight=0.5)
            if (new_data[2]):
                add_bar_series("Algorithm", "highlight-special", new_data[1], [self.AlgorithmController.data_y[x_value] for x_value in new_data[1]], weight=0.5)
            else:
                add_bar_series("Algorithm", "highlight-special", [0], [0], weight=0.5)


    def new_dataset(self):
        self.AlgorithmController.set_random_data()
        self.initialize_plot()

    def next_step(self):
        self.AlgorithmController.next_step()

    def start_sim(self):
        self.AlgorithmController.start_sim()