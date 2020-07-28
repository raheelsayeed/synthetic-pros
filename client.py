#!/usr/bin/env python3 

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
        self.response_handler = response_handler("rand") 
        self.response_resource = None 
        self.question_serial = 0 


    def begin(self, fhir_id):
        pass 


   

if __name__ == '__main__':
    print("PROMIS Synthetic Generator")
    ac = adaptive_client(accessidentifier, accesssecret) 
    ac.response_handler.answer_print()

