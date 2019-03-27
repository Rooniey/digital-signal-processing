import pandas as pd
import PySimpleGUI as sg

def saveFile(signal, fileName, saveToBin):
    openMode = 'w'
    if saveToBin:
        fileName = f"{fileName}.bin"
        openMode = 'wb'
    else :
        fileName = f"{fileName}.txt"

    with open(fileName, openMode) as f:
        params = signal["params"]
        data = {
            "data": {
                "name": signal["name"],
                "fp": params["fp"],
                "n": params["n"],
                "t1": params["t1"],
                "type": "real",
                "x": signal["x"],
                "y": signal["y"]
            }
        }
        dumped = pd.Series(data).to_json(orient='values')
        if saveToBin:
            f.write(dumped.encode('utf-8'))
        else:
            f.write(dumped)

def readFile(fileName):
    extension = fileName.split('.')[-1]
    openMode = ''
    isBinary = False
    if extension == 'bin':
        openMode = 'rb'
        isBinary = True
    elif extension == 'txt':
        openMode = 'r'
    else:
        sg.Popup('Error!', 'select correct file for deserialization')
        return

    with open(fileName, openMode) as f:
        readData = f.read()
        if isBinary:
            readData = readData.decode('utf-8')
        data = pd.read_json(readData, orient='values')

        return { 
            'name': data["name"][0], 
            'isDiscrete': True,
            'isPeriodic': False,
            'isComplex': False,
            'x': data["x"][0], 
            'y': data["y"][0], 
            'params': {
                "fp": data["fp"][0],
                "n": data["n"][0],
                "t1": data["t1"][0]
            }
        }
        
    