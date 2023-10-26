import pandas as pd
import os

# Define the column names
column_names = [
    "Database ID",
    "Date",
    "Species",
    "File Name",
    "Time appearence",
    "Time leave",
    "Elapsed time",
    "Behavior",
    "IDed",
    "ID number",
    "Notes",
    "Number of Indiv",
    "Site",
    "Location",
    "Method",
    "Inputted by",
    "Latest check date",
    "Associations"
]

def createDataframe():
    # Create an empty DataFrame with the specified column names
    df = pd.DataFrame(columns=column_names)
    return df

def addSightingToDataframe(df, sighting):
    new_row_values = [
        sighting.databaseId,
        sighting.date,
        sighting.species,
        sighting.fileName,
        sighting.timeAppear,
        sighting.timeEnd,
        sighting.elapsedTime,
        sighting.behaviour,
        sighting.ided,
        sighting.idnumber,
        sighting.notes,
        sighting.noIndividuals,
        sighting.site,
        sighting.location,
        sighting.method,
        sighting.inputtedBy,
        sighting.latestCheckDate,
        sighting.associations
    ]

    df.loc[df.shape[0]] = new_row_values
    # print(df)

def updateRowWithNewInfo(df, sighting):
    new_row_values = [
        sighting.databaseId,
        sighting.date,
        sighting.species,
        sighting.fileName,
        sighting.timeAppear,
        sighting.timeEnd,
        sighting.elapsedTime,
        sighting.behaviour,
        sighting.ided,
        sighting.idnumber,
        sighting.notes,
        sighting.noIndividuals,
        sighting.site,
        sighting.location,
        sighting.method,
        sighting.inputtedBy,
        sighting.latestCheckDate,
        sighting.associations
    ]

    index = df[df["Database ID"] == sighting.databaseId].index
    df.loc[index] = new_row_values

def saveDataframe(data):
    file_name = data.date + '.csv'
    outputFile = os.path.join(data.exe_dir, "output/", file_name)
    # data.df = data.df.drop(columns="Database ID")

    data.df.to_csv(outputFile, index=False)

def printDataframe(data):
    print(data.df)