import json
import re


def parse_descriptions(target, output):
    with open(target, 'rb') as file:
        raw_data = json.load(file)

        # establish and write prefix URIs
        out = open(output, "w")
        out.write("@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>.")

        # Creating tuples
        for course in raw_data:
            print("Parsing: " + course["ID"])

            description = re.sub("Prerequisite.*\.", "",
                                 course["description"])  # remove all prereqs from the description
            description = re.sub("NOTE|Note:.*\.", "", description)  # The notes in the description are useless too
            description = description.replace('\n', '')

            if description != "":
                out.write(f'\n\nCourse:{course["ID"]}\n\trdfs:comment \"{description}\".')
