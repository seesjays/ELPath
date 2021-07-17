from dearpygui.core import *
from dearpygui.simple import *
from pathfindhost import PathfindingHost
import consts as cnsts
from random import randint
from time import sleep

class PathingWindow:
    def __init__(self):
        self.pathing_host = PathfindingHost()
        #self.message = self.pathing_host.alg_name

    def initialize_grid(self):
        grid_name = "Pathfinding_Grid"
        add_drawing(grid_name, parent="Simulation", width=800, height=800)
        for i in range(20):
            for j in range(20):
                draw_rectangle(grid_name, [i, j], [(i+1)*20, (j+1)*20], [255, 255, 255, 255], fill=[255, 255, 255, 255], rounding=5)
        #self.message = f"{self.pathing_host.alg_name}"

    def update(self, new_data):
        pass
        self.message = f"{self.pathing_host.alg_name} Step {self.pathing_host.step_counter}: {new_data['message']}"

    def next_step(self):
        value = self.pathing_host.next_step()
        self.update(value)
        return value

    def change_algorithm(self):
        self.clear_highlights()
        self.pathing_host.set_algorithm(get_value("algorithm_combobox"))
        self.original_data()