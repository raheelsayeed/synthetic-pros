#!/usr/bin/env python3 

#--------------------------
# Synthetic PRO Generator
# Raheel Sayeed
# -------------------------

import base64, json, urllib.request, urllib.response, time
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


    def next_q(self, questionnaire_id, post_data=None):
        return self.perform_request(f'Questionnaire/{questionnaire_id}/next-q', postData=post_data)





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

    def select_answer_foritem(self, questionitem, answerlevel=None):
        subitems = questionitem['item']
        subitem = questionitem['item'][1]
        answer_item = {
                "linkId": questionitem['linkId'],
                "item": [{
                    "linkId": subitem['linkId'],
                    "text": subitem['text'],
                    "answer": [
                            {
                                "valueCoding" : {
                                    "system": "http://loinc.org",
                                    "code": "LA10044-8",
                                    "display": "Often"
                                }
                            }
                        ]
                    }],
                "extension": questionitem['extension']
                }
        return answer_item
        
    def start_survey(self):
        empty_qr = empty_questionnaireresponse.new('empty_questionnaireresponse.json')
        response = self.client.next_q(self.questionnaire_id, empty_qr) 
        return response

    def get_next_question(self, response, answerlevel=None):

        # Get Latest question item
        questionitems = response['contained'][0]['item']
        self.questions = len(questionitems)
        print(f'number of questions: {self.questions}')
        self.serial += 1
        print(f'serial: {self.serial}')
        newQuestionIndex = 0
        new_question = questionitems[newQuestionIndex]

        # Select new Answer
        answer = self.select_answer_foritem(new_question, answerlevel)
        response['item'].insert(0, answer) 
        print(f'answers in response: {len(response["item"])}')
        return  self.client.next_q(self.questionnaire_id, response)

        
if __name__ == '__main__':
    print("PROMIS Synthetic Generator")
    ac = adaptive_client(accessidentifier, accesssecret) 
    ac.response_handler.answer_print()

    # Depression
    depression_fhirid = '96FE494D-F176-4EFB-A473-2AB406610626'
    instrument = instrument_session(depression_fhirid, ac) 
    questionnaireresponse = instrument.start_survey()
    completed = False
    while completed is not True:
        time.sleep(5)
         # Check if Survey completed
        questionnaireresponse = instrument.get_next_question(questionnaireresponse, None)
        status = questionnaireresponse['status']
        print(status)
        if status == 'completed':
            completed = True
            print(json.dumps(questionnaireresponse, indent=4, sort_keys=False))


    
