import PySimpleGUI as sg


gui = [
    [sg.Text("Sensor time unit", size=(20, 1)), sg.InputText(key="stu", do_not_clear=True)],
    [sg.Text("Object velocity", size=(20, 1)), sg.InputText(key="ov", do_not_clear=True)],
    [sg.Text("Signal velocity", size=(20, 1)), sg.InputText(key="sv", do_not_clear=True)],
    [sg.Text("Signal period", size=(20, 1)), sg.InputText(key="sp", do_not_clear=True)],
    [sg.Text("Signal sampling frequency", size=(20, 1)), sg.InputText(key="ssf", do_not_clear=True)],
    [sg.Text("Buffer length", size=(20, 1)), sg.InputText(key="bl", do_not_clear=True)],
    [sg.Text("Raport period", size=(20, 1)), sg.InputText(key="rp", do_not_clear=True)],


]