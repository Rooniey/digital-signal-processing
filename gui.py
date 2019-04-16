import PySimpleGUI as sg
import plotly.offline as py
import plotly.graph_objs as go
import json
import pandas as pd

import operations as ops
from statistics import calculateStatistics
from helpers import getSelectedGraphIndex
import fileOperations as fileOps 
from constants import signals, allFields
from helpers import getSelectedGraphIndex
from validators import validate_input, try_int, try_float
from signalGenerator import generate_signal
from processing.quantization import quantize
from processing.sampling import sample 
from processing.conversion import reconstruct
from processing.errorStatistics import calculateErrorStatistics
from utility import pluck

inputFields = map(lambda fieldName: [sg.Text(fieldName, size=(3, 1)), sg.InputText(key=fieldName, do_not_clear=True)], allFields)

column1 = sg.Column([
        [sg.InputCombo(values=list(signals.keys()), change_submits=True, key="signalType", readonly=True)],
        *inputFields,
        [
            sg.Button('Generate signal', key="generateSignal"), 
            sg.Button('Show', key="showSignal"), 
        ],
        [
            sg.Button('Histogram', key="showHistogram"),
            sg.Text('Ranges count: '),
            sg.Slider(range=(5,20), default_value=15, size=(10,10), orientation='horizontal', font=('Helvetica', 7), key="ranges"),
            sg.Button('SignalProperties', key="showSignalProperties"),
        ],
        [
            sg.Listbox(values=[], select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE, size=(60, 10), key="selectedGraphs"), 
            sg.Button('Remove signal/s', key='removeSignal'), 
        ],
        [sg.Button('+'), sg.Button('—'), sg.Button('*'), sg.Button('/')],
        [
            sg.Input(key='readFile', change_submits=True, visible=False),
            sg.FileBrowse('Read file',  target="readFile", change_submits=True),
            sg.Input(key='saveFile', change_submits=True, visible=False),
            sg.FileSaveAs('Write file', target='saveFile', change_submits=True, file_types=(("Text files", "*.txt"),("Binary files", "*.bin"))),
            sg.Checkbox('Save to binary', key='saveToBin')
        ]
])

column2 = sg.Column([
    [sg.Button('Sample', key='sample', size=(10, 1)), sg.Text('Fp', size=(7, 1)), sg.Input(key='samplingFrequency', size=(10, 10), do_not_clear=True)],
    [sg.Button('Quantize', key='quantize', size=(10, 1)), sg.Text('Levels', size=(7, 1)), sg.Input(key='quantizationSteps', size=(10, 10), do_not_clear=True)],
    [sg.Button('Reconstruct', size=(10, 1), key='reconstruct'), sg.Text('Fe', size=(7, 1)),  sg.Input(key='fe', size=(10, 10), do_not_clear=True), sg.Checkbox('Sinc?', enable_events=True, change_submits=True, key='Sinc?'), sg.Text('Neighbors', size=(7, 1)), sg.Input(key='sincNeighbors', size=(10, 10), do_not_clear=True)],
    [sg.Button('Compute error parameters', key='computeErrors', size=(30,10), pad=(100,100))]
])

layout = [[column1, column2]]

def onComputeErrorParameters(window, values, storedSignals):
    selectedGraphs = values['selectedGraphs']
    if len(selectedGraphs) != 1:
        sg.Popup('Error!', 'Select 1 graph for error parameters computation!')
        return None

    selectedSignal = storedSignals[getSelectedGraphIndex(selectedGraphs[0])]
    name, x, y, params = pluck(selectedSignal, 'name', 'x', 'y', 'params')

    actualValuesForSignal = ops.computeSignal(selectedSignal, x)

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
        sg.Popup('Error!', 'Select 1 graph to sample!')
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

def onSignalProperties(window, selectedSignals, storedSignals):
    if(len(selectedSignals) != 1):
        sg.Popup('Error!', "Select single signal")
    else:
        selectedSignal = storedSignals[getSelectedGraphIndex(selectedSignals[0])]
        data = calculateStatistics(selectedSignal)
        sg.Popup('Signal properties', f"""
        Average value: {data['average']}
        Average absolute value: {data['averageAbsolute']}
        Average power: {data['averagePower']}
        Standard deviation: {data['standardDeviation']}
        Effective value: {data['effectiveValue']}
        """)

def onSubtractSignals(window, values, storedSignals):
    first, second = ops.extractSignalsForOperation(values, storedSignals)
    if first == None: return
    newSignal = ops.applyOperation("-", first, second)
    if(newSignal != None):
        addToSelectionList(window, newSignal, storedSignals)

def onAddSignals(window, values, storedSignals):
    first, second = ops.extractSignalsForOperation(values, storedSignals)
    if first == None: return
    newSignal = ops.applyOperation("+", first, second)
    if(newSignal != None):
        addToSelectionList(window, newSignal, storedSignals)

def onMultiplySignals(window, values, storedSignals):
    first, second = ops.extractSignalsForOperation(values, storedSignals)
    if first == None: return
    newSignal = ops.applyOperation("*", first, second)
    if(newSignal != None):
        addToSelectionList(window, newSignal, storedSignals)

