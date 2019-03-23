import PySimpleGUI as sg
from constants import signals, allFields
from validators import validate_input
import plotly.offline as py
import plotly.graph_objs as go

inputFields = map(lambda fieldName: [sg.Text(fieldName, size=(15, 1)), sg.InputText(key=fieldName, do_not_clear=True)], allFields)

layout = [
        [sg.InputCombo(values=list(signals.keys()), change_submits=True, key="signalType", default_value='sin')],
        *inputFields,
        [sg.Button('Generate signal')]
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

    print(param_values)
    
    xSet, ySet = signals[signalType]['fn'](**param_values)
 
    # Create a trace
    trace = go.Scatter(
        x = xSet,
        y = ySet
    )
 
    data = [trace]
 
    py.plot(data, filename='basic-line')