#!/usr/bin/env python

import sys
import pysam

bam = pysam.AlignmentFile(sys.argv[1])
ref = pysam.Fastafile('/home/data/ref/hg38/Homo_sapiens_assembly38.fasta')
#ref = pysam.Fastafile('/home/data/ref/mm10/mm10.fa')

def rc(dna):
    ''' reverse complement '''
    complements = str.maketrans('acgtrymkbdhvACGTRYMKBDHV', 'tgcayrkmvhdbTGCAYRKMVHDB')
    return dna.translate(complements)[::-1]


def split_ml(mod_strings, ml):
    mls = []

    total_ms = sum([len(ms.split(',')[1:]) for ms in mod_strings])

    assert total_ms == len(ml), 'mod bam formatting error'

    i = 0
    for mod_string in mod_strings:
        m = mod_string.split(',')[1:] # discard first item (desc of mod base)
        mls.append(ml[i:i+len(m)])
        i += len(m)

        assert len(m) == len(mls[-1]), 'mod bam formatting error'
    
    return mls


for rec in bam.fetch(until_eof=True):
    if rec.is_unmapped:
        continue

    ap = dict([(k, v) for (k, v) in rec.get_aligned_pairs() if k is not None])

    mm = str(rec.get_tag('Mm')).rstrip(';')

    try:
        ml = rec.get_tag('Ml')
    except KeyError:
        continue 


    mod_strings = mm.split(';')
    mls = split_ml(mod_strings, ml)

    seq = rec.seq

    read_str = '+'

    if rec.is_reverse:
        seq = rc(seq)
        read_str = '-'

    for mod_string, scores in zip(mod_strings, mls):
        m = mod_string.split(',')

        mod_info = m[0]

        mod_relpos = list(map(int, m[1:]))

        mod_strand = '+'

        if '-' in mod_info:
            mod_strand = '-'

        mod_base, mod_type = mod_info.split(mod_strand)

        assert len(mod_type) == 1, 'multiple modfications listed this way: %s is not yet supported, please send me an example!' % mod_info

        base_pos = [i for i, b in enumerate(seq) if b == mod_base]

        i = -1

        for skip, score in zip(mod_relpos, scores):
            i += 1

            if skip > 0:
                i += skip

            genome_pos = ap[base_pos[i]]

            if rec.is_reverse:
                genome_pos = ap[len(rec.seq)-base_pos[i]-1]-1

            refseq = ref.fetch(rec.reference_name, genome_pos, genome_pos+2)

            p_mod = score/255
            p_can = 1-p_mod

            assert p_mod <= 1.0

            print(rec.qname, rec.reference_name, genome_pos, read_str, mod_type, p_mod, refseq, i)



