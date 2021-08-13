import dearpygui.dearpygui as dpg
from consts import *
from ELPath import *

dpg.setup_registries()

ELPath = ELPath()

ELPath.viewport_config()

dpg.start_dearpygui()
