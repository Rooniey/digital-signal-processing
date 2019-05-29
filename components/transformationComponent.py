import PySimpleGUI as sg
from commons.validators import try_int, try_float
from commons.signalList import getSelectedGraphIndex, addToSelectionList
from signals import operations
import transformation.transformationTypes as transform
import numpy as np

TRANSFORM_OPTIONS = ['FFT', 'DFT']

frameLayout = [
    [
        sg.Text("Window function:", size=(15, 1)),
        sg.InputCombo(values=TRANSFORM_OPTIONS, key="fourierTransformOptions", readonly=True, size=(15,1))
    ],
    [
        sg.Button("Filter", key="transform")
    ]
]

gui = [
    [sg.Frame("Transformation", layout=frameLayout, size=(100, 50))],
]

def onTransformSignal(window, values, storedSignals):
    selectedSignal = values['selectedGraphs']
    if len(selectedSignal) != 1:
        sg.Popup('Error!', 'Select 1 graph to filter!')
        return None
    selectedSignal = storedSignals[getSelectedGraphIndex(selectedSignal[0])]

    selectedTransform = values['fourierTransformOptions']

    transformed = transform.proxy(selectedTransform, selectedSignal)

    addToSelectionList(window, transformed, storedSignals)
