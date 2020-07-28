#!/usr/bin/env python3 

#--------------------------
# Synthetic PRO Generator
# Raheel Sayeed
# -------------------------

import base64, json, urllib.request, urllib.response
from random import randint
from configparser import ConfigParser


config = ConfigParser() 
config.read('credentials.txt') 


endpoint = config.get('endpoint', 'demo')
accessidentifier  = config.get('basic', 'identifier')
accesssecret = config.get('basic', 'token')



class response_handler(object): 

    def __init__(self, code):
        if code == 'rand':
            self.code = ['mild', 'moderate', 'severe'][randint(0,2)] 
        else:
            self.code = code 
   
    def select_response(self):
        if self.code == 'mild':
            return randint(0,1) 
        if self.code == 'moderate':
            return randint(1,3)
        if self.code == 'severe':
            return randint(2,4) 
        else:
            return -1

    def answer_print(self):
        print(f'{self.code}: {self.select_response()}')
        print(self.select_response()) 



class adaptive_client(object): 

    # intializer
    def __init__(self, access_token, access_secret): 
        self.identifier = access_token
        self.secret = access_secret 
        self.base_url = endpoint
        self.response_handler = response_handler("rand") 
        self.response_resource = None 
        self.question_serial = 0 

        # url request
        self.request = urllib.request

    def perform_request(self,  endpoint, postData=None):
        string = '%s:%s' % (self.identifier, self.secret)
        encoded = string.encode() # utf_8
        base64string = base64.b64encode(encoded)
        authstring = 'Basic %s' % base64string.decode() # utf_8
        url = urllib.parse.urljoin(self.base_url, endpoint)
        print(url)
        req = self.request.Request(url)
        req.add_header("Authorization", authstring)
        req.add_header("Content-Type", "application/json; charset=utf-8")
        req.get_method = lambda: 'POST'
        
        jsonbytes = None 
        if postData is not None:
            json_data = json.dumps(postData)
            jsonbytes = json_data.encode('utf-8')
            req.add_header('Content-Length', len(jsonbytes))
        result = urllib.request.urlopen(req, jsonbytes).read()
        jsondict = json.loads(result.decode())
        if jsondict is not None:
           return jsondict
        else:
            return None


class empty_questionnaireresponse:

    @staticmethod
    def new(filename):
        with open(filename) as json_data:
            json_dict = json.load(json_data)
            return json_dict if not None else None

class instrument_session(object):

    def __init__(self, questionnaire_fhir_id, client=adaptive_client):

        # Client to make and reeive calls
        self.client = client
        # Questionnaire ID
        self.questionnaire_id = questionnaire_fhir_id
        # question serial number
        self.serial = 0 
        #  total number of questions
        self.quesitons = 0



    def begin_session(self, answerlevel=None):
        make_request = self.client.perform_request(f'Questionnaire/{self.questionnaire_id}/next-q', empty_questionnaireresponse.new('empty_questionnaireresponse.json'))
        d = len(make_request['contained'])
        
        new_question = make_request['contained'][0]['date']
        print(d)
        print(new_question)

        
        
                

   

if __name__ == '__main__':
    print("PROMIS Synthetic Generator")
    ac = adaptive_client(accessidentifier, accesssecret) 
    ac.response_handler.answer_print()

    # Depression
    depression_fhirid = '96FE494D-F176-4EFB-A473-2AB406610626'
    instrument = instrument_session(depression_fhirid, ac) 
    instrument.begin_session()
    
    # print(empty_questionnaireresponse.new('empty_questionnaireresponse.json'))
