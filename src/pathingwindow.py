from dearpygui.core import *
from dearpygui.simple import *
from pathfindhost import PathfindingHost
import consts as cnsts
from random import randint
from time import sleep
from math import trunc


class PathingWindow:
    def __init__(self):

        self.window_size = 800
        self.side_cell_count = 40
        self.cell_size = self.window_size/self.side_cell_count

        self.min_x = 0
        self.min_y = 0
        self.max_x = 800
        self.max_y = 800

        self.pathing_host = PathfindingHost(self.side_cell_count)

        #self.message = self.pathing_host.alg_name

    def initialize_grid(self):
        set_mouse_down_callback(self.get_clicked_cell)

        for i in range(self.side_cell_count):
            for j in range(self.side_cell_count):
                itag = f"{i:02d}"
                jtag = f"{j:02d}"
                draw_rectangle("grid", [i*self.cell_size, j*self.cell_size], [(i+1)*self.cell_size, (j+1)*self.cell_size], [
                               34, 36, 37, 255], fill=[255, 255, 255, 255], rounding=2, thickness=1, tag=f"{itag}{jtag}")
        #self.message = f"{self.pathing_host.alg_name}"

        # drawing the start and end positions

        modify_draw_command(
            "grid", f"{self.pathing_host.start_point[0]:02d}{self.pathing_host.start_point[1]:02d}", fill=[127, 255, 0, 255])
        modify_draw_command(
            "grid", f"{self.pathing_host.end_point[0]:02d}{self.pathing_host.end_point[1]:02d}", fill=[255, 0, 0, 255])

    def get_clicked_cell(self):
        pos = get_drawing_mouse_pos()
        left_bound_adjusted_x = pos[0]
        top_bound_adjusted_y = pos[1]

        within_x = left_bound_adjusted_x >= self.min_x and left_bound_adjusted_x <= self.max_x
        within_y = top_bound_adjusted_y >= self.min_y and top_bound_adjusted_y <= self.max_y

        x_cell = trunc(pos[0]//self.cell_size)
        y_cell = trunc(pos[1]//self.cell_size)

        clearing = 1 if is_mouse_button_down(1) else 0

        if (get_active_window() == "Simulation" and within_x and within_y):

            print(f"X: {x_cell}\nY: {y_cell}")
            itag = f"{x_cell:02d}"
            jtag = f"{y_cell:02d}"
            print(get_draw_command("grid", f"{itag}{jtag}"))

            if (clearing):
                modify_draw_command(
                    "grid", f"{itag}{jtag}", fill=[255, 255, 255, 255])
            else:
                modify_draw_command(
                    "grid", f"{itag}{jtag}", fill=[54, 54, 54, 255])

        # prevent drawing over start and end
        modify_draw_command(
            "grid", f"{self.pathing_host.start_point[0]:02d}{self.pathing_host.start_point[1]:02d}", fill=[127, 255, 0, 255])
        modify_draw_command(
            "grid", f"{self.pathing_host.end_point[0]:02d}{self.pathing_host.end_point[1]:02d}", fill=[255, 0, 0, 255])

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
