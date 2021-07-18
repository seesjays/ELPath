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
        window_size = 800
        side_cell_count = 20
        cell_size = window_size/side_cell_count
        set_mouse_click_callback(self.get_clicked_cell)
        
        for i in range(side_cell_count):
            for j in range(side_cell_count):
                draw_rectangle("Simulation", [i*cell_size+10, j*cell_size], [(i+1)*cell_size+10, (j+1)*cell_size], [
                               34, 36, 37, 255], fill=[255, 255, 255, 255], rounding=2, thickness=1)
        #self.message = f"{self.pathing_host.alg_name}"


    def get_clicked_cell(self):
        pos = get_mouse_pos()
        left_bound_adjusted_x = pos[0]-10
        top_bound_adjusted_y = pos[1]+30

        min_x = 0
        min_y = 0
        max_x = 810
        max_y = 770
        
        print((left_bound_adjusted_x, top_bound_adjusted_y))

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
