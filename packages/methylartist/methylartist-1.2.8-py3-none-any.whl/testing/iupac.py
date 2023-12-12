#!/usr/bin/env python

'''
R   A or G
Y   C or T
S   G or C
W   A or T
K   G or T
M   A or C
B   C or G or T
D   A or G or T
H   A or C or T
V   A or C or G
N   any base
'''

import sys

def iupac_motif(motif):
    motif = motif.upper()

    iupac = {
        'A':['A'],
        'C':['C'],
        'G':['G'],
        'T':['T'],
        'U':['T'],
        'R':['A','G'],
        'Y':['C','T'],
        'S':['G','C'],
        'W':['A','T'],
        'K':['G','T'],
        'M':['A','C'],
        'B':['C','G','T'],
        'D':['A','G','T'],
        'H':['A','C','T'],
        'V':['A','C','G'],
        'N':['A','C','G','T']
    }

    motifs = []

    for ib in list(motif):
        if ib not in iupac:
            sys.exit('base %s not an IUPAC base, please modify --motif' % b)

        if len(motifs) == 0:
            for bp in iupac[ib]:
                motifs.append(bp)
        else:
            next_motifs = []

            for bp in iupac[ib]:
                for m in motifs:
                    next_motifs.append(m + bp)

            motifs = next_motifs

    return motifs

    print(motifs)
    print(len(motifs))


iupac_motif('CHH')
