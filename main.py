import os
import platform
import re
import sys

from dictionaries import possibleSightingTypes, possibleSightingTypeToListDict, scientificNameDict, scientificAbbreviationDict, behaviourList
from tools import getOption, getPhotoId, checkPermissions
from imageShowing import openAllBestMantaImages
from timeFunctions import getDateOfPhoto, updateTimeVariables, checkRecentSightings, checkSimultaneousSightings
from data import Data
from dataframe import addSightingToDataframe, updateRowWithNewInfo, saveDataframe, printDataframe
from sighting import Sighting, printSightingInfo
from manageOutputPhotos import manageOutputPhotos
from header_dataframe import addHeaderInfo
from saveProgress import saveGame, loadGame

# Loading screen
from lamaveAscii import printLamaveAscii
printLamaveAscii()
print("\nLoading Lamave Image Classification, please wait.")


def chooseFolderForClassification(data):
    directory = os.path.join(data.exe_dir, 'input/')

    print(f"\nLooking for photos to analyse within directory {directory}.")

    # Define the pattern using regular expressions
    pattern = r'\d{4}-[A-Za-z]{3}-\d{2}_SIP_RUV\d+_ST\d+(_[A-Za-z]+)?'

    # Check if the directory exists
    if not os.path.exists(directory):
        print(f"The directory '{directory}' does not exist.")
        print(f"Stopping code - please ensure {directory} exists and has relevant data.")
        return False

    possibleFoldersToChooseOG = os.listdir(directory)
    possibleFoldersToChoose = []

    for folder in possibleFoldersToChooseOG:
        if re.fullmatch(pattern, folder):
            # print(f"{folder} matches the format")
            possibleFoldersToChoose.append(folder)
        else:
            # print(f"{folder} does not match the format")
            pass
    
    possibleFoldersToChoose.sort()
    print(f'Found {len(possibleFoldersToChoose)} folder(s) with correct naming convention.')
    if possibleFoldersToChoose == []:
        print(f"\nNo relevant folders found in directory {directory}. \nFolder names should be in format: \nyyyy-mmm-dd_SIP_RUVx_STy \n2022-Sep-06_SIP_RUV3_ST3 \n")
        print(f"Please ensure {directory} contains relevant data with correctly named folders. Stopping code.")
        return False
    
    print("\nWhich folder would you like to to analyse?")
    choice = getOption(possibleFoldersToChoose)

    splitDirectory = choice.split("_")
    data.date = splitDirectory[0]
    data.ruv = splitDirectory[2]
    data.site = splitDirectory[3]

    data.parentFolder = choice
    goProSubFolders = os.listdir(os.path.join(directory, choice))
    for subFolder in goProSubFolders:
        if(subFolder[0] == "."):
            continue
        path = directory + choice + "/" + subFolder
        if os.path.isdir(path):
            data.goproFolders.append(directory + choice + "/" + subFolder)
    
    if len(data.goproFolders) == 0:
        print(f"\nNo sub folders found inside {data.parentFolder}. Please make sure there are images inside sub folders, example:")
        print(f">>> {data.exe_dir}/{data.parentFolder}/100GOPRO/G0056001.JPG")

        print("Stopping code")
        return False
    
    return True

