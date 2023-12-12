#!/usr/bin/env python

import sys

with open(sys.argv[1]) as _:
    for line in _:
        c = line.strip().split()
        if c[4] != 'WG_10kbp':
            c[4] = 'EPD'

        print('\t'.join(c))
