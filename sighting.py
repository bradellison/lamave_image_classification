from datetime import datetime

class Sighting:
    def __init__(self, databaseId, site, checkedBy):
        # non scientificName
        self.databaseId = databaseId

        self.sightingOf = "Reef Manta Ray"
        self.animalGroup = "Mobula Ray"
        self.isManta = False
        self.numberSightingOfDay = 1;
        
        self.startPhotoNumber = 12345
        self.endPhotoNumber = 23456
        self.startPhotoId = "G0012345.JPG"
        self.endPhotoId = "G0023456.JPG"
        self.bestPhotoId = "G0034567.JPG"
        self.bestPhotoIdNoJpg = "G0034567"

        self.uniqueSightingGroups = []
        self.simultaneousSightings = []
        self.mantaIdWithUnknown = ""

        self.date = ""
        self.species = ""
        self.fileName = ""
        self.timeAppear = 0
        self.timeEnd = 10
        self.elapsedTime = 0
        self.behaviour = ""
        self.ided = "NA"
        self.idnumber = "NA"
        self.notes = ""
        self.noIndividuals = 1
        self.site = site
        self.location = "Sibaltan"
        self.method = "RUV"
        self.inputtedBy = checkedBy
        self.latestCheckDate = datetime.today().date().strftime('%d/%m/%Y')

        self.associationsList = []
        self.associations = ""


def printSightingInfo(sighting):
    print("\nPrinting information for sighting")

    print("date:", sighting.date)
    print("species:", sighting.species)
    print("fileName:", sighting.fileName)
    print("timeAppear:", sighting.timeAppear)
    print("timeEnd:", sighting.timeEnd)
    print("elapsedTime:", sighting.elapsedTime)
    print("behaviour:", sighting.behaviour)
    print("ided:", sighting.ided)
    print("idnumber:", sighting.idnumber)
    print("notes:", sighting.notes)
    print("noIndividuals:", sighting.noIndividuals)
    print("site:", sighting.site)
    print("location:", sighting.location)
    print("method:", sighting.method)
    print("inputtedBy:", sighting.inputtedBy)
    print("latestCheckDate:", sighting.latestCheckDate)
    print("associations:", sighting.associations)