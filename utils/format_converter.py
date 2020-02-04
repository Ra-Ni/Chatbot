"""
A converter for different file paths that are given.

It supports ttl, xml, and json formatting.

for help, run python format_converter.py -h
"""

from argparse import ArgumentParser
from http.client import HTTPConnection
from os.path import isfile
from urllib.parse import quote

parser = ArgumentParser(description='Converts one format to another using HTTP requests.')
parser.add_argument('path', metavar='PATH', type=str,
                    help='relative or absolute path of file including the extension.')
parser.add_argument('--ext', dest='ext', default='xml',
                    help='extension to convert to: ttl, xml, json. Defaults to xml.')
args = parser.parse_args()


def converter_error(msg):
    print(parser.print_help())
    print(f'\n\n\033[91m Error: {msg} \033[0m')
    exit(-1)


if not isfile(args.path):
    converter_error(f'File "{args.path}" does not exist.')

if not ('.ttl' or '.json' or '.xml' in args.path):
    converter_error(f'File "{args.path}" must contain an extension')

ext_form = {'json': 'application%2Fld%2Bjson',
            'ttl': 'text%2Fturtle',
            'xml': 'application%2Frdf%2Bxml'}

headers = {'Host': 'rdfvalidator.mybluemix.net',
           'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
           'Content-Length': None}

init_format = ext_form[args.path[args.path.rfind('.') + 1:]]
end_format = ext_form[args.ext]
new_file_path = args.path[:args.path.rfind('.') + 1] + args.ext

f = open(args.path, 'r')
body = f.readlines()
f.close()

body = ''.join(body)
body = body.replace('\n', '\r\n')
body = body.replace(' ', '+')
body = quote(body, safe='+')
body = 'content=' + body + f'&from={init_format}&to={end_format}'

headers['Content-Length'] = len(body)

request = HTTPConnection(headers['Host'], 80)
request.request('POST', '/validate', body=body, headers=headers)

response = request.getresponse()
status = response.status
response = response.read().decode('utf-8')
request.close()

if status != 200:
    converter_error('Server did not accept the format presented. Check for syntax/format errors')

f = open(new_file_path, 'w')
f.write(response)
f.close()

print(f'\033[32m Successfully converted results to "{new_file_path}" \033[0m')
exit(0)