def requestPhotoInfo(data):
    sighting = Sighting(data.sightingsHandled, data.site, data.checkedBy)

    print("\nWhat type of animal have you seen?")
    sightingType = getOption(possibleSightingTypes)

    # if exiting game
    if(sightingType == possibleSightingTypes[-1]):
        addHeaderInfo(data)
        manageOutputPhotos(data)
        return data, False

    # if pausing to continue later
    if(sightingType == possibleSightingTypes[-2]):
        print("\nPausing here, quitting code.")
        return data, False

    # if type with no options, just go straight through
    if possibleSightingTypeToListDict[sightingType] is None:
        sighting.sightingOf = sightingType
    else:
        print("\nWhat type of", sightingType, "have you seen?")
        sighting.sightingOf = getOption(possibleSightingTypeToListDict[sightingType])
    
    sighting.species = scientificNameDict[sighting.sightingOf]

    if(sighting.sightingOf in ["Reef Manta Ray", "Oceanic Manta Ray"]):
        sighting.isManta = True
        data.haveSeenManta = True

    print("\nWhat photo ID did it enter the sighting? ie G00xxxxx")
    startPhotoPath, sighting.startPhotoId, sighting.startPhotoNumber = getPhotoId(data)

    print("\nWhat photo ID did it leave the sighting? ie G00xxxxx")
    endPhotoPath, sighting.endPhotoId, sighting.endPhotoNumber = getPhotoId(data, minNumber=sighting.startPhotoNumber)
    sighting.uniqueSightingGroups.append([sighting.startPhotoNumber, sighting.endPhotoNumber])

    # update time variables for sighting
    updateTimeVariables(data, sighting)

    simultaneousSightings = checkSimultaneousSightings(data, sighting)
    if(simultaneousSightings != []):
        print("Updating simultaneous sightings")
        updateSimultaneousSightings(data, sighting, simultaneousSightings)

        
    # check here whether there was another sighting of the same non-manta animal within 10 mins
    previousSightings = checkRecentSightings(data, sighting)
    if previousSightings != []:
        if not sighting.isManta:
            updatePreviousSighting(data, previousSightings, sighting)
            return data, True
        else:
            while True:
                print("Is this the same manta as one of these previously seen within 10 minutes?")
                mantaList = []
                bestIdList = []
                for prevSighting in previousSightings:
                    mantaList.append(prevSighting.mantaIdWithUnknown)
                    bestIdList.append(prevSighting.bestPhotoId)
                mantaList.append("New manta")                
                mantaList.append("Open images")
                option = getOption(mantaList)

                # allow user to open best images of previous mantas to help with identification
                if option == "Open images":
                    #showBestMantas(data)
                    openAllBestMantaImages(data)
                else:
                    break

            # continue as usual
            if(option != "New manta"):
                index = mantaList.index(option)
                previousSighting = previousSightings[index]
                updatePreviousSighting(data, previousSighting, sighting)

                # print(previousSighting.ided)
                if(previousSighting.ided == "No"):
                    print("\nPrevious viewings of this manta was not identifiable")
                    updateMantaIDs(data, previousSighting)
                
                # for each sighting, if the current sighting is a simultaneous, replace with the old sighitng of this animal
                for eachSighting in data.sightings:
                    if sighting in eachSighting.simultaneousSightings:
                        eachSighting.simultaneousSightings.remove(sighting)
                        if previousSighting not in eachSighting.simultaneousSightings:
                            eachSighting.simultaneousSightings.append(previousSighting)

                # updateAssociations(data, previousSighting, simultaneousSightings)
                createFileName(data, previousSighting)
                for simultaneousSighting in previousSighting.simultaneousSightings:
                    # updateAssociations(data, simultaneousSighting, simultaneousSighting.simultaneousSightings)
                    createFileName(data, simultaneousSighting)
                    updateRowWithNewInfo(data.df, simultaneousSighting)                

                updateRowWithNewInfo(data.df, previousSighting)
                # printSightingInfo(previousSighting)
                return data, True

    print("\nWhat photo ID provides the best ID'able image in this sighting? ie G00xxxxx")
    bestPhotoPath, sighting.bestPhotoId, bestPhotoNumber = getPhotoId(data, minNumber=sighting.startPhotoNumber, maxNumber=sighting.endPhotoNumber)
    sighting.bestPhotoIdNoJpg = sighting.bestPhotoId.split(".")[0]

    print("\nWhat behaviour is the animal exhibiting?")
    sighting.behaviour = getOption(behaviourList)

    if not (sighting.isManta):
        sighting.noIndividuals = askForIndividuals()

    if sighting.isManta: 
        updateMantaIDs(data, sighting)

    addNotes(sighting)
    addDate(data, sighting)

    createFileName(data, sighting)
    for simultaneousSighting in sighting.simultaneousSightings:
        createFileName(data, simultaneousSighting)
        updateRowWithNewInfo(data.df, simultaneousSighting)

    data.sightings.append(sighting)
    addSightingToDataframe(data.df, sighting)
    
    return data, True
    # printSightingInfo(sighting)
    # print("\nSighting info is as above, would you like to commit these changes to the database or delete this input?")
    # option = getOption(["Save changes", "Delete sighting"])
    # if option == "Save changes":
    #     saveGame(data)
    # else:
    #     print("Deleting sighting and loading data from previous entry.")
    #     data = loadGame(data)
    #     print(data.sightingsHandled)

    # return data, True

def addDate(data, sighting):
    sighting.date = getDateOfPhoto(data, sighting.bestPhotoId)

def addNotes(sighting):
    print("\nWould you like to add any notes about this sighting?")
    yesNo = getOption(["Yes", "No"])
    if(yesNo == "Yes"):
        print("Please write your notes and hit enter:")
        sighting.notes = input("-- ")
        # sighting.notes = f'"{notes}"'

