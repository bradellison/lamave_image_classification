import dataframe
from header_dataframe import Header, createHeader
from versionNumber import version_number

class Data:
    def __init__ (self):
        # self.app = None
        # self.model = None
        self.version = version_number

        self.df = dataframe.createDataframe()
        self.header = Header()
        self.headerdf = createHeader()
        self.sightingsHandled = 0;

        self.exe_dir = None
        self.parentFolder = ""
        self.goproFolders = [];
        self.splitChar = "/"

        self.date = None;
        self.ruv = None;
        self.site = None;
        self.checkedBy = ""

        self.sightings = []  

        self.haveSeenManta = False