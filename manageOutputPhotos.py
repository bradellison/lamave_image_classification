import os
import platform
import tools
import shutil

def createDateFolders(data):
    dateName = data.date + "_SIP_" + data.ruv + "_" + data.site

    os.makedirs(os.path.join(data.exe_dir, "output", dateName, "other"), exist_ok=True)
    os.makedirs(os.path.join(data.exe_dir, "output", dateName, "manta"), exist_ok=True)

def getOutputFolder(data, sighting):
    dateFolder = sighting.date + "_SIP_" + data.ruv + "_" + data.site + "/"
    baseDir = os.path.join(data.exe_dir, "output", dateFolder)

    if sighting.isManta:
        newDir = os.path.join(baseDir, "manta", sighting.fileName)
    else:
        newDir = os.path.join(baseDir, "other", sighting.fileName)

    return newDir

def manageOutputPhotos(data):
    print("\nCreating folders and moving photos:")
    # createDateFolders(data)
    for sighting in data.sightings:
        newDir = getOutputFolder(data, sighting)
        os.makedirs(newDir, exist_ok=True)
        photosCopied = 0
        photosToCopy = 0
        for group in sighting.uniqueSightingGroups:
            photosToCopy += group[1] - group[0] + 1

        for group in sighting.uniqueSightingGroups:
            for i in range(group[0], group[1] + 1):
                photoId = "G00" + str(i) + ".JPG"
                photoPath = tools.photoPathForId(data, photoId)
                if not photoPath:
                    continue
                photosCopied += 1
                copyPhoto(photoPath, newDir)
                print(f"\r{sighting.fileName}: Copied {photosCopied}/{photosToCopy} photos", end='', flush=True)                
        
        # print("", flush=False)
                
            # print(f"{sighting.fileName}: Copied {photosCopied} photos")
            
        # move best photo again and rename to parent dir
        bestPhotoId = sighting.bestPhotoId
        bestPhotoPath = tools.photoPathForId(data, bestPhotoId)
        copyPhoto(bestPhotoPath, newDir, renameToParent=True, sightingFileName = sighting.fileName)
        print(", duplicated best image", flush=False)

    print("\nCSV saved and images moved into the outputs folder. Exiting code.")

def copyPhoto(source_file, destination_folder, renameToParent = False, sightingFileName = ""):
    try:
        # Get the filename from the source path
        originalFileName = os.path.basename(source_file)

        # Create the destination path by joining the destination folder and the filename
        if(renameToParent):
            destination_path = os.path.join(destination_folder, sightingFileName + ".JPG")
        else:
            destination_path = os.path.join(destination_folder, originalFileName)

        try:
            shutil.copy(source_file, destination_path)
        except Exception as e:
            print(f"Error copying file: {str(e)}")

        # print(f"File '{source_file}' copied to '{destination_folder}'.")
    except FileNotFoundError:
        print("Source file not found.")
    except PermissionError:
        print("Permission denied. You may need administrator privileges.")
    except Exception as e:
        print(f"An error occurred: {e}")