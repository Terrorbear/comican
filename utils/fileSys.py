import os

def makeDir(path):
    try:
        os.makedirs(path)
    except:
        pass
    return
