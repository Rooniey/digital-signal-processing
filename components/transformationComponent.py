import PySimpleGUI as sg
from commons.validators import try_int, try_float
from commons.signalList import getSelectedGraphIndex, addToSelectionList
from signals import operations
import transformation.transformationTypes as transform
import numpy as np

frameLayout = [
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

    transformed = transform.proxy('DFT', selectedSignal)

    addToSelectionList(window, transformed, storedSignals)
