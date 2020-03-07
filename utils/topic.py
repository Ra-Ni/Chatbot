from http.client import RemoteDisconnected
from json import loads, load
from typing import Union
from urllib.parse import quote

from urllib3.connection import HTTPConnection

from utils import prefixes, rdf_converter
from utils.nordvpn import NordVPNClient
from utils.progress_bar import ProgressBar


def parse(target: Union[str, bytes, int], output: Union[str, bytes, int]) -> None:
    owl_prefix, owl_acronym = prefixes.OWL
    _, course_acronym = prefixes.COURSE

    uri = 'api.dbpedia-spotlight.org'
    path = '/en/annotate'
    headers = {'Host': uri,
               'User-Agent': 'Conupedia Extractor',
               'Accept': 'application/json',
               'Accept-Language': 'en-US, en; q=0.5',
               'Accept-Encoding': 'gzip, deflate, br',
               'Origin': 'https://www.dbpedia-spotlight.org',
               'DNT': '1',
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
    response = None
    status_code = None
    nordvpn = NordVPNClient()
    threshold = 5
    cache = []

    with open(target, 'r') as reader:
        json_form = load(reader)

    content_list = json_form['@graph']
    progress_bar = ProgressBar(len(content_list))

    for item in content_list:
        progress_bar.console_update()
        course = item['@id']
        description = item['description']
        description = description.replace(' ', '+')
        description = quote(description, safe='+')

        body['text'] = description
        string_body = [f'{key}={value}' for key, value in body.items()]
        string_body = '&'.join(string_body)
        headers['Content-Length'] = str(len(string_body))

        for i in range(threshold):
            request.request('POST', path, body=string_body, headers=headers)
            try:
                response = request.getresponse()
                status_code = response.status

                if status_code == 200:
                    response = response.read().decode('UTF-8')
                    response = loads(response)
                    break
            except RemoteDisconnected:
                pass

            request.close()
            nordvpn.connect()
            request.connect()

        if status_code != 200:
            print(f'ignored {course}.')
            continue

        buffer = set()
        try:
            for x in response['Resources']:
                buffer.add(x['@URI'])
        except KeyError:
            pass

        if buffer:
            buffer = ';\n'.join([f'\t{owl_acronym}:sameAs <{uri}>' for uri in buffer])
            cache.append(f'\n\n<{course}>\n{buffer}.')

    with open(output, 'w') as writer:
        writer.write(''.join(cache))

    nordvpn.reset()


if __name__ == '__main__':
    target = '../assets/Descriptions'
    output = '../assets/Topics.ttl'
    rdf_converter.fetch(f'{target}.ttl', f'{target}.json')
    parse(f'{target}.json', output)
