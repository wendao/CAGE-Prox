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
    data["WT"] = []       #mono WT
    data["MUT"] = []      #mono MUT
    data["WT_OPT"] = []   #mono WT
    data["MUT_OPT"] = []  #mono MUT
    data["B_WT"] = []     #bind WT
    data["B_MUT"] = []    #bind MUT
    database[mutation] = data
    with open( mut, 'r' ) as fp:
        for line in fp.readlines():
            elems = line.split()
            if (elems[0]=="COMPLEX:"):
                if (elems[2]=="WT:"):
                    database[mutation]["B_WT"].append(float(elems[3]))
                elif (elems[2][0:3]=="MUT"):
                    database[mutation]["B_MUT"].append(float(elems[3]))
            if (elems[0]=="OPT_APART:"):
                if (elems[2]=="WT:"):
                    database[mutation]["WT_OPT"].append(float(elems[3]))
                elif (elems[2][0:3]=="MUT"):
                    database[mutation]["MUT_OPT"].append(float(elems[3]))
            if (elems[0]=="APART:"):
                if (elems[2]=="WT:"):
                    database[mutation]["WT"].append(float(elems[3]))
                elif (elems[2][0:3]=="MUT"):
                    database[mutation]["MUT"].append(float(elems[3]))

for mutation in database.keys():
    data = database[mutation]
    #print mutation
    #print data
    if len(data["MUT"])>=1:
      Efmut = np.min(data["MUT"]) #MUT unbound
      Eomut = np.min(data["MUT_OPT"]) #WT unbound opt
      Ebmut = np.min(data["B_MUT"]) #WT bound
      #print "MUT dGmut dGmut_opt"
      print "%4s %6.2f %6.2f" % (mutation, Ebmut-Efmut, Eomut-Efmut)
    else:
      Efwt = np.min(data["WT"]) #WT unbound
      Eowt = np.min(data["WT_OPT"]) #WT unbound opt
      Ebwt = np.min(data["B_WT"]) #WT bound
      print "%4s %6.2f %6.2f" % (mutation, Ebwt-Efwt, Eowt-Efwt)
