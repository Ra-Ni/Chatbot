"""
The session class is responsible for interfacing with the server (http://conupedia.sytes.net) and the chat bot.

It simplifies the process of sending sparql queries by calling the submit method and specifying a custom query that
respects the SPARQL syntax.

"""

from http.client import HTTPConnection
from urllib.parse import quote

from json import loads


class Session:

    def __init__(self):
        self._path = '/sparql'

        self._method = 'GET'

        self._headers = {
            'Host': 'conupedia.sytes.net',
            'User-Agent': 'Query',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US, en; q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'DNT': '1',
            'Connection': 'closed',
            'Upgrade-Insecure-Requests': '1',
            'Origin': 'http://conupedia.sytes.net',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache'
        }

        temp_params = {
            'default-graph-uri': '',
            'should-sponge': '',
            'format': 'application%2Fsparql-results%2Bjson',
            'timeout': '0',
            'debug': 'on',
            'query': '',
        }

        buffer = []

        for key, value in temp_params.items():
            buffer.append(f'{key}={value}')

        self._params = '&'.join(buffer)

    def submit(self, query='select * where {?s ?p ?o.} limit 100'):

        request = HTTPConnection(self._headers['Host'], 80)

        new_query = quote(query.replace(' ', '+'), safe='+')
        new_params = f'{self._params}{new_query}'

        request.request(self._method, f'{self._path}?{new_params}', headers=self._headers)
        response = request.getresponse()

        if response.status != 200:
            request.close()
            raise ValueError('Invalid query parameter sent.')

        content = response.read().decode('utf-8')
        request.close()

        json_t = loads(content)['results']['bindings']

        for dictionary in json_t:
            for key in dictionary.keys():
                yield key, dictionary[key]['value']


if __name__ == '__main__':
    # First create a session
    session = Session()
    # Call submit if you want to query something remotely.
    query = """select * 
    where {
    ?ID rdf:type schema:Course .
    } limit 100"""

    response = session.submit(query)

    # The response is a generator/iterator that returns a tuple
    for item in response:
        print(item)
