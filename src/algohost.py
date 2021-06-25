from bubbling import bubble
from random import randint
from time import sleep

class AlgorithmHost:
    def __init__(self, data_set=[]):
        self.data_set_size = 30

        self.running = False

        self.current_algorithm = "bubble_sort"

        self.data_x = [i for i in range(self.data_set_size)]
        self.data_y = []

        self.alg_name = "Bubble Sort"
        self.alg_list = {
            "Bubble Sort": (lambda dataset: bubble(self.data_y))
        }

        self.update_callback = None
        if not data_set:
            self.set_random_data()
    
    def sim_change_pause_state(self):
        if self.running:
            self.running = False
        else:
            self.running = True

    def set_algorithm(self, name):
        self.current_algorithm = self.alg_list[name](self.data_y)

    def set_random_data(self):
        self.data_y = [randint(1, self.data_set_size) for i in range(self.data_set_size)]
        self.current_algorithm = self.alg_list[self.alg_name](self.data_y)

    def next_step(self):
        try:
            return next(self.current_algorithm)
        except StopIteration:
            return 1


        
