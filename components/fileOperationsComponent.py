import PySimpleGUI as sg
import signals.fileOperations as fileOps
from commons.signalList import getSelectedGraphIndex, addToSelectionList

gui = [
    [
        sg.Input(key='readFile', change_submits=True, visible=False),
        sg.FileBrowse('Read file',  target="readFile", change_submits=True),
        sg.Input(key='saveFile', change_submits=True, visible=False),
        sg.FileSaveAs('Write file', target='saveFile', change_submits=True, file_types=(("Text files", "*.txt"),("Binary files", "*.bin"))),
        sg.Checkbox('Save to binary', key='saveToBin')
    ]
]

def saveFile(window, values, storedSignals):
    selected = values["selectedGraphs"]
    fileName = values['saveFile']
    saveToBin = values['saveToBin']
    if len(selected) != 1:
        sg.Popup("Error!", "You have to select 1 signal to save.")
        return
    signalToSave = storedSignals[getSelectedGraphIndex(selected[0])]

    fileOps.saveFile(signalToSave, fileName, saveToBin)

def readFile(window, values, storedSignals):
    fileName = values['readFile']
    signal = fileOps.readFile(fileName)
    if(signal == None):
        return
    addToSelectionList(window, signal, storedSignals)
