# -*- coding: utf-8 -*-
import csv
import re
import os
import time
import itertools
import pygeoj
import json

'''
The script assumes that the .csv file (derived from the Google Form spreadsheet) is structured as follows:
column A = "Informazioni cronologiche" (date and time of when the questionnaire was filled in)
B = "Your name"
C = "Your surname"
D = "Where are you from (country)"
E = "Where are you based (address)"
F = "Describe yourself in one tweet"
G = "Your skille and competences"
H = "Language skills"
I = "Social links"
J = "Profile picture"
'''

######################################
#   MANUAL CONFIGURATION
######################################

#Change the input filename so that it matches the .csv file of the spreadsheet
gform_file = ('dati_interviste.csv')

#Change the name of the geojson output (containing the map data)
geojson_name = ('test.geojson')

#Change the name of the json file (containing the categories for filtering the map points)
json_name = ('test.json')

#Copy your Google API Key in a file named google_api.txt and save it in the same folder as this script (see included example).
g_api_key_file = open("google_api.txt")



#######################################
#   DATA COLLECTION
#######################################

#Check if the folder "images" already exists; if not, create it
'''
if os.path.exists('images/'):
    pass
else:
    os.makedirs("images/")
'''

#Start reading the csv file
with open(gform_file, 'r', newline='') as gform_file:
    file_output = pygeoj.new()
    readgform = csv.reader(gform_file, delimiter='\t')
    prog_number = itertools.count()
    json_values = []

    # Skip the first row, containing the header
    next(readgform, None)
    rows = [r for r in readgform]
    for row in rows:
        gform_nome = row[0].capitalize()
        gform_cognome = row[1].capitalize()
        gform_luogonascita = row[2]
        gform_datanascita = row[3]
        gform_intervista = row[4]
        gform_qualifica = row[5]
        gform_lat = row[6]
        gform_lon = row[7]
        cartodb_id = next(prog_number)
        

#Create the geojson output structure
        file_output.add_feature(
            geometry={
                "type":"Point",
                "coordinates":[(str(gform_lon)),(str(gform_lat))]
                },
            properties={
            "cartodb_id":str(cartodb_id),
            "name":str(gform_nome + ' ' + gform_cognome),
            "luogonascita":str(gform_luogonascita),
            "datanascita":str(gform_datanascita),
            "intervista":str(gform_intervista),
            "qualifica": str(gform_qualifica),
            "lat":str(gform_lon),
            "lon":str(gform_lat),
            })


    file_output.save(geojson_name)
