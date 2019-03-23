import PySimpleGUI as sg
from constants import signals, allFields
from validators import validate_input
from signalGenerator import generate_signal
import re
import plotly.offline as py
import plotly.graph_objs as go
import json
import pandas as pd
import sys

def getSelectedGraphIndex(x):
    return int(re.search(r'^\d+', x).group())

inputFields = map(lambda fieldName: [sg.Text(fieldName, size=(3, 1)), sg.InputText(key=fieldName, do_not_clear=True)], allFields)

layout = [
        [sg.InputCombo(values=list(signals.keys()), change_submits=True, key="signalType", readonly=True)],
        *inputFields,
        [sg.Button('Generate signal'), sg.Button('Show')],
        [sg.Listbox(values=[], select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE, size=(50, 6), key="selectedGraphs"), sg.Button('Remove signal/s', key='removeSignal')],
        [sg.Button('+'), sg.Button('—'), sg.Button('*'), sg.Button('/')],
        [
            sg.Input(key='readFile', change_submits=True, visible=False),
            sg.FileBrowse('Read file',  target="readFile", change_submits=True),
            sg.Input(key='saveFile', change_submits=True, visible=False),
            sg.FileSaveAs('Write file', target='saveFile', change_submits=True, file_types=['json']),
            sg.Checkbox('Save to binary', key='saveToBin')
        ]
]

def extractSignalsForOperation(values, storedSignals):
    selectedGraphs = values['selectedGraphs']
    if len(selectedGraphs) != 2:
        sg.Popup('Error!', 'Select 2 graphs to add')
        return (None, None)
    return storedSignals[getSelectedGraphIndex(selectedGraphs[0])], storedSignals[getSelectedGraphIndex(selectedGraphs[1])]

def onSubtractSignals(window, values, storedSignals):
    first, second = extractSignalsForOperation(values, storedSignals)
    if first == None: return

    new_y = [a - b for a, b in zip(first['y'], second['y'])]
    new_x = [x for x, _ in zip(first['x'], second['x'])]
    newSignal = {
        'type': f"{first['type']} - {second['type']}",
        'x': new_x,
        'y': new_y,
        'params': {
            'A': first['params']['A'] + first['params']['A'],
        },
    }
    addToSelectionList(window, newSignal, storedSignals)

def onAddSignals(window, values, storedSignals):
    first, second = extractSignalsForOperation(values, storedSignals)

    added_y = [a + b for a, b in zip(first['y'], second['y'])]
    added_x = [x for x, _ in zip(first['x'], second['x'])]
    newSignal = {
        'type': f"{first['type']} + {second['type']}",
        'x': added_x,
        'y': added_y,
        'params': {
            'A': first['params']['A'] + first['params']['A'],
        },
    }
    addToSelectionList(window, newSignal, storedSignals)

def onMultiplySignals(window, values, storedSignals):
    first, second = extractSignalsForOperation(values, storedSignals)

    new_y = [a * b for a, b in zip(first['y'], second['y'])]
    new_x = [x for x, _ in zip(first['x'], second['x'])]
    newSignal = {
        'type': f"{first['type']} * {second['type']}",
        'x': new_x,
        'y': new_y,
        'params': {
            'A': first['params']['A'] * first['params']['A'],
        },
    }
    addToSelectionList(window, newSignal, storedSignals)

def onDivideSignals(window, values, storedSignals):
    first, second = extractSignalsForOperation(values, storedSignals)

    new_y = [a / b if b != 0 else 0 for a, b in zip(first['y'], second['y'])]
    new_x = [x for x, _ in zip(first['x'], second['x'])]
    newSignal = {
        'type': f"{first['type']} / {second['type']}",
        'x': new_x,
        'y': new_y,
        'params': {
            'A': 'unknown',
        },
    }
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
    print(inputValues)
    err_msg, param_values = validate_input(inputValues)
    if err_msg != "":
        sg.Popup('Error!', err_msg)
        return

    xSet, ySet = generate_signal(signalType, param_values)

    # Create a trace
    trace = go.Scatter(
        x = xSet,
        y = ySet
    )
 
    data = [trace]
    # py.plot(data, filename='basic-line')

    newSignal = { 'type':signalType, 'x': xSet, 'y':ySet, 'params': param_values }
    addToSelectionList(window, newSignal, storedSignals)

def onShowGraph(window, values, storedSignals):
    selectedGraphs = values["selectedGraphs"]
    data = []
    for x in selectedGraphs:
        graph = storedSignals[getSelectedGraphIndex(x)]
        data.append(go.Scatter(x=graph['x'], y=graph['y']))
    py.plot(data, filename='graph')

def addToSelectionList(window, newSignal, storedSignals):
      storedSignals.append(newSignal)
      selectionList = window.FindElement('selectedGraphs')
      currentState = selectionList.GetListValues()
      currentState.append(f"{len(currentState)}. {newSignal['type']} {newSignal['params']}")
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

    openMode = 'w'
    if saveToBin:
        fileName = f"{fileName}.bin"
        openMode = 'wb'
    else :
        fileName = f"{fileName}.txt"

    with open(fileName, openMode) as f:
        # dumped = json.dumps(signalToSave)
        dumped = pd.Series(signalToSave).to_json(orient='values')
        if saveToBin:
            f.write(dumped.encode('utf-8'))
        else:
            f.write(dumped)

def readFile(window, values, storedSignals):
    fileName = values['readFile']
    extension = fileName.split('.')[-1]

    openMode = ''
    isBinary = False
    if extension == 'bin':
        openMode = 'rb'
        isBinary = True
    elif extension == 'txt':
        openMode = 'r'
    else:
        sg.Popup('Error!', 'select correct file for deserialization')
        return

    with open(fileName, openMode) as f:
        readData = f.read()
        if isBinary:
            readData = readData.decode('utf-8')
        series = pd.read_json(readData, orient='values')[0]

        signal = series[0]
        x_values = series[1]
        y_values = series[2]
        param_values = series[3]
        print(f"s={signal}\nx={x_values}\ny={y_values}\nps={param_values}")
        newSignal = { 'type':signal, 'x': x_values, 'y':y_values, 'params': param_values }
        addToSelectionList(window, newSignal, storedSignals)