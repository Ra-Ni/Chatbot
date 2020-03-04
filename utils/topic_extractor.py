from http.client import HTTPConnection
from json import loads
from urllib.parse import quote

CRLF = '\r\n'

API_URL = 'api.dbpedia-spotlight.org'
API_PATH = '/en/annotate'

HEADERS = {
    'Host': API_URL,
    'User-Agent': 'Extractor',
    'Accept': 'application/json',
    'Accept-Language': 'en-US, en; q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Origin': 'https://www.dbpedia-spotlight.org',
    'DNT': 1,
    'Connection': 'closed',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    'Content-Length': None
}

BODY = {
    'text': None,
    'confidence': 0.35,
    'support': 0,
    'spotter': 'Default',
    'disambiguator': 'Default',
    'policy': 'whitelist',
    'types': '',
    'sparql': ''
}


def run(course_id, description: str, resource) -> None:
    encoded_description = description.replace(' ', '+')
    encoded_description = quote(encoded_description, safe='+')
    BODY['text'] = encoded_description

    body = [f'{key}={value}' for key, value in BODY.items()]
    body = '&'.join(body)

    HEADERS['Content-Length'] = len(body)

    request = HTTPConnection(API_URL, 80)
    request.request('POST', API_PATH, body=body, headers=HEADERS)

    response = request.getresponse()
    response_dictionary = response.read().decode('UTF-8')
    response_dictionary = loads(response_dictionary)

    buffer = []

    try:
        for x in response_dictionary['Resources']:
            uri = x['@URI']
            if uri not in buffer:
                buffer.append(uri)
    except KeyError:
        pass

    request.close()

    if buffer:
        buffer = '\n'.join([f'\towl:sameAs <{uri}>' for uri in buffer])
        resource.write(f'Course:{course_id}\n{buffer}\n')
