import plotly.offline as py
import plotly.graph_objs as go
import easygui as gui
import numpy as np
import signalGenerators as sgen
from constants import sin_fields, noise_fields, signals
from validators import validate_input, try_parse_field
 
values = []
while 1:
    choice = gui.choicebox(msg='Choose a signal to generate', choices=signals.keys())
    fields = signals[choice]['fields']

    values = gui.multenterbox(fields=fields, values=values)
    
    err_msg = validate_input(values, fields)
    if err_msg != "":
        gui.msgbox(err_msg, 'Error!')
        continue

    param_values = {}
    for i in range(len(values)):
        param_values[fields[i]] = try_parse_field(fields[i])(values[i].strip().strip('"'))
 
    random_x, random_y = signals[choice]['fn'](**param_values)
 
    # Create a trace
    trace = go.Scatter(
        x = random_x,
        y = random_y
    )
 
    data = [trace]
 
    py.plot(data, filename='basic-line')