import PySimpleGUI as sg
import components.converterComponent as converterComponent
import components.fileOperationsComponent as fileOperationsComponent
import components.signalComponent as signalComponent
import components.convolutionComponent as convolutionComponent

column1 = sg.Column([
        *signalComponent.gui,
        *fileOperationsComponent.gui
])

column2 = sg.Column([
    *converterComponent.gui,
    *convolutionComponent.gui
])

layout = [[column1, column2]]