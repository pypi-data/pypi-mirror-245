#!/usr/bin/env python

import sys
import pysam


def is_bam(fn):
    for f in fn.split(','):
        try:
            bam = pysam.AlignmentFile(f)
        except:
            return False

    return True


print(is_bam(sys.argv[1]))
