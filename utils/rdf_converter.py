from http.client import HTTPConnection
from typing import Union
from urllib.parse import quote


def fetch(target: Union[str, bytes, int], output: Union[str, bytes, int]) -> None:
    ext_form = {'json': 'application%2Fld%2Bjson',
                'ttl': 'text%2Fturtle',
                'xml': 'application%2Frdf%2Bxml'}

    headers = {'Host': 'rdfvalidator.mybluemix.net',
               'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
               'Content-Length': None}

    init_format = target[target.rfind('.') + 1:]
    init_format = ext_form[init_format]

    end_format = output[output.rfind('.') + 1:]
    end_format = ext_form[end_format]

    with open(target, 'r') as reader:
        contents = reader.read()

    contents = contents.replace(' ', '+')
    body = quote(contents, safe='+')
    body = 'content=' + body + f'&from={init_format}&to={end_format}'

    headers['Content-Length'] = len(body)

    request = HTTPConnection(headers['Host'], 80)
    request.request('POST', '/validate', body=body, headers=headers)

    response = request.getresponse()
    status = response.status
    response = response.read().decode('utf-8')
    request.close()

    if status != 200:
        raise ConnectionError

    with open(output, 'w') as writer:
        writer.write(response)


if __name__ == '__main__':
    target = '../assets/Descriptions'
    fetch(f'{target}.ttl', f'{target}.json')
