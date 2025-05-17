#!/usr/bin/env python
import sys, os
from Bio import SeqIO
from Bio import pairwise2
from Bio.SubsMat import MatrixInfo
matb62 = MatrixInfo.blosum62

def load_pdb_fst(pdb):
    lines = open(pdb, 'r').readlines()
    return lines[1].strip()

def load_gene_fst(gene):
    #print "test", gene
    for seq_recored in SeqIO.parse(gene, "fasta"):
        return seq_recored.seq

########
# main #
########

pdb = sys.argv[1]
gene = sys.argv[2]

pdbseq = load_pdb_fst(pdb)
geneseq = load_gene_fst(gene)
aln = pairwise2.align.localms( pdbseq, geneseq, 2, -0.5, -5, -0.5 )
print gene, aln[0][2]
print aln[0][0]
print aln[0][1]
#print
aln_pseq = aln[0][0]
aln_gseq = aln[0][1]
#mutfile = open()
resi = 0
for i in xrange(len(aln_pseq)):
    p = aln_pseq[i]
    g = aln_gseq[i]
    if g == "-":
        print "warning: gene",gene, i
    elif p != "-":
        resi = resi + 1
        if p!=g:
            print resi, "\t", p, "->", g
            #resfile.write(str(resi)+" "+ch+" PIKAA "+g+"\n")
#resfile.close()

print
