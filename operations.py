from constants import signals
import PySimpleGUI as sg
from helpers import getSelectedGraphIndex


def extractSignalsForOperation(values, storedSignals):
    selectedGraphs = values['selectedGraphs']
    if len(selectedGraphs) != 2:
        sg.Popup('Error!', 'Select 2 graphs to add')
        return (None, None)
    return storedSignals[getSelectedGraphIndex(selectedGraphs[0])], storedSignals[getSelectedGraphIndex(selectedGraphs[1])]

def applyOperation(operation, first, second):
    result = None
    if operation == "+":
        result = addSignals(first,second)
    elif operation == "-":
        result = subtractSignals(first,second)
    elif operation == "/":
        result = divideSignals(first,second)
    elif operation == "*":
        result = multiplySignals(first,second)

    params = second['params']
    isPeriodic = first['isPeriodic'] and second['isPeriodic']
    if isPeriodic:
        params['T'] = first['params']['T'] * second['params']['T']
        
    return  {
        'name': second['name'],
        'isDiscrete': (first['isDiscrete'] or second['isDiscrete']),
        'isComplex': True,
        'isPeriodic': isPeriodic,
        'x': result[0],
        'y': result[1],
        "params": second['params'],
        "operation": operation,
        "firstOperand": first,
        "secondOperand": second
    }

def computeSignal(signal, x_values):
    if signal['isComplex'] == True:
        operation = signal['operation']
        firstOperand = signal['firstOperand']
        secondOperand = signal['secondOperand']
        LsigVal, RsigVal = None, None
        if(firstOperand['isComplex']):
            LsigVal = computeSignal(firstOperand, x_values)
        else:
            sigName = firstOperand['name']
            LsigVal = signals[sigName]['fn'](x_values, firstOperand['params'])
        
        if(secondOperand['isComplex']):
            RsigVal = computeSignal(secondOperand, x_values)
        else:
            RsigVal = secondOperand['name']
            RsigVal = signals[sigName]['fn'](x_values, secondOperand['params'])

        return applyOperation(operation, LsigVal, RsigVal)
    else:
        RsigVal = secondOperand['name']
        return signals[sigName]['fn'](x_values, secondOperand['params'])
    
def subtractSignals(first, second):
    new_y = [a - b for a, b in zip(first['y'], second['y'])]
    new_x = [x for x, _ in zip(first['x'], second['x'])]
    return (new_x, new_y)

def addSignals(first, second):
    new_y = [a + b for a, b in zip(first['y'], second['y'])]
    new_x = [x for x, _ in zip(first['x'], second['x'])]
    return (new_x, new_y)

def multiplySignals(first, second):
    new_y = [a * b for a, b in zip(first['y'], second['y'])]
    new_x = [x for x, _ in zip(first['x'], second['x'])]
    return (new_x, new_y)

def divideSignals(first, second):
    new_y = [a / b if b != 0 else 0 for a, b in zip(first['y'], second['y'])]
    new_x = [x for x, _ in zip(first['x'], second['x'])]
    return (new_x, new_y)