import PySimpleGUI as sg
from commons.utility import pluck
from commons.validators import try_int, try_float
from commons.signalList import getSelectedGraphIndex, addToSelectionList
from signals.signalGenerator import computeSignal
from processing.errorStatistics import calculateErrorStatistics
from processing.conversion import reconstruct
from processing.quantization import quantize
from processing.sampling import sample


gui = [
        [sg.Button('Sample', key='sample', size=(10, 1)), sg.Text('Fp', size=(7, 1)), sg.Input(key='samplingFrequency', size=(10, 10), do_not_clear=True)],
        [sg.Button('Quantize', key='quantize', size=(10, 1)), sg.Text('Levels', size=(7, 1)), sg.Input(key='quantizationSteps', size=(10, 10), do_not_clear=True)],
        [sg.Button('Reconstruct', size=(10, 1), key='reconstruct'), sg.Text('Fe', size=(7, 1)),  sg.Input(key='fe', size=(10, 10), do_not_clear=True), sg.Checkbox('Sinc?', enable_events=True, change_submits=True, key='Sinc?'), sg.Text('Neighbors', size=(7, 1)), sg.Input(key='sincNeighbors', size=(10, 10), do_not_clear=True)],
        [sg.Button('Compute error parameters', key='computeErrors', size=(30,1))],  
]

def onComputeErrorParameters(window, values, storedSignals):
    selectedGraphs = values['selectedGraphs']
    if len(selectedGraphs) != 1:
        sg.Popup('Error!', 'Select 1 graph for error parameters computation!')
        return None

    selectedSignal = storedSignals[getSelectedGraphIndex(selectedGraphs[0])]
    name, x, y, params = pluck(selectedSignal, 'name', 'x', 'y', 'params')

    actualValuesForSignal = computeSignal(selectedSignal, x)

    #test
    newSignal = {
        **selectedSignal,
        'displayName': f"computed: {selectedSignal['displayName']}",
        'y': actualValuesForSignal
    }
    addToSelectionList(window, newSignal, storedSignals)
    #test

    errors = calculateErrorStatistics(selectedSignal['y'], actualValuesForSignal)
    MSE, SNR, PSNR, MD, ENOB = pluck(errors, 'MSE', 'SNR', 'PSNR', 'MD', 'ENOB')

    sg.Popup('Signal properties', f"""
        MSE: {MSE}
        SNR: {SNR}
        PSNR: {PSNR}
        MD: {MD}
        ENOB: {ENOB}
        """)


def onReconstructSignal(window, values, storedSignals):
    selectedGraphs = values['selectedGraphs']
    if len(selectedGraphs) != 1:
        sg.Popup('Error!', 'Select 1 graph to reconstruct!')
        return None

    reconstructed = reconstruct(storedSignals[getSelectedGraphIndex(selectedGraphs[0])], params=values)
    addToSelectionList(window, reconstructed, storedSignals)


def onQuantizeSignal(window, values, storedSignals):
    selectedGraphs = values['selectedGraphs']
    if len(selectedGraphs) != 1:
        sg.Popup('Error!', 'Select 1 graph to quantize!')
        return None

    steps = try_int(values['quantizationSteps'])
    if steps == None:
        sg.Popup('Error!', 'Specify amount of quantization levels!')
        return None
    
    selectedGraph =  storedSignals[getSelectedGraphIndex(selectedGraphs[0])]
    quantized = quantize(selectedGraph, steps)

    addToSelectionList(window, quantized, storedSignals)
    
def onSampleSignal(window, values, storedSignals):
    selectedGraphs = values['selectedGraphs']
    if len(selectedGraphs) != 1:
        sg.Popup('Error!', 'Select 1 graph to sample!')
        return None

    fp = try_float(values['samplingFrequency'])
    if fp == None or fp == 0:
        sg.Popup('Error!', 'Specify correct sampling frequency!')
        return None

    selectedGraph = storedSignals[getSelectedGraphIndex(selectedGraphs[0])]
    sampled = sample(selectedGraph, fp)

    addToSelectionList(window, sampled, storedSignals)

def onChangeReconstructMethod(window, values):
    sinc = values['Sinc?']
    window.FindElement('sincNeighbors').Update(disabled=not sinc, value='')
