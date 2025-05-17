import sys

def write_mutfile( pos, nat, mut_lst ):
    N = len(mut_lst)
    if N==1:
        mut = mut_lst[0]
        fp = open( "mutfiles/"+pos+mut+".mutfile", 'w' ) 
        fp.write( "total 1\n" )
        fp.write( "1\n" )
        fp.write( nat+" "+pos+" "+mut+"\n" )
        print "+pos:", pos, "nat:", nat, "mut", mut
    else:
        fp = open( "mutfiles/"+pos+"X.mutfile", 'w' ) 
        fp.write( "total %d\n" % (N) )
        for mut in mut_lst:
            fp.write( "1\n" )
            fp.write( nat+" "+pos+" "+mut+"\n" )
    fp.close()

lines = open(sys.argv[1], 'r').readlines()
for i, line in enumerate(lines):
    elems = line.split()
    pos = elems[0].strip()
    nat = elems[1].strip()
    print "-pos:", pos, "nat:", nat, "n=", i
    #write_mutfile( pos, nat, ["A", "C", "D", "E", "F", "G", "H", "I", "K", "L", "M", "N", "P", "Q", "R", "S", "T", "V", "W", "Y"] )
    write_mutfile( pos, nat, ["Y"] )
