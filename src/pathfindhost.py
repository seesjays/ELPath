from random import randint
from time import sleep
import math
from queue import PriorityQueue

# 7/20/21 - pathingalgs moved into host, for simplicity's sake,
# and because I don't think generators are the way to go in this case.

class PathfindingHost:
    def __init__(self, sidecellcount):
        self.totalcellcount = sidecellcount*sidecellcount
        self.alg_list = []

        self.grid = []
        for i in range(sidecellcount):
            self.grid.append([])
            for j in range(sidecellcount):
                node = Node((i, j), sidecellcount)
                self.grid[i].append(node)

        self.start_point = (0, 0)
        self.end_point = (39, 39)


    def set_algorithm(self, name):
        pass
    def set_random_data(self):
        pass
    def reset_data(self):
        pass
    def next_step(self):
        pass

class Node:
    def __init__(self, pos, grid_side_length):
        self.x, self.y = pos
        self.state = "EMPTY"
        self.neighbors = []

    def change_color(self):
        pass
    def get_state(self):
        pass
    def draw_self(self):
        pass

