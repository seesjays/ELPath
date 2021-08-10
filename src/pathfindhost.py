from random import randint, choice
from time import sleep
import math
import queue
from collections import deque
from typing import Type


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
    def __init__(self, sidecellcount, draw_node_func, draw_weights_func, algorithm="Breadth-First Search"):
        self.sidecellcount = sidecellcount

        self.grid = []
        for y in range(sidecellcount):
            self.grid.append([])
            for x in range(sidecellcount):
                node = Node((x, y), sidecellcount)
                self.grid[y].append(node)

        self.start_point = (0, 0)
        self.end_point = (sidecellcount-1, sidecellcount-1)

        self.start = self.node_from_pos(self.start_point)
        self.end = self.node_from_pos(self.end_point)

        self.start.set_state_start()
        self.end.set_state_end()

        self.draw_node = draw_node_func
        self.draw_weights = draw_weights_func

        self.alg_list = {
            "Breadth-First Search": (lambda: self.breadthfirst(self.draw_node)),
            "Depth-First Search": (lambda: self.depthfirst(self.draw_node)),
            "Dijkstra's Algorithm": (lambda: self.dijkstras(self.draw_node)),
            "A* Algorithm": (lambda: self.astar(self.draw_node)),
        }
        self.alg_name = algorithm
        self.current_algorithm = self.alg_list[self.alg_name]

        self.initialized = False

        # Info
        self.step_counter = 0
        self.path_length = 0
        self.nodes_visited = 0
        self.nodes_detected = 0

    def set_algorithm(self, name):
        self.alg_name = name
        self.step_counter = 0
        self.current_algorithm = self.alg_list[name]

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
        self.draw_node(self.start)

    def remove_start(self):
        start = self.node_from_pos(self.start_point)
        start.set_state_empty()
        self.draw_node(start)
        self.start_point = None
        self.start = None

    def add_end(self, node):
        node.set_state_end()
        self.end_point = (node.x, node.y)
        self.end = node
        self.draw_node(self.end)

    def remove_end(self):
        end = self.node_from_pos(self.end_point)
        end.set_state_empty()
        self.draw_node(end)
        self.end_point = None
        self.end = None

    def update_node_neighbors(self, node):
        right = self.node_from_pos((node.x+1, node.y))
        left = self.node_from_pos((node.x-1, node.y))
        up = self.node_from_pos((node.x, node.y+1))
        down = self.node_from_pos((node.x, node.y-1))

        if right is not None and right.state != "BARR":
            node.neighbors.append(right)
        if left is not None and left.state != "BARR":
            node.neighbors.append(left)
        if up is not None and up.state != "BARR":
            node.neighbors.append(up)
        if down is not None and down.state != "BARR":
            node.neighbors.append(down)

    def cost(self, node, node2):
        return 1

    def initialize_neighbors(self):
        for row in self.grid:
            for node in row:
                node.origstate = node.state
                self.update_node_neighbors(node)
        self.initialized = True
        self.current_algorithm = self.current_algorithm()

    def retry_maze(self):
        self.step_counter = 0

        for row in self.grid:
            for node in row:
                node.neighbors = []
                node.state = node.altstate = node.origstate
                self.draw_node(node)

        # start/end not placed
        try:
            self.add_start(self.node_from_pos(self.start_point))
            self.add_end(self.node_from_pos(self.end_point))
        except TypeError:  # start/end not initialized
            self.start_point = (0, 0)
            self.end_point = (self.sidecellcount-1, self.sidecellcount-1)

            self.start = self.node_from_pos(self.start_point)
            self.end = self.node_from_pos(self.end_point)

            self.add_start(self.node_from_pos(self.start_point))
            self.add_end(self.node_from_pos(self.end_point))

        self.initialized = False
        self.current_algorithm = self.alg_list[self.alg_name]

    def next_step(self):
        try:
            self.step_counter += 1
            return next(self.current_algorithm)
        except StopIteration:
            self.step_counter -= 1
            return False
        # Notice that we don't return any actual data here, unlike the sorting next_step
        # We do all the window updating work in the algorithm

    def rand_maze(self):
        def emptys_at_dist_2(node):
            right = self.node_from_pos((node.x+2, node.y))
            left = self.node_from_pos((node.x-2, node.y))
            up = self.node_from_pos((node.x, node.y+2))
            down = self.node_from_pos((node.x, node.y-2))

            outlist = []
            if right is not None and right.state == "EMPTY":
                outlist.append(right)
            if left is not None and left.state == "EMPTY":
                outlist.append(left)
            if up is not None and up.state == "EMPTY":
                outlist.append(up)
            if down is not None and down.state == "EMPTY":
                outlist.append(down)

            return outlist
        if self.start is not None:
            self.remove_start()
        if self.end is not None:
            self.remove_end()

        for row in self.grid:
            for node in row:
                node.set_state_barrier()
                self.draw_node(node)

        open_nodes = []
        for i in range(1, len(self.grid)-1):
            for j in range(1, len(self.grid)-1):
                node = self.grid[i][j]
                if i % 2 != 0 and j % 2 != 0:
                    node.set_state_empty()
                    self.draw_node(node)
                    open_nodes.append(node)

        visited = set()
        stack = deque()

        startcell = choice(open_nodes)
        visited.add(startcell)
        stack.append(startcell)

        self.add_start(startcell)

        sleep_tracker = 0

        while len(stack) > 0:
            current_cell = stack.pop()
            neighbors = emptys_at_dist_2(current_cell)

            prevstate = current_cell.state
            current_cell.set_state_closed()
            self.draw_node(current_cell)

            for neighbor in neighbors:
                if neighbor not in visited:
                    stack.append(current_cell)

                    unvis = choice(neighbors)
                    while (unvis in visited):
                        unvis = choice(neighbors)

                    between = ((unvis.x + current_cell.x)//2,
                               (unvis.y + current_cell.y)//2)
                    between = self.node_from_pos(between)

                    between.set_state_empty()
                    self.draw_node(between)

                    visited.add(unvis)
                    stack.append(unvis)
                    break

            sleep_tracker += 1
            if sleep_tracker == 10:
                sleep_tracker = 0
                # sleep(0.1)

            current_cell.set_state(prevstate)
            self.draw_node(current_cell)
        self.add_end(choice(open_nodes))

    def rand_weights(self):
        # Generates a random list of weights for each node - to help along Dijkstras's
        weightlevels = [20, 200]
        weightlist = {node: choice(weightlevels)
                      for row in self.grid for node in row if
                      node.state != "START" and node.state != "END" and node.state != "BARR"}
        weightlist[self.start] = 0
        weightlist[self.end] = 0

        return weightlist


    def reset_info(self):
        self.step_counter = 0
        self.path_length = 0
        self.nodes_visited = 0
        self.nodes_detected = 0

    # algs

    def tracepath(self, draw_func, came_from):
        current = self.end
        path = []
        while current != self.start:
            path.append(current)
            current.set_state_path()
            draw_func(current)
            current = came_from[current]

            self.start.set_alt_state("START")
            draw_func(self.start)
            self.end.set_alt_state("END")
            draw_func(self.end)
            yield 2
      
    def breadthfirst(self, draw_func):
        self.reset_info()

        frontier = queue.Queue()
        frontier.put(self.start)
        came_from = dict()
        came_from[self.start] = None

        while not frontier.empty():
            current = frontier.get()
            current.set_state_open()
            current.set_alt_state("SPCL")
            draw_func(current)

            if current == self.end:
                self.start.set_alt_state("START")
                draw_func(self.start)
                self.end.set_alt_state("END")
                draw_func(self.end)
                break

            for nxt in current.neighbors:
                if nxt not in came_from:
                    nxt.set_state_open()
                    frontier.put(nxt)
                    came_from[nxt] = current
                draw_func(nxt)
            yield 1

            current.reset_alt_state()
            current.set_state_closed()
            draw_func(current)

            self.start.set_alt_state("START")
            draw_func(self.start)
            self.end.set_alt_state("END")
            draw_func(self.end)

        for stepback in self.tracepath(draw_func, came_from):
            yield "Retracing Path"

    def depthfirst(self, draw_func):
        self.reset_info()

        stack = []
        discovered = set()
        stack.append(self.start)
        came_from = dict()

        while len(stack) > 0:
            current = stack.pop()
            current.set_alt_state("SPCL")
            draw_func(current)

            if current == self.end:
                self.start.set_alt_state("START")
                draw_func(self.start)
                self.end.set_alt_state("END")
                draw_func(self.end)
                break

            if current not in discovered:
                discovered.add(current)
                for neighbor in current.neighbors:
                    if neighbor not in discovered:
                        stack.append(neighbor)
                        neighbor.set_state_open()
                        draw_func(neighbor)
                        if neighbor not in came_from:
                            came_from[neighbor] = current

                    self.start.set_alt_state("START")
                    draw_func(self.start)
                    self.end.set_alt_state("END")
                    draw_func(self.end)

                yield f"Examining neighbors around node at ({current.x}, {current.y})"

            current.set_state_closed()
            draw_func(current)
        
        for stepback in self.tracepath(draw_func, came_from):
            yield "Retracing Path"

    def dijkstras(self, draw_func):
        self.reset_info()

        weights = self.rand_weights()
        self.draw_weights(weights)

        vertset = []
        distances = {}
        came_from = {}

        for row in self.grid:
            for node in row:
                distances[node] = float("inf")
                came_from[node] = None
                vertset.append(node)

        initial_node = self.start
        distances[initial_node] = 0

        while len(vertset) > 0:
            tempmin = None
            lowest = None
            for thing in vertset:
                if tempmin is None or distances[thing] < tempmin:
                    tempmin = distances[thing]
                    lowest = thing

            vertset.remove(lowest)
            lowest.set_alt_state("SPCL")
            draw_func(lowest)

            if lowest == self.end:
                break

            for neighbor in lowest.neighbors:
                if neighbor in vertset:
                    alt = distances[lowest] + weights[neighbor]
                    if alt < distances[neighbor]:
                        distances[neighbor] = alt
                        came_from[neighbor] = lowest
                    neighbor.set_state_open()
                    draw_func(neighbor)

                self.start.set_alt_state("START")
                draw_func(self.start)
                self.end.set_alt_state("END")
                draw_func(self.end)
            yield 1

            lowest.set_state_closed()
            draw_func(lowest)

        for stepback in self.tracepath(draw_func, came_from):
            yield "Retracing Path"

    def astar(self, draw_func):
        self.reset_info()
        
        count = 0
        open_set = queue.PriorityQueue()
        open_set.put((0, count, self.start))
        came_from = {}
        g_score = {spot: float("inf") for row in self.grid for spot in row}
        g_score[self.start] = 0
        f_score = {spot: float("inf") for row in self.grid for spot in row}
        f_score[self.start] = self.manhattanheur(
            (self.start.x, self.start.y), (self.end.x, self.end.y))

        open_set_hash = {self.start}

        while not open_set.empty():
            current = open_set.get()[2]
            current.set_alt_state("SPCL")
            draw_func(current)
            open_set_hash.remove(current)

            if current == self.end:
                break

            for neighbor in current.neighbors:
                temp_g_score = g_score[current] + 1
                if temp_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = temp_g_score
                    f_score[neighbor] = temp_g_score + self.manhattanheur(
                        (neighbor.x, neighbor.y), (self.end.x, self.end.y))
                    if neighbor not in open_set_hash:
                        count += 1
                        open_set.put((f_score[neighbor], count, neighbor))
                        open_set_hash.add(neighbor)
                        neighbor.set_state_open()
                        draw_func(neighbor)
                self.start.set_alt_state("START")
                draw_func(self.start)
                self.end.set_alt_state("END")
                draw_func(self.end)
            yield 1

            if current != self.start:
                current.set_state_closed()
                draw_func(current)
            
        for stepback in self.tracepath(draw_func, came_from):
            yield "Retracing Path"

    def manhattanheur(self, a, b):
        x1, y1 = a
        x2, y2 = b
        return abs(x1 - x2) + abs(y1 - y2)


class Node:
    def __init__(self, pos, grid_side_length):
        self.x, self.y = pos
        self.state = "EMPTY"
        self.altstate = "EMPTY"
        self.origstate = "EMPTY"
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

    def set_state(self, state):
        self.altstate = self.state = state

    def set_state_start(self):
        self.origstate = self.altstate = self.state = "START"

    def set_state_end(self):
        self.origstate = self.altstate = self.state = "END"

    def set_state_open(self):
        self.altstate = self.state = "OPEN"

    def set_state_closed(self):
        self.altstate = self.state = "CLOSE"

    def set_state_path(self):
        self.altstate = self.state = "PATH"

    def set_state_empty(self):
        self.origstate = self.altstate = self.state = "EMPTY"

    def set_state_barrier(self):
        self.origstate = self.altstate = self.state = "BARR"

    def set_alt_state(self, state):
        self.altstate = state

    def reset_alt_state(self):
        self.altstate = self.state

    def __lt__(a, b):
        return (a.x, a.y) > (b.x, b.y)
