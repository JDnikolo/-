import pymongo
from pymongo import MongoClient
import xml.etree.ElementTree as ET
from bson import json_util
import json,os
from pprint import pprint

#connect to database
client=MongoClient('localhost',27017)
db=client.local

#target directory
folders="E:\\Giannis Nikolopoulos\\Ergasia2"

#Accesses all files in subfolders of the target directory, parses them 
#via ElementTree and adds relevant data to a collection in the database.
#WARNING: This doesn't erase any existing documents in the collection.
#Use it on an empty collection to avoid data duplication.
def populate():
    for subfolders in os.listdir(folders):
        for files in os.listdir(folders+'\\'+subfolders):
            tree=ET.parse(folders+'\\'+subfolders+'\\'+files)
            conditions=tree.findall('condition')
            interventions=tree.findall('intervention')
            for vent in interventions:
                if vent.find('intervention_type').text!='Drug':
                    interventions.remove(vent)
                #else:
                    #print(vent.text)
            if interventions!=[]:
                for cond in conditions:
                    data=dict()
                    data['condition']=cond.text
                    drugs=list()
                    for vent in interventions:
                        print("Creating entry: "+data["condition"]+' - '+ vent.find('intervention_name').text.capitalize()+"in folder: "+subfolders+'.')
                        drugs.append(vent.find('intervention_name').text.capitalize())
                    data['drugs']=drugs
                    inserted=db.Studies.insert_one(data)


if __name__=='__main__':
    populate()