
possibleSightingTypes = [
    'Mobula Ray',
    'Other Ray',
    'Turtle',
    'Shark',
    'Dugong',
    'Humanity',
    'Pause: Save information and return later to complete',
    'Exit: All photos analysed',
]

possibleSightingTypesOnly = [
    'Mobula Ray',
    'Other Ray',
    'Turtle',
    'Shark',
    'Dugong',
    'Diver',
]

possibleMobula = [
    'Reef Manta Ray',
    'Oceanic Manta Ray',
    'Pygmy Devil Ray',
    'Spine-Tail Devil Ray',
    'Unknown Mobula'
]

possibleTurtle = [
    'Hawksbill Turtle',
    'Green Sea Turtle',
    'Unknown Turtle',
]

possibleOtherRay = [
    'Eagle Ray',
    'Blue-Spotted Sting Ray',
    'Honeycomb Ray',
    'Marble Ray',
    'Unknown Ray',
]

possibleShark = [
    'Thresher Shark',
    'Black-Tip Reef Shark',
    'Scalloped Hammerhead Shark',
    'Whale Shark',
    'White-Tip Reef Shark',
    'Unknown Shark',
]

possibleHumanity = [
    'Diver',
    'Freediver',
    'Boat',
    'Other'
]

possibleDugong = [
    'Dugong'
]

possibleSightingTypeToListDict = {
    'Mobula Ray': possibleMobula,
    'Other Ray': possibleOtherRay,
    'Turtle': possibleTurtle,
    'Shark': possibleShark,
    'Dugong': possibleDugong,
    'Humanity': possibleHumanity,
}

scientificNameDict = {
    'Reef Manta Ray':'Mobula alfredi',
    'Oceanic Manta Ray':'Mobula birostris',
    'Pygmy Devil Ray':'Mobula eregoodootenkee',
    'Spine-Tail Devil Ray':'Mobular japanica',
    'Unknown Mobula':'Unknown mobula',
    'Eagle Ray':'Aetobatus narinari',
    'Blue-Spotted Sting Ray':'Neotrygon kuhlii',
    'Honeycomb Ray':'Himantura uarnak',
    'Marble Ray':'Taeniurops meyeni',
    'Unknown Ray':'Unknown ray',
    'Hawksbill Turtle':'Eretmochelys imbricata',
    'Green Sea Turtle':'Chelonia mydas',
    'Unknown Turtle':'Unknown turtle',
    'Thresher Shark':'Alopias vulpinus',
    'Black-Tip Reef Shark':'Carcharhinus melanopterus',
    'Scalloped Hammerhead Shark':'Sphyrna lewini',
    'Whale Shark':'Rhincodon typus',
    'White-Tip Reef Shark':'Triaenodon obesus',
    'Unknown Shark':'Unknown shark',
    'Dugong':'Dugong dugon',
    'Diver':'Diver',
    'Freediver':'Freediver',
    'Boat':'Boat',
    'Other':'Humanity'
}

scientificAbbreviationDict = {
    'Reef Manta Ray':'M.alfredi',
    'Oceanic Manta Ray':'M.birostris',
    'Pygmy Devil Ray':'M.eregoodootenkee',
    'Spine-Tail Devil Ray':'M.japanica',
    'Unknown Mobula':'U.mobula',
    'Eagle Ray':'A.narinari',
    'Blue-Spotted Sting Ray':'N.kuhlii',
    'Honeycomb Ray':'H.uarnak',
    'Marble Ray':'T.meyeni',
    'Unknown Ray':'U.ray',
    'Hawksbill Turtle':'E.imbricata',
    'Green Sea Turtle':'C.mydas',
    'Unknown Turtle':'U.turtle',
    'Thresher Shark':'A.vulpinus',
    'Black-Tip Reef Shark':'C.melanopterus',
    'Scalloped Hammerhead Shark':'S.lewini',
    'Whale Shark':'R.typus',
    'White-Tip Reef Shark':'T.obesus',
    'Unknown Shark':'U.shark',
    'Dugong':'D.dugon',
    'Diver':'Diver',
    'Freediver':'Freediver',
    'Boat':'Boat',
    'Other':'Humanity'    
    }

behaviourList = [
    "Travel",
    "Avoidance",
    "Cleaning",
    "Courtship",
    "Foraging",
    "Mobile",
    "Immobile",
    "Undetermined"
    ]