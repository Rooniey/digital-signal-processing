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
    result = None
    ft1, ffp = pluck(first['params'], 't1', 'fp')
    st1, sfp = pluck(second['params'], 't1', 'fp')

    if(ft1 != st1 or ffp != sfp):
        sg.Popup('Error', 't1 and fp must match')
        return None
        
    new_x = [x for x, _ in zip(first['x'], second['x'])]
    if operation == "+":
        result = addSignals(first['y'],second['y'])
    elif operation == "-":
        result = subtractSignals(first['y'],second['y'])
    elif operation == "/":
        result = divideSignals(first['y'],second['y'])
    elif operation == "*":
        result = multiplySignals(first['y'],second['y'])

    params = second['params']
    isPeriodic = first['isPeriodic'] and second['isPeriodic']
    if isPeriodic:
        params['T'] = first['params']['T'] * second['params']['T']
        
    return  {
        'name': second['name'],
        'isDiscrete': (first['isDiscrete'] or second['isDiscrete']),
        'isComplex': True,
        'isPeriodic': isPeriodic,
        'x': new_x,
        'y': result,
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
    print(f"signal in computeSignal: {signal}")
    firstOperand, secondOperand = None, None
    if signal['isComplex'] == True:
        operation = signal['operation']
        firstOperand = signal['firstOperand']
        secondOperand = signal['secondOperand']
        LsigVal, RsigVal = None, None
        if(firstOperand['isComplex']):
            LsigVal = computeSignal(firstOperand, x_values)
        else:
            sigName = firstOperand['name']
            LsigVal = signals[sigName]['fn'](x_values, firstOperand['params'])[1]
        
        if(secondOperand['isComplex']):
            RsigVal = computeSignal(secondOperand, x_values)
        else:
            sigName = secondOperand['name']
            RsigVal = signals[sigName]['fn'](x_values, secondOperand['params'])[1]

        return applyOperationSimple(operation, LsigVal, RsigVal)
    else:
        sigName = signal['name']
        return signals[sigName]['fn'](x_values, signal['params'])[1]
    
def subtractSignals(first, second):
    new_y = [a - b for a, b in zip(first, second)]
    return new_y

def addSignals(first, second):
    new_y = [a + b for a, b in zip(first, second)]
    return new_y

def multiplySignals(first, second):
    new_y = [a * b for a, b in zip(first, second)]
    return new_y

def divideSignals(first, second):
    new_y = [a / b if b != 0 else 0 for a, b in zip(first, second)]
    return new_y