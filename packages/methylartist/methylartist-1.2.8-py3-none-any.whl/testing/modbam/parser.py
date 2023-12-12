#!/usr/bin/env python

import sys
import pysam
import logging

FORMAT = '%(asctime)s %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def rc(dna):
    ''' reverse complement '''
    complements = str.maketrans('acgtrymkbdhvACGTRYMKBDHV', 'tgcayrkmvhdbTGCAYRKMVHDB')
    return dna.translate(complements)[::-1]


def mods_methbam(bam_fn):
    bam = pysam.AlignmentFile(bam_fn)

    mm_warned = False

    for rec in bam.fetch():
        try:
            mm = str(rec.get_tag('Mm')).rstrip(';')
        except KeyError:
            if not mm_warned:
                logger.debug('cannot find Mm tag in at least one read, ensure this bam has Mm and Ml tags!')
                mm_warned = True
                continue
        
        mod_strings = mm.split(';')

        mods = []

        for mod_string in mod_strings:
            m = mod_string.split(',')
            mod_info = m[0]

            mod_strand = '+'
            if '-' in mod_info:
                mod_strand = '-'
            
            mod_base, mod_type = mod_info.split(mod_strand)
            mod_type = mod_type.rstrip('?.')

            mods.append(mod_type)
        
        return mods # assumes all mods are represented for each read that has an Mm tag
        

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


def parse_methbam(bam_fn, reads, chrom, start, end, motifsize=2, meth_thresh=0.8, can_thresh=0.8, restrict_motif=None, restrict_ref=None):
    bam = pysam.AlignmentFile(bam_fn)

    if restrict_ref is not None:
        restrict_ref = pysam.Fastafile(restrict_ref)

    mm_warned = False

    for rec in bam.fetch(chrom, start, end):
        if rec.is_unmapped:
            continue

        if rec.qname not in reads:
            continue

        ap = dict([(k, v) for (k, v) in rec.get_aligned_pairs() if k is not None])

        try:
            mm = str(rec.get_tag('Mm')).rstrip(';')

        except KeyError:
            if not mm_warned:
                logger.debug('cannot find Mm tag in at least one read, ensure this bam has Mm and Ml tags!')
                mm_warned = True
                continue

        try:
            ml = rec.get_tag('Ml')
        except KeyError:
            continue

        mod_strings = mm.split(';')
        mls = split_ml(mod_strings, ml)

        seq = rec.seq

        if rec.is_reverse:
            seq = rc(seq)

        for mod_string, scores in zip(mod_strings, mls):
            m = mod_string.split(',')
            mod_info = m[0]

            mod_relpos = list(map(int, m[1:]))

            mod_strand = '+'

            if '-' in mod_info:
                mod_strand = '-'

            try:
                mod_base, mod_type = mod_info.split(mod_strand)
                mod_type = mod_type.rstrip('?.')
            except ValueError:
                logger.debug('%s: malformed mod string for read %s (%s) skipped.' % (bam_fn, rec.qname, mod_info))
                continue

            assert len(mod_type) == 1, 'multiple modfications listed this way: %s is not yet supported, please send me an example!' % mod_info

            base_pos = [i for i, b in enumerate(seq) if b == mod_base]

            i = -1

            for skip, score in zip(mod_relpos, scores):
                i += 1

                if skip > 0:
                    i += skip

                genome_pos = None

                if rec.is_reverse:
                    genome_pos = ap[len(rec.seq)-base_pos[i]-1]

                    if genome_pos is None:
                        continue

                    genome_pos -= (int(motifsize)-1)

                else:
                    genome_pos = ap[base_pos[i]]

                if genome_pos is None:
                    continue

                p_mod = score/255
                p_can = 1-p_mod

                assert p_mod <= 1.0

                methstate = 0

                if p_mod > meth_thresh:
                    methstate = 1

                if p_can > can_thresh:
                    methstate = -1

                if None not in (restrict_motif, restrict_ref):
                    ref_motif = restrict_ref.fetch(rec.reference_name, genome_pos, genome_pos+2)
                    if ref_motif.upper() != restrict_motif.upper():
                        continue

                yield (rec.qname, rec.reference_name, genome_pos, p_mod, methstate, mod_type)


if len(sys.argv) == 2:
    bam = pysam.AlignmentFile(sys.argv[1])
    #ref = pysam.Fastafile('/home/data/ref/hg38/Homo_sapiens_assembly38.fasta')
    ref = pysam.Fastafile('/home/data/ref/mm10/mm10.fa')

    test_chrom='chr10'
    test_start=3100000
    test_end=4105936

    modlist = mods_methbam(sys.argv[1])

    print('mods: %s' % ','.join(modlist))

    #bcea46b8-e1fc-423a-a783-734160314d13    16      chr10   3102936

    read_names = []

    for read in bam.fetch(test_chrom, test_start, test_end):
        read_names.append(read.qname)

    print('len(read_names): %d' % len(read_names))

    for mod_rec in parse_methbam(sys.argv[1], read_names, test_chrom, test_start, test_end, motifsize=2, meth_thresh=0.8, can_thresh=0.8, restrict_motif='CG', restrict_ref='/home/data/ref/mm10/mm10.fa'):

        pos = mod_rec[2]
        ref_base = ref.fetch(test_chrom, pos, pos+2)

        print(mod_rec, ref_base)
        