import PySimpleGUI as sg
import components.converterComponent as convComp
import components.fileOperationsComponent as fileOpsComp
import components.signalComponent as sigComp

column1 = sg.Column([
        *sigComp.gui,
        *fileOpsComp.gui
])

column2 = sg.Column(
    *convComp.gui
)

layout = [[column1, column2]]