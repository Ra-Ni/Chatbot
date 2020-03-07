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

import os
from random import randint


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
        'Singapore',
        'Brazil',
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
        'Japan',
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
        'Netherlands',
        'United_Kingdom',
        'New_Zealand',
        'United_States',
        'Georgia',
        'North_Macedonia',
    ]

    def __init__(self):
        self._max = len(NordVPNClient.COUNTRIES)
        self.current_country = randint(0, self._max - 1)

    def connect(self):
        os.system(f'nordvpn connect {NordVPNClient.COUNTRIES[self.current_country]}')
        self.current_country = (self.current_country + 1) % self._max

    def reset(self):
        os.system(f'nordvpn disconnect')
        self.current_country = 0
