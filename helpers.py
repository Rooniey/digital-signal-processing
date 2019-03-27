import re

def getSelectedGraphIndex(x):
    return int(re.search(r'^\d+', x).group())