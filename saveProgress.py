import pickle

from tools import getOption

def saveOrLoad(data):
    option = getOption(['Save', 'Load']) 
    if option == "Save":
        saveGame(data)
    else:
        loadGame(data)

def saveGame(data):
    pickle_out = open(data.exe_dir + "/saveData.pickle", "wb")
    pickle.dump(data, pickle_out)
    pickle_out.close

def loadGame(data):
    pickle_in = open(data.exe_dir + "/saveData.pickle","rb")
    data = pickle.load(pickle_in)
    return data

    