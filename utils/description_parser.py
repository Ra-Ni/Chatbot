import json
import re


def parse_descriptions(target, output):
    with open(target, 'rb') as reader:
        raw_data = json.load(reader)

        # establish and write prefix URIs
        with open(output, 'w') as writer:
            writer.write("@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>.")

            # Creating tuples
            for course in raw_data:
                print(f"Parsing: {course['ID']}")

                # remove all prereqs from the description
                description = re.sub("Prerequisite.*\.", "", course["description"])
                # The notes in the description are useless too
                description = re.sub("NOTE|Note:.*\.", "", description)
                description = description.replace('\n', '')

                if description != "":
                    writer.write(f'\n\nCourse:{course["ID"]}\n\trdfs:comment \"{description}\".')
