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
    argparser.add_argument('--mintvd', '-t', type=float, default=5000,
            help='Minimum by-formation target TVD')
    argparser.add_argument('--maxtvd', '-T', type=float, default=15000,
            help='Maximum by-formation target TVD')
    argparser.add_argument('--minlateral', '-l', type=float, default=3000,
            help='Minimum by-formation target lateral length')
    argparser.add_argument('--maxlateral', '-L', type=float, default=6000,
            help='Maximum by-formation target lateral length')
    argparser.add_argument('--tvdnoise', '-nt', type=float, default=200,
            help="TVD 'noise' (+/-)")
    argparser.add_argument('--lateralnoise', '-nl', type=float, default=100,
            help="Lateral length 'noise' (+/-)")
    argparser.add_argument('--anglenoise', '-na', type=float, default=5,
            help="Angle 'noise' (+/-, degrees)")
    argparser.add_argument('--surveynoise', '-ns', type=float, default=1,
            help="Survey 'noise' (std. dev.)")
    argparser.add_argument('--build', '-b', type=float, default=400,
            help='Build section length')
    argparser.add_argument('--step', '-s', type=float, default=1,
            help='Survey step distance')
    argparser.add_argument('--surfacetvd', '-st', type=float, default=0,
            help='Surface TVD')
    args = argparser.parse_args(argv[1:])

    wells = list(ng.well_names(args.wells))
    formations = list(ng.formation_names(args.wells, args.formations))

    frm_target_tvds = [random.uniform(-args.mintvd, -args.maxtvd)
            for _ in range(args.formations)]
    frm_target_lengths = [random.uniform(args.minlateral, args.maxlateral)
            for _ in range(args.formations)]
    frm_target_angles = [random.uniform(0, 2 * PI)
            for _ in range(args.formations)]
    frm_index = { f : i for (i, f) in enumerate(set(formations)) }

    anglenoise_rad = args.anglenoise * PI / 180
    surveys = (sg.deviation_survey(
        frm_target_tvds[frm_index[f]] +
          random.uniform(-args.tvdnoise, args.tvdnoise),
        frm_target_lengths[frm_index[f]] +
          random.uniform(-args.lateralnoise, args.lateralnoise),
        frm_target_angles[frm_index[f]] +
          (PI if random.random() > 0.5 else 0) +
          random.uniform(-anglenoise_rad, anglenoise_rad),
        noise_sd=args.surveynoise, surface_tvd=args.surfacetvd,
        step=args.step, build=args.build)
        for f in formations)

    offsets = [(random.uniform(-args.fieldX / 2, args.fieldX / 2),
        random.uniform(-args.fieldY / 2, args.fieldY / 2))
        for _ in range(args.wells)]

    seq = zip(wells, formations, surveys, offsets)
    output_tables(seq)

def output_tables(seq):
    print('\t'.join(('Well', 'Formation', 'x', 'y', 'z')))
    for (w, f, s, (x, y)) in seq:
        for p in s:
            print('\t'.join((w, f, str(p[0] + x), str(p[1] + y), str(p[2]))))

sys.exit(main(sys.argv))
