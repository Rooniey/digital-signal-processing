import PySimpleGUI as sg  
import gui

prevState = 'sin'
storedSignals = []

window = sg.Window('New GUI').Layout(gui.layout)
window.Finalize()
sg.SetOptions(button_color=sg.COLOR_SYSTEM_DEFAULT)
gui.initialize_inputs(window, prevState)

while True:                 # Event Loop
  event, values = window.Read()
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