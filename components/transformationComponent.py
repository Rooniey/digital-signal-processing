import PySimpleGUI as sg
from commons.validators import try_int, try_float
from commons.signalList import getSelectedGraphIndex, addToSelectionList
from signals import operations
import transformation.transformationTypes as tt
import numpy as np

TRANSFORM_OPTIONS = ['DFT', 'INV_DFT', 'FFT', 'FFT_VECT', 'DB4']

frameLayout = [
    [
        sg.Text("Transformation type:", size=(15, 1)),
        sg.InputCombo(values=TRANSFORM_OPTIONS, key="fourierTransformOptions", readonly=True, size=(15,1))
    ],
    [
        sg.Button("Transform", key="transform")
    ]
]

gui = [
    [sg.Frame("Transformation", layout=frameLayout, size=(100, 50))],
]

def onTransformSignal(window, values, storedSignals):
    selectedSignal = values['selectedGraphs']
    if len(selectedSignal) != 1:
        sg.Popup('Error!', 'Select 1 graph to perform transformation!')
        return None
    selectedSignal = storedSignals[getSelectedGraphIndex(selectedSignal[0])]

    selectedTransform = values['fourierTransformOptions']

    (result, elapsed)  = tt.perform_transformation(selectedTransform, selectedSignal)

    for signal in result:
        addToSelectionList(window, signal, storedSignals)

    sg.Popup('Performance', f"Time elapsed: {elapsed}s")


