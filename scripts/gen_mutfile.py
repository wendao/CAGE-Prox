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
    write_mutfile( pos, nat, "A" )
    write_mutfile( pos, nat, "C" )
    write_mutfile( pos, nat, "D" )
    write_mutfile( pos, nat, "E" )
    write_mutfile( pos, nat, "F" )
    write_mutfile( pos, nat, "G" )
    write_mutfile( pos, nat, "H" )
    write_mutfile( pos, nat, "I" )
    write_mutfile( pos, nat, "K" )
    write_mutfile( pos, nat, "L" )
    write_mutfile( pos, nat, "M" )
    write_mutfile( pos, nat, "N" )
    write_mutfile( pos, nat, "P" )
    write_mutfile( pos, nat, "Q" )
    write_mutfile( pos, nat, "R" )
    write_mutfile( pos, nat, "S" )
    write_mutfile( pos, nat, "T" )
    write_mutfile( pos, nat, "V" )
    write_mutfile( pos, nat, "W" )
    write_mutfile( pos, nat, "Y" )
