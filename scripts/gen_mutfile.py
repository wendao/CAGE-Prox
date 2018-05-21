#!/usr/bin/env python
import sys

def write_mutfile( pos, nat, mut ):
    fp = open( "mutfiles/"+pos+mut+".mutfile", 'w' )
    fp.write( "total 1\n" )
    fp.write( "1\n" )
    fp.write( nat+" "+pos+" "+mut+"\n" )
    fp.close()
    print "+pos:", pos, "nat:", nat, "mut", mut

lines = open(sys.argv[1], 'r').readlines()
for i, line in enumerate(lines):
    elems = line.split()
    pos = elems[0].strip()
    nat = elems[1].strip()
    print "-pos:", pos, "nat:", nat, "n=", i
    write_mutfile( pos, nat, "Y" )
