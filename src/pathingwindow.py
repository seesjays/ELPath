import dearpygui.dearpygui as dpg
from pathfindhost import PathfindingHost
from math import trunc


class PathingWindow:
    def __init__(self, window_tag=None):
        self.window_tag = window_tag
        self.window_size = dpg.get_item_height(
            window_tag) - 16 if window_tag else 800
        self.side_cell_count = 33
        self.cell_size = self.window_size/self.side_cell_count

        self.min_x = 0
        self.min_y = 0
        self.max_x = self.window_size
        self.max_y = self.window_size

        self.pathing_host = PathfindingHost(
            self.side_cell_count, lambda node: self.draw_node(node), self.draw_weights)
        self.colors = {
            "EMPTY": [255, 255, 255],
            "START": [85, 168, 104],
            "END": [196, 78, 82],
            "OPEN": [204, 185, 116],
            "CLOSE": [76, 114, 176],
            "PATH": [129, 114, 179],
            "BARR": [37, 37, 38],
            "SPCL": [221, 132, 82]
        }
        self.message = self.pathing_host.alg_name

        self.drawlist = None
        self.node_grid = {}

        self.clickregistry = None
        self.clickhandler = None

    def change_algorithm(self):
        self.retry()
        self.pathing_host.set_algorithm(dpg.get_value("algorithm_combobox"))
        self.message = self.pathing_host.alg_name

    def change_algorithm(self, alg):
        self.retry()
        self.pathing_host.set_algorithm(alg)
        self.message = self.pathing_host.alg_name

    def draw_node(self, node):
        nodeident = self.node_grid[(node.x, node.y)]

        if node.state == node.altstate:
            dpg.configure_item(nodeident, fill=self.colors[node.state])
        else:
            dpg.configure_item(nodeident, fill=self.colors[node.altstate])

    def draw_weights(self, weightlist):
        # higher weights cost more, so make those less green - increase the tint of the color
        for node in weightlist:
            weightednode = weightlist[node] + 10
            nodeident = self.node_grid[(node.x, node.y)]
            dpg.configure_item(
                nodeident, fill=[weightednode, 255, weightednode, 255])

    def initialize_grid(self):
        self.drawlist = dpg.add_drawlist(parent=self.window_tag,
                                         width=self.window_size+1, height=self.window_size+1, show=True)

        span = 0
        for row in self.pathing_host.grid:
            for node in row:
                nodeident = dpg.draw_rectangle([self.min_x+node.x*self.cell_size, self.min_y+node.y*self.cell_size], [self.min_x+(
                    node.x+1)*self.cell_size, (node.y+1)*self.cell_size], color=self.colors[node.state], fill=self.colors[node.state], parent=self.drawlist)
                self.node_grid[(node.x, node.y)] = nodeident
            span += self.cell_size

        for col in range(len(self.pathing_host.grid)):
            dpg.draw_rectangle([self.min_x+col*self.cell_size, 0], [self.min_x+(
                    col+1)*self.cell_size, span], color=[0, 0, 0, 255], thickness=2, fill=[0, 0, 0, 0], parent=self.drawlist)
            
            dpg.draw_rectangle([0, self.min_y+col*self.cell_size], [span, self.min_y+(
                    col+1)*self.cell_size], color=[0, 0, 0, 255], thickness=2, fill=[0, 0, 0, 0], parent=self.drawlist)

        dpg.draw_line([0, 0], [0, self.window_size], color=[
                      0, 0, 0], thickness=4, parent=self.drawlist)
        dpg.draw_line([0, 0], [self.window_size, 0], color=[
                      0, 0, 0], thickness=4, parent=self.drawlist)
        dpg.draw_line([self.window_size, self.window_size], [
                      0, self.window_size], color=[0, 0, 0], thickness=4, parent=self.drawlist)
        dpg.draw_line([self.window_size, self.window_size], [
                      self.window_size, 0], color=[0, 0, 0], thickness=4, parent=self.drawlist)  
        
        with dpg.handler_registry() as self.clickregistry:
            self.clickhandler = dpg.add_mouse_down_handler(
                callback=self.cell_clicked)



    def change_side_len(self, changeamnt):
        if (changeamnt < 0 and self.side_cell_count - abs(changeamnt) < 9) or (changeamnt > 0 and self.side_cell_count + abs(changeamnt) > 60):
            return False

        self.side_cell_count += changeamnt
        self.cell_size = self.window_size/self.side_cell_count
        return True

    def grow_maze(self):
        if not self.change_side_len(3):
            return

        self.reset()

    def shrink_maze(self):
        if not self.change_side_len(-3):
            return

        self.reset()

    def cell_clicked(self):
        try:
            if not self.is_initial():
                return
        except AttributeError:
            return

        # Preventing click detection when outside of window
        genpos = dpg.get_mouse_pos()
        genpos[1] -= 15  # account for window padding

        if (genpos[1] > self.max_y or genpos[1] < self.min_y or genpos[0] < 0 or genpos[0] > self.max_x or dpg.get_active_window() != self.window_tag):
            return

        pos = dpg.get_drawing_mouse_pos()

        within_x = pos[0] >= self.min_x and pos[0] <= self.max_x
        within_y = pos[1] >= self.min_y and pos[1] <= self.max_y

        x_cell = trunc(pos[0]//self.cell_size)
        y_cell = trunc(pos[1]//self.cell_size)

        clearing = True if (dpg.is_mouse_button_down(
            1)) else False  # True if right clicking

        if (within_x and within_y):
            node = self.pathing_host.node_from_pos((x_cell, y_cell))

            if node is None:
                return

            tempstate = node.state
            if clearing:
                if (tempstate == "BARR"):
                    node.set_state_empty()
                if (tempstate == "START"):
                    self.pathing_host.remove_start()
                if (tempstate == "END"):
                    self.pathing_host.remove_end()

            else:
                if (tempstate == "EMPTY"):
                    node.set_state_barrier()
                    if (self.pathing_host.start_point is None):
                        self.pathing_host.add_start(node)
                    elif (self.pathing_host.end_point is None):
                        self.pathing_host.add_end(node)

            self.draw_node(node)

    # interfacing with ELPath
    def next_step(self):
        if not self.pathing_host.start or not self.pathing_host.end:
            return False

        if not self.pathing_host.initialized:
            self.pathing_host.initialize_neighbors()

        result = self.pathing_host.next_step()

        opensquares = (self.side_cell_count *
                       self.side_cell_count-self.pathing_host.barr_count)

        if result:
            self.message = f"{self.pathing_host.alg_name} ({self.side_cell_count}x{self.side_cell_count}) "
            self.message += f"Step {self.pathing_host.step_counter}:\n{result}\n"
            self.message += f"Nodes visited: {self.pathing_host.nodes_found} / {opensquares}"

        else:
            self.message = f"{self.pathing_host.alg_name} ({self.side_cell_count}x{self.side_cell_count}): Complete in {self.pathing_host.step_counter} steps.\n"
            self.message += f"{self.pathing_host.nodes_found} / {opensquares} nodes visited in total. ({((self.pathing_host.nodes_found / opensquares) * 100):.2f}%)\n"
            self.message += f"Path of length {self.pathing_host.path_length} traced."

        return result

    def reset(self):
        curr_alg_name = self.pathing_host.alg_name
        dpg.delete_item(self.drawlist, children_only=False)
        self.pathing_host = PathfindingHost(
            self.side_cell_count, lambda node: self.draw_node(node), self.draw_weights, algorithm=curr_alg_name)
        self.initialize_grid()

    def retry(self):
        self.pathing_host.retry_maze()

    def randmaze(self):
        self.pathing_host.rand_maze()  # drawing is handled in-alg

    def unmount(self):
        dpg.delete_item(self.drawlist, children_only=False)
        dpg.delete_item(self.clickregistry, children_only=False)
        self.pathing_host = None

    def current_alg(self):
        return self.pathing_host.alg_name

    def is_initial(self):
        if self.pathing_host.step_counter == 0:
            return True
        return False
