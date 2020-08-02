#!/usr/bin/env python3 

#--------------------------
# Synthetic PRO Generator
# Raheel Sayeed
# -------------------------

import base64, json, urllib.request, urllib.response, time, os
from random import randint
from configparser import ConfigParser

# Credentials
config = ConfigParser() 
config.read('credentials.ini') 
endpoint = config.get('endpoint', 'demo')
accessidentifier  = config.get('basic', 'identifier')
accesssecret = config.get('basic', 'token')

# Depression
depression_fhirid = '96FE494D-F176-4EFB-A473-2AB406610626'
answerlevel = 'verysevere'
delay = 10    

def write_to_file(json_data, filename):
    with open(filename, 'w') as output:
        dumps = json.dumps(json_data, sort_keys=False, indent=4)
        output.write(dumps)
        output.close()

def create_dir(dirname):
    try: 
        os.system(f'rm -rf {dirname}')
        os.mkdir(dirname)
    except OSError:
        print(f'could not create dir: {dirname}')

class response_handler(object): 

    def __init__(self, code):
        self.code = code 
   
    def select_response(self):
        if self.code == 'mild':
            return randint(0,1) 
        if self.code == 'moderate':
            return randint(1,3)
        if self.code == 'severe':
            return randint(2,4) 
        if self.code == 'verysevere':
            return randint(3,4)
        if self.code == 'normal':
            return 0
        if self.code == 'absolute':
            return 4
        else:
            return -1

   
class adaptive_client(object): 

    # intializer
    def __init__(self, access_token, access_secret): 
        self.identifier = access_token
        self.secret = access_secret 
        self.base_url = endpoint
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

    def __init__(self, questionnaire_fhir_id, client=adaptive_client, resp_handler=None):

        # Client to make and reeive calls
        self.client = client
        # Questionnaire ID
        self.questionnaire_id = questionnaire_fhir_id
        # question serial number
        self.serial = 0 
        #  total number of questions
        self.quesitons = 0

        # auto response type
        self.answer_handler = resp_handler or response_handler('rand')

    def select_answer_foritem(self, questionitem):
        subitems = questionitem['item']
        subitem = questionitem['item'][1]
        answerchoices = [choice['valueCoding'] for choice in subitem['answerOption']]
        selected_choice = answerchoices[self.answer_handler.select_response()]
        answer_item = {
                "linkId": questionitem['linkId'],
                "item": [{
                    "linkId": subitem['linkId'],
                    "text": subitem['text'],
                    "answer": [
                            {
                                "valueCoding" : selected_choice
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

    def get_next_question(self, response):

        # Get Latest question item
        questionitems = response['contained'][0]['item']
        self.questions = len(questionitems)
        self.serial += 1
        newQuestionIndex = 0
        new_question = questionitems[newQuestionIndex]

        # Select new Answer
        answer = self.select_answer_foritem(new_question)
        response['item'].insert(0, answer) 
        return  self.client.next_q(self.questionnaire_id, response)




        
if __name__ == '__main__':
    print("PROMIS Synthetic Generator")
    print(f'Instrument: {depression_fhirid}')
    answer_handler = response_handler(answerlevel)
    print(f'synthesizing answer level: {answer_handler.code}')
    create_dir(answerlevel)
    print(f'Output director: {answerlevel}')
    ac = adaptive_client(accessidentifier, accesssecret) 
    for i in range(1, 100):

        instrument = instrument_session(depression_fhirid, ac, answer_handler)
        questionnaireresponse = instrument.start_survey()
        completed = False
        while completed is not True:
            time.sleep(delay)
            questionnaireresponse = instrument.get_next_question(questionnaireresponse)
            status = questionnaireresponse['status']
            if status == 'completed':
                os.system('echo -n .')
                completed = True
                write_to_file(questionnaireresponse, f'{answerlevel}/{i}_{answerlevel}_QuestionnaireResponse.json')


    
