# Computer Aided Proximal Decaging (CAGE-Pro)

## 1. Structure Preparation

### 1.0 Building Parameter File for Ligand Molecule

Save the protein and ligand into seperate pdb files:

    grep ^ATOM complex.pdb > pro.pdb
    grep ^HETATM complex.pdb > lig.pdb

Add hydrogens using other softwares like Avogadro, and save as mol2 format. Then generate Rosetta params (Optional: you can use acpype.py to generate more accurate charge based on ambertools)

    acpype.py -i lig.mol2 -n [charge]
    convert_qm2mol2.sh lig_bcc_gaff.mol2
    /path/of/rosetta/source/scripts/python/public/molfile_to_params.py \
      -n LIG \
      --extra_torsion_output lig_bcc_gaff.mol2

### 1.1 Relax in Torsion Space
Put the protein and ligand structure into a single pdb, and relax in internal coordinates:

    cat pro.pdb LIG_0001.pdb > complex.pdb
    /path/of/rosetta/source/bin/relax.mpi.linuxgccrelease \
      -s complex.pdb \
      -extra_res_fa LIG.params \
      -relax:constrain_relax_to_start_coords \
      -ramp_constraints false \
      -relax:coord_constrain_sidechains \
      -nstruct 40 \
      -ex1 \
      -ex2 \
      -use_input_sc \
      -flip_HNQ \
      -no_optH false

### 1.2 Relax in Cartesian Space
Select the structure with the lowest score, fix the ligand with a movemap (not necessary):

    RESIDUE * BBCHI
    RESIDUE [number of ligand] NO

Relax the structure in Cartesian coordinates:

    /path/of/rosetta/source/bin/relax.mpi.linuxgccrelease \
      -s complex.pdb \
      -extra_res_fa LIG.params \
      -relax:constrain_relax_to_start_coords \
      -ramp_constraints true -relax:coord_constrain_sidechains \
      -nstruct 200 \
      -ex1 \
      -ex2 \
      -use_input_sc \
      -flip_HNQ \
      -no_optH false \
      -relax:cartesian \
      -score:weights talaris2014_cart \
      -in:file:movemap movemap \
      -crystal_refine

## 2. Pocket Localization
We define those residues proximal to the known ligand position (add correct direction) as pocket residues.

    /path/of/rosetta/source/bin/gen_lig_grids.mpi.linuxgccrelease \
      -s pro.pdb lig.pdb \
      -grid_active_res_cutoff 6.0 \
      -vector_angle_threshold 90 \
      -ignore_zero_occupancy false \
      -ignore_unrecognized_res

This app will generate pos file and grid file, we only need pos file which has all proximal residues' number.

## 3. Geometry Filter

## 4. DDG Calculation

## 5. Parsing Results
