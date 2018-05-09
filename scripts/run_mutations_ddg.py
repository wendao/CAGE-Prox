import sys, os
from subprocess import *
import multiprocessing

def save_del( fn ):
    try:
        os.remove(fn)
    except OSError:
        pass

def calc_ddg( args ):
    pdb = args[0]
    resfile = args[1]
    cmd = "~/rosetta/cart_ddg/source/bin/cartesian_ddg.linuxgccrelease -s " + pdb + " -ddg::mut_file " + resfile + " -relax:min_type lbfgs_armijo_nonmonotone -ex1 -ex2 -use_input_sc -flip_HNQ -ddg:iterations 3 -mute all -unmute apps.pilot.wendao.ddg -fa_max_dis 9.0 -ddg::dump_pdbs false -bbnbr 1 -score:weights talaris2014_cart -interface_ddg 1 -extra_res_fa DC1.params DC2.params -optimization:default_max_cycles 200 -crystal_refine -relax:cartesian"
    print cmd
    return 0

def main():
    pdb = sys.argv[1]
    resfiles = open(sys.argv[2], 'r').readlines()
    args = []
    for resfile in resfiles:
        resfile = resfile.strip()
        args.append([pdb, resfile])

    #nproc = 1
    #pool = multiprocessing.Pool( processes=nproc )
    #ans = pool.map( calc_ddg, args )

    for arg in args:
        calc_ddg(arg)

main()
