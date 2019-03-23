import PySimpleGUI as sg  
import gui

window = sg.Window('New GUI').Layout(gui.layout)
prevState = 'sin'
storedSignals = []

while True:                 # Event Loop
  event, values = window.Read()
  print(event, values)
  if event is None or event == 'Exit':  
      break  
  if event == 'signalType':  
      prevState =  gui.onSignalTypeChange(window, values["signalType"], prevState)
  if event == 'Generate signal':
      newSignal = gui.onGenerateSignal(window, values)
      gui.addToSelectionList(window, newSignal, storedSignals)
  if event == 'removeSignal':
      gui.removeFromSelectionList(window, values["selectedGraphs"], storedSignals)
window.Close()