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
from math import sqrt, sin, cos

BUILD_FT = 200

def jitter(pts, noise_sd):
    for p in pts:
        yield tuple(v + random.gauss(0, noise_sd) for v in p)

def deviation_survey(tvd, lat_length, angle, noise_sd = 1,
        surface_tvd = 0, step = 1):
    x = 0
    y = 0
    z = 0
    survey = list()

    while z > tvd:
        survey.append((x, y, z))
        z = z - step

    hz_distance = 0
    x_step = step * cos(angle)
    y_step = step * sin(angle)
    while hz_distance < lat_length:
        survey.append((x, y, z))
        hz_distance = sqrt(x ** 2 + y ** 2)
        x += x_step
        y += y_step

    return jitter(survey, noise_sd)
