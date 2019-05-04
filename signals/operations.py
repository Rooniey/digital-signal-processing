from signals.constants import signals
from commons.utility import pluck
from commons.signalList import getSelectedGraphIndex
import PySimpleGUI as sg
import numpy as np

def extractSignalsForOperation(values, storedSignals):
    selectedGraphs = values['selectedGraphs']
    if len(selectedGraphs) != 2:
        sg.Popup('Error!', 'Select 2 graphs to add')
        return (None, None)
    return storedSignals[getSelectedGraphIndex(selectedGraphs[0])], storedSignals[getSelectedGraphIndex(selectedGraphs[1])]

def applyOperation(operation, first, second):
    ft1, ffp = pluck(first['params'], 't1', 'fp')
    st1, sfp = pluck(second['params'], 't1', 'fp')

    if(ft1 != st1 or ffp != sfp):
        sg.Popup('Error', 't1 and fp must match')
        return None
        
    new_x = [x for x, _ in zip(first['x'], second['x'])]
    new_y = applyOperationSimple(operation, first['y'], second['y'])

    params = second['params']
    isPeriodic = first['isPeriodic'] and second['isPeriodic']
    if isPeriodic:
        fT = first['params']['T']
        sT = second['params']['T']
        params['T'] = fT if fT == sT else fT*sT
        
    return  {
        'name': second['name'],
        'displayName': f"{first['displayName']}{operation}{second['displayName']}",
        'isDiscrete': (first['isDiscrete'] or second['isDiscrete']),
        'isComplex': True,
        'isPeriodic': isPeriodic,
        'x': new_x,
        'y': new_y,
        "params": second['params'],
        "operation": operation,
        "firstOperand": first,
        "secondOperand": second
    }

def applyOperationSimple(operation, first, second): 
    if operation == "+":
        return addSignals(first,second)
    elif operation == "-":
        return subtractSignals(first,second)
    elif operation == "/":
        return divideSignals(first,second)
    elif operation == "*":
        return multiplySignals(first,second)

# Operation on signals

def subtractSignals(first, second):
    return [a - b for a, b in zip(first, second)]

def addSignals(first, second):
    return [a + b for a, b in zip(first, second)]

def multiplySignals(first, second):
    return [a * b for a, b in zip(first, second)]

def divideSignals(first, second):
    return [a / b if b != 0 else 0 for a, b in zip(first, second)]