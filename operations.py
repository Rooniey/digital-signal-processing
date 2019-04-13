from constants import signals
from utility import pluck
import PySimpleGUI as sg
import numpy as np
from helpers import getSelectedGraphIndex

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

def computeSignal(signal, x_values):
    if signal['isComplex'] == True:
        operation, firstOperand, secondOperand = pluck(signal, 'operation', 'firstOperand', 'secondOperand')
        LsigVal, RsigVal = None, None
        if(firstOperand['isComplex']):
            LsigVal = computeSignal(firstOperand, x_values)
        else:
            sigName = firstOperand['name']
            LsigVal = signals[sigName]['fn'](x_values, firstOperand['params'])
        
        if(secondOperand['isComplex']):
            RsigVal = computeSignal(secondOperand, x_values)
        else:
            sigName = secondOperand['name']
            RsigVal = signals[sigName]['fn'](x_values, secondOperand['params'])

        return applyOperationSimple(operation, LsigVal, RsigVal)
    else:
        sigName = signal['name']
        return signals[sigName]['fn'](x_values, signal['params'])
    
# Operation on signals

def subtractSignals(first, second):
    return [a - b for a, b in zip(first, second)]

def addSignals(first, second):
    return [a + b for a, b in zip(first, second)]

def multiplySignals(first, second):
    return [a * b for a, b in zip(first, second)]

def divideSignals(first, second):
    return [a / b if b != 0 else 0 for a, b in zip(first, second)]