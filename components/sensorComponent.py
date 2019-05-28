import PySimpleGUI as sg
from commons.utility import pluck
from commons.signalList import getSelectedGraphIndex
from commons.validators import try_int, try_float
import signals.operations as ops
from signals.signalGenerator import create_signal_with_metadata
import convolution.correlationStrategies as cor
import convolution.convolutionStrategies as conv
import components.signalComponent as signalComponent

import plotly.offline as py
import plotly.graph_objs as go

import numpy as np


gui = [
    [sg.Text("Sensor time unit", size=(20, 1)), sg.InputText(key="stu", do_not_clear=True)],
    [sg.Text("Object velocity", size=(20, 1)), sg.InputText(key="ov", do_not_clear=True)],
    [sg.Text("Signal velocity", size=(20, 1)), sg.InputText(key="sv", do_not_clear=True)],
    [sg.Text("Signal period", size=(20, 1)), sg.InputText(key="sp", do_not_clear=True)],
    [sg.Text("Signal sampling frequency", size=(20, 1)), sg.InputText(key="ssf", do_not_clear=True)],
    [sg.Text("Buffer length", size=(20, 1)), sg.InputText(key="bl", do_not_clear=True)],
    [sg.Text("Raport period", size=(20, 1)), sg.InputText(key="rp", do_not_clear=True)],
    [sg.Text("Simulation length", size=(20, 1)), sg.InputText(key="sim_len", do_not_clear=True)],
    [sg.Button("Simulate", key="simulate")]
]

def onSimulate(window, values, storedSignals):
    sim_params = pluck(values, 'stu', 'ov', 'sv', 'sp', 'ssf', 'bl', 'rp', 'sim_len')
    stu, object_v, signal_v, signal_T, signal_sampling_freq, buffer_len, report_T, simulation_length = [try_float(param) for param in sim_params]
    buffer_len, report_T = int(buffer_len), int(report_T)
    
    lesser_signal_periods_per_signal_T = 0.05
    lesser_signal_T = signal_T * lesser_signal_periods_per_signal_T
    # lesser_signal_T = lesser_signal_T * 1.1

    lesser_signal_T = 0.00636942675
    signal_T = 0.05263157894

    SIGNAL_LENGTH = 100
    param_values = {
        'A': 1,
        't1': 0,
        'T': signal_T,
        'd': SIGNAL_LENGTH,
        'fp': signal_sampling_freq
    }
    lesser_param_values = { **param_values, 'T': lesser_signal_T }

    first = create_signal_with_metadata('sin', param_values)
    second = create_signal_with_metadata('sin', lesser_param_values)

    probing_signal = ops.applyOperation("+", first, second)
    probing_values = probing_signal['y']

    time = .0

    outgoing_buffer = [0] * buffer_len
    incoming_buffer = [0] * buffer_len

    object_real_distance = 100

    samples_per_stu = signal_sampling_freq * stu

    i = buffer_len

    distances = []
    r_distances = []
    correlation_serieses = []
    correlation = []
    print('x')
    while time < simulation_length:
        first_sample_index = int((i - buffer_len) * samples_per_stu)
        outgoing_buffer = probing_values[first_sample_index:first_sample_index + buffer_len] # jak nizej

        delay_samples = int(abs(object_real_distance) / signal_v * signal_sampling_freq * 2)

        incoming_buffer = probing_values[first_sample_index + delay_samples: first_sample_index + buffer_len + delay_samples] #jak wypelniac
        

        print(f"{first_sample_index} -- {probing_values[first_sample_index + buffer_len]}")
        print(f"{delay_samples} -- {probing_values[first_sample_index + delay_samples]}")

        if ((i - buffer_len) % report_T == 0 and i > buffer_len):
            correlation = cor.convCorrelation(outgoing_buffer, incoming_buffer)
            correlation_half = correlation[int(len(correlation)/2):]
            if correlation_half.size == 0: break
            offset = np.argmax(correlation_half)
            distance = offset * signal_v / signal_sampling_freq / 2
            distances.append(distance)
            r_distances.append(object_real_distance)
            print(f"distance: {object_real_distance}  calculated: {distance}  offset {offset}")
            if(i - buffer_len) % report_T * 5: correlation_serieses.append(correlation)

        object_real_distance -= object_v * stu
        time += stu
        i+=1
        print(f"time: {time}")
    show([distances, r_distances, correlation])

def show(values):
    
    layout = signalComponent.plotly_layout
    data = []
    for correlation in values:
        data.append(go.Scatter(
            x=list(range(len(correlation))),
            y=correlation,
            mode="markers" if True else 'lines',
        ))

    figure = go.Figure(data=data, layout=layout)
    
    py.plot(figure, filename='graph')


def onConvolveSignals(window, values, storedSignals):
    first, second = ops.extractSignalsForOperation(values, storedSignals)
    if first == None: return
    strat = values["convolution_strategy"]
    conv_values = []
    if strat == 'numpy':
        conv_values = conv.numpyConvolve(first['y'], second['y'])
    elif strat == 'fft':
        conv_values = conv.scipyConvolve(first['y'], second['y'])
    else:
        conv_values = conv.naiveConvolve(first['y'], second['y'])
    show([conv_values])

def onCorrelateSignals(window, values, storedSignals):
    first, second = ops.extractSignalsForOperation(values, storedSignals)
    if first == None: return
    strat = values["convolution_strategy"]
    conv_values = []
    if strat == 'normal':
        conv_values = cor.correlation(first['y'], second['y'])
    else:
        conv_values = cor.convCorrelation(first['y'], second['y'])
    show([conv_values])
