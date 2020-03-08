import json
import re
import typing

from utils import prefixes, opendata
from utils.progress_bar import ProgressBar


def fetch(output: typing.Union[str, bytes, int]) -> None:
    json_form = opendata.fetch("/course/description/filter/*")
    with open(output, 'w') as writer:
        json.dump(json_form, writer, indent=4)


def parse(target: typing.Union[str, bytes, int], output: typing.Union[str, bytes, int]) -> None:
    cpc_p, cpc_ns = prefixes.CPC
    schema_p, schema_ns = prefixes.SCHEMA

    with open(target, 'rb') as reader:
        raw_data = json.load(reader)
        progress_bar = ProgressBar(len(raw_data))

    # establish and write prefix URIs
    with open(output, 'w') as writer:
        writer.write(f'{cpc_p}\n{schema_p}')

        # Creating tuples
        for course in raw_data:
            progress_bar.console_update()
            # removing references to grad/ugrad calendars
            description = re.sub("(Please|See) .*alendar\.*|(PLEASE )?SEE .*DAR(\.)?", "", course["description"])
            # Removing other strange strings from descriptions
            description = re.sub("\*\*\*(PLESE)*", "", description)
            description = re.sub("\*VID\*\n*\*KEYB\*\n|\*VID\*\n|\*(CNT|APP)\*", "", description)
            # Removing unwanted spaces, newlines, quotation marks and other unconventional punctuation
            description = re.sub("\"|\*|\n|\r|^ |~*|<.*>", "", description)
            # The notes in the description are useless, and so are the prerequisities
            description = re.sub("(IMPORTANT )?NOTE(S)?(:|-).*|Note(s)?(:|-).*", "", description)
            description = re.sub("Prerequisite.*?[\.!\?](?:\s|$)", "", description)
            description = re.sub("(?i).*(Students who have taken).*", "", description)

            if description != "":
                description = re.sub("(\t|\r\n|\n)", "", description)
                description = re.sub('\\\\', "", description)
                writer.write(f'\n\n<{cpc_ns}:{course["ID"]}>\n\t{schema_ns}:description \"{description}\" .')


if __name__ == '__main__':
    target = '../assets/Descriptions'

    fetch(f'{target}_Raw.json')
    parse(f'{target}_Raw.json', f'{target}.ttl')
