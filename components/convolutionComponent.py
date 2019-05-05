import PySimpleGUI as sg
from commons.validators import try_int, try_float
from commons.signalList import getSelectedGraphIndex, addToSelectionList
from convolution.filter import FILTER_TYPES, WINDOW_FUNCTIONS
from convolution.filter import filterSignal

frameLayout = [
    [   
        sg.Text("M:", size=(15, 1)),
        sg.Input(key='M', size=(15, 1), do_not_clear=True)
    ],
    [sg.Checkbox('Use K?', enable_events=True, change_submits=True, key='useK?')],
    [   
        sg.Text("fo:", size=(15, 1)),
        sg.Input(key='fo', size=(15, 1), do_not_clear=True)
    ],
    [   
        sg.Text("K:", size=(15, 1)),
        sg.Input(key='K', size=(15, 1), do_not_clear=True, disabled=True)
    ],
    [
        sg.Text("Filter type:", size=(15, 1)),
        sg.InputCombo(values=FILTER_TYPES, key="filterType", readonly=True, size=(15,1))
    ],
    [
        sg.Text("Window function:", size=(15, 1)),
        sg.InputCombo(values=WINDOW_FUNCTIONS, key="windowFunction", readonly=True, size=(15,1))
    ],
    [
        sg.Button("Filter", key="filter")
    ]
]

gui = [
    [sg.Frame("Filter designer", layout=frameLayout, size=(100, 50))],
]

def onFilter(window, values, storedSignals):
    errors, params = assembleFilterParams(values)
    if errors != "":
        sg.Popup('Invalid parameters', errors)
        return None
    
    selectedSignal = values['selectedGraphs']
    if len(selectedSignal) != 1:
        sg.Popup('Error!', 'Select 1 graph to filter!')
        return None
    selectedSignal = storedSignals[getSelectedGraphIndex(selectedSignal[0])]

    if not values["useK?"]:
        params["K"] = selectedSignal["params"]["fp"] / params["K"]

    filteredSignal = {
        'name': selectedSignal["name"],
        'displayName': f"filtered {selectedSignal['displayName']}",
        'isDiscrete': True,
        'isComplex': False,
        'isPeriodic': False,
        'x': selectedSignal["x"],
        'y': filterSignal(selectedSignal, **params),
        "params": selectedSignal['params']
    }
    
    addToSelectionList(window, filteredSignal, storedSignals)

def assembleFilterParams(values):
    errors = ""
     
    tmp = values["M"].strip()
    M = try_int(tmp)
    if tmp == "":
        errors = errors + "M is required field\n"
    elif M == None:
        errors = errors + f"M must be an integer (not {tmp})\n"
    elif M % 2 == 0:
        errors = errors + f"M must be an odd integer\n"

    params = {
        "M": M,
        "filter": values["filterType"],
        "window": values["windowFunction"]
    }

    if values["useK?"]:
        tmp = values["K"].strip()
        K = try_float(tmp)
        if tmp == "":
            errors = errors + "K is required field\n"
        elif K == None:
            errors = errors + f"K must be a float (not {tmp})\n"
        params["K"] = K
    else:
        tmp = values["fo"].strip()
        fo = try_float(tmp)
        if tmp == "":
            errors = errors + "fo is required field\n"
        elif fo == None:
            errors = errors + f"fo must be a float (not {tmp})\n"
        params["K"] = fo
    
    return (errors, params)

def onFrequencyLimitParameterChange(window, values):
    useK = values['useK?']
    window.FindElement('K').Update(disabled=not useK, value='')
    window.FindElement('fo').Update(disabled=useK, value='')
    