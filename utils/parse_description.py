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

                #removing references to grad/ugrad calendars
                description = re.sub ("(Please|See) .*alendar\.*|(PLEASE )?SEE .*DAR(\.)?", "", course["description"])
                # Removing other strange strings from descriptions
                description = re.sub ("\*\*\*(PLESE)*", "", description)
                description = re.sub ("\*VID\*\n*\*KEYB\*\n|\*VID\*\n|\*(CNT|APP)\*", "", description)
                #Removing unwanted spaces, newlines, quotation marks and other unconventional punctuation
                description = re.sub ("\"|\*|\n|\r|^ |~*|<.*>", "", description)
                # The notes in the description are useless, and so are the prerequisities
                description = re.sub("(IMPORTANT )?NOTE(S)?(:|-).*|Note(s)?(:|-).*", "", description)
                description = re.sub("Prerequisite.*?[\.!\?](?:\s|$)", "", description) 
                description = re.sub("(?i).*(Students who have taken).*", "", description)
                if description != "":
                    description = re.sub("\t|\r\n|\n", "", description)
                    writer.write(f'\n\n{course_acronym}:{course["ID"]}\n\t{rdfs_acronym}:comment \"{description}\".')

if __name__ == '__main__':
    parse_descriptions('../assets/description.json', '../assets/Course_Descriptions.txt')