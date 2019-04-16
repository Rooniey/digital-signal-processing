import PySimpleGUI as sg  
import gui

prevState = 'sin'
storedSignals = []
# processedSignals = []

window = sg.Window('New GUI').Layout(gui.layout)
window.Finalize()
sg.SetOptions(button_color=sg.COLOR_SYSTEM_DEFAULT)
gui.initialize_inputs(window, prevState)

 # Event Loop
while True:                
    event, values = window.Read()
    if event is None or event == 'Exit':  
        break  
    if event == 'signalType':  
        prevState =  gui.onSignalTypeChange(window, values["signalType"], prevState)
    if event == 'generateSignal':
        gui.onGenerateSignal(window, values, storedSignals)
    if event == 'showSignal':
        gui.onShowGraph(window, values, storedSignals)
    if event == 'showSignalProperties':
        gui.onSignalProperties(window, values["selectedGraphs"], storedSignals)
    if event == 'showHistogram':
        gui.onShowHistogram(window, values, storedSignals)
    if event == 'removeSignal':
        gui.removeFromSelectionList(window, values["selectedGraphs"], storedSignals)
    if event == 'saveFile':
        gui.saveFile(window, values, storedSignals)
    if event == 'readFile':
        gui.readFile(window, values, storedSignals)
    if event == '+':
        gui.onAddSignals(window, values, storedSignals)
    if event == '—':
        gui.onSubtractSignals(window, values, storedSignals)
    if event == '*':
        gui.onMultiplySignals(window, values, storedSignals)
    if event == '/':
        gui.onDivideSignals(window, values, storedSignals)
    if event == 'Sinc?':
        gui.onChangeReconstructMethod(window, values)
    if event == 'quantize':
        gui.onQuantizeSignal(window, values, storedSignals)
    if event == 'sample': 
        gui.onSampleSignal(window, values, storedSignals)
    if event == 'reconstruct':
        gui.onReconstructSignal(window, values, storedSignals)
    if event == 'computeErrors':
        gui.onComputeErrorParameters(window, values, storedSignals)
window.Close()