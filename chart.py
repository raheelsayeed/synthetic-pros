#!/usr/bin/env python3 

#--------------------------
# CHART  PRO Resources to Patient
# Raheel Sayeed
# -------------------------

import json, os, time, random, csv, numpy, plotly, datetime, pandas
import matplotlib.pyplot as plt

# lazily copied from stackoverflow
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
    files = getListOfFiles('final_output2')
    try:
         files.remove('final_output2/.DS_Store')
    except:
         pass
    resources = []
    for ff in files:
        with open (ff, 'r') as json_data:
             resource = json.load(json_data)
             resources.append(resource)
             json_data.close()
    
    monthlabels = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
             'August', 'September', 'October', 'November', 'December']
    scores = [resource['extension'][2]['extension'][2]['valueDecimal'] for resource in resources]
    dates  = [datetime.datetime.strptime(resource['authored'], '%Y-%m-%d') for resource in resources]

    vector = {'dates': dates, 'scores': scores}
    df = pandas.DataFrame(vector, columns = ['dates', 'scores'])
    months = df.groupby(df['dates'].dt.strftime('%m-%Y'))['scores'].mean()

    print(months)
    months.plot.line(x="Year", title="Synthesized PROs", ylim=(10, 90))
    
    plt.show()
    


    
