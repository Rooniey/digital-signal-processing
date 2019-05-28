import re

def getSelectedGraphIndex(x):
    return int(re.search(r'^\d+', x).group())

def addToSelectionList(window, newSignal, storedSignals):
      storedSignals.append(newSignal)
      selectionList = window.FindElement('selectedGraphs')
      currentState = selectionList.GetListValues()
      currentState.append(f"{len(currentState)}. {newSignal['displayName']} {newSignal['params']}")
      selectionList.Update(currentState)
      selectionList.SetValue(values=[])
