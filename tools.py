import os
# from PIL import Image, ImageFile
# ImageFile.LOAD_TRUNCATED_IMAGES = True
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

def checkPermissions(directoryPath):
   # Check if the script has the necessary permissions
    if os.access(directoryPath, os.R_OK | os.W_OK):
        return True
    
    print(f"This script needs read and write permissions in {directoryPath}.")
    print("Please move the script to a location where you have full write permissions.")
    return False

def displayOptions(options):
    for index, option in enumerate(options, start=1):
        print(f"{index} - {option}")

def getOption(options):
    while True:
        displayOptions(options)
        choice_input = input('Enter your choice: ')
        try:
            choice_input = int(choice_input)
            if 1 <= choice_input <= len(options):
                return options[choice_input - 1]
            else:
                print("Invalid input. Please enter a valid number.")
        except ValueError:
            if choice_input in options:
                return choice_input
            else:
                print("Invalid input. Please enter a valid number or option.")

def getPhotoId(data, minNumber = 0, maxNumber = 9999999):
    # QUESTION, IS THIS ALWAYS 5 DIGIT??
    while True:
        user_input = input('-- ')
        if user_input.isdigit():
            number = int(user_input)
            if(number < minNumber or number > maxNumber):
                print("Number not within valid range of", str(minNumber), "to", str(maxNumber))
                continue
            formatted_number = '{:07d}'.format(number)
            photoId = "G" + formatted_number + ".JPG"

            photoPath = photoPathForId(data, photoId)
            if(photoPath):
                return photoPath, photoId, number
            else:
                print("Photo doesn't exist")
                continue
        else:
            print("Invalid input. Please enter a valid number, up to 7 digits long.")

def photoPathForId(data, fullId):
    # print("searching for", photoId)
    for folder in data.goproFolders:
        photos = os.listdir(folder)
        for photo in photos:
            # print(photo)
            if photo.upper() == fullId.upper():
                # print("Photo exists")
                fullPath = folder + "/" + photo
                return fullPath
    print("\nCannot find photo with id", fullId)
    return False

def openAllBestMantaImages(data, currentEnterFrameId):
    print("Opening images in new plot - you must close the plot for the code to continue")
    image_paths = []
    labels = []
    handledMantas = []
    for sighting in data.sightings:
        if sighting.isManta and sighting.mantaIdWithUnknown not in handledMantas:
            handledMantas.append(sighting.mantaIdWithUnknown)
            image_paths.append(photoPathForId(data, sighting.bestPhotoId))
            labels.append(sighting.mantaIdWithUnknown)

    # Create a subplot grid
    num_images = len(image_paths)
    num_cols = 3  # You can adjust the number of columns as per your preference
    num_rows = (num_images + num_cols - 1) // num_cols

    # Create the subplots and display images with labels
    fig, axes = plt.subplots(num_rows, num_cols, figsize=(12, 8))
    axes = axes.flatten()  # Convert the 2D array of axes to a 1D array
    for i, (image_path, label) in enumerate(zip(image_paths, labels)):
        ax = axes[i]

        # Load and display the image
        img = mpimg.imread(image_path)
        ax.imshow(img)
        ax.set_title(label)
        ax.axis('off')  # Turn off axis labels

    # Hide any remaining empty subplots
    for i in range(num_images, num_rows * num_cols):
        fig.delaxes(axes[i])

    # Adjust subplot layout
    plt.tight_layout()

    # Show the plot
    plt.show()


# def openImagesWithIds(data, fullIdList, mantaList):
#     print("Opening images in new plot - you must close the plot for the code to continue")
#     image_paths = []
#     labels = []
#     for i in range(len(fullIdList)):
#         image_paths.append(photoPathForId(data, fullIdList[i]))
#         labels.append(mantaList[i] + " - " + fullIdList[i])
    
#     # Create a subplot grid
#     num_images = len(image_paths)
#     num_cols = 3  # You can adjust the number of columns as per your preference
#     num_rows = (num_images + num_cols - 1) // num_cols


#     # Create the subplots and display images with labels
#     fig, axes = plt.subplots(num_rows, num_cols, figsize=(12, 8))
#     axes = axes.flatten()  # Convert the 2D array of axes to a 1D array
#     for i, (image_path, label) in enumerate(zip(image_paths, labels)):
#         ax = axes[i]

#         # Load and display the image
#         img = mpimg.imread(image_path)
#         ax.imshow(img)
#         ax.set_title(label)
#         ax.axis('off')  # Turn off axis labels

#     # Hide any remaining empty subplots
#     for i in range(num_images, num_rows * num_cols):
#         fig.delaxes(axes[i])

#     # Adjust subplot layout
#     plt.tight_layout()

#     # Show the plot
#     plt.show()

def convertDate(dateObject):
    return dateObject.strftime("%Y-%b-%d")

def getStartDate():
    from datetime import date
    from datetime import timedelta
    today = date.today()
    print("Today is", today, "- What numeric day value are we starting from today?")
    print("For example, for 29th August, just enter 29")
    while True:
        choice = input("-- ")
        if(choice.isnumeric()):
            intChoice = int(choice)
            if(intChoice > 0 and intChoice < 32):
                print("You have provided", choice)
                for i in range(31):
                    tryDate = today - timedelta(days = i)
                    checkDate = tryDate.strftime("%d")
                    if int(checkDate) == intChoice:
                        startDate = convertDate(tryDate)
                        print("Starting from", startDate)
                        return startDate
                print("No match found")
                return None
        print("Invalid entry")             