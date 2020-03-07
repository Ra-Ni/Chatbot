"""
The purpose of NordVPNClient is to bypass API call limitations set by dbpedia spotlight.
It serves as a wrapper class for NordVPN commands installed as a command-line application.

----------
Variables
----------

COUNTRIES:
    A list of strings representing the name of the country.
    The list contains filtered countries that were selected from the set of countries offered by NordVPN.

--------
Methods
--------

connect() -> None:
    Connects to a NordVPN session with the next country in the list.
    The public IP Address of the device will be that which is provided by the application.

reset() -> None:
    Disconnects from the NordVPN session.
    Reverts to the default public IP address of the device.
"""

from random import randint
from subprocess import check_call


class NordVPNClient:
    COUNTRIES = [
        'Germany',
        'Norway',
        'Argentina',
        'Greece',
        'Poland',
        'Australia',
        'Portugal',
        'Austria',
        'Hungary',
        'Romania',
        'Belgium',
        'Iceland',
        'Serbia',
        'Bosnia_And_Herzegovina',
        'Slovakia',
        'Bulgaria',
        'Ireland',
        'South_Africa',
        'Canada',
        'Israel',
        'South_Korea',
        'Chile',
        'Italy',
        'Spain',
        'Costa_Rica',
        'Sweden',
        'Croatia',
        'Latvia',
        'Switzerland',
        'Cyprus',
        'Luxembourg',
        'Taiwan',
        'Czech_Republic',
        'Malaysia',
        'Thailand',
        'Denmark',
        'Mexico',
        'Turkey',
        'Estonia',
        'Moldova',
        'Ukraine',
        'Finland',
        'United_Kingdom',
        'United_States',
        'Georgia',
        'North_Macedonia',
    ]

    def __init__(self):
        self._max = len(NordVPNClient.COUNTRIES)
        self.current_country = randint(0, self._max - 1)

    def connect(self):
        check_call(['nordvpn', 'connect', f'{NordVPNClient.COUNTRIES[self.current_country]}'], stdout=None)
        self.current_country = (self.current_country + 1) % self._max

    def reset(self):
        check_call(['nordvpn', 'disconnect'], stdout=None)
        self.current_country = randint(0, self._max - 1)
