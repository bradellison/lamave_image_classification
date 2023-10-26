import os
import time
from datetime import datetime, timedelta
import tools

def updateTimeVariables(data, sighting):
    sighting.timeAppear = getTimeOfPhoto(data, sighting.startPhotoId)
    sighting.timeEnd = getTimeOfPhoto(data, sighting.endPhotoId)
    sighting.elapsedTime, _ = elapsedTimeBetweenTimes(sighting.timeAppear, sighting.timeEnd)

def getTimeOfPhoto(data, photoId):
    # return modified time of photo
    photo_path = tools.photoPathForId(data, photoId)
    modification_time = os.path.getmtime(photo_path)
    formatted_time = time.strftime('%H:%M:%S', time.localtime(modification_time))
    return formatted_time

def getDateOfPhoto(data, photoId):
    # return modified time of photo
    photo_path = tools.photoPathForId(data, photoId)
    modification_time = os.path.getmtime(photo_path)
    formatted_time = time.strftime('%H:%M:%S', time.localtime(modification_time))
    formatted_date = time.strftime('%Y-%b-%d', time.localtime(modification_time))
    return formatted_date

def elapsedTimeBetweenTimes(time_str1, time_str2):
    # Define the two time strings in '%H:%M:%S' format
    # Parse the time strings into datetime objects
    time_format = '%H:%M:%S'
    time1 = datetime.strptime(time_str1, time_format)
    time2 = datetime.strptime(time_str2, time_format)
    # print(f"time1 {time1} and time2 {time2}")

    # Calculate the time difference
    time_difference = time2 - time1

    # Convert the time difference to minutes
    minutes_difference = time_difference.total_seconds() / 60

    # format time diff
    time_difference_formatted = str(timedelta(minutes=minutes_difference))

    # print(f"Minutes between the two times: {time_difference_formatted} minutes")
    return time_difference_formatted, minutes_difference

def checkRecentSightings(data, currentSighting):
    print("\nChecking for recent sightings")
    previousSightings = []
    for prevSighting in data.sightings:
        if prevSighting in currentSighting.simultaneousSightings:
            continue

        time_difference_formatted, time_difference = elapsedTimeBetweenTimes(prevSighting.timeEnd, currentSighting.timeAppear)
        if(time_difference < 10 and time_difference > -10):
            if(prevSighting.sightingOf == currentSighting.sightingOf):
                split = time_difference_formatted.split(":")
                minutes = split[1]
                seconds = split[2]

                if not currentSighting.isManta:
                    print(f"Your last sighting of this animal was within 10 minutes: {minutes}m{seconds}s passed")
                    return prevSighting
                
                previousSightings.append(prevSighting)

    print(f"Found {len(previousSightings)} previous sightings of this animal within 10 minutes")
    return previousSightings

def checkSimultaneousSightings(data, currentSighting):
    if(currentSighting.isManta == False):
        return []

    print("\nChecking for simultaneous sightings of manta rays")
    simultaneousSightings = []
    for prevSighting in data.sightings:
        if not prevSighting.isManta:
            continue
        for occurrence in prevSighting.uniqueSightingGroups:
            # if photo numbers indicate that the views overlap
            if((currentSighting.startPhotoNumber >= occurrence[0] and currentSighting.startPhotoNumber <= occurrence[1]) 
            or (currentSighting.endPhotoNumber >= occurrence[0] and currentSighting.endPhotoNumber <= occurrence[1])):
                print("Simultaneous viewing found")
                simultaneousSightings.append(prevSighting)
                # add to prev sighting also if not already there
                # if currentSighting not in prevSighting.simultaneousSightings:
                #     prevSighting.simultaneousSightings.append(currentSighting)



    print(f"Found {len(simultaneousSightings)} simultaneous sightings")
    return simultaneousSightings