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

import sys
import argparse

import deviation
import deviation.namegen as ng
import deviation.surveygen as sg

import random
from math import pi as PI

def main(argv):
    argparser = argparse.ArgumentParser(
            description='Generate mock horizontal wellbore deviation surveys.',
            prog='python -m {}'.format(deviation.__name__))
    argparser.add_argument('wells', type=int, help='Number of wellbores')
    argparser.add_argument('--formations', '-f', type=int, default=1,
            help='Number of distinct formations')
    argparser.add_argument('--fieldX', '-x', type=float, default=50000,
            help='Field dimensions (X)')
    argparser.add_argument('--fieldY', '-y', type=float, default=50000,
            help='Field dimensions (Y)')
    args = argparser.parse_args(argv[1:])

    wells = list(ng.well_names(args.wells))
    formations = list(ng.formation_names(args.wells, args.formations))

    frm_target_tvds = [random.uniform(-5000, -15000)
            for _ in range(args.formations)]
    frm_target_lengths = [random.uniform(3000, 6000)
            for _ in range(args.formations)]
    frm_target_angles = [random.uniform(0, 2 * PI)
            for _ in range(args.formations)]
    frm_index = { f : i for (i, f) in enumerate(set(formations)) }

    surveys = (sg.deviation_survey(
        frm_target_tvds[frm_index[f]] + random.uniform(-200, 200),
        frm_target_lengths[frm_index[f]] + random.uniform(-100, 100),
        frm_target_angles[frm_index[f]] + random.uniform(-PI / 16, PI / 16))
        for f in formations)

    offsets = [(random.uniform(-args.fieldX / 2, args.fieldX / 2),
        random.uniform(-args.fieldY / 2, args.fieldY / 2))
        for _ in range(args.wells)]

    for (w, f, s, (x, y)) in zip(wells, formations, surveys, offsets):
        print('{}: {} formation'.format(w, f))
        for p in s:
            print((p[0] + x, p[1] + y, p[2]))

sys.exit(main(sys.argv))
