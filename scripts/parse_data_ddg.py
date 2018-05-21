#!/usr/bin/env python
import numpy as np

mutations = []
with open( "list", 'r' ) as flist:
    for line in flist.readlines():
        fn = line.strip()
        mutations.append(fn)

database = {}
for mut in mutations:
    mutation = mut[0:-4]
    data = {}
    data["WT"] = []   #mono WT
    data["MUT"] = []  #mono MUT
    data["B_WT"] = [] #bind WT
    data["B_MUT"] = []#bind MUT
    database[mutation] = data
    with open( mut, 'r' ) as fp:
        for line in fp.readlines():
            elems = line.split()
            if (elems[0]=="BEFORE_JUMP:"):
                if (elems[2]=="WT:"):
                    database[mutation]["B_WT"].append(float(elems[3]))
                elif (elems[2][0:3]=="MUT"):
                    database[mutation]["B_MUT"].append(float(elems[3]))
            if (elems[0]=="AFTER_JUMP:"):
                if (elems[2]=="WT:"):
                    database[mutation]["WT"].append(float(elems[3]))
                elif (elems[2][0:3]=="MUT"):
                    database[mutation]["MUT"].append(float(elems[3]))

for mutation in database.keys():
    data = database[mutation]
    Efwt = np.min(data["WT"])
    Efmut = np.min(data["MUT"])
    Ebwt = np.min(data["B_WT"])
    Ebmut = np.min(data["B_MUT"])
    print "%4s %6.2f %6.2f %6.2f" % (mutation, Efmut-Efwt, Ebmut-Ebwt, (Ebmut-Efmut)-(Ebwt-Efwt)), Ebwt, Ebmut

