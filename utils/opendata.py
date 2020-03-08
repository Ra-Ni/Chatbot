"""
OpenData module connects to Concordia's Opendata platform and uses API calls to fetch information about courses

---------
Variables
---------

API_USER:
    Your API username.

API_Password:
    Your API password.

-------
Methods
-------

fetch(path: str) -> dict:
    Creates a GET request with the path parameter included.
    Returns a dictionary object of json format.
"""

from json import loads

import requests
from requests.auth import HTTPBasicAuth

# todo we need to remove this before we go public.
API_USER = '295'
API_PASSWORD = '50cb40a1af0752086248f8b05b1f88b5'


def fetch(path: str):
    if not API_USER or not API_PASSWORD:
        raise PermissionError

    response = requests.get(f'https://opendata.concordia.ca/API/v1{path}',
                            auth=HTTPBasicAuth(API_USER, API_PASSWORD))

    json_form = loads(response.text)
    return json_form
