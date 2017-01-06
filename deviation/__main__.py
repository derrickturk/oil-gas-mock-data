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

import deviation
import deviation.namegen as ng
import deviation.surveygen as sg

import random
from math import pi as PI

def main(argv):
    if len(argv) < 2 or len(argv) > 5:
        print(('Usage: python -m {} num-wells [num-formations] ' +
            '[fieldX] [fieldY]').format(deviation.__name__), file=sys.stderr)
        return 0

    n_wells = int(argv[1])
    n_formations = int(argv[2]) if len(argv) >= 3 else 1
    field_x = float(argv[3]) if len(argv) >= 4 else 50000
    field_y = float(argv[4]) if len(argv) >= 5 else 50000

    wells = list(ng.well_names(n_wells))
    formations = list(ng.formation_names(n_wells, n_formations))

    frm_target_tvds = [random.uniform(-5000, -15000)
            for _ in range(n_formations)]
    frm_target_lengths = [random.uniform(3000, 6000)
            for _ in range(n_formations)]
    frm_target_angles = [random.uniform(0, 2 * PI)
            for _ in range(n_formations)]
    frm_index = { f : i for (i, f) in enumerate(set(formations)) }

    surveys = (sg.deviation_survey(
        frm_target_tvds[frm_index[f]] + random.uniform(-200, 200),
        frm_target_lengths[frm_index[f]] + random.uniform(-100, 100),
        frm_target_angles[frm_index[f]] + random.uniform(-PI / 16, PI / 16))
        for f in formations)

    offsets = [(random.uniform(-field_x / 2, field_x / 2),
        random.uniform(-field_y / 2, field_y / 2))
        for _ in range(n_wells)]

    for (w, f, s, (x, y)) in zip(wells, formations, surveys, offsets):
        print('{}: {} formation'.format(w, f))
        for p in s:
            print((p[0] + x, p[1] + y, p[2]))

sys.exit(main(sys.argv))
