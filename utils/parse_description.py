import json
import re
import typing

from utils import prefixes


def parse_descriptions(target: typing.Union[str, bytes, int], output: typing.Union[str, bytes, int]) -> None:
    rdfs_prefix, rdfs_acronym = prefixes.RDFS
    course_prefix, course_acronym = prefixes.COURSE

    with open(target, 'rb') as reader:
        raw_data = json.load(reader)

        # establish and write prefix URIs
        with open(output, 'w') as writer:
            writer.write(f'{rdfs_prefix}\n{course_prefix}')

            # Creating tuples
            for course in raw_data:
                print(f"Parsing: {course['ID']}")

                # remove all prereqs from the description
                description = re.sub("Prerequisite.*\.", "", course["description"])
                # The notes in the description are useless too
                description = re.sub("NOTE|Note:.*\.", "", description)


                if description != "":
                    description = re.sub("\t|\r\n|\n", "", description)
                    writer.write(f'\n\n{course_acronym}:{course["ID"]}\n\t{rdfs_acronym}:comment \"{description}\".')

if __name__ == '__main__':
    parse_descriptions('../assets/description.json', '../assets/CourseDescriptions.txt')