import dearpygui.dearpygui as dpg
from ELPath import ELPath

dpg.create_context()

ELPath = ELPath()


ELPath.viewport_config()


dpg.start_dearpygui()
