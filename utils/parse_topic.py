from json import loads
from re import sub
from urllib import parse
from typing import Union

from urllib3.connection import HTTPConnection

from utils import prefixes
from utils.nordvpn import NordVPNClient


def parse_topics(target: Union[str, bytes, int], output: Union[str, bytes, int]) -> None:
    owl_prefix, owl_acronym = prefixes.OWL
    _, course_acronym = prefixes.COURSE

    uri = 'api.dbpedia-spotlight.org'
    path = '/en/annotate'
    headers = {'Host': uri,
               'User-Agent': 'Extractor',
               'Accept': 'application/json',
               'Accept-Language': 'en-US, en; q=0.5',
               'Accept-Encoding': 'gzip, deflate, br',
               'Origin': 'https://www.dbpedia-spotlight.org',
               'DNT': '1',
               'Connection': 'closed',
               'Pragma': 'no-cache',
               'Cache-Control': 'no-cache',
               'Content-Length': None}
    body = {'text': None,
            'confidence': 0.35,
            'support': 0,
            'spotter': 'Default',
            'disambiguator': 'Default',
            'policy': 'whitelist',
            'types': '',
            'sparql': ''}
    request = HTTPConnection(uri, 80)
    nordvpn = NordVPNClient()
    with open(output, 'w') as writer:
        writer.write(owl_prefix)
        with open(target, 'r') as reader:

            line = reader.readline()

            while line:
                if '@prefix' in line or line == '\n':
                    line = reader.readline()
                    continue

                course = line[:-1]
                description = reader.readline()

                # this needs to be dealt with in descriptions
                if 'Please see ' in description:
                    line = reader.readline()
                    continue

                description = description[description.find("\"") + 1:-3]
                description = description.replace(' ', '+')
                description = parse.quote(description, safe='+')

                body['text'] = description

                string_body = [f'{key}={value}' for key, value in body.items()]
                string_body = '&'.join(string_body)

                headers['Content-Length'] = str(len(string_body))
                print(course, end='')

                status_code = -1

                while status_code != 200:
                    print('.', end='')
                    request.request('POST', path, body=string_body, headers=headers)
                    response = request.getresponse()

                    status_code = response.status

                    if status_code == 200:
                        response = response.read().decode('UTF-8')
                        response = loads(response)
                        print('OK')
                    else:
                        request.close()
                        nordvpn.connect()
                        request.connect()

                buffer = set()
                try:
                    for x in response['Resources']:
                        buffer.add(x['@URI'])
                except KeyError:
                    pass

                if buffer:
                    buffer = '\n'.join([f'\t{owl_acronym}:sameAs <{uri}>' for uri in buffer])
                    writer.write(f'\n\n{course}\n{buffer}')

                line = reader.readline()


if __name__ == '__main__':
    import os

    print(os.getcwd())
    parse_topics('../assets/CourseDescriptions.txt', '../assets/me.txt')
