#!/usr/bin/env python3 

#--------------------------
# Assign PRO Resources to Patient
# Raheel Sayeed
# -------------------------


import json, time, os, calendar, random, csv


def randomdate(_year, month):
    dates = calendar.Calendar().itermonthdates(_year, month)
    return random.choice([date for date in dates if date.month == month])


def write_to_file(json_data, filename):
    with open(filename, 'w') as output:
        dumps = json.dumps(json_data, sort_keys=False, indent=4)
        output.write(dumps)
        output.close()

# 1. Rename all files and add an extension with a t-score also remove and replace id.
def organizefiles(dirname):
    import os
    files = os.listdir(dirname)
    for filename in files:
        filepath = f'{dirname}/{filename}' 
        with open(filepath) as json_data:
            qresponse = json.load(json_data)
            json_data.close()
            theta = qresponse['extension'][2]['extension'][0]['valueDecimal']
            stderror = qresponse['extension'][2]['extension'][1]['valueDecimal']
            tscore = (theta * 10) + 50.0
            print(f'{theta}: {stderror} ---> {tscore}')
            qresponse['extension'][2]['extension'].append({
                    "url": "tscore",
                    "valueDecimal": tscore
                })
            print(qresponse['extension'][2]['extension'][2]['valueDecimal'])
            write_to_file(qresponse, f'I____{dirname}/{dirname}_{filename}')




def patients_csv():
    with open('output/p16-18.csv', newline='') as csvfile:
        pts = csv.reader(csvfile, delimiter=',')
        return [row[0] for row in pts]

def create_dir(dirname):
    try: 
        os.system(f'rm -rf {dirname}')
        # os.mkdir(dirname)
        os.makedirs(dirname)
    except OSError:
        print(f'could not create dir: {dirname}')

# ---------------------------------------------------
# List of Mild QuestionnaireResponses

def mild_responses():
    return get_responses(['mild'])

def mod_severe_responses():
    return get_responses(['moderate', 'severe'])

def mod_responses():
    return get_responses(['moderate'])


def get_responses(categories):
    filenames = []
    for cat in categories:
        files = os.listdir(f'output/{cat}') # Grab from output directory
        flist = [f'{cat}/{fn}' for fn in files]
        filenames.extend(flist)
    return filenames
# ---------------------------------------------------

def assign(q_responses, patient_id, authored_month, year, outputdirectory):
    qr = random.choice(q_responses)
    head, filename = os.path.split(qr)
    json_dict = None
    with open(f'output/{qr}') as json_data:
        json_dict = json.load(json_data)
        json_data.close()


    #assign to questionnaire response
    json_dict['subject'] = f'Patient/{patient_id}'
    json_dict['authored'] = str(randomdate(year, authored_month))
    outputfilepath = f'{outputdirectory}/{year}/{filename}'
    write_to_file(json_dict, outputfilepath)
    return outputfilepath

def synthesize_for(patient_csv_instance, year, mild_percentage, range_responses_permonth, outputdirectory):

    create_dir(outputdirectory)
    create_dir(f'{outputdirectory}/{year}')
    
    # patient lists
    pts = patient_csv_instance
    try:
        pts.remove('fhirid')
    except:
        pass

    # number of patients
    pt_count = len(pts) 
    print(f'Number of patients: {pt_count}')
    
    # assessments each month range for one year
    total_number_of_responses = 0
    for _month in range(1,13):
   
        monthly_assessments = random.randrange(range_responses_permonth[0], range_responses_permonth[1])
        mild_count = round(monthly_assessments *  mild_percentage)
        severe_count = monthly_assessments - mild_count
        mild_responses = get_responses(['mild'])
        severe_responses = get_responses(['severe', 'verysevere'])
        moderate_responses = get_responses(['moderate', 'severe'])
        
        print(f'Month: {_month}, (Count: {monthly_assessments}) Mild: {mild_count}, Severe: {severe_count}')

        
        # round 1  
        # mild / Normal
        for response_count in range(1, mild_count+1):
 
            pt = random.choice(pts)
            pts.remove(pt)
            assign(mild_responses, pt, _month, year, outputdir)
            total_number_of_responses += 1
        
        # moderate / severe
        for response_count in range(1, severe_count+1):

            pt = random.choice(pts)
            pts.remove(pt)
            assign(severe_responses, pt, _month, year, outputdir)
            total_number_of_responses += 1
            
            next_month = random.randint(1, 3)
            assign(moderate_responses, pt, next_month, year,  outputdir)
            total_number_of_responses += 1
    

    print(f'Operation completed, New QRs assigned: {total_number_of_responses}')


if __name__ == '__main__':

    # output directory 
 
    year = 2018
    mild_percentage = 0.8
    outputdir = 'final_output2'
    range_responses_permonth = (4,6)

    create_dir(outputdir)
    create_dir(f'{outputdir}/{year}')
    
    # patient lists
    pts = patients_csv()

    # number of patients
    pt_count = len(pts) 
    print(f'Number of patients: {pt_count}')
    
    # assessments each month range for one year
    total_number_of_responses = 0
    for year in [2017, 2018]:
        print(f'************** {year} ****************')
        synthesize_for(patients_csv(), year, mild_percentage, range_responses_permonth, outputdir)
    







    



