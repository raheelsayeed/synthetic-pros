#!/usr/bin/env python3 

#--------------------------
# Assign PRO Resources to Patient
# Raheel Sayeed
# -------------------------

import base64, json, urllib.request, urllib.response, time, os
from random import randint
from configparser import ConfigParser

# Create %% for assigning Majority Normal, Few Abnormal
# Pick: 50 from Mild, Moderate
# Pick: 10% from Severe
# Create patient list
# Loop over QR and Patient, add reference, move to next
# each patient should be assigned from 
#
