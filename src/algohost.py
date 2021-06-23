from bubbling import bubble
from random import randint
from time import sleep

class AlgorithmHost:
    def __init__(self, dataUpdateCallback, data_set=[]):
        self.data_set_size = 30

        self.running = False
        self.step_sleep = 0.05

        self.current_algorithm = None

        self.data_x = [i for i in range(self.data_set_size)]
        self.data_y = []

        self.alg_name = "Bubble Sort"
        self.alg_list = {
            "Bubble Sort": (lambda dataset: bubble(self.data_y))
        }

        self.update_callback = dataUpdateCallback
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
            self.update_callback(next(self.current_algorithm))
        except StopIteration:
            self.update_callback(1)

    def change_sim_state(self):
        for i in self.current_algorithm:
            self.update_callback(i)
            sleep(self.step_sleep)
        self.update_callback(1)

        