def updateMantaIDs(data, sighting):
    idOutput = tryToIdManta()
    if(idOutput):
        sighting.ided = "Yes"
        sighting.idnumber = idOutput
    else:
        sighting.ided = "No"

    count = returnStrCountOfAnimal(data, sighting)
    if sighting.ided == "Yes":
        sighting.mantaIdWithUnknown = sighting.idnumber + count
    else:
        sighting.mantaIdWithUnknown = "manta" + count

def updateSimultaneousSightings(data, currentSighting, simultaneousSightings):
    simultaneousSightings.append(currentSighting)
    for sighting in simultaneousSightings:
        for sighting2 in simultaneousSightings:
            if sighting == sighting2:
                continue
            if sighting2 not in sighting.simultaneousSightings:
                sighting.simultaneousSightings.append(sighting2)
    
# def updateAssociations(data, currentSighting, simultaneousSightings):
#     for sighting in simultaneousSightings:
#         for sighting2 in simultaneousSightings:
#             if sighting == sighting2:
#                 continue
#             if(sighting2.mantaIdWithUnknown not in sighting.associations):
#                 sighting.associationsList.append(sighting2.mantaIdWithUnknown)
#                 sighting.associations += sighting2.mantaIdWithUnknown + ","

def askForIndividuals():
    print("\nHow many individuals of this animal are in this sighting?")
    while True:
        user_input = input('-- ')
        if user_input.isdigit() and len(user_input) < 5:
            number = int(user_input)
            if(number > 0):
                return number
            else:
                print("Invalid input. Please enter a valid number (1-9999)")
        else:
            print("Invalid input. Please enter a valid number (1-9999)")

def returnStrCountOfAnimal(data, sighting):
    count = 1
    for prevSighting in data.sightings:
        # ignore same sighting, needed for if a sighting is updating with new info
        if(prevSighting == sighting):
            continue
        # check that you've seen the same thing
        if(sighting.sightingOf == prevSighting.sightingOf):
            #if check IDs of mantas match
            if(sighting.isManta):
                if(sighting.ided == "Yes"):
                    if(sighting.idnumber == prevSighting.idnumber):
                        count += 1
                else:
                    # if not id'd, increase
                    if(prevSighting.ided == "No"):
                        count += 1
            else:
                count += 1
    
    if(sighting.isManta):
        if(sighting.ided == "No"):
            # always return the number, including for 1, nothing around it
            return str(count)
    
    # else return number only if more than 1
    if(count > 1):
        return "(" + str(count) + ")"

    return ""

def createFileName(data, sighting):
    sighting.associations = ""
    sighting.associationsList = []
    if(sighting.isManta):
        # logic for mantas
        sighting.fileName = sighting.date + "_SIP_" + data.ruv + "_" + sighting.bestPhotoIdNoJpg + "_" 
        if(sighting.ided == "Yes"):
            sighting.fileName += sighting.idnumber
        else:
            sighting.fileName += "manta"
        sighting.fileName += returnStrCountOfAnimal(data, sighting)
        for simultaneousSighting in sighting.simultaneousSightings:
            sighting.fileName += "_"
            sighting.fileName += simultaneousSighting.mantaIdWithUnknown.split("-")[-1]
            
            # also add to associations
            if sighting.associations != "":
                sighting.associations += ","
            
            sighting.associations += simultaneousSighting.mantaIdWithUnknown
        # print(sighting.fileName)
    else:
        # logic for all other animals
        sighting.fileName = sighting.date + "_SIP_" + data.ruv + "_" + sighting.bestPhotoIdNoJpg + "_" + scientificAbbreviationDict[sighting.sightingOf]
        sighting.fileName += returnStrCountOfAnimal(data, sighting)

def tryToIdManta():
    print("\nAre you able to identify this manta ray?")
    yesNo = getOption(["Yes", "No"])
    if(yesNo == "Yes"):
        identificationCode = userInputMantaId()
        return identificationCode
    else:
        return False

def userInputMantaId():
    print("\nWhat is this identification code for this manta? ie for PW-MA-0046, just enter 46")
    while True:
        user_input = input('-- ')
        if user_input.isdigit() and len(user_input) < 5:
            number = int(user_input)
            if(number > 0):
                formatted_number = '{:04d}'.format(number)
                mantaId = "PW-MA-" + formatted_number
                return mantaId
            else:
                print("Invalid input. Please enter a valid number (1-9999)")
        else:
            print("Invalid input. Please enter a valid number (1-9999)")

