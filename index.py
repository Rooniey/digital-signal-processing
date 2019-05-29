import PySimpleGUI as sg  
import gui
import components as comp

prevState = 'sin'
storedSignals = []
# processedSignals = []

window = sg.Window('New GUI').Layout(gui.layout)
window.Finalize()
sg.SetOptions(button_color=sg.COLOR_SYSTEM_DEFAULT)
comp.signalComponent.initialize_inputs(window, prevState)

 # Event Loop
while True:                
    event, values = window.Read()
    if event is None or event == 'Exit':  
        break  
    if event == 'signalType':  
        prevState = comp.signalComponent.onSignalTypeChange(window, values["signalType"], prevState)
    if event == 'generateSignal':
        comp.signalComponent.onGenerateSignal(window, values, storedSignals)
    if event == 'showSignal':
        comp.signalComponent.onShowGraph(window, values, storedSignals)
    if event == 'showSignalProperties':
        comp.signalComponent.onSignalProperties(window, values["selectedGraphs"], storedSignals)
    if event == 'showHistogram':
        comp.signalComponent.onShowHistogram(window, values, storedSignals)
    if event == 'removeSignal':
        comp.signalComponent.removeFromSelectionList(window, values["selectedGraphs"], storedSignals)
    if event == '+':
        comp.signalComponent.onAddSignals(window, values, storedSignals)
    if event == '—':
        comp.signalComponent.onSubtractSignals(window, values, storedSignals)
    if event == '*':
        comp.signalComponent.onMultiplySignals(window, values, storedSignals)
    if event == '/':
        comp.signalComponent.onDivideSignals(window, values, storedSignals)
    if event == "generateSpectrum":
        comp.signalComponent.onGenerateSpectrum(window, values["selectedGraphs"], storedSignals)
    
    if event == 'saveFile':
        comp.fileOperationsComponent.saveFile(window, values, storedSignals)
    if event == 'readFile':
        comp.fileOperationsComponent.readFile(window, values, storedSignals)
    

    if event == 'Sinc?':
        comp.converterComponent.onChangeReconstructMethod(window, values)
    if event == 'quantize':
        comp.converterComponent.onQuantizeSignal(window, values, storedSignals)
    if event == 'sample': 
        comp.converterComponent.onSampleSignal(window, values, storedSignals)
    if event == 'reconstruct':
        comp.converterComponent.onReconstructSignal(window, values, storedSignals)
    if event == 'computeErrors':
        comp.converterComponent.onComputeErrorParameters(window, values, storedSignals)

    if event == 'filter':
        comp.convolutionComponent.onFilter(window, values, storedSignals)
    if event == 'useK?':
        comp.convolutionComponent.onFrequencyLimitParameterChange(window, values)

    if event == 'simulate':
        comp.sensorComponent.onSimulate(window, values, storedSignals)

    if event == 'op_convolve':
        comp.sensorComponent.onConvolveSignals(window, values, storedSignals)
    if event == 'op_correlate':
        comp.sensorComponent.onCorrelateSignals(window, values, storedSignals)

    if event == 'transform':
        comp.transformationComponent.onTransformSignal(window, values, storedSignals)

window.Close()



