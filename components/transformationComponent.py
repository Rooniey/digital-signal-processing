import PySimpleGUI as sg
from commons.validators import try_int, try_float
from commons.signalList import getSelectedGraphIndex, addToSelectionList
from signals import operations
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
  print('x')