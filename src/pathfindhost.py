from random import randint
from time import sleep
import math
import queue

# 7/20/21 - pathingalgs moved into host, for simplicity's sake,
# and because I don't think generators are the way to go in this case.

"""
7/22/21 - Turns out I still want to use generators for this,
it's such an easy way to "pause" execution of an algorithm.
But, it will be different this time: Updating the window will no
longer be the duty of the host's Window. Rather, the host will update
the window, which kind of turns the initial philosophy on its head,
but it's convenient, makes some more sense, and reduces the whole
"how am i gonna make this algorithm into a generator" issue.
That modified version of merge sort from the sorting portion?
That's what drove this decision.
"""

class PathfindingHost:
    def __init__(self, sidecellcount, draw_node_func):
        self.sidecellcount = sidecellcount

        self.grid = []
        for y in range(sidecellcount):
            self.grid.append([])
            for x in range(sidecellcount):
                node = Node((x, y), sidecellcount)
                self.grid[y].append(node)   
        
        self.start_point = (0, 0)
        self.end_point = (39, 39)

        self.start = self.node_from_pos(self.start_point)
        self.end = self.node_from_pos(self.end_point)

        self.start.set_state_start()
        self.end.set_state_end()

        self.draw_node = draw_node_func

        self.alg_list = {
            "Breadth-First Search": (lambda: self.breadthfirst(self.draw_node))
        }
        self.alg_name = "Breadth-First Search"
        self.current_alg = self.alg_list[self.alg_name]

        self.initialized = False


    def node_from_pos(self, pos):
        y = pos[1]
        x = pos[0]

        if 0 <= x < self.sidecellcount and 0 <= y < self.sidecellcount:
            return self.grid[y][x]
        else:
            return None

    def add_start(self, node):
        node.set_state_start()
        self.start_point = (node.x, node.y)
        self.start = node

    def remove_start(self):
        start = self.node_from_pos(self.start_point)
        start.set_state_empty()
        self.start_point = None
        self.start = None


    def add_end(self, node):
        node.set_state_end()
        self.end_point = (node.x, node.y)
        self.end = node

    def remove_end(self):
        end = self.node_from_pos(self.end_point)
        end.set_state_empty()
        self.end_point = None
        self.end = None

    def update_node_neighbors(self, node):
        right = self.node_from_pos((node.x+1, node.y))
        left = self.node_from_pos((node.x-1, node.y))
        up = self.node_from_pos((node.x, node.y+1))
        down = self.node_from_pos((node.x, node.y-1))

        if right is not None:
            node.neighbors.append(right)
        if left is not None:
            node.neighbors.append(left)
        if up is not None:
            node.neighbors.append(up)
        if down is not None:
            node.neighbors.append(down)

    # alg
    def breadthfirst(self, draw_func):
        frontier = queue.Queue()
        frontier.put(self.start)
        reached = set()
        reached.add(self.start)

        yield 1

        while not frontier.empty():
            current = frontier.get()
            current.set_state_open()
            draw_func(current)
            for next in current.neighbors:
                if next not in reached:
                    frontier.put(next)
                    reached.add(next)
                    next.set_state_closed()
                    draw_func(next)
            yield 1

    def initialize_neighbors(self):
        for row in self.grid:
            for node in row:
                self.update_node_neighbors(node)
        self.initialized = True
        self.current_alg = self.current_alg()

    def next_step(self):
        result = next(self.current_alg)
        if not result:
            print(result, 1)
            return False
        else:
            print(result, 2)
            return True
        # Notice that we don't return any actual data here, unlike the sorting next_step
        # We do all the window updating work in the algorithm

class Node:
    def __init__(self, pos, grid_side_length):
        self.x, self.y = pos
        self.state = "EMPTY"
        self.neighbors = []
        self.sidecount = grid_side_length

    def __str__(self):
        return f"{self.state.lower()} node at x {self.x} and y {self.y}"

    def get_state(self):
        return self.state

    def set_state_start(self):
        self.state = "START"
    def set_state_end(self):
        self.state = "END"

    def set_state_open(self):
        self.state = "OPEN"
    def set_state_closed(self):
        self.state = "CLOSE"

    def set_state_path(self):
        self.state = "PATH"

    def set_state_empty(self):
        self.state = "EMPTY"    
    def set_state_barrier(self):
        self.state = "BARR"
