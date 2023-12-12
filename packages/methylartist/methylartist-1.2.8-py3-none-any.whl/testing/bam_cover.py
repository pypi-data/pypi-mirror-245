#!/usr/bin/env python

import pysam
import multiprocessing as mp

def bam_cover(bam_fn, chrom, start, end):
    start = int(start)
    end = int(end)
    bam = pysam.AlignmentFile(bam_fn)

    count = 0

    for rec in bam.fetch(chrom, start, end):
        if not rec.is_duplicate:
            count += 1

    return [start, count]


def bam_bincover(bam_fn, chrom, w_starts, w_ends, procs=1):
    assert len(w_starts) == len(w_ends)

    pool = mp.Pool(processes=int(procs))
    results = []

    for start, end in zip(w_starts, w_ends):
        res = pool.apply_async(bam_cover, [bam_fn, chrom, start, end])
        results.append(res)

    segs = []
    for res in results:
        segs.append(res.get())

    segs = sorted(segs, key=itemgetter(0))
    cover = [s[1] for s in segs]

    return cover


def bam_poscover(bam_fn, chrom, start, end, pos_list):
    pass
