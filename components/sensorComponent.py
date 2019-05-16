import PySimpleGUI as sg
from commons.utility import pluck
from commons.signalList import getSelectedGraphIndex
from commons.validators import try_int, try_float


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
    
    selectedSignal = values['selectedGraphs']
    if len(selectedSignal) != 1:
        sg.Popup("Error!", "You have to select 1 signal to save.")
        return

    # stu = try_float(stu)
    stu, object_v, signal_v, signal_T, signal_sampling_freq, buffer_len, report_T, simulation_length = [try_float(param) for param in sim_params]
    buffer_len, report_T = int(buffer_len), int(report_T)
    print(object_v)
    probing_signal = storedSignals[getSelectedGraphIndex(selectedSignal[0])]

    lesser_signal_periods_per_signal_T = 0.01
    lesser_signal_T = signal_T * lesser_signal_periods_per_signal_T

    time = .0

    outgoing_buffer = [0] * buffer_len
    incoming_buffer = [0] * buffer_len

    object_real_distance = 10

    samples_per_stu = signal_sampling_freq * stu

    i = buffer_len
    while time < simulation_length:
        outgoing_buffer = probing_signal['y'][i * samples_per_stu - buffer_len:i * samples_per_stu] # jak nizej

        delay_samples = object_real_distance / signal_v * signal_sampling_freq * 2

        incoming_buffer = probing_signal['y'] #jak wypelniac
        
        

        if (i % report_T == 0):
            print(outgoing_buffer)

        object_real_distance -= object_v * stu
        time += stu
        i+=1
