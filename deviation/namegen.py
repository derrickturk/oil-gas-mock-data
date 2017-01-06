# Horizontal wellbore mock deviation survey generator
# (c) 2016 Derrick W. Turk | terminus data science, LLC

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import random

FORMATIONS = [
        'Wolfmother',
        'Whitesnake',
        'Showerfruit',
        'Hawk Dodge',
        'Los Garbanzos',
]

FIRST_NAMES = [
        'Cedric',
        'Sanda',
        'King',
        'Iraida',
        'Cordell',
        'Barney',
        'Roseline',
        'Rodrigo',
        'Antonette',
        'Veta',
        'Christie',
        'Elvis',
        'Carlyn',
        'Deeann',
        'Edna',
        'Lyndsay',
        'Perry',
        'Sanjuanita',
        'Dominga',
        'Patsy',
]

LAST_NAMES = [
        'Lamarre',
        'Maddy',
        'Chaney',
        'Hilson',
        'Nold',
        'Parkerson',
        'Schofield',
        'Nemeth',
        'Nevers',
        'Hanby',
        'Ravenscroft',
        'Grant',
        'Joye',
        'Mencer',
        'Gauer',
        'Smedley',
        'Hickman',
        'Northam',
        'Smyers',
        'Caron',
]

MAX_WELL_NUM = 23

def well_names(n, prob_ranch=0.2, prob_estate=0.2):
    first = [random.choice(FIRST_NAMES) for _ in range(n)]
    last = [random.choice(LAST_NAMES) for _ in range(n)]
    ranch = [' Ranch' if random.random() <= prob_ranch else '' for _ in first]
    estate = [' Estate' if not r and random.random() <= prob_estate else ''
            for r in ranch]
    num = [' ' + str(random.randrange(MAX_WELL_NUM) + 1) + 'H' for _ in first]
    return (f + ' ' + l + r + e + n
            for (f, l, r, e, n) in zip(first, last, ranch, estate, num))

def formation_names(n, num_formations=len(FORMATIONS)):
    if num_formations <= len(FORMATIONS):
        formations = FORMATIONS[:num_formations]
    else:
        letter = 'A'
        formations = []
        while len(formations) < num_formations:
            take = min(len(FORMATIONS), num_formations - len(formations))
            formations += [f + ' ' + letter for f in FORMATIONS[:take]]
            letter = chr(ord(letter) + 1)
    return [random.choice(formations) for _ in range(n)]
