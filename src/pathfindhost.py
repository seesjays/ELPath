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

        if right is not None and right.state is not "BARR":
            node.neighbors.append(right)
        if left is not None and left.state is not "BARR":
            node.neighbors.append(left)
        if up is not None and up.state is not "BARR":
            node.neighbors.append(up)
        if down is not None and down.state is not "BARR":
            node.neighbors.append(down)

    # alg
    def breadthfirst(self, draw_func):
        frontier = queue.Queue()
        frontier.put(self.start)
        came_from = dict()
        came_from[self.start] = None

        while not frontier.empty():
            current = frontier.get()

            if current == self.end:
                self.start.set_alt_state("START")
                draw_func(self.start)
                self.end.set_alt_state("END")
                draw_func(self.end)
                break

            current.set_state_open()
            draw_func(current)
            for nxt in current.neighbors:
                if nxt not in came_from:
                    frontier.put(nxt)
                    came_from[nxt] = current
                    nxt.set_state_closed()
                    draw_func(nxt)
                    
                self.start.set_alt_state("START")
                draw_func(self.start)
                self.end.set_alt_state("END")
                draw_func(self.end)

                     
            yield 1

        print("path found")
        current = self.end
        path = []
        while current != self.start: 
            print("finding")
            path.append(current)
            current.set_state_path()
            draw_func(current)
            current = came_from[current]

            self.start.set_alt_state("START")
            draw_func(self.start)
            self.end.set_alt_state("END")
            draw_func(self.end)
            yield 2

    def initialize_neighbors(self):
        for row in self.grid:
            for node in row:
                self.update_node_neighbors(node)
        self.initialized = True
        self.current_alg = self.current_alg()

    def next_step(self):
        result = next(self.current_alg)
        if not result:
            return False
        else:
            return True
        # Notice that we don't return any actual data here, unlike the sorting next_step
        # We do all the window updating work in the algorithm

class Node:
    def __init__(self, pos, grid_side_length):
        self.x, self.y = pos
        self.state = "EMPTY"
        self.altstate = "EMPTY"
        # altstate is a way to keep nodes from changing color when they're drawn
        # For example, it would be reasonable to have the start node always be green,
        # even when added to the closed set of an algorithm.
        # Thus, in such cases, it makes sense to maintain the actual state
        # but use altstate as a facade of sorts, to clearly visualize what's necessary.
    
        self.neighbors = []
        self.sidecount = grid_side_length

    def __str__(self):
        return f"{self.state.lower()} node at x {self.x} and y {self.y}"

    def get_state(self):
        return self.state

    def set_state_start(self):
        self.altstate = self.state = "START"
    def set_state_end(self):
        self.altstate = self.state = "END"

    def set_state_open(self):
        self.altstate = self.state = "OPEN"
    def set_state_closed(self):
        self.altstate = self.state = "CLOSE"

    def set_state_path(self):
        self.altstate = self.state = "PATH"

    def set_state_empty(self):
        self.altstate = self.state = "EMPTY"    
    def set_state_barrier(self):
        self.altstate = self.state = "BARR"

    def set_alt_state(self, state):
        self.altstate = state
