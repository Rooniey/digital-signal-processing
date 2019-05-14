import PySimpleGUI as sg
import plotly.offline as py
import plotly.graph_objs as go
import signals.operations as ops
import numpy as np
from signals.constants import signals, allFields
from signals.signalGenerator import generate_signal
from signals.statistics import calculateStatistics
from commons.signalList import getSelectedGraphIndex, addToSelectionList
from commons.validators import validate_input

inputFields = map(lambda fieldName: [sg.Text(fieldName, size=(3, 1)), sg.InputText(key=fieldName, do_not_clear=True)], allFields)

gui = [
    [sg.InputCombo(values=list(signals.keys()), change_submits=True, key="signalType", readonly=True)],
    *inputFields,
    [
        sg.Button('Generate signal', key="generateSignal"), 
        sg.Button('Show', key="showSignal"), 
        sg.Button('GenerateSpectrum', key="generateSpectrum")
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
    [sg.Button('+'), sg.Button('—'), sg.Button('*'), sg.Button('/')]
]

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

def onGenerateSpectrum(window, selectedSignals, storedSignals):
    if(len(selectedSignals) != 1):
        sg.Popup('Error!', "Select single signal")
    else:
        selectedSignal = storedSignals[getSelectedGraphIndex(selectedSignals[0])]
        spectrum = ops.calculateSpectrum(selectedSignal)
        addToSelectionList(window, spectrum, storedSignals)
        