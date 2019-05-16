import PySimpleGUI as sg
import components.converterComponent as converterComponent
import components.fileOperationsComponent as fileOperationsComponent
import components.signalComponent as signalComponent
import components.convolutionComponent as convolutionComponent
import components.sensorComponent as sensorComponent


column1 = sg.Column([
        *signalComponent.gui,
        *fileOperationsComponent.gui
])

column2 = sg.Column([
    *converterComponent.gui,
    *convolutionComponent.gui
])


tab1_layout = [[column1, column2]]

tab2_layout = [*sensorComponent.gui]

layout = [[sg.TabGroup([[sg.Tab('Signal processing', tab1_layout), sg.Tab('Simulator', tab2_layout)]])]]