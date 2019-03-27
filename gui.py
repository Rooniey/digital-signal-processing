import PySimpleGUI as sg
import plotly.offline as py
import plotly.graph_objs as go
import json
import pandas as pd

import operations as ops
import fileOperations as fileOps 
from constants import signals, allFields
from helpers import getSelectedGraphIndex
from validators import validate_input
from signalGenerator import generate_signal

inputFields = map(lambda fieldName: [sg.Text(fieldName, size=(3, 1)), sg.InputText(key=fieldName, do_not_clear=True)], allFields)

layout = [
        [sg.InputCombo(values=list(signals.keys()), change_submits=True, key="signalType", readonly=True)],
        *inputFields,
        [
            sg.Button('Generate signal'), 
            sg.Button('Show'), 
        ],
        [
            sg.Button('Histogram'),
            sg.Text('Ranges count: '),
            sg.Slider(range=(5,20), default_value=15, size=(10,10), orientation='horizontal', font=('Helvetica', 7), key="ranges")
        ],
        [
            sg.Listbox(values=[], select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE, size=(50, 6), key="selectedGraphs"), 
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
]

def onSubtractSignals(window, values, storedSignals):
    first, second = ops.extractSignalsForOperation(values, storedSignals)
    if first == None: return
    newSignal = ops.applyOperation("-", first, second)
    addToSelectionList(window, newSignal, storedSignals)

def onAddSignals(window, values, storedSignals):
    first, second = ops.extractSignalsForOperation(values, storedSignals)
    if first == None: return
    newSignal = ops.applyOperation("+", first, second)
    addToSelectionList(window, newSignal, storedSignals)

def onMultiplySignals(window, values, storedSignals):
    first, second = ops.extractSignalsForOperation(values, storedSignals)
    if first == None: return
    newSignal = ops.applyOperation("*", first, second)
    addToSelectionList(window, newSignal, storedSignals)

def onDivideSignals(window, values, storedSignals):
    first, second = ops.extractSignalsForOperation(values, storedSignals)
    if first == None: return
    newSignal = ops.applyOperation("/", first, second)
    addToSelectionList(window, newSignal, storedSignals)

def initialize_inputs(window, initialSignalType):
    initialSignal = signals[initialSignalType]
    window.FindElement('signalType').Update(value = initialSignalType)
    for field in allFields:
        if field not in initialSignal['fields']:
            window.FindElement(field).Update(disabled=True)

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

    trace = go.Scatter(
        x = xSet,
        y = ySet
    )
 
    data = [trace]

    newSignal = { 
        'name':signalType, 
        'isDiscrete': signals[signalType]['isDiscrete'],
        'isPeriodic': signals[signalType]['isPeriodic'],
        'isComplex': False,
        'x': xSet, 
        'y': ySet, 
        'params': param_values 
    }
    addToSelectionList(window, newSignal, storedSignals)

def onShowGraph(window, values, storedSignals):
    selectedGraphs = values["selectedGraphs"]
    data = []
    for x in selectedGraphs:
        graph = storedSignals[getSelectedGraphIndex(x)]
        print(len(graph['x']))
        data.append(go.Scatter(x=graph['x'], y=graph['y']))
    py.plot(data, filename='graph')

def onShowHistogram(window, values, storedSignals):
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
      currentState.append(f"{len(currentState)}. {newSignal['name']} {newSignal['params']}")
      selectionList.Update(currentState)

def removeFromSelectionList(window, selectedToRemove, storedSignals):
      selectionList = window.FindElement('selectedGraphs')
      alreadyRemoved = 0
      for x in selectedToRemove:
          number = getSelectedGraphIndex(x)
          storedSignals.pop(number-alreadyRemoved)
          alreadyRemoved += 1

      currentList = []
      for i in range(len(storedSignals)):
        currentList.append(f"{i}. {storedSignals[i]['type']} {storedSignals[i]['params']}")

      selectionList.Update(currentList)
    
def saveFile(window, values, storedSignals):
    selected = values["selectedGraphs"]
    fileName = values['saveFile']
    saveToBin = values['saveToBin']
    if len(selected) != 1:
        sg.Popup("Error!", "You have to select 1 signal to save.")
    signalToSave = storedSignals[getSelectedGraphIndex(selected[0])]

    fileOps.saveFile(signalToSave, fileName, saveToBin)

def readFile(window, values, storedSignals):
    fileName = values['readFile']
    signal = fileOps.readFile(fileName)
    addToSelectionList(window, signal, storedSignals)

   