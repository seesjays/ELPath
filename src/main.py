from dearpygui.core import *
from dearpygui.simple import *
from consts import *
import initialwindows
from algowindow import AlgorithmWindow


initialwindows.initialize_ELPath()

algorithms = AlgorithmWindow()

algorithms.AlgorithmController.set_algorithm("Bubble Sort")
initialwindows.link_buttons(algorithms.start_sim, algorithms.AlgorithmController.next_step, algorithms.new_dataset)
start_dearpygui(primary_window="ELPath") 