def onDivideSignals(window, values, storedSignals):
    first, second = ops.extractSignalsForOperation(values, storedSignals)
    if first == None: return
    newSignal = ops.applyOperation("/", first, second)
    if(newSignal != None):
        addToSelectionList(window, newSignal, storedSignals)

def initialize_inputs(window, initialSignalType):
    initialSignal = signals[initialSignalType]
    window.FindElement('signalType').Update(value = initialSignalType)
    for field in allFields:
        if field not in initialSignal['fields']:
            window.FindElement(field).Update(disabled=True)
    window.FindElement('sincNeighbors').Update(disabled=True)

def onSignalTypeChange(window, signalType, prevSignalType):
    used = signals[signalType]['fields']  
    previouslyUsed = signals[prevSignalType]['fields']  
    for x in used:
        if x not in previouslyUsed:
            window.FindElement(x).Update(disabled=False, value = '')

    for x in previouslyUsed:
        if x not in used:
            window.FindElement(x).Update(disabled=True, value = '')

    return signalType

def onGenerateSignal(window, values, storedSignals):
    signalType = values["signalType"]
    inputFields = signals[signalType]["fields"]
    inputValues = {k:v for k,v in  values.items() if k in inputFields}
    err_msg, param_values = validate_input(inputValues)
    if err_msg != "":
        sg.Popup('Error!', err_msg)
        return

    xSet, ySet = generate_signal(signalType, param_values)

    newSignal = { 
        'name':signalType,
        'displayName': signalType, 
        'isDiscrete': signals[signalType]['isDiscrete'],
        'isPeriodic': signals[signalType]['isPeriodic'],
        'isComplex': False,
        'x': xSet, 
        'y': ySet, 
        'params': param_values 
    }
    addToSelectionList(window, newSignal, storedSignals)

def onShowGraph(window, values, storedSignals):
    if(len(values['selectedGraphs']) == 0):
        sg.Popup('Error!', "Select at least one signal")
        return
    selectedGraphs = values["selectedGraphs"]
    data = []
    layout = go.Layout(
        xaxis=dict(
            title='t[s]',
            titlefont=dict(
                family='Arial, sans-serif',
                size=18,
                color='lightgrey'
            ),
            showticklabels=True,
            tickfont=dict(
                family='Old Standard TT, serif',
                size=14,
                color='black'
            ),
            exponentformat='e',
            showexponent='all'
        ),
        yaxis=dict(
            title='A[m]',
            titlefont=dict(
                family='Arial, sans-serif',
                size=18,
                color='lightgrey'
            ),
            showticklabels=True,
            tickfont=dict(
                family='Old Standard TT, serif',
                size=14,
                color='black'
            ),
            exponentformat='e',
            showexponent='all'
        )
    )


    for x in selectedGraphs:
        graph = storedSignals[getSelectedGraphIndex(x)]

        isCoercedToContinuous = None
        try:
            isCoercedToContinuous = graph['displayContinuous']
        except KeyError:
            isCoercedToContinuous = False 
        
        data.append(go.Scatter(
            x=graph['x'],
            y=graph['y'],
            mode="markers" if graph['isDiscrete'] and not isCoercedToContinuous else 'lines',
        ))

    figure = go.Figure(data=data, layout=layout)
    
    py.plot(figure, filename='graph')

def onShowHistogram(window, values, storedSignals):
    if(len(values['selectedGraphs']) != 1):
        sg.Popup('Error!', "Select only one signal")
        return
    selectedGraphs = values["selectedGraphs"]
    ranges = int(values['ranges'])
    data = []
    for x in selectedGraphs:
        graph = storedSignals[getSelectedGraphIndex(x)]
        data.append(go.Histogram(
            x=graph['y'],
            xbins={
                'size': (max(graph['y']) - min(graph['y'])) / (ranges - 1)
            },
        ))
    py.plot(data, filename='graph')

def addToSelectionList(window, newSignal, storedSignals):
      storedSignals.append(newSignal)
      selectionList = window.FindElement('selectedGraphs')
      currentState = selectionList.GetListValues()
      currentState.append(f"{len(currentState)}. {newSignal['displayName']} {newSignal['params']}")
      selectionList.Update(currentState)
      selectionList.SetValue(values=[])

def removeFromSelectionList(window, selectedToRemove, storedSignals):
      selectionList = window.FindElement('selectedGraphs')
      alreadyRemoved = 0
      for x in selectedToRemove:
          number = getSelectedGraphIndex(x)
          storedSignals.pop(number-alreadyRemoved)
          alreadyRemoved += 1

      currentList = []
      for i in range(len(storedSignals)):
        currentList.append(f"{i}. {storedSignals[i]['displayName']} {storedSignals[i]['params']}")

      selectionList.Update(currentList)
    
def saveFile(window, values, storedSignals):
    selected = values["selectedGraphs"]
    fileName = values['saveFile']
    saveToBin = values['saveToBin']
    if len(selected) != 1:
        sg.Popup("Error!", "You have to select 1 signal to save.")
        return
    signalToSave = storedSignals[getSelectedGraphIndex(selected[0])]

    fileOps.saveFile(signalToSave, fileName, saveToBin)

def readFile(window, values, storedSignals):
    fileName = values['readFile']
    signal = fileOps.readFile(fileName)
    if(signal == None):
        return
    addToSelectionList(window, signal, storedSignals)

   