def updatePreviousSighting(data, prevSighting, currentSighting):
    print("\nUpdating previous sighting with this information")
    prevSighting.endPhotoId = currentSighting.endPhotoId
    prevSighting.endPhotoNumber = currentSighting.endPhotoNumber
    prevSighting.uniqueSightingGroups.append(currentSighting.uniqueSightingGroups[0])
    updateTimeVariables(data, prevSighting)

    print("\nDo you want to update the best ID'able image ID?")
    yesNo = getOption(["Yes", "No"])
    if(yesNo == "Yes"):
        print("\nWhat photo ID provides the best ID'able image in this sighting? ie G00xxxxx")
        bestPhotoPath, prevSighting.bestPhotoId, bestPhotoNumber = getPhotoId(data, prevSighting.startPhotoNumber, prevSighting.endPhotoNumber)
        prevSighting.bestPhotoIdNoJpg = prevSighting.bestPhotoId.split(".")[0]
        createFileName(data, prevSighting)

    # add  simultaenous sightings from current to prev if manta
    if(currentSighting.isManta):
        for simultaneousSighting in currentSighting.simultaneousSightings:
            if simultaneousSighting not in prevSighting.simultaneousSightings:
                prevSighting.simultaneousSightings.append(simultaneousSighting)
        return

    updateRowWithNewInfo(data.df, prevSighting)
    printSightingInfo(prevSighting)

def printPreviousSighting(data):
    if(data.sightingsHandled > 0):
        printDataframe(data)
        lastSighting = data.sightings[-1]
        print(f"\nThe last sighting input was a {lastSighting.sightingOf} which left the frame on photo ID {lastSighting.endPhotoId}")

def checkAllInputPhotos(data):
    while True:
        printPreviousSighting(data)
        data.sightingsHandled += 1
        data, entry = requestPhotoInfo(data)
        if(entry == False):
            saveDataframe(data)
            break
        data = checkSave(data)
        saveDataframe(data)
        print("\nCurrently there are", str(len(data.sightings)), "entries of sighting data.")

def findRootDir(data):
    # Get the path to the directory containing the executable
    if(getattr(sys, 'frozen', False) or hasattr(sys, '_MEIPASS')):
        # if running as exe
        # this logic may need to change if no longer building as onefile
        exe = sys.executable
        data.splitChar = "\\" if platform.system() == "Windows" else "/"
        split = exe.split(data.splitChar)[:-1]
        exe_dir = ""
        for directory in split:
            exe_dir += directory + data.splitChar
        data.exe_dir = os.path.join(exe_dir)
    else:
        # if running as local python script
        exe_dir = os.path.dirname(os.path.abspath(__file__))
        data.exe_dir = exe_dir
    print(f"Running script from root directory: {data.exe_dir}")

def checkInitialFolders(data):
    # Check if the directory exists
    print("\nChecking required directories exist.")
    directories = ["input", "output"]
    for directory in directories:
        dirName = os.path.join(data.exe_dir, directory)
        if not os.path.exists(dirName):
            print(f"The directory '{dirName}' does not exist, creating.")
            os.mkdir(dirName)
    print("All required directories exist.")

def getInitials(data):
    while True:
        initials = input("Please enter your initials for the collection (2 or 3 characters): ").strip().upper()
        
        if len(initials) >= 2 and len(initials) <= 3 and initials.isalpha():
            break
        else:
            print("Invalid input. Please enter 2 or 3 letters, all letters.")
    
    data.checkedBy = initials
    print("Your initials are:", initials)

def checkSave(data):
    sighting = data.sightings[-1]
    printSightingInfo(sighting)
    print("\nSighting info is as above, would you like to commit these changes to the database or delete this input?")
    option = getOption(["Save changes", "Delete sighting"])
    if option == "Save changes":
        saveGame(data)
    else:
        print("Deleting sighting and loading data from previous entry.")
        data = loadGame(data)

    return data

def checkLoad(data):
    filesInDir = os.listdir(data.exe_dir)
    # print(filesInDir)
    if "saveData.pickle" in filesInDir:
        loadData = loadGame(data)
        if len(loadData.sightings) == 0:
            return data, False
        print(f"\nFound previous save data for folder {loadData.parentFolder} with {len(loadData.sightings)} sightings, would you like to continue from here?")
        if getOption(["Yes", "No"]) == "Yes":
            return loadData, True
    return data, False

def main():
    data = Data()
    print(f"Version number is {data.version}")
    findRootDir(data)
    
    if not checkPermissions(data.exe_dir):
        input("") 
        return
    
    # check whether loading previous save
    data, loadBool = checkLoad(data)
    if not loadBool:
        checkInitialFolders(data)
        if not chooseFolderForClassification(data):
            input("")
            return
        getInitials(data)
    else:
        saveGame(data)
    
    # createDateFolders(data)
    checkAllInputPhotos(data)

if __name__ == "__main__":
    main()
    