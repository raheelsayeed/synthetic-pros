#!/usr/bin/env python3 

#--------------------------
# CHART  PRO Resources to Patient
# Raheel Sayeed
# -------------------------

import json, os, time, random, csv, numpy


def getListOfFiles(dirName):
    # create a list of file and sub directories 
    # names in the given directory 
    listOfFile = os.listdir(dirName)
    allFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        # If entry is a directory then get the list of files in this directory 
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFiles(fullPath)
        else:
            allFiles.append(fullPath)
                
    return allFiles       

if __name__ == '__main__':
    files = getListOfFiles('final_output')
    resources = []
    for ff in files:
        with open (ff, 'r') as json_data:
            resource = json.load(json_data)
            resources.append(resource)
            json_data.close()
    
    scores = [resource['extension'][2]['extension'][2]['valueDecimal'] for resource in resources]
    dates  = [resource['authored'] for resource in resources]
    
    # TODO
    # sort by scores and group by months
    # chart
    
