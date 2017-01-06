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

def main(argv):
    if len(argv) < 2 or len(argv) > 3:
        print('Usage: python -m {} num-wells [num-formations]'.format(
            deviation.__name__), file=sys.stderr)
        return 0

    n_wells = int(argv[1])
    n_formations = int(argv[2]) if len(argv) == 3 else 1

    wells = ng.well_names(n_wells)
    formations = ng.formation_names(n_wells, n_formations)

    for (w, f) in zip(wells, formations):
        print('{}: {} formation'.format(w, f))

sys.exit(main(sys.argv))
