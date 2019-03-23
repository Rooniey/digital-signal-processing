import PySimpleGUI as sg
from constants import signals, allFields
from validators import validate_input
import re
import plotly.offline as py
import plotly.graph_objs as go

inputFields = map(lambda fieldName: [sg.Text(fieldName, size=(15, 1)), sg.InputText(key=fieldName, do_not_clear=True)], allFields)

layout = [
        [sg.InputCombo(values=list(signals.keys()), change_submits=True, key="signalType", default_value='sin', readonly=True)],
        *inputFields, 
        [sg.Button('Generate signal')],
        [sg.Listbox(values=[], select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE, size=(50, 6), key="selectedGraphs")],
        [sg.Button('Remove signal/s', key='removeSignal')],
]

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

def onGenerateSignal(window, values):
    signalType = values["signalType"]
    inputFields = signals[signalType]["fields"]
    inputValues = {k:v for k,v in  values.items() if k in inputFields}
    print(inputValues)
    err_msg, param_values = validate_input(inputValues)
    if err_msg != "":
        sg.Popup('Error!', err_msg)
        return

    param_values['n'] = param_values['d'] * param_values['fp']
    del param_values['fp']

    xSet, ySet = signals[signalType]['fn'](**param_values)
 
    # Create a trace
    trace = go.Scatter(
        x = xSet,
        y = ySet
    )
 
    data = [trace]
    # py.plot(data, filename='basic-line')

    return { 'type':signalType, 'x': xSet, 'y':ySet, 'params': param_values }

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
          number = int(re.search(r'\d+', x).group())
          storedSignals.pop(number-alreadyRemoved)
          alreadyRemoved += 1

      currentList = []
      for i in range(len(storedSignals)):
        currentList.append(f"{i}. {storedSignals[i]['type']} {storedSignals[i]['params']}")

      selectionList.Update(currentList)
    