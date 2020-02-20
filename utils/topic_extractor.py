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

TARGET_PATH = None

def extract(course_id, description: str) -> None:
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
    # todo something
    print(f'Course:{course_id}')
    try:
        for x in response_dictionary['Resources']:
            # what to do?
            topic = x['@surfaceForm']
            topic = topic.replace(' ', '_')
            url = x['@URI']

            print(f'\tCourse:describes <{url}>')

    except KeyError:
        pass

    request.close()

extract(0, "In this applied learning experience, students select a topic related to\ntheir area of interest and carry out a research project in collaboration with faculty\nsupervisors, or managers in for-profit and non-profit organizations. The student\ncarries out the project using the appropriate methodology, writes a research report,\nand gives an oral presentation at the end of the term. The course allows students to develop their skills while providing a useful service to practitioners, deepening their understanding of key areas in management, and building a career-enhancing\nprofessional network.")
