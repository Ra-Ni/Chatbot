import rdflib
import json
import re
import os

def parse_descriptions():

    #specifying path to assets directory
    asset_path = os.path.join(os.path.dirname(__file__), '..', 'assets')

    with open(os.path.join(asset_path, 'description.json'), 'rb') as file:
        RawData = json.load(file)
        
        # establish and write prefix URIs
        out = open(os.path.join(asset_path, 'CourseDescriptions.txt'), "w")
        out.write (
            "@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>."
        ) 
        
        # Creating tuples
        for Course in RawData:
            print ("Parsing: " + Course["ID"])
            
            description = re.sub("Prerequisite.*\.", "", Course["description"])  # remove all prereqs from the description
            description = re.sub("NOTE|Note:.*\.", "", description)  # The notes in the description are useless too
            
            if description != "":
                tuples = (
                    "\n\nCourse:" + Course["ID"] + 
                    "\n\t" + "rdfs:comment " + "\"" + description.replace("\n", "") + "\"."
                    )
                out.write(tuples)
        

#Main method begins here
if __name__ == "__main__":

    parse_descriptions()
