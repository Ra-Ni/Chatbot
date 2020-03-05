import os
from random import randint


class NordVPNClient:
    COUNTRIES = [
        'Albania',
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
        'France',
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
