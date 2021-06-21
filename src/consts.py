# For maximum compat (and because I don't see any real reason not to,) the window is designed to fit in smaller screens (laptops, etc)
WINDOW_WIDTH, WINDOW_HEIGHT = 1200, 900
FILL_WIDTH = WINDOW_WIDTH-15

CHILD_WINDOW_FILL_PARAMS = {
    "width": FILL_WIDTH, 
    "no_resize": True, 
    "no_collapse": True, 
    "no_close": True, 
    "no_move": True
}

UNINTERACTIVE_GRAPH_PARAMS= {
    "xaxis_no_tick_labels": True, 
    "xaxis_no_gridlines": True, 
    "x_axis_name": "", 
    "xaxis_no_tick_marks": True,
    "yaxis_no_tick_labels": True, 
    "yaxis_no_gridlines": True, 
    "y_axis_name": "", 
    "yaxis_no_tick_marks": True,
    "no_box_select": True,
    "xaxis_lock_min": True,
    "xaxis_lock_max": True,
    "yaxis_lock_min": True,
    "yaxis_lock_max": True,
    "no_legend": True,
    "no_mouse_pos": True,
}