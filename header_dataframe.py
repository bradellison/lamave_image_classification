import pandas as pd
import os
from timeFunctions import elapsedTimeBetweenTimes, getTimeOfPhoto
from datetime import datetime

class Header:
    def __init__(self):
        self.recordingDate = None;
        self.ruvNo = 0;
        self.sdCardNo = ""
        self.waypoint = ""
        self.cameraDir = "N"
        self.setting = ""
        self.deploymentTime = ""
        self.recStart = ""
        self.recStop = ""
        self.elapsedTime = ""
        self.deploymentTime = ""
        self.deployedBy = ""
        self.retrievalTime = ""
        self.checkedBy = ""
        self.inputDate = datetime.today().date().strftime('%d/%m/%Y')
        self.notes = ""
        self.mantaPresence = "No"
        self.noMantas = 0
        self.noIdentifiedMantas = 0

# Define the column names
column_names = [
    "Recording Date",
    "RUV #",
    "SD Card #",
    "Waypoint",
    "Camera Direction",
    "Setting",
    "Deployment Time",
    "Recording Start",
    "Recording Stop",
    "Elapsed Time",
    "Deployment Date",
    "Deployed By",
    "Retrieval Date",
    "Checked By",
    "Input Date",
    "Notes",
    "Manta Presence",
    "No. of Manta Sightings",
    "No. of Mantas Identified"
]

def createHeader():
    # Create an empty DataFrame with the specified column names
    df = pd.DataFrame(columns=column_names)
    return df

def addToDf(headdf, header):
    new_row_values = [
        header.recordingDate,
        header.ruvNo,
        header.sdCardNo,
        header.waypoint,
        header.cameraDir,
        header.setting,
        header.deploymentTime,
        header.recStart,
        header.recStop,
        header.elapsedTime,
        header.deploymentTime,
        header.deployedBy,
        header.retrievalTime,
        header.checkedBy,
        header.inputDate,
        header.notes,
        header.mantaPresence,
        header.noMantas,
        header.noIdentifiedMantas
    ]

    headdf.loc[headdf.shape[0]] = new_row_values
    # print(headdf)

def addHeaderInfo(data):
    mantaStatsCollection(data)
    data.header.recordingDate = data.date
    data.header.ruvNo = data.ruv
    data.header.checkedBy = data.checkedBy
    data.header.waypoint = "Saan Ka " + data.site[-1]
    findRecordingTimes(data)

    # printHeader(data.header)
    addToDf(data.headerdf, data.header)
    saveHeader(data)

def saveHeader(data):
    file_name = data.date + '_header.csv'
    outputFile = os.path.join(data.exe_dir, "output/", file_name)
    data.headerdf.to_csv(outputFile, index=False)

def mantaStatsCollection(data):
    identifiedMantas = []
    allMantas = []
    for sighting in data.sightings:
        if not sighting.isManta:
            continue
        if sighting.ided == "Yes":
            if sighting.idnumber not in identifiedMantas:
                identifiedMantas.append(sighting.idnumber)
                allMantas.append(sighting.idnumber)
        else:
            if sighting.mantaIdWithUnknown not in allMantas:
                allMantas.append(sighting.mantaIdWithUnknown)

    if(len(allMantas) > 0):
        data.header.mantaPresence = "Yes"
        data.header.noMantas = len(allMantas)
        data.header.noIdentifiedMantas = len(identifiedMantas)

def findRecordingTimes(data):
    allPhotos = []
    for folder in data.goproFolders:
        allPhotos += os.listdir(folder)
    allPhotos.sort()

    data.header.recStart = getTimeOfPhoto(data, allPhotos[0])
    data.header.recStop = getTimeOfPhoto(data, allPhotos[-1])
    data.header.elapsedTime, _ = elapsedTimeBetweenTimes(data.header.recStart, data.header.recStop)

def printHeader(header):
    print(f"Recording Date - {header.recordingDate}")
    print(f"RUV # - {header.ruvNo}")
    print(f"SD Card # - {header.sdCardNo}")
    print(f"Waypoint - {header.waypoint}")
    print(f"Camera Direction - {header.cameraDir}")
    print(f"Setting - {header.setting}")
    print(f"Deployment Time - {header.deploymentTime}")
    print(f"Recording Start - {header.recStart}")
    print(f"Recording Stop - {header.recStop}")
    print(f"Elapsed Time - {header.elapsedTime}")
    print(f"Deployment Date - {header.deploymentTime}")
    print(f"Deployed By - {header.deployedBy}")
    print(f"Retrieval Date - {header.retrievalTime}")
    print(f"Checked By - {header.checkedBy}")
    print(f"Input Date - {header.inputDate}")
    print(f"Notes - {header.notes}")
    print(f"Manta Presence - {header.mantaPresence}")
    print(f"No. of Manta Sightings - {header.noMantas}")
    print(f"No. of Mantas Identified - {header.noIdentifiedMantas}")