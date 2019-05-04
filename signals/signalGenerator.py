import numpy as np
from signals.constants import signals
from signals.operations import applyOperationSimple 
from commons.utility import pluck


def generate_signal(signalType, param_values):
    d, fp, t1 = pluck(param_values, 'd', 'fp', 't1')
    n = int(d * fp)
    param_values['n'] = n
    x_values = np.linspace(t1, t1+d, n + 1)
    y_values = signals[signalType]['fn'](x_values, param_values)
    return [x_values, y_values]

# Signal computation
